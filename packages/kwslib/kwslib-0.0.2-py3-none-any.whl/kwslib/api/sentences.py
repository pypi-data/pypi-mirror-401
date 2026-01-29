"""
Sentences API
"""

from typing import Optional, Dict, Any, List
from .base import BaseAPI


class SentencesAPI(BaseAPI):
    """Sentence management endpoints"""
    
    def list(
        self,
        dataset_version_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List sentences"""
        params = {"page": page, "page_size": min(page_size, 100)}
        if dataset_version_id:
            params["dataset_version_id"] = dataset_version_id
        return self.client._request("GET", "sentences/", params=params)
    
    def get(self, sentence_id: int) -> Dict[str, Any]:
        """Get sentence by ID"""
        return self.client._request("GET", f"sentences/{sentence_id}")
    
    def create(
        self,
        dataset_version_id: int,
        text: str,
    ) -> Dict[str, Any]:
        """Create a new sentence"""
        return self.client._request(
            "POST",
            "sentences/",
            json={"dataset_version_id": dataset_version_id, "text": text}
        )
    
    def create_batch(
        self,
        dataset_version_id: int,
        texts: List[str],
    ) -> Dict[str, Any]:
        """Create multiple sentences"""
        return self.client._request(
            "POST",
            "sentences/batch",
            json={"dataset_version_id": dataset_version_id, "texts": texts}
        )
    
    def update(
        self,
        sentence_id: int,
        text: str,
    ) -> Dict[str, Any]:
        """Update sentence"""
        return self.client._request(
            "PUT",
            f"sentences/{sentence_id}",
            json={"text": text}
        )
    
    def delete(self, sentence_id: int) -> None:
        """Delete sentence"""
        self.client._request("DELETE", f"sentences/{sentence_id}")
    
    def list_frames(self, sentence_id: int) -> List[Dict[str, Any]]:
        """List sentence frames"""
        return self.client._request("GET", f"sentences/{sentence_id}/frames")
