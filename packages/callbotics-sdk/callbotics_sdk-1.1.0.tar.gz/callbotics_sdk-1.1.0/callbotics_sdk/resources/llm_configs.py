"""
LLM Configs Resource - LLM configuration endpoints.
"""

from typing import Any, Dict, List, Optional

from callbotics_sdk.resources.base import BaseResource
from callbotics_sdk.models import PaginatedResponse


class LLMConfigsResource(BaseResource):
    """LLM configuration resource."""

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        company_id: Optional[str] = None,
    ) -> PaginatedResponse[Dict[str, Any]]:
        """List LLM configurations."""
        params = self._clean_params({
            "current_page": page,
            "per_page": per_page,
            "company_id": company_id,
        })
        response = self._client.get(self._build_path("llm", "config"), params=params)
        return PaginatedResponse.from_dict(response)

    def get(self, config_id: str) -> Dict[str, Any]:
        """Get a specific LLM config by ID."""
        response = self._client.get(self._build_path("llm", "config", config_id))
        return response.get("data", response)

    def create(
        self,
        name: str,
        provider: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a new LLM configuration."""
        data = self._clean_params({
            "name": name,
            "provider": provider,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs,
        })
        response = self._client.post(self._build_path("llm", "config"), json_data=data)
        return response.get("data", response)

    def update(self, config_id: str, **kwargs) -> Dict[str, Any]:
        """Update an LLM configuration."""
        data = self._clean_params(kwargs)
        response = self._client.put(self._build_path("llm", "config", config_id), json_data=data)
        return response.get("data", response)

    def delete(self, config_id: str) -> Dict[str, Any]:
        """Delete an LLM configuration."""
        return self._client.delete(self._build_path("llm", "config", config_id))

    def assign_to_company(self, config_id: str, company_id: str) -> Dict[str, Any]:
        """Assign LLM config to a company."""
        data = {"llm_config_id": config_id, "company_id": company_id}
        return self._client.post(self._build_path("llm", "config", "assign-company"), json_data=data)

    def get_assigned_llms(self, company_id: str) -> List[Dict[str, Any]]:
        """Get LLM configs assigned to a company."""
        response = self._client.get(
            self._build_path("llm", "config", "assigned-llms", company_id)
        )
        return response.get("data", [])
