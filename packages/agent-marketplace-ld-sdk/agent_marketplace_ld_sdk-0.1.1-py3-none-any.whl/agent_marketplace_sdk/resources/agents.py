"""Agent resource operations."""

from __future__ import annotations

import builtins
import io
import zipfile
from pathlib import Path
from typing import TYPE_CHECKING, Any

import httpx

from agent_marketplace_sdk.exceptions import AgentNotFoundError, handle_response_error
from agent_marketplace_sdk.models.agent import Agent, AgentVersion

if TYPE_CHECKING:
    from agent_marketplace_sdk.models.agent import AgentCreate


class AgentsResource:
    """Synchronous agent operations."""

    def __init__(self, http: httpx.Client) -> None:
        """Initialize agents resource.

        Args:
            http: HTTP client instance.
        """
        self._http = http

    def list(
        self,
        category: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> builtins.list[Agent]:
        """List agents.

        Args:
            category: Filter by category.
            limit: Maximum results.
            offset: Pagination offset.

        Returns:
            List of agents.
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if category:
            params["category"] = category

        response = self._http.get("/api/v1/agents", params=params)
        handle_response_error(response)
        return [Agent(**item) for item in response.json()["items"]]

    def get(self, slug: str) -> Agent:
        """Get agent by slug.

        Args:
            slug: Agent slug.

        Returns:
            Agent details.

        Raises:
            AgentNotFoundError: If agent doesn't exist.
        """
        response = self._http.get(f"/api/v1/agents/{slug}")
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{slug}' not found")
        handle_response_error(response)
        return Agent(**response.json())

    def get_versions(self, slug: str) -> builtins.list[AgentVersion]:
        """Get agent versions.

        Args:
            slug: Agent slug.

        Returns:
            List of agent versions.

        Raises:
            AgentNotFoundError: If agent doesn't exist.
        """
        response = self._http.get(f"/api/v1/agents/{slug}/versions")
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{slug}' not found")
        handle_response_error(response)
        return [AgentVersion(**item) for item in response.json()["items"]]

    def install(
        self,
        slug: str,
        version: str | None = None,
        path: Path | str = ".",
    ) -> Path:
        """Install agent locally.

        Args:
            slug: Agent slug.
            version: Specific version (default: latest).
            path: Installation directory.

        Returns:
            Path to installed agent.

        Raises:
            AgentNotFoundError: If agent doesn't exist.
        """
        download_url = f"/api/v1/agents/{slug}/download"
        if version:
            download_url = f"/api/v1/agents/{slug}/download/{version}"

        response = self._http.get(download_url)
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{slug}' not found")
        handle_response_error(response)

        agent_path = Path(path) / slug
        agent_path.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
            zf.extractall(agent_path)

        return agent_path

    def publish(
        self,
        agent_data: AgentCreate,
        code_path: Path | str,
    ) -> Agent:
        """Publish new agent.

        Args:
            agent_data: Agent creation data.
            code_path: Path to agent code.

        Returns:
            Created agent.
        """
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            code_path_obj = Path(code_path)
            for file in code_path_obj.rglob("*"):
                if file.is_file():
                    zf.write(file, file.relative_to(code_path_obj))

        zip_buffer.seek(0)
        files = {"code": ("agent.zip", zip_buffer.getvalue(), "application/zip")}
        data = agent_data.model_dump()

        response = self._http.post("/api/v1/agents", files=files, data=data)
        handle_response_error(response)
        return Agent(**response.json())

    def update(
        self,
        slug: str,
        version: str,
        code_path: Path | str,
        changelog: str | None = None,
    ) -> Agent:
        """Update agent with new version.

        Args:
            slug: Agent slug.
            version: New version number.
            code_path: Path to agent code.
            changelog: Version changelog.

        Returns:
            Updated agent.

        Raises:
            AgentNotFoundError: If agent doesn't exist.
        """
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            code_path_obj = Path(code_path)
            for file in code_path_obj.rglob("*"):
                if file.is_file():
                    zf.write(file, file.relative_to(code_path_obj))

        zip_buffer.seek(0)
        files = {"code": ("agent.zip", zip_buffer.getvalue(), "application/zip")}
        data: dict[str, Any] = {"version": version}
        if changelog:
            data["changelog"] = changelog

        response = self._http.put(f"/api/v1/agents/{slug}", files=files, data=data)
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{slug}' not found")
        handle_response_error(response)
        return Agent(**response.json())

    def delete(self, slug: str) -> None:
        """Delete an agent.

        Args:
            slug: Agent slug.

        Raises:
            AgentNotFoundError: If agent doesn't exist.
        """
        response = self._http.delete(f"/api/v1/agents/{slug}")
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{slug}' not found")
        handle_response_error(response)

    def star(self, slug: str) -> None:
        """Star an agent.

        Args:
            slug: Agent slug.

        Raises:
            AgentNotFoundError: If agent doesn't exist.
        """
        response = self._http.post(f"/api/v1/agents/{slug}/star")
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{slug}' not found")
        handle_response_error(response)

    def unstar(self, slug: str) -> None:
        """Unstar an agent.

        Args:
            slug: Agent slug.

        Raises:
            AgentNotFoundError: If agent doesn't exist.
        """
        response = self._http.delete(f"/api/v1/agents/{slug}/star")
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{slug}' not found")
        handle_response_error(response)


class AsyncAgentsResource:
    """Asynchronous agent operations."""

    def __init__(self, http: httpx.AsyncClient) -> None:
        """Initialize async agents resource.

        Args:
            http: Async HTTP client instance.
        """
        self._http = http

    async def list(
        self,
        category: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> builtins.list[Agent]:
        """List agents.

        Args:
            category: Filter by category.
            limit: Maximum results.
            offset: Pagination offset.

        Returns:
            List of agents.
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if category:
            params["category"] = category

        response = await self._http.get("/api/v1/agents", params=params)
        handle_response_error(response)
        return [Agent(**item) for item in response.json()["items"]]

    async def get(self, slug: str) -> Agent:
        """Get agent by slug.

        Args:
            slug: Agent slug.

        Returns:
            Agent details.

        Raises:
            AgentNotFoundError: If agent doesn't exist.
        """
        response = await self._http.get(f"/api/v1/agents/{slug}")
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{slug}' not found")
        handle_response_error(response)
        return Agent(**response.json())

    async def get_versions(self, slug: str) -> builtins.list[AgentVersion]:
        """Get agent versions.

        Args:
            slug: Agent slug.

        Returns:
            List of agent versions.

        Raises:
            AgentNotFoundError: If agent doesn't exist.
        """
        response = await self._http.get(f"/api/v1/agents/{slug}/versions")
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{slug}' not found")
        handle_response_error(response)
        return [AgentVersion(**item) for item in response.json()["items"]]

    async def install(
        self,
        slug: str,
        version: str | None = None,
        path: Path | str = ".",
    ) -> Path:
        """Install agent locally.

        Args:
            slug: Agent slug.
            version: Specific version (default: latest).
            path: Installation directory.

        Returns:
            Path to installed agent.

        Raises:
            AgentNotFoundError: If agent doesn't exist.
        """
        download_url = f"/api/v1/agents/{slug}/download"
        if version:
            download_url = f"/api/v1/agents/{slug}/download/{version}"

        response = await self._http.get(download_url)
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{slug}' not found")
        handle_response_error(response)

        agent_path = Path(path) / slug
        agent_path.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
            zf.extractall(agent_path)

        return agent_path

    async def publish(
        self,
        agent_data: AgentCreate,
        code_path: Path | str,
    ) -> Agent:
        """Publish new agent.

        Args:
            agent_data: Agent creation data.
            code_path: Path to agent code.

        Returns:
            Created agent.
        """
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            code_path_obj = Path(code_path)
            for file in code_path_obj.rglob("*"):
                if file.is_file():
                    zf.write(file, file.relative_to(code_path_obj))

        zip_buffer.seek(0)
        files = {"code": ("agent.zip", zip_buffer.getvalue(), "application/zip")}
        data = agent_data.model_dump()

        response = await self._http.post("/api/v1/agents", files=files, data=data)
        handle_response_error(response)
        return Agent(**response.json())

    async def update(
        self,
        slug: str,
        version: str,
        code_path: Path | str,
        changelog: str | None = None,
    ) -> Agent:
        """Update agent with new version.

        Args:
            slug: Agent slug.
            version: New version number.
            code_path: Path to agent code.
            changelog: Version changelog.

        Returns:
            Updated agent.

        Raises:
            AgentNotFoundError: If agent doesn't exist.
        """
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            code_path_obj = Path(code_path)
            for file in code_path_obj.rglob("*"):
                if file.is_file():
                    zf.write(file, file.relative_to(code_path_obj))

        zip_buffer.seek(0)
        files = {"code": ("agent.zip", zip_buffer.getvalue(), "application/zip")}
        data: dict[str, Any] = {"version": version}
        if changelog:
            data["changelog"] = changelog

        response = await self._http.put(f"/api/v1/agents/{slug}", files=files, data=data)
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{slug}' not found")
        handle_response_error(response)
        return Agent(**response.json())

    async def delete(self, slug: str) -> None:
        """Delete an agent.

        Args:
            slug: Agent slug.

        Raises:
            AgentNotFoundError: If agent doesn't exist.
        """
        response = await self._http.delete(f"/api/v1/agents/{slug}")
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{slug}' not found")
        handle_response_error(response)

    async def star(self, slug: str) -> None:
        """Star an agent.

        Args:
            slug: Agent slug.

        Raises:
            AgentNotFoundError: If agent doesn't exist.
        """
        response = await self._http.post(f"/api/v1/agents/{slug}/star")
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{slug}' not found")
        handle_response_error(response)

    async def unstar(self, slug: str) -> None:
        """Unstar an agent.

        Args:
            slug: Agent slug.

        Raises:
            AgentNotFoundError: If agent doesn't exist.
        """
        response = await self._http.delete(f"/api/v1/agents/{slug}/star")
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{slug}' not found")
        handle_response_error(response)
