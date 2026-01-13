"""
Unified Gzip Processing Module

Provides utilities for reading and writing gzip-compressed JSON and text files.
All operations use UTF-8 encoding. JSON files use compact format (no spaces, no ASCII escaping).
"""

import gzip
import json
import logging
from pathlib import Path
from typing import Any, Iterable, Union

from .exceptions import UniGzipJsonReadError, UniGzipJsonWriteError, UniGzipTxtReadError, UniGzipTxtWriteError

logger = logging.getLogger(__name__)


def readJsonGz(path: Union[str, Path]) -> Any:
    """
    Read a gzip-compressed JSON file.

    Opens the file in text mode with UTF-8 encoding, decompresses it,
    and parses the JSON content.

    Args:
        path: Path to the gzip-compressed JSON file (str or Path).

    Returns:
        Parsed JSON data (dict, list, or other JSON-serializable types).

    Raises:
        UniGzipJsonReadError: If reading fails due to:
            - File not found
            - Invalid gzip format
            - JSON parsing errors
            - I/O errors
    """
    path_str = str(path)
    try:
        with gzip.open(path_str, "rt", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise UniGzipJsonReadError(f"File not found: {path_str}", file_path=path_str) from e
    except gzip.BadGzipFile as e:
        raise UniGzipJsonReadError(f"Invalid gzip format: {path_str}", file_path=path_str) from e
    except json.JSONDecodeError as e:
        raise UniGzipJsonReadError(f"JSON parsing error in {path_str}: {e}", file_path=path_str) from e
    except OSError as e:
        raise UniGzipJsonReadError(f"I/O error reading {path_str}: {e}", file_path=path_str) from e
    except Exception as e:
        raise UniGzipJsonReadError(f"Unexpected error reading {path_str}: {e}", file_path=path_str) from e


def writeJsonGz(path: Union[str, Path], data: Any) -> None:
    """
    Write data to a gzip-compressed JSON file.

    Serializes the data to JSON and writes it as a gzip-compressed file
    in text mode with UTF-8 encoding. Uses compact JSON format (no spaces,
    no ASCII escaping) for efficient storage.

    Args:
        path: Path to the output file (str or Path).
        data: Data to serialize (must be JSON-serializable).

    Raises:
        UniGzipJsonWriteError: If writing fails due to:
            - Permission denied
            - Disk space issues
            - I/O errors
        TypeError: If data is not JSON-serializable.
    """
    path_str = str(path)
    try:
        with gzip.open(path_str, "wt", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    except PermissionError as e:
        raise UniGzipJsonWriteError(f"Permission denied writing to {path_str}", file_path=path_str) from e
    except OSError as e:
        raise UniGzipJsonWriteError(f"I/O error writing to {path_str}: {e}", file_path=path_str) from e
    except TypeError as e:
        # Re-raise TypeError for non-serializable data (not wrapped in UniGzipJsonWriteError)
        raise
    except Exception as e:
        raise UniGzipJsonWriteError(f"Unexpected error writing to {path_str}: {e}", file_path=path_str) from e


def readTxtGz(path: Union[str, Path]) -> str:
    """
    Read a gzip-compressed text file.

    Opens the file in text mode with UTF-8 encoding, decompresses it,
    and returns the text content.

    Args:
        path: Path to the gzip-compressed text file (str or Path).

    Returns:
        Text content as a string.

    Raises:
        UniGzipTxtReadError: If reading fails due to:
            - File not found
            - Invalid gzip format
            - Encoding errors
            - I/O errors
    """
    path_str = str(path)
    try:
        with gzip.open(path_str, "rt", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError as e:
        raise UniGzipTxtReadError(f"File not found: {path_str}", file_path=path_str) from e
    except gzip.BadGzipFile as e:
        raise UniGzipTxtReadError(f"Invalid gzip format: {path_str}", file_path=path_str) from e
    except UnicodeDecodeError as e:
        raise UniGzipTxtReadError(f"Encoding error reading {path_str}: {e}", file_path=path_str) from e
    except OSError as e:
        raise UniGzipTxtReadError(f"I/O error reading {path_str}: {e}", file_path=path_str) from e
    except Exception as e:
        raise UniGzipTxtReadError(f"Unexpected error reading {path_str}: {e}", file_path=path_str) from e


def writeTxtGz(path: Union[str, Path], content: Union[str, Iterable[str]]) -> None:
    """
    Write content to a gzip-compressed text file.

    Writes the content as a gzip-compressed file in text mode with UTF-8 encoding.
    If content is a string, it is written as-is. If content is an iterable of strings,
    each string is written as a line (no newline is added automatically).

    Args:
        path: Path to the output file (str or Path).
        content: Text content to write. Can be:
            - A string: written as-is
            - An iterable of strings: each string is written as a line

    Raises:
        UniGzipTxtWriteError: If writing fails due to:
            - Permission denied
            - Disk space issues
            - I/O errors
        TypeError: If content is not a string or iterable of strings.
    """
    path_str = str(path)
    try:
        with gzip.open(path_str, "wt", encoding="utf-8") as f:
            if isinstance(content, str):
                f.write(content)
            else:
                # content is an iterable of strings
                try:
                    for line in content:
                        f.write(line)
                except TypeError:
                    raise TypeError(f"content must be a string or iterable of strings, got {type(content).__name__}")
    except PermissionError as e:
        raise UniGzipTxtWriteError(f"Permission denied writing to {path_str}", file_path=path_str) from e
    except OSError as e:
        raise UniGzipTxtWriteError(f"I/O error writing to {path_str}: {e}", file_path=path_str) from e
    except TypeError as e:
        # Re-raise TypeError for invalid content type (not wrapped in UniGzipTxtWriteError)
        raise
    except Exception as e:
        raise UniGzipTxtWriteError(f"Unexpected error writing to {path_str}: {e}", file_path=path_str) from e
