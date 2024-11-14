#!/usr/bin/env python3
""" Basic authentication module for the API. """

from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """BasicAuth class that inherits from Auth."""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts the Base64 part of the Authorization header."""
        if (authorization_header is None or
                not isinstance(authorization_header, str)):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 part of the Authorization header.

        Parameters:
            base64_authorization_header (str): The Base64 encoded string.

        Returns:
            str: Decoded UTF-8 string if decoding is
            successful; otherwise None.
        """
        if base64_authorization_header is None or \
           not isinstance(base64_authorization_header, str):
            return None

        try:
            # Decode Base64 and convert to UTF-8
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            # Return None if decoding fails
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts the user email and password from the decoded Base64
        authorization header.

        Parameters:
            decoded_base64_authorization_header (str): The decoded Base64
            authorization header.

        Returns:
            tuple: The user email and password as a tuple, or (None, None) if
            extraction fails.
        """
        if decoded_base64_authorization_header is None or \
           not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split at the first occurrence of ':' to separate email and password
        user_email, user_password = decoded_base64_authorization_header.split(
            ':', 1
        )
        return user_email, user_password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """ Check if user_email and user_pwd are valid strings"""
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        """ Search for user by email using User.search
        """
        users = User.search({"email": user_email})

        """ Check if a user was found and validate the password
        """
        if users:
            user = users[0]
            if user.is_valid_password(user_pwd):
                return user

        # Return None if no valid user was found
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Step 1: Extract Authorization header"""
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        """ Step 2: Extract Base64 part from the header"""
        base64_auth = self.extract_base64_authorization_header(auth_header)
        if base64_auth is None:
            return None

        """ Step 3: Decode the Base64 string"""
        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if decoded_auth is None:
            return None

        """ Step 4: Extract user email and password"""
        user_email, user_pwd = self.extract_user_credentials(decoded_auth)
        if user_email is None or user_pwd is None:
            return None

        """ Step 5: Retrieve User object using email and password
        """
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
