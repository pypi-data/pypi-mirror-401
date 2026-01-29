"""
FewShot API
"""

from typing import Optional, Dict, Any, List
from pathlib import Path
from .base import BaseAPI


class FewShotAPI(BaseAPI):
    """Few-shot learning endpoints"""
    
    # Episodes
    def list_episodes(
        self,
        user_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List few-shot episodes"""
        params = {"page": page, "page_size": min(page_size, 100)}
        if user_id:
            params["user_id"] = user_id
        return self.client._request("GET", "fewshot/episodes", params=params)
    
    def get_episode(self, episode_id: int) -> Dict[str, Any]:
        """Get episode by ID"""
        return self.client._request("GET", f"fewshot/episodes/{episode_id}")
    
    def create_episode(
        self,
        dataset_version_id: int,
        n_way: int,
        k_shot: int,
        q_query: int,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create episode"""
        data = {
            "dataset_version_id": dataset_version_id,
            "n_way": n_way,
            "k_shot": k_shot,
            "q_query": q_query,
        }
        if description:
            data["description"] = description
        return self.client._request("POST", "fewshot/episodes", json=data)
    
    def generate_episode(self, episode_id: int) -> Dict[str, Any]:
        """Generate episode samples (background job)"""
        return self.client._request(
            "POST",
            f"fewshot/episodes/{episode_id}/generate"
        )
    
    def list_episode_samples(self, episode_id: int) -> List[Dict[str, Any]]:
        """List episode samples"""
        return self.client._request("GET", f"fewshot/episodes/{episode_id}/samples")
    
    def get_episode_metrics(self, episode_id: int) -> List[Dict[str, Any]]:
        """Get episode metrics"""
        return self.client._request("GET", f"fewshot/episodes/{episode_id}/metrics")
    
    def predict_episode(
        self,
        episode_id: int,
        file_path: str,
    ) -> Dict[str, Any]:
        """Predict using episode (background job)"""
        with open(file_path, "rb") as f:
            files = {"file": (Path(file_path).name, f, "audio/wav")}
            return self.client._request(
                "POST",
                f"fewshot/episodes/{episode_id}/predict",
                files=files
            )
    
    def get_episode_predictions(self, episode_id: int) -> List[Dict[str, Any]]:
        """Get episode predictions"""
        return self.client._request(
            "GET",
            f"fewshot/episodes/{episode_id}/predictions"
        )
    
    def get_episode_projections(self, episode_id: int) -> List[Dict[str, Any]]:
        """Get episode projections"""
        return self.client._request(
            "GET",
            f"fewshot/episodes/{episode_id}/projections"
        )
    
    # Keywords
    def list_keywords(
        self,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List few-shot keywords"""
        params = {"page": page, "page_size": min(page_size, 100)}
        return self.client._request("GET", "fewshot/keywords", params=params)
    
    def create_keyword(self, name: str) -> Dict[str, Any]:
        """Create few-shot keyword"""
        return self.client._request(
            "POST",
            "fewshot/keywords",
            json={"name": name}
        )
    
    def upload_keyword_audio(
        self,
        keyword_id: int,
        file_path: str,
    ) -> Dict[str, Any]:
        """Upload audio for few-shot keyword"""
        with open(file_path, "rb") as f:
            files = {"file": (Path(file_path).name, f, "audio/wav")}
            return self.client._request(
                "POST",
                f"fewshot/keywords/{keyword_id}/upload",
                files=files
            )
    
    def list_keyword_samples(self, keyword_id: int) -> List[Dict[str, Any]]:
        """List samples for keyword"""
        return self.client._request(
            "GET",
            f"fewshot/keywords/{keyword_id}/samples"
        )
    
    # Audio samples
    def list_audio_samples(
        self,
        keyword_id: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """List few-shot audio samples"""
        params = {}
        if keyword_id:
            params["keyword_id"] = keyword_id
        return self.client._request("GET", "fewshot/audio-samples", params=params)
    
    def get_audio_sample(self, sample_id: int) -> Dict[str, Any]:
        """Get audio sample by ID"""
        return self.client._request("GET", f"fewshot/audio-samples/{sample_id}")
    
    def create_audio_sample(
        self,
        keyword_id: int,
        file_path: str,
    ) -> Dict[str, Any]:
        """Create audio sample"""
        with open(file_path, "rb") as f:
            files = {"file": (Path(file_path).name, f, "audio/wav")}
            data = {"keyword_id": keyword_id}
            return self.client._request(
                "POST",
                "fewshot/audio-samples",
                files=files,
                data=data
            )
    
    def delete_audio_sample(self, sample_id: int) -> None:
        """Delete audio sample"""
        self.client._request("DELETE", f"fewshot/audio-samples/{sample_id}")
