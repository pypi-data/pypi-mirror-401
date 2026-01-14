"""
Call Logs Resource - Call logs and reports endpoints.
"""

from typing import Any, Dict, List, Optional

from callbotics_sdk.resources.base import BaseResource
from callbotics_sdk.models import PaginatedResponse


class CallLogsResource(BaseResource):
    """Call logs and reports resource."""

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        campaign_id: Optional[str] = None,
        org_id: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "desc",
    ) -> PaginatedResponse[Dict[str, Any]]:
        """List call logs with pagination and filtering."""
        params = self._clean_params({
            "current_page": page,
            "per_page": per_page,
            "campaign_id": campaign_id,
            "org_id": org_id,
            "status": status,
            "start_date": start_date,
            "end_date": end_date,
            "sort_by": sort_by,
            "sort_order": sort_order,
        })
        response = self._client.get(self._build_path("call-logs"), params=params)
        return PaginatedResponse.from_dict(response)

    def get(self, call_id: str) -> Dict[str, Any]:
        """Get a specific call log by ID."""
        response = self._client.get(self._build_path("call-logs", call_id))
        return response.get("data", response)

    def download(
        self,
        campaign_id: Optional[str] = None,
        org_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        format: str = "csv",
    ) -> bytes:
        """Download call logs as file."""
        params = self._clean_params({
            "campaign_id": campaign_id,
            "org_id": org_id,
            "start_date": start_date,
            "end_date": end_date,
            "format": format,
        })
        return self._client.get(self._build_path("call-logs", "download"), params=params)

    def get_reports(
        self,
        page: int = 1,
        per_page: int = 10,
        campaign_id: Optional[str] = None,
        org_id: Optional[str] = None,
    ) -> PaginatedResponse[Dict[str, Any]]:
        """List call reports."""
        params = self._clean_params({
            "current_page": page,
            "per_page": per_page,
            "campaign_id": campaign_id,
            "org_id": org_id,
        })
        response = self._client.get(self._build_path("report-logs"), params=params)
        return PaginatedResponse.from_dict(response)

    def get_report(self, report_id: str) -> Dict[str, Any]:
        """Get a specific report by ID."""
        response = self._client.get(self._build_path("report-logs", report_id))
        return response.get("data", response)

    def update_report(self, report_id: str, **kwargs) -> Dict[str, Any]:
        """Update a report."""
        data = self._clean_params(kwargs)
        response = self._client.put(self._build_path("report-logs", report_id), json_data=data)
        return response.get("data", response)

    def download_reports(
        self,
        report_ids: List[str],
        format: str = "csv",
    ) -> bytes:
        """Download multiple reports."""
        data = {"report_ids": report_ids, "format": format}
        return self._client.post(self._build_path("report-logs", "download"), json_data=data)

    def publish_report(self, report_id: str) -> Dict[str, Any]:
        """Publish a report to client."""
        return self._client.post(
            self._build_path("report-logs", "publish-to-client"),
            json_data={"report_id": report_id}
        )

    def get_recording_url(self, call_id: str) -> str:
        """Get presigned URL for call recording."""
        response = self._client.get(
            self._build_path("recordings", "presigned-url"),
            params={"call_id": call_id}
        )
        return response.get("url", response.get("data", {}).get("url", ""))
