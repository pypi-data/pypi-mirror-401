"""Tests for users resource."""

import pytest
from httpx import Response

from agent_marketplace_sdk import AsyncMarketplaceClient, MarketplaceClient
from agent_marketplace_sdk.exceptions import UserNotFoundError


class TestUsersResource:
    """Tests for UsersResource."""

    def test_get_user(self, mock_api):
        """Test getting user by username."""
        with MarketplaceClient(api_key="test-key") as client:
            user = client.users.get("testuser")
            assert user.username == "testuser"
            assert user.email == "test@example.com"

    def test_get_user_not_found(self, mock_api):
        """Test getting nonexistent user."""
        with MarketplaceClient(api_key="test-key") as client:
            with pytest.raises(UserNotFoundError):
                client.users.get("nonexistent")

    def test_me(self, mock_api):
        """Test getting current user."""
        with MarketplaceClient(api_key="test-key") as client:
            user = client.users.me()
            assert user.username == "testuser"

    def test_get_agents(self, mock_api):
        """Test getting user's agents."""
        with MarketplaceClient(api_key="test-key") as client:
            agents = client.users.get_agents("testuser")
            assert len(agents) == 2

    def test_get_agents_not_found(self, mock_api):
        """Test getting agents for nonexistent user."""
        mock_api.get("/api/v1/users/nonexistent/agents").mock(return_value=Response(404))
        with MarketplaceClient(api_key="test-key") as client:
            with pytest.raises(UserNotFoundError):
                client.users.get_agents("nonexistent")

    def test_get_starred(self, mock_api):
        """Test getting user's starred agents."""
        with MarketplaceClient(api_key="test-key") as client:
            agents = client.users.get_starred("testuser")
            assert len(agents) == 2

    def test_get_starred_not_found(self, mock_api):
        """Test getting starred for nonexistent user."""
        mock_api.get("/api/v1/users/nonexistent/starred").mock(return_value=Response(404))
        with MarketplaceClient(api_key="test-key") as client:
            with pytest.raises(UserNotFoundError):
                client.users.get_starred("nonexistent")


class TestAsyncUsersResource:
    """Tests for AsyncUsersResource."""

    @pytest.mark.asyncio
    async def test_get_user(self, mock_api):
        """Test getting user by username asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            user = await client.users.get("testuser")
            assert user.username == "testuser"

    @pytest.mark.asyncio
    async def test_get_user_not_found(self, mock_api):
        """Test getting nonexistent user."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            with pytest.raises(UserNotFoundError):
                await client.users.get("nonexistent")

    @pytest.mark.asyncio
    async def test_me(self, mock_api):
        """Test getting current user asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            user = await client.users.me()
            assert user.username == "testuser"

    @pytest.mark.asyncio
    async def test_get_agents(self, mock_api):
        """Test getting user's agents asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            agents = await client.users.get_agents("testuser")
            assert len(agents) == 2

    @pytest.mark.asyncio
    async def test_get_agents_not_found(self, mock_api):
        """Test getting agents for nonexistent user."""
        mock_api.get("/api/v1/users/nonexistent/agents").mock(return_value=Response(404))
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            with pytest.raises(UserNotFoundError):
                await client.users.get_agents("nonexistent")

    @pytest.mark.asyncio
    async def test_get_starred(self, mock_api):
        """Test getting user's starred agents asynchronously."""
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            agents = await client.users.get_starred("testuser")
            assert len(agents) == 2

    @pytest.mark.asyncio
    async def test_get_starred_not_found(self, mock_api):
        """Test getting starred for nonexistent user."""
        mock_api.get("/api/v1/users/nonexistent/starred").mock(return_value=Response(404))
        async with AsyncMarketplaceClient(api_key="test-key") as client:
            with pytest.raises(UserNotFoundError):
                await client.users.get_starred("nonexistent")
