"""Base resource class for API resources."""

from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import SipNavClient


class BaseResource:
    """Base class for API resource handlers."""

    def __init__(self, client: "SipNavClient") -> None:
        """Initialize the resource with a client instance.
        
        Args:
            client: SipNavClient instance to use for API calls
        """
        self._client = client

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request."""
        return self._client.get(endpoint, params=params)

    def _post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a POST request."""
        return self._client.post(endpoint, data=data, params=params)

    def _put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a PUT request."""
        return self._client.put(endpoint, data=data, params=params)

    def _delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a DELETE request."""
        return self._client.delete(endpoint, params=params)

    def _patch(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a PATCH request."""
        return self._client._make_request("PATCH", endpoint, data=data, params=params)
