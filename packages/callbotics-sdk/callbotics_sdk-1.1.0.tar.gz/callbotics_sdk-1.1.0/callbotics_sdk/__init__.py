"""
Callbotics SDK - Python client library for the Callbotics Core API.

Usage:
    from callbotics_sdk import CallboticsClient

    client = CallboticsClient(
        base_url="https://api.callbotics.ai",
        api_key="your-api-key"
    )

    # List users
    users = client.users.list(page=1, per_page=10)

    # Create a campaign
    campaign = client.campaigns.create(name="My Campaign", ...)

    # Connect to live monitoring WebSocket
    async with client.live_monitoring.connect_campaigns() as ws:
        async for message in ws:
            print(message)
"""

from callbotics_sdk.client import CallboticsClient
from callbotics_sdk.exceptions import (
    CallboticsError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
)
from callbotics_sdk.models import (
    PaginatedResponse,
    APIResponse,
)

__version__ = "1.0.0"
__all__ = [
    "CallboticsClient",
    "CallboticsError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
    "PaginatedResponse",
    "APIResponse",
]
