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
