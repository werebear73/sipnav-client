"""LRN (Local Routing Number) lookup resource."""

from typing import Any, Dict
from .base import BaseResource


class LRNResource(BaseResource):
    """Handle LRN lookup operations."""

    def lookup(self, phone_number: str) -> Dict[str, Any]:
        """Perform LRN lookup for a phone number.
        
        Args:
            phone_number: Phone number to lookup
            
        Returns:
            LRN lookup results
        """
        return self._get(f"/api/lrnlookup/{phone_number}")
