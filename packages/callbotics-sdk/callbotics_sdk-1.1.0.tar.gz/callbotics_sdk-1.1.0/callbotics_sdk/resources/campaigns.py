"""
Campaigns Resource - Campaign management endpoints.
"""

from typing import Any, Dict, List, Optional

from callbotics_sdk.resources.base import BaseResource
from callbotics_sdk.models import PaginatedResponse


class CampaignsResource(BaseResource):
    """Campaign management resource."""

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        organisation_id: Optional[str] = None,
        status: Optional[str] = None,
        direction: Optional[str] = None,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "desc",
    ) -> PaginatedResponse[Dict[str, Any]]:
        """List campaigns with pagination and filtering."""
        params = self._clean_params({
            "current_page": page,
            "per_page": per_page,
            "organisation_id": organisation_id,
            "status": status,
            "direction": direction,
            "search": search,
            "sort_by": sort_by,
            "sort_order": sort_order,
        })
        response = self._client.get(self._build_path("campaigns"), params=params)
        return PaginatedResponse.from_dict(response)

    def get(self, campaign_id: str) -> Dict[str, Any]:
        """Get a specific campaign by ID."""
        response = self._client.get(self._build_path("campaigns", campaign_id))
        return response.get("data", response)

    def create(
        self,
        name: str,
        organisation_id: str,
        agent_id: str,
        direction: str = "outbound",
        concurrency: int = 1,
        telephony_config_id: Optional[str] = None,
        from_number: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a new campaign."""
        data = self._clean_params({
            "name": name,
            "organisation": organisation_id,
            "agent": agent_id,
            "direction": direction,
            "concurrency": concurrency,
            "telephony_config": telephony_config_id,
            "from_number": from_number,
            **kwargs,
        })
        response = self._client.post(self._build_path("campaigns"), json_data=data)
        return response.get("data", response)

    def update(
        self,
        campaign_id: str,
        name: Optional[str] = None,
        concurrency: Optional[int] = None,
        agent_id: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Update a campaign."""
        data = self._clean_params({
            "name": name,
            "concurrency": concurrency,
            "agent": agent_id,
            **kwargs,
        })
        response = self._client.put(self._build_path("campaigns", campaign_id), json_data=data)
        return response.get("data", response)

    def delete(self, campaign_id: str) -> Dict[str, Any]:
        """Delete a campaign (soft delete)."""
        return self._client.delete(self._build_path("campaigns", campaign_id))

    def start(self, campaign_id: str) -> Dict[str, Any]:
        """Start a campaign."""
        return self._client.post(self._build_path("campaigns", "start", campaign_id))

    def pause(self, campaign_id: str) -> Dict[str, Any]:
        """Pause a campaign."""
        return self._client.post(self._build_path("campaigns", "pause", campaign_id))

    def reset(self, campaign_id: str) -> Dict[str, Any]:
        """Reset a campaign."""
        return self._client.post(self._build_path("campaigns", "reset", campaign_id))

    def get_available_concurrency(self, campaign_id: str) -> Dict[str, Any]:
        """Get available concurrency for a campaign."""
        response = self._client.get(
            self._build_path("campaigns", "available_concurrency"),
            params={"campaign_id": campaign_id}
        )
        return response.get("data", response)
