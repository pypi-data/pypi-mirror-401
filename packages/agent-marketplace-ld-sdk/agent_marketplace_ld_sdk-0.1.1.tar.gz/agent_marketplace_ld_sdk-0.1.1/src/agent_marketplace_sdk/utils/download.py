"""Download utilities for Agent Marketplace SDK."""

from __future__ import annotations

import io
import zipfile
from pathlib import Path


def download_file(content: bytes, destination: Path) -> Path:
    """Save downloaded content to a file.

    Args:
        content: File content bytes.
        destination: Destination file path.

    Returns:
        Path to saved file.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)
    return destination


def extract_zip(content: bytes, destination: Path) -> Path:
    """Extract zip content to a directory.

    Args:
        content: Zip file content bytes.
        destination: Destination directory.

    Returns:
        Path to extraction directory.
    """
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        zf.extractall(destination)
    return destination
