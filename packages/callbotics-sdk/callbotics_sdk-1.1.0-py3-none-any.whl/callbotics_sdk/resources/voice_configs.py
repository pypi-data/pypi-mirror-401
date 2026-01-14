"""
Voice Configs Resource - Voice configuration endpoints.
"""

from typing import Any, Dict, List, Optional

from callbotics_sdk.resources.base import BaseResource
from callbotics_sdk.models import PaginatedResponse


class VoiceConfigsResource(BaseResource):
    """Voice configuration resource."""

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        company_id: Optional[str] = None,
    ) -> PaginatedResponse[Dict[str, Any]]:
        """List voice configurations."""
        params = self._clean_params({
            "current_page": page,
            "per_page": per_page,
            "company_id": company_id,
        })
        response = self._client.get(self._build_path("voice-configs"), params=params)
        return PaginatedResponse.from_dict(response)

    def get(self, config_id: str) -> Dict[str, Any]:
        """Get a specific voice config by ID."""
        response = self._client.get(self._build_path("voice-configs", config_id))
        return response.get("data", response)

    def create(
        self,
        name: str,
        provider: str,
        voice_id: str,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a new voice configuration."""
        data = self._clean_params({
            "name": name,
            "provider": provider,
            "voice_id": voice_id,
            **kwargs,
        })
        response = self._client.post(self._build_path("voice-configs"), json_data=data)
        return response.get("data", response)

    def update(self, config_id: str, **kwargs) -> Dict[str, Any]:
        """Update a voice configuration."""
        data = self._clean_params(kwargs)
        response = self._client.put(self._build_path("voice-configs", config_id), json_data=data)
        return response.get("data", response)

    def delete(self, config_id: str) -> Dict[str, Any]:
        """Delete a voice configuration."""
        return self._client.delete(self._build_path("voice-configs", config_id))

    def assign_to_company(self, config_id: str, company_id: str) -> Dict[str, Any]:
        """Assign voice config to a company."""
        data = {"voice_config_id": config_id, "company_id": company_id}
        return self._client.post(self._build_path("voice-configs", "assign-company"), json_data=data)

    def get_assigned_voices(self, company_id: str) -> List[Dict[str, Any]]:
        """Get voice configs assigned to a company."""
        response = self._client.get(
            self._build_path("voice-configs", "assigned-voices", company_id)
        )
        return response.get("data", [])
