"""Category resource operations."""

from __future__ import annotations

import httpx

from agent_marketplace_sdk.exceptions import handle_response_error
from agent_marketplace_sdk.models.category import Category


class CategoriesResource:
    """Synchronous category operations."""

    def __init__(self, http: httpx.Client) -> None:
        """Initialize categories resource.

        Args:
            http: HTTP client instance.
        """
        self._http = http

    def list(self) -> list[Category]:
        """List all categories.

        Returns:
            List of categories.
        """
        response = self._http.get("/api/v1/categories")
        handle_response_error(response)
        return [Category(**item) for item in response.json()["items"]]

    def get(self, slug: str) -> Category:
        """Get category by slug.

        Args:
            slug: Category slug.

        Returns:
            Category details.
        """
        response = self._http.get(f"/api/v1/categories/{slug}")
        handle_response_error(response)
        return Category(**response.json())


class AsyncCategoriesResource:
    """Asynchronous category operations."""

    def __init__(self, http: httpx.AsyncClient) -> None:
        """Initialize async categories resource.

        Args:
            http: Async HTTP client instance.
        """
        self._http = http

    async def list(self) -> list[Category]:
        """List all categories.

        Returns:
            List of categories.
        """
        response = await self._http.get("/api/v1/categories")
        handle_response_error(response)
        return [Category(**item) for item in response.json()["items"]]

    async def get(self, slug: str) -> Category:
        """Get category by slug.

        Args:
            slug: Category slug.

        Returns:
            Category details.
        """
        response = await self._http.get(f"/api/v1/categories/{slug}")
        handle_response_error(response)
        return Category(**response.json())
