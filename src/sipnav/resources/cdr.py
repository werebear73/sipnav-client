"""CDR (Call Detail Records) resource."""

from typing import Any, Dict, Optional
from .base import BaseResource


class CDRResource(BaseResource):
    """Handle CDR search operations."""

    def search(
        self,
        p_id: Optional[str] = None,
        lrn_number: Optional[str] = None,
        account_id: Optional[str] = None,
        carrier_id: Optional[str] = None,
        src_number: Optional[str] = None,
        dst_number: Optional[str] = None,
        start_date: Optional[str] = None,
        end_time: Optional[str] = None,
        min_duration: Optional[int] = None,
        max_duration: Optional[int] = None,
        search_completed: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Search CDR records.
        
        Args:
            p_id: Platform ID
            lrn_number: LRN number
            account_id: Account ID
            carrier_id: Carrier ID
            src_number: Source/Caller ID
            dst_number: Destination/Called Number
            start_date: Time range start (e.g., '2025-02-27 01:02:03')
            end_time: Time range end (e.g., '2025-02-28 01:02:03')
            min_duration: Minimum actual duration
            max_duration: Maximum actual duration
            search_completed: Completed search flag
            limit: Result limit
            
        Returns:
            CDR search results
        """
        params = {}
        if p_id is not None:
            params["p_id"] = p_id
        if lrn_number is not None:
            params["lrn_number"] = lrn_number
        if account_id is not None:
            params["account_id"] = account_id
        if carrier_id is not None:
            params["carrier_id"] = carrier_id
        if src_number is not None:
            params["src_number"] = src_number
        if dst_number is not None:
            params["dst_number"] = dst_number
        if start_date is not None:
            params["start_date"] = start_date
        if end_time is not None:
            params["end_time"] = end_time
        if min_duration is not None:
            params["min_duration"] = min_duration
        if max_duration is not None:
            params["max_duration"] = max_duration
        if search_completed is not None:
            params["search_completed"] = search_completed
        if limit is not None:
            params["limit"] = limit
        
        return self._get("/api/cdr/search", params=params)
