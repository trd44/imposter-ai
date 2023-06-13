import functools
import jwt
import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from backend.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def create_token(user_id):
    payload = {
        'user_id': user_id,  # User ID to be stored in the token
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),  # Expiration time
        'iat': datetime.datetime.utcnow()  # Issued at time
    }

    token = jwt.encode(payload, 'your-secret-key', algorithm='HS256')  # Secret key should be kept safe
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, 'your-secret-key', algorithms=['HS256'])
        return payload['user_id']  # Return user ID or any information you stored in the token
    except jwt.ExpiredSignatureError:
        return None  # Signature has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        error = None
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        db = get_db()

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password are required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
                user = db.execute(
                    'SELECT * FROM user WHERE username = ?', (username,)
                ).fetchone()
            except db.IntegrityError:
                error = f"User {username} is already registered."

            if error is None:
                token = create_token(username)
                return jsonify({'token': token}), 200
            else:
                return jsonify({'error': error}), 400
        
        return jsonify({'error': error}), 400

                

@bp.route("/authdata")
def get_time():
    return{
        'Name':"Tim",
        'Age':"29",
        'Date':'x',
        "Programming":"Python"
    }

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        error = None
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                error = 'Username and password are required.'
                return jsonify({'error': error}), 400
            
            db = get_db()
            user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()

            if user is None:
                return jsonify({'error': 'Incorrect username.'}), 400
            elif not check_password_hash(user['password'], password):
                return jsonify({'error': 'Incorrect password.'}), 400

            session.clear()
            user = dict(user)
            session['user_id'] = user['id']
            # Assuming you have a function get_token that returns a token for the user
            token = create_token(user)
            return {'token': token}, 200
        
        except Exception as e:
            # catch any other error
            print('hi')
            print(e)
            return jsonify({'error': 'An error occurred, please try again later.'}), 500

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view