"""Tests for search resource."""

import pytest

from agent_marketplace_sdk import AsyncMarketplaceClient, MarketplaceClient


class TestSearchResource:
    """Tests for SearchResource."""

    def test_search(self, mock_api):
        """Test searching agents."""
        with MarketplaceClient(api_key="test-key") as client:
            agents = client.search.search("code review")
            assert len(agents) == 1
            assert agents[0].name == "Advanced PM"

    def test_search_with_filters(self, mock_api):
        """Test searching agents with filters."""
        with MarketplaceClient(api_key="test-key") as client:
            agents = client.search.search(
                "code review",
                category="pm",
                min_rating=4.0,
                sort="downloads",
                limit=10,
                offset=0,
            )
            assert len(agents) == 1


class TestAsyncSearchResource:
    """Tests for AsyncSearchResource."""

    @pytest.mark.asyncio
    async def test_search(self, mock_api):
        """Test searching agents asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            agents = await client.search.search("code review")
            assert len(agents) == 1

    @pytest.mark.asyncio
    async def test_search_with_filters(self, mock_api):
        """Test searching agents with filters asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            agents = await client.search.search(
                "code review",
                category="pm",
                min_rating=4.0,
                sort="downloads",
                limit=10,
                offset=0,
            )
            assert len(agents) == 1
