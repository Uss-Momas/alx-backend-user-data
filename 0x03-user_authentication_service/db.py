#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
# from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """add user method
        Args:
            - user email
            - user hashed password
        """
        new_session = self._session
        user = User()
        user.email = email
        user.hashed_password = hashed_password
        new_session.add(user)
        new_session.commit()
        return user

    def find_user_by(self, **kwargs: dict) -> User:
        """Find a specific user
        Args:
            - kwargs: key named values dictionaires
        """
        session = self._session
        for key, value in kwargs.items():
            if hasattr(User, key) is None:
                raise InvalidRequestError
        user = session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs: dict) -> None:
        """update user method
        Args:
            - user_id
        """
        for key in kwargs.keys():
            if hasattr(User, key) is None:
                raise ValueError
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        session = self._session
        session.add(user)
        session.commit()
