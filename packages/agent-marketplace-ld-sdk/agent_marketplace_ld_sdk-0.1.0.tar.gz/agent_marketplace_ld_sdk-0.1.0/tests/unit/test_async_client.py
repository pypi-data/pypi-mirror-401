"""Tests for AsyncMarketplaceClient."""

import os
from unittest.mock import patch

import pytest

from agent_marketplace_sdk import AsyncMarketplaceClient
from agent_marketplace_sdk.exceptions import ConfigurationError


class TestAsyncMarketplaceClient:
    """Tests for AsyncMarketplaceClient."""

    def test_init_with_api_key(self):
        """Test async client initialization with API key."""
        client = AsyncMarketplaceClient(api_key="test-key")
        assert client.api_key == "test-key"
        assert client.base_url == "https://api.agent-marketplace.com"

    def test_init_with_env_var(self):
        """Test async client initialization with environment variable."""
        with patch.dict(os.environ, {"MARKETPLACE_API_KEY": "env-key"}):
            client = AsyncMarketplaceClient()
            assert client.api_key == "env-key"

    def test_init_without_api_key_raises(self):
        """Test async client initialization without API key raises error."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("MARKETPLACE_API_KEY", None)
            with pytest.raises(ConfigurationError) as exc_info:
                AsyncMarketplaceClient()
            assert "API key required" in str(exc_info.value)

    def test_init_custom_settings(self):
        """Test async client initialization with custom settings."""
        client = AsyncMarketplaceClient(
            api_key="test-key",
            base_url="https://custom.api.com",
            timeout=60.0,
            max_retries=5,
        )
        assert client.base_url == "https://custom.api.com"

    @pytest.mark.asyncio
    async def test_context_manager(self, mock_api):
        """Test async client as context manager."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            assert client.api_key == "test-key"

    def test_resources_initialized(self):
        """Test that all resources are initialized."""
        client = AsyncMarketplaceClient(api_key="test-key")
        assert client.agents is not None
        assert client.users is not None
        assert client.reviews is not None
        assert client.categories is not None
        assert client.search is not None
        assert client.analytics is not None

    @pytest.mark.asyncio
    async def test_request_method(self, mock_api):
        """Test the _request method."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            response = await client._request("GET", "/api/v1/agents")
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_close(self, mock_api):
        """Test async close method."""
        client = AsyncMarketplaceClient(api_key="test-key")
        await client.close()
