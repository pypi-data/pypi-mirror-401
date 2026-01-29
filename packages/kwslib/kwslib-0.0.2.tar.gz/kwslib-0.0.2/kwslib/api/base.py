"""
Base API class for all API modules
"""

from typing import Optional, Dict, Any, List
from ..client import KWSClient


class BaseAPI:
    """Base class for all API modules"""
    
    def __init__(self, client: KWSClient):
        self.client = client
    
    def _paginate_all(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        max_pages: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch all pages of a paginated endpoint.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            max_pages: Maximum number of pages to fetch (None for all)
            
        Returns:
            List of all items across all pages
        """
        if params is None:
            params = {}
        
        all_items = []
        page = 1
        page_size = 100  # Max page size
        
        while True:
            params["page"] = page
            params["page_size"] = page_size
            
            response = self.client._request("GET", endpoint, params=params)
            
            if isinstance(response, dict) and "items" in response:
                items = response["items"]
                all_items.extend(items)
                
                total_pages = response.get("total_pages", 1)
                if page >= total_pages:
                    break
                    
                if max_pages and page >= max_pages:
                    break
                    
                page += 1
            else:
                # Not a paginated response
                if isinstance(response, list):
                    all_items.extend(response)
                break
        
        return all_items
