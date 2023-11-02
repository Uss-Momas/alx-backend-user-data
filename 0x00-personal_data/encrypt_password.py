#!/usr/bin/env python3
"""
encrypt_password module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    hash_password function
    Args:
        - password: the message to be hashed
    Return:
        - a salted, hashed password of byte string
    """
    hashed = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    is_valid function expects 2 arguments and returns a boolean.
    Args:
        - hashed_password: bytes type
        - password: string type
    Return:
        - boolean value indicating if password is valida or not
    """
    return bcrypt.checkpw(bytes(password, 'utf-8'), hashed_password)
