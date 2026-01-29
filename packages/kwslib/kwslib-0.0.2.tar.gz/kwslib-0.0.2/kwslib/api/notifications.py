"""
Notifications API
"""

from typing import Dict, Any
from .base import BaseAPI


class NotificationsAPI(BaseAPI):
    """Notification endpoints"""
    
    def upload_complete(
        self,
        upload_id: str,
        status: str,
    ) -> Dict[str, Any]:
        """Notify upload completion"""
        return self.client._request(
            "POST",
            "notifications/upload-complete",
            json={"upload_id": upload_id, "status": status}
        )
