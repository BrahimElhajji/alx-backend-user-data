#!/usr/bin/env python3
""" Module for Session Authentication """
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """Session authentication class"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for a given user ID.

        Args:
            user_id (str): The user ID to create a session for.

        Returns:
            str: The generated session ID, or None if user_id is invalid.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a user ID based on a session ID.

        Args:
            session_id (str): The session ID to retrieve the user ID for.

        Returns:
            str: The user ID if found,
            or None if session_id is invalid or not found.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)
