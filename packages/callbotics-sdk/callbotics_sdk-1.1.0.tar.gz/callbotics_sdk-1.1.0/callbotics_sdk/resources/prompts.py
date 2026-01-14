"""
Prompts Resource - Prompt template management endpoints.
"""

from typing import Any, Dict, List, Optional

from callbotics_sdk.resources.base import BaseResource
from callbotics_sdk.models import PaginatedResponse


class PromptsResource(BaseResource):
    """Prompt template management resource."""

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        company_id: Optional[str] = None,
        search: Optional[str] = None,
    ) -> PaginatedResponse[Dict[str, Any]]:
        """List prompt templates with pagination."""
        params = self._clean_params({
            "current_page": page,
            "per_page": per_page,
            "company_id": company_id,
            "search": search,
        })
        response = self._client.get(self._build_path("prompt"), params=params)
        return PaginatedResponse.from_dict(response)

    def get(self, prompt_id: str) -> Dict[str, Any]:
        """Get a specific prompt template by ID."""
        response = self._client.get(self._build_path("prompt", prompt_id))
        return response.get("data", response)

    def create(
        self,
        name: str,
        system_prompt: str,
        initial_message: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a new prompt template."""
        data = self._clean_params({
            "name": name,
            "system_prompt": system_prompt,
            "initial_message": initial_message,
            **kwargs,
        })
        response = self._client.post(self._build_path("prompt"), json_data=data)
        return response.get("data", response)

    def update(
        self,
        prompt_id: str,
        name: Optional[str] = None,
        system_prompt: Optional[str] = None,
        initial_message: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Update a prompt template."""
        data = self._clean_params({
            "name": name,
            "system_prompt": system_prompt,
            "initial_message": initial_message,
            **kwargs,
        })
        response = self._client.put(self._build_path("prompt", prompt_id), json_data=data)
        return response.get("data", response)

    def delete(self, prompt_id: str) -> Dict[str, Any]:
        """Delete a prompt template."""
        return self._client.delete(self._build_path("prompt", prompt_id))

    def assign_to_company(self, prompt_id: str, company_id: str) -> Dict[str, Any]:
        """Assign prompt to a company."""
        data = {"prompt_id": prompt_id, "company_id": company_id}
        return self._client.post(self._build_path("prompt", "assign-company"), json_data=data)

    def get_assigned_prompts(self, company_id: str) -> List[Dict[str, Any]]:
        """Get prompts assigned to a company."""
        response = self._client.get(
            self._build_path("prompt", "assigned-prompts", company_id)
        )
        return response.get("data", [])
