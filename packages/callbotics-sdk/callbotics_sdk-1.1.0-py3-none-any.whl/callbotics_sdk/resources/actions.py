"""
Actions Resource - Action management endpoints.
"""

from typing import Any, Dict, List, Optional

from callbotics_sdk.resources.base import BaseResource
from callbotics_sdk.models import PaginatedResponse


class ActionsResource(BaseResource):
    """Action management resource."""

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        search: Optional[str] = None,
    ) -> PaginatedResponse[Dict[str, Any]]:
        """List actions with pagination."""
        params = self._clean_params({
            "current_page": page,
            "per_page": per_page,
            "search": search,
        })
        response = self._client.get(self._build_path("actions"), params=params)
        return PaginatedResponse.from_dict(response)

    def get(self, action_id: str) -> Dict[str, Any]:
        """Get a specific action by ID."""
        response = self._client.get(self._build_path("actions", action_id))
        return response.get("data", response)

    def create(
        self,
        name: str,
        action_type: str,
        config: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a new action."""
        data = self._clean_params({
            "name": name,
            "action_type": action_type,
            "config": config,
            **kwargs,
        })
        response = self._client.post(self._build_path("actions"), json_data=data)
        return response.get("data", response)

    def update(
        self,
        action_id: str,
        name: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Update an action."""
        data = self._clean_params({
            "name": name,
            "config": config,
            **kwargs,
        })
        response = self._client.put(self._build_path("actions", action_id), json_data=data)
        return response.get("data", response)

    def delete(self, action_id: str) -> Dict[str, Any]:
        """Delete an action."""
        return self._client.delete(self._build_path("actions", action_id))

    def get_organisations(self, action_id: str) -> List[Dict[str, Any]]:
        """Get organisations for an action."""
        response = self._client.get(self._build_path("actions", action_id, "orgs"))
        return response.get("data", [])
