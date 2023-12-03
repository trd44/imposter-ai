"""
auth.py

Author: Tim Duggan
Date: 12/3/2023
Company: ImposterAI
Contact: csw73@cornell.edu

This file provides the necessary servicing for managing user interactions on a
Flask-based backend server. It includes operations such as token creation and decoding,
user registration, login, logout and also implementing the required login decorator.

It uses JWT for authentication and sqlite for database.
"""
# regin General/API Imports
import datetime
import functools
from typing import Callable

from flask import Blueprint, current_app, g, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import jwt

# endregion

# region Backend Imports
from backend.db import get_db

# endregion

bp = Blueprint("auth", __name__, url_prefix="/auth")


# region Token Related Operations
def create_token(user_id: int) -> (str, float):
    """
    Create the jwt authentication token and return it along with its expiry timestamp.

    Args:
        user_id (int): ID of User for whom the token is to be created

    Returns:
        tuple: Generated JWT Token and expiry timestamp
    """
    print(f"Creating token with user_id: {user_id}")
    token_expiry = (
        datetime.datetime.utcnow() + current_app.config["JWT_EXPIRATION_DELTA"]
    )
    token = jwt.encode(
        {"user_id": user_id, "exp": token_expiry, "iat": datetime.datetime.utcnow()},
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256",
    )

    return token, token_expiry.timestamp()


def decode_token(token: str) -> int:
    """
    Decode the jwt authentication token and return the user_id embedded in it.

    Args:
        token (str): JWT Token to be decoded

    Returns:
        int: User ID extracted from the decoded token or None if error occurred during
        decoding.
    """
    try:
        payload = jwt.decode(
            token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"]
        )
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        print("Error, token expired")
        return None
    except jwt.InvalidTokenError:
        print("Error, invalid token")
        return None


# endregion


# region User Authentication Routes
@bp.route("/register", methods=("GET", "POST"))
def register():
    """
    Register a new user with given username and password.

    Returns:
        JSON response containing JWT Token and its expiry,
        along with status code 200 on Successful registration or,
        JSON response containing error message,
        along with status code 400 or 500 in case of any error during registration.
    """
    if request.method == "POST":
        error = None
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        db = get_db()

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password are required."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (USERNAME, PASSWORD) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
                user = db.execute(
                    "SELECT * FROM users WHERE USERNAME = ?", (username,)
                ).fetchone()
            except db.IntegrityError:
                error = f"User {username} is already registered."

            if error is None:
                session.clear()
                user = dict(user)
                session["user_id"] = user["ID"]
                token, token_expiry = create_token(user["ID"])
                return (
                    jsonify(
                        {
                            "token": token
                            if isinstance(token, str)
                            else token.decode("utf-8"),
                            "token_expiry": token_expiry,
                        }
                    ),
                    200,
                )
            else:
                print("e2", error)
                return jsonify({"error": error}), 400

        print("e1", error)
        return jsonify({"error": error}), 400


@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Log in an existing user by verifying their credentials.

    Returns:
        JSON response containing JWT Token and its expiry,
        along with status code 200 on Successful login or,
        JSON response containing error message,
        along with status code 400 or 500 in case of any error during login.
    """
    if request.method == "POST":
        error = None
        try:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                error = "Username and password are required."
                return jsonify({"error": error}), 400

            db = get_db()
            user = db.execute(
                "SELECT * FROM users WHERE USERNAME = ?", (username,)
            ).fetchone()

            if user is None:
                return jsonify({"error": "Incorrect username."}), 400
            elif not check_password_hash(user["PASSWORD"], password):
                return jsonify({"error": "Incorrect password."}), 400

            session.clear()
            user = dict(user)
            session["user_id"] = user["ID"]
            token, token_expiry = create_token(user["ID"])
            return (
                jsonify(
                    {
                        "token": token
                        if isinstance(token, str)
                        else token.decode("utf-8"),
                        "token_expiry": token_expiry,
                    }
                ),
                200,
            )

        except Exception as e:
            # catch any other error
            print(e)
            return jsonify({"error": "An error occurred, please try again later."}), 500


@bp.route("/logout", methods=["POST"])
def logout() -> (str, int):
    """
    Clear the current session, including the stored 'user_id'.

    Returns:
        A response notifying the user logout and
        an HTTP status code of 200 for successful operation.
    """
    # Clear Flask's session
    session.clear()

    # Notify of logout
    return jsonify({"message": "User logged out"}), 200


@bp.before_app_request
def load_logged_in_user() -> None:
    """
    Get the current logged in user before each HTTP request within
    the application.

    If the user is not logged in, the method will set g.user to None.
    If the user is logged in, the method fetches the user's data from the database
    and assigns it to g.user.
    """

    # Fetch user id from session
    user_id = session.get("user_id")

    # Check if user_id exists
    if user_id is None:
        g.user = None
    else:
        # Fetch user's data from database using user_id and set it to g.user
        g.user = (
            get_db().execute("SELECT * FROM users WHERE ID = ?", (user_id,)).fetchone()
        )


def login_required(view: Callable) -> Callable:
    """
    Decorator function to ensure certain views require user authentication (login)
    to access.

    Args:
        view (Callable): Original view to be modified

    Returns:
        Modified view function.
    """

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        # Get the authorization header
        auth_header = request.headers.get("Authorization")

        # Check for the existence of the authorization header and the 'Bearer' keyword
        if not auth_header or "Bearer" not in auth_header:
            return jsonify({"error": "Unauthorized"}), 401

        # Extract token from "Bearer <token>"
        token = auth_header.split(" ")[1]

        # Decode token to get user_id
        user_id = decode_token(token)
        print(f"User ID: {user_id}")
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401

        # Fetch user and attach to g.user for duration of request
        g.user = (
            get_db().execute("SELECT * FROM users WHERE ID = ?", (user_id,)).fetchone()
        )

        return view(*args, **kwargs)

    return wrapped_view


# endregion
