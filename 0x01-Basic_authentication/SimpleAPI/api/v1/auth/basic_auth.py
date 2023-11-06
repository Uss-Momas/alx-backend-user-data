#!/usr/bin/env python3
"""basic_auth module
used for basic authentication
"""
from api.v1.auth.auth import Auth


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
