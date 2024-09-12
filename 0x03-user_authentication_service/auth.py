#!/usr/bin/env python3
"""
Auth module
"""
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user with the given email and password.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            User: The newly created user object.

        Raises:
            ValueError: If a user with the provided email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(
                    email, hashed_password.decode('utf-8'))
            return new_user
