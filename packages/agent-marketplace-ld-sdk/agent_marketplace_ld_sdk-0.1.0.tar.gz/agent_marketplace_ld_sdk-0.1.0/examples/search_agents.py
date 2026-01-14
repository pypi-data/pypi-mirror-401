"""Search agents example for Agent Marketplace SDK."""

from agent_marketplace_sdk import MarketplaceClient

# Initialize client with context manager
with MarketplaceClient(api_key="your-api-key") as client:
    # Basic search
    print("=== Basic Search ===")
    agents = client.search.search("code review")
    for agent in agents:
        print(f"- {agent.name}: {agent.rating} stars")

    # Search with filters
    print("\n=== Filtered Search ===")
    filtered = client.search.search(
        query="testing",
        category="testing",
        min_rating=4.0,
        sort="downloads",
        limit=10,
    )
    for agent in filtered:
        print(f"- {agent.name}: {agent.downloads} downloads")

    # Get trending agents
    print("\n=== Trending Agents ===")
    trending = client.analytics.get_trending(limit=5)
    for agent in trending:
        print(f"- {agent.name}: trend score {agent.trend_score}")
