#!/usr/bin/env python3
"""
filtered_logger module
To handle personal data
"""
import logging
import mysql.connector
import os
from typing import List
import re


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_db() -> mysql.connector.connection.MySQLConnection:
    """get_db functions
    Returns a new mysql connection connector
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", default="root")
    host = os.getenv("PERSONAL_DATA_DB_HOST", default="localhost")
    pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", default="")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    connection = mysql.connector.connection.MySQLConnection(
        host=host, user=username, password=pwd, database=db_name)
    return connection


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


def main() -> None:
    """Main function to be executed when filtered_loger is
    called
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    data = cursor.fetchall()

    cursor.close()
    db.close()
    logger = get_logger()
    for row in data:
        message = f"name={row[0]};email={row[1]};phone={row[2]};ssn={row[3]};\
password={row[4]};ip={row[5]};last_login={row[6]};user_agent={row[7]};"
        logger.info(message)


if __name__ == "__main__":
    main()
