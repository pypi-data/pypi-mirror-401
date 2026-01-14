"""Tests for config module."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from agent_marketplace_sdk.config import (
    DEFAULT_BASE_URL,
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    MarketplaceConfig,
)
from agent_marketplace_sdk.exceptions import ConfigurationError


class TestMarketplaceConfig:
    """Tests for MarketplaceConfig."""

    def test_init_with_api_key(self):
        """Test config initialization with API key."""
        config = MarketplaceConfig(api_key="test-key")
        assert config.api_key == "test-key"
        assert config.base_url == DEFAULT_BASE_URL
        assert config.timeout == DEFAULT_TIMEOUT
        assert config.max_retries == DEFAULT_MAX_RETRIES

    def test_init_with_env_var(self):
        """Test config initialization with environment variable."""
        with patch.dict(os.environ, {"MARKETPLACE_API_KEY": "env-key"}):
            config = MarketplaceConfig()
            assert config.api_key == "env-key"

    def test_init_with_custom_base_url_env(self):
        """Test config initialization with custom base URL from env."""
        with patch.dict(
            os.environ,
            {
                "MARKETPLACE_API_KEY": "test-key",
                "MARKETPLACE_BASE_URL": "https://custom.api.com",
            },
        ):
            config = MarketplaceConfig()
            assert config.base_url == "https://custom.api.com"

    def test_init_without_api_key_raises(self):
        """Test config initialization without API key raises error."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("MARKETPLACE_API_KEY", None)
            with pytest.raises(ConfigurationError):
                MarketplaceConfig()

    def test_init_custom_settings(self):
        """Test config initialization with custom settings."""
        config = MarketplaceConfig(
            api_key="test-key",
            base_url="https://custom.api.com",
            timeout=60.0,
            max_retries=5,
        )
        assert config.base_url == "https://custom.api.com"
        assert config.timeout == 60.0
        assert config.max_retries == 5

    def test_from_file(self, tmp_path: Path):
        """Test loading config from file."""
        config_file = tmp_path / "config.toml"
        config_file.write_text(
            """
api_key = "file-key"
base_url = "https://file.api.com"
timeout = 45.0
max_retries = 4
"""
        )

        config = MarketplaceConfig.from_file(config_file)
        assert config.api_key == "file-key"
        assert config.base_url == "https://file.api.com"
        assert config.timeout == 45.0
        assert config.max_retries == 4

    def test_from_file_not_found(self):
        """Test loading config from nonexistent file."""
        with pytest.raises(ConfigurationError) as exc_info:
            MarketplaceConfig.from_file("/nonexistent/config.toml")
        assert "Config file not found" in str(exc_info.value)

    def test_from_file_invalid_toml(self, tmp_path: Path):
        """Test loading config from invalid TOML file."""
        config_file = tmp_path / "config.toml"
        config_file.write_text("invalid toml [[[")

        with pytest.raises(ConfigurationError) as exc_info:
            MarketplaceConfig.from_file(config_file)
        assert "Failed to parse" in str(exc_info.value)

    def test_save(self, tmp_path: Path):
        """Test saving config to file."""
        config = MarketplaceConfig(
            api_key="test-key",
            base_url="https://test.api.com",
            timeout=30.0,
            max_retries=3,
        )

        config_file = tmp_path / "config.toml"
        config.save(config_file)

        assert config_file.exists()
        content = config_file.read_text()
        assert 'api_key = "test-key"' in content
        assert 'base_url = "https://test.api.com"' in content

    def test_save_creates_parent_dirs(self, tmp_path: Path):
        """Test saving config creates parent directories."""
        config = MarketplaceConfig(api_key="test-key")

        config_file = tmp_path / "subdir" / "config.toml"
        config.save(config_file)

        assert config_file.exists()
