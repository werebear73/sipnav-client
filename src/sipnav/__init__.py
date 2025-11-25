"""SIPNAV Python Client Library."""

from .client import SipNavClient
from .exceptions import SipNavException, AuthenticationError, APIError

try:
    from ._version import __version__
except ImportError:
    __version__ = "0.0.0.dev0"

__all__ = ["SipNavClient", "SipNavException", "AuthenticationError", "APIError"]
