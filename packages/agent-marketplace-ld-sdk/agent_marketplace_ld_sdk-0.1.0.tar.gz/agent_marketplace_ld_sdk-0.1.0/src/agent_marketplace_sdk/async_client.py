"""Asynchronous Agent Marketplace client."""

from __future__ import annotations

import os
from types import TracebackType
from typing import Any

import httpx

from agent_marketplace_sdk.auth import BearerAuth
from agent_marketplace_sdk.config import DEFAULT_BASE_URL, DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT
from agent_marketplace_sdk.exceptions import ConfigurationError
from agent_marketplace_sdk.resources.agents import AsyncAgentsResource
from agent_marketplace_sdk.resources.analytics import AsyncAnalyticsResource
from agent_marketplace_sdk.resources.categories import AsyncCategoriesResource
from agent_marketplace_sdk.resources.reviews import AsyncReviewsResource
from agent_marketplace_sdk.resources.search import AsyncSearchResource
from agent_marketplace_sdk.resources.users import AsyncUsersResource


class AsyncMarketplaceClient:
    """Asynchronous Agent Marketplace client.

    Example:
        >>> async with AsyncMarketplaceClient(api_key="your-api-key") as client:
        ...     agents = await client.search.search("code review")
        ...     await client.agents.install("advanced-pm", version="1.2.0")
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        """Initialize async marketplace client.

        Args:
            api_key: API key (or set MARKETPLACE_API_KEY env var).
            base_url: API base URL.
            timeout: Request timeout in seconds.
            max_retries: Maximum retry attempts.

        Raises:
            ConfigurationError: If API key is not provided.
        """
        self._api_key = api_key or os.getenv("MARKETPLACE_API_KEY")
        self._base_url = base_url
        self._timeout = timeout
        self._max_retries = max_retries

        if not self._api_key:
            raise ConfigurationError(
                "API key required. Set MARKETPLACE_API_KEY env var or pass api_key parameter."
            )

        transport = httpx.AsyncHTTPTransport(retries=max_retries)
        self._http = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            auth=BearerAuth(self._api_key),
            transport=transport,
        )

        # Initialize resources
        self.agents = AsyncAgentsResource(self._http)
        self.users = AsyncUsersResource(self._http)
        self.reviews = AsyncReviewsResource(self._http)
        self.categories = AsyncCategoriesResource(self._http)
        self.search = AsyncSearchResource(self._http)
        self.analytics = AsyncAnalyticsResource(self._http)

    @property
    def api_key(self) -> str:
        """Get the API key."""
        return self._api_key  # type: ignore[return-value]

    @property
    def base_url(self) -> str:
        """Get the base URL."""
        return self._base_url

    async def close(self) -> None:
        """Close HTTP client."""
        await self._http.aclose()

    async def __aenter__(self) -> AsyncMarketplaceClient:
        """Enter async context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit async context manager."""
        await self.close()

    async def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> httpx.Response:
        """Make async HTTP request.

        Args:
            method: HTTP method.
            path: Request path.
            **kwargs: Additional request arguments.

        Returns:
            HTTP response.
        """
        return await self._http.request(method, path, **kwargs)
