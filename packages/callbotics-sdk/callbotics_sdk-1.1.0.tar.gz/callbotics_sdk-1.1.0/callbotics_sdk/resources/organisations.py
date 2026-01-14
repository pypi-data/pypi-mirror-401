"""
Organisations Resource - Organisation management endpoints.
"""

from typing import Any, Dict, List, Optional

from callbotics_sdk.resources.base import BaseResource
from callbotics_sdk.models import PaginatedResponse


class OrganisationsResource(BaseResource):
    """Organisation management resource."""

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "desc",
    ) -> PaginatedResponse[Dict[str, Any]]:
        """List organisations with pagination and filtering."""
        params = self._clean_params({
            "current_page": page,
            "per_page": per_page,
            "search": search,
            "is_active": is_active,
            "sort_by": sort_by,
            "sort_order": sort_order,
        })
        response = self._client.get(self._build_path("organisations"), params=params)
        return PaginatedResponse.from_dict(response)

    def get(self, org_id: str) -> Dict[str, Any]:
        """Get a specific organisation by ID."""
        response = self._client.get(self._build_path("organisations", org_id))
        return response.get("data", response)

    def get_details(self, org_id: str) -> Dict[str, Any]:
        """Get organisation details."""
        response = self._client.get(
            self._build_path("organisations", "org-details"),
            params={"org_id": org_id}
        )
        return response.get("data", response)

    def create(
        self,
        name: str,
        minutes_available: int = 0,
        concurrency: int = 1,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a new organisation."""
        data = self._clean_params({
            "name": name,
            "minutes_available": minutes_available,
            "concurrency": concurrency,
            **kwargs,
        })
        response = self._client.post(self._build_path("organisations"), json_data=data)
        return response.get("data", response)

    def update(
        self,
        org_id: str,
        name: Optional[str] = None,
        minutes_available: Optional[int] = None,
        concurrency: Optional[int] = None,
        is_active: Optional[bool] = None,
        agent_pricing: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Update an organisation."""
        data = self._clean_params({
            "name": name,
            "minutes_available": minutes_available,
            "concurrency": concurrency,
            "is_active": is_active,
            "agent_pricing": agent_pricing,
            **kwargs,
        })
        response = self._client.put(self._build_path("organisations", org_id), json_data=data)
        return response.get("data", response)

    def delete(self, org_id: str) -> Dict[str, Any]:
        """Delete an organisation (soft delete)."""
        return self._client.delete(self._build_path("organisations", org_id))
