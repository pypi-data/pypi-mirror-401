"""
Datasets API
"""

from typing import Optional, Dict, Any, List
from .base import BaseAPI


class DatasetsAPI(BaseAPI):
    """Dataset management endpoints"""
    
    def list(
        self,
        type: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """
        List datasets with pagination.
        
        Args:
            type: Filter by dataset type
            page: Page number
            page_size: Items per page (max 100)
        """
        params = {"page": page, "page_size": min(page_size, 100)}
        if type:
            params["type"] = type
        return self.client._request("GET", "datasets", params=params)
    
    def get(self, dataset_id: int) -> Dict[str, Any]:
        """Get dataset by ID"""
        return self.client._request("GET", f"datasets/{dataset_id}")
    
    def create(
        self,
        name: str,
        type: str,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new dataset"""
        data = {"name": name, "type": type}
        if description:
            data["description"] = description
        return self.client._request("POST", "datasets", json=data)
    
    def update(
        self,
        dataset_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update dataset"""
        data = {}
        if name:
            data["name"] = name
        if description is not None:
            data["description"] = description
        return self.client._request("PUT", f"datasets/{dataset_id}", json=data)
    
    def delete(self, dataset_id: int) -> Dict[str, Any]:
        """Delete dataset"""
        return self.client._request("DELETE", f"datasets/{dataset_id}")
    
    def get_detail(self, dataset_id: int) -> Dict[str, Any]:
        """Get dataset with versions"""
        return self.client._request("GET", f"datasets/{dataset_id}/detail")
    
    # Version management
    def list_versions(
        self,
        dataset_id: int,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List versions for a dataset"""
        params = {"page": page, "page_size": min(page_size, 100)}
        return self.client._request(
            "GET",
            f"datasets/{dataset_id}/versions",
            params=params
        )
    
    def get_version(
        self,
        dataset_id: int,
        version: str,
    ) -> Dict[str, Any]:
        """Get specific version"""
        return self.client._request(
            "GET",
            f"datasets/{dataset_id}/versions/{version}"
        )
    
    def create_version(
        self,
        dataset_id: int,
        version: str,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new version"""
        data = {"version": version}
        if description:
            data["description"] = description
        return self.client._request(
            "POST",
            f"datasets/{dataset_id}/versions",
            json=data
        )
    
    def update_version(
        self,
        dataset_id: int,
        version: str,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update version"""
        data = {}
        if description is not None:
            data["description"] = description
        return self.client._request(
            "PUT",
            f"datasets/{dataset_id}/versions/{version}",
            json=data
        )
    
    def activate_version(
        self,
        dataset_id: int,
        version: str,
    ) -> Dict[str, Any]:
        """Activate a version"""
        return self.client._request(
            "POST",
            f"datasets/{dataset_id}/versions/{version}/activate"
        )
    
    def delete_version(
        self,
        dataset_id: int,
        version: str,
    ) -> Dict[str, Any]:
        """Delete version"""
        return self.client._request(
            "DELETE",
            f"datasets/{dataset_id}/versions/{version}"
        )
    
    def get_active_version(self, dataset_id: int) -> Dict[str, Any]:
        """Get active version"""
        return self.client._request(
            "GET",
            f"datasets/{dataset_id}/versions/active"
        )
    
    def suggest_version(self, dataset_id: int) -> Dict[str, Any]:
        """Get suggested version number"""
        return self.client._request(
            "GET",
            f"datasets/{dataset_id}/versions/suggest"
        )
    
    def get_version_statistics(
        self,
        dataset_id: int,
        version_id: int,
    ) -> Dict[str, Any]:
        """Get version statistics"""
        return self.client._request(
            "GET",
            f"datasets/{dataset_id}/versions/{version_id}/statistics"
        )
