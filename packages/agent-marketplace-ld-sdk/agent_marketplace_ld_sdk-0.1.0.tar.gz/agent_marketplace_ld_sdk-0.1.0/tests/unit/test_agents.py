"""Tests for agents resource."""

import pytest
from httpx import Response

from agent_marketplace_sdk import AsyncMarketplaceClient, MarketplaceClient
from agent_marketplace_sdk.exceptions import AgentNotFoundError
from agent_marketplace_sdk.models import AgentCreate


class TestAgentsResource:
    """Tests for AgentsResource."""

    def test_list_agents(self, mock_api):
        """Test listing agents."""
        with MarketplaceClient(api_key="test-key") as client:
            agents = client.agents.list()
            assert len(agents) == 2
            assert agents[0].name == "Advanced PM"
            assert agents[0].slug == "advanced-pm"

    def test_list_agents_with_filters(self, mock_api):
        """Test listing agents with filters."""
        with MarketplaceClient(api_key="test-key") as client:
            agents = client.agents.list(category="pm", limit=10, offset=0)
            assert len(agents) == 2

    def test_get_agent(self, mock_api):
        """Test getting agent by slug."""
        with MarketplaceClient(api_key="test-key") as client:
            agent = client.agents.get("advanced-pm")
            assert agent.name == "Advanced PM"
            assert agent.stars == 50

    def test_get_agent_not_found(self, mock_api):
        """Test getting nonexistent agent raises error."""
        with MarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                client.agents.get("nonexistent")

    def test_get_versions(self, mock_api):
        """Test getting agent versions."""
        with MarketplaceClient(api_key="test-key") as client:
            versions = client.agents.get_versions("advanced-pm")
            assert len(versions) == 1
            assert versions[0].version == "1.2.0"

    def test_get_versions_not_found(self, mock_api):
        """Test getting versions for nonexistent agent."""
        mock_api.get("/api/v1/agents/nonexistent/versions").mock(return_value=Response(404))
        with MarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                client.agents.get_versions("nonexistent")

    def test_install(self, mock_api_with_download, temp_dir):
        """Test installing agent."""
        with MarketplaceClient(api_key="test-key") as client:
            path = client.agents.install("advanced-pm", path=temp_dir)
            assert path.exists()
            assert (path / "agent.py").exists()

    def test_install_specific_version(self, mock_api_with_download, temp_dir):
        """Test installing specific version."""
        with MarketplaceClient(api_key="test-key") as client:
            path = client.agents.install("advanced-pm", version="1.2.0", path=temp_dir)
            assert path.exists()

    def test_install_not_found(self, mock_api_with_download, temp_dir):
        """Test installing nonexistent agent."""
        with MarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                client.agents.install("nonexistent", path=temp_dir)

    def test_publish(self, mock_api, sample_agent_dir):
        """Test publishing agent."""
        with MarketplaceClient(api_key="test-key") as client:
            agent_data = AgentCreate(
                name="Sample Agent",
                description="A sample agent for testing purposes.",
                category="testing",
                version="1.0.0",
            )
            agent = client.agents.publish(agent_data, sample_agent_dir)
            assert agent.name == "Advanced PM"  # Mock returns SAMPLE_AGENT

    def test_update(self, mock_api, sample_agent_dir):
        """Test updating agent."""
        with MarketplaceClient(api_key="test-key") as client:
            agent = client.agents.update(
                "advanced-pm",
                version="1.3.0",
                code_path=sample_agent_dir,
                changelog="New features",
            )
            assert agent is not None

    def test_update_not_found(self, mock_api, sample_agent_dir):
        """Test updating nonexistent agent."""
        mock_api.put("/api/v1/agents/nonexistent").mock(return_value=Response(404))
        with MarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                client.agents.update("nonexistent", "1.0.0", sample_agent_dir)

    def test_delete(self, mock_api):
        """Test deleting agent."""
        with MarketplaceClient(api_key="test-key") as client:
            client.agents.delete("advanced-pm")

    def test_delete_not_found(self, mock_api):
        """Test deleting nonexistent agent."""
        mock_api.delete("/api/v1/agents/nonexistent").mock(return_value=Response(404))
        with MarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                client.agents.delete("nonexistent")

    def test_star(self, mock_api):
        """Test starring agent."""
        with MarketplaceClient(api_key="test-key") as client:
            client.agents.star("advanced-pm")

    def test_star_not_found(self, mock_api):
        """Test starring nonexistent agent."""
        mock_api.post("/api/v1/agents/nonexistent/star").mock(return_value=Response(404))
        with MarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                client.agents.star("nonexistent")

    def test_unstar(self, mock_api):
        """Test unstarring agent."""
        with MarketplaceClient(api_key="test-key") as client:
            client.agents.unstar("advanced-pm")

    def test_unstar_not_found(self, mock_api):
        """Test unstarring nonexistent agent."""
        mock_api.delete("/api/v1/agents/nonexistent/star").mock(return_value=Response(404))
        with MarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                client.agents.unstar("nonexistent")


