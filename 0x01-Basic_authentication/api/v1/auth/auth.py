#!/usr/bin/env python3
""" Authentication module for the API.
"""
from flask import request
from typing import List, TypeVar

class Auth:
    """Auth class to manage API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if a path requires authentication.
        Currently returns False as authentication is not implemented yet.
        
        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths that don't require authentication.
        
        Returns:
            bool: False for now, indicating no path requires authentication.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Retrieves the authorization header from the request.
        
        Args:
            request (Flask request): The request object.
        
        Returns:
            str: None, as this is just a template for now.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the current user.
        
        Args:
            request (Flask request): The request object.
        
        Returns:
            TypeVar('User'): None, as this is just a template for now.
        """
        return None
