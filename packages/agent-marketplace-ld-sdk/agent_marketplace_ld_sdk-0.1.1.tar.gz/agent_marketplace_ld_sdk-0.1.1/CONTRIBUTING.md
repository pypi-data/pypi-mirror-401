# Contributing to agent-marketplace-ld-sdk

Thank you for your interest in contributing to the Agent Marketplace SDK!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/kmcallorum/agent-marketplace-ld-sdk.git
cd agent-marketplace-ld-sdk
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/agent_marketplace_sdk --cov-report=term

# Run specific test file
pytest tests/unit/test_client.py

# Run with verbose output
pytest -v
```

## Code Quality

### Linting

```bash
# Check for issues
ruff check src tests

# Fix auto-fixable issues
ruff check --fix src tests

# Format code
ruff format src tests
```

### Type Checking

```bash
mypy src
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Write docstrings for public APIs
- Keep functions focused and small
- Write tests for new functionality

## Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less

## Questions?

Feel free to open an issue for any questions or concerns.
