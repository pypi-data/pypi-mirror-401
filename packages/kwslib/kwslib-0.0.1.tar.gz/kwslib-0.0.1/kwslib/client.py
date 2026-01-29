"""
Base KWS API Client

Handles authentication, HTTP requests, and provides base functionality
for all API endpoint wrappers.
"""

import requests
from typing import Optional, Dict, Any, List
from urllib.parse import urljoin
import logging

logger = logging.getLogger(__name__)


class KWSClient:
    """
    Main client for interacting with KWS Platform API.
    
    Example:
        >>> client = KWSClient(base_url="http://localhost:8000")
        >>> client.login(username="admin", password="password")
        >>> datasets = client.datasets.list()
    """
    
    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        token: Optional[str] = None,
        timeout: int = 30,
    ):
        """
        Initialize KWS API client.
        
        Args:
            base_url: Base URL of the KWS API server
            token: Optional authentication token (can be set later via login)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.api_url = urljoin(self.base_url, "/api/v1/")
        self.token = token
        self.timeout = timeout
        self.session = requests.Session()
        
        # Initialize API modules
        from .api import (
            AuthAPI, DatasetsAPI, ModelsAPI, ExperimentsAPI,
            KeywordsAPI, SentencesAPI, AudioAPI, FeaturesAPI,
            DatasetSplitsAPI, JobsAPI, EmbeddingsAPI, FewShotAPI,
            PredictAPI, DashboardAPI, TasksAPI, CollectionAPI,
            RecordingsAPI, MetricsAPI, VisualizeAPI, CompareAPI,
            DevicesAPI, ArtifactsAPI, DeployedModelsAPI,
            QualityControlAPI, RewardPayoutAPI, ConfigAPI,
            MetadataAPI, NotificationsAPI, AdminAPI, UsersAPI
        )
        
        self.auth = AuthAPI(self)
        self.datasets = DatasetsAPI(self)
        self.models = ModelsAPI(self)
        self.experiments = ExperimentsAPI(self)
        self.keywords = KeywordsAPI(self)
        self.sentences = SentencesAPI(self)
        self.audio = AudioAPI(self)
        self.features = FeaturesAPI(self)
        self.dataset_splits = DatasetSplitsAPI(self)
        self.jobs = JobsAPI(self)
        self.embeddings = EmbeddingsAPI(self)
        self.fewshot = FewShotAPI(self)
        self.predict = PredictAPI(self)
        self.dashboard = DashboardAPI(self)
        self.tasks = TasksAPI(self)
        self.collection = CollectionAPI(self)
        self.recordings = RecordingsAPI(self)
        self.metrics = MetricsAPI(self)
        self.visualize = VisualizeAPI(self)
        self.compare = CompareAPI(self)
        self.devices = DevicesAPI(self)
        self.artifacts = ArtifactsAPI(self)
        self.deployed_models = DeployedModelsAPI(self)
        self.quality_control = QualityControlAPI(self)
        self.reward_payout = RewardPayoutAPI(self)
        self.config = ConfigAPI(self)
        self.metadata = MetadataAPI(self)
        self.notifications = NotificationsAPI(self)
        self.admin = AdminAPI(self)
        self.users = UsersAPI(self)
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Login and get authentication token.
        
        Args:
            username: Admin username
            password: Admin password
            
        Returns:
            Token response with access_token, admin_id, role
            
        Raises:
            requests.HTTPError: If login fails
        """
        response = self._request(
            "POST",
            "auth/admin/login",
            json={"username": username, "password": password},
            require_auth=False
        )
        self.token = response["access_token"]
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        return response
    
    def logout(self) -> Dict[str, Any]:
        """
        Logout and clear authentication token.
        
        Returns:
            Message response
        """
        response = self._request("POST", "auth/admin/logout")
        self.token = None
        self.session.headers.pop("Authorization", None)
        return response
    
    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh authentication token.
        
        Args:
            refresh_token: Refresh token
            
        Returns:
            New token response
        """
        response = self._request(
            "POST",
            "auth/admin/refresh",
            json={"refresh_token": refresh_token},
            require_auth=False
        )
        self.token = response["access_token"]
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        return response
    
    def get_me(self) -> Dict[str, Any]:
        """
        Get current admin information.
        
        Returns:
            Admin profile information
        """
        return self._request("GET", "auth/admin/me")
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json: Optional[Dict] = None,
        data: Optional[Any] = None,
        files: Optional[Dict] = None,
        require_auth: bool = True,
        stream: bool = False,
    ) -> Any:
        """
        Make HTTP request to API endpoint.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint path (relative to /api/v1/)
            params: Query parameters
            json: JSON body
            data: Form data
            files: Files to upload
            require_auth: Whether authentication is required
            stream: Whether to stream the response
            
        Returns:
            Response data (parsed JSON or raw response for streaming)
            
        Raises:
            requests.HTTPError: If request fails
        """
        url = urljoin(self.api_url, endpoint.lstrip("/"))
        
        headers = {}
        if require_auth and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                data=data,
                files=files,
                headers=headers,
                timeout=self.timeout,
                stream=stream,
            )
            response.raise_for_status()
            
            if stream:
                return response
            
            # Handle empty responses
            if response.status_code == 204:
                return {}
            
            # Try to parse JSON
            try:
                return response.json()
            except ValueError:
                return response.text
                
        except requests.HTTPError as e:
            error_msg = f"API request failed: {method} {url}"
            if e.response is not None:
                try:
                    error_detail = e.response.json()
                    error_msg += f" - {error_detail}"
                except:
                    error_msg += f" - {e.response.text}"
            logger.error(error_msg)
            raise
        except requests.RequestException as e:
            logger.error(f"Request exception: {e}")
            raise
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check API health status.
        
        Returns:
            Health status response
        """
        return self._request("GET", "health", require_auth=False)
    
    def health_db(self) -> Dict[str, Any]:
        """Check database health"""
        return self._request("GET", "health/db")
    
    def health_minio(self) -> Dict[str, Any]:
        """Check MinIO health"""
        return self._request("GET", "health/minio")
    
    def health_redis(self) -> Dict[str, Any]:
        """Check Redis health"""
        return self._request("GET", "health/redis")
    
    def health_status(self) -> Dict[str, Any]:
        """Get system status"""
        return self._request("GET", "health/status")
