"""Upload utilities for Agent Marketplace SDK."""

from __future__ import annotations

import io
import zipfile
from pathlib import Path
from typing import BinaryIO


def prepare_upload(code_path: Path | str) -> BinaryIO:
    """Prepare agent code for upload by creating a zip archive.

    Args:
        code_path: Path to agent code directory.

    Returns:
        Binary IO containing zip archive.
    """
    zip_buffer = io.BytesIO()
    code_path_obj = Path(code_path)

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in code_path_obj.rglob("*"):
            if file.is_file():
                zf.write(file, file.relative_to(code_path_obj))

    zip_buffer.seek(0)
    return zip_buffer
