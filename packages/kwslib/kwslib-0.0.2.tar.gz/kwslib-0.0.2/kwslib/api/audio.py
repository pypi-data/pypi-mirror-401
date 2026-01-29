"""
Audio API
"""

from typing import Optional, Dict, Any, BinaryIO
from pathlib import Path
from .base import BaseAPI


class AudioAPI(BaseAPI):
    """Audio sample management endpoints"""
    
    # Keyword audio samples
    def list_keyword_samples(
        self,
        keyword_id: Optional[int] = None,
        dataset_version_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List keyword audio samples"""
        params = {"page": page, "page_size": min(page_size, 100)}
        if keyword_id:
            params["keyword_id"] = keyword_id
        if dataset_version_id:
            params["dataset_version_id"] = dataset_version_id
        return self.client._request("GET", "audio/keywords", params=params)
    
    def get_keyword_sample(self, sample_id: int) -> Dict[str, Any]:
        """Get keyword audio sample by ID"""
        return self.client._request("GET", f"audio/keywords/{sample_id}")
    
    def get_keyword_sample_url(
        self,
        sample_id: int,
        expires_in: int = 3600,
    ) -> Dict[str, Any]:
        """Get presigned URL for keyword audio sample"""
        params = {"expires_in": expires_in}
        return self.client._request(
            "GET",
            f"audio/keywords/{sample_id}/presigned-url",
            params=params
        )
    
    def create_keyword_sample(
        self,
        keyword_id: int,
        file_path: str,
        duration: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Upload keyword audio sample"""
        with open(file_path, "rb") as f:
            files = {"file": (Path(file_path).name, f, "audio/wav")}
            data = {"keyword_id": keyword_id}
            if duration:
                data["duration"] = duration
            return self.client._request(
                "POST",
                "audio/keywords",
                files=files,
                data=data
            )
    
    def update_keyword_sample(
        self,
        sample_id: int,
        duration: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Update keyword audio sample"""
        data = {}
        if duration:
            data["duration"] = duration
        return self.client._request(
            "PUT",
            f"audio/keywords/{sample_id}",
            json=data
        )
    
    def delete_keyword_sample(self, sample_id: int) -> None:
        """Delete keyword audio sample"""
        self.client._request("DELETE", f"audio/keywords/{sample_id}")
    
    # Sentence audio samples
    def list_sentence_samples(
        self,
        sentence_id: Optional[int] = None,
        dataset_version_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List sentence audio samples"""
        params = {"page": page, "page_size": min(page_size, 100)}
        if sentence_id:
            params["sentence_id"] = sentence_id
        if dataset_version_id:
            params["dataset_version_id"] = dataset_version_id
        return self.client._request("GET", "audio/sentences", params=params)
    
    def get_sentence_sample(self, sample_id: int) -> Dict[str, Any]:
        """Get sentence audio sample by ID"""
        return self.client._request("GET", f"audio/sentences/{sample_id}")
    
    def create_sentence_sample(
        self,
        sentence_id: int,
        file_path: str,
        duration: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Upload sentence audio sample"""
        with open(file_path, "rb") as f:
            files = {"file": (Path(file_path).name, f, "audio/wav")}
            data = {"sentence_id": sentence_id}
            if duration:
                data["duration"] = duration
            return self.client._request(
                "POST",
                "audio/sentences",
                files=files,
                data=data
            )
    
    def update_sentence_sample(
        self,
        sample_id: int,
        duration: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Update sentence audio sample"""
        data = {}
        if duration:
            data["duration"] = duration
        return self.client._request(
            "PUT",
            f"audio/sentences/{sample_id}",
            json=data
        )
    
    def delete_sentence_sample(self, sample_id: int) -> None:
        """Delete sentence audio sample"""
        self.client._request("DELETE", f"audio/sentences/{sample_id}")
    
    # Sentence frame audio samples
    def list_sentence_frame_samples(
        self,
        sentence_frame_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List sentence frame audio samples"""
        params = {"page": page, "page_size": min(page_size, 100)}
        if sentence_frame_id:
            params["sentence_frame_id"] = sentence_frame_id
        return self.client._request("GET", "audio/sentence-frames", params=params)
    
    def get_sentence_frame_sample(self, sample_id: int) -> Dict[str, Any]:
        """Get sentence frame audio sample by ID"""
        return self.client._request("GET", f"audio/sentence-frames/{sample_id}")
    
    def create_sentence_frame_sample(
        self,
        sentence_frame_id: int,
        file_path: str,
        duration: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Upload sentence frame audio sample"""
        with open(file_path, "rb") as f:
            files = {"file": (Path(file_path).name, f, "audio/wav")}
            data = {"sentence_frame_id": sentence_frame_id}
            if duration:
                data["duration"] = duration
            return self.client._request(
                "POST",
                "audio/sentence-frames",
                files=files,
                data=data
            )
    
    def delete_sentence_frame_sample(self, sample_id: int) -> None:
        """Delete sentence frame audio sample"""
        self.client._request("DELETE", f"audio/sentence-frames/{sample_id}")
    
    # Import/Upload
    def import_audio(
        self,
        dataset_version_id: int,
        zip_file_path: str,
    ) -> Dict[str, Any]:
        """Import audio files from ZIP"""
        with open(zip_file_path, "rb") as f:
            files = {"file": (Path(zip_file_path).name, f, "application/zip")}
            data = {"dataset_version_id": dataset_version_id}
            return self.client._request(
                "POST",
                "audio/import",
                files=files,
                data=data
            )
    
    def upload_audio(
        self,
        dataset_version_id: int,
        file_path: str,
        keyword_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Upload single audio file"""
        with open(file_path, "rb") as f:
            files = {"file": (Path(file_path).name, f, "audio/wav")}
            data = {"dataset_version_id": dataset_version_id}
            if keyword_name:
                data["keyword_name"] = keyword_name
            return self.client._request(
                "POST",
                "audio/upload",
                files=files,
                data=data
            )
