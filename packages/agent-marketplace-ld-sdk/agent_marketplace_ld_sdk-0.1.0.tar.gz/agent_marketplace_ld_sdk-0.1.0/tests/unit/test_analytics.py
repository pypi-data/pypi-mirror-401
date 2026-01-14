"""Tests for analytics resource."""

import pytest
from httpx import Response

from agent_marketplace_sdk import AsyncMarketplaceClient, MarketplaceClient
from agent_marketplace_sdk.exceptions import AgentNotFoundError


class TestAnalyticsResource:
    """Tests for AnalyticsResource."""

    def test_get_agent_analytics(self, mock_api):
        """Test getting agent analytics."""
        with MarketplaceClient(api_key="test-key") as client:
            analytics = client.analytics.get_agent_analytics("advanced-pm")
            assert analytics.agent_slug == "advanced-pm"
            assert analytics.total_downloads == 1000

    def test_get_agent_analytics_not_found(self, mock_api):
        """Test getting analytics for nonexistent agent."""
        mock_api.get("/api/v1/agents/nonexistent/analytics").mock(return_value=Response(404))
        with MarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                client.analytics.get_agent_analytics("nonexistent")

    def test_get_trending(self, mock_api):
        """Test getting trending agents."""
        with MarketplaceClient(api_key="test-key") as client:
            trending = client.analytics.get_trending()
            assert len(trending) == 1
            assert trending[0].slug == "advanced-pm"

    def test_get_trending_with_limit(self, mock_api):
        """Test getting trending agents with limit."""
        with MarketplaceClient(api_key="test-key") as client:
            trending = client.analytics.get_trending(limit=5)
            assert len(trending) == 1


class TestAsyncAnalyticsResource:
    """Tests for AsyncAnalyticsResource."""

    @pytest.mark.asyncio
    async def test_get_agent_analytics(self, mock_api):
        """Test getting agent analytics asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            analytics = await client.analytics.get_agent_analytics("advanced-pm")
            assert analytics.agent_slug == "advanced-pm"

    @pytest.mark.asyncio
    async def test_get_agent_analytics_not_found(self, mock_api):
        """Test getting analytics for nonexistent agent."""
        mock_api.get("/api/v1/agents/nonexistent/analytics").mock(return_value=Response(404))
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                await client.analytics.get_agent_analytics("nonexistent")

    @pytest.mark.asyncio
    async def test_get_trending(self, mock_api):
        """Test getting trending agents asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            trending = await client.analytics.get_trending()
            assert len(trending) == 1

    @pytest.mark.asyncio
    async def test_get_trending_with_limit(self, mock_api):
        """Test getting trending agents with limit asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            trending = await client.analytics.get_trending(limit=5)
            assert len(trending) == 1
