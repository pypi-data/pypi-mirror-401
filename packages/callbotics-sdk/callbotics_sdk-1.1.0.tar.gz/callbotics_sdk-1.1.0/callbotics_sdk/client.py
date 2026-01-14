"""
Callbotics SDK Client.

Main client class for interacting with the Callbotics API.
"""

from typing import Optional

from callbotics_sdk.http import HTTPClient
from callbotics_sdk.resources.users import UsersResource
from callbotics_sdk.resources.organisations import OrganisationsResource
from callbotics_sdk.resources.campaigns import CampaignsResource
from callbotics_sdk.resources.calls import CallsResource
from callbotics_sdk.resources.agents import AgentsResource
from callbotics_sdk.resources.contacts import ContactsResource
from callbotics_sdk.resources.live_monitoring import LiveMonitoringResource
from callbotics_sdk.resources.prompts import PromptsResource
from callbotics_sdk.resources.voice_configs import VoiceConfigsResource
from callbotics_sdk.resources.llm_configs import LLMConfigsResource
from callbotics_sdk.resources.stt_configs import STTConfigsResource
from callbotics_sdk.resources.telephony import TelephonyResource
from callbotics_sdk.resources.billing import BillingResource
from callbotics_sdk.resources.call_logs import CallLogsResource
from callbotics_sdk.resources.analytics import AnalyticsResource
from callbotics_sdk.resources.workflows import WorkflowsResource
from callbotics_sdk.resources.roles import RolesResource
from callbotics_sdk.resources.actions import ActionsResource


