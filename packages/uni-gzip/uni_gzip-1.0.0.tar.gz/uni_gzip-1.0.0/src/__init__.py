"""
Uni Gzip - A unified Python library for reading and writing gzip-compressed JSON and text files.

This package provides utilities for:
- Reading gzip-compressed JSON files
- Writing data to gzip-compressed JSON files
- Reading gzip-compressed text files
- Writing text content to gzip-compressed files
- Automatic UTF-8 encoding handling
- Compact JSON format for efficient storage
"""

import logging

from .exceptions import UniGzipError, UniGzipJsonError, UniGzipJsonReadError, UniGzipJsonWriteError, UniGzipTxtError, UniGzipTxtReadError, UniGzipTxtWriteError
from .uni_gzip import readJsonGz, readTxtGz, writeJsonGz, writeTxtGz

__version__ = "1.0.0"

# Configure library root logger
# Use NullHandler to ensure library remains silent when user hasn't configured logging
# If user configures logging (e.g., logging.basicConfig()), logs will bubble up to root logger for processing
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__all__ = [
    "readJsonGz",
    "writeJsonGz",
    "readTxtGz",
    "writeTxtGz",
    "UniGzipError",
    "UniGzipJsonError",
    "UniGzipJsonReadError",
    "UniGzipJsonWriteError",
    "UniGzipTxtError",
    "UniGzipTxtReadError",
    "UniGzipTxtWriteError",
]
