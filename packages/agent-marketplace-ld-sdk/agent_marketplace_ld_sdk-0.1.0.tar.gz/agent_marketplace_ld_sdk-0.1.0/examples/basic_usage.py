"""Basic usage example for Agent Marketplace SDK."""

from agent_marketplace_sdk import MarketplaceClient

# Initialize client
client = MarketplaceClient(api_key="your-api-key")

# List agents
print("=== Listing Agents ===")
agents = client.agents.list(limit=5)
for agent in agents:
    print(f"- {agent.name} ({agent.slug}): {agent.description[:50]}...")

# Get agent details
print("\n=== Agent Details ===")
agent = client.agents.get("advanced-pm")
print(f"Name: {agent.name}")
print(f"Stars: {agent.stars}")
print(f"Rating: {agent.rating}")
print(f"Downloads: {agent.downloads}")

# Get categories
print("\n=== Categories ===")
categories = client.categories.list()
for category in categories:
    print(f"- {category.name}: {category.agent_count} agents")

# Close client
client.close()
