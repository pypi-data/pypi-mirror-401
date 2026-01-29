"""
Visualize API
"""

from typing import Optional, Dict, Any
from .base import BaseAPI


class VisualizeAPI(BaseAPI):
    """Visualization endpoints"""
    
    def get_data(
        self,
        dataset_version_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get visualization data"""
        params = {}
        if dataset_version_id:
            params["dataset_version_id"] = dataset_version_id
        return self.client._request("GET", "visualize/", params=params)
