"""
STT Configs Resource - Speech-to-Text configuration endpoints.
"""

from typing import Any, Dict, List, Optional

from callbotics_sdk.resources.base import BaseResource
from callbotics_sdk.models import PaginatedResponse


class STTConfigsResource(BaseResource):
    """Speech-to-Text configuration resource."""

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        company_id: Optional[str] = None,
    ) -> PaginatedResponse[Dict[str, Any]]:
        """List STT configurations."""
        params = self._clean_params({
            "current_page": page,
            "per_page": per_page,
            "company_id": company_id,
        })
        response = self._client.get(self._build_path("stt"), params=params)
        return PaginatedResponse.from_dict(response)

    def get(self, config_id: str) -> Dict[str, Any]:
        """Get a specific STT config by ID."""
        response = self._client.get(self._build_path("stt", config_id))
        return response.get("data", response)

    def create(
        self,
        name: str,
        provider: str,
        language: str = "en",
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a new STT configuration."""
        data = self._clean_params({
            "name": name,
            "provider": provider,
            "language": language,
            **kwargs,
        })
        response = self._client.post(self._build_path("stt"), json_data=data)
        return response.get("data", response)

    def update(self, config_id: str, **kwargs) -> Dict[str, Any]:
        """Update an STT configuration."""
        data = self._clean_params(kwargs)
        response = self._client.put(self._build_path("stt", config_id), json_data=data)
        return response.get("data", response)

    def delete(self, config_id: str) -> Dict[str, Any]:
        """Delete an STT configuration."""
        return self._client.delete(self._build_path("stt", config_id))

    def assign_to_company(self, config_id: str, company_id: str) -> Dict[str, Any]:
        """Assign STT config to a company."""
        data = {"stt_config_id": config_id, "company_id": company_id}
        return self._client.post(self._build_path("stt", "assign-company"), json_data=data)

    def get_assigned_stt(self, company_id: str) -> List[Dict[str, Any]]:
        """Get STT configs assigned to a company."""
        response = self._client.get(
            self._build_path("stt", "assigned-stt", company_id)
        )
        return response.get("data", [])
