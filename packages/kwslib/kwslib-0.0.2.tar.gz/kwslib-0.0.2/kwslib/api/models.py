"""
Models API
"""

from typing import Optional, Dict, Any
from .base import BaseAPI


class ModelsAPI(BaseAPI):
    """Model management endpoints"""
    
    # Model Init endpoints
    def list_model_inits(
        self,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List model architectures"""
        params = {"page": page, "page_size": min(page_size, 100)}
        return self.client._request("GET", "models/model-init", params=params)
    
    def get_model_init(self, model_init_id: int) -> Dict[str, Any]:
        """Get model architecture by ID"""
        return self.client._request("GET", f"models/model-init/{model_init_id}")
    
    def create_model_init(
        self,
        name: str,
        type: str,
    ) -> Dict[str, Any]:
        """Create model architecture"""
        return self.client._request(
            "POST",
            "models/model-init",
            json={"name": name, "type": type}
        )
    
    def update_model_init(
        self,
        model_init_id: int,
        name: Optional[str] = None,
        type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update model architecture"""
        data = {}
        if name:
            data["name"] = name
        if type:
            data["type"] = type
        return self.client._request(
            "PUT",
            f"models/model-init/{model_init_id}",
            json=data
        )
    
    def delete_model_init(self, model_init_id: int) -> None:
        """Delete model architecture"""
        self.client._request("DELETE", f"models/model-init/{model_init_id}")
    
    # Model endpoints
    def list(
        self,
        model_init_type: Optional[str] = None,
        name: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List models"""
        params = {"page": page, "page_size": min(page_size, 100)}
        if model_init_type:
            params["model_init_type"] = model_init_type
        if name:
            params["name"] = name
        return self.client._request("GET", "models/", params=params)
    
    def get(self, model_id: int) -> Dict[str, Any]:
        """Get model by ID"""
        return self.client._request("GET", f"models/{model_id}")
    
    def create(
        self,
        name: str,
        model_init_id: int,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new model"""
        data = {"name": name, "model_init_id": model_init_id}
        if description:
            data["description"] = description
        return self.client._request("POST", "models/", json=data)
    
    def update(
        self,
        model_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update model"""
        data = {}
        if name:
            data["name"] = name
        if description is not None:
            data["description"] = description
        return self.client._request("PUT", f"models/{model_id}", json=data)
    
    def delete(self, model_id: int) -> None:
        """Delete model"""
        self.client._request("DELETE", f"models/{model_id}")
