"""
Tasks API
"""

from typing import Optional, Dict, Any
from .base import BaseAPI


class TasksAPI(BaseAPI):
    """Task management endpoints"""
    
    def list(
        self,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List tasks"""
        params = {"page": page, "page_size": min(page_size, 100)}
        return self.client._request("GET", "tasks/", params=params)
