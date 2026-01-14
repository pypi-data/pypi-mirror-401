"""
Live Monitoring Resource - Real-time monitoring endpoints and WebSocket connections.
"""

import asyncio
import json
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict, List, Optional, TYPE_CHECKING

from callbotics_sdk.resources.base import BaseResource
from callbotics_sdk.models import LiveCampaign, LiveCall, TranscriptMessage

if TYPE_CHECKING:
    from callbotics_sdk.http import HTTPClient

try:
    import websockets
    from websockets.client import WebSocketClientProtocol
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False


class WebSocketConnection:
    """WebSocket connection wrapper for live monitoring."""

    def __init__(
        self,
        ws: "WebSocketClientProtocol",
        message_type: str,
    ):
        self._ws = ws
        self._message_type = message_type
        self._closed = False

    async def receive(self) -> Optional[Dict[str, Any]]:
        """Receive a message from the WebSocket."""
        if self._closed:
            return None
        try:
            message = await self._ws.recv()
            data = json.loads(message)
            return data
        except Exception:
            self._closed = True
            return None

    async def send_ping(self) -> None:
        """Send a ping message."""
        if not self._closed:
            await self._ws.send(json.dumps({"type": "ping"}))

    async def close(self) -> None:
        """Close the WebSocket connection."""
        if not self._closed:
            self._closed = True
            await self._ws.close()

    @property
    def closed(self) -> bool:
        """Check if connection is closed."""
        return self._closed

    def __aiter__(self) -> "WebSocketConnection":
        return self

    async def __anext__(self) -> Dict[str, Any]:
        """Async iterator for receiving messages."""
        message = await self.receive()
        if message is None:
            raise StopAsyncIteration
        return message


