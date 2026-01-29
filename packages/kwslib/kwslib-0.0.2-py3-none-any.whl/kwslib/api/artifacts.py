"""
Artifacts API
"""

from typing import Optional, Dict, Any
from pathlib import Path
from .base import BaseAPI


class ArtifactsAPI(BaseAPI):
    """Model artifact endpoints"""
    
    def list(
        self,
        model_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List artifacts"""
        params = {"page": page, "page_size": min(page_size, 100)}
        if model_id:
            params["model_id"] = model_id
        return self.client._request("GET", "artifacts/", params=params)
    
    def get(self, artifact_id: int) -> Dict[str, Any]:
        """Get artifact by ID"""
        return self.client._request("GET", f"artifacts/{artifact_id}")
    
    def create(
        self,
        model_id: int,
        artifact_type: str,
        file_path: str,
    ) -> Dict[str, Any]:
        """Upload artifact"""
        with open(file_path, "rb") as f:
            files = {"file": (Path(file_path).name, f, "application/octet-stream")}
            data = {
                "model_id": model_id,
                "artifact_type": artifact_type,
            }
            return self.client._request(
                "POST",
                "artifacts/",
                files=files,
                data=data
            )
    
    def download(self, artifact_id: int, output_path: str) -> str:
        """Download artifact"""
        response = self.client._request(
            "GET",
            f"artifacts/{artifact_id}/download",
            stream=True
        )
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return str(output_path)
    
    def export(self, artifact_id: int) -> Dict[str, Any]:
        """Export artifact (background job)"""
        return self.client._request(
            "POST",
            f"artifacts/{artifact_id}/export"
        )
