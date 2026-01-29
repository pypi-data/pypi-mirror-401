"""
Config API
"""

from typing import Dict, Any
from .base import BaseAPI


class ConfigAPI(BaseAPI):
    """Configuration endpoints"""
    
    def get(self) -> Dict[str, Any]:
        """Get configuration"""
        return self.client._request("GET", "config/")
