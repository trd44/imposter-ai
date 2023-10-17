import datetime
import functools

from flask import (
    Blueprint, current_app, g, jsonify, request, session
)
from werkzeug.security import check_password_hash, generate_password_hash
import jwt

from backend.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


def create_token(user_id):
    """Create the jwt authentication token and return it."""
    print(f"Creating token with user_id: {user_id}")
    token_expiry = datetime.datetime.utcnow() + current_app.config['JWT_EXPIRATION_DELTA']
    token = jwt.encode({
        'user_id': user_id,
        'exp': token_expiry,
        'iat': datetime.datetime.utcnow()
    }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

    return token, token_expiry.timestamp()


def decode_token(token):
    """Decode the jwt authentication token and return the user_id"""
    try:
        payload = jwt.decode(
            token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        print("Error, token expired")
        return None
    except jwt.InvalidTokenError:
        print("Error, invalid token")
        return None


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Register a new user"""
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
                    "INSERT INTO users (USERNAME, PASSWORD) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
                user = db.execute(
                    'SELECT * FROM users WHERE USERNAME = ?', (username,)
                ).fetchone()
            except db.IntegrityError:
                error = f"User {username} is already registered."

            if error is None:
                session.clear()
                user = dict(user)
                session['user_id'] = user['ID']
                token, token_expiry = create_token(user['ID'])
                return jsonify({'token': token if isinstance(token, str) else token.decode('utf-8'), 'token_expiry': token_expiry}), 200
            else:
                print("e2", error)
                return jsonify({'error': error}), 400

        print("e1", error)
        return jsonify({'error': error}), 400


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Log in a registered user"""
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
                'SELECT * FROM users WHERE USERNAME = ?', (username,)
            ).fetchone()

            if user is None:
                return jsonify({'error': 'Incorrect username.'}), 400
            elif not check_password_hash(user['PASSWORD'], password):
                return jsonify({'error': 'Incorrect password.'}), 400

            session.clear()
            user = dict(user)
            session['user_id'] = user['ID']
            token, token_expiry = create_token(user['ID'])
            return jsonify({'token': token if isinstance(token, str) else token.decode('utf-8'), 'token_expiry': token_expiry}), 200

        except Exception as e:
            # catch any other error
            print(e)
            return jsonify({'error': 'An error occurred, please try again later.'}), 500


@bp.route('/logout', methods=['POST'])
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return jsonify({'message': 'User logged out'}), 200


@bp.before_app_request
def load_logged_in_user():
    """Get the current logged in user"""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE ID = ?', (user_id,)
        ).fetchone()


def login_required(view):
    """Login required decorator"""
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or 'Bearer' not in auth_header:
            print("Error, unauthorized")
            return jsonify({"error": "Unauthorized"}), 401

        # Extract token from "Bearer <token>"
        token = auth_header.split(' ')[1]

        user_id = decode_token(token)  # Decode token to get user_id
        print(f"User ID: {user_id}")
        if not user_id:
            print("Error, invalid or expired token")
            return jsonify({"error": "Invalid or expired token"}), 401

        # Fetch user and attach to g.user for duration of request
        g.user = get_db().execute(
            'SELECT * FROM users WHERE ID = ?', (user_id,)
        ).fetchone()

        return view(*args, **kwargs)
    return wrapped_view
