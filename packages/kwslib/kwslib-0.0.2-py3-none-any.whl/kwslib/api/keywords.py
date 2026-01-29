"""
Keywords API
"""

from typing import Optional, Dict, Any, List
from .base import BaseAPI


class KeywordsAPI(BaseAPI):
    """Keyword management endpoints"""
    
    def list(
        self,
        dataset_version_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "name",
        sort_order: str = "asc",
    ) -> Dict[str, Any]:
        """List keywords"""
        params = {
            "page": page,
            "page_size": min(page_size, 100),
            "sort_by": sort_by,
            "sort_order": sort_order,
        }
        if dataset_version_id:
            params["dataset_version_id"] = dataset_version_id
        return self.client._request("GET", "keywords", params=params)
    
    def get(self, keyword_id: int) -> Dict[str, Any]:
        """Get keyword by ID"""
        return self.client._request("GET", f"keywords/{keyword_id}")
    
    def create(
        self,
        dataset_version_id: int,
        name: str,
    ) -> Dict[str, Any]:
        """Create a new keyword"""
        return self.client._request(
            "POST",
            "keywords",
            json={"dataset_version_id": dataset_version_id, "name": name}
        )
    
    def create_batch(
        self,
        dataset_version_id: int,
        names: List[str],
    ) -> Dict[str, Any]:
        """Create multiple keywords"""
        return self.client._request(
            "POST",
            "keywords/batch",
            json={"dataset_version_id": dataset_version_id, "names": names}
        )
    
    def update(
        self,
        keyword_id: int,
        name: str,
    ) -> Dict[str, Any]:
        """Update keyword"""
        return self.client._request(
            "PUT",
            f"keywords/{keyword_id}",
            json={"name": name}
        )
    
    def delete(self, keyword_id: int) -> None:
        """Delete keyword"""
        self.client._request("DELETE", f"keywords/{keyword_id}")
    
    def list_audio_samples(
        self,
        keyword_id: int,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List audio samples for a keyword"""
        params = {"page": page, "page_size": min(page_size, 100)}
        return self.client._request(
            "GET",
            f"keywords/{keyword_id}/audio-samples",
            params=params
        )
