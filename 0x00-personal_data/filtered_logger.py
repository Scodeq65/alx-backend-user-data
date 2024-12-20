#!/usr/bin/env python3
"""
filtered_logger module
"""

import re
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection
from typing import List, Tuple
import logging


# Define sensitive fields to redact in logs
PII_FIELDS: Tuple[str, ...] = (
    "name",
    "email",
    "phone",
    "ssn",
    "password",
)


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
) -> str:
    """Obfuscates specified fields in a log message."""
    pattern = r'({})=([^{}]*)'.format('|'.join(fields), separator)
    return re.sub(pattern, r'\1={}'.format(redaction), message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats the log record, filtering sensitive fields."""
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.getMessage(),
            self.SEPARATOR
        )
        return super().format(record)


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger to redact sensitive
    fields in logs.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Set up StreamHandler with RedactingFormatter
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    """
    Connects to a MySQL database using credentials from
    environment variables.

    Returns:
        MySQLConnection: Connection object to interact with the database.
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    if not db_name:
        raise ValueError(
            "Database name not provided in environment variables."
        )

    try:
        connection = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=db_name
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise  # Reraise the error after logging it


def main():
    """
    Main function to retrieve all users from the database
    and display their information with sensitive
    fields redacted.
    """
    logger = get_logger()
    db = get_db()

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    for user in users:
        # Constructing log message for each user with redacted data
        log_message = (
            f"name={user['name']}; "
            f"email={user['email']}; "
            f"phone={user['phone']}; "
            f"ssn={user['ssn']}; "
            f"password={user['password']}; "
            f"ip={user['ip']}; "
            f"last_login={user['last_login']}; "
            f"user_agent={user['user_agent']}"
        )
        logger.info(log_message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
