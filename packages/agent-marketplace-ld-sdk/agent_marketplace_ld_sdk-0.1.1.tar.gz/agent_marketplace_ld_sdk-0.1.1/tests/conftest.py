"""Pytest configuration and fixtures."""

import io
import zipfile
from collections.abc import Generator
from pathlib import Path

import pytest
import respx
from httpx import Response

from tests.fixtures.mock_api_responses import (
    AGENTS_LIST_RESPONSE,
    CATEGORIES_LIST_RESPONSE,
    REVIEWS_LIST_RESPONSE,
    SAMPLE_AGENT,
    SAMPLE_AGENT_ANALYTICS,
    SAMPLE_CATEGORY,
    SAMPLE_REVIEW,
    SAMPLE_USER_PROFILE,
    SEARCH_RESPONSE,
    TRENDING_LIST_RESPONSE,
    VERSIONS_LIST_RESPONSE,
)

BASE_URL = "https://api.agent-marketplace.com"


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """Create a temporary directory for tests."""
    return tmp_path


@pytest.fixture
def sample_agent_dir(tmp_path: Path) -> Path:
    """Create a sample agent directory structure."""
    agent_dir = tmp_path / "sample-agent"
    agent_dir.mkdir()

    # Create required files
    (agent_dir / "agent.py").write_text('"""Sample agent."""\n\ndef run():\n    pass\n')
    (agent_dir / "agent.yaml").write_text("name: sample-agent\nversion: 1.0.0\n")
    (agent_dir / "README.md").write_text("# Sample Agent\n")

    # Create a subdirectory to cover the file.is_file() branch
    (agent_dir / "utils").mkdir()
    (agent_dir / "utils" / "helpers.py").write_text('"""Helpers."""\n')

    return agent_dir


@pytest.fixture
def sample_zip_content() -> bytes:
    """Create sample zip content."""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        zf.writestr("agent.py", '"""Agent code."""\n')
        zf.writestr("agent.yaml", "name: test\n")
    return zip_buffer.getvalue()


@pytest.fixture
def mock_api() -> Generator[respx.MockRouter, None, None]:
    """Mock API responses using respx."""
    with respx.mock(base_url=BASE_URL, assert_all_called=False) as respx_mock:
        # Agents endpoints
        respx_mock.get("/api/v1/agents").mock(return_value=Response(200, json=AGENTS_LIST_RESPONSE))
        respx_mock.get("/api/v1/agents/advanced-pm").mock(
            return_value=Response(200, json=SAMPLE_AGENT)
        )
        respx_mock.get("/api/v1/agents/nonexistent").mock(return_value=Response(404))
        respx_mock.get("/api/v1/agents/advanced-pm/versions").mock(
            return_value=Response(200, json=VERSIONS_LIST_RESPONSE)
        )
        respx_mock.post("/api/v1/agents").mock(return_value=Response(201, json=SAMPLE_AGENT))
        respx_mock.put("/api/v1/agents/advanced-pm").mock(
            return_value=Response(200, json=SAMPLE_AGENT)
        )
        respx_mock.delete("/api/v1/agents/advanced-pm").mock(return_value=Response(204))
        respx_mock.post("/api/v1/agents/advanced-pm/star").mock(return_value=Response(204))
        respx_mock.delete("/api/v1/agents/advanced-pm/star").mock(return_value=Response(204))

        # Users endpoints
        respx_mock.get("/api/v1/users/me").mock(
            return_value=Response(200, json=SAMPLE_USER_PROFILE)
        )
        respx_mock.get("/api/v1/users/testuser").mock(
            return_value=Response(200, json=SAMPLE_USER_PROFILE)
        )
        respx_mock.get("/api/v1/users/nonexistent").mock(return_value=Response(404))
        respx_mock.get("/api/v1/users/testuser/agents").mock(
            return_value=Response(200, json=AGENTS_LIST_RESPONSE)
        )
        respx_mock.get("/api/v1/users/testuser/starred").mock(
            return_value=Response(200, json=AGENTS_LIST_RESPONSE)
        )

        # Reviews endpoints
        respx_mock.get("/api/v1/agents/advanced-pm/reviews").mock(
            return_value=Response(200, json=REVIEWS_LIST_RESPONSE)
        )
        respx_mock.post("/api/v1/agents/advanced-pm/reviews").mock(
            return_value=Response(201, json=SAMPLE_REVIEW)
        )
        respx_mock.put("/api/v1/agents/advanced-pm/reviews/1").mock(
            return_value=Response(200, json=SAMPLE_REVIEW)
        )
        respx_mock.delete("/api/v1/agents/advanced-pm/reviews/1").mock(return_value=Response(204))
        respx_mock.post("/api/v1/agents/advanced-pm/reviews/1/helpful").mock(
            return_value=Response(204)
        )

        # Categories endpoints
        respx_mock.get("/api/v1/categories").mock(
            return_value=Response(200, json=CATEGORIES_LIST_RESPONSE)
        )
        respx_mock.get("/api/v1/categories/pm").mock(
            return_value=Response(200, json=SAMPLE_CATEGORY)
        )

        # Search endpoints
        respx_mock.get("/api/v1/search/agents").mock(
            return_value=Response(200, json=SEARCH_RESPONSE)
        )

        # Analytics endpoints
        respx_mock.get("/api/v1/agents/advanced-pm/analytics").mock(
            return_value=Response(200, json=SAMPLE_AGENT_ANALYTICS)
        )
        respx_mock.get("/api/v1/analytics/trending").mock(
            return_value=Response(200, json=TRENDING_LIST_RESPONSE)
        )

        yield respx_mock


@pytest.fixture
def mock_api_with_download(
    mock_api: respx.MockRouter, sample_zip_content: bytes
) -> respx.MockRouter:
    """Mock API with download endpoints."""
    mock_api.get("/api/v1/agents/advanced-pm/download").mock(
        return_value=Response(200, content=sample_zip_content)
    )
    mock_api.get("/api/v1/agents/advanced-pm/download/1.2.0").mock(
        return_value=Response(200, content=sample_zip_content)
    )
    mock_api.get("/api/v1/agents/nonexistent/download").mock(return_value=Response(404))
    return mock_api


@pytest.fixture
def mock_api_errors() -> Generator[respx.MockRouter, None, None]:
    """Mock API error responses."""
    with respx.mock(base_url=BASE_URL, assert_all_called=False) as respx_mock:
        respx_mock.get("/api/v1/agents/unauthorized").mock(return_value=Response(401))
        respx_mock.get("/api/v1/agents/validation-error").mock(
            return_value=Response(422, json={"detail": "Invalid input"})
        )
        respx_mock.get("/api/v1/agents/rate-limited").mock(return_value=Response(429))
        respx_mock.get("/api/v1/agents/server-error").mock(return_value=Response(500))
        yield respx_mock
