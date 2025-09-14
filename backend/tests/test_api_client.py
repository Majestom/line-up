"""
Unit tests for ReqRes API client.
"""
import pytest
from api_client import ReqResAPIClient


class TestReqResAPIClient:
    """Test ReqRes API client business logic."""

    @pytest.fixture
    def api_client(self):
        """Create API client instance for testing."""
        return ReqResAPIClient()

    def test_get_headers_includes_api_key(self, api_client):
        """Test headers include API key when configured."""
        api_client.api_key = "test-api-key"
        headers = api_client._get_headers()

        assert headers["x-api-key"] == "test-api-key"
        assert "User-Agent" in headers
        assert "Accept" in headers
        assert "Content-Type" in headers

    def test_get_headers_no_api_key(self, api_client):
        """Test headers work without API key."""
        api_client.api_key = ""
        headers = api_client._get_headers()

        assert "x-api-key" not in headers
        assert "User-Agent" in headers
        assert "Accept" in headers

    def test_client_initialization(self, api_client):
        """Test API client initializes with correct base URL."""
        assert "reqres.in/api" in api_client.base_url
        assert hasattr(api_client, 'api_key')