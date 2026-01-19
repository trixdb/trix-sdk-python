"""Webhook-related types for Trix SDK."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseResponse
from .enums import WebhookEvent


class WebhookFilter(BaseModel):
    """Webhook event filters."""

    space_ids: Optional[List[str]] = None
    tags: Optional[List[str]] = None


class Webhook(BaseResponse):
    """Webhook configuration."""

    id: str
    name: str
    url: str
    events: List[WebhookEvent]
    space_id: Optional[str] = None
    headers: Dict[str, str] = Field(default_factory=dict)
    filters: Optional[WebhookFilter] = None
    active: bool = True
    created_at: datetime
    updated_at: datetime


class WebhookCreate(BaseModel):
    """Request to create a webhook."""

    name: str
    url: str
    events: List[WebhookEvent]
    space_id: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    filters: Optional[WebhookFilter] = None


class WebhookUpdate(BaseModel):
    """Request to update a webhook."""

    name: Optional[str] = None
    url: Optional[str] = None
    events: Optional[List[WebhookEvent]] = None
    headers: Optional[Dict[str, str]] = None
    filters: Optional[WebhookFilter] = None
    active: Optional[bool] = None


class WebhookList(BaseResponse):
    """List of webhooks."""

    data: List[Webhook]


class WebhookDelivery(BaseResponse):
    """Webhook delivery attempt."""

    id: str
    webhook_id: str
    event_type: WebhookEvent
    status_code: Optional[int] = None
    success: bool
    payload: Dict[str, Any]
    error: Optional[str] = None
    attempted_at: datetime


class WebhookDeliveryList(BaseResponse):
    """List of webhook deliveries."""

    data: List[WebhookDelivery]


class WebhookEventInfo(BaseModel):
    """Webhook event."""

    id: str
    type: str
    data: Dict[str, Any]
    created_at: datetime


class WebhookEventList(BaseResponse):
    """List of webhook events."""

    data: List[WebhookEventInfo]


class WebhookEventTypeInfo(BaseModel):
    """Webhook event type info."""

    name: str
    description: str
    event_schema: Optional[Dict[str, Any]] = Field(default=None, alias="schema")


class WebhookEventTypesResult(BaseResponse):
    """Result of getting webhook event types."""

    types: List[WebhookEventTypeInfo]


class WebhookEventStats(BaseModel):
    """Stats for a webhook event type."""

    count: int
    success_rate: float


class WebhookStats(BaseResponse):
    """Webhook statistics."""

    total_deliveries: int
    success_rate: float
    avg_latency: float
    by_event: Dict[str, WebhookEventStats]
