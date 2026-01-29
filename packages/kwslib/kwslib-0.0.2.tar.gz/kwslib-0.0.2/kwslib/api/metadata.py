"""
Metadata API
"""

from typing import Optional, Dict, Any
from .base import BaseAPI


class MetadataAPI(BaseAPI):
    """Metadata endpoints"""
    
    def get(
        self,
        entity_type: str,
        entity_id: int,
    ) -> Dict[str, Any]:
        """Get metadata"""
        params = {"entity_type": entity_type, "entity_id": entity_id}
        return self.client._request("GET", "metadata/", params=params)
