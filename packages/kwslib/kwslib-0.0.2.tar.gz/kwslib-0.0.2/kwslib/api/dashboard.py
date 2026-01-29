"""
Dashboard API
"""

from typing import Dict, Any
from .base import BaseAPI


class DashboardAPI(BaseAPI):
    """Dashboard endpoints"""
    
    def get_stats(self) -> Dict[str, Any]:
        """Get dashboard statistics"""
        return self.client._request("GET", "dashboard/")
    
    def get_overview(self) -> Dict[str, Any]:
        """Get dashboard overview"""
        return self.client._request("GET", "dashboard/overview")
    
    def get_active_datasets(self) -> Dict[str, Any]:
        """Get active datasets"""
        return self.client._request("GET", "dashboard/active-datasets")
    
    def get_keyword_sentence_summary(self) -> Dict[str, Any]:
        """Get keyword/sentence summary"""
        return self.client._request("GET", "dashboard/keyword-sentence-summary")
    
    def get_model_overview(self) -> Dict[str, Any]:
        """Get model overview"""
        return self.client._request("GET", "dashboard/model-overview")
    
    def get_recent_collection(self) -> Dict[str, Any]:
        """Get recent collection activity"""
        return self.client._request("GET", "dashboard/recent-collection")
