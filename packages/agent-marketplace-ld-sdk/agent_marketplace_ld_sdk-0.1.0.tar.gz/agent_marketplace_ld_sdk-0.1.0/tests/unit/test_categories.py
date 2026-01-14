"""Tests for categories resource."""

import pytest

from agent_marketplace_sdk import AsyncMarketplaceClient, MarketplaceClient


class TestCategoriesResource:
    """Tests for CategoriesResource."""

    def test_list_categories(self, mock_api):
        """Test listing categories."""
        with MarketplaceClient(api_key="test-key") as client:
            categories = client.categories.list()
            assert len(categories) == 2
            assert categories[0].name == "Project Management"

    def test_get_category(self, mock_api):
        """Test getting category by slug."""
        with MarketplaceClient(api_key="test-key") as client:
            category = client.categories.get("pm")
            assert category.name == "Project Management"
            assert category.slug == "pm"


class TestAsyncCategoriesResource:
    """Tests for AsyncCategoriesResource."""

    @pytest.mark.asyncio
    async def test_list_categories(self, mock_api):
        """Test listing categories asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            categories = await client.categories.list()
            assert len(categories) == 2

    @pytest.mark.asyncio
    async def test_get_category(self, mock_api):
        """Test getting category by slug asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            category = await client.categories.get("pm")
            assert category.slug == "pm"
