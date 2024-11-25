#!/usr/bin/env python3
"""
Authentication module.
"""
from db import DB
from user import User
from bcrypt import hashpw, gensalt, checkpw


def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    if not isinstance(password, str) or not password:
        raise ValueError("Password must be a non-empty string.")
    return hashpw(password.encode('utf-8'), gensalt())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def valid_login(self, email: str, password: str) -> bool:
        """
        Check if the provided email and password match.

        Args:
            email (str): The user's email.
            password (str): The user's plain text password.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        try:
            # Find the user by email
            user = self._db.find_user_by(email=email)

            # Check if the provided password matches the stored hashed password
            if checkpw(
                password.encode('utf-8'),
                user.hashed_password.encode('utf-8')
            ):
                return True
            return False
        except Exception:
            return False

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with an email and password.

        Args:
            email (str): User's email.
            password (str): User's plain text password.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If the email is already registered.
        """
        try:
            # Check if the user already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except Exception:
            # If user is not found, proceed to create one
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password.decode('utf-8'))
