"""Companies resource for managing companies."""

from typing import Any, Dict, List, Optional
from .base import BaseResource


class CompaniesResource(BaseResource):
    """Handle company operations."""

    def list(
        self,
        external: int = 1,
        platform_id: Optional[int] = None,
        platform_filter: Optional[List[int]] = None,
        per_page: int = 10,
    ) -> Dict[str, Any]:
        """Retrieve paginated list of companies.
        
        Args:
            external: External request flag (0 or 1, default 1)
            platform_id: Optional platform ID filter
            platform_filter: Optional list of platform IDs to filter by
            per_page: Number of companies per page (default 10)
            
        Returns:
            Paginated list of companies with detailed data
        """
        params: Dict[str, Any] = {"external": external, "per_page": per_page}
        if platform_id:
            params["platform_id"] = platform_id
        if platform_filter:
            params["platform_filter"] = platform_filter
        return self._get("/api/companies", params=params)

    def get(self, company_id: int, external: int = 1, platform_id: Optional[int] = None) -> Dict[str, Any]:
        """Get company details by ID.
        
        Args:
            company_id: Company ID
            external: External request flag (default 1)
            platform_id: Optional platform ID
            
        Returns:
            Company details including billing info and company detail
        """
        params: Dict[str, Any] = {"external": external}
        if platform_id:
            params["platform_id"] = platform_id
        return self._get(f"/api/companies/{company_id}", params=params)

    def create(self, company_data: Dict[str, Any], external: int = 1, platform_id: Optional[int] = None) -> Dict[str, Any]:
        """Create a new company.
        
        Args:
            company_data: Company data dictionary (customer_name required)
            external: External request flag (default 1)
            platform_id: Optional platform ID
            
        Returns:
            Created company data
        """
        params: Dict[str, Any] = {"external": external}
        if platform_id:
            params["platform_id"] = platform_id
        return self._post("/api/companies", data=company_data, params=params)

    def update(
        self, 
        company_id: int, 
        company_data: Dict[str, Any], 
        external: int = 1, 
        platform_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Update company details.
        
        Args:
            company_id: Company ID to update
            company_data: Updated company data
            external: External request flag (default 1)
            platform_id: Optional platform ID
            
        Returns:
            Updated company data
        """
        params: Dict[str, Any] = {"external": external}
        if platform_id:
            params["platform_id"] = platform_id
        return self._put(f"/api/companies/{company_id}", data=company_data, params=params)

    def get_balance(self, company_id: int, platform_id: Optional[int] = None) -> Dict[str, Any]:
        """Get balance for a company.
        
        Args:
            company_id: Company ID
            platform_id: Optional platform ID
            
        Returns:
            Company balance information
        """
        params = {}
        if platform_id:
            params["platform_id"] = platform_id
        return self._get(f"/api/companies/{company_id}/getBalance", params=params)

    def get_names(self, platform_id: Optional[int] = None) -> Dict[str, Any]:
        """Get list of company names.
        
        Args:
            platform_id: Optional platform ID (for system admins)
            
        Returns:
            List of company names and IDs
        """
        params = {}
        if platform_id:
            params["platform_id"] = platform_id
        return self._get("/api/companies-names", params=params)
