"""
Callbotics SDK Models.

Data classes for API responses and common structures.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Generic, List, Optional, TypeVar

T = TypeVar("T")


@dataclass
class APIResponse(Generic[T]):
    """Standard API response wrapper."""

    success: bool
    message: str
    data: Optional[T] = None
    status_code: int = 200

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "APIResponse":
        return cls(
            success=data.get("success", True),
            message=data.get("message", ""),
            data=data.get("data"),
            status_code=data.get("status_code", 200),
        )


@dataclass
class PaginatedResponse(Generic[T]):
    """Paginated list response."""

    items: List[T]
    total_records: int
    total_pages: int
    current_page: int
    per_page: int
    has_next: bool = False
    has_prev: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any], items_key: str = "data") -> "PaginatedResponse":
        items = data.get(items_key, [])
        total_records = data.get("total_records", len(items))
        per_page = data.get("per_page", 10)
        current_page = data.get("current_page", 1)
        total_pages = data.get("total_pages", 1)

        return cls(
            items=items,
            total_records=total_records,
            total_pages=total_pages,
            current_page=current_page,
            per_page=per_page,
            has_next=current_page < total_pages,
            has_prev=current_page > 1,
        )


@dataclass
class User:
    """User model."""

    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role_name: Optional[str] = None
    organisation_ids: List[str] = field(default_factory=list)
    is_active: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        return cls(
            id=data.get("id", data.get("_id", "")),
            email=data.get("email", ""),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            role_name=data.get("role_name"),
            organisation_ids=data.get("organisation_ids", []),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )


@dataclass
class Organisation:
    """Organisation model."""

    id: str
    name: str
    is_active: bool = True
    minutes_available: int = 0
    concurrency: int = 1
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Organisation":
        return cls(
            id=data.get("id", data.get("_id", "")),
            name=data.get("name", ""),
            is_active=data.get("is_active", True),
            minutes_available=data.get("minutes_available", 0),
            concurrency=data.get("concurrency", 1),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )


@dataclass
class Campaign:
    """Campaign model."""

    id: str
    name: str
    status: str = "draft"
    direction: str = "outbound"
    concurrency: int = 1
    organisation_id: Optional[str] = None
    agent_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Campaign":
        return cls(
            id=data.get("id", data.get("_id", "")),
            name=data.get("name", ""),
            status=data.get("status", "draft"),
            direction=data.get("direction", "outbound"),
            concurrency=data.get("concurrency", 1),
            organisation_id=data.get("organisation_id", data.get("organisation")),
            agent_id=data.get("agent_id", data.get("agent")),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )


@dataclass
class Call:
    """Call model."""

    id: str
    call_id: str
    status: str = "initiated"
    direction: str = "outbound"
    from_number: Optional[str] = None
    to_number: Optional[str] = None
    campaign_id: Optional[str] = None
    org_id: Optional[str] = None
    duration: Optional[int] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Call":
        return cls(
            id=data.get("id", data.get("_id", "")),
            call_id=data.get("call_id", ""),
            status=data.get("status", "initiated"),
            direction=data.get("direction", "outbound"),
            from_number=data.get("from_number"),
            to_number=data.get("to_number"),
            campaign_id=data.get("campaign_id"),
            org_id=data.get("org_id"),
            duration=data.get("duration"),
            created_at=data.get("created_at"),
        )


@dataclass
class Agent:
    """Agent configuration model."""

    id: str
    name: str
    prompt_id: Optional[str] = None
    voice_config_id: Optional[str] = None
    llm_config_id: Optional[str] = None
    stt_config_id: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Agent":
        return cls(
            id=data.get("id", data.get("_id", "")),
            name=data.get("name", ""),
            prompt_id=data.get("prompt_id", data.get("prompt")),
            voice_config_id=data.get("voice_config_id", data.get("voice_config")),
            llm_config_id=data.get("llm_config_id", data.get("llm_config")),
            stt_config_id=data.get("stt_config_id", data.get("stt_config")),
            created_at=data.get("created_at"),
        )


@dataclass
class ContactList:
    """Contact list model."""

    id: str
    list_name: str
    campaign_id: Optional[str] = None
    total_contacts: int = 0
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactList":
        return cls(
            id=data.get("id", data.get("_id", "")),
            list_name=data.get("list_name", ""),
            campaign_id=data.get("campaign_id"),
            total_contacts=data.get("total_contacts", 0),
            created_at=data.get("created_at"),
        )


@dataclass
class LiveCampaign:
    """Live campaign monitoring data."""

    campaign_id: str
    campaign_name: str
    active_calls_count: int = 0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LiveCampaign":
        return cls(
            campaign_id=data.get("campaign_id", ""),
            campaign_name=data.get("campaign_name", ""),
            active_calls_count=data.get("active_calls_count", 0),
        )


@dataclass
class LiveCall:
    """Live call monitoring data."""

    call_id: str
    from_number: str
    to_number: str
    monitoring: bool = False
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LiveCall":
        return cls(
            call_id=data.get("call_id", ""),
            from_number=data.get("from_number", ""),
            to_number=data.get("to_number", ""),
            monitoring=data.get("monitoring", False),
            created_at=data.get("created_at"),
        )


@dataclass
class TranscriptMessage:
    """Transcript message model."""

    time: str
    message: str
    type: str  # 'agent', 'human', 'call_ended'

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TranscriptMessage":
        # Handle nested format from API
        for key in ["callbotics", "Human", "call_ended", "unknown"]:
            if key in data:
                inner = data[key]
                return cls(
                    time=inner.get("time", ""),
                    message=inner.get("message", ""),
                    type=inner.get("type", key),
                )
        return cls(
            time=data.get("time", ""),
            message=data.get("message", ""),
            type=data.get("type", "unknown"),
        )
