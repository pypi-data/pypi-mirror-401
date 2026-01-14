"""
Callbotics SDK Resources.

API resource classes for different endpoints.
"""

from callbotics_sdk.resources.base import BaseResource
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

__all__ = [
    "BaseResource",
    "UsersResource",
    "OrganisationsResource",
    "CampaignsResource",
    "CallsResource",
    "AgentsResource",
    "ContactsResource",
    "LiveMonitoringResource",
    "PromptsResource",
    "VoiceConfigsResource",
    "LLMConfigsResource",
    "STTConfigsResource",
    "TelephonyResource",
    "BillingResource",
    "CallLogsResource",
    "AnalyticsResource",
    "WorkflowsResource",
    "RolesResource",
    "ActionsResource",
]
