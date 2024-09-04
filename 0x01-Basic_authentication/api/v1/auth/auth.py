#!/usr/bin/env python3
""" Module for API authentication management """
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class to manage API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for a given path.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that
            do not require authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True

        if not excluded_paths:
            return True

        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('/') and path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the request.

        Args:
            request: The Flask request object.

        Returns:
            str: None for now; will return the Authorization
            header if present in the request.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request.

        Args:
            request: The Flask request object.

        Returns:
            TypeVar('User'): None for now; will return the current
            user if authenticated.
        """
        return None
