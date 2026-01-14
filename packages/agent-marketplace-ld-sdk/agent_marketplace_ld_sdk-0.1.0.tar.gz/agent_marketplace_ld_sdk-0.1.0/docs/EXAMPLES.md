# Examples

Practical examples for common use cases.

## Search and Filter Agents

```python
from agent_marketplace_sdk import MarketplaceClient

with MarketplaceClient() as client:
    # Basic search
    agents = client.search.search("code review")

    # Search with filters
    agents = client.search.search(
        query="testing",
        category="testing",
        min_rating=4.0,
        sort="downloads",
        limit=10,
    )

    # Browse by category
    testing_agents = client.agents.list(category="testing")

    # Get trending
    trending = client.analytics.get_trending(limit=5)
```

## Install and Manage Agents

```python
from pathlib import Path
from agent_marketplace_sdk import MarketplaceClient

with MarketplaceClient() as client:
    # Install latest version
    path = client.agents.install("advanced-pm", path="./agents")

    # Install specific version
    path = client.agents.install(
        "code-reviewer",
        version="2.0.0",
        path="./agents",
    )

    # List available versions
    versions = client.agents.get_versions("advanced-pm")
    for v in versions:
        print(f"v{v.version}: {v.changelog or 'No changelog'}")
```

## Publish and Update Agents

```python
from agent_marketplace_sdk import MarketplaceClient
from agent_marketplace_sdk.models import AgentCreate

with MarketplaceClient() as client:
    # Publish new agent
    agent_data = AgentCreate(
        name="My Code Analyzer",
        description="Analyzes code for best practices and potential issues.",
        category="testing",
        version="1.0.0",
    )

    agent = client.agents.publish(agent_data, code_path="./my-agent")
    print(f"Published: {agent.slug}")

    # Update with new version
    updated = client.agents.update(
        slug=agent.slug,
        version="1.1.0",
        code_path="./my-agent",
        changelog="Added support for TypeScript",
    )
```

## Work with Reviews

```python
from agent_marketplace_sdk import MarketplaceClient
from agent_marketplace_sdk.models import ReviewCreate

with MarketplaceClient() as client:
    # Get reviews
    reviews = client.reviews.list("advanced-pm")
    for review in reviews:
        print(f"{review.user.username}: {review.rating}/5 - {review.comment}")

    # Add a review
    review = client.reviews.create(
        "advanced-pm",
        ReviewCreate(rating=5, comment="Excellent agent! Very helpful."),
    )

    # Mark helpful
    client.reviews.mark_helpful("advanced-pm", review_id=review.id)
```

## User Operations

```python
from agent_marketplace_sdk import MarketplaceClient

with MarketplaceClient() as client:
    # Get current user profile
    me = client.users.me()
    print(f"Logged in as: {me.username}")
    print(f"Reputation: {me.reputation}")

    # Get another user's profile
    user = client.users.get("some-user")

    # Get user's published agents
    agents = client.users.get_agents("some-user")

    # Get user's starred agents
    starred = client.users.get_starred("some-user")
```

## Async Operations

```python
import asyncio
from agent_marketplace_sdk import AsyncMarketplaceClient

async def main():
    async with AsyncMarketplaceClient() as client:
        # Parallel searches
        results = await asyncio.gather(
            client.search.search("code review"),
            client.search.search("testing"),
            client.search.search("documentation"),
        )

        all_agents = [agent for agents in results for agent in agents]

        # Parallel agent fetches
        details = await asyncio.gather(*[
            client.agents.get(agent.slug)
            for agent in all_agents[:10]
        ])

        for agent in details:
            print(f"{agent.name}: {agent.downloads} downloads")

asyncio.run(main())
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

with MarketplaceClient() as client:
    try:
        agent = client.agents.get("nonexistent-agent")
    except AgentNotFoundError:
        print("Agent not found")
    except AuthenticationError:
        print("Check your API key")
    except RateLimitError:
        print("Too many requests, try again later")
    except ValidationError as e:
        print(f"Invalid input: {e}")
```

## Configuration from File

```python
from agent_marketplace_sdk import MarketplaceConfig, MarketplaceClient

# Load from file
config = MarketplaceConfig.from_file("~/.marketplace/config.toml")

# Create client with config
client = MarketplaceClient(
    api_key=config.api_key,
    base_url=config.base_url,
    timeout=config.timeout,
    max_retries=config.max_retries,
)

# Save config
config.save("~/.marketplace/config.toml")
```
