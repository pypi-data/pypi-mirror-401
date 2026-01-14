"""Tests for exceptions module."""

import pytest
from httpx import Response

from agent_marketplace_sdk.exceptions import (
    AgentNotFoundError,
    AuthenticationError,
    ConfigurationError,
    MarketplaceError,
    NetworkError,
    RateLimitError,
    UserNotFoundError,
    ValidationError,
    handle_response_error,
)


class TestExceptions:
    """Tests for custom exceptions."""

    def test_marketplace_error(self):
        """Test MarketplaceError."""
        error = MarketplaceError("Test error")
        assert str(error) == "Test error"

    def test_agent_not_found_error(self):
        """Test AgentNotFoundError."""
        error = AgentNotFoundError("Agent not found")
        assert isinstance(error, MarketplaceError)

    def test_user_not_found_error(self):
        """Test UserNotFoundError."""
        error = UserNotFoundError("User not found")
        assert isinstance(error, MarketplaceError)

    def test_authentication_error(self):
        """Test AuthenticationError."""
        error = AuthenticationError("Invalid API key")
        assert isinstance(error, MarketplaceError)

    def test_validation_error(self):
        """Test ValidationError."""
        error = ValidationError("Validation failed")
        assert isinstance(error, MarketplaceError)

    def test_network_error(self):
        """Test NetworkError."""
        error = NetworkError("Network error")
        assert isinstance(error, MarketplaceError)

    def test_rate_limit_error(self):
        """Test RateLimitError."""
        error = RateLimitError("Rate limit exceeded")
        assert isinstance(error, MarketplaceError)

    def test_configuration_error(self):
        """Test ConfigurationError."""
        error = ConfigurationError("Configuration error")
        assert isinstance(error, MarketplaceError)


class TestHandleResponseError:
    """Tests for handle_response_error function."""

    def test_handle_401(self):
        """Test handling 401 response."""
        response = Response(401)
        with pytest.raises(AuthenticationError):
            handle_response_error(response)

    def test_handle_404(self):
        """Test handling 404 response."""
        response = Response(404)
        with pytest.raises(AgentNotFoundError):
            handle_response_error(response)

    def test_handle_422_with_detail(self):
        """Test handling 422 response with detail."""
        response = Response(422, json={"detail": "Invalid input"})
        with pytest.raises(ValidationError) as exc_info:
            handle_response_error(response)
        assert "Invalid input" in str(exc_info.value)

    def test_handle_422_without_detail(self):
        """Test handling 422 response without detail."""
        response = Response(422, json={})
        with pytest.raises(ValidationError) as exc_info:
            handle_response_error(response)
        assert "Validation failed" in str(exc_info.value)

    def test_handle_422_invalid_json(self):
        """Test handling 422 response with invalid JSON."""
        response = Response(422, content=b"not json")
        with pytest.raises(ValidationError) as exc_info:
            handle_response_error(response)
        assert "Validation failed" in str(exc_info.value)

    def test_handle_429(self):
        """Test handling 429 response."""
        response = Response(429)
        with pytest.raises(RateLimitError):
            handle_response_error(response)

    def test_handle_500(self):
        """Test handling 500 response."""
        response = Response(500, text="Internal Server Error")
        with pytest.raises(MarketplaceError) as exc_info:
            handle_response_error(response)
        assert "HTTP 500" in str(exc_info.value)

    def test_handle_200_no_error(self):
        """Test handling 200 response (no error)."""
        response = Response(200)
        handle_response_error(response)  # Should not raise
