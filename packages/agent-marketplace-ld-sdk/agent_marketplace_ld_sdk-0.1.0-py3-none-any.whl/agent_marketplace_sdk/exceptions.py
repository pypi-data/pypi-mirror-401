"""Custom exceptions for Agent Marketplace SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import httpx


class MarketplaceError(Exception):
    """Base exception for marketplace errors."""

    pass


class AgentNotFoundError(MarketplaceError):
    """Agent not found."""

    pass


class UserNotFoundError(MarketplaceError):
    """User not found."""

    pass


class AuthenticationError(MarketplaceError):
    """Authentication failed."""

    pass


class ValidationError(MarketplaceError):
    """Validation failed."""

    pass


class NetworkError(MarketplaceError):
    """Network error."""

    pass


class RateLimitError(MarketplaceError):
    """Rate limit exceeded."""

    pass


class ConfigurationError(MarketplaceError):
    """Configuration error."""

    pass


def handle_response_error(response: httpx.Response) -> None:
    """Handle HTTP errors and raise appropriate exceptions.

    Args:
        response: The HTTP response to check.

    Raises:
        AuthenticationError: If status is 401.
        AgentNotFoundError: If status is 404.
        ValidationError: If status is 422.
        RateLimitError: If status is 429.
        MarketplaceError: For other error status codes.
    """
    if response.status_code == 401:
        raise AuthenticationError("Invalid API key")
    elif response.status_code == 404:
        raise AgentNotFoundError("Resource not found")
    elif response.status_code == 422:
        try:
            detail = response.json().get("detail", "Validation failed")
        except Exception:
            detail = "Validation failed"
        raise ValidationError(detail)
    elif response.status_code == 429:
        raise RateLimitError("Rate limit exceeded")
    elif response.status_code >= 400:
        raise MarketplaceError(f"HTTP {response.status_code}: {response.text}")