class CallboticsClient:
    """
    Main client for interacting with the Callbotics API.

    Usage:
        # Initialize with API key
        client = CallboticsClient(
            base_url="https://api.callbotics.ai",
            api_key="your-api-key"
        )

        # Or with bearer token
        client = CallboticsClient(
            base_url="https://api.callbotics.ai",
            token="your-bearer-token"
        )

        # List users
        users = client.users.list(page=1, per_page=10)

        # Create a campaign
        campaign = client.campaigns.create(
            name="My Campaign",
            organisation_id="org-123",
            agent_id="agent-456"
        )

        # Connect to live monitoring WebSocket
        async with client.live_monitoring.connect_campaigns() as ws:
            async for message in ws:
                print(message)
    """

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        token: Optional[str] = None,
        api_prefix: str = "/api/v1",
        timeout: float = 30.0,
    ):
        """
        Initialize the Callbotics client.

        Args:
            base_url: Base URL of the Callbotics API
            api_key: API key for authentication (X-API-Key header)
            token: Bearer token for authentication
            api_prefix: API path prefix (default: /api/v1)
            timeout: Request timeout in seconds
        """
        self._base_url = base_url.rstrip("/")
        self._api_prefix = api_prefix
        self._timeout = timeout

        # Initialize HTTP client
        headers = {}
        if api_key:
            headers["X-API-Key"] = api_key
        if token:
            headers["Authorization"] = f"Bearer {token}"

        self._http = HTTPClient(
            base_url=self._base_url,
            timeout=timeout,
            headers=headers,
        )

        # Initialize resources
        self._users: Optional[UsersResource] = None
        self._organisations: Optional[OrganisationsResource] = None
        self._campaigns: Optional[CampaignsResource] = None
        self._calls: Optional[CallsResource] = None
        self._agents: Optional[AgentsResource] = None
        self._contacts: Optional[ContactsResource] = None
        self._live_monitoring: Optional[LiveMonitoringResource] = None
        self._prompts: Optional[PromptsResource] = None
        self._voice_configs: Optional[VoiceConfigsResource] = None
        self._llm_configs: Optional[LLMConfigsResource] = None
        self._stt_configs: Optional[STTConfigsResource] = None
        self._telephony: Optional[TelephonyResource] = None
        self._billing: Optional[BillingResource] = None
        self._call_logs: Optional[CallLogsResource] = None
        self._analytics: Optional[AnalyticsResource] = None
        self._workflows: Optional[WorkflowsResource] = None
        self._roles: Optional[RolesResource] = None
        self._actions: Optional[ActionsResource] = None

    def set_token(self, token: str) -> None:
        """Set or update the bearer token."""
        self._http.set_header("Authorization", f"Bearer {token}")

    def set_api_key(self, api_key: str) -> None:
        """Set or update the API key."""
        self._http.set_header("X-API-Key", api_key)

    def close(self) -> None:
        """Close the HTTP client connections."""
        self._http.close()

    async def close_async(self) -> None:
        """Close the async HTTP client connections."""
        await self._http.close_async()

    # Resource properties with lazy initialization
    @property
    def users(self) -> UsersResource:
        """User management resource."""
        if self._users is None:
            self._users = UsersResource(self._http, self._api_prefix)
        return self._users

    @property
    def organisations(self) -> OrganisationsResource:
        """Organisation management resource."""
        if self._organisations is None:
            self._organisations = OrganisationsResource(self._http, self._api_prefix)
        return self._organisations

    # Alias for British/American spelling
    @property
    def organizations(self) -> OrganisationsResource:
        """Organisation management resource (US spelling alias)."""
        return self.organisations

    @property
    def campaigns(self) -> CampaignsResource:
        """Campaign management resource."""
        if self._campaigns is None:
            self._campaigns = CampaignsResource(self._http, self._api_prefix)
        return self._campaigns

    @property
    def calls(self) -> CallsResource:
        """Call management resource."""
        if self._calls is None:
            self._calls = CallsResource(self._http, self._api_prefix)
        return self._calls

    @property
    def agents(self) -> AgentsResource:
        """Agent configuration resource."""
        if self._agents is None:
            self._agents = AgentsResource(self._http, self._api_prefix)
        return self._agents

    @property
    def contacts(self) -> ContactsResource:
        """Contact list management resource."""
        if self._contacts is None:
            self._contacts = ContactsResource(self._http, self._api_prefix)
        return self._contacts

    @property
    def live_monitoring(self) -> LiveMonitoringResource:
        """Live monitoring resource (REST + WebSocket)."""
        if self._live_monitoring is None:
            self._live_monitoring = LiveMonitoringResource(self._http, self._api_prefix)
        return self._live_monitoring

    @property
    def prompts(self) -> PromptsResource:
        """Prompt template resource."""
        if self._prompts is None:
            self._prompts = PromptsResource(self._http, self._api_prefix)
        return self._prompts

    @property
    def voice_configs(self) -> VoiceConfigsResource:
        """Voice configuration resource."""
        if self._voice_configs is None:
            self._voice_configs = VoiceConfigsResource(self._http, self._api_prefix)
        return self._voice_configs

    @property
    def llm_configs(self) -> LLMConfigsResource:
        """LLM configuration resource."""
        if self._llm_configs is None:
            self._llm_configs = LLMConfigsResource(self._http, self._api_prefix)
        return self._llm_configs

    @property
    def stt_configs(self) -> STTConfigsResource:
        """STT configuration resource."""
        if self._stt_configs is None:
            self._stt_configs = STTConfigsResource(self._http, self._api_prefix)
        return self._stt_configs

    @property
    def telephony(self) -> TelephonyResource:
        """Telephony configuration resource."""
        if self._telephony is None:
            self._telephony = TelephonyResource(self._http, self._api_prefix)
        return self._telephony

    @property
    def billing(self) -> BillingResource:
        """Billing and usage resource."""
        if self._billing is None:
            self._billing = BillingResource(self._http, self._api_prefix)
        return self._billing

    @property
    def call_logs(self) -> CallLogsResource:
        """Call logs and reports resource."""
        if self._call_logs is None:
            self._call_logs = CallLogsResource(self._http, self._api_prefix)
        return self._call_logs

    @property
    def analytics(self) -> AnalyticsResource:
        """Dashboard analytics resource."""
        if self._analytics is None:
            self._analytics = AnalyticsResource(self._http, self._api_prefix)
        return self._analytics

    @property
    def workflows(self) -> WorkflowsResource:
        """Workflow management resource."""
        if self._workflows is None:
            self._workflows = WorkflowsResource(self._http, self._api_prefix)
        return self._workflows

    @property
    def roles(self) -> RolesResource:
        """Role management resource."""
        if self._roles is None:
            self._roles = RolesResource(self._http, self._api_prefix)
        return self._roles

    @property
    def actions(self) -> ActionsResource:
        """Action management resource."""
        if self._actions is None:
            self._actions = ActionsResource(self._http, self._api_prefix)
        return self._actions

    def __enter__(self) -> "CallboticsClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    async def __aenter__(self) -> "CallboticsClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close_async()
