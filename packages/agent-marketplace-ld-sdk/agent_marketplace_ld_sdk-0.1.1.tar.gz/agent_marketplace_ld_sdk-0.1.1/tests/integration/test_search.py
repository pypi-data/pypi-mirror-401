"""Integration tests for search operations."""

import pytest

from agent_marketplace_sdk import AsyncMarketplaceClient, MarketplaceClient


@pytest.mark.integration
class TestSearchFlow:
    """Integration tests for search workflow."""

    def test_search_flow(self, mock_api):
        """Test search workflow."""
        with MarketplaceClient(api_key="test-key") as client:
            # Basic search
            agents = client.search.search("code review")
            assert len(agents) > 0

            # Search with filters
            filtered_agents = client.search.search(
                "code review",
                category="pm",
                min_rating=4.0,
                sort="downloads",
            )
            assert len(filtered_agents) > 0

            # Get categories
            categories = client.categories.list()
            assert len(categories) > 0

            # Get trending
            trending = client.analytics.get_trending()
            assert len(trending) > 0


@pytest.mark.integration
class TestAsyncSearchFlow:
    """Integration tests for async search workflow."""

    @pytest.mark.asyncio
    async def test_async_search_flow(self, mock_api):
        """Test async search workflow."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            # Basic search
            agents = await client.search.search("code review")
            assert len(agents) > 0

            # Search with filters
            filtered_agents = await client.search.search(
                "code review",
                category="pm",
                min_rating=4.0,
                sort="downloads",
            )
            assert len(filtered_agents) > 0

            # Get categories
            categories = await client.categories.list()
            assert len(categories) > 0

            # Get trending
            trending = await client.analytics.get_trending()
            assert len(trending) > 0
