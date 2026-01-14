"""Search resource operations."""

from __future__ import annotations

from typing import Any

import httpx

from agent_marketplace_sdk.exceptions import handle_response_error
from agent_marketplace_sdk.models.agent import Agent


class SearchResource:
    """Synchronous search operations."""

    def __init__(self, http: httpx.Client) -> None:
        """Initialize search resource.

        Args:
            http: HTTP client instance.
        """
        self._http = http

    def search(
        self,
        query: str,
        category: str | None = None,
        min_rating: float | None = None,
        sort: str = "relevance",
        limit: int = 20,
        offset: int = 0,
    ) -> list[Agent]:
        """Search agents.

        Args:
            query: Search query.
            category: Filter by category.
            min_rating: Minimum rating filter.
            sort: Sort by (relevance, downloads, stars, rating).
            limit: Maximum results.
            offset: Pagination offset.

        Returns:
            List of matching agents.
        """
        params: dict[str, Any] = {
            "q": query,
            "sort": sort,
            "limit": limit,
            "offset": offset,
        }
        if category:
            params["category"] = category
        if min_rating is not None:
            params["min_rating"] = min_rating

        response = self._http.get("/api/v1/search/agents", params=params)
        handle_response_error(response)
        return [Agent(**item) for item in response.json()["items"]]


class AsyncSearchResource:
    """Asynchronous search operations."""

    def __init__(self, http: httpx.AsyncClient) -> None:
        """Initialize async search resource.

        Args:
            http: Async HTTP client instance.
        """
        self._http = http

    async def search(
        self,
        query: str,
        category: str | None = None,
        min_rating: float | None = None,
        sort: str = "relevance",
        limit: int = 20,
        offset: int = 0,
    ) -> list[Agent]:
        """Search agents.

        Args:
            query: Search query.
            category: Filter by category.
            min_rating: Minimum rating filter.
            sort: Sort by (relevance, downloads, stars, rating).
            limit: Maximum results.
            offset: Pagination offset.

        Returns:
            List of matching agents.
        """
        params: dict[str, Any] = {
            "q": query,
            "sort": sort,
            "limit": limit,
            "offset": offset,
        }
        if category:
            params["category"] = category
        if min_rating is not None:
            params["min_rating"] = min_rating

        response = await self._http.get("/api/v1/search/agents", params=params)
        handle_response_error(response)
        return [Agent(**item) for item in response.json()["items"]]
