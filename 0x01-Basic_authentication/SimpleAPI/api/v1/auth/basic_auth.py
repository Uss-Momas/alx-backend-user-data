#!/usr/bin/env python3
"""basic_auth module
used for basic authentication
"""
from api.v1.auth.auth import Auth
import base64
import binascii


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
        decode_base64 = decoded_base64_authorization_header.split(":")
        if len(decode_base64) != 2:
            return None, None
        # email, pwd tuple
        return tuple(decode_base64)
