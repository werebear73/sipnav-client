"""Carriers resource for managing carriers."""

from typing import Any, Dict, List, Optional
from .base import BaseResource


class CarriersResource(BaseResource):
    """Handle carrier operations."""

    def list(
        self,
        external: int = 1,
        platform_id: Optional[int] = None,
        company_id: Optional[int] = None,
        platform_filter: Optional[List[int]] = None,
        per_page: int = 10,
        page: int = 1,
    ) -> Dict[str, Any]:
        """Retrieve paginated list of carriers.
        
        Args:
            external: External request flag (0 or 1, default 1)
            platform_id: Optional platform ID filter
            company_id: Optional company ID filter
            platform_filter: Optional list of platform IDs to filter by
            per_page: Number of carriers per page (default 10)
            page: Page number to retrieve (default 1)
            
        Returns:
            Paginated list of carriers with detailed data
        """
        params: Dict[str, Any] = {"external": external, "per_page": per_page, "page": page}
        if platform_id:
            params["platform_id"] = platform_id
        if company_id:
            params["company_id"] = company_id
        if platform_filter:
            params["platform_filter"] = platform_filter
        return self._get("/api/carriers", params=params)

    def get(self, carrier_id: int, external: int = 1, platform_id: Optional[int] = None) -> Dict[str, Any]:
        """Get carrier details by ID.
        
        Args:
            carrier_id: Carrier ID
            external: External request flag (default 1)
            platform_id: Optional platform ID
            
        Returns:
            Carrier details
        """
        params: Dict[str, Any] = {"external": external}
        if platform_id:
            params["platform_id"] = platform_id
        return self._get(f"/api/carriers/{carrier_id}", params=params)

    def create(self, carrier_data: Dict[str, Any], external: int = 1, platform_id: Optional[int] = None) -> Dict[str, Any]:
        """Create a new carrier.
        
        Args:
            carrier_data: Carrier data dictionary
            external: External request flag (default 1)
            platform_id: Optional platform ID
            
        Returns:
            Created carrier data
        """
        params: Dict[str, Any] = {"external": external}
        if platform_id:
            params["platform_id"] = platform_id
        return self._post("/api/carriers", data=carrier_data, params=params)

    def update(
        self, 
        carrier_id: int, 
        carrier_data: Dict[str, Any], 
        external: int = 1, 
        platform_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Update carrier details.
        
        Args:
            carrier_id: Carrier ID to update
            carrier_data: Updated carrier data
            external: External request flag (default 1)
            platform_id: Optional platform ID
            
        Returns:
            Updated carrier data
        """
        params: Dict[str, Any] = {"external": external}
        if platform_id:
            params["platform_id"] = platform_id
        return self._put(f"/api/carriers/{carrier_id}", data=carrier_data, params=params)

    def get_accounts(
        self, 
        carrier_id: int, 
        external: int = 1, 
        platform_id: Optional[int] = None,
        per_page: int = 10
    ) -> Dict[str, Any]:
        """Get accounts for a specific carrier.
        
        Args:
            carrier_id: Carrier ID
            external: External request flag (default 1)
            platform_id: Optional platform ID
            per_page: Number of accounts per page (default 10)
            
        Returns:
            List of accounts for the carrier
        """
        params: Dict[str, Any] = {"external": external, "per_page": per_page}
        if platform_id:
            params["platform_id"] = platform_id
        return self._get(f"/api/carrieraccounts/{carrier_id}", params=params)
