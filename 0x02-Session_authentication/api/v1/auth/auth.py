#!/usr/bin/env python3
""" Module for API authentication management """
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class to manage API authentication."""

    def session_cookie(self, request=None):
        """
        Returns the value of a session cookie from the request.

        Args:
            request (flask.Request): The Flask request object.

        Returns:
            str: The value of the session cookie,
            or None if the cookie is not found or request is None.
        """
        if request is None:
            return None

        cookie_name = os.getenv('SESSION_NAME', '_my_session_id')

        return request.cookies.get(cookie_name)

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for a given path.
        """
        if path is None:
            return True
        if not excluded_paths:
            return True
        if not path.endswith('/'):
            path += '/'
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the request.

        Args:
            request: The Flask request object.

        Returns:
            str: The Authorization header if present, None otherwise.
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request.
        """
        return None
