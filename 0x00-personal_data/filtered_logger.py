#!/usr/bin/env python3
"""
Module for filtering log messages.
"""

import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates certain fields in a log message.

    Args:
        fields (List[str]): The list of fields to obfuscate.
        redaction (str): The string to replace the field values with.
        message (str): The original log message.
        separator (str): The character separating fields in the log message.

    Returns:
        str: The obfuscated log message.
    """
    for field in fields:
        message = re.sub(
            rf"{field}=.*?{separator}",
            f"{field}={redaction}{separator}",
            message
        )
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the RedactingFormatter.

        Args:
            fields (List[str]): A list of field names to be obfuscated
            in log messages.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the specified record as text.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log message with sensitive fields obfuscated.
        """
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            original_message, self.SEPARATOR)
