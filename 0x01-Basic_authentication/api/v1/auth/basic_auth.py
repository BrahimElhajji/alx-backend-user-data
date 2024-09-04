#!/usr/bin/env python3
""" Module for Basic Authentication """
import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth.
    Provides Basic Authentication mechanisms.
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization
        header for Basic Authentication.

        Args:
            authorization_header (str):
            The Authorization header from the request.

        Returns:
            str: The Base64 part of the header, or None if invalid.
        """
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 string to a UTF-8 string.

        Args:
            base64_authorization_header (str): The Base64 string to decode.

        Returns:
            str: The decoded string, or None if invalid.
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None
