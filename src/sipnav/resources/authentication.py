"""Authentication resource for login, logout, and password management."""

from typing import Any, Dict, Optional
from .base import BaseResource


class AuthenticationResource(BaseResource):
    """Handle authentication operations."""

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """User login.
        
        Args:
            username: User's username
            password: User's password
            
        Returns:
            Response containing access token and user information
        """
        data = {"username": username, "password": password}
        return self._post("/api/login", data=data)

    def logout(self) -> Dict[str, Any]:
        """Logout current user.
        
        Returns:
            Logout confirmation response
        """
        return self._post("/api/logout")

    def send_password_reset_email(
        self, username: str, platform_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Send password reset email.
        
        Args:
            username: Username to reset password for
            platform_id: Optional platform ID for sipnav admin
            
        Returns:
            Response confirming email sent
        """
        params = {}
        if platform_id:
            params["platform_id"] = platform_id
        return self._get(f"/api/password/email/{username}", params=params)

    def reset_password(
        self, encrypted_user: str, temp_password: str, new_password: str, confirm_password: str
    ) -> Dict[str, Any]:
        """Reset user password.
        
        Args:
            encrypted_user: Encrypted user ID from reset email
            temp_password: Temporary password from email
            new_password: New password to set
            confirm_password: Password confirmation
            
        Returns:
            Response confirming password reset
        """
        data = {
            "t_password": temp_password,
            "password": new_password,
            "c_password": confirm_password,
        }
        return self._post(f"/api/password/reset/{encrypted_user}", data=data)

    def verify_otp(self, encrypted_user: str, two_factor_code: int) -> Dict[str, Any]:
        """Verify one-time password code.
        
        Args:
            encrypted_user: Encrypted user ID
            two_factor_code: One-time code sent to user
            
        Returns:
            Response with authentication token
        """
        data = {"two_factor_code": two_factor_code}
        return self._post(f"/api/verify/{encrypted_user}", data=data)
