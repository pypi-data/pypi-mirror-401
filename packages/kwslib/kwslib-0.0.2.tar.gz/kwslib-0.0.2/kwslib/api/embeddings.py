"""
Embeddings API
"""

from typing import Optional, Dict, Any, List
from .base import BaseAPI


class EmbeddingsAPI(BaseAPI):
    """Embedding management endpoints"""
    
    def list(
        self,
        entity_type: Optional[str] = None,
        model_id: Optional[int] = None,
        feature_type_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List embeddings"""
        params = {"page": page, "page_size": min(page_size, 100)}
        if entity_type:
            params["entity_type"] = entity_type
        if model_id:
            params["model_id"] = model_id
        if feature_type_id:
            params["feature_type_id"] = feature_type_id
        return self.client._request("GET", "embeddings/", params=params)
    
    def get(self, embedding_id: int) -> Dict[str, Any]:
        """Get embedding by ID"""
        return self.client._request("GET", f"embeddings/{embedding_id}")
    
    def compute(
        self,
        entity_type: str,
        entity_ids: List[int],
        model_id: int,
        feature_type_id: int,
    ) -> Dict[str, Any]:
        """Compute embeddings (background job)"""
        return self.client._request(
            "POST",
            "embeddings/compute",
            json={
                "entity_type": entity_type,
                "entity_ids": entity_ids,
                "model_id": model_id,
                "feature_type_id": feature_type_id,
            }
        )
    
    def get_similar(
        self,
        embedding_id: int,
        top_k: int = 10,
    ) -> List[Dict[str, Any]]:
        """Get similar embeddings"""
        params = {"top_k": top_k}
        return self.client._request(
            "GET",
            f"embeddings/{embedding_id}/similar",
            params=params
        )
    
    def project(
        self,
        embedding_id: int,
        method: str = "pca",
        n_components: int = 2,
    ) -> Dict[str, Any]:
        """Project embeddings (background job)"""
        return self.client._request(
            "POST",
            f"embeddings/{embedding_id}/project",
            json={
                "method": method,
                "n_components": n_components,
            }
        )
    
    def get_projections(self, embedding_id: int) -> Dict[str, Any]:
        """Get embedding projections"""
        return self.client._request(
            "GET",
            f"embeddings/{embedding_id}/projections"
        )
