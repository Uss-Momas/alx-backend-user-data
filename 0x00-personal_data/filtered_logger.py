#!/usr/bin/env python3
"""
filtered_logger module
"""
from typing import List
from re import sub


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    filter_datum function
    Args:
        - fields: list of strings representing all fields to obfuscate
        - redaction: string representing by what the field will be obfuscated
        - message: string representing the log line
        - separator: string representing by which character is separating all
        fields in the log line (message)
    Returns:
        - log message obfuscated
    """
    for field in fields:
        replicate = f"{field}={redaction}{separator}"
        message = sub(f"{field}=.*?{separator}", replicate, message)
    return message
