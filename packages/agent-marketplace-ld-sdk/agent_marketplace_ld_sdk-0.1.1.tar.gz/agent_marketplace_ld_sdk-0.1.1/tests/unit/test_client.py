"""Tests for MarketplaceClient."""

import os
from unittest.mock import patch

import pytest

from agent_marketplace_sdk import MarketplaceClient
from agent_marketplace_sdk.exceptions import ConfigurationError


class TestMarketplaceClient:
    """Tests for MarketplaceClient."""

    def test_init_with_api_key(self, mock_api):
        """Test client initialization with API key."""
        client = MarketplaceClient(api_key="test-key")
        assert client.api_key == "test-key"
        assert client.base_url == "https://api.agent-marketplace.com"
        client.close()

    def test_init_with_env_var(self, mock_api):
        """Test client initialization with environment variable."""
        with patch.dict(os.environ, {"MARKETPLACE_API_KEY": "env-key"}):
            client = MarketplaceClient()
            assert client.api_key == "env-key"
            client.close()

    def test_init_without_api_key_raises(self):
        """Test client initialization without API key raises error."""
        with patch.dict(os.environ, {}, clear=True):
            # Remove MARKETPLACE_API_KEY if it exists
            os.environ.pop("MARKETPLACE_API_KEY", None)
            with pytest.raises(ConfigurationError) as exc_info:
                MarketplaceClient()
            assert "API key required" in str(exc_info.value)

    def test_init_custom_settings(self, mock_api):
        """Test client initialization with custom settings."""
        client = MarketplaceClient(
            api_key="test-key",
            base_url="https://custom.api.com",
            timeout=60.0,
            max_retries=5,
        )
        assert client.base_url == "https://custom.api.com"
        client.close()

    def test_context_manager(self, mock_api):
        """Test client as context manager."""
        with MarketplaceClient(api_key="test-key") as client:
            assert client.api_key == "test-key"

    def test_resources_initialized(self, mock_api):
        """Test that all resources are initialized."""
        with MarketplaceClient(api_key="test-key") as client:
            assert client.agents is not None
            assert client.users is not None
            assert client.reviews is not None
            assert client.categories is not None
            assert client.search is not None
            assert client.analytics is not None

    def test_request_method(self, mock_api):
        """Test the _request method."""
        with MarketplaceClient(api_key="test-key") as client:
            response = client._request("GET", "/api/v1/agents")
            assert response.status_code == 200
