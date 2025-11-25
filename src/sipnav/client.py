"""Main client for interacting with the SIPNAV REST API."""

from typing import Any, Dict, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import SipNavException, AuthenticationError, APIError
from .resources import (
    AccountsResource,
    CarriersResource,
    CompaniesResource,
    CDRResource,
    CallRestrictionsResource,
    AuthenticationResource,
    LRNResource,
    RateDeckResource,
)


class SipNavClient:
    """Client for interacting with the SIPNAV REST API.
    
    Args:
        api_key: API key for authentication (Bearer token). Optional if username/password provided.
        base_url: Base URL for the SIPNAV API (default: https://api.bluedragonnetwork.com)
        platform_id: Optional platform ID for multi-platform users
        timeout: Request timeout in seconds (default: 30)
        max_retries: Maximum number of retry attempts (default: 3)
        username: Username for authentication. Used with password to obtain bearer token.
        password: Password for authentication. Used with username to obtain bearer token.
        
    Examples:
        Using bearer token:
            >>> client = SipNavClient(api_key="your_token")
        
        Using username and password:
            >>> client = SipNavClient(username="user@example.com", password="secret")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.bluedragonnetwork.com",
        platform_id: Optional[int] = None,
        timeout: int = 30,
        max_retries: int = 3,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.platform_id = platform_id
        self.timeout = timeout
        self.session = self._create_session(max_retries)
        
        # Authenticate if username and password provided
        if username and password:
            self.api_key = self._login(username, password)
        elif api_key:
            self.api_key = api_key
        else:
            raise ValueError("Either api_key or both username and password must be provided")
        
        # Initialize resource classes
        self.accounts = AccountsResource(self)
        self.carriers = CarriersResource(self)
        self.companies = CompaniesResource(self)
        self.cdr = CDRResource(self)
        self.call_restrictions = CallRestrictionsResource(self)
        self.auth = AuthenticationResource(self)
        self.lrn = LRNResource(self)
        self.rate_decks = RateDeckResource(self)

    def _create_session(self, max_retries: int) -> requests.Session:
        """Create a requests session with retry logic."""
        session = requests.Session()
        
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session

    def _login(self, username: str, password: str) -> str:
        """Authenticate with username and password to obtain bearer token.
        
        Args:
            username: User's username
            password: User's password
            
        Returns:
            Bearer token for API authentication
            
        Raises:
            AuthenticationError: If login fails
            SipNavException: For other errors
        """
        url = f"{self.base_url}/api/login"
        payload = {
            "username": username,
            "password": password,
        }
        
        # Add platform_id if set
        if self.platform_id:
            payload["platform_id"] = self.platform_id
        
        try:
            response = self.session.post(
                url=url,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                timeout=self.timeout,
            )
            
            if response.status_code == 401:
                raise AuthenticationError("Invalid username or password")
            
            if not response.ok:
                error_msg = f"Login failed with status {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg = error_data.get("message", error_msg)
                except ValueError:
                    error_msg = response.text or error_msg
                raise AuthenticationError(error_msg)
            
            response_data = response.json()
            
            # Extract token from response
            if "data" in response_data and "token" in response_data["data"]:
                return response_data["data"]["token"]
            elif "token" in response_data:
                return response_data["token"]
            else:
                raise SipNavException("Token not found in login response")
                
        except requests.exceptions.RequestException as e:
            raise SipNavException(f"Login request failed: {str(e)}") from e

    def _get_headers(self) -> Dict[str, str]:
        """Get default headers for API requests."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        # Add platform_id as query param if set (handled in _make_request)
        return headers

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an HTTP request to the SIPNAV API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint path
            data: Request body data
            params: URL query parameters
            
        Returns:
            Response data as a dictionary
            
        Raises:
            AuthenticationError: If authentication fails
            APIError: If the API returns an error
            SipNavException: For other errors
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Add platform_id to params if set and not already in params
        if self.platform_id and params is not None and 'platform_id' not in params:
            params['platform_id'] = self.platform_id
        elif self.platform_id and params is None:
            params = {'platform_id': self.platform_id}
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=self._get_headers(),
                json=data,
                params=params,
                timeout=self.timeout,
            )
            
            # Handle authentication errors
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key or authentication failed")
            
            # Handle other errors
            if not response.ok:
                error_msg = f"API request failed with status {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg = error_data.get("message", error_msg)
                except ValueError:
                    error_msg = response.text or error_msg
                raise APIError(error_msg, status_code=response.status_code)
            
            # Return JSON response
            return response.json() if response.content else {}
            
        except requests.exceptions.RequestException as e:
            raise SipNavException(f"Request failed: {str(e)}") from e

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request to the API."""
        return self._make_request("GET", endpoint, params=params)

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a POST request to the API."""
        return self._make_request("POST", endpoint, data=data, params=params)

    def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a PUT request to the API."""
        return self._make_request("PUT", endpoint, data=data, params=params)

    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a DELETE request to the API."""
        return self._make_request("DELETE", endpoint, params=params)

    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()

    def __enter__(self) -> "SipNavClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()
