# agent-marketplace-ld-sdk - AGENTS.md

## Project Vision

A production-grade Python SDK for interacting with the Agent Marketplace API. Provides a clean, type-safe interface for discovering, installing, and publishing AI agents programmatically.

**Target Users:**
- Developers building tools that use the Agent Marketplace
- CI/CD pipelines automating agent deployment
- Organizations managing private agent repositories
- Power users preferring programmatic access over CLI

**Core Value Proposition:**
> "The official Python client for Agent Marketplace. Install agents with one line of code, publish with two. Type-safe, async-first, battle-tested."

## EXECUTION MODE: AUTONOMOUS

Claude should make ALL changes without asking for approval unless a critical architectural decision arises.
Quality gates at the end determine success. If all tests pass, linting succeeds, and coverage hits 100%, the implementation is acceptable.

---

## What It Does

### Core Functionality
1. **Agent Discovery**: Search, filter, browse agents
2. **Agent Installation**: Download and install agents locally
3. **Agent Publishing**: Upload agents to marketplace
4. **User Management**: Authentication, profile access
5. **Review System**: Create, read, update reviews and ratings
6. **Analytics Access**: View stats, trending agents
7. **Version Management**: Install specific versions, update agents
8. **Configuration**: Manage API credentials, preferences

### What It Does NOT Do
- ❌ NO agent execution (use pytest-agents for that)
- ❌ NO validation pipeline (API handles that)
- ❌ NO web scraping (uses official API)
- ❌ NO CLI interface (that's agent-marketplace-cli)
- ❌ NO GUI (Python library only)

---

## Project Structure

```
agent-marketplace-ld-sdk/
├── src/
│   └── agent_marketplace_sdk/
│       ├── __init__.py
│       ├── client.py              # Main MarketplaceClient class
│       ├── async_client.py        # Async MarketplaceClient
│       ├── config.py              # Configuration management
│       ├── auth.py                # Authentication handling
│       ├── exceptions.py          # Custom exceptions
│       ├── models/
│       │   ├── __init__.py
│       │   ├── agent.py           # Agent models
│       │   ├── user.py            # User models
│       │   ├── review.py          # Review models
│       │   ├── category.py        # Category models
│       │   └── analytics.py       # Analytics models
│       ├── resources/
│       │   ├── __init__.py
│       │   ├── agents.py          # Agent operations
│       │   ├── users.py           # User operations
│       │   ├── reviews.py         # Review operations
│       │   ├── categories.py      # Category operations
│       │   ├── search.py          # Search operations
│       │   └── analytics.py       # Analytics operations
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── download.py        # Download utilities
│       │   ├── upload.py          # Upload utilities
│       │   ├── validation.py      # Client-side validation
│       │   └── packaging.py       # Agent packaging utilities
│       └── py.typed
├── tests/
│   ├── unit/
│   │   ├── test_client.py
│   │   ├── test_auth.py
│   │   ├── test_agents.py
│   │   ├── test_models.py
│   │   └── test_utils.py
│   ├── integration/
│   │   ├── test_agent_flow.py
│   │   ├── test_publish_flow.py
│   │   └── test_search.py
│   ├── fixtures/
│   │   ├── mock_api_responses.py
│   │   └── sample_agents/
│   └── conftest.py
├── examples/
│   ├── basic_usage.py
│   ├── search_agents.py
│   ├── install_agent.py
│   ├── publish_agent.py
│   └── async_usage.py
├── docs/
│   ├── QUICKSTART.md
│   ├── API_REFERENCE.md
│   ├── AUTHENTICATION.md
│   └── EXAMPLES.md
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── release.yml
│       ├── security.yml
│       └── coverage.yml
├── pyproject.toml
├── README.md
├── AGENTS.md                      # This file
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md
├── LICENSE
└── .gitignore
```

---

## Technical Stack

### Core Dependencies (MUST USE)
```toml
[project.dependencies]
httpx = ">=0.26.0"                 # Async HTTP client
pydantic = ">=2.0.0"               # Data validation
typing-extensions = ">=4.9.0"      # Type hints
python-dateutil = ">=2.8.0"        # Date parsing
```

### Dev Dependencies
```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "pytest-asyncio>=0.23.0",
    "pytest-mock>=3.12.0",
    "respx>=0.20.0",               # HTTP mocking for httpx
    "ruff>=0.1.0",
    "mypy>=1.8.0",
    "faker>=22.0.0",               # Mock data generation
]
```

### DO NOT ADD
- ❌ No requests (use httpx for async support)
- ❌ No aiohttp (httpx is simpler and more modern)
- ❌ No click (no CLI, that's agent-marketplace-cli)
- ❌ No Flask/FastAPI (not building a server)

---

## Architecture Constraints

### DO: Resource-Based API Design
```python
# GOOD: Resource-based with clear responsibilities
class AgentMarketplaceClient:
    def __init__(self, api_key: str, base_url: str = DEFAULT_URL):
        self.agents = AgentsResource(self)
        self.users = UsersResource(self)
        self.reviews = ReviewsResource(self)
        self.categories = CategoriesResource(self)
        self.search = SearchResource(self)
        self.analytics = AnalyticsResource(self)

# Usage
client = AgentMarketplaceClient(api_key="...")
agents = client.agents.list()
agent = client.agents.get("advanced-pm")
client.agents.star("advanced-pm")

# BAD: Flat namespace
class AgentMarketplaceClient:
    def list_agents(self): ...
    def get_agent(self, slug): ...
    def star_agent(self, slug): ...
    def list_users(self): ...
    def get_user(self, username): ...
    # ... 50 more methods
```

### DO: Both Sync and Async Clients
```python
# Sync client
from agent_marketplace_sdk import MarketplaceClient

client = MarketplaceClient(api_key="...")
agents = client.agents.list()

# Async client
from agent_marketplace_sdk import AsyncMarketplaceClient

async with AsyncMarketplaceClient(api_key="...") as client:
    agents = await client.agents.list()
```

### DO: Pydantic Models for Everything
```python
# All API responses as typed models
class Agent(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    author: User
    version: str
    downloads: int
    stars: int
    rating: float
    created_at: datetime
    updated_at: datetime

# Type-safe access
agent = client.agents.get("advanced-pm")
print(agent.name)  # IDE autocomplete works
print(agent.stars)  # Type checking works
```

### DO: Dependency Injection for Testing
```python
# All HTTP calls go through injected client
class AgentsResource:
    def __init__(
        self,
        http_client: httpx.Client | httpx.AsyncClient,
        base_url: str,
    ):
        self.http = http_client
        self.base_url = base_url
    
    def list(self) -> list[Agent]:
        response = self.http.get(f"{self.base_url}/agents")
        return [Agent(**item) for item in response.json()["items"]]

# Easy to mock in tests
mock_http = Mock(spec=httpx.Client)
mock_http.get.return_value.json.return_value = {"items": [...]}
resource = AgentsResource(mock_http, "http://test")
```

---

## Client API Design

### Main Client
```python
class MarketplaceClient:
    """Synchronous Agent Marketplace client.
    
    Example:
        >>> client = MarketplaceClient(api_key="your-api-key")
        >>> agents = client.agents.search("code review")
        >>> client.agents.install("advanced-pm", version="1.2.0")
    """
    
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://api.agent-marketplace.com",
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        """Initialize marketplace client.
        
        Args:
            api_key: API key (or set MARKETPLACE_API_KEY env var)
            base_url: API base URL
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
        """
        self.api_key = api_key or os.getenv("MARKETPLACE_API_KEY")
        self.base_url = base_url
        
        # HTTP client with retries
        self.http = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        
        # Resources
        self.agents = AgentsResource(self.http, base_url)
        self.users = UsersResource(self.http, base_url)
        self.reviews = ReviewsResource(self.http, base_url)
        self.categories = CategoriesResource(self.http, base_url)
        self.search = SearchResource(self.http, base_url)
        self.analytics = AnalyticsResource(self.http, base_url)
    
    def close(self) -> None:
        """Close HTTP client."""
        self.http.close()
    
    def __enter__(self) -> "MarketplaceClient":
        return self
    
    def __exit__(self, *args: Any) -> None:
        self.close()
```

### Agents Resource
```python
class AgentsResource:
    """Agent operations."""
    
    def list(
        self,
        category: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Agent]:
        """List agents.
        
        Args:
            category: Filter by category
            limit: Maximum results
            offset: Pagination offset
            
        Returns:
            List of agents
        """
        params = {"limit": limit, "offset": offset}
        if category:
            params["category"] = category
        
        response = self.http.get("/api/v1/agents", params=params)
        response.raise_for_status()
        return [Agent(**item) for item in response.json()["items"]]
    
    def get(self, slug: str) -> Agent:
        """Get agent by slug.
        
        Args:
            slug: Agent slug
            
        Returns:
            Agent details
            
        Raises:
            AgentNotFoundError: If agent doesn't exist
        """
        response = self.http.get(f"/api/v1/agents/{slug}")
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{slug}' not found")
        response.raise_for_status()
        return Agent(**response.json())
    
    def install(
        self,
        slug: str,
        version: str | None = None,
        path: Path | str = ".",
    ) -> Path:
        """Install agent locally.
        
        Args:
            slug: Agent slug
            version: Specific version (default: latest)
            path: Installation directory
            
        Returns:
            Path to installed agent
        """
        # Download agent
        download_url = f"/api/v1/agents/{slug}/download"
        if version:
            download_url += f"/{version}"
        
        response = self.http.get(download_url)
        response.raise_for_status()
        
        # Extract to path
        agent_path = Path(path) / slug
        agent_path.mkdir(parents=True, exist_ok=True)
        
        # Unzip
        with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
            zf.extractall(agent_path)
        
        return agent_path
    
    def publish(
        self,
        name: str,
        description: str,
        category: str,
        code_path: Path | str,
        version: str = "1.0.0",
    ) -> Agent:
        """Publish new agent.
        
        Args:
            name: Agent name
            description: Agent description
            category: Agent category
            code_path: Path to agent code
            version: Version number
            
        Returns:
            Created agent
        """
        # Zip agent code
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zf:
            for file in Path(code_path).rglob('*'):
                if file.is_file():
                    zf.write(file, file.relative_to(code_path))
        
        # Upload
        files = {"code": ("agent.zip", zip_buffer.getvalue())}
        data = {
            "name": name,
            "description": description,
            "category": category,
            "version": version,
        }
        
        response = self.http.post(
            "/api/v1/agents",
            files=files,
            data=data,
        )
        response.raise_for_status()
        return Agent(**response.json())
    
    def star(self, slug: str) -> None:
        """Star an agent."""
        response = self.http.post(f"/api/v1/agents/{slug}/star")
        response.raise_for_status()
    
    def unstar(self, slug: str) -> None:
        """Unstar an agent."""
        response = self.http.delete(f"/api/v1/agents/{slug}/star")
        response.raise_for_status()
```

### Search Resource
```python
class SearchResource:
    """Search operations."""
    
    def search(
        self,
        query: str,
        category: str | None = None,
        min_rating: float | None = None,
        sort: str = "relevance",
        limit: int = 20,
    ) -> list[Agent]:
        """Search agents.
        
        Args:
            query: Search query
            category: Filter by category
            min_rating: Minimum rating filter
            sort: Sort by (relevance, downloads, stars, rating)
            limit: Maximum results
            
        Returns:
            List of matching agents
        """
        params = {
            "q": query,
            "sort": sort,
            "limit": limit,
        }
        if category:
            params["category"] = category
        if min_rating:
            params["min_rating"] = min_rating
        
        response = self.http.get("/api/v1/search/agents", params=params)
        response.raise_for_status()
        return [Agent(**item) for item in response.json()["items"]]
```

---

## Data Models

### Agent Model
```python
class Agent(BaseModel):
    """Agent model."""
    
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
    
    model_config = ConfigDict(from_attributes=True)

class AgentVersion(BaseModel):
    """Agent version model."""
    
    id: int
    agent_id: int
    version: str
    changelog: str | None = None
    size_bytes: int
    tested: bool
    security_scan_passed: bool
    quality_score: float | None = None
    published_at: datetime

class AgentCreate(BaseModel):
    """Agent creation schema."""
    
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10, max_length=1000)
    category: str
    version: str = "1.0.0"
    
    @field_validator('version')
    @classmethod
    def validate_version(cls, v: str) -> str:
        """Validate semantic version."""
        if not re.match(r'^\d+\.\d+\.\d+$', v):
            raise ValueError("Version must be semantic (e.g., 1.0.0)")
        return v
```

### User Model
```python
class User(BaseModel):
    """User model."""
    
    id: int
    username: str
    email: str
    avatar_url: str | None = None
    bio: str | None = None
    reputation: int
    created_at: datetime
```

### Review Model
```python
class Review(BaseModel):
    """Review model."""
    
    id: int
    agent: Agent
    user: User
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = None
    helpful_count: int
    created_at: datetime
    updated_at: datetime

class ReviewCreate(BaseModel):
    """Review creation schema."""
    
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = Field(None, max_length=1000)
```

---

## Error Handling

### Custom Exceptions
```python
class MarketplaceError(Exception):
    """Base exception."""
    pass

class AgentNotFoundError(MarketplaceError):
    """Agent not found."""
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

# Exception mapping from HTTP status codes
def handle_response_error(response: httpx.Response) -> None:
    """Handle HTTP errors."""
    if response.status_code == 401:
        raise AuthenticationError("Invalid API key")
    elif response.status_code == 404:
        raise AgentNotFoundError("Resource not found")
    elif response.status_code == 422:
        raise ValidationError(response.json().get("detail", "Validation failed"))
    elif response.status_code == 429:
        raise RateLimitError("Rate limit exceeded")
    else:
        response.raise_for_status()
```

---

## Configuration Management

### Config Class
```python
class MarketplaceConfig:
    """SDK configuration."""
    
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
    ):
        """Initialize configuration.
        
        Args:
            api_key: API key (or MARKETPLACE_API_KEY env var)
            base_url: API base URL (or MARKETPLACE_BASE_URL env var)
            timeout: Request timeout
        """
        self.api_key = api_key or os.getenv("MARKETPLACE_API_KEY")
        self.base_url = base_url or os.getenv(
            "MARKETPLACE_BASE_URL",
            "https://api.agent-marketplace.com"
        )
        self.timeout = timeout
        
        if not self.api_key:
            raise ValueError(
                "API key required. Set MARKETPLACE_API_KEY env var or pass api_key parameter."
            )
    
    @classmethod
    def from_file(cls, path: Path | str = "~/.marketplace/config.toml") -> "MarketplaceConfig":
        """Load configuration from file.
        
        Args:
            path: Config file path
            
        Returns:
            Configuration instance
        """
        path = Path(path).expanduser()
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        
        with path.open() as f:
            config = toml.load(f)
        
        return cls(
            api_key=config.get("api_key"),
            base_url=config.get("base_url"),
            timeout=config.get("timeout", 30.0),
        )
    
    def save(self, path: Path | str = "~/.marketplace/config.toml") -> None:
        """Save configuration to file.
        
        Args:
            path: Config file path
        """
        path = Path(path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        
        config = {
            "api_key": self.api_key,
            "base_url": self.base_url,
            "timeout": self.timeout,
        }
        
        with path.open('w') as f:
            toml.dump(config, f)
```

---

## Testing Strategy

### Mock HTTP Responses
```python
# conftest.py
import pytest
import respx
from httpx import Response

@pytest.fixture
def mock_api():
    """Mock API responses."""
    with respx.mock(base_url="https://api.agent-marketplace.com") as respx_mock:
        # Mock agent list
        respx_mock.get("/api/v1/agents").mock(
            return_value=Response(
                200,
                json={
                    "items": [
                        {
                            "id": 1,
                            "name": "Advanced PM",
                            "slug": "advanced-pm",
                            "description": "Enhanced PM agent",
                            "author": {"id": 1, "username": "testuser"},
                            "current_version": "1.2.0",
                            "downloads": 100,
                            "stars": 50,
                            "rating": 4.5,
                            "category": "pm",
                            "is_public": True,
                            "is_validated": True,
                            "created_at": "2025-01-01T00:00:00Z",
                            "updated_at": "2025-01-01T00:00:00Z",
                        }
                    ],
                    "total": 1,
                }
            )
        )
        
        # Mock agent get
        respx_mock.get("/api/v1/agents/advanced-pm").mock(
            return_value=Response(200, json={...})
        )
        
        yield respx_mock
```

### Unit Tests
```python
# tests/unit/test_agents.py
import pytest
from agent_marketplace_sdk import MarketplaceClient

class TestAgentsResource:
    """Tests for AgentsResource."""
    
    def test_list_agents(self, mock_api):
        """Test listing agents."""
        client = MarketplaceClient(api_key="test-key")
        agents = client.agents.list()
        
        assert len(agents) == 1
        assert agents[0].name == "Advanced PM"
        assert agents[0].slug == "advanced-pm"
    
    def test_get_agent(self, mock_api):
        """Test getting agent by slug."""
        client = MarketplaceClient(api_key="test-key")
        agent = client.agents.get("advanced-pm")
        
        assert agent.name == "Advanced PM"
        assert agent.stars == 50
    
    def test_get_agent_not_found(self, mock_api):
        """Test agent not found error."""
        mock_api.get("/api/v1/agents/nonexistent").mock(
            return_value=Response(404)
        )
        
        client = MarketplaceClient(api_key="test-key")
        
        with pytest.raises(AgentNotFoundError):
            client.agents.get("nonexistent")
```

### Integration Tests
```python
# tests/integration/test_agent_flow.py
import pytest
from agent_marketplace_sdk import MarketplaceClient

@pytest.mark.integration
class TestAgentFlow:
    """Integration tests for agent operations."""
    
    def test_complete_agent_flow(self, temp_dir):
        """Test complete agent workflow."""
        client = MarketplaceClient(api_key=TEST_API_KEY)
        
        # Search agents
        agents = client.search.search("code review")
        assert len(agents) > 0
        
        # Get agent details
        agent = client.agents.get(agents[0].slug)
        assert agent.name is not None
        
        # Install agent
        install_path = client.agents.install(
            agent.slug,
            path=temp_dir,
        )
        assert install_path.exists()
        
        # Star agent
        client.agents.star(agent.slug)
        
        # Leave review
        client.reviews.create(
            agent.slug,
            rating=5,
            comment="Great agent!",
        )
```

---

## Example Usage

### Basic Usage
```python
from agent_marketplace_sdk import MarketplaceClient

# Initialize client
client = MarketplaceClient(api_key="your-api-key")

# Search agents
agents = client.search.search("code review")
for agent in agents:
    print(f"{agent.name} - {agent.description}")

# Get agent details
agent = client.agents.get("advanced-pm")
print(f"Stars: {agent.stars}, Rating: {agent.rating}")

# Install agent
client.agents.install("advanced-pm", version="1.2.0")

# Star agent
client.agents.star("advanced-pm")

# Leave review
client.reviews.create(
    "advanced-pm",
    rating=5,
    comment="Excellent agent!"
)
```

### Async Usage
```python
from agent_marketplace_sdk import AsyncMarketplaceClient

async def main():
    async with AsyncMarketplaceClient(api_key="your-api-key") as client:
        # Search agents
        agents = await client.search.search("testing")
        
        # Get multiple agents in parallel
        import asyncio
        agent_details = await asyncio.gather(*[
            client.agents.get(agent.slug)
            for agent in agents[:5]
        ])
        
        # Install agents
        for agent in agent_details:
            await client.agents.install(agent.slug)

asyncio.run(main())
```

### Publishing Agent
```python
from agent_marketplace_sdk import MarketplaceClient
from pathlib import Path

client = MarketplaceClient(api_key="your-api-key")

# Publish new agent
agent = client.agents.publish(
    name="My Custom Agent",
    description="Does amazing things",
    category="testing",
    code_path=Path("./my-agent"),
    version="1.0.0",
)

print(f"Published: {agent.slug}")
print(f"Status: {'Validated' if agent.is_validated else 'Pending validation'}")
```

---

## CI/CD Configuration

### GitHub Actions - ci.yml
```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: pip install -e ".[dev]"
      
      - name: Run ruff
        run: ruff check src tests
      
      - name: Run mypy
        run: mypy src
      
      - name: Run tests with coverage
        run: pytest --cov=src/agent_marketplace_sdk --cov-report=xml --cov-report=term
      
      - name: Check 100% coverage
        run: coverage report --fail-under=100
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage.xml
```

---

## PyPI Publication

**Package name:** `agent-marketplace-ld-sdk`

**Installation:**
```bash
pip install agent-marketplace-ld-sdk
```

**Entry point:**
```python
from agent_marketplace_sdk import MarketplaceClient, AsyncMarketplaceClient
```

---

## Repository Configuration

**Repository:** `github.com/kmcallorum/agent-marketplace-ld-sdk`

**Description:**
> "Official Python SDK for Agent Marketplace. Discover, install, and publish AI agents programmatically with a clean, type-safe API."

**Topics:**
```
python, sdk, client, api-client, agent-marketplace, pytest-agents,
async, httpx, pydantic, type-safe, agent-discovery, agent-installation
```

---

## README.md Structure

```markdown
# agent-marketplace-ld-sdk

[![PyPI](https://img.shields.io/pypi/v/agent-marketplace-ld-sdk.svg)](https://pypi.org/project/agent-marketplace-ld-sdk/)
[![CI](https://github.com/kmcallorum/agent-marketplace-ld-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/kmcallorum/agent-marketplace-ld-sdk/actions)
[![codecov](https://codecov.io/gh/kmcallorum/agent-marketplace-ld-sdk/graph/badge.svg)](https://codecov.io/gh/kmcallorum/agent-marketplace-ld-sdk)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Python SDK for Agent Marketplace.

## Features

- 🔍 **Search & Discovery**: Find agents by capability
- 📦 **Install Agents**: One-line agent installation
- 📤 **Publish Agents**: Programmatic agent publishing
- ⭐ **Social Features**: Stars, reviews, ratings
- 🔄 **Async Support**: Full async/await support
- 🎯 **Type Safe**: Complete type hints and Pydantic models
- ✅ **100% Tested**: Comprehensive test coverage

## Quick Start

```python
from agent_marketplace_sdk import MarketplaceClient

# Initialize client
client = MarketplaceClient(api_key="your-api-key")

# Search agents
agents = client.search.search("code review")

# Install agent
client.agents.install("advanced-pm")
```

## Installation

```bash
pip install agent-marketplace-ld-sdk
```

## Documentation

See [docs/](docs/) for detailed documentation.

## License

MIT License - see [LICENSE](LICENSE) for details.
```

---

## Success Criteria

1. ✅ Client can authenticate with API
2. ✅ Can search and list agents
3. ✅ Can get agent details
4. ✅ Can install agents locally
5. ✅ Can publish new agents
6. ✅ Can star/unstar agents
7. ✅ Can create/read reviews
8. ✅ All tests pass with 100% coverage
9. ✅ Type checking passes (mypy strict)
10. ✅ Async client works identically to sync

---

**This AGENTS.md is complete and ready for Claude Code.** 🚀
