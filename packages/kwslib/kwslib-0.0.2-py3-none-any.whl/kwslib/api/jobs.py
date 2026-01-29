"""
Jobs API
"""

from typing import Optional, Dict, Any
from .base import BaseAPI


class JobsAPI(BaseAPI):
    """Job status tracking endpoints"""
    
    def get(self, job_id: str) -> Dict[str, Any]:
        """Get job status by ID"""
        return self.client._request("GET", f"jobs/{job_id}")
    
    def list(
        self,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List jobs"""
        params = {"page": page, "page_size": min(page_size, 100)}
        if status:
            params["status"] = status
        return self.client._request("GET", "jobs", params=params)
    
    def cancel(self, job_id: str) -> Dict[str, Any]:
        """Cancel a running job"""
        return self.client._request("POST", f"jobs/{job_id}/cancel")
    
    def wait_for_completion(
        self,
        job_id: str,
        timeout: int = 3600,
        poll_interval: int = 2,
    ) -> Dict[str, Any]:
        """
        Wait for job to complete.
        
        Args:
            job_id: Job ID
            timeout: Maximum time to wait in seconds
            poll_interval: Time between status checks in seconds
            
        Returns:
            Final job status
        """
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get(job_id)
            job_status = status.get("status", "unknown")
            
            if job_status in ["completed", "failed", "cancelled"]:
                return status
            
            time.sleep(poll_interval)
        
        raise TimeoutError(f"Job {job_id} did not complete within {timeout} seconds")
