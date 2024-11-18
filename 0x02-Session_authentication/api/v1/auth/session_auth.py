#!/usr/bin/env python3
""" Session Authentication module """
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """ SessionAuth class that inherits from Auth """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id """
        if user_id is None or type(user_id) is not str:
            return None

        # Generate a new session ID using uuid4()
        session_id = str(uuid.uuid4())

        # Store the session ID and corresponding user ID in the distionary
        self.user_id_by_session_id[session_id] = user_id

        return session_id
