"""
Workflows Resource - Workflow management endpoints.
"""

from typing import Any, BinaryIO, Dict, List, Optional

from callbotics_sdk.resources.base import BaseResource
from callbotics_sdk.models import PaginatedResponse


class WorkflowsResource(BaseResource):
    """Workflow management resource."""

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        org_id: Optional[str] = None,
        search: Optional[str] = None,
    ) -> PaginatedResponse[Dict[str, Any]]:
        """List workflows with pagination."""
        params = self._clean_params({
            "current_page": page,
            "per_page": per_page,
            "org_id": org_id,
            "search": search,
        })
        response = self._client.get(self._build_path("workflows"), params=params)
        return PaginatedResponse.from_dict(response)

    def get(self, workflow_id: str) -> Dict[str, Any]:
        """Get a specific workflow by ID."""
        response = self._client.get(self._build_path("workflows", workflow_id))
        return response.get("data", response)

    def create(
        self,
        name: str,
        workflow_data: Dict[str, Any],
        org_id: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a new workflow."""
        data = self._clean_params({
            "name": name,
            "workflow_data": workflow_data,
            "org_id": org_id,
            **kwargs,
        })
        response = self._client.post(self._build_path("workflows"), json_data=data)
        return response.get("data", response)

    def update(
        self,
        workflow_id: str,
        name: Optional[str] = None,
        workflow_data: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Update a workflow."""
        data = self._clean_params({
            "name": name,
            "workflow_data": workflow_data,
            **kwargs,
        })
        response = self._client.put(self._build_path("workflows", workflow_id), json_data=data)
        return response.get("data", response)

    def delete(self, workflow_id: str) -> Dict[str, Any]:
        """Delete a workflow."""
        return self._client.delete(self._build_path("workflows", workflow_id))

    def duplicate(self, workflow_id: str, new_name: Optional[str] = None) -> Dict[str, Any]:
        """Duplicate a workflow."""
        data = self._clean_params({"new_name": new_name})
        response = self._client.post(
            self._build_path("workflows", workflow_id, "duplicate"),
            json_data=data
        )
        return response.get("data", response)

    def transform(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform workflow data."""
        response = self._client.post(
            self._build_path("workflows", "transform"),
            json_data=workflow_data
        )
        return response.get("data", response)

    def transform_by_id(self, workflow_id: str) -> Dict[str, Any]:
        """Transform workflow by ID."""
        response = self._client.post(
            self._build_path("workflows", "transform-by-id"),
            json_data={"workflow_id": workflow_id}
        )
        return response.get("data", response)

    def create_campaign_from_workflow(
        self,
        workflow_id: str,
        campaign_name: str,
        org_id: str,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a campaign using workflow."""
        data = self._clean_params({
            "workflow_id": workflow_id,
            "campaign_name": campaign_name,
            "org_id": org_id,
            **kwargs,
        })
        response = self._client.post(
            self._build_path("workflows", "campaign-using-workflow"),
            json_data=data
        )
        return response.get("data", response)

    def upload_contacts(
        self,
        file: BinaryIO,
        filename: str = "contacts.xlsx",
    ) -> Dict[str, Any]:
        """Upload contact lists for workflow."""
        response = self._client.request(
            "POST",
            self._build_path("workflows", "contact-lists", "upload"),
            files={"file": (filename, file)},
        )
        return response.get("data", response)

    def get_contact_list(self, contact_list_id: str) -> Dict[str, Any]:
        """Get workflow contact list."""
        response = self._client.get(
            self._build_path("workflows", "contact-lists", contact_list_id)
        )
        return response.get("data", response)

    def download_contacts(self, contact_list_id: str) -> bytes:
        """Download contact lists for workflow."""
        return self._client.get(
            self._build_path("workflows", "contact-lists", contact_list_id, "download")
        )
