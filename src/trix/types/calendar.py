"""Calendar types for Trix SDK (ADR-075)."""

from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel

from .base import BaseResponse


class CalendarEventTime(BaseModel):
    """Start or end time for a calendar event."""

    dateTime: Optional[str] = None
    date: Optional[str] = None
    timeZone: Optional[str] = None


class CalendarEvent(BaseResponse):
    """A calendar event."""

    id: str
    title: str
    start: CalendarEventTime
    end: CalendarEventTime
    location: Optional[str] = None
    description: Optional[str] = None
    attendee_count: Optional[int] = None
    calendar_id: str
    provider: str


class CalendarEventsResponse(BaseResponse):
    """Response for listing calendar events."""

    events: List[CalendarEvent]
    total: int
    has_more: Optional[bool] = None


class CalendarSyncResult(BaseResponse):
    """Result of syncing calendar events to memories."""

    synced: int
    skipped: int
    failed: int
    total_events: int


class CalendarConnection(BaseResponse):
    """A calendar provider connection."""

    id: str
    provider: str
    status: str
    connected_at: str
    last_sync_at: Optional[str] = None


class CalendarConnectionsResponse(BaseResponse):
    """Response for listing calendar connections."""

    connections: List[CalendarConnection]


class Calendar(BaseResponse):
    """A calendar within a connection."""

    id: str
    name: str
    primary: Optional[bool] = None
    sync_enabled: Optional[bool] = None


class CalendarListResponse(BaseResponse):
    """Response for listing calendars."""

    calendars: List[Calendar]
    provider: str


class SyncCalendarParams(BaseModel):
    """Parameters for syncing calendar events to memories."""

    connection_id: str
    calendar_id: Optional[str] = None
    days_past: int = 30
    days_future: int = 90
    space_id: Optional[str] = None
    pii_level: Literal["full", "minimal", "none"] = "minimal"
    tags: Optional[List[str]] = None
