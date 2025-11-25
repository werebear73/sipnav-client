"""Rate Deck resources for account and carrier rate decks."""

from typing import Any, Dict, Optional
from .base import BaseResource


class RateDeckResource(BaseResource):
    """Handle rate deck operations for both accounts and carriers."""

    # Account Rate Deck Methods
    def get_account_rate_decks(
        self,
        local: Optional[int] = None,
        enabled: Optional[int] = None,
        account_id: Optional[int] = None,
        platform_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get account rate decks.
        
        Args:
            local: Type of rate deck (0=international, 1=local)
            enabled: Filter enabled/disabled rate decks (0 or 1)
            account_id: Account ID filter
            platform_id: Optional platform ID
            
        Returns:
            List of account rate decks
        """
        params = {}
        if local is not None:
            params["local"] = local
        if enabled is not None:
            params["enabled"] = enabled
        if account_id is not None:
            params["account_id"] = account_id
        if platform_id:
            params["platform_id"] = platform_id
        return self._get("/api/account-rate-deck", params=params)

    def upload_account_rate_deck(
        self,
        file_path: str,
        account_id: Optional[int] = None,
        local: Optional[int] = None,
        platform_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Upload account rate deck CSV file.
        
        Note: This is a file upload operation that requires special handling.
        You may need to use requests directly for multipart/form-data.
        
        Args:
            file_path: Path to CSV file
            account_id: Account ID
            local: Type of rate deck (0=international, 1=local)
            platform_id: Optional platform ID
            
        Returns:
            Upload response with file details
        """
        # File upload would require multipart/form-data handling
        # This is a placeholder - actual implementation would need requests or httpx
        raise NotImplementedError("File upload requires multipart/form-data handling")

    def process_account_rate_deck(
        self,
        account_id: int,
        crd_id: int,
        filename: str,
        fieldsmap: Dict[str, str],
        platform_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Initiate account rate deck CSV file processing.
        
        Args:
            account_id: Account ID
            crd_id: Rate deck ID
            filename: Name of uploaded file
            fieldsmap: Mapping of CSV columns to fields
            platform_id: Optional platform ID
            
        Returns:
            Processing response
        """
        data = {
            "account_id": account_id,
            "crd_id": crd_id,
            "filename": filename,
            "fieldsmap": fieldsmap,
        }
        params = {}
        if platform_id:
            params["platform_id"] = platform_id
        return self._post("/api/account-rate-deck/process", data=data, params=params)

    # Carrier Rate Deck Methods
    def get_carrier_rate_decks(
        self,
        local: Optional[int] = None,
        carrier_id: Optional[int] = None,
        platform_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get carrier rate decks.
        
        Args:
            local: Type of rate deck (0=international, 1=local)
            carrier_id: Carrier ID filter
            platform_id: Optional platform ID
            
        Returns:
            List of carrier rate decks
        """
        params = {}
        if local is not None:
            params["local"] = local
        if carrier_id is not None:
            params["carrier_id"] = carrier_id
        if platform_id:
            params["platform_id"] = platform_id
        return self._get("/api/carrier-rate-deck", params=params)

    def upload_carrier_rate_deck(
        self,
        file_path: str,
        carrier_id: Optional[int] = None,
        local: Optional[int] = None,
        platform_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Upload carrier rate deck CSV file.
        
        Note: This is a file upload operation that requires special handling.
        
        Args:
            file_path: Path to CSV file
            carrier_id: Carrier ID
            local: Type of rate deck (0=international, 1=local)
            platform_id: Optional platform ID
            
        Returns:
            Upload response with file details
        """
        raise NotImplementedError("File upload requires multipart/form-data handling")

    def process_carrier_rate_deck(
        self,
        carrier_id: int,
        crd_id: int,
        filename: str,
        fieldsmap: Dict[str, str],
    ) -> Dict[str, Any]:
        """Initiate carrier rate deck CSV file processing.
        
        Args:
            carrier_id: Carrier ID
            crd_id: Rate deck ID
            filename: Name of uploaded file
            fieldsmap: Mapping of CSV columns to fields
            
        Returns:
            Processing response
        """
        data = {
            "carrier_id": carrier_id,
            "crd_id": crd_id,
            "filename": filename,
            "fieldsmap": fieldsmap,
        }
        return self._post("/api/carrier-rate-deck/process", data=data)

    def check_rate_deck_status(
        self, filename: str, platform_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Check uploaded rate deck processing status.
        
        Args:
            filename: Name of the file to check status
            platform_id: Optional platform ID
            
        Returns:
            Status information
        """
        params = {"filename": filename}
        if platform_id:
            params["platform_id"] = platform_id
        return self._get("/api/carrier-rate-deck/status", params=params)

    def download_rate_deck(
        self, rate_deck_id: int, local: Optional[int] = None, platform_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Download system rate deck file link (valid for 1 hour).
        
        Args:
            rate_deck_id: Rate deck ID
            local: Type of rate deck (0=international, 1=local)
            platform_id: Optional platform ID
            
        Returns:
            Download link information
        """
        params = {}
        if local is not None:
            params["local"] = local
        if platform_id:
            params["platform_id"] = platform_id
        return self._post(f"/api/carrier-rate-deck/download/{rate_deck_id}", params=params)

    def get_failures(self, crd_id: int, platform_id: Optional[int] = None) -> Dict[str, Any]:
        """Get link to download failed rows from carrier rate deck.
        
        Args:
            crd_id: Carrier rate deck ID
            platform_id: Optional platform ID
            
        Returns:
            Link to failed rows file (valid for 1 hour)
        """
        params = {"crd_id": crd_id}
        if platform_id:
            params["platform_id"] = platform_id
        return self._get("/api/carrier-rate-deck/failures", params=params)
