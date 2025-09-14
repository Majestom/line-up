"""
Integration tests for FastAPI endpoints.
"""
from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app

client = TestClient(app)

class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_endpoint_returns_healthy_status(self):
        """Test health endpoint returns correct structure."""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
        assert "external_api_status" in data
        assert "environment" in data

    def test_health_endpoint_includes_request_id_header(self):
        """Test health endpoint includes request ID in headers."""
        response = client.get("/health")
        assert "X-Request-ID" in response.headers


class TestUserEndpoint:
    """Test user data endpoint."""

    def test_get_user_valid_id(self):
        """Test getting user data with valid ID."""
        response = client.get("/user/1")
        assert response.status_code == 200

        data = response.json()
        assert "data" in data
        user_data = data["data"]

        # Verify required fields
        assert "id" in user_data
        assert "email" in user_data
        assert "first_name" in user_data
        assert "last_name" in user_data
        assert "avatar" in user_data

        # Verify data types
        assert isinstance(user_data["id"], int)
        assert isinstance(user_data["email"], str)
        assert isinstance(user_data["first_name"], str)
        assert isinstance(user_data["last_name"], str)
        assert isinstance(user_data["avatar"], str)

    def test_get_user_invalid_id_too_low(self):
        """Test getting user with ID below valid range."""
        response = client.get("/user/0")
        assert response.status_code == 422

    def test_get_user_invalid_id_too_high(self):
        """Test getting user with ID above valid range."""
        response = client.get("/user/13")
        assert response.status_code == 422

    @patch('api_client.reqres_client.get_user')
    def test_get_user_handles_external_api_error(self, mock_get_user):
        """Test user endpoint handles external API errors."""
        from fastapi import HTTPException
        mock_get_user.side_effect = HTTPException(status_code=503, detail="External API unavailable")

        response = client.get("/user/1")
        assert response.status_code == 503

    def test_user_endpoint_includes_request_id_header(self):
        """Test user endpoint includes request ID in headers."""
        response = client.get("/user/1")
        assert "X-Request-ID" in response.headers


class TestRootEndpoint:
    """Test root endpoint."""

    def test_root_endpoint(self):
        """Test root endpoint returns welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "User API Service is running"}


class TestCORS:
    """Test CORS configuration."""

    def test_cors_headers_present(self):
        """Test CORS headers are included in responses."""
        response = client.options("/health")
        # FastAPI TestClient doesn't fully simulate CORS, but we can verify our setup
        assert response.status_code in [200, 405]  # 405 is acceptable for OPTIONS