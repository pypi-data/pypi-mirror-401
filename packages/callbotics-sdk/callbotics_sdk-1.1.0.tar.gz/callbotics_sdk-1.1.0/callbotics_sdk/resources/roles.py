"""
Roles Resource - Role management endpoints.
"""

from typing import Any, Dict, List, Optional

from callbotics_sdk.resources.base import BaseResource
from callbotics_sdk.models import PaginatedResponse


class RolesResource(BaseResource):
    """Role management resource."""

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        search: Optional[str] = None,
    ) -> PaginatedResponse[Dict[str, Any]]:
        """List roles with pagination."""
        params = self._clean_params({
            "current_page": page,
            "per_page": per_page,
            "search": search,
        })
        response = self._client.get(self._build_path("roles"), params=params)
        return PaginatedResponse.from_dict(response)

    def get(self, role_id: str) -> Dict[str, Any]:
        """Get a specific role by ID."""
        response = self._client.get(self._build_path("roles", role_id))
        return response.get("data", response)

    def create(
        self,
        name: str,
        permissions: Optional[List[str]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a new role."""
        data = self._clean_params({
            "name": name,
            "permissions": permissions,
            **kwargs,
        })
        response = self._client.post(self._build_path("roles"), json_data=data)
        return response.get("data", response)

    def update(
        self,
        role_id: str,
        name: Optional[str] = None,
        permissions: Optional[List[str]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Update a role."""
        data = self._clean_params({
            "name": name,
            "permissions": permissions,
            **kwargs,
        })
        response = self._client.put(self._build_path("roles", role_id), json_data=data)
        return response.get("data", response)

    def delete(self, role_id: str) -> Dict[str, Any]:
        """Delete a role."""
        return self._client.delete(self._build_path("roles", role_id))

    def list_permissions(
        self,
        page: int = 1,
        per_page: int = 100,
    ) -> PaginatedResponse[Dict[str, Any]]:
        """List available permissions."""
        params = self._clean_params({
            "current_page": page,
            "per_page": per_page,
        })
        response = self._client.get(self._build_path("permissions"), params=params)
        return PaginatedResponse.from_dict(response)
