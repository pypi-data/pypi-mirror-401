"""
Agents Resource - Agent configuration endpoints.
"""

from typing import Any, Dict, List, Optional

from callbotics_sdk.resources.base import BaseResource
from callbotics_sdk.models import PaginatedResponse


class AgentsResource(BaseResource):
    """Agent configuration resource."""

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        organisation_id: Optional[str] = None,
        search: Optional[str] = None,
    ) -> PaginatedResponse[Dict[str, Any]]:
        """List agents with pagination."""
        params = self._clean_params({
            "current_page": page,
            "per_page": per_page,
            "organisation_id": organisation_id,
            "search": search,
        })
        response = self._client.get(self._build_path("agents"), params=params)
        return PaginatedResponse.from_dict(response)

    def get(self, agent_id: str) -> Dict[str, Any]:
        """Get a specific agent by ID."""
        response = self._client.get(self._build_path("agents", agent_id))
        return response.get("data", response)

    def create(
        self,
        name: str,
        prompt_id: Optional[str] = None,
        voice_config_id: Optional[str] = None,
        llm_config_id: Optional[str] = None,
        stt_config_id: Optional[str] = None,
        organisation_id: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a new agent."""
        data = self._clean_params({
            "name": name,
            "prompt": prompt_id,
            "voice_config": voice_config_id,
            "llm_config": llm_config_id,
            "stt_config": stt_config_id,
            "organisation": organisation_id,
            **kwargs,
        })
        response = self._client.post(self._build_path("agents"), json_data=data)
        return response.get("data", response)

    def update(
        self,
        agent_id: str,
        name: Optional[str] = None,
        prompt_id: Optional[str] = None,
        voice_config_id: Optional[str] = None,
        llm_config_id: Optional[str] = None,
        stt_config_id: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Update an agent."""
        data = self._clean_params({
            "name": name,
            "prompt": prompt_id,
            "voice_config": voice_config_id,
            "llm_config": llm_config_id,
            "stt_config": stt_config_id,
            **kwargs,
        })
        response = self._client.put(self._build_path("agents", agent_id), json_data=data)
        return response.get("data", response)

    def delete(self, agent_id: str) -> Dict[str, Any]:
        """Delete an agent."""
        return self._client.delete(self._build_path("agents", agent_id))
