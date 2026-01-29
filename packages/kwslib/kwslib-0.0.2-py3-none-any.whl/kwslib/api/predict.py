"""
Predict API
"""

from typing import Optional, Dict, Any, List
from pathlib import Path
from .base import BaseAPI


class PredictAPI(BaseAPI):
    """Prediction/inference endpoints"""
    
    def predict_upload(
        self,
        model_id: int,
        feature_type_id: int,
        file_path: str,
    ) -> Dict[str, Any]:
        """Predict from uploaded audio file"""
        with open(file_path, "rb") as f:
            files = {"file": (Path(file_path).name, f, "audio/wav")}
            data = {
                "model_id": model_id,
                "feature_type_id": feature_type_id,
            }
            return self.client._request(
                "POST",
                "predict/upload",
                files=files,
                data=data
            )
    
    def predict_batch(
        self,
        model_id: int,
        feature_type_id: int,
        file_paths: List[str],
    ) -> Dict[str, Any]:
        """Batch prediction (returns job ID)"""
        files = []
        for file_path in file_paths:
            files.append(("files", (Path(file_path).name, open(file_path, "rb"), "audio/wav")))
        
        try:
            data = {
                "model_id": model_id,
                "feature_type_id": feature_type_id,
            }
            return self.client._request(
                "POST",
                "predict/upload/batch",
                files=files,
                data=data
            )
        finally:
            for _, (_, file_obj, _) in files:
                file_obj.close()
    
    def get_batch_prediction(self, job_id: str) -> Dict[str, Any]:
        """Get batch prediction results"""
        return self.client._request("GET", f"predict/upload/{job_id}")
    
    def fewshot_predict_upload(
        self,
        episode_id: int,
        file_path: str,
    ) -> Dict[str, Any]:
        """Few-shot prediction from uploaded file"""
        with open(file_path, "rb") as f:
            files = {"file": (Path(file_path).name, f, "audio/wav")}
            data = {"episode_id": episode_id}
            return self.client._request(
                "POST",
                "predict/few-shot/upload",
                files=files,
                data=data
            )
    
    def fewshot_predict_episode(
        self,
        episode_id: int,
        file_path: str,
    ) -> Dict[str, Any]:
        """Few-shot prediction using episode"""
        with open(file_path, "rb") as f:
            files = {"file": (Path(file_path).name, f, "audio/wav")}
            return self.client._request(
                "POST",
                f"predict/few-shot/episode/{episode_id}",
                files=files
            )
