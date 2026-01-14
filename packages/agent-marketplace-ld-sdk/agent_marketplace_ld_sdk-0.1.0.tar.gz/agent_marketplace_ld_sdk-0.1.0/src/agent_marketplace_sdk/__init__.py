"""Agent Marketplace SDK - Official Python client for Agent Marketplace."""

from agent_marketplace_sdk.async_client import AsyncMarketplaceClient
from agent_marketplace_sdk.client import MarketplaceClient
from agent_marketplace_sdk.config import MarketplaceConfig
from agent_marketplace_sdk.exceptions import (
    AgentNotFoundError,
    AuthenticationError,
    ConfigurationError,
    MarketplaceError,
    NetworkError,
    RateLimitError,
    UserNotFoundError,
    ValidationError,
)
from agent_marketplace_sdk.models import (
    Agent,
    AgentAnalytics,
    AgentCreate,
    AgentSummary,
    AgentVersion,
    Category,
    DownloadStats,
    Review,
    ReviewCreate,
    TrendingAgent,
    User,
    UserProfile,
)

__version__ = "0.1.0"

__all__ = [
    # Clients
    "MarketplaceClient",
    "AsyncMarketplaceClient",
    # Config
    "MarketplaceConfig",
    # Models
    "Agent",
    "AgentCreate",
    "AgentSummary",
    "AgentVersion",
    "User",
    "UserProfile",
    "Review",
    "ReviewCreate",
    "Category",
    "AgentAnalytics",
    "DownloadStats",
    "TrendingAgent",
    # Exceptions
    "MarketplaceError",
    "AgentNotFoundError",
    "UserNotFoundError",
    "AuthenticationError",
    "ValidationError",
    "NetworkError",
    "RateLimitError",
    "ConfigurationError",
]
