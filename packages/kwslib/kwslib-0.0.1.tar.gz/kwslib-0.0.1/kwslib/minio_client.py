"""
Dataset Split Files Client for downloading .wav and .npz files for training
Uses KWS API instead of direct MinIO connection
"""

from typing import Optional, List, Dict, Any
from pathlib import Path
import numpy as np
import requests
import logging
import io

logger = logging.getLogger(__name__)


class DatasetSplitFilesClient:
    """
    Client for downloading audio and feature files from dataset splits via API.
    This replaces direct MinIO connection - all file access goes through KWS API.
    
    Example:
        >>> from kwslib import KWSClient, DatasetSplitFilesClient
        >>> 
        >>> # Initialize API client
        >>> api = KWSClient(base_url="http://localhost:8000")
        >>> api.login(username="admin", password="password")
        >>> 
        >>> # Initialize files client (uses API client)
        >>> files_client = DatasetSplitFilesClient(api)
        >>> 
        >>> # List files in split
        >>> files = files_client.list_files(split_id=1, file_type="npz")
        >>> 
        >>> # Download all .npz files
        >>> files_client.download_all_npz(split_id=1, output_dir="features")
    """
    
    def __init__(self, api_client):
        """
        Initialize dataset split files client.
        
        Args:
            api_client: KWSClient instance (must be authenticated)
        """
        self.api = api_client
    
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
        return self.api.dataset_splits.list_files(split_id, file_type)
    
    def download_wav(
        self,
        split_id: int,
        file_id: int,
        output_path: str,
    ) -> str:
        """
        Download a .wav file from dataset split.
        
        Args:
            split_id: Dataset split ID
            file_id: File ID
            output_path: Local path to save the file
            
        Returns:
            Path to downloaded file
        """
        return self.api.dataset_splits.download_file(
            split_id=split_id,
            file_id=file_id,
            file_type="wav",
            output_path=output_path
        )
    
    def download_npz(
        self,
        split_id: int,
        file_id: int,
        output_path: Optional[str] = None,
    ) -> dict:
        """
        Download a .npz file from dataset split and load as numpy dict.
        
        Args:
            split_id: Dataset split ID
            file_id: File ID
            output_path: Optional local path to save the file
            
        Returns:
            Dictionary of numpy arrays loaded from .npz file
        """
        if output_path:
            file_path = self.api.dataset_splits.download_file(
                split_id=split_id,
                file_id=file_id,
                file_type="npz",
                output_path=output_path
            )
            data = np.load(file_path)
        else:
            # Download to temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.npz') as tmp:
                file_path = self.api.dataset_splits.download_file(
                    split_id=split_id,
                    file_id=file_id,
                    file_type="npz",
                    output_path=tmp.name
                )
                data = np.load(file_path)
                import os
                os.unlink(file_path)  # Clean up temp file
        
        # Convert to dict
        result = {key: data[key] for key in data.keys()}
        logger.info(f"Downloaded and loaded npz file {file_id}")
        return result
    
    def download_all_wav(
        self,
        split_id: int,
        output_dir: str,
    ) -> List[str]:
        """
        Download all .wav files for a dataset split.
        
        Args:
            split_id: Dataset split ID
            output_dir: Directory to save audio files
            
        Returns:
            List of paths to downloaded files
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Get file list
        files_info = self.list_files(split_id, file_type="wav")
        wav_files = [f for f in files_info["files"] if f["file_type"] == "wav"]
        
        downloaded_files = []
        for file_info in wav_files:
            output_path = output_dir / file_info["file_name"]
            try:
                # Download using presigned URL
                response = requests.get(file_info["presigned_url"], timeout=300)
                response.raise_for_status()
                with open(output_path, "wb") as f:
                    f.write(response.content)
                downloaded_files.append(str(output_path))
            except Exception as e:
                logger.error(f"Error downloading {file_info['file_name']}: {e}")
                continue
        
        logger.info(f"Downloaded {len(downloaded_files)} wav files for split {split_id}")
        return downloaded_files
    
    def download_all_npz(
        self,
        split_id: int,
        output_dir: str,
    ) -> List[str]:
        """
        Download all .npz files for a dataset split.
        
        Args:
            split_id: Dataset split ID
            output_dir: Directory to save feature files
            
        Returns:
            List of paths to downloaded files
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Get file list
        files_info = self.list_files(split_id, file_type="npz")
        npz_files = [f for f in files_info["files"] if f["file_type"] == "npz"]
        
        downloaded_files = []
        for file_info in npz_files:
            output_path = output_dir / file_info["file_name"]
            try:
                # Download using presigned URL
                response = requests.get(file_info["presigned_url"], timeout=300)
                response.raise_for_status()
                with open(output_path, "wb") as f:
                    f.write(response.content)
                downloaded_files.append(str(output_path))
            except Exception as e:
                logger.error(f"Error downloading {file_info['file_name']}: {e}")
                continue
        
        logger.info(f"Downloaded {len(downloaded_files)} npz files for split {split_id}")
        return downloaded_files
    
    def download_all_files_zip(
        self,
        split_id: int,
        file_type: str,
        output_path: str,
    ) -> str:
        """
        Download all files as ZIP from dataset split.
        
        Args:
            split_id: Dataset split ID
            file_type: File type ('wav' or 'npz')
            output_path: Path to save ZIP file
            
        Returns:
            Path to downloaded ZIP file
        """
        return self.api.dataset_splits.download_all_files(
            split_id=split_id,
            file_type=file_type,
            format="zip",
            output_path=output_path
        )
    
    def get_file_urls(
        self,
        split_id: int,
        file_type: str,
    ) -> Dict[str, Any]:
        """
        Get presigned URLs for all files in dataset split.
        
        Args:
            split_id: Dataset split ID
            file_type: File type ('wav' or 'npz')
            
        Returns:
            Dictionary with list of file URLs
        """
        return self.api.dataset_splits.download_all_files(
            split_id=split_id,
            file_type=file_type,
            format="urls"
        )
