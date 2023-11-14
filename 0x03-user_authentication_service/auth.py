#!/usr/bin/env python3
"""auth module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """function to hash password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """_generate_uuid generates a uuid
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        """Constructor of the class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register_user method used to add new user
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            pwd = _hash_password(password)
            return self._db.add_user(email, pwd)
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """valid_login method
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        encoded_pwd = password.encode('utf-8')
        return bcrypt.checkpw(encoded_pwd, user.hashed_password)

    def create_session(self, email: str) -> str:
        """create_session returns session id as string
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id
