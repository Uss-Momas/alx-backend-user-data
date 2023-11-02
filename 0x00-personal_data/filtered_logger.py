#!/usr/bin/env python3
"""
filtered_logger module
To handle personal data
"""
from typing import List
from re import sub


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """filter_datum function retuns a obsfucated log message"""
    for field in fields:
        replicate = f"{field}={redaction}{separator}"
        message = sub(f"{field}=.*?{separator}", replicate, message)
    return message
