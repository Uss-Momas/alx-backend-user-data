#!/usr/bin/env python3
"""
filtered_logger module
To handle personal data
"""
import logging
from typing import List
import re


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """filter_datum function retuns a obsfucated log message
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
        message = re.sub(f"{field}=.*?{separator}", replicate, message)
    return message


def get_logger() -> logging.Logger:
    """get_logger function
    returns a logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)
    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """RedactingFormatter logging Constructor
        Params:
            - fields: fields to be redacted
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format method -> Filter values in incoming log records
        using filter_datum
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
