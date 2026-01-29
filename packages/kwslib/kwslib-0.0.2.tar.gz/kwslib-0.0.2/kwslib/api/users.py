"""
Users API
"""

from typing import Optional, Dict, Any
from .base import BaseAPI


class UsersAPI(BaseAPI):
    """User management endpoints"""
    
    def list(
        self,
        region: Optional[str] = None,
        gender: Optional[str] = None,
        user_type: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """List users"""
        params = {"page": page, "limit": min(limit, 100)}
        if region:
            params["region"] = region
        if gender:
            params["gender"] = gender
        if user_type:
            params["user_type"] = user_type
        if search:
            params["search"] = search
        return self.client._request("GET", "users/", params=params)
    
    def get(self, user_id: int) -> Dict[str, Any]:
        """Get user by ID"""
        return self.client._request("GET", f"users/{user_id}")
    
    def get_statistics(self, user_id: int) -> Dict[str, Any]:
        """Get user statistics"""
        return self.client._request("GET", f"users/{user_id}/statistics")
