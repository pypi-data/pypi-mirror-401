"""
Billing Resource - Billing and usage endpoints.
"""

from typing import Any, Dict, List, Optional

from callbotics_sdk.resources.base import BaseResource
from callbotics_sdk.models import PaginatedResponse


class BillingResource(BaseResource):
    """Billing and usage resource."""

    def get_usage(
        self,
        org_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get usage records."""
        params = self._clean_params({
            "org_id": org_id,
            "start_date": start_date,
            "end_date": end_date,
        })
        response = self._client.get(self._build_path("usage"), params=params)
        return response.get("data", [])

    def get_usage_summary(
        self,
        org_id: Optional[str] = None,
        period: str = "monthly",
    ) -> Dict[str, Any]:
        """Get usage summary."""
        params = self._clean_params({
            "org_id": org_id,
            "period": period,
        })
        response = self._client.get(self._build_path("usage", "summary"), params=params)
        return response.get("data", response)

    def get_billing_info(self, org_id: Optional[str] = None) -> Dict[str, Any]:
        """Get billing information."""
        params = self._clean_params({"org_id": org_id})
        response = self._client.get(self._build_path("usage", "billing-info"), params=params)
        return response.get("data", response)

    def get_org_billing_summary(self, org_id: str) -> Dict[str, Any]:
        """Get organisation billing summary."""
        response = self._client.get(
            self._build_path("usage", "organization", org_id, "billing-summary")
        )
        return response.get("data", response)

    def create_stripe_session(
        self,
        amount: float,
        currency: str = "usd",
        org_id: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a Stripe checkout session."""
        data = self._clean_params({
            "amount": amount,
            "currency": currency,
            "org_id": org_id,
            **kwargs,
        })
        response = self._client.post(
            self._build_path("billing", "stripe", "create-session"),
            json_data=data
        )
        return response.get("data", response)

    def get_invoice(self, txn_id: str) -> Dict[str, Any]:
        """Get invoice details."""
        response = self._client.get(self._build_path("billing", "invoice", txn_id))
        return response.get("data", response)

    def get_usage_report(
        self,
        org_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get usage report."""
        params = self._clean_params({
            "org_id": org_id,
            "start_date": start_date,
            "end_date": end_date,
        })
        response = self._client.get(self._build_path("billing", "usage-report"), params=params)
        return response.get("data", response)

    def get_campaign_usage_report(
        self,
        campaign_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get campaign-specific usage report."""
        params = self._clean_params({
            "campaign_id": campaign_id,
            "start_date": start_date,
            "end_date": end_date,
        })
        response = self._client.get(
            self._build_path("billing", "campaign-usage-report"),
            params=params
        )
        return response.get("data", response)

    def get_payment_transactions(
        self,
        page: int = 1,
        per_page: int = 10,
        org_id: Optional[str] = None,
    ) -> PaginatedResponse[Dict[str, Any]]:
        """Get payment transactions."""
        params = self._clean_params({
            "current_page": page,
            "per_page": per_page,
            "org_id": org_id,
        })
        response = self._client.get(self._build_path("payment-transactions"), params=params)
        return PaginatedResponse.from_dict(response)

    def export_payment_transactions(
        self,
        org_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> bytes:
        """Export payment transactions."""
        params = self._clean_params({
            "org_id": org_id,
            "start_date": start_date,
            "end_date": end_date,
        })
        return self._client.get(self._build_path("payment-transactions", "export"), params=params)
