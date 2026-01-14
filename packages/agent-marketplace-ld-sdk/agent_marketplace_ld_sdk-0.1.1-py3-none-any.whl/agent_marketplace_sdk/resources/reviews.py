"""Review resource operations."""

from __future__ import annotations

import httpx

from agent_marketplace_sdk.exceptions import AgentNotFoundError, handle_response_error
from agent_marketplace_sdk.models.review import Review, ReviewCreate


class ReviewsResource:
    """Synchronous review operations."""

    def __init__(self, http: httpx.Client) -> None:
        """Initialize reviews resource.

        Args:
            http: HTTP client instance.
        """
        self._http = http

    def list(
        self,
        agent_slug: str,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Review]:
        """List reviews for an agent.

        Args:
            agent_slug: Agent slug.
            limit: Maximum results.
            offset: Pagination offset.

        Returns:
            List of reviews.

        Raises:
            AgentNotFoundError: If agent doesn't exist.
        """
        response = self._http.get(
            f"/api/v1/agents/{agent_slug}/reviews",
            params={"limit": limit, "offset": offset},
        )
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{agent_slug}' not found")
        handle_response_error(response)
        return [Review(**item) for item in response.json()["items"]]

    def create(
        self,
        agent_slug: str,
        review: ReviewCreate,
    ) -> Review:
        """Create a review for an agent.

        Args:
            agent_slug: Agent slug.
            review: Review data.

        Returns:
            Created review.

        Raises:
            AgentNotFoundError: If agent doesn't exist.
        """
        response = self._http.post(
            f"/api/v1/agents/{agent_slug}/reviews",
            json=review.model_dump(),
        )
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{agent_slug}' not found")
        handle_response_error(response)
        return Review(**response.json())

    def update(
        self,
        agent_slug: str,
        review_id: int,
        review: ReviewCreate,
    ) -> Review:
        """Update a review.

        Args:
            agent_slug: Agent slug.
            review_id: Review ID.
            review: Updated review data.

        Returns:
            Updated review.

        Raises:
            AgentNotFoundError: If agent or review doesn't exist.
        """
        response = self._http.put(
            f"/api/v1/agents/{agent_slug}/reviews/{review_id}",
            json=review.model_dump(),
        )
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{agent_slug}' or review not found")
        handle_response_error(response)
        return Review(**response.json())

    def delete(
        self,
        agent_slug: str,
        review_id: int,
    ) -> None:
        """Delete a review.

        Args:
            agent_slug: Agent slug.
            review_id: Review ID.

        Raises:
            AgentNotFoundError: If agent or review doesn't exist.
        """
        response = self._http.delete(f"/api/v1/agents/{agent_slug}/reviews/{review_id}")
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{agent_slug}' or review not found")
        handle_response_error(response)

    def mark_helpful(
        self,
        agent_slug: str,
        review_id: int,
    ) -> None:
        """Mark a review as helpful.

        Args:
            agent_slug: Agent slug.
            review_id: Review ID.

        Raises:
            AgentNotFoundError: If agent or review doesn't exist.
        """
        response = self._http.post(f"/api/v1/agents/{agent_slug}/reviews/{review_id}/helpful")
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{agent_slug}' or review not found")
        handle_response_error(response)


class AsyncReviewsResource:
    """Asynchronous review operations."""

    def __init__(self, http: httpx.AsyncClient) -> None:
        """Initialize async reviews resource.

        Args:
            http: Async HTTP client instance.
        """
        self._http = http

    async def list(
        self,
        agent_slug: str,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Review]:
        """List reviews for an agent.

        Args:
            agent_slug: Agent slug.
            limit: Maximum results.
            offset: Pagination offset.

        Returns:
            List of reviews.

        Raises:
            AgentNotFoundError: If agent doesn't exist.
        """
        response = await self._http.get(
            f"/api/v1/agents/{agent_slug}/reviews",
            params={"limit": limit, "offset": offset},
        )
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{agent_slug}' not found")
        handle_response_error(response)
        return [Review(**item) for item in response.json()["items"]]

    async def create(
        self,
        agent_slug: str,
        review: ReviewCreate,
    ) -> Review:
        """Create a review for an agent.

        Args:
            agent_slug: Agent slug.
            review: Review data.

        Returns:
            Created review.

        Raises:
            AgentNotFoundError: If agent doesn't exist.
        """
        response = await self._http.post(
            f"/api/v1/agents/{agent_slug}/reviews",
            json=review.model_dump(),
        )
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{agent_slug}' not found")
        handle_response_error(response)
        return Review(**response.json())

    async def update(
        self,
        agent_slug: str,
        review_id: int,
        review: ReviewCreate,
    ) -> Review:
        """Update a review.

        Args:
            agent_slug: Agent slug.
            review_id: Review ID.
            review: Updated review data.

        Returns:
            Updated review.

        Raises:
            AgentNotFoundError: If agent or review doesn't exist.
        """
        response = await self._http.put(
            f"/api/v1/agents/{agent_slug}/reviews/{review_id}",
            json=review.model_dump(),
        )
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{agent_slug}' or review not found")
        handle_response_error(response)
        return Review(**response.json())

    async def delete(
        self,
        agent_slug: str,
        review_id: int,
    ) -> None:
        """Delete a review.

        Args:
            agent_slug: Agent slug.
            review_id: Review ID.

        Raises:
            AgentNotFoundError: If agent or review doesn't exist.
        """
        response = await self._http.delete(f"/api/v1/agents/{agent_slug}/reviews/{review_id}")
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{agent_slug}' or review not found")
        handle_response_error(response)

    async def mark_helpful(
        self,
        agent_slug: str,
        review_id: int,
    ) -> None:
        """Mark a review as helpful.

        Args:
            agent_slug: Agent slug.
            review_id: Review ID.

        Raises:
            AgentNotFoundError: If agent or review doesn't exist.
        """
        response = await self._http.post(f"/api/v1/agents/{agent_slug}/reviews/{review_id}/helpful")
        if response.status_code == 404:
            raise AgentNotFoundError(f"Agent '{agent_slug}' or review not found")
        handle_response_error(response)
