"""
Telephony Resource - Telephony configuration endpoints.
"""

from typing import Any, Dict, List, Optional

from callbotics_sdk.resources.base import BaseResource
from callbotics_sdk.models import PaginatedResponse


class TelephonyResource(BaseResource):
    """Telephony configuration resource."""

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        company_id: Optional[str] = None,
    ) -> PaginatedResponse[Dict[str, Any]]:
        """List telephony configurations."""
        params = self._clean_params({
            "current_page": page,
            "per_page": per_page,
            "company_id": company_id,
        })
        response = self._client.get(self._build_path("telephony"), params=params)
        return PaginatedResponse.from_dict(response)

    def get(self, telephony_id: str) -> Dict[str, Any]:
        """Get a specific telephony config by ID."""
        response = self._client.get(self._build_path("telephony", telephony_id))
        return response.get("data", response)

    def create(
        self,
        name: str,
        provider: str,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a new telephony configuration."""
        data = self._clean_params({
            "name": name,
            "provider": provider,
            **kwargs,
        })
        response = self._client.post(self._build_path("telephony"), json_data=data)
        return response.get("data", response)

    def update(self, telephony_id: str, **kwargs) -> Dict[str, Any]:
        """Update a telephony configuration."""
        data = self._clean_params(kwargs)
        response = self._client.put(self._build_path("telephony", telephony_id), json_data=data)
        return response.get("data", response)

    def delete(self, telephony_id: str) -> Dict[str, Any]:
        """Delete a telephony configuration."""
        return self._client.delete(self._build_path("telephony", telephony_id))

    def assign_to_company(self, telephony_id: str, company_id: str) -> Dict[str, Any]:
        """Assign telephony config to a company."""
        data = {"telephony_id": telephony_id, "company_id": company_id}
        return self._client.post(self._build_path("telephony", "assign-company"), json_data=data)

    def get_assigned_telephony(self, company_id: str) -> List[Dict[str, Any]]:
        """Get telephony configs assigned to a company."""
        response = self._client.get(
            self._build_path("telephony", "assigned-telephony", company_id)
        )
        return response.get("data", [])

    def get_available_numbers(
        self,
        country: str = "US",
        area_code: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Get available phone numbers for purchase."""
        data = self._clean_params({
            "country": country,
            "area_code": area_code,
            "limit": limit,
        })
        response = self._client.post(
            self._build_path("telephony", "available_phone_numbers"),
            json_data=data
        )
        return response.get("data", [])

    def get_purchased_numbers(self) -> List[Dict[str, Any]]:
        """Get purchased phone numbers."""
        response = self._client.get(self._build_path("telephony", "purchased_numbers"))
        return response.get("data", [])
