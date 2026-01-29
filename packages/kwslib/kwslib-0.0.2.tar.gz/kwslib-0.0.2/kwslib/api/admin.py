"""
Admin API
"""

from typing import Optional, Dict, Any, List
from .base import BaseAPI


class AdminAPI(BaseAPI):
    """Admin management endpoints"""
    
    def list_users(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """List users (admin only)"""
        params = {"page": page, "page_size": min(page_size, 100)}
        if search:
            params["search"] = search
        return self.client._request("GET", "admin/users", params=params)
    
    def list_payouts(
        self,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List payouts (admin only)"""
        params = {"page": page, "page_size": min(page_size, 100)}
        return self.client._request("GET", "admin/payouts", params=params)
