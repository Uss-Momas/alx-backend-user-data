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
    msg = []
    for k_val in message.split(separator):
        att = sub(r"[^{}=].*".format(k_val.split("=")[0]), redaction,
                  k_val) if k_val.split("=")[0] in fields else k_val
        msg.append(att)
    return ";".join(msg)
