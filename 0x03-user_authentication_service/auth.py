#!/usr/bin/env python3
"""
Authentication module.
"""
from db import DB
from user import User
from bcrypt import hashpw, gensalt


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
            """ Check if the user already exists"""
            self._db.find_user_by(email=email)
            # If the user is found, raise a ValueError
            raise ValueError(f"User {email} already exists")
        except Exception:
            pass

        """ Hash the password and create the user"""
        hashed_password = _hash_password(password)
        return self._db.add_user(email, hashed_password)
