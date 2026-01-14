"""Publish agent example for Agent Marketplace SDK."""

from pathlib import Path

from agent_marketplace_sdk import MarketplaceClient
from agent_marketplace_sdk.models import AgentCreate

# Initialize client
with MarketplaceClient(api_key="your-api-key") as client:
    # Create agent data
    agent_data = AgentCreate(
        name="My Custom Agent",
        description="A custom agent that does amazing things with code analysis.",
        category="testing",
        version="1.0.0",
    )

    # Publish new agent
    print("=== Publishing Agent ===")
    agent = client.agents.publish(
        agent_data=agent_data,
        code_path=Path("./my-agent"),
    )
    print(f"Published: {agent.slug}")
    print(f"Status: {'Validated' if agent.is_validated else 'Pending validation'}")

    # Update agent with new version
    print("\n=== Updating Agent ===")
    updated = client.agents.update(
        slug=agent.slug,
        version="1.1.0",
        code_path=Path("./my-agent"),
        changelog="Added new features and bug fixes",
    )
    print(f"Updated to version: {updated.current_version}")

    # Delete agent
    print("\n=== Deleting Agent ===")
    client.agents.delete(agent.slug)
    print("Agent deleted successfully")
