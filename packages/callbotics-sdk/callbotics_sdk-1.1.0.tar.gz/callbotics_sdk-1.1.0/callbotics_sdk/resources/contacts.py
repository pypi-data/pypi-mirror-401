"""
Contacts Resource - Contact list management endpoints.
"""

from typing import Any, BinaryIO, Dict, List, Optional

from callbotics_sdk.resources.base import BaseResource
from callbotics_sdk.models import PaginatedResponse


class ContactsResource(BaseResource):
    """Contact list management resource."""

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        campaign_id: Optional[str] = None,
        organisation_id: Optional[str] = None,
        search: Optional[str] = None,
    ) -> PaginatedResponse[Dict[str, Any]]:
        """List contact lists with pagination."""
        params = self._clean_params({
            "current_page": page,
            "per_page": per_page,
            "campaign_id": campaign_id,
            "organisation_id": organisation_id,
            "search": search,
        })
        response = self._client.get(self._build_path("contacts"), params=params)
        return PaginatedResponse.from_dict(response)

    def get(self, contact_list_id: str) -> Dict[str, Any]:
        """Get a specific contact list by ID."""
        response = self._client.get(self._build_path("contacts", contact_list_id))
        return response.get("data", response)

    def create(
        self,
        list_name: str,
        campaign_id: str,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a new contact list."""
        data = self._clean_params({
            "list_name": list_name,
            "campaign_id": campaign_id,
            **kwargs,
        })
        response = self._client.post(self._build_path("contacts"), json_data=data)
        return response.get("data", response)

    def upload(
        self,
        contact_list_id: str,
        file: BinaryIO,
        filename: str = "contacts.xlsx",
    ) -> Dict[str, Any]:
        """Upload contacts from file to a contact list."""
        response = self._client.request(
            "POST",
            self._build_path("contacts", contact_list_id, "upload"),
            files={"file": (filename, file)},
        )
        return response.get("data", response)

    def update_contact(
        self,
        contact_list_id: str,
        contact_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Update a specific contact in a list."""
        response = self._client.put(
            self._build_path("contacts", "specific-contact", contact_list_id),
            json_data=contact_data,
        )
        return response.get("data", response)

    def delete(self, contact_id: str) -> Dict[str, Any]:
        """Delete a contact."""
        return self._client.delete(self._build_path("contacts", contact_id))

    def activate(self, contact_id: str) -> Dict[str, Any]:
        """Activate a contact."""
        return self._client.put(self._build_path("contacts", contact_id, "activate"))

    def get_active_contacts(self, campaign_id: str) -> List[Dict[str, Any]]:
        """Get active contacts for a campaign."""
        response = self._client.get(
            self._build_path("contacts", "active_contacts", campaign_id)
        )
        return response.get("data", [])

    def get_timezones(self) -> List[str]:
        """Get list of available timezones."""
        response = self._client.get(self._build_path("contacts", "timezones"))
        return response.get("data", [])

    def get_sample_excel(self, campaign_id: str) -> bytes:
        """Get sample Excel template for contact upload."""
        response = self._client.get(
            self._build_path("contacts", "sample-excel", campaign_id)
        )
        return response
