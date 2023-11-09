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
    user_id_by_session_id = {}

    def __init__(self) -> None:
        """Constructor of the class"""
        super().__init__()

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

    def current_user(self, request=None):
        """current_user method overloaded from Auth
        Args:
            - request
        Returns:
            - current user found
        """
        from models.user import User
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """destroys current session id"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