class LiveMonitoringResource(BaseResource):
    """Live monitoring resource with REST and WebSocket support."""

    def __init__(self, client: "HTTPClient", api_prefix: str = "/api/v1"):
        super().__init__(client, api_prefix)
        self._ws_base_url: Optional[str] = None

    def set_websocket_url(self, ws_url: str) -> None:
        """Set the WebSocket base URL."""
        self._ws_base_url = ws_url.rstrip("/")

    def _get_ws_url(self) -> str:
        """Get WebSocket URL from HTTP base URL."""
        if self._ws_base_url:
            return self._ws_base_url
        # Convert http(s) to ws(s)
        base = self._client.base_url
        if base.startswith("https://"):
            return base.replace("https://", "wss://")
        elif base.startswith("http://"):
            return base.replace("http://", "ws://")
        return f"ws://{base}"

    # REST Endpoints
    def get_live_campaigns(self) -> Dict[str, Any]:
        """Get live campaigns with ongoing calls."""
        response = self._client.get(self._build_path("live-monitoring"))
        return response.get("data", response)

    def get_live_calls(
        self,
        campaign_id: Optional[str] = None,
        org_id: Optional[str] = None,
        page: int = 1,
        per_page: int = 10,
    ) -> Dict[str, Any]:
        """Get live calls list."""
        params = self._clean_params({
            "campaign_id": campaign_id,
            "org_id": org_id,
            "current_page": page,
            "per_page": per_page,
        })
        response = self._client.get(self._build_path("live-monitoring"), params=params)
        return response.get("data", response)

    def get_transcript(self, call_id: str) -> List[Dict[str, Any]]:
        """Get call transcript."""
        response = self._client.get(self._build_path("live-monitoring", "transcript", call_id))
        return response.get("data", [])

    def end_call(self, call_id: str) -> Dict[str, Any]:
        """End an active call."""
        return self._client.post(
            self._build_path("live-monitoring", "end_call"),
            json_data={"call_id": call_id}
        )

    def get_dashboard_metrics(self, org_id: Optional[str] = None) -> Dict[str, Any]:
        """Get dashboard metrics."""
        params = self._clean_params({"org_id": org_id})
        response = self._client.get(
            self._build_path("live-monitoring", "dashboard_metrics"),
            params=params
        )
        return response.get("data", response)

    # WebSocket Endpoints
    @asynccontextmanager
    async def connect_campaigns(
        self,
        token: Optional[str] = None,
    ) -> AsyncIterator[WebSocketConnection]:
        """Connect to live campaigns WebSocket.

        Usage:
            async with client.live_monitoring.connect_campaigns() as ws:
                async for message in ws:
                    print(message)
        """
        if not WEBSOCKETS_AVAILABLE:
            raise ImportError("websockets package is required for WebSocket support. Install with: pip install websockets")

        ws_url = f"{self._get_ws_url()}{self._api_prefix}/live-monitoring-ws/ws/campaigns/"

        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        elif "Authorization" in self._client._headers:
            headers["Authorization"] = self._client._headers["Authorization"]

        async with websockets.connect(ws_url, extra_headers=headers) as ws:
            yield WebSocketConnection(ws, "live_campaigns")

    @asynccontextmanager
    async def connect_campaign_calls(
        self,
        campaign_id: str,
        token: Optional[str] = None,
    ) -> AsyncIterator[WebSocketConnection]:
        """Connect to campaign calls WebSocket.

        Usage:
            async with client.live_monitoring.connect_campaign_calls("campaign-123") as ws:
                async for message in ws:
                    print(message)
        """
        if not WEBSOCKETS_AVAILABLE:
            raise ImportError("websockets package is required for WebSocket support. Install with: pip install websockets")

        ws_url = f"{self._get_ws_url()}{self._api_prefix}/live-monitoring-ws/ws/campaign/{campaign_id}/calls"

        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        elif "Authorization" in self._client._headers:
            headers["Authorization"] = self._client._headers["Authorization"]

        async with websockets.connect(ws_url, extra_headers=headers) as ws:
            yield WebSocketConnection(ws, "campaign_calls")

    @asynccontextmanager
    async def connect_transcript(
        self,
        call_id: str,
        token: Optional[str] = None,
    ) -> AsyncIterator[WebSocketConnection]:
        """Connect to call transcript WebSocket.

        Usage:
            async with client.live_monitoring.connect_transcript("call-123") as ws:
                async for message in ws:
                    print(message)
        """
        if not WEBSOCKETS_AVAILABLE:
            raise ImportError("websockets package is required for WebSocket support. Install with: pip install websockets")

        ws_url = f"{self._get_ws_url()}{self._api_prefix}/live-monitoring-ws/ws/transcript/{call_id}"

        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        elif "Authorization" in self._client._headers:
            headers["Authorization"] = self._client._headers["Authorization"]

        async with websockets.connect(ws_url, extra_headers=headers) as ws:
            yield WebSocketConnection(ws, "transcript")

    async def stream_campaigns(
        self,
        token: Optional[str] = None,
        on_message: Optional[callable] = None,
        on_error: Optional[callable] = None,
    ) -> None:
        """Stream live campaigns updates.

        Args:
            token: Optional auth token
            on_message: Callback for each message
            on_error: Callback for errors
        """
        try:
            async with self.connect_campaigns(token) as ws:
                async for message in ws:
                    if on_message:
                        on_message(message)
        except Exception as e:
            if on_error:
                on_error(e)
            else:
                raise

    async def stream_transcript(
        self,
        call_id: str,
        token: Optional[str] = None,
        on_message: Optional[callable] = None,
        on_error: Optional[callable] = None,
    ) -> None:
        """Stream live transcript updates.

        Args:
            call_id: The call ID to stream
            token: Optional auth token
            on_message: Callback for each message
            on_error: Callback for errors
        """
        try:
            async with self.connect_transcript(call_id, token) as ws:
                async for message in ws:
                    if on_message:
                        on_message(message)
        except Exception as e:
            if on_error:
                on_error(e)
            else:
                raise
