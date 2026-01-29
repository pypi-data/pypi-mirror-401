"""
Compare API
"""

from typing import Optional, Dict, Any, List
from .base import BaseAPI


class CompareAPI(BaseAPI):
    """Comparison endpoints"""
    
    def compare_models(
        self,
        model_ids: List[int],
    ) -> Dict[str, Any]:
        """Compare models"""
        return self.client._request(
            "POST",
            "compare/models",
            json={"model_ids": model_ids}
        )
