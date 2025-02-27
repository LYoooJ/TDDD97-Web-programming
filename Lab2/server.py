from flask import Flask, request, jsonify
import secrets
import database_helper
import string
import re

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def root():
    return "", 200

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
    if database_helper.find_user_by_email(data['email']) is not None:
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
    if search_resp is not None:
        if search_resp[1] == data['password']:
            token = generate_random_token()
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
    if token is None:
        return jsonify({"success": False, "message": "token is required."})
    
    email_resp = database_helper.get_user_email_by_token(token)
    if email_resp is not None:
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
    token = request.headers.get('Authorization')
    if token is None:
        return jsonify({"success": False, "message": "token is required."})
    
    email_resp = database_helper.get_user_email_by_token(token)
    if email_resp is not None:
        search_resp = database_helper.find_user_by_email(email_resp[0])

        ## Delete password from returned data
        user_data = list(search_resp)
        del user_data[1]
        userdata = tuple(user_data)
        return jsonify({"success": True, "message": "User data retrieved.", "data": userdata})
    else:
        return jsonify({"success": False, "message": "Invalid token."})


@app.route('/post_message', methods = ['POST'])
def post_message():
    data = request.get_json()
    # Check validity of Data
    if any(value == None or value == "" for value in data.values()):
        return jsonify({"success": False, "message": "Form data missing"})
    
    # Get and check token
    token = request.headers.get('Authorization')
    if token is None:
        return jsonify({"success": False, "message": "token is required."})

    # Validate the email of  recipient.
    resp = database_helper.find_user_by_email(data['email'])
    if resp is None:
        return jsonify({"success": False, "message": "No such user."})
    
    email_resp = database_helper.get_user_email_by_token(token)
    if email_resp is not None:
        database_helper.save_message(email_resp[0], data['email'], data['message'])
        return jsonify({"success": True, "message": "Message posted"})
    else:
        return jsonify({"success": False, "message": "Invalid token."})
    

@app.route('/get_user_messages_by_token', methods = ['GET'])
def get_user_messages_by_token():
    token = request.headers.get('Authorization')
    if token is None:
        return jsonify({"success": False, "message": "token is required."})  

    email_resp = database_helper.get_user_email_by_token(token)
    if email_resp is not None:
        search_resp = database_helper.find_messages_by_email(email_resp[0])
        return jsonify({"success": True, "message": "User messages retrieved.", 'data': search_resp})
    else:
        return jsonify({"success": False, "message": "Invalid token."})

def generate_random_token():
    letters = string.ascii_letters + string.digits
    token = "".join(secrets.choice(letters) for _ in range(36))
    return token


def validate_email(email):
    pattern = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return pattern.match(email) != None


@app.route('/get_user_data_by_email/<email>', methods = ['GET'])
def get_user_data_by_email(email):
    token = request.headers.get('Authorization')
    if token is None:
        return jsonify({"success": False, "message": "token is required."})  
    
    email_resp = database_helper.get_user_email_by_token(token)
    if email_resp is None:
        return jsonify({"success": False, "message": "Invalid token."})
    
    search_resp = database_helper.find_user_by_email(email)
    if search_resp is None:
        return jsonify({"success": False, "message": "No such User."})
    else:
        ## Delete password from returned data
        user_data = list(search_resp)
        del user_data[1]
        userdata = tuple(user_data)
        return jsonify({"success": True, "message": "User data retrieved.", "data": userdata})


@app.route('/get_user_messages_by_email/<email>', methods = ['GET'])
def get_user_message_by_email(email):
    if email is None:
        return jsonify({"success": False, "message": "Missing Email."}) 
    
    if database_helper.find_user_by_email(email) is None:
        return jsonify({"success": False, "message": "Wrong email."})
    
    token = request.headers.get('Authorization')
    if token is None:
        return jsonify({"success": False, "message": "token is required."})
    
    email_resp = database_helper.get_user_email_by_token(token)
    if email_resp is None:
        return jsonify({"success": False, "message": "Invalid token."})
    
    search_resp = database_helper.find_messages_by_email(email)
    if search_resp is None:
        return jsonify({"success": False, "message": "No such User."})
    else:
        return jsonify({"success": True, "message": "User messages retrieved.", 'data': search_resp})


@app.route('/sign_out', methods = ['DELETE'])
def sign_out():
    token = request.headers.get('Authorization')
    if token is None:
        return jsonify({"success": False, "message": "token is required."})

    email_resp = database_helper.get_user_email_by_token(token)
    if email_resp is None:
        return jsonify({"success": False, "message": "Invalid token."})
    else:
        if database_helper.delete_logged_in_user(token):
            return jsonify({"success": True, "message": "Successfully signed out."}) 
        else:
            return jsonify({"success": False, "message": "Something wrong."})


if __name__ == '__main__':
    app.debug = True
    app.run()
