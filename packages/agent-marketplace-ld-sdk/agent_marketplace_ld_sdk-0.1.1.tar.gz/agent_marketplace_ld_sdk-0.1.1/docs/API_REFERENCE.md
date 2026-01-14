# API Reference

Complete API documentation for the Agent Marketplace SDK.

## Client

### MarketplaceClient

Synchronous client for the Agent Marketplace API.

```python
from agent_marketplace_sdk import MarketplaceClient

client = MarketplaceClient(
    api_key: str | None = None,      # API key (or MARKETPLACE_API_KEY env var)
    base_url: str = "https://api.agent-marketplace.com",
    timeout: float = 30.0,           # Request timeout in seconds
    max_retries: int = 3,            # Maximum retry attempts
)
```

### AsyncMarketplaceClient

Asynchronous client with identical API.

```python
from agent_marketplace_sdk import AsyncMarketplaceClient

async with AsyncMarketplaceClient(api_key="...") as client:
    # Use async methods
    agents = await client.agents.list()
```

## Resources

### Agents

#### list

List agents with optional filtering.

```python
agents = client.agents.list(
    category: str | None = None,  # Filter by category
    limit: int = 20,              # Maximum results
    offset: int = 0,              # Pagination offset
) -> list[Agent]
```

#### get

Get agent by slug.

```python
agent = client.agents.get(slug: str) -> Agent
```

#### get_versions

Get all versions of an agent.

```python
versions = client.agents.get_versions(slug: str) -> list[AgentVersion]
```

#### install

Install agent locally.

```python
path = client.agents.install(
    slug: str,
    version: str | None = None,  # Specific version (default: latest)
    path: Path | str = ".",      # Installation directory
) -> Path
```

#### publish

Publish a new agent.

```python
agent = client.agents.publish(
    agent_data: AgentCreate,
    code_path: Path | str,
) -> Agent
```

#### update

Update agent with new version.

```python
agent = client.agents.update(
    slug: str,
    version: str,
    code_path: Path | str,
    changelog: str | None = None,
) -> Agent
```

#### delete

Delete an agent.

```python
client.agents.delete(slug: str) -> None
```

#### star / unstar

Star or unstar an agent.

```python
client.agents.star(slug: str) -> None
client.agents.unstar(slug: str) -> None
```

### Search

#### search

Search agents with filters.

```python
agents = client.search.search(
    query: str,
    category: str | None = None,
    min_rating: float | None = None,
    sort: str = "relevance",     # relevance, downloads, stars, rating
    limit: int = 20,
    offset: int = 0,
) -> list[Agent]
```

### Users

#### get

Get user by username.

```python
user = client.users.get(username: str) -> UserProfile
```

#### me

Get current authenticated user.

```python
user = client.users.me() -> UserProfile
```

#### get_agents

Get agents published by user.

```python
agents = client.users.get_agents(username: str) -> list[Agent]
```

#### get_starred

Get agents starred by user.

```python
agents = client.users.get_starred(username: str) -> list[Agent]
```

### Reviews

#### list

List reviews for an agent.

```python
reviews = client.reviews.list(
    agent_slug: str,
    limit: int = 20,
    offset: int = 0,
) -> list[Review]
```

#### create

Create a review.

```python
review = client.reviews.create(
    agent_slug: str,
    review: ReviewCreate,
) -> Review
```

#### update

Update a review.

```python
review = client.reviews.update(
    agent_slug: str,
    review_id: int,
    review: ReviewCreate,
) -> Review
```

#### delete

Delete a review.

```python
client.reviews.delete(agent_slug: str, review_id: int) -> None
```

#### mark_helpful

Mark review as helpful.

```python
client.reviews.mark_helpful(agent_slug: str, review_id: int) -> None
```

### Categories

#### list

List all categories.

```python
categories = client.categories.list() -> list[Category]
```

#### get

Get category by slug.

```python
category = client.categories.get(slug: str) -> Category
```

### Analytics

#### get_agent_analytics

Get analytics for an agent.

```python
analytics = client.analytics.get_agent_analytics(agent_slug: str) -> AgentAnalytics
```

#### get_trending

Get trending agents.

```python
trending = client.analytics.get_trending(limit: int = 10) -> list[TrendingAgent]
```

## Models

### Agent

```python
class Agent:
    id: int
    name: str
    slug: str
    description: str
    author: User
    current_version: str
    downloads: int
    stars: int
    rating: float
    category: str
    is_public: bool
    is_validated: bool
    created_at: datetime
    updated_at: datetime
```

### AgentCreate

```python
class AgentCreate:
    name: str                    # 3-100 characters
    description: str             # 10-1000 characters
    category: str
    version: str = "1.0.0"       # Semantic version
```

### Review

```python
class Review:
    id: int
    agent_id: int
    agent_slug: str
    user: User
    rating: int                  # 1-5
    comment: str | None
    helpful_count: int
    created_at: datetime
    updated_at: datetime
```

### ReviewCreate

```python
class ReviewCreate:
    rating: int                  # 1-5
    comment: str | None          # Max 1000 characters
```

## Exceptions

```python
from agent_marketplace_sdk.exceptions import (
    MarketplaceError,      # Base exception
    AgentNotFoundError,    # Agent not found (404)
    UserNotFoundError,     # User not found (404)
    AuthenticationError,   # Invalid API key (401)
    ValidationError,       # Validation failed (422)
    RateLimitError,        # Rate limit exceeded (429)
    NetworkError,          # Network error
    ConfigurationError,    # Configuration error
)
```
