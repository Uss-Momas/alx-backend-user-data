#!/usr/bin/env python3
"""session_auth module
used for session authentication
"""
import uuid
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
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """user_id_for_session_id method
        Args:
            - session_id: uuid string key of the session
        Return:
            - user ID associated with the session
        """
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)
