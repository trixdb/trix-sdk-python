"""Calendar resource for Trix SDK (ADR-075)."""

from typing import Any, Dict, List, Optional

from .base import BaseAsyncResource, BaseSyncResource
from ..types.calendar import (
    CalendarConnectionsResponse,
    CalendarEventsResponse,
    CalendarListResponse,
    CalendarSyncResult,
    SyncCalendarParams,
)
from ..utils.security import validate_id


class CalendarResource(BaseSyncResource):
    """Sync resource for calendar operations.

    Example:
        >>> events = client.calendar.list_events(days=7)
        >>> client.calendar.sync_to_memories(connection_id="conn-123")
    """

    def list_events(
        self,
        *,
        connection_id: Optional[str] = None,
        calendar_id: Optional[str] = None,
        days: int = 7,
        limit: int = 50,
    ) -> CalendarEventsResponse:
        """List upcoming calendar events."""
        params: Dict[str, Any] = {"days": days, "limit": limit}
        if connection_id is not None:
            params["connection_id"] = connection_id
        if calendar_id is not None:
            params["calendar_id"] = calendar_id
        response = self._request("GET", "/calendar/events", params=params)
        return CalendarEventsResponse.model_validate(response)

    def sync_to_memories(
        self,
        *,
        connection_id: str,
        calendar_id: Optional[str] = None,
        days_past: int = 30,
        days_future: int = 90,
        space_id: Optional[str] = None,
        pii_level: str = "minimal",
        tags: Optional[List[str]] = None,
    ) -> CalendarSyncResult:
        """Sync calendar events to memories."""
        data = SyncCalendarParams(
            connection_id=connection_id,
            calendar_id=calendar_id,
            days_past=days_past,
            days_future=days_future,
            space_id=space_id,
            pii_level=pii_level,
            tags=tags,
        )
        response = self._request(
            "POST", "/calendar/sync", json=data.model_dump(exclude_none=True)
        )
        return CalendarSyncResult.model_validate(response)

    def list_connections(self) -> CalendarConnectionsResponse:
        """List calendar connections."""
        response = self._request("GET", "/calendar/connections")
        return CalendarConnectionsResponse.model_validate(response)

    def list_calendars(self, connection_id: str) -> CalendarListResponse:
        """List calendars for a connection."""
        validate_id(connection_id, "connection")
        response = self._request(
            "GET", f"/calendar/connections/{connection_id}/calendars"
        )
        return CalendarListResponse.model_validate(response)


class AsyncCalendarResource(BaseAsyncResource):
    """Async resource for calendar operations."""

    async def list_events(
        self,
        *,
        connection_id: Optional[str] = None,
        calendar_id: Optional[str] = None,
        days: int = 7,
        limit: int = 50,
    ) -> CalendarEventsResponse:
        """List upcoming calendar events (async)."""
        params: Dict[str, Any] = {"days": days, "limit": limit}
        if connection_id is not None:
            params["connection_id"] = connection_id
        if calendar_id is not None:
            params["calendar_id"] = calendar_id
        response = await self._request("GET", "/calendar/events", params=params)
        return CalendarEventsResponse.model_validate(response)

    async def sync_to_memories(
        self,
        *,
        connection_id: str,
        calendar_id: Optional[str] = None,
        days_past: int = 30,
        days_future: int = 90,
        space_id: Optional[str] = None,
        pii_level: str = "minimal",
        tags: Optional[List[str]] = None,
    ) -> CalendarSyncResult:
        """Sync calendar events to memories (async)."""
        data = SyncCalendarParams(
            connection_id=connection_id,
            calendar_id=calendar_id,
            days_past=days_past,
            days_future=days_future,
            space_id=space_id,
            pii_level=pii_level,
            tags=tags,
        )
        response = await self._request(
            "POST", "/calendar/sync", json=data.model_dump(exclude_none=True)
        )
        return CalendarSyncResult.model_validate(response)

    async def list_connections(self) -> CalendarConnectionsResponse:
        """List calendar connections (async)."""
        response = await self._request("GET", "/calendar/connections")
        return CalendarConnectionsResponse.model_validate(response)

    async def list_calendars(self, connection_id: str) -> CalendarListResponse:
        """List calendars for a connection (async)."""
        validate_id(connection_id, "connection")
        response = await self._request(
            "GET", f"/calendar/connections/{connection_id}/calendars"
        )
        return CalendarListResponse.model_validate(response)
