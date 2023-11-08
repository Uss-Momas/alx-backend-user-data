#!/usr/bin/env python3
"""session_auth module
used for session authentication
"""
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """SessionAuth class
    Class responsible for Session Authentication Example
    """
    def __init__(self) -> None:
        super().__init__()
