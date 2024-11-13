#!/usr/bin/env python3
""" Authentication module for the API.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class to manage API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if a path requires authentication.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths that
            don't require authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True

        # Normalize path by ensuring it ends with a slash for comparison
        normalized_path = path if path.endswith('/') else path + '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('/'):
                if normalized_path == excluded_path:
                    return False
            elif normalized_path == excluded_path + '/':
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Retrieves the authorization header from the request.

        Args:
            request (Flask request): The request object.

        Returns:
            str: None, as this is just a template for now.
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the current user.

        Args:
            request (Flask request): The request object.

        Returns:
            TypeVar('User'): None, as this is just a template for now.
        """
        return None
