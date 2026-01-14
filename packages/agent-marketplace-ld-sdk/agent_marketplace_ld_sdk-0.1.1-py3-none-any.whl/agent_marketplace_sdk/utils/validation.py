"""Validation utilities for Agent Marketplace SDK."""

from __future__ import annotations

import re
from pathlib import Path

from agent_marketplace_sdk.exceptions import ValidationError

# Agent name pattern: alphanumeric with hyphens, 3-100 chars
AGENT_NAME_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9-]{2,99}$")

# Semantic version pattern
VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")

# Required files for agent structure
REQUIRED_FILES = ["agent.py", "agent.yaml"]


def validate_agent_name(name: str) -> bool:
    """Validate agent name.

    Args:
        name: Agent name to validate.

    Returns:
        True if valid.

    Raises:
        ValidationError: If name is invalid.
    """
    if not AGENT_NAME_PATTERN.match(name):
        raise ValidationError(
            "Agent name must start with a letter, be 3-100 characters, "
            "and contain only alphanumeric characters and hyphens."
        )
    return True


def validate_version(version: str) -> bool:
    """Validate semantic version.

    Args:
        version: Version string to validate.

    Returns:
        True if valid.

    Raises:
        ValidationError: If version is invalid.
    """
    if not VERSION_PATTERN.match(version):
        raise ValidationError("Version must be semantic (e.g., 1.0.0)")
    return True


def validate_agent_structure(path: Path | str) -> bool:
    """Validate agent directory structure.

    Args:
        path: Path to agent directory.

    Returns:
        True if valid.

    Raises:
        ValidationError: If structure is invalid.
    """
    path_obj = Path(path)

    if not path_obj.is_dir():
        raise ValidationError(f"Path '{path}' is not a directory")

    missing_files = []
    for required_file in REQUIRED_FILES:
        if not (path_obj / required_file).exists():
            missing_files.append(required_file)

    if missing_files:
        raise ValidationError(f"Missing required files: {', '.join(missing_files)}")

    return True
