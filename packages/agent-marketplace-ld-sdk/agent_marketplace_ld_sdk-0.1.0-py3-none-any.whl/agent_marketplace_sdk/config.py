"""Configuration management for Agent Marketplace SDK."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from agent_marketplace_sdk.exceptions import ConfigurationError

DEFAULT_BASE_URL = "https://api.agent-marketplace.com"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 3


class MarketplaceConfig:
    """SDK configuration."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        """Initialize configuration.

        Args:
            api_key: API key (or MARKETPLACE_API_KEY env var).
            base_url: API base URL (or MARKETPLACE_BASE_URL env var).
            timeout: Request timeout in seconds.
            max_retries: Maximum retry attempts.

        Raises:
            ConfigurationError: If API key is not provided.
        """
        self.api_key = api_key or os.getenv("MARKETPLACE_API_KEY")
        self.base_url = base_url or os.getenv("MARKETPLACE_BASE_URL", DEFAULT_BASE_URL)
        self.timeout = timeout
        self.max_retries = max_retries

        if not self.api_key:
            raise ConfigurationError(
                "API key required. Set MARKETPLACE_API_KEY env var or pass api_key parameter."
            )

    @classmethod
    def from_file(cls, path: Path | str = "~/.marketplace/config.toml") -> MarketplaceConfig:
        """Load configuration from file.

        Args:
            path: Config file path.

        Returns:
            Configuration instance.

        Raises:
            ConfigurationError: If config file not found or invalid.
        """
        import tomllib

        expanded_path = Path(path).expanduser()
        if not expanded_path.exists():
            raise ConfigurationError(f"Config file not found: {expanded_path}")

        try:
            with expanded_path.open("rb") as f:
                config: dict[str, Any] = tomllib.load(f)
        except Exception as e:
            raise ConfigurationError(f"Failed to parse config file: {e}") from e

        return cls(
            api_key=config.get("api_key"),
            base_url=config.get("base_url"),
            timeout=config.get("timeout", DEFAULT_TIMEOUT),
            max_retries=config.get("max_retries", DEFAULT_MAX_RETRIES),
        )

    def save(self, path: Path | str = "~/.marketplace/config.toml") -> None:
        """Save configuration to file.

        Args:
            path: Config file path.
        """
        expanded_path = Path(path).expanduser()
        expanded_path.parent.mkdir(parents=True, exist_ok=True)

        config_content = f"""# Agent Marketplace SDK Configuration
api_key = "{self.api_key}"
base_url = "{self.base_url}"
timeout = {self.timeout}
max_retries = {self.max_retries}
"""

        with expanded_path.open("w") as f:
            f.write(config_content)
