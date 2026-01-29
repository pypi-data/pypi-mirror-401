"""
Reward Payout API
"""

from typing import Optional, Dict, Any
from .base import BaseAPI


class RewardPayoutAPI(BaseAPI):
    """Reward and payout endpoints"""
    
    def list_payouts(
        self,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List payouts"""
        params = {"page": page, "page_size": min(page_size, 100)}
        return self.client._request("GET", "reward-payout/admin/payouts", params=params)
