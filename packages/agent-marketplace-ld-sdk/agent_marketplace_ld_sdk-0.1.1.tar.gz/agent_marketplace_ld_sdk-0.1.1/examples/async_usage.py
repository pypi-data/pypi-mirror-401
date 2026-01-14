"""Async usage example for Agent Marketplace SDK."""

import asyncio

from agent_marketplace_sdk import AsyncMarketplaceClient
from agent_marketplace_sdk.models import ReviewCreate


async def main() -> None:
    """Main async function."""
    # Initialize async client
    async with AsyncMarketplaceClient(api_key="your-api-key") as client:
        # Search agents
        print("=== Searching Agents ===")
        agents = await client.search.search("testing")
        for agent in agents[:5]:
            print(f"- {agent.name}")

        # Get multiple agents in parallel
        print("\n=== Fetching Agents in Parallel ===")
        agent_details = await asyncio.gather(
            *[client.agents.get(agent.slug) for agent in agents[:3]]
        )
        for agent in agent_details:
            print(f"- {agent.name}: {agent.stars} stars")

        # Star and review agents
        if agents:
            first_agent = agents[0]

            print(f"\n=== Starring {first_agent.name} ===")
            await client.agents.star(first_agent.slug)
            print("Starred!")

            print(f"\n=== Reviewing {first_agent.name} ===")
            review = await client.reviews.create(
                first_agent.slug,
                ReviewCreate(rating=5, comment="Great agent!"),
            )
            print(f"Review created with rating: {review.rating}")

        # Get user profile
        print("\n=== User Profile ===")
        user = await client.users.me()
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Reputation: {user.reputation}")


if __name__ == "__main__":
    asyncio.run(main())
