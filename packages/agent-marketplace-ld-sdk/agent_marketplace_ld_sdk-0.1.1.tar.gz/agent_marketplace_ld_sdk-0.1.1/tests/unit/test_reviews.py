"""Tests for reviews resource."""

import pytest
from httpx import Response

from agent_marketplace_sdk import AsyncMarketplaceClient, MarketplaceClient
from agent_marketplace_sdk.exceptions import AgentNotFoundError
from agent_marketplace_sdk.models import ReviewCreate


class TestReviewsResource:
    """Tests for ReviewsResource."""

    def test_list_reviews(self, mock_api):
        """Test listing reviews."""
        with MarketplaceClient(api_key="test-key") as client:
            reviews = client.reviews.list("advanced-pm")
            assert len(reviews) == 1
            assert reviews[0].rating == 5

    def test_list_reviews_with_pagination(self, mock_api):
        """Test listing reviews with pagination."""
        with MarketplaceClient(api_key="test-key") as client:
            reviews = client.reviews.list("advanced-pm", limit=10, offset=0)
            assert len(reviews) == 1

    def test_list_reviews_not_found(self, mock_api):
        """Test listing reviews for nonexistent agent."""
        mock_api.get("/api/v1/agents/nonexistent/reviews").mock(return_value=Response(404))
        with MarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                client.reviews.list("nonexistent")

    def test_create_review(self, mock_api):
        """Test creating review."""
        with MarketplaceClient(api_key="test-key") as client:
            review_data = ReviewCreate(rating=5, comment="Great agent!")
            review = client.reviews.create("advanced-pm", review_data)
            assert review.rating == 5

    def test_create_review_not_found(self, mock_api):
        """Test creating review for nonexistent agent."""
        mock_api.post("/api/v1/agents/nonexistent/reviews").mock(return_value=Response(404))
        with MarketplaceClient(api_key="test-key") as client:
            review_data = ReviewCreate(rating=5)
            with pytest.raises(AgentNotFoundError):
                client.reviews.create("nonexistent", review_data)

    def test_update_review(self, mock_api):
        """Test updating review."""
        with MarketplaceClient(api_key="test-key") as client:
            review_data = ReviewCreate(rating=4, comment="Updated review")
            review = client.reviews.update("advanced-pm", 1, review_data)
            assert review is not None

    def test_update_review_not_found(self, mock_api):
        """Test updating review for nonexistent agent."""
        mock_api.put("/api/v1/agents/nonexistent/reviews/1").mock(return_value=Response(404))
        with MarketplaceClient(api_key="test-key") as client:
            review_data = ReviewCreate(rating=4)
            with pytest.raises(AgentNotFoundError):
                client.reviews.update("nonexistent", 1, review_data)

    def test_delete_review(self, mock_api):
        """Test deleting review."""
        with MarketplaceClient(api_key="test-key") as client:
            client.reviews.delete("advanced-pm", 1)

    def test_delete_review_not_found(self, mock_api):
        """Test deleting review for nonexistent agent."""
        mock_api.delete("/api/v1/agents/nonexistent/reviews/1").mock(return_value=Response(404))
        with MarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                client.reviews.delete("nonexistent", 1)

    def test_mark_helpful(self, mock_api):
        """Test marking review as helpful."""
        with MarketplaceClient(api_key="test-key") as client:
            client.reviews.mark_helpful("advanced-pm", 1)

    def test_mark_helpful_not_found(self, mock_api):
        """Test marking helpful for nonexistent review."""
        mock_api.post("/api/v1/agents/nonexistent/reviews/1/helpful").mock(
            return_value=Response(404)
        )
        with MarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                client.reviews.mark_helpful("nonexistent", 1)


class TestAsyncReviewsResource:
    """Tests for AsyncReviewsResource."""

    @pytest.mark.asyncio
    async def test_list_reviews(self, mock_api):
        """Test listing reviews asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            reviews = await client.reviews.list("advanced-pm")
            assert len(reviews) == 1

    @pytest.mark.asyncio
    async def test_list_reviews_with_pagination(self, mock_api):
        """Test listing reviews with pagination asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            reviews = await client.reviews.list("advanced-pm", limit=10, offset=0)
            assert len(reviews) == 1

    @pytest.mark.asyncio
    async def test_list_reviews_not_found(self, mock_api):
        """Test listing reviews for nonexistent agent."""
        mock_api.get("/api/v1/agents/nonexistent/reviews").mock(return_value=Response(404))
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                await client.reviews.list("nonexistent")

    @pytest.mark.asyncio
    async def test_create_review(self, mock_api):
        """Test creating review asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            review_data = ReviewCreate(rating=5, comment="Great agent!")
            review = await client.reviews.create("advanced-pm", review_data)
            assert review.rating == 5

    @pytest.mark.asyncio
    async def test_create_review_not_found(self, mock_api):
        """Test creating review for nonexistent agent."""
        mock_api.post("/api/v1/agents/nonexistent/reviews").mock(return_value=Response(404))
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            review_data = ReviewCreate(rating=5)
            with pytest.raises(AgentNotFoundError):
                await client.reviews.create("nonexistent", review_data)

    @pytest.mark.asyncio
    async def test_update_review(self, mock_api):
        """Test updating review asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            review_data = ReviewCreate(rating=4, comment="Updated")
            review = await client.reviews.update("advanced-pm", 1, review_data)
            assert review is not None

    @pytest.mark.asyncio
    async def test_update_review_not_found(self, mock_api):
        """Test updating review for nonexistent agent."""
        mock_api.put("/api/v1/agents/nonexistent/reviews/1").mock(return_value=Response(404))
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            review_data = ReviewCreate(rating=4)
            with pytest.raises(AgentNotFoundError):
                await client.reviews.update("nonexistent", 1, review_data)

    @pytest.mark.asyncio
    async def test_delete_review(self, mock_api):
        """Test deleting review asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            await client.reviews.delete("advanced-pm", 1)

    @pytest.mark.asyncio
    async def test_delete_review_not_found(self, mock_api):
        """Test deleting review for nonexistent agent."""
        mock_api.delete("/api/v1/agents/nonexistent/reviews/1").mock(return_value=Response(404))
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                await client.reviews.delete("nonexistent", 1)

    @pytest.mark.asyncio
    async def test_mark_helpful(self, mock_api):
        """Test marking review as helpful asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            await client.reviews.mark_helpful("advanced-pm", 1)

    @pytest.mark.asyncio
    async def test_mark_helpful_not_found(self, mock_api):
        """Test marking helpful for nonexistent review."""
        mock_api.post("/api/v1/agents/nonexistent/reviews/1/helpful").mock(
            return_value=Response(404)
        )
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                await client.reviews.mark_helpful("nonexistent", 1)
