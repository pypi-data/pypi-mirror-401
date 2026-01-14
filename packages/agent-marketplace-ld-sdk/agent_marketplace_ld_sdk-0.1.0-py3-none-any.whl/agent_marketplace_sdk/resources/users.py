"""User resource operations."""

from __future__ import annotations

import httpx

from agent_marketplace_sdk.exceptions import UserNotFoundError, handle_response_error
from agent_marketplace_sdk.models.agent import Agent
from agent_marketplace_sdk.models.user import UserProfile


class UsersResource:
    """Synchronous user operations."""

    def __init__(self, http: httpx.Client) -> None:
        """Initialize users resource.

        Args:
            http: HTTP client instance.
        """
        self._http = http

    def get(self, username: str) -> UserProfile:
        """Get user by username.

        Args:
            username: Username.

        Returns:
            User profile.

        Raises:
            UserNotFoundError: If user doesn't exist.
        """
        response = self._http.get(f"/api/v1/users/{username}")
        if response.status_code == 404:
            raise UserNotFoundError(f"User '{username}' not found")
        handle_response_error(response)
        return UserProfile(**response.json())

    def me(self) -> UserProfile:
        """Get current authenticated user profile.

        Returns:
            Current user profile.
        """
        response = self._http.get("/api/v1/users/me")
        handle_response_error(response)
        return UserProfile(**response.json())

    def get_agents(self, username: str) -> list[Agent]:
        """Get agents published by a user.

        Args:
            username: Username.

        Returns:
            List of agents.

        Raises:
            UserNotFoundError: If user doesn't exist.
        """
        response = self._http.get(f"/api/v1/users/{username}/agents")
        if response.status_code == 404:
            raise UserNotFoundError(f"User '{username}' not found")
        handle_response_error(response)
        return [Agent(**item) for item in response.json()["items"]]

    def get_starred(self, username: str) -> list[Agent]:
        """Get agents starred by a user.

        Args:
            username: Username.

        Returns:
            List of starred agents.

        Raises:
            UserNotFoundError: If user doesn't exist.
        """
        response = self._http.get(f"/api/v1/users/{username}/starred")
        if response.status_code == 404:
            raise UserNotFoundError(f"User '{username}' not found")
        handle_response_error(response)
        return [Agent(**item) for item in response.json()["items"]]


class AsyncUsersResource:
    """Asynchronous user operations."""

    def __init__(self, http: httpx.AsyncClient) -> None:
        """Initialize async users resource.

        Args:
            http: Async HTTP client instance.
        """
        self._http = http

    async def get(self, username: str) -> UserProfile:
        """Get user by username.

        Args:
            username: Username.

        Returns:
            User profile.

        Raises:
            UserNotFoundError: If user doesn't exist.
        """
        response = await self._http.get(f"/api/v1/users/{username}")
        if response.status_code == 404:
            raise UserNotFoundError(f"User '{username}' not found")
        handle_response_error(response)
        return UserProfile(**response.json())

    async def me(self) -> UserProfile:
        """Get current authenticated user profile.

        Returns:
            Current user profile.
        """
        response = await self._http.get("/api/v1/users/me")
        handle_response_error(response)
        return UserProfile(**response.json())

    async def get_agents(self, username: str) -> list[Agent]:
        """Get agents published by a user.

        Args:
            username: Username.

        Returns:
            List of agents.

        Raises:
            UserNotFoundError: If user doesn't exist.
        """
        response = await self._http.get(f"/api/v1/users/{username}/agents")
        if response.status_code == 404:
            raise UserNotFoundError(f"User '{username}' not found")
        handle_response_error(response)
        return [Agent(**item) for item in response.json()["items"]]

    async def get_starred(self, username: str) -> list[Agent]:
        """Get agents starred by a user.

        Args:
            username: Username.

        Returns:
            List of starred agents.

        Raises:
            UserNotFoundError: If user doesn't exist.
        """
        response = await self._http.get(f"/api/v1/users/{username}/starred")
        if response.status_code == 404:
            raise UserNotFoundError(f"User '{username}' not found")
        handle_response_error(response)
        return [Agent(**item) for item in response.json()["items"]]
