#!/usr/bin/env python3
"""
Authentication module for password hashing.
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        bytes: The salted hash of the password.

    Raises:
        ValueError: If the password is not a non-empty string.
    """
    if not isinstance(password, str) or not password:
        raise ValueError("Password must be a non-empty string.")

    # Generate a salted hash of the password
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
