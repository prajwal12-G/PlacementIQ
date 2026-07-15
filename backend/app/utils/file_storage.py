"""
File storage utilities.

This module centralizes low-level filesystem operations for PlacementIQ,
including:

- Generating unique, collision-resistant filenames
- Extracting file extensions
- Persisting uploaded files to disk
- Removing previously stored files

It contains no business logic, no database access, no authentication,
and no FastAPI request handling. Callers are expected to perform all
validation, business decisions, and persistence of metadata themselves.
"""

from pathlib import Path
from shutil import copyfileobj
from uuid import uuid4

from fastapi import UploadFile


# ---------------------------------------------------------------------------
# Filename Utilities
# ---------------------------------------------------------------------------

def get_file_extension(filename: str) -> str:
    """
    Return the lowercase extension of ``filename`` without the leading dot.

    Args:
        filename: Original filename (e.g. ``"Resume.PDF"``).

    Returns:
        The extension in lowercase without a leading dot
        (e.g. ``"pdf"``). Returns an empty string if the filename has
        no extension.
    """
    return Path(filename).suffix.lstrip(".").lower()


def generate_unique_filename(filename: str) -> str:
    """
    Generate a UUID4-based filename that preserves the original extension.

    Args:
        filename: Original filename whose extension should be kept
            (e.g. ``"resume.pdf"``).

    Returns:
        A new filename of the form ``"<uuid4>.<ext>"`` where ``<ext>``
        is the lowercased original extension. Example:
        ``"6dbbe8d8-5d53-47a8-b0a0-14b58c7cb50d.pdf"``.
    """
    extension = get_file_extension(filename)
    unique_id = uuid4()

    if extension:
        return f"{unique_id}.{extension}"

    return str(unique_id)


# ---------------------------------------------------------------------------
# File I/O Utilities
# ---------------------------------------------------------------------------

def save_uploaded_file(
    file: UploadFile,
    directory: Path,
    filename: str,
) -> Path:
    """
    Save an uploaded file to ``directory`` under ``filename``.

    The destination directory is created if it does not already exist.
    The file is streamed to disk using ``shutil.copyfileobj`` so large
    uploads are not loaded fully into memory.

    Args:
        file: The uploaded file object supplied by FastAPI.
        directory: Destination directory on disk.
        filename: Target filename within ``directory``.

    Returns:
        The full :class:`pathlib.Path` to the saved file.
    """
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination = directory / filename

    # Reset the stream in case it has already been read during validation.
    file.file.seek(0)

    # Binary mode preserves the uploaded file exactly as received.
    with destination.open("wb") as buffer:
        copyfileobj(file.file, buffer)

    return destination


def delete_uploaded_file(file_path: Path) -> None:
    """
    Delete ``file_path`` from disk, ignoring missing files.

    This helper is intentionally tolerant: if the file does not exist
    the call is a no-op so callers do not need to guard for race
    conditions where the file has already been removed.

    Args:
        file_path: Absolute or relative path to the file to delete.
    """
    if file_path.exists():
        file_path.unlink()


__all__ = [
    "get_file_extension",
    "generate_unique_filename",
    "save_uploaded_file",
    "delete_uploaded_file",
]