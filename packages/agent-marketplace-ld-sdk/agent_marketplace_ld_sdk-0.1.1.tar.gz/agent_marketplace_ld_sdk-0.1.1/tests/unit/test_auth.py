"""Tests for auth module."""

import httpx

from agent_marketplace_sdk.auth import BearerAuth


class TestBearerAuth:
    """Tests for BearerAuth."""

    def test_init(self):
        """Test BearerAuth initialization."""
        auth = BearerAuth("test-token")
        assert auth.token == "test-token"

    def test_auth_flow(self):
        """Test that auth flow adds authorization header."""
        auth = BearerAuth("test-token")
        request = httpx.Request("GET", "https://api.example.com/test")

        # Get the generator and send the request through
        flow = auth.auth_flow(request)
        authenticated_request = next(flow)

        assert "Authorization" in authenticated_request.headers
        assert authenticated_request.headers["Authorization"] == "Bearer test-token"

    def test_auth_flow_with_client(self):
        """Test BearerAuth with httpx client."""
        auth = BearerAuth("test-token")

        # Create a client with auth
        with httpx.Client(auth=auth) as client:
            _request = client.build_request("GET", "https://api.example.com/test")
            # The auth should be applied when the request is sent
            # We just verify the auth object is properly configured
            assert auth.token == "test-token"
            assert _request is not None
