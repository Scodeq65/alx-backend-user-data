#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)

AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome():
    """
    Returns a JSON payload with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """
    POST /users endpoint to register a new user.

    Expects form data with:
        - email: user's email
        - password: user's password

    Returns:
        JSON response:
            - {"email": "<registered email>", "message": "user created"}
              if user is successfully registered.
            - {"message": "email already registered"} if user already exists.
    """
    # Get form data
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        # Register the user using AUTH
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        # Handle case where email is already registered
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
