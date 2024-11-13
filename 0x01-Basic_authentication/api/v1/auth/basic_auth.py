#!/usr/bin/env python3
""" Basic authentication module for the API. """

from api.v1.auth.auth import Auth
import base64


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