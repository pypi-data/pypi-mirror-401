"""Authentication handling for Agent Marketplace SDK."""

from __future__ import annotations

from collections.abc import Generator
from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    pass


class BearerAuth(httpx.Auth):
    """Bearer token authentication for httpx."""

    def __init__(self, token: str) -> None:
        """Initialize bearer auth.

        Args:
            token: The API key/token for authentication.
        """
        self.token = token

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        """Add authorization header to request.

        Args:
            request: The HTTP request to authenticate.

        Yields:
            The authenticated request.
        """
        request.headers["Authorization"] = f"Bearer {self.token}"
        yield request
