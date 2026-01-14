# Authentication

The Agent Marketplace SDK uses API key authentication.

## Getting an API Key

1. Sign up at [Agent Marketplace](https://agent-marketplace.com)
2. Navigate to Settings > API Keys
3. Create a new API key
4. Copy the key (it won't be shown again)

## Configuration Methods

### Environment Variable (Recommended)

Set the `MARKETPLACE_API_KEY` environment variable:

```bash
export MARKETPLACE_API_KEY="your-api-key"
```

Then initialize the client without passing the key:

```python
from agent_marketplace_sdk import MarketplaceClient

client = MarketplaceClient()  # Uses MARKETPLACE_API_KEY
```

### Direct Parameter

Pass the API key directly to the client:

```python
client = MarketplaceClient(api_key="your-api-key")
```

### Configuration File

Create a TOML configuration file:

```toml
# ~/.marketplace/config.toml
api_key = "your-api-key"
base_url = "https://api.agent-marketplace.com"
timeout = 30.0
max_retries = 3
```

Load the configuration:

```python
from agent_marketplace_sdk import MarketplaceConfig, MarketplaceClient

config = MarketplaceConfig.from_file("~/.marketplace/config.toml")
client = MarketplaceClient(
    api_key=config.api_key,
    base_url=config.base_url,
    timeout=config.timeout,
)
```

## Security Best Practices

1. **Never commit API keys** - Add `.env` and config files to `.gitignore`
2. **Use environment variables** - Preferred for production deployments
3. **Rotate keys regularly** - Create new keys periodically
4. **Use minimal permissions** - Request only the permissions you need
5. **Monitor usage** - Check for unusual activity in the dashboard

## Error Handling

If authentication fails, an `AuthenticationError` is raised:

```python
from agent_marketplace_sdk import MarketplaceClient
from agent_marketplace_sdk.exceptions import AuthenticationError

try:
    client = MarketplaceClient(api_key="invalid-key")
    client.agents.list()
except AuthenticationError:
    print("Invalid API key")
```
