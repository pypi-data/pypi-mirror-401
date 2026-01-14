"""Analytics resource operations."""

from __future__ import annotations

import httpx

from agent_marketplace_sdk.exceptions import AgentNotFoundError, handle_response_error
from agent_marketplace_sdk.models.analytics import AgentAnalytics, TrendingAgent


class AnalyticsResource:
    """Synchronous analytics operations."""

    def __init__(self, http: httpx.Client) -> None:
        """Initialize analytics resource.

        Args:
            http: HTTP client instance.
        """
        self._http = http

    def get_agent_analytics(self, agent_slug: str) -> AgentAnalytics:
        """Get analytics for an agent.

        Args:
            agent_slug: Agent slug.

        Returns:
            Agent analytics.

        Raises:
            AgentNotFoundError: If agent doesn't exist.
        """
        response = self._http.get(f"/api/v1/agents/{agent_slug}/analytics")
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{agent_slug}' not found")
        handle_response_error(response)
        return AgentAnalytics(**response.json())

    def get_trending(self, limit: int = 10) -> list[TrendingAgent]:
        """Get trending agents.

        Args:
            limit: Maximum results.

        Returns:
            List of trending agents.
        """
        response = self._http.get("/api/v1/analytics/trending", params={"limit": limit})
        handle_response_error(response)
        return [TrendingAgent(**item) for item in response.json()["items"]]


class AsyncAnalyticsResource:
    """Asynchronous analytics operations."""

    def __init__(self, http: httpx.AsyncClient) -> None:
        """Initialize async analytics resource.

        Args:
            http: Async HTTP client instance.
        """
        self._http = http

    async def get_agent_analytics(self, agent_slug: str) -> AgentAnalytics:
        """Get analytics for an agent.

        Args:
            agent_slug: Agent slug.

        Returns:
            Agent analytics.

        Raises:
            AgentNotFoundError: If agent doesn't exist.
        """
        response = await self._http.get(f"/api/v1/agents/{agent_slug}/analytics")
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{agent_slug}' not found")
        handle_response_error(response)
        return AgentAnalytics(**response.json())

    async def get_trending(self, limit: int = 10) -> list[TrendingAgent]:
        """Get trending agents.

        Args:
            limit: Maximum results.

        Returns:
            List of trending agents.
        """
        response = await self._http.get("/api/v1/analytics/trending", params={"limit": limit})
        handle_response_error(response)
        return [TrendingAgent(**item) for item in response.json()["items"]]
