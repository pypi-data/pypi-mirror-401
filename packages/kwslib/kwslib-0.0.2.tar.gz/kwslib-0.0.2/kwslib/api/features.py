"""
Features API
"""

from typing import Optional, Dict, Any, List
from .base import BaseAPI


class FeaturesAPI(BaseAPI):
    """Feature management endpoints"""
    
    # Feature types
    def list_feature_types(
        self,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List feature types"""
        params = {"page": page, "page_size": min(page_size, 100)}
        return self.client._request("GET", "features/feature-types", params=params)
    
    def get_feature_type(self, feature_type_id: int) -> Dict[str, Any]:
        """Get feature type by ID"""
        return self.client._request("GET", f"features/feature-types/{feature_type_id}")
    
    def create_feature_type(
        self,
        name: str,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create feature type"""
        data = {"name": name}
        if description:
            data["description"] = description
        return self.client._request("POST", "features/feature-types", json=data)
    
    def update_feature_type(
        self,
        feature_type_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update feature type"""
        data = {}
        if name:
            data["name"] = name
        if description is not None:
            data["description"] = description
        return self.client._request(
            "PUT",
            f"features/feature-types/{feature_type_id}",
            json=data
        )
    
    def delete_feature_type(self, feature_type_id: int) -> None:
        """Delete feature type"""
        self.client._request("DELETE", f"features/feature-types/{feature_type_id}")
    
    # Features
    def get_keyword_features(self, sample_id: int) -> List[Dict[str, Any]]:
        """Get features for keyword audio sample"""
        return self.client._request("GET", f"features/keyword/{sample_id}")
    
    def get_sentence_frame_features(self, sample_id: int) -> List[Dict[str, Any]]:
        """Get features for sentence frame audio sample"""
        return self.client._request("GET", f"features/sentence-frame/{sample_id}")
    
    def extract_keyword_features(self, sample_id: int) -> Dict[str, Any]:
        """Extract features for keyword audio sample (background job)"""
        return self.client._request(
            "POST",
            f"features/extract/keyword/{sample_id}"
        )
    
    def extract_sentence_frame_features(self, sample_id: int) -> Dict[str, Any]:
        """Extract features for sentence frame audio sample (background job)"""
        return self.client._request(
            "POST",
            f"features/extract/sentence-frame/{sample_id}"
        )
    
    def list_audio_without_features(
        self,
        feature_type_id: int,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List audio samples without features"""
        params = {
            "feature_type_id": feature_type_id,
            "page": page,
            "page_size": min(page_size, 100),
        }
        return self.client._request("GET", "features/audio-without-features", params=params)
