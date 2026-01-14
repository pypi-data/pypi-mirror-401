"""
Users Resource - User management endpoints.
"""

from typing import Any, Dict, List, Optional

from callbotics_sdk.resources.base import BaseResource
from callbotics_sdk.models import User, PaginatedResponse


class UsersResource(BaseResource):
    """User management resource."""

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        search: Optional[str] = None,
        role_id: Optional[str] = None,
        organisation_id: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "desc",
    ) -> PaginatedResponse[Dict[str, Any]]:
        """List users with pagination and filtering."""
        params = self._clean_params({
            "current_page": page,
            "per_page": per_page,
            "search": search,
            "role_id": role_id,
            "organisation_id": organisation_id,
            "sort_by": sort_by,
            "sort_order": sort_order,
        })
        response = self._client.get(self._build_path("users"), params=params)
        return PaginatedResponse.from_dict(response)

    def get(self, user_id: str) -> Dict[str, Any]:
        """Get a specific user by ID."""
        response = self._client.get(self._build_path("users", user_id))
        return response.get("data", response)

    def create(
        self,
        email: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        role_id: Optional[str] = None,
        organisation_ids: Optional[List[str]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a new user."""
        data = self._clean_params({
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "role_id": role_id,
            "organisation_ids": organisation_ids,
            **kwargs,
        })
        response = self._client.post(self._build_path("users", "create"), json_data=data)
        return response.get("data", response)

    def update(
        self,
        user_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        role_id: Optional[str] = None,
        organisation_ids: Optional[List[str]] = None,
        is_active: Optional[bool] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Update a user."""
        data = self._clean_params({
            "first_name": first_name,
            "last_name": last_name,
            "role_id": role_id,
            "organisation_ids": organisation_ids,
            "is_active": is_active,
            **kwargs,
        })
        response = self._client.put(self._build_path("users", user_id), json_data=data)
        return response.get("data", response)

    def delete(self, user_id: str) -> Dict[str, Any]:
        """Delete a user (soft delete)."""
        return self._client.delete(self._build_path("users", user_id))

    def get_profile(self) -> Dict[str, Any]:
        """Get current user profile."""
        response = self._client.get(self._build_path("users", "profile"))
        return response.get("data", response)

    def update_profile(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Update current user profile."""
        data = self._clean_params({
            "first_name": first_name,
            "last_name": last_name,
            **kwargs,
        })
        response = self._client.put(self._build_path("users", "profile"), json_data=data)
        return response.get("data", response)

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login and get authentication tokens."""
        data = {"email": email, "password": password}
        return self._client.post(self._build_path("users", "login"), json_data=data)

    def logout(self) -> Dict[str, Any]:
        """Logout and invalidate tokens."""
        return self._client.post(self._build_path("users", "logout"))

    def reset_password(self, email: str) -> Dict[str, Any]:
        """Request password reset."""
        return self._client.post(
            self._build_path("users", "reset-password"),
            json_data={"email": email}
        )

    def list_companies(self) -> List[Dict[str, Any]]:
        """List all companies (superuser only)."""
        response = self._client.get(self._build_path("users", "companies"))
        return response.get("data", [])
