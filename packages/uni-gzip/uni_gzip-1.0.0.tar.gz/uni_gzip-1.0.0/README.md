# uni-gzip

A unified lightweight Python library for reading and writing gzip-compressed JSON and text files with UTF-8 encoding and compact JSON format.

## Features

- **Unified API**: Four simple functions (`readJsonGz`, `writeJsonGz`, `readTxtGz`, `writeTxtGz`) for all operations
- **UTF-8 encoding**: Automatic handling of UTF-8 encoding for international characters
- **Compact JSON format**: Uses minimal JSON format (no spaces, no ASCII escaping) for efficient storage
- **Flexible text writing**: Supports writing strings or iterables of strings
- **Type safety**: Supports both `str` and `Path` objects for file paths
- **Error handling**: Comprehensive exception hierarchy for precise error handling
- **Zero dependencies**: Uses only Python standard library (gzip, json)

## Installation

```bash
pip install uni-gzip
```

## Quick Start

### Reading and writing gzip-compressed JSON files

```python
from uni_gzip import readJsonGz, writeJsonGz

# Write data to a gzip-compressed JSON file
data = {"key": "value", "number": 42, "list": [1, 2, 3]}
writeJsonGz("output.json.gz", data)

# Read a gzip-compressed JSON file
data = readJsonGz("output.json.gz")
print(data)
```

### Reading and writing gzip-compressed text files

```python
from uni_gzip import readTxtGz, writeTxtGz

# Write a string to a gzip-compressed text file
writeTxtGz("output.txt.gz", "Hello, World!")

# Write multiple lines from an iterable
lines = ["Line 1", "Line 2", "Line 3"]
writeTxtGz("output.txt.gz", lines)

# Read a gzip-compressed text file
content = readTxtGz("output.txt.gz")
print(content)
```

### Using Path objects

```python
from pathlib import Path
from uni_gzip import readJsonGz, writeJsonGz, readTxtGz, writeTxtGz

# Both str and Path objects are supported
path = Path("data.json.gz")
data = readJsonGz(path)

writeJsonGz(Path("output.json.gz"), {"example": "data"})
writeTxtGz(Path("output.txt.gz"), "Example text")
```

## API Reference

### `readJsonGz(path)`

Read a gzip-compressed JSON file.

**Parameters:**

- `path` (str | Path): Path to the gzip-compressed JSON file.

**Returns:**

- Any: Parsed JSON data (dict, list, or other JSON-serializable types).

**Raises:**

- `UniGzipJsonReadError`: If reading fails due to:
  - File not found
  - Invalid gzip format
  - JSON parsing errors
  - I/O errors

**Example:**

```python
from uni_gzip import readJsonGz

data = readJsonGz("data.json.gz")
```

### `writeJsonGz(path, data)`

Write data to a gzip-compressed JSON file.

The file is written in compact JSON format (no spaces, no ASCII escaping) with UTF-8 encoding for efficient storage.

**Parameters:**

- `path` (str | Path): Path to the output file.
- `data` (Any): Data to serialize (must be JSON-serializable).

**Raises:**

- `UniGzipJsonWriteError`: If writing fails due to:
  - Permission denied
  - Disk space issues
  - I/O errors
- `TypeError`: If data is not JSON-serializable.

**Example:**

```python
from uni_gzip import writeJsonGz

data = {"key": "value", "number": 42}
writeJsonGz("output.json.gz", data)
```

### `readTxtGz(path)`

Read a gzip-compressed text file.

**Parameters:**

- `path` (str | Path): Path to the gzip-compressed text file.

**Returns:**

- str: Text content as a string.

**Raises:**

- `UniGzipTxtReadError`: If reading fails due to:
  - File not found
  - Invalid gzip format
  - Encoding errors
  - I/O errors

**Example:**

```python
from uni_gzip import readTxtGz

content = readTxtGz("data.txt.gz")
```

### `writeTxtGz(path, content)`

Write content to a gzip-compressed text file.

The file is written with UTF-8 encoding. If content is a string, it is written as-is. If content is an iterable of strings, each string is written as a line (no newline is added automatically).

**Parameters:**

- `path` (str | Path): Path to the output file.
- `content` (str | Iterable[str]): Text content to write. Can be:
  - A string: written as-is
  - An iterable of strings: each string is written as a line

**Raises:**

- `UniGzipTxtWriteError`: If writing fails due to:
  - Permission denied
  - Disk space issues
  - I/O errors
- `TypeError`: If content is not a string or iterable of strings.

**Example:**

```python
from uni_gzip import writeTxtGz

# Write a string
writeTxtGz("output.txt.gz", "Hello, World!")

# Write multiple lines
lines = ["Line 1", "Line 2", "Line 3"]
writeTxtGz("output.txt.gz", lines)
```

## Exceptions

### `UniGzipError`

Base exception class for all uni-gzip related errors.

**Attributes:**

- `message`: Primary error message (required)
- `file_path`: Path to the file that caused the error (optional)

### `UniGzipJsonError`

Base exception class for uni-gzip JSON processing errors.

### `UniGzipJsonReadError`

Raised when reading a gzip-compressed JSON file fails.

This exception indicates that an error occurred during the read operation, such as file not found, invalid gzip format, JSON parsing errors, or I/O errors.

**Example:**

```python
from uni_gzip import readJsonGz, UniGzipJsonReadError

try:
    data = readJsonGz("nonexistent.json.gz")
except UniGzipJsonReadError as e:
    print(f"Error reading file: {e.message}")
    print(f"File path: {e.file_path}")
```

### `UniGzipJsonWriteError`

Raised when writing a gzip-compressed JSON file fails.

This exception indicates that an error occurred during the write operation, such as permission denied, disk space issues, or I/O errors.

**Example:**

```python
from uni_gzip import writeJsonGz, UniGzipJsonWriteError

try:
    writeJsonGz("/readonly/output.json.gz", {"data": "value"})
except UniGzipJsonWriteError as e:
    print(f"Error writing file: {e.message}")
    print(f"File path: {e.file_path}")
```

### `UniGzipTxtError`

Base exception class for uni-gzip text processing errors.

### `UniGzipTxtReadError`

Raised when reading a gzip-compressed text file fails.

This exception indicates that an error occurred during the read operation, such as file not found, invalid gzip format, encoding errors, or I/O errors.

**Example:**

```python
from uni_gzip import readTxtGz, UniGzipTxtReadError

try:
    content = readTxtGz("nonexistent.txt.gz")
except UniGzipTxtReadError as e:
    print(f"Error reading file: {e.message}")
    print(f"File path: {e.file_path}")
```

### `UniGzipTxtWriteError`

Raised when writing a gzip-compressed text file fails.

This exception indicates that an error occurred during the write operation, such as permission denied, disk space issues, or I/O errors.

**Example:**

```python
from uni_gzip import writeTxtGz, UniGzipTxtWriteError

try:
    writeTxtGz("/readonly/output.txt.gz", "Hello, World!")
except UniGzipTxtWriteError as e:
    print(f"Error writing file: {e.message}")
    print(f"File path: {e.file_path}")
```

## Requirements

- Python >= 3.10

No external dependencies required. This package uses only Python standard library modules (`gzip` and `json`).

## License

MIT License
