#!/usr/bin/env python3
"""
encrypt_password module
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt with a generated salt.

    Args:
        password (str): The plain-text password to hash.

    Returns:
        bytes: The salted, hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates if a provided password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password to validate against.
        password (str): The plain-text password to check.

    Returns:
        bool: True if the password matches the hashed
        password, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
