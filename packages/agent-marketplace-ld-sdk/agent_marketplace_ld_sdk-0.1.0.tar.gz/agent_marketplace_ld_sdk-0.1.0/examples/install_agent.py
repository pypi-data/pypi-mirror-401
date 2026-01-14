"""Install agent example for Agent Marketplace SDK."""

from pathlib import Path

from agent_marketplace_sdk import MarketplaceClient

# Initialize client
with MarketplaceClient(api_key="your-api-key") as client:
    # Install latest version
    print("=== Installing Agent ===")
    install_path = client.agents.install("advanced-pm", path="./agents")
    print(f"Installed to: {install_path}")

    # Install specific version
    print("\n=== Installing Specific Version ===")
    install_path = client.agents.install(
        "code-reviewer",
        version="2.0.0",
        path="./agents",
    )
    print(f"Installed to: {install_path}")

    # Get agent versions
    print("\n=== Available Versions ===")
    versions = client.agents.get_versions("advanced-pm")
    for version in versions:
        print(f"- {version.version}: {version.changelog or 'No changelog'}")
