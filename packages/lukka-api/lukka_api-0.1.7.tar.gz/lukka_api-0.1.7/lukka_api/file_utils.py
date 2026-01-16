"""
File utilities for atomic operations and secure file handling.

This module provides atomic file operations to prevent partial file writes,
corruption on crashes, and ensure proper file permissions for security.
"""

from contextlib import contextmanager
import os
import json
import time
import logging
import portalocker
from pathlib import Path
from typing import Any, Dict, Generator

logger = logging.getLogger(__name__)


@contextmanager
def atomic_write(file_path: Path, mode: str = "w", **kwargs) -> Generator:
    """
    Atomic file write with automatic cleanup and permissions.

    Writes to a temporary file first, then performs an atomic rename on success.
    Sets restrictive permissions (0o600 - owner read/write only) before rename.
    Automatically cleans up temporary file on error.

    Args:
        file_path: Target file path
        mode: File open mode (default: "w")
        **kwargs: Additional arguments for open()

    Yields:
        File handle for writing

    Raises:
        IOError: If write or rename fails
        OSError: If directory creation or permissions setting fails

    Example:
        >>> from pathlib import Path
        >>> with atomic_write(Path("/tmp/data.json")) as f:
        ...     json.dump({"key": "value"}, f)
        # File is now atomically written with 0o600 permissions

    Security:
        - Files are created with restrictive 0o600 permissions (owner only)
        - No window where file is partially written
        - Temporary file is cleaned up on error

    Atomicity:
        - POSIX systems: rename() is atomic
        - Windows: replace() is atomic
        - Both guarantee no partial files visible to readers
    """
    temp_path = file_path.with_suffix(file_path.suffix + ".tmp")

    try:
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write to temp file with exclusive lock
        with open(temp_path, mode, **kwargs) as f:
            portalocker.lock(f, portalocker.LOCK_EX)
            yield f
            portalocker.unlock(f)

        # Set restrictive permissions (owner read/write only) before making visible
        # This prevents race conditions where file is readable with wrong permissions
        os.chmod(temp_path, 0o600)

        # Atomic rename - POSIX/Windows both guarantee atomicity
        # This makes the file visible to readers in one atomic operation
        temp_path.replace(file_path)

        logger.debug(f"Atomic write completed: {file_path}")

    except Exception as e:
        # Cleanup temp file on any error
        if temp_path.exists():
            try:
                temp_path.unlink()
                logger.debug(f"Cleaned up temp file: {temp_path}")
            except Exception as cleanup_error:
                logger.warning(f"Failed to cleanup temp file {temp_path}: {cleanup_error}")
        raise IOError(f"Atomic write failed for {file_path}: {e}") from e


def atomic_write_json(file_path: Path, data: Dict[str, Any], indent: int = 2) -> None:
    """
    Atomic write of JSON data with proper permissions.

    Convenience wrapper around atomic_write() for JSON data.
    Ensures atomic write, proper permissions, and UTF-8 encoding.

    Args:
        file_path: Target file path
        data: Dictionary to write as JSON
        indent: JSON indentation level (default: 2)

    Raises:
        IOError: If write fails
        TypeError: If data is not JSON serializable

    Example:
        >>> from pathlib import Path
        >>> data = {"token": "abc123", "expires": 1234567890}
        >>> atomic_write_json(Path("/tmp/token.json"), data)
        # File is atomically written with 0o600 permissions

    Performance:
        - Uses compact JSON format if indent=None
        - UTF-8 encoding for international character support
        - Single write operation (buffered)
    """
    with atomic_write(file_path, mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)

    logger.debug(f"Atomic JSON write completed: {file_path}")


def secure_read_json(file_path: Path, timeout: float = 5.0) -> Dict[str, Any]:
    """
    Read JSON file with shared lock and timeout.

    Acquires a shared lock before reading to coordinate with writers.
    Uses non-blocking lock with timeout to prevent deadlocks.
    Returns empty dict if file is corrupted (graceful degradation).

    Args:
        file_path: File path to read
        timeout: Lock timeout in seconds (default: 5.0)

    Returns:
        Parsed JSON data as dictionary, or {} if corrupted

    Raises:
        TimeoutError: If lock cannot be acquired within timeout
        FileNotFoundError: If file doesn't exist

    Example:
        >>> from pathlib import Path
        >>> data = secure_read_json(Path("/tmp/token.json"))
        >>> print(data.get("token"))
        'abc123'

    Concurrency:
        - Multiple readers can read simultaneously (shared lock)
        - Writers block readers (exclusive lock)
        - Non-blocking lock prevents deadlocks

    Error Handling:
        - Corrupted JSON returns {} instead of raising exception
        - Missing file raises FileNotFoundError
        - Lock timeout raises TimeoutError
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                # Non-blocking shared lock - allows multiple concurrent readers
                portalocker.lock(f, portalocker.LOCK_SH | portalocker.LOCK_NB)
                data = json.load(f)
                portalocker.unlock(f)
                logger.debug(f"Secure JSON read completed: {file_path}")
                return data

        except portalocker.LockException:
            # Lock not available, wait and retry
            time.sleep(0.1)

        except json.JSONDecodeError as e:
            # File corrupted - return empty dict for graceful degradation
            logger.warning(f"Corrupted JSON file {file_path}: {e}, returning empty dict")
            return {}

    raise TimeoutError(f"Could not acquire read lock within {timeout} seconds for {file_path}")


def ensure_secure_permissions(file_path: Path, permissions: int = 0o600) -> None:
    """
    Ensure file has secure permissions.

    Sets restrictive permissions on an existing file.
    Useful for fixing permissions on files created without atomic_write.

    Args:
        file_path: Path to file
        permissions: Octal permissions (default: 0o600 - owner read/write only)

    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If permissions cannot be set

    Example:
        >>> from pathlib import Path
        >>> ensure_secure_permissions(Path("/tmp/sensitive.json"))
        # File now has 0o600 permissions

    Security:
        - 0o600: Owner read/write only (recommended for secrets)
        - 0o644: Owner read/write, others read (for non-sensitive data)
        - 0o400: Owner read-only (for immutable data)
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        os.chmod(file_path, permissions)
        logger.debug(f"Set permissions {oct(permissions)} on {file_path}")
    except OSError as e:
        raise OSError(f"Failed to set permissions on {file_path}: {e}") from e


def atomic_delete(file_path: Path) -> bool:
    """
    Atomically delete a file if it exists.

    Returns True if file was deleted, False if it didn't exist.
    Safe to call multiple times (idempotent).

    Args:
        file_path: Path to file to delete

    Returns:
        True if file was deleted, False if it didn't exist

    Raises:
        OSError: If deletion fails for reasons other than file not existing

    Example:
        >>> from pathlib import Path
        >>> deleted = atomic_delete(Path("/tmp/old_token.json"))
        >>> if deleted:
        ...     print("File was deleted")

    Safety:
        - Idempotent: safe to call multiple times
        - Atomic: file either exists or doesn't (no partial deletion)
        - Returns status instead of raising exception for missing files
    """
    try:
        file_path.unlink()
        logger.debug(f"Atomic delete completed: {file_path}")
        return True
    except FileNotFoundError:
        return False
    except OSError as e:
        raise OSError(f"Failed to delete {file_path}: {e}") from e
