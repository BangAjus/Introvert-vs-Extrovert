from flask import session
from database.config import get_db

def login_user(username, password):

    db = get_db()

    with db.cursor() as cursor:

        query = """
                SELECT 
                    id,
                    username 
                FROM users
                WHERE username=%s AND password=%s
                """
        cursor.execute(query, 
                       (username, password))
        user = cursor.fetchone()

    if user:

        session['user_id'] = user['id']
        session['username'] = user['username']

        return True
    
    return False

def is_logged_in():
    return 'user_id' in session

def logout_user():
    
    session.pop('user_id', None)
    session.pop('username', None)
