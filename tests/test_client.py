"""Tests for the SipNavClient class."""

import pytest
from unittest.mock import Mock, patch
from sipnav import SipNavClient
from sipnav.exceptions import AuthenticationError, APIError, SipNavException


@pytest.fixture
def client():
    """Create a test client instance."""
    return SipNavClient(api_key="test_api_key", base_url="https://api.test.com")


def test_client_initialization(client):
    """Test that the client initializes correctly."""
    assert client.api_key == "test_api_key"
    assert client.base_url == "https://api.test.com"
    assert client.timeout == 30


def test_get_headers(client):
    """Test that headers are correctly formatted."""
    headers = client._get_headers()
    assert headers["Authorization"] == "Bearer test_api_key"
    assert headers["Content-Type"] == "application/json"
    assert headers["Accept"] == "application/json"


@patch("sipnav.client.requests.Session.request")
def test_successful_get_request(mock_request, client):
    """Test a successful GET request."""
    mock_response = Mock()
    mock_response.ok = True
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "test"}
    mock_request.return_value = mock_response
    
    result = client.get("/test/endpoint")
    
    assert result == {"data": "test"}
    mock_request.assert_called_once()


@patch("sipnav.client.requests.Session.request")
def test_authentication_error(mock_request, client):
    """Test that authentication errors are raised correctly."""
    mock_response = Mock()
    mock_response.ok = False
    mock_response.status_code = 401
    mock_request.return_value = mock_response
    
    with pytest.raises(AuthenticationError):
        client.get("/test/endpoint")


@patch("sipnav.client.requests.Session.request")
def test_api_error(mock_request, client):
    """Test that API errors are raised correctly."""
    mock_response = Mock()
    mock_response.ok = False
    mock_response.status_code = 400
    mock_response.json.return_value = {"message": "Bad request"}
    mock_request.return_value = mock_response
    
    with pytest.raises(APIError) as exc_info:
        client.get("/test/endpoint")
    
    assert exc_info.value.status_code == 400


def test_context_manager(client):
    """Test that the client works as a context manager."""
    with SipNavClient(api_key="test_key") as client:
        assert client.api_key == "test_key"