class TestAsyncAgentsResource:
    """Tests for AsyncAgentsResource."""

    @pytest.mark.asyncio
    async def test_list_agents(self, mock_api):
        """Test listing agents asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            agents = await client.agents.list()
            assert len(agents) == 2

    @pytest.mark.asyncio
    async def test_list_agents_with_filters(self, mock_api):
        """Test listing agents with filters asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            agents = await client.agents.list(category="pm", limit=10, offset=0)
            assert len(agents) == 2

    @pytest.mark.asyncio
    async def test_get_agent(self, mock_api):
        """Test getting agent by slug asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            agent = await client.agents.get("advanced-pm")
            assert agent.name == "Advanced PM"

    @pytest.mark.asyncio
    async def test_get_agent_not_found(self, mock_api):
        """Test getting nonexistent agent raises error."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                await client.agents.get("nonexistent")

    @pytest.mark.asyncio
    async def test_get_versions(self, mock_api):
        """Test getting agent versions asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            versions = await client.agents.get_versions("advanced-pm")
            assert len(versions) == 1

    @pytest.mark.asyncio
    async def test_get_versions_not_found(self, mock_api):
        """Test getting versions for nonexistent agent."""
        mock_api.get("/api/v1/agents/nonexistent/versions").mock(return_value=Response(404))
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                await client.agents.get_versions("nonexistent")

    @pytest.mark.asyncio
    async def test_install(self, mock_api_with_download, temp_dir):
        """Test installing agent asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            path = await client.agents.install("advanced-pm", path=temp_dir)
            assert path.exists()

    @pytest.mark.asyncio
    async def test_install_specific_version(self, mock_api_with_download, temp_dir):
        """Test installing specific version asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            path = await client.agents.install("advanced-pm", version="1.2.0", path=temp_dir)
            assert path.exists()

    @pytest.mark.asyncio
    async def test_install_not_found(self, mock_api_with_download, temp_dir):
        """Test installing nonexistent agent."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                await client.agents.install("nonexistent", path=temp_dir)

    @pytest.mark.asyncio
    async def test_publish(self, mock_api, sample_agent_dir):
        """Test publishing agent asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            agent_data = AgentCreate(
                name="Sample Agent",
                description="A sample agent for testing purposes.",
                category="testing",
            )
            agent = await client.agents.publish(agent_data, sample_agent_dir)
            assert agent is not None

    @pytest.mark.asyncio
    async def test_update(self, mock_api, sample_agent_dir):
        """Test updating agent asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            agent = await client.agents.update(
                "advanced-pm",
                version="1.3.0",
                code_path=sample_agent_dir,
                changelog="New features",
            )
            assert agent is not None

    @pytest.mark.asyncio
    async def test_update_not_found(self, mock_api, sample_agent_dir):
        """Test updating nonexistent agent."""
        mock_api.put("/api/v1/agents/nonexistent").mock(return_value=Response(404))
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                await client.agents.update("nonexistent", "1.0.0", sample_agent_dir)

    @pytest.mark.asyncio
    async def test_delete(self, mock_api):
        """Test deleting agent asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            await client.agents.delete("advanced-pm")

    @pytest.mark.asyncio
    async def test_delete_not_found(self, mock_api):
        """Test deleting nonexistent agent."""
        mock_api.delete("/api/v1/agents/nonexistent").mock(return_value=Response(404))
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                await client.agents.delete("nonexistent")

    @pytest.mark.asyncio
    async def test_star(self, mock_api):
        """Test starring agent asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            await client.agents.star("advanced-pm")

    @pytest.mark.asyncio
    async def test_star_not_found(self, mock_api):
        """Test starring nonexistent agent."""
        mock_api.post("/api/v1/agents/nonexistent/star").mock(return_value=Response(404))
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                await client.agents.star("nonexistent")

    @pytest.mark.asyncio
    async def test_unstar(self, mock_api):
        """Test unstarring agent asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            await client.agents.unstar("advanced-pm")

    @pytest.mark.asyncio
    async def test_unstar_not_found(self, mock_api):
        """Test unstarring nonexistent agent."""
        mock_api.delete("/api/v1/agents/nonexistent/star").mock(return_value=Response(404))
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            with pytest.raises(AgentNotFoundError):
                await client.agents.unstar("nonexistent")
