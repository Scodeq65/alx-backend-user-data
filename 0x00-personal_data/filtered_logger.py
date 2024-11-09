#!/usr/bin/env python3
"""
filtered_logger module
"""

import re
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
) -> str:
    """Obfuscates specified fields in a log message."""
    pattern = r'({})=([^{}]*)'.format('|'.join(fields), separator)
    return re.sub(pattern, r'\1={}'.format(redaction), message)
