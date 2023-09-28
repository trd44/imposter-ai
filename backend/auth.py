import functools
import jwt
import datetime
import os

from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from backend.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


def create_token(user_id):
    token_expiry = datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=1)

    token = jwt.encode({
        'user_id': user_id,
        'exp': token_expiry,
        'iat': datetime.datetime.utcnow()
    }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

    return token, token_expiry.timestamp()


# def create_token(user_id):
#     token_expiry = datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5)

#     token = jwt.encode({
#         'user_id': user_id,
#         'exp': token_expiry,
#         'iat': datetime.datetime.utcnow()
#     }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

#     return jsonify({'token': token, 'token_expiry': token_expiry.timestamp()}), 200

    # payload = {
    #     'user_id': user_id,  # User ID to be stored in the token
    #     'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),  # Expiration time
    #     'iat': datetime.datetime.utcnow()  # Issued at time
    # }

    # token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')  # Secret key should be kept safe
    # return token

def decode_token(token):
    try:
        payload = jwt.decode(
            token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        # Return user ID or any information you stored in the token
        return payload['user_id']
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
                session.clear()
                user = dict(user)
                session['user_id'] = user['id']
                token, token_expiry = create_token(user['id'])
                return jsonify({'token': token if isinstance(token, str) else token.decode('utf-8'), 'token_expiry': token_expiry}), 200
            else:
                print("e2", error)
                return jsonify({'error': error}), 400

        print("e1", error)
        return jsonify({'error': error}), 400


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
            token, token_expiry = create_token(user['id'])
            return jsonify({'token': token if isinstance(token, str) else token.decode('utf-8'), 'token_expiry': token_expiry}), 200

        except Exception as e:
            # catch any other error
            print('hi')
            print(e)
            return jsonify({'error': 'An error occurred, please try again later.'}), 500

@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'User logged out'}), 200

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))

#         return view(**kwargs)

#     return wrapped_view

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or 'Bearer' not in auth_header:
            return jsonify({"error": "Unauthorized"}), 401
        
        token = auth_header.split(' ')[1]  # Extract token from "Bearer <token>"
        
        user_id = decode_token(token)  # Decode token to get user_id
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Fetch user and attach to g.user for duration of request
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

        return view(*args, **kwargs)
    return wrapped_view
