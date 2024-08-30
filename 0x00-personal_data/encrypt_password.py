#!/usr/bin/env python3
"""
Module for password hashing.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password with a random salt using bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        bytes: The salted, hashed password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed
