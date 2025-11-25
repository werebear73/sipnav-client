"""Call Restrictions resource for managing call restrictions."""

from typing import Any, Dict, Optional
from .base import BaseResource


class CallRestrictionsResource(BaseResource):
    """Handle call restriction operations."""

    def list(
        self,
        platform_id: Optional[int] = None,
        carrier_id: Optional[int] = None,
        account_id: Optional[int] = None,
        src_number: Optional[int] = None,
        dst_number: Optional[int] = None,
        per_page: int = 100,
        page_token: str = "",
    ) -> Dict[str, Any]:
        """Retrieve main list of call restrictions.
        
        Args:
            platform_id: Optional platform ID
            carrier_id: Carrier ID to filter results
            account_id: Account ID to filter results
            src_number: Source number to filter results
            dst_number: Destination number to filter results
            per_page: Number of results per page (10, 25, 50, 100, 1000)
            page_token: Paging token for subsequent requests
            
        Returns:
            List of call restrictions
        """
        params: Dict[str, Any] = {"per_page": per_page, "page_token": page_token}
        if platform_id:
            params["platform_id"] = platform_id
        if carrier_id:
            params["carrier_id"] = carrier_id
        if account_id:
            params["account_id"] = account_id
        if src_number:
            params["src_number"] = src_number
        if dst_number:
            params["dst_number"] = dst_number
        return self._get("/api/call-restrictions/num", params=params)

    def get(self, restriction_id: int, platform_id: Optional[int] = None) -> Dict[str, Any]:
        """Get single call restriction record.
        
        Args:
            restriction_id: Restriction ID to retrieve
            platform_id: Optional platform ID
            
        Returns:
            Call restriction details
        """
        params = {}
        if platform_id:
            params["platform_id"] = platform_id
        return self._get(f"/api/call-restrictions/num/{restriction_id}", params=params)

    def create(
        self,
        priority: int,
        carrier_id: int,
        account_id: int,
        dst_number: int,
        restriction_start: str,
        restriction_end: str,
        src_number: Optional[str] = None,
        src_match_type: int = 0,
        note: Optional[str] = None,
        platform_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Create a new call restriction record.
        
        Args:
            priority: Priority (positive integer from 1 and up)
            carrier_id: Carrier ID (0 for all, else specific carrier_id)
            account_id: Account ID (0 for all, else specific account_id)
            dst_number: Destination phone number
            restriction_start: Start date/time (e.g., '2025-01-01 00:00:00')
            restriction_end: End date/time (e.g., '2055-12-31 23:59:59')
            src_number: Source phone number (optional, up to 16 digits)
            src_match_type: Match type (0=default, 1=starts with, 2=exact)
            note: Optional note (max 100 chars)
            platform_id: Optional platform ID
            
        Returns:
            Created restriction data
        """
        params: Dict[str, Any] = {
            "priority": priority,
            "carrier_id": carrier_id,
            "account_id": account_id,
            "dst_number": dst_number,
            "restriction_start": restriction_start,
            "restriction_end": restriction_end,
            "src_match_type": src_match_type,
        }
        if src_number:
            params["src_number"] = src_number
        if note:
            params["note"] = note
        if platform_id:
            params["platform_id"] = platform_id
        return self._post("/api/call-restrictions/num", params=params)

    def update(
        self,
        restriction_id: int,
        priority: Optional[int] = None,
        carrier_id: Optional[int] = None,
        account_id: Optional[int] = None,
        src_number: Optional[str] = None,
        src_match_type: Optional[int] = None,
        dst_number: Optional[int] = None,
        restriction_start: Optional[str] = None,
        restriction_end: Optional[str] = None,
        note: Optional[str] = None,
        platform_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update a call restriction record (partial update).
        
        Args:
            restriction_id: Restriction ID to update
            priority: Priority (optional)
            carrier_id: Carrier ID (optional)
            account_id: Account ID (optional)
            src_number: Source phone number (optional)
            src_match_type: Match type (optional)
            dst_number: Destination phone number (optional)
            restriction_start: Start date/time (optional)
            restriction_end: End date/time (optional)
            note: Optional note (optional)
            platform_id: Optional platform ID
            
        Returns:
            Updated restriction data
        """
        params: Dict[str, Any] = {"restriction_id": restriction_id}
        if priority is not None:
            params["priority"] = priority
        if carrier_id is not None:
            params["carrier_id"] = carrier_id
        if account_id is not None:
            params["account_id"] = account_id
        if src_number is not None:
            params["src_number"] = src_number
        if src_match_type is not None:
            params["src_match_type"] = src_match_type
        if dst_number is not None:
            params["dst_number"] = dst_number
        if restriction_start is not None:
            params["restriction_start"] = restriction_start
        if restriction_end is not None:
            params["restriction_end"] = restriction_end
        if note is not None:
            params["note"] = note
        if platform_id:
            params["platform_id"] = platform_id
        return self._patch("/api/call-restrictions/num", params=params)

    def disable(self, restriction_id: int, platform_id: Optional[int] = None) -> Dict[str, Any]:
        """Disable a call restriction record.
        
        Args:
            restriction_id: Restriction ID to disable
            platform_id: Optional platform ID
            
        Returns:
            Response confirming disable
        """
        params = {}
        if platform_id:
            params["platform_id"] = platform_id
        return self._patch(f"/api/call-restrictions/num/{restriction_id}", params=params)

    def get_history(
        self, platform_id: Optional[int] = None, per_page: int = 100, page_token: str = ""
    ) -> Dict[str, Any]:
        """Retrieve call restriction history.
        
        Args:
            platform_id: Optional platform ID
            per_page: Number of results per page (10, 25, 50, 100, 1000)
            page_token: Paging token for subsequent requests
            
        Returns:
            Call restriction history
        """
        params: Dict[str, Any] = {"per_page": per_page, "page_token": page_token}
        if platform_id:
            params["platform_id"] = platform_id
        return self._get("/api/call-restrictions/history", params=params)
