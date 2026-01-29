"""
Experiments API
"""

from typing import Optional, Dict, Any
from .base import BaseAPI


class ExperimentsAPI(BaseAPI):
    """Experiment management endpoints"""
    
    def list(
        self,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List experiments"""
        params = {"page": page, "page_size": min(page_size, 100)}
        return self.client._request("GET", "experiments/", params=params)
    
    def get(self, experiment_id: int) -> Dict[str, Any]:
        """Get experiment by ID"""
        return self.client._request("GET", f"experiments/{experiment_id}")
    
    def create(
        self,
        name: str,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new experiment"""
        data = {"name": name}
        if description:
            data["description"] = description
        return self.client._request("POST", "experiments/", json=data)
    
    def update(
        self,
        experiment_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update experiment"""
        data = {}
        if name:
            data["name"] = name
        if description is not None:
            data["description"] = description
        return self.client._request(
            "PUT",
            f"experiments/{experiment_id}",
            json=data
        )
    
    def delete(self, experiment_id: int) -> None:
        """Delete experiment"""
        self.client._request("DELETE", f"experiments/{experiment_id}")
    
    # Experiment Runs
    def list_runs(
        self,
        experiment_id: int,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List experiment runs"""
        params = {"page": page, "page_size": min(page_size, 100)}
        return self.client._request(
            "GET",
            f"experiments/{experiment_id}/runs",
            params=params
        )
    
    def get_run(
        self,
        experiment_id: int,
        run_id: int,
    ) -> Dict[str, Any]:
        """Get experiment run by ID"""
        return self.client._request(
            "GET",
            f"experiments/{experiment_id}/runs/{run_id}"
        )
    
    def create_run(
        self,
        experiment_id: int,
        name: str,
        model_id: int,
        dataset_split_id: int,
        description: Optional[str] = None,
        hyperparameters: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Create a new experiment run"""
        data = {
            "name": name,
            "model_id": model_id,
            "dataset_split_id": dataset_split_id,
        }
        if description:
            data["description"] = description
        if hyperparameters:
            data["hyperparameters"] = hyperparameters
        return self.client._request(
            "POST",
            f"experiments/{experiment_id}/runs",
            json=data
        )
    
    def update_run(
        self,
        experiment_id: int,
        run_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        hyperparameters: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Update experiment run"""
        data = {}
        if name:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if hyperparameters is not None:
            data["hyperparameters"] = hyperparameters
        return self.client._request(
            "PUT",
            f"experiments/{experiment_id}/runs/{run_id}",
            json=data
        )
    
    def delete_run(
        self,
        experiment_id: int,
        run_id: int,
    ) -> None:
        """Delete experiment run"""
        self.client._request(
            "DELETE",
            f"experiments/{experiment_id}/runs/{run_id}"
        )
