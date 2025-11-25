"""Accounts resource for managing accounts."""

from typing import Any, Dict, List, Optional
from .base import BaseResource


class AccountsResource(BaseResource):
    """Handle account operations."""

    def list(
        self,
        external: int = 1,
        platform_id: Optional[int] = None,
        company_id: Optional[int] = None,
        platform_filter: Optional[List[int]] = None,
        per_page: int = 100,
    ) -> Dict[str, Any]:
        """Retrieve paginated list of accounts.
        
        Args:
            external: External request flag (0 or 1, default 1)
            platform_id: Optional platform ID filter
            company_id: Optional company ID filter
            platform_filter: Optional list of platform IDs to filter by
            per_page: Number of accounts per page (default 100)
            
        Returns:
            Paginated list of accounts with detailed data
        """
        params: Dict[str, Any] = {"external": external, "per_page": per_page}
        if platform_id:
            params["platform_id"] = platform_id
        if company_id:
            params["company_id"] = company_id
        if platform_filter:
            params["platform_filter"] = platform_filter
        return self._get("/api/accounts", params=params)

    def get(self, account_id: int, external: int = 1, platform_id: Optional[int] = None) -> Dict[str, Any]:
        """Get account details by ID.
        
        Args:
            account_id: Account ID
            external: External request flag (default 1)
            platform_id: Optional platform ID
            
        Returns:
            Account details
        """
        params: Dict[str, Any] = {"external": external}
        if platform_id:
            params["platform_id"] = platform_id
        return self._get(f"/api/accounts/{account_id}", params=params)

    def create(self, account_data: Dict[str, Any], external: int = 1, platform_id: Optional[int] = None) -> Dict[str, Any]:
        """Create a new account.
        
        Args:
            account_data: Account data dictionary
            external: External request flag (default 1)
            platform_id: Optional platform ID
            
        Returns:
            Created account data
        """
        params: Dict[str, Any] = {"external": external}
        if platform_id:
            params["platform_id"] = platform_id
        return self._post("/api/accounts", data=account_data, params=params)

    def update(
        self, 
        account_id: int, 
        account_data: Dict[str, Any], 
        external: int = 1, 
        platform_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Update account details.
        
        Args:
            account_id: Account ID to update
            account_data: Updated account data
            external: External request flag (default 1)
            platform_id: Optional platform ID
            
        Returns:
            Updated account data
        """
        params: Dict[str, Any] = {"external": external}
        if platform_id:
            params["platform_id"] = platform_id
        return self._put(f"/api/accounts/{account_id}", data=account_data, params=params)

    def get_carriers(
        self, 
        account_id: int, 
        external: int = 1, 
        platform_id: Optional[int] = None,
        per_page: int = 10
    ) -> Dict[str, Any]:
        """Get carriers for a specific account.
        
        Args:
            account_id: Account ID
            external: External request flag (default 1)
            platform_id: Optional platform ID
            per_page: Number of carriers per page (default 10)
            
        Returns:
            List of carriers for the account
        """
        params: Dict[str, Any] = {"external": external, "per_page": per_page}
        if platform_id:
            params["platform_id"] = platform_id
        return self._get(f"/api/accountcarriers/{account_id}", params=params)
