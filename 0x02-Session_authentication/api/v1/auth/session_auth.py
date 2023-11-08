#!/usr/bin/env python3
"""session_auth module
used for session authentication
"""
from uuid import uuid4
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """SessionAuth class
    Class responsible for Session Authentication Example
    """
    def __init__(self) -> None:
        """Constructor of the class"""
        super().__init__()
        self.user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create_session method
        Args:
            - user_id: string containing the id of the user
        return:
            - uuid4 in string format
        """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
