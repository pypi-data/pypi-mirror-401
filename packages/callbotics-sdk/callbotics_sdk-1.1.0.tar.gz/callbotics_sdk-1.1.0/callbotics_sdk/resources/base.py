"""
Base Resource class for all API resources.
"""

from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from callbotics_sdk.http import HTTPClient


class BaseResource:
    """Base class for API resources."""

    def __init__(self, client: "HTTPClient", api_prefix: str = "/api/v1"):
        self._client = client
        self._api_prefix = api_prefix

    def _build_path(self, *parts: str) -> str:
        """Build API path from parts."""
        path_parts = [self._api_prefix] + [str(p).strip("/") for p in parts if p]
        return "/".join(path_parts)

    def _clean_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Remove None values from params dict."""
        return {k: v for k, v in params.items() if v is not None}
