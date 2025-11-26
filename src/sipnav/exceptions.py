"""Custom exceptions for the SIPNAV client library."""


class SipNavException(Exception):
    """Base exception for all SIPNAV client errors."""
    pass


class AuthenticationError(SipNavException):
    """Raised when authentication fails."""
    pass


class APIError(SipNavException):
    """Raised when the API returns an error response.
    
    Attributes:
        message: Error message
        status_code: HTTP status code
        request_method: HTTP method used
        request_url: URL that was requested
    """
    
    def __init__(
        self, 
        message: str, 
        status_code: int = None,
        request_method: str = None,
        request_url: str = None
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.request_method = request_method
        self.request_url = request_url
    
    def __str__(self) -> str:
        """Return a detailed string representation."""
        details = [str(self.args[0]) if self.args else "API Error"]
        if self.status_code:
            details.append(f"Status: {self.status_code}")
        return " | ".join(details)
