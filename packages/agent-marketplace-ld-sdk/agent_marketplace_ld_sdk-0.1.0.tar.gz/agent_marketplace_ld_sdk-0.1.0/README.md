# agent-marketplace-ld-sdk

[![PyPI](https://img.shields.io/pypi/v/agent-marketplace-ld-sdk.svg)](https://pypi.org/project/agent-marketplace-ld-sdk/)
[![CI](https://github.com/kmcallorum/agent-marketplace-ld-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/kmcallorum/agent-marketplace-ld-sdk/actions)
[![codecov](https://codecov.io/gh/kmcallorum/agent-marketplace-ld-sdk/graph/badge.svg)](https://codecov.io/gh/kmcallorum/agent-marketplace-ld-sdk)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Python SDK for Agent Marketplace. Discover, install, and publish AI agents programmatically with a clean, type-safe API.

## Features

- **Search & Discovery**: Find agents by capability, category, or rating
- **Install Agents**: One-line agent installation with version support
- **Publish Agents**: Programmatic agent publishing and updates
- **Social Features**: Stars, reviews, and ratings
- **Async Support**: Full async/await support with identical API
- **Type Safe**: Complete type hints and Pydantic models
- **100% Tested**: Comprehensive test coverage

## Installation

```bash
pip install agent-marketplace-ld-sdk
```

## Quick Start

```python
from agent_marketplace_sdk import MarketplaceClient

# Initialize client
client = MarketplaceClient(api_key="your-api-key")

# Search agents
agents = client.search.search("code review")

# Install agent
client.agents.install("advanced-pm")

# Close client
client.close()
```

### Using Context Manager

```python
from agent_marketplace_sdk import MarketplaceClient

with MarketplaceClient(api_key="your-api-key") as client:
    agents = client.agents.list()
    for agent in agents:
        print(f"{agent.name}: {agent.rating} stars")
```

### Async Usage

```python
import asyncio
from agent_marketplace_sdk import AsyncMarketplaceClient

async def main():
    async with AsyncMarketplaceClient(api_key="your-api-key") as client:
        agents = await client.search.search("testing")

        # Fetch multiple agents in parallel
        details = await asyncio.gather(*[
            client.agents.get(agent.slug)
            for agent in agents[:5]
        ])

asyncio.run(main())
```

## Configuration

### Environment Variables

```bash
export MARKETPLACE_API_KEY="your-api-key"
export MARKETPLACE_BASE_URL="https://api.agent-marketplace.com"  # optional
```

### From File

```python
from agent_marketplace_sdk import MarketplaceConfig

config = MarketplaceConfig.from_file("~/.marketplace/config.toml")
```

## API Reference

### Client

```python
from agent_marketplace_sdk import MarketplaceClient

client = MarketplaceClient(
    api_key="your-api-key",
    base_url="https://api.agent-marketplace.com",  # default
    timeout=30.0,  # seconds
    max_retries=3,
)
```

### Agents

```python
# List agents
agents = client.agents.list(category="pm", limit=20, offset=0)

# Get agent
agent = client.agents.get("advanced-pm")

# Get versions
versions = client.agents.get_versions("advanced-pm")

# Install agent
path = client.agents.install("advanced-pm", version="1.2.0", path="./agents")

# Publish agent
from agent_marketplace_sdk.models import AgentCreate

agent_data = AgentCreate(
    name="My Agent",
    description="Does amazing things",
    category="testing",
    version="1.0.0",
)
agent = client.agents.publish(agent_data, code_path="./my-agent")

# Update agent
client.agents.update("my-agent", version="1.1.0", code_path="./my-agent")

# Star/Unstar
client.agents.star("advanced-pm")
client.agents.unstar("advanced-pm")

# Delete
client.agents.delete("my-agent")
```

### Search

```python
agents = client.search.search(
    query="code review",
    category="testing",
    min_rating=4.0,
    sort="downloads",  # relevance, downloads, stars, rating
    limit=20,
)
```

### Users

```python
# Get current user
me = client.users.me()

# Get user profile
user = client.users.get("username")

# Get user's agents
agents = client.users.get_agents("username")

# Get starred agents
starred = client.users.get_starred("username")
```

### Reviews

```python
from agent_marketplace_sdk.models import ReviewCreate

# List reviews
reviews = client.reviews.list("advanced-pm")

# Create review
review = client.reviews.create(
    "advanced-pm",
    ReviewCreate(rating=5, comment="Great agent!"),
)

# Update review
client.reviews.update("advanced-pm", review_id=1, review=ReviewCreate(rating=4))

# Delete review
client.reviews.delete("advanced-pm", review_id=1)

# Mark helpful
client.reviews.mark_helpful("advanced-pm", review_id=1)
```

### Categories

```python
# List categories
categories = client.categories.list()

# Get category
category = client.categories.get("pm")
```

### Analytics

```python
# Get agent analytics
analytics = client.analytics.get_agent_analytics("advanced-pm")

# Get trending agents
trending = client.analytics.get_trending(limit=10)
```

## Error Handling

```python
from agent_marketplace_sdk import MarketplaceClient
from agent_marketplace_sdk.exceptions import (
    AgentNotFoundError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
)

with MarketplaceClient(api_key="your-api-key") as client:
    try:
        agent = client.agents.get("nonexistent")
    except AgentNotFoundError:
        print("Agent not found")
    except AuthenticationError:
        print("Invalid API key")
    except RateLimitError:
        print("Rate limit exceeded")
    except ValidationError as e:
        print(f"Validation error: {e}")
```

## Development

```bash
# Clone repository
git clone https://github.com/kmcallorum/agent-marketplace-ld-sdk.git
cd agent-marketplace-ld-sdk

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check src tests

# Run type checking
mypy src
```

## License

MIT License - see [LICENSE](LICENSE) for details.
