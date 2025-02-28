import sqlite3
from flask import g

DATABASE_URI = "database.db"

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = sqlite3.connect(DATABASE_URI)
    
    return db

def disconnect():
    db = getattr(g, 'db', None)
    if db is not None:
        g.db.close()
        g.db = None

def create_user(email, password, firstName, familyName, gender, city, country):
    try:
        get_db().execute("insert into userinfo values(?, ?, ?, ?, ?, ?, ?);", [email, password, firstName, familyName, gender, city, country])
        get_db().commit()
        return True
    except Exception as e:
        return False

def find_user_by_email(email) -> tuple:
    cursor = get_db().execute("select * from userinfo where email = ?;", [email])
    userdata = cursor.fetchone()
    cursor.close()
    return userdata
    
def save_token_info(email, token) -> None:
    try:
        get_db().execute("insert or replace into loggedInUsers values(?, ?);", [email, token])
        get_db().commit()
        return True
    except Exception as e:
        return False

def get_user_email_by_token(token):
    cursor = get_db().execute("select * from loggedInUsers where token = ?;", [token])
    email = cursor.fetchone()
    cursor.close()
    return email

def get_user_token_login_by_email(email):
    cursor = get_db().execute("select * from loggedInUsers where email = ?;", [email])
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[1]
    else:
        return None

def find_messages_by_email(email):
    cursor = get_db().execute("select * from messages where toemail = ?;", [email])
    messages = cursor.fetchall()
    cursor.close()
    return messages
   
def update_password(newpassword, email):
    try:
        get_db().execute("update userinfo set password = ? where email = ?;", [newpassword, email])
        get_db().commit()
        return True
    except Exception as e:
        return False
    
def save_message(fromemail, toemail, msg):
    try:
        get_db().execute("insert into messages values(?, ?, ?);", [fromemail, toemail, msg])
        get_db().commit()
        return True
    except Exception as e:
        return False
    
def delete_logged_in_user(token):
    try:
        get_db().execute("delete from loggedInUsers where token = ?;", [token])
        get_db().commit()
        return True
    except Exception as e:
        return False    