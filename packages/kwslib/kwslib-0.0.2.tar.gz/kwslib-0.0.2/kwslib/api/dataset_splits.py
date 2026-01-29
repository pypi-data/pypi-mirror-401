"""
Dataset Splits API
"""

from typing import Optional, Dict, Any, List, Union
from pathlib import Path
from .base import BaseAPI


class DatasetSplitsAPI(BaseAPI):
    """Dataset split management endpoints"""
    
    def list(
        self,
        dataset_version_id: Optional[int] = None,
        config_name: Optional[str] = None,
        name: Optional[str] = None,
        ratio: Optional[float] = None,
        seed: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List dataset splits"""
        params = {"page": page, "page_size": min(page_size, 100)}
        if dataset_version_id:
            params["dataset_version_id"] = dataset_version_id
        if config_name:
            params["config_name"] = config_name
        if name:
            params["name"] = name
        if ratio is not None:
            params["ratio"] = ratio
        if seed:
            params["seed"] = seed
        return self.client._request("GET", "dataset_splits/", params=params)
    
    def get(self, split_id: int) -> Dict[str, Any]:
        """Get dataset split by ID"""
        return self.client._request("GET", f"dataset_splits/{split_id}")
    
    def create(
        self,
        dataset_version_id: int,
        name: str,
        config_name: str,
        seed: int,
        split_option: str = "ratio",  # "ratio" or "fixed"
        ratio: Optional[float] = None,
        fixed_count: Optional[int] = None,
        keyword_ids: Optional[List[int]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new dataset split.
        
        Args:
            dataset_version_id: Dataset version ID
            name: Split name
            config_name: Config name (e.g., "train", "val", "test")
            seed: Random seed
            split_option: "ratio" or "fixed"
            ratio: Ratio (0 < ratio <= 1.0) for "ratio" option
            fixed_count: Fixed count per keyword for "fixed" option
            keyword_ids: List of keyword IDs to include (optional)
        """
        data = {
            "dataset_version_id": dataset_version_id,
            "name": name,
            "config_name": config_name,
            "seed": seed,
            "split_option": split_option,
        }
        if split_option == "ratio":
            if ratio is None:
                raise ValueError("ratio is required when split_option is 'ratio'")
            data["ratio"] = ratio
        elif split_option == "fixed":
            if fixed_count is None:
                raise ValueError("fixed_count is required when split_option is 'fixed'")
            data["fixed_count"] = fixed_count
            if keyword_ids:
                data["keyword_ids"] = keyword_ids
        
        return self.client._request("POST", "dataset_splits/", json=data)
    
    def update(
        self,
        split_id: int,
        name: Optional[str] = None,
        config_name: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update dataset split"""
        data = {}
        if name:
            data["name"] = name
        if config_name:
            data["config_name"] = config_name
        if seed:
            data["seed"] = seed
        return self.client._request("PUT", f"dataset_splits/{split_id}", json=data)
    
    def delete(self, split_id: int) -> None:
        """Delete dataset split"""
        self.client._request("DELETE", f"dataset_splits/{split_id}")
    
    def download(self, split_id: int, output_path: str) -> str:
        """
        Download dataset split as ZIP file.
        
        Args:
            split_id: Dataset split ID
            output_path: Path to save the ZIP file
            
        Returns:
            Path to downloaded file
        """
        response = self.client._request(
            "GET",
            f"dataset_splits/{split_id}/download",
            stream=True
        )
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return str(output_path)
    
    def list_files(
        self,
        split_id: int,
        file_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        List all files (.wav or .npz) in dataset split.
        
        Args:
            split_id: Dataset split ID
            file_type: Filter by file type ('wav' or 'npz'), None for all
            
        Returns:
            Dictionary with file list and metadata
        """
        params = {}
        if file_type:
            params["file_type"] = file_type
        return self.client._request(
            "GET",
            f"dataset_splits/{split_id}/files",
            params=params
        )
    
    def download_file(
        self,
        split_id: int,
        file_id: int,
        file_type: str,
        output_path: Optional[str] = None,
    ) -> str:
        """
        Download a specific file (.wav or .npz) from dataset split.
        
        Args:
            split_id: Dataset split ID
            file_id: File ID
            file_type: File type ('wav' or 'npz')
            output_path: Optional path to save file (if None, uses presigned URL)
            
        Returns:
            Path to downloaded file or presigned URL
        """
        params = {"file_type": file_type}
        response = self.client._request(
            "GET",
            f"dataset_splits/{split_id}/files/{file_id}/download",
            params=params,
            stream=output_path is not None
        )
        
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return str(output_path)
        else:
            # Return presigned URL (from redirect)
            return response.url if hasattr(response, 'url') else str(response)
    
    def download_all_files(
        self,
        split_id: int,
        file_type: str,
        format: str = "zip",
        output_path: Optional[str] = None,
    ) -> Union[str, Dict[str, Any]]:
        """
        Download all files (.wav or .npz) from dataset split.
        
        Args:
            split_id: Dataset split ID
            file_type: File type ('wav' or 'npz')
            format: Download format ('zip' or 'urls')
            output_path: Path to save ZIP file (required if format='zip')
            
        Returns:
            Path to downloaded ZIP file or dictionary with URLs
        """
        params = {"file_type": file_type, "format": format}
        
        if format == "zip":
            if not output_path:
                raise ValueError("output_path is required when format='zip'")
            
            response = self.client._request(
                "GET",
                f"dataset_splits/{split_id}/files/download-all",
                params=params,
                stream=True
            )
            
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return str(output_path)
        else:
            # Return URLs list
            return self.client._request(
                "GET",
                f"dataset_splits/{split_id}/files/download-all",
                params=params
            )
    
    def generate(self, split_id: int) -> Dict[str, Any]:
        """Generate dataset split (triggers background job)"""
        return self.client._request(
            "POST",
            f"dataset_splits/{split_id}/generate"
        )
