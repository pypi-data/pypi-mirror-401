# Quick Start Guide

Get started with the Agent Marketplace SDK in minutes.

## Installation

```bash
pip install agent-marketplace-ld-sdk
```

## Authentication

Get your API key from the Agent Marketplace dashboard and set it as an environment variable:

```bash
export MARKETPLACE_API_KEY="your-api-key"
```

Or pass it directly to the client:

```python
from agent_marketplace_sdk import MarketplaceClient

client = MarketplaceClient(api_key="your-api-key")
```

## Basic Usage

### Search for Agents

```python
from agent_marketplace_sdk import MarketplaceClient

with MarketplaceClient() as client:
    # Search for agents
    agents = client.search.search("code review")

    for agent in agents:
        print(f"{agent.name}: {agent.rating} stars")
```

### Install an Agent

```python
with MarketplaceClient() as client:
    # Install latest version
    path = client.agents.install("advanced-pm")
    print(f"Installed to: {path}")

    # Install specific version
    path = client.agents.install("advanced-pm", version="1.2.0")
```

### Publish an Agent

```python
from agent_marketplace_sdk import MarketplaceClient
from agent_marketplace_sdk.models import AgentCreate

with MarketplaceClient() as client:
    agent_data = AgentCreate(
        name="My Agent",
        description="Does amazing things with code analysis.",
        category="testing",
        version="1.0.0",
    )

    agent = client.agents.publish(agent_data, code_path="./my-agent")
    print(f"Published: {agent.slug}")
```

## Async Usage

```python
import asyncio
from agent_marketplace_sdk import AsyncMarketplaceClient

async def main():
    async with AsyncMarketplaceClient() as client:
        agents = await client.search.search("testing")

        # Fetch multiple agents in parallel
        details = await asyncio.gather(*[
            client.agents.get(agent.slug)
            for agent in agents[:5]
        ])

asyncio.run(main())
```

## Next Steps

- See [API_REFERENCE.md](API_REFERENCE.md) for complete API documentation
- Check [EXAMPLES.md](EXAMPLES.md) for more usage examples
- Read [AUTHENTICATION.md](AUTHENTICATION.md) for authentication details
