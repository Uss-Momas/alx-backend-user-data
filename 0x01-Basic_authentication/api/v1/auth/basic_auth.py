#!/usr/bin/env python3
"""basic_auth module
used for basic authentication
"""
from api.v1.auth.auth import Auth
from models.user import User
import base64
import binascii
from typing import TypeVar


class BasicAuth(Auth):
    """BasicAuth Class
    """

    def __init__(self) -> None:
        """Constructor"""
        super().__init__()

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract_base64_authorization_header method
        Args:
            - authorization_header: string containing the Authorizarion with
            the basic Auth token

        Returns:
            - the base64 part of the header
        """
        if not authorization_header:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """decode_base64_authorization_header method
        Args:
            - base64_authorization_header: string containing the Authorizarion
            with the basic Auth token in base 64
        Returns:
            - returns the decoded value of a Base64 string
            base64_authorization_header
        """
        if not base64_authorization_header:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            base64_bytes = base64.b64decode(base64_authorization_header)
        except binascii.Error:
            return None
        return base64_bytes.decode('utf-8')

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        extract_user_credentials method
        Args:
            - decoded_base64_authorization_header: string containing the
            decoded token
        Returns:
            - returns the user email and password from the Base64 decoded
            value
        """
        if not decoded_base64_authorization_header:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        decoded_base64 = decoded_base64_authorization_header.split(":")
        email = decoded_base64[0]
        pwd = ":".join(decoded_base64[1:])
        return email, pwd

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """user_object_from_credentials method
        Args:
            - user_email: email of the user
            - user_pwd: password of the user
        Returns:
            - returns the User instance based on his email and password.
        """
        if not user_email or type(user_email) is not str:
            return None
        if not user_pwd or type(user_pwd) is not str:
            return None
        user_list = User.search({"email": user_email})
        if len(user_list) == 0:
            return None
        user = user_list[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """current_user method
        Args:
            - request: request object
        Returns:
            - a user object
        """
        authorization = self.authorization_header(request)
        base64_token = self.extract_base64_authorization_header(authorization)
        decoded_base64 = self.decode_base64_authorization_header(base64_token)
        user_email, user_pwd = self.extract_user_credentials(decoded_base64)
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
