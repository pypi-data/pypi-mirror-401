"""
Authentication API
"""

from typing import Dict, Any
from .base import BaseAPI


class AuthAPI(BaseAPI):
    """Authentication endpoints"""
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login and get authentication token"""
        return self.client.login(username, password)
    
    def logout(self) -> Dict[str, Any]:
        """Logout and clear authentication token"""
        return self.client.logout()
    
    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh authentication token"""
        return self.client.refresh_token(refresh_token)
    
    def get_me(self) -> Dict[str, Any]:
        """Get current admin information"""
        return self.client.get_me()
