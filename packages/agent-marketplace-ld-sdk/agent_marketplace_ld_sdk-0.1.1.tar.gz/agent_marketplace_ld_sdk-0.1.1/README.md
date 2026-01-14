# Agent Marketplace SDK

[![PyPI](https://img.shields.io/pypi/v/agent-marketplace-ld-sdk.svg)](https://pypi.org/project/agent-marketplace-ld-sdk/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/agent-marketplace-ld-sdk.svg)](https://pypi.org/project/agent-marketplace-ld-sdk/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![CI](https://github.com/kmcallorum/agent-marketplace-ld-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/kmcallorum/agent-marketplace-ld-sdk/actions/workflows/ci.yml)
[![CodeQL](https://github.com/kmcallorum/agent-marketplace-ld-sdk/actions/workflows/codeql.yml/badge.svg)](https://github.com/kmcallorum/agent-marketplace-ld-sdk/actions/workflows/codeql.yml)
[![Security](https://github.com/kmcallorum/agent-marketplace-ld-sdk/actions/workflows/security.yml/badge.svg)](https://github.com/kmcallorum/agent-marketplace-ld-sdk/actions/workflows/security.yml)
[![Coverage](https://github.com/kmcallorum/agent-marketplace-ld-sdk/actions/workflows/coverage.yml/badge.svg)](https://github.com/kmcallorum/agent-marketplace-ld-sdk/actions/workflows/coverage.yml)

[![codecov](https://codecov.io/gh/kmcallorum/agent-marketplace-ld-sdk/graph/badge.svg)](https://codecov.io/gh/kmcallorum/agent-marketplace-ld-sdk)
[![Snyk](https://snyk.io/test/github/kmcallorum/agent-marketplace-ld-sdk/badge.svg)](https://snyk.io/test/github/kmcallorum/agent-marketplace-ld-sdk)
[![Dependabot](https://img.shields.io/badge/dependabot-enabled-025E8C?logo=dependabot)](https://github.com/kmcallorum/agent-marketplace-ld-sdk/security/dependabot)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](http://mypy-lang.org/)
[![pytest](https://img.shields.io/badge/tested%20with-pytest-blue.svg)](https://docs.pytest.org/)
[![pytest-agents](https://img.shields.io/badge/tested%20with-pytest--agents-purple.svg)](https://github.com/kmcallorum/pytest-agents)

---

Official Python SDK for Agent Marketplace. Discover, install, and publish AI agents programmatically with a clean, type-safe API.

## Features

- **Search & Discovery**: Find agents by capability, category, or rating
- **Install Agents**: One-line agent installation with version support
- **Publish Agents**: Programmatic agent publishing and updates
- **Social Features**: Stars, reviews, and ratings
- **Async Support**: Full async/await support with identical API
- **Type Safe**: Complete type hints and Pydantic models
- **100% Test Coverage**: Comprehensive test suite with pytest

## Requirements

- Python 3.11 or higher
- An Agent Marketplace API key ([get one here](https://agent-marketplace.com/settings/api))

## Installation

### From PyPI (Recommended)

```bash
pip install agent-marketplace-ld-sdk
```

### From Source

```bash
git clone https://github.com/kmcallorum/agent-marketplace-ld-sdk.git
cd agent-marketplace-ld-sdk
pip install -e .
```

### With Optional Dependencies

```bash
# Development dependencies (testing, linting, type checking)
pip install agent-marketplace-ld-sdk[dev]
```

## Quick Start

### Basic Usage

```python
from agent_marketplace_sdk import MarketplaceClient

# Initialize client with API key
client = MarketplaceClient(api_key="your-api-key")

# Search for agents
agents = client.search.search("code review")
for agent in agents:
    print(f"{agent.name} - {agent.rating} stars")

# Install an agent
path = client.agents.install("advanced-pm")
print(f"Agent installed to: {path}")

# Always close the client when done
client.close()
```

### Using Context Manager (Recommended)

```python
from agent_marketplace_sdk import MarketplaceClient

with MarketplaceClient(api_key="your-api-key") as client:
    # List all agents
    agents = client.agents.list()
    for agent in agents:
        print(f"{agent.name}: {agent.downloads} downloads, {agent.stars} stars")

    # Get a specific agent
    agent = client.agents.get("advanced-pm")
    print(f"Description: {agent.description}")
    print(f"Current version: {agent.current_version}")
```

### Async Usage

```python
import asyncio
from agent_marketplace_sdk import AsyncMarketplaceClient

async def main():
    async with AsyncMarketplaceClient(api_key="your-api-key") as client:
        # Search for testing agents
        agents = await client.search.search("testing")

        # Fetch multiple agent details in parallel
        details = await asyncio.gather(*[
            client.agents.get(agent.slug)
            for agent in agents[:5]
        ])

        for agent in details:
            print(f"{agent.name}: {agent.description}")

asyncio.run(main())
```

## Configuration

### Environment Variables

Set your API key as an environment variable:

```bash
export MARKETPLACE_API_KEY="your-api-key"

# Optional: Custom base URL (defaults to https://api.agent-marketplace.com)
export MARKETPLACE_BASE_URL="https://api.agent-marketplace.com"
```

Then use without passing the key:

```python
from agent_marketplace_sdk import MarketplaceClient

# Will automatically use MARKETPLACE_API_KEY environment variable
with MarketplaceClient() as client:
    agents = client.agents.list()
```

### Configuration File

Create a config file at `~/.marketplace/config.toml`:

```toml
[marketplace]
api_key = "your-api-key"
base_url = "https://api.agent-marketplace.com"
timeout = 30.0
max_retries = 3
```

Then load it:

```python
from agent_marketplace_sdk import MarketplaceClient, MarketplaceConfig

config = MarketplaceConfig.from_file("~/.marketplace/config.toml")
client = MarketplaceClient(
    api_key=config.api_key,
    base_url=config.base_url,
    timeout=config.timeout,
)
```

### Client Options

```python
from agent_marketplace_sdk import MarketplaceClient

client = MarketplaceClient(
    api_key="your-api-key",           # Required (or set MARKETPLACE_API_KEY)
    base_url="https://...",           # API base URL (optional)
    timeout=30.0,                      # Request timeout in seconds (default: 30)
    max_retries=3,                     # Max retry attempts (default: 3)
)
```

## API Reference

### Agents

```python
# List agents with optional filters
agents = client.agents.list(
    category="pm",      # Filter by category
    limit=20,           # Max results (default: 20)
    offset=0,           # Pagination offset
)

# Get agent by slug
agent = client.agents.get("advanced-pm")

# Get all versions of an agent
versions = client.agents.get_versions("advanced-pm")

# Install agent to local directory
path = client.agents.install(
    "advanced-pm",
    version="1.2.0",        # Optional: specific version
    path="./agents",        # Optional: install directory
)

# Publish a new agent
from agent_marketplace_sdk.models import AgentCreate

agent_data = AgentCreate(
    name="My Agent",
    description="An agent that does amazing things",
    category="testing",
    version="1.0.0",
)
agent = client.agents.publish(agent_data, code_path="./my-agent")

# Update an existing agent
client.agents.update(
    "my-agent",
    version="1.1.0",
    code_path="./my-agent",
    changelog="Bug fixes and improvements",
)

# Star/Unstar an agent
client.agents.star("advanced-pm")
client.agents.unstar("advanced-pm")

# Delete your agent
client.agents.delete("my-agent")
```

### Search

```python
# Search agents with filters
agents = client.search.search(
    query="code review",        # Search query
    category="testing",         # Filter by category
    min_rating=4.0,             # Minimum rating
    sort="downloads",           # Sort by: relevance, downloads, stars, rating
    limit=20,                   # Max results
)
```

### Users

```python
# Get current authenticated user
me = client.users.me()
print(f"Logged in as: {me.username}")
print(f"Reputation: {me.reputation}")

# Get any user's profile
user = client.users.get("username")

# Get user's published agents
agents = client.users.get_agents("username")

# Get user's starred agents
starred = client.users.get_starred("username")
```

### Reviews

```python
from agent_marketplace_sdk.models import ReviewCreate

# List reviews for an agent
reviews = client.reviews.list("advanced-pm")
for review in reviews:
    print(f"{review.user.username}: {review.rating}/5 - {review.comment}")

# Create a review
review = client.reviews.create(
    "advanced-pm",
    ReviewCreate(rating=5, comment="Excellent agent! Highly recommended."),
)

# Update a review
client.reviews.update(
    "advanced-pm",
    review_id=1,
    review=ReviewCreate(rating=4, comment="Updated review"),
)

# Delete a review
client.reviews.delete("advanced-pm", review_id=1)

# Mark a review as helpful
client.reviews.mark_helpful("advanced-pm", review_id=1)
```

### Categories

```python
# List all categories
categories = client.categories.list()
for cat in categories:
    print(f"{cat.name}: {cat.agent_count} agents")

# Get a specific category
category = client.categories.get("pm")
```

### Analytics

```python
# Get analytics for your agent
analytics = client.analytics.get_agent_analytics("my-agent")
print(f"Total downloads: {analytics.total_downloads}")
print(f"Total stars: {analytics.total_stars}")
print(f"Average rating: {analytics.average_rating}")

# Get trending agents
trending = client.analytics.get_trending(limit=10)
for agent in trending:
    print(f"{agent.name}: {agent.trend_score} trend score")
```

## Error Handling

The SDK provides specific exceptions for different error scenarios:

```python
from agent_marketplace_sdk import MarketplaceClient
from agent_marketplace_sdk.exceptions import (
    MarketplaceError,       # Base exception for all SDK errors
    AgentNotFoundError,     # Agent doesn't exist (404)
    AuthenticationError,    # Invalid or missing API key (401)
    RateLimitError,         # Rate limit exceeded (429)
    ValidationError,        # Invalid request data (422)
    ServerError,            # Server-side error (5xx)
)

with MarketplaceClient(api_key="your-api-key") as client:
    try:
        agent = client.agents.get("nonexistent-agent")
    except AgentNotFoundError:
        print("Agent not found")
    except AuthenticationError:
        print("Invalid API key - check your credentials")
    except RateLimitError as e:
        print(f"Rate limited - retry after {e.retry_after} seconds")
    except ValidationError as e:
        print(f"Invalid request: {e.message}")
    except ServerError:
        print("Server error - try again later")
    except MarketplaceError as e:
        print(f"Unexpected error: {e}")
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/kmcallorum/agent-marketplace-ld-sdk.git
cd agent-marketplace-ld-sdk

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src/agent_marketplace_sdk --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_agents.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Linting with Ruff
ruff check src tests

# Auto-fix linting issues
ruff check --fix src tests

# Format code
ruff format src tests

# Type checking with mypy
mypy src

# Run all checks
ruff check src tests && ruff format --check src tests && mypy src
```

### Project Structure

```
agent-marketplace-ld-sdk/
├── src/
│   └── agent_marketplace_sdk/
│       ├── __init__.py          # Package exports
│       ├── client.py            # Sync client
│       ├── async_client.py      # Async client
│       ├── auth.py              # Authentication
│       ├── config.py            # Configuration
│       ├── exceptions.py        # Custom exceptions
│       ├── models/              # Pydantic models
│       │   ├── agent.py
│       │   ├── user.py
│       │   ├── review.py
│       │   ├── category.py
│       │   └── analytics.py
│       ├── resources/           # API resources
│       │   ├── agents.py
│       │   ├── users.py
│       │   ├── reviews.py
│       │   ├── categories.py
│       │   ├── search.py
│       │   └── analytics.py
│       └── utils/               # Utilities
│           └── zip.py
├── tests/
│   ├── conftest.py              # Pytest fixtures
│   ├── fixtures/                # Test data
│   ├── unit/                    # Unit tests
│   └── integration/             # Integration tests
├── examples/                    # Usage examples
├── docs/                        # Documentation
├── pyproject.toml               # Project configuration
└── README.md
```

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on:

- Code of Conduct
- Development workflow
- Pull request process
- Coding standards

## Security

For security vulnerabilities, please see our [Security Policy](SECURITY.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes in each release.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- [PyPI Package](https://pypi.org/project/agent-marketplace-ld-sdk/)
- [GitHub Repository](https://github.com/kmcallorum/agent-marketplace-ld-sdk)
- [Issue Tracker](https://github.com/kmcallorum/agent-marketplace-ld-sdk/issues)
- [Codecov Coverage](https://codecov.io/gh/kmcallorum/agent-marketplace-ld-sdk)
