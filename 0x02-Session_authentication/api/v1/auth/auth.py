#!/usr/bin/env python3
"""auth module
used for basic authentication
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Class Auth - Implementation of Basic Authentication
    """
    def __init__(self) -> None:
        """Constructor method"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require_auth
        Args:
            - path: string
            - excluded_paths: list of strings
        Returns:
            - boolean value
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        new_path = list(path)
        if new_path[-1] != "/":
            new_path.append("/")
        new_path = "".join(new_path)
        # Returns True if the path is not in the excluded_paths
        # Returns False if the path is in the excluded_paths
        return new_path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """ authorization_header method
        Args:
            - request: Flask request object
        Returns:
            - a string
        """
        # if request is None
        if not request:
            return None
        header = request.headers
        if not header.get("Authorization"):
            return None
        return header.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """current_user method
        Args:
            - request: Flask request object
        Returns:
            - User object
        """
        return None

    def session_cookie(self, request=None):
        """session_cookie method
        Args:
            - request: request object
        Returns:
            - a cookie value from a request
        """
        if not request:
            return None
        print(request.cookies)
        return request.cookies.get(os.getenv('SESSION_NAME'))
