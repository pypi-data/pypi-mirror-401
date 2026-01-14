"""
Calls Resource - Call management endpoints.
"""

from typing import Any, Dict, List, Optional

from callbotics_sdk.resources.base import BaseResource
from callbotics_sdk.models import PaginatedResponse


class CallsResource(BaseResource):
    """Call management resource."""

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        campaign_id: Optional[str] = None,
        contact_list_id: Optional[str] = None,
        status: Optional[str] = None,
        org_id: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "desc",
    ) -> PaginatedResponse[Dict[str, Any]]:
        """List calls with pagination and filtering."""
        params = self._clean_params({
            "current_page": page,
            "per_page": per_page,
            "campaign_id": campaign_id,
            "contact_list_id": contact_list_id,
            "status": status,
            "org_id": org_id,
            "sort_by": sort_by,
            "sort_order": sort_order,
        })
        response = self._client.get(self._build_path("calls"), params=params)
        return PaginatedResponse.from_dict(response)

    def create(
        self,
        campaign_id: str,
        to_number: str,
        from_number: Optional[str] = None,
        contact_data: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create/queue a new call."""
        data = self._clean_params({
            "campaign_id": campaign_id,
            "to_number": to_number,
            "from_number": from_number,
            "contact_data": contact_data,
            **kwargs,
        })
        response = self._client.post(self._build_path("calls", "create-call"), json_data=data)
        return response.get("data", response)

    def delete(self, call_id: str) -> Dict[str, Any]:
        """Delete a call (soft delete)."""
        return self._client.delete(self._build_path("calls", call_id))

    def get_minutes_summary(
        self,
        org_id: Optional[str] = None,
        period: str = "daily",
    ) -> Dict[str, Any]:
        """Get call minutes summary."""
        params = self._clean_params({
            "org_id": org_id,
            "period": period,
        })
        response = self._client.get(
            self._build_path("calls", "call-minutes-summary"),
            params=params
        )
        return response.get("data", response)
