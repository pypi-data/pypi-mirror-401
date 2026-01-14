"""Packaging utilities for Agent Marketplace SDK."""

from __future__ import annotations

import io
import zipfile
from pathlib import Path


def create_agent_package(code_path: Path | str) -> bytes:
    """Create a zip package from agent code.

    Args:
        code_path: Path to agent code directory.

    Returns:
        Zip file content as bytes.
    """
    zip_buffer = io.BytesIO()
    code_path_obj = Path(code_path)

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in code_path_obj.rglob("*"):
            if file.is_file():
                zf.write(file, file.relative_to(code_path_obj))

    return zip_buffer.getvalue()


def get_package_size(code_path: Path | str) -> int:
    """Get the size of the agent package.

    Args:
        code_path: Path to agent code directory.

    Returns:
        Package size in bytes.
    """
    return len(create_agent_package(code_path))
