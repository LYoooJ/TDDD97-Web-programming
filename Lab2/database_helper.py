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
        get_db().execute("insert into loggedInUsers values(?, ?);", [email, token])
        get_db().commit()
        return True
    except Exception as e:
        return False

def get_userdata_by_token(token):
    cursor = get_db().execute("select * from loggedInUser where token = ?;", [token])
    email = cursor.fetchone()
    cursor.close()
    return find_user_by_email(email)
