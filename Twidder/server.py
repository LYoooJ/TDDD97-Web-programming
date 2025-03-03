from flask import Flask, request, jsonify
import secrets
import database_helper
import string
import re
from flask_sock import Sock

app = Flask(__name__, static_folder='static')
sock = Sock(app)

logged_in_users = {}

@app.route("/", methods = ['GET'])
def root():
    return app.send_static_file('client.html')

@sock.route('/connect')
def connect_user(ws):
    token = ws.receive()
    email_resp = database_helper.get_user_email_by_token(token)
    if email_resp != None:
        logged_in_users[(email_resp[0], token)] = ws

    try:
        while True:
            message = ws.receive()
            ws.send(message)
    finally:
        if (email_resp[0], token) in logged_in_users:
            del logged_in_users[(email_resp[0], token)]

def check_and_logout_user(email):
    token = next((key[1] for key in logged_in_users if key[0] == email), None)
    if token != None:
        socket = logged_in_users[(email, token)]
        socket.send("user logout")
        socket.close()
        del logged_in_users[(email, token)]
        
@app.teardown_request
def teardown(exception):
    database_helper.disconnect()

@app.route('/sign_up', methods = ['POST'])
def sign_up():
    data = request.get_json()
    # Check validity of Data
    if any(value == None or value == "" for value in data.values()):
        return jsonify({"success": False, "message": "Form data missing"})

    # Check validity of Email
    if validate_email(data['email']) is False:
        return jsonify({"success": False, "message": "Wrong email"})

    # Check password length
    if len(data['password']) <8:
        return jsonify({"success": False, "message": "password length"})
    
    # Check if user already exist
    if database_helper.find_user_by_email(data['email']) != None:
        return jsonify({"success": False, "message": "User already exists."})
    else:
        resp = database_helper.create_user(data['email'], data['password'], data['firstname'], data['familyname'], data['gender'], data['city'], data['country'])
        if resp:
            return jsonify({"success": True, "message": "Successfully created a new user."})
        else:
            return jsonify({"success": False, "message": "Failed to create a new user."})


@app.route('/sign_in', methods = ['POST'])
def sign_in():
    data = request.get_json()

    # Check validity of Data
    if any(value == None or value == "" for value in data.values()):
        return jsonify({"success": False, "message": "Form data missing"})
    
    # Check if user with the email exists
    search_resp = database_helper.find_user_by_email(data['username'])
    if search_resp != None:
        if search_resp[1] == data['password']:
            token = generate_random_token()
            check_and_logout_user(data['username'])
            resp = database_helper.save_token_info(data['username'], token)
            if resp:
                return jsonify({"success": True, "message": "Successfully signed in", "data": token})
            else:
                return jsonify({"success": False, "message": "Error"})
        else:
            return jsonify({"success": False, "message": "Wrong password"})
    else:
        return jsonify({"success": False, "message": "Wrong Email"})


@app.route('/change_password', methods = ['PUT'])
def change_password():
    data = request.get_json()
    # Check validity of Data
    if any(value == None or value == "" for value in data.values()):
        return jsonify({"success": False, "message": "Form data missing"})
    
    token = request.headers.get('Authorization')
    if token == None:
        return jsonify({"success": False, "message": "token is required."})
    
    email_resp = database_helper.get_user_email_by_token(token)
    if email_resp != None:
        search_resp = database_helper.find_user_by_email(email_resp[0])
        if search_resp[1] == data['oldpassword']:
            update_resp = database_helper.update_password(data['newpassword'], email_resp[0])
            if update_resp:
                return jsonify({"success": True, "message": "Password changed."})
            else:
                return jsonify({"success": False, "message": "Something wrong."})
        else:
            return jsonify({"success": False, "message": "Wrong password."})
    else:
        return jsonify({"success": False, "message": "Invalid token."})


@app.route('/get_user_data_by_token', methods = ['GET'])
def get_user_data_by_token():
     if request.method != 'GET':
        return jsonify({"success": False, "message": "Method not allowed"}), 405
     try:
        token = request.headers.get('Authorization')
        if token == None:
            return jsonify({"success": False, "message": "token is required."}), 401
        
        email_resp = database_helper.get_user_email_by_token(token)
        if email_resp != None:
            search_resp = database_helper.find_user_by_email(email_resp[0])

            ## Delete password from returned data
            user_data = list(search_resp)
            del user_data[1]
            userdata = tuple(user_data)
            return jsonify({"success": True, "message": "User data retrieved.", "data": userdata}), 200
        else:
            return jsonify({"success": False, "message": "Invalid token."}), 401
     except Exception as e:
        return jsonify({"success": False, "message": "Internal Server Error"}), 500             



@app.route('/post_message', methods = ['POST'])
def post_message():
    if request.method != 'POST':
        return jsonify({"success": False, "message": "Method not allowed"}), 405
    try:
        data = request.get_json()
        # Check validity of Data
        if any(value == None or value == "" for value in data.values()):
            return jsonify({"success": False, "message": "data missing"}), 400
        
        # Get and check token
        token = request.headers.get('Authorization')
        if token == None:
            return jsonify({"success": False, "message": "token is required."}), 401

        # Validate the email of  recipient.
        resp = database_helper.find_user_by_email(data['email'])
        if resp == None:
            return jsonify({"success": False, "message": "No such user."}), 400
        
        email_resp = database_helper.get_user_email_by_token(token)
        if email_resp != None:
            database_helper.save_message(email_resp[0], data['email'], data['message'])
            return jsonify({"success": True, "message": "Message posted"}), 201
        else:
            return jsonify({"success": False, "message": "Invalid token."}), 401
    except Exception as e:
            return jsonify({"success": False, "message": "Internal Server Error"}), 500
    
    

@app.route('/get_user_messages_by_token', methods = ['GET'])
def get_user_messages_by_token():
    if request.method != 'GET':
        return jsonify({"success": False, "message": "Method not allowed"}), 405
    try:
        token = request.headers.get('Authorization')
        if token == None:
            return jsonify({"success": False, "message": "token is required."}), 401 

        email_resp = database_helper.get_user_email_by_token(token)
        if email_resp != None:
            search_resp = database_helper.find_messages_by_email(email_resp[0])
            return jsonify({"success": True, "message": "User messages retrieved.", 'data': search_resp}), 200
        else:
            return jsonify({"success": False, "message": "Invalid token."}), 401
    except Exception as e:
        return jsonify({"success": False, "message": "Internal Server Error"}), 500    


def generate_random_token():
    letters = string.ascii_letters + string.digits
    token = "".join(secrets.choice(letters) for _ in range(36))
    return token


def validate_email(email):
    pattern = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return pattern.match(email) != None


@app.route('/get_user_data_by_email/<email>', methods = ['GET'])
def get_user_data_by_email(email):
    if request.method != 'GET':
        return jsonify({"success": False, "message": "Method not allowed"}), 405
    try:
        token = request.headers.get('Authorization')
        if token == None:
            return jsonify({"success": False, "message": "token is required."}), 401 
        
        email_resp = database_helper.get_user_email_by_token(token)
        if email_resp == None:
            return jsonify({"success": False, "message": "Invalid token."}), 401
        
        search_resp = database_helper.find_user_by_email(email)
        if search_resp == None:
            return jsonify({"success": False, "message": "No such User."}), 404
        else:
            ## Delete password from returned data
            user_data = list(search_resp)
            del user_data[1]
            userdata = tuple(user_data)
            return jsonify({"success": True, "message": "User data retrieved.", "data": userdata}), 200
    except Exception as e:
        return jsonify({"success": False, "message": "Internal Server Error"}), 500     



@app.route('/get_user_messages_by_email/<email>', methods = ['GET'])
def get_user_message_by_email(email):
    if request.method != 'GET':
        return jsonify({"success": False, "message": "Method not allowed"}), 405
    try:
        if email == None:
            return jsonify({"success": False, "message": "Missing Email."}) , 400
    
        if database_helper.find_user_by_email(email) == None:
            return jsonify({"success": False, "message": "No such User."}), 400
            
        token = request.headers.get('Authorization')
        if token == None:
            return jsonify({"success": False, "message": "token is required."}), 401
            
        email_resp = database_helper.get_user_email_by_token(token)
        if email_resp == None:
            return jsonify({"success": False, "message": "Invalid token."}), 401
            
        search_resp = database_helper.find_messages_by_email(email)
        if search_resp == None:
            return jsonify({"success": False, "message": "No message."}), 404
        else:
            return jsonify({"success": True, "message": "User messages retrieved.", 'data': search_resp}), 200
    except Exception as e:
        return jsonify({"success": False, "message": "Internal Server Error"}), 500



@app.route('/sign_out', methods = ['DELETE'])
def sign_out():
    token = request.headers.get('Authorization')
    if token == None:
        return jsonify({"success": False, "message": "token is required."})

    email_resp = database_helper.get_user_email_by_token(token)
    if email_resp == None:
        return jsonify({"success": False, "message": "Invalid token."})
    else:
        if database_helper.delete_logged_in_user(token):
            if any(key[0] == email_resp[0] for key in logged_in_users):
                ws = logged_in_users[(email_resp[0], token)]
                ws.close()
                del logged_in_users[(email_resp[0], token)]
            return jsonify({"success": True, "message": "Successfully signed out."}) 
        else:
            return jsonify({"success": False, "message": "Something wrong."})

# if __name__ == '__main__':
#     app.debug = True
#     app.run()