"""Integration tests for agent operations."""

import pytest

from agent_marketplace_sdk import AsyncMarketplaceClient, MarketplaceClient
from agent_marketplace_sdk.models import ReviewCreate


@pytest.mark.integration
class TestAgentFlow:
    """Integration tests for complete agent workflow."""

    def test_complete_agent_flow(self, mock_api_with_download, temp_dir):
        """Test complete agent workflow."""
        with MarketplaceClient(api_key="test-key") as client:
            # Search agents
            agents = client.search.search("code review")
            assert len(agents) > 0

            # Get agent details
            agent = client.agents.get(agents[0].slug)
            assert agent.name is not None

            # Install agent
            install_path = client.agents.install(agent.slug, path=temp_dir)
            assert install_path.exists()

            # Star agent
            client.agents.star(agent.slug)

            # Leave review
            review = client.reviews.create(
                agent.slug,
                ReviewCreate(rating=5, comment="Great agent!"),
            )
            assert review.rating == 5


@pytest.mark.integration
class TestAsyncAgentFlow:
    """Integration tests for async agent workflow."""

    @pytest.mark.asyncio
    async def test_complete_async_agent_flow(self, mock_api_with_download, temp_dir):
        """Test complete async agent workflow."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            # Search agents
            agents = await client.search.search("code review")
            assert len(agents) > 0

            # Get agent details
            agent = await client.agents.get(agents[0].slug)
            assert agent.name is not None

            # Install agent
            install_path = await client.agents.install(agent.slug, path=temp_dir)
            assert install_path.exists()

            # Star agent
            await client.agents.star(agent.slug)

            # Leave review
            review = await client.reviews.create(
                agent.slug,
                ReviewCreate(rating=5, comment="Great agent!"),
            )
            assert review.rating == 5
