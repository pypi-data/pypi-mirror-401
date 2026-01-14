"""Integration tests for publish operations."""

import pytest

from agent_marketplace_sdk import AsyncMarketplaceClient, MarketplaceClient
from agent_marketplace_sdk.models import AgentCreate


@pytest.mark.integration
class TestPublishFlow:
    """Integration tests for publish workflow."""

    def test_publish_agent_flow(self, mock_api, sample_agent_dir):
        """Test publishing an agent."""
        with MarketplaceClient(api_key="test-key") as client:
            # Create agent data
            agent_data = AgentCreate(
                name="My Test Agent",
                description="A test agent for integration testing.",
                category="testing",
                version="1.0.0",
            )

            # Publish agent
            agent = client.agents.publish(agent_data, sample_agent_dir)
            assert agent is not None

            # Update agent
            updated_agent = client.agents.update(
                agent.slug,
                version="1.1.0",
                code_path=sample_agent_dir,
                changelog="Added new features",
            )
            assert updated_agent is not None


@pytest.mark.integration
class TestAsyncPublishFlow:
    """Integration tests for async publish workflow."""

    @pytest.mark.asyncio
    async def test_async_publish_agent_flow(self, mock_api, sample_agent_dir):
        """Test publishing an agent asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            # Create agent data
            agent_data = AgentCreate(
                name="My Test Agent",
                description="A test agent for integration testing.",
                category="testing",
                version="1.0.0",
            )

            # Publish agent
            agent = await client.agents.publish(agent_data, sample_agent_dir)
            assert agent is not None

            # Update agent
            updated_agent = await client.agents.update(
                agent.slug,
                version="1.1.0",
                code_path=sample_agent_dir,
                changelog="Added new features",
            )
            assert updated_agent is not None
