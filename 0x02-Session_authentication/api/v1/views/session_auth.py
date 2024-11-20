#!/usr/bin/env python3
""" Handles all routes for Session Authentication """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth_login():
    """
    POST /auth_session/login
    Handles login using Session Authentication
    """
    # Get email and password from the form
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email is missing
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Check if password is missing
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Search for a user by email
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    # Ensure only one user is found
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    # Validate the password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a session ID for the user
    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    # Prepare the response
    response = jsonify(user.to_json())

    # Set the session ID in the cookie
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response
