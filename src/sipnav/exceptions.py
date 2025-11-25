"""Custom exceptions for the SIPNAV client library."""


class SipNavException(Exception):
    """Base exception for all SIPNAV client errors."""
    pass


class AuthenticationError(SipNavException):
    """Raised when authentication fails."""
    pass


class APIError(SipNavException):
    """Raised when the API returns an error response."""
    
    def __init__(self, message: str, status_code: int = None) -> None:
        super().__init__(message)
        self.status_code = status_code
