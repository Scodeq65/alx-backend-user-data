#!/usr/bin/env python3
""" Session Authentication module """
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ SessionAuth class that inherits from Auth """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id.

        Args:
            user_id (str): The user ID.

        Returns:
            str: The session ID, or None if user_id is invalid.
        """
        if user_id is None or type(user_id) is not str:
            return None

        # Generate a new session ID using uuid4()
        session_id = str(uuid.uuid4())

        # Store the session ID and corresponding user ID in the dictionary
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns the user ID based on the session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user ID, or None if session_id is invalid or not found.
        """
        if session_id is None or type(session_id) is not str:
            return None

        # Return the user ID associated with the session ID
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieves the current User instance based on a session cookie.

        Args:
            request: The HTTP request object (optional).

        Returns:
            User instance corresponding to the session ID,
            or None if no valid session or user is found.
        """
        # Get the session ID from the cookie
        session_id = self.session_cookie(request)

        if not session_id:
            return None

        # Retrieve the user ID associated with the session ID
        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return None

        # Fetch and return the User instance from the database
        try:
            return User.get(user_id)
        except Exception:
            return None
