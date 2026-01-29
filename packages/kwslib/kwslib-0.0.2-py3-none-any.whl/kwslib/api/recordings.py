"""
Recordings API
"""

from typing import Optional, Dict, Any
from .base import BaseAPI


class RecordingsAPI(BaseAPI):
    """Recording endpoints"""
    
    def list(
        self,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List recordings"""
        params = {"page": page, "page_size": min(page_size, 100)}
        return self.client._request("GET", "recordings/", params=params)
