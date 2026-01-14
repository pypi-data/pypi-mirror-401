"""
Analytics Resource - Dashboard analytics endpoints.
"""

from typing import Any, Dict, List, Optional

from callbotics_sdk.resources.base import BaseResource


class AnalyticsResource(BaseResource):
    """Dashboard analytics resource."""

    def get_calls_count(
        self,
        org_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get calls count analytics."""
        params = self._clean_params({
            "org_id": org_id,
            "campaign_id": campaign_id,
            "start_date": start_date,
            "end_date": end_date,
        })
        response = self._client.get(self._build_path("analytics", "calls_count"), params=params)
        return response.get("data", response)

    def get_call_minutes(
        self,
        org_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get call minutes analytics."""
        params = self._clean_params({
            "org_id": org_id,
            "campaign_id": campaign_id,
            "start_date": start_date,
            "end_date": end_date,
        })
        response = self._client.get(self._build_path("analytics", "call_minutes"), params=params)
        return response.get("data", response)

    def get_average_minutes(
        self,
        org_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get average call minutes analytics."""
        params = self._clean_params({
            "org_id": org_id,
            "campaign_id": campaign_id,
            "start_date": start_date,
            "end_date": end_date,
        })
        response = self._client.get(self._build_path("analytics", "average_minutes"), params=params)
        return response.get("data", response)

    def get_disposition_distribution(
        self,
        org_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get call disposition distribution."""
        params = self._clean_params({
            "org_id": org_id,
            "campaign_id": campaign_id,
            "start_date": start_date,
            "end_date": end_date,
        })
        response = self._client.get(
            self._build_path("analytics", "disposition_distribution"),
            params=params
        )
        return response.get("data", response)

    def get_campaigns_analytics(
        self,
        org_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get campaigns analytics."""
        params = self._clean_params({
            "org_id": org_id,
            "start_date": start_date,
            "end_date": end_date,
        })
        response = self._client.get(self._build_path("analytics", "campaigns"), params=params)
        return response.get("data", [])

    def get_qa_analysis_logs(
        self,
        campaign_id: Optional[str] = None,
        org_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get QA analysis logs."""
        params = self._clean_params({
            "campaign_id": campaign_id,
            "org_id": org_id,
            "start_date": start_date,
            "end_date": end_date,
        })
        response = self._client.get(self._build_path("qa-analysis-logs"), params=params)
        return response.get("data", [])
