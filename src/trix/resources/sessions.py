"""Sessions resource for Trix SDK."""

from typing import Any, Dict, List, Optional

from .base import BaseAsyncResource, BaseSyncResource
from ..types import (
    Session,
    SessionsResponse,
    SessionType,
    SessionStatus,
    RetentionPolicy,
    CreateSessionParams,
    UpdateSessionParams,
    CompleteSessionParams,
)
from ..utils.security import validate_id


class SessionsResource(BaseSyncResource):
    """Resource for managing CLI sessions.

    Sessions provide lifecycle management for conversations, projects, and tasks
    with features like pause/resume, completion tracking, and retention policies.

    Example:
        >>> # Create a session
        >>> session = client.sessions.create(
        ...     name="My Project",
        ...     type=SessionType.PROJECT,
        ...     tags=["work"]
        ... )
        >>>
        >>> # List all sessions
        >>> sessions = client.sessions.list()
        >>>
        >>> # Get active sessions
        >>> active = client.sessions.get_active()
        >>>
        >>> # Pause a session
        >>> client.sessions.pause("sess_123")
        >>>
        >>> # Complete a session
        >>> client.sessions.complete("sess_123", summary="Project completed")
    """

    def create(
        self,
        name: str,
        description: Optional[str] = None,
        type: SessionType = SessionType.CONVERSATION,
        space_id: Optional[str] = None,
        origin_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        retention_policy: RetentionPolicy = RetentionPolicy.PERMANENT,
        retention_days: Optional[int] = None,
        is_private: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Session:
        """Create a new session.

        Args:
            name: Session name (required).
            description: Optional session description.
            type: Session type (default: conversation).
            space_id: Optional space to associate with.
            origin_type: Optional origin context.
            tags: List of tags for categorization.
            retention_policy: Retention policy (default: permanent).
            retention_days: Days to retain data (for auto_delete policy).
            is_private: Whether session is private to user.
            metadata: Additional custom metadata.

        Returns:
            Created session object.

        Example:
            >>> session = client.sessions.create(
            ...     name="Sprint Planning",
            ...     type=SessionType.PROJECT,
            ...     tags=["agile", "planning"],
            ...     retention_policy=RetentionPolicy.AUTO_DELETE,
            ...     retention_days=90
            ... )
        """
        data = CreateSessionParams(
            name=name,
            description=description,
            type=type,
            space_id=space_id,
            origin_type=origin_type,
            tags=tags,
            retention_policy=retention_policy,
            retention_days=retention_days,
            is_private=is_private,
            metadata=metadata,
        )
        response = self._request(
            "POST",
            "/cli-sessions",
            json=data.model_dump(exclude_none=True)
        )
        return Session.model_validate(response)

    def list(
        self,
        status: Optional[SessionStatus] = None,
        type: Optional[SessionType] = None,
        space_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        search: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> SessionsResponse:
        """List sessions with optional filtering.

        Args:
            status: Filter by session status.
            type: Filter by session type.
            space_id: Filter by space ID.
            tags: Filter by tags.
            search: Search query for name/description.
            limit: Maximum number of results (default: 100).
            offset: Offset for pagination (default: 0).

        Returns:
            Paginated list of sessions.

        Example:
            >>> # Get all active sessions
            >>> sessions = client.sessions.list(status=SessionStatus.ACTIVE)
            >>>
            >>> # Get project sessions with specific tags
            >>> sessions = client.sessions.list(
            ...     type=SessionType.PROJECT,
            ...     tags=["work"],
            ...     limit=50
            ... )
        """
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status.value
        if type:
            params["type"] = type.value
        if space_id:
            params["space_id"] = space_id
        if tags:
            params["tags"] = ",".join(tags)
        if search:
            params["search"] = search

        response = self._request("GET", "/cli-sessions", params=params)
        return SessionsResponse.model_validate(response)

    def get(self, id: str) -> Session:
        """Get a session by ID.

        Args:
            id: Session ID.

        Returns:
            Session object.

        Raises:
            ValidationError: If ID format is invalid.
            NotFoundError: If session doesn't exist.

        Example:
            >>> session = client.sessions.get("sess_123")
            >>> print(f"{session.name}: {session.message_count} messages")
        """
        validate_id(id, "session")
        response = self._request("GET", f"/cli-sessions/{id}")
        return Session.model_validate(response)

    def update(
        self,
        id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        retention_policy: Optional[RetentionPolicy] = None,
        retention_days: Optional[int] = None,
        is_private: Optional[bool] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Session:
        """Update a session.

        Args:
            id: Session ID.
            name: New session name.
            description: New description.
            tags: New tags list.
            retention_policy: New retention policy.
            retention_days: New retention days.
            is_private: New privacy setting.
            metadata: New metadata.

        Returns:
            Updated session object.

        Raises:
            ValidationError: If ID format is invalid.
            NotFoundError: If session doesn't exist.

        Example:
            >>> session = client.sessions.update(
            ...     "sess_123",
            ...     name="Updated Name",
            ...     tags=["updated", "important"]
            ... )
        """
        validate_id(id, "session")
        data = UpdateSessionParams(
            name=name,
            description=description,
            tags=tags,
            retention_policy=retention_policy,
            retention_days=retention_days,
            is_private=is_private,
            metadata=metadata,
        )
        response = self._request(
            "PATCH",
            f"/cli-sessions/{id}",
            json=data.model_dump(exclude_none=True)
        )
        return Session.model_validate(response)

    def delete(self, id: str) -> None:
        """Delete a session.

        Args:
            id: Session ID.

        Raises:
            ValidationError: If ID format is invalid.
            NotFoundError: If session doesn't exist.

        Example:
            >>> client.sessions.delete("sess_123")
        """
        validate_id(id, "session")
        self._request("DELETE", f"/cli-sessions/{id}")

    def get_active(self) -> SessionsResponse:
        """Get all active sessions.

        Returns:
            List of active sessions.

        Example:
            >>> active_sessions = client.sessions.get_active()
            >>> for session in active_sessions.data:
            ...     print(f"{session.name}: {session.status}")
        """
        response = self._request("GET", "/cli-sessions/active")
        return SessionsResponse.model_validate(response)

    def pause(self, id: str) -> Session:
        """Pause an active session.

        Args:
            id: Session ID.

        Returns:
            Updated session object with paused status.

        Raises:
            ValidationError: If ID format is invalid.
            NotFoundError: If session doesn't exist.

        Example:
            >>> session = client.sessions.pause("sess_123")
            >>> assert session.status == SessionStatus.PAUSED
        """
        validate_id(id, "session")
        response = self._request("POST", f"/cli-sessions/{id}/pause")
        return Session.model_validate(response)

    def resume(self, id: str) -> Session:
        """Resume a paused session.

        Args:
            id: Session ID.

        Returns:
            Updated session object with active status.

        Raises:
            ValidationError: If ID format is invalid.
            NotFoundError: If session doesn't exist.

        Example:
            >>> session = client.sessions.resume("sess_123")
            >>> assert session.status == SessionStatus.ACTIVE
        """
        validate_id(id, "session")
        response = self._request("POST", f"/cli-sessions/{id}/resume")
        return Session.model_validate(response)

    def complete(
        self,
        id: str,
        summary: Optional[str] = None,
    ) -> Session:
        """Complete a session.

        Args:
            id: Session ID.
            summary: Optional completion summary.

        Returns:
            Updated session object with completed status.

        Raises:
            ValidationError: If ID format is invalid.
            NotFoundError: If session doesn't exist.

        Example:
            >>> session = client.sessions.complete(
            ...     "sess_123",
            ...     summary="Project completed successfully with all goals met"
            ... )
            >>> assert session.status == SessionStatus.COMPLETED
        """
        validate_id(id, "session")
        data = CompleteSessionParams(summary=summary)
        response = self._request(
            "POST",
            f"/cli-sessions/{id}/complete",
            json=data.model_dump(exclude_none=True)
        )
        return Session.model_validate(response)

    def get_memories(
        self,
        id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Get memories associated with a session.

        Args:
            id: Session ID.
            limit: Maximum number of results (default: 100).
            offset: Offset for pagination (default: 0).

        Returns:
            Dictionary containing list of memories with pagination info.

        Raises:
            ValidationError: If ID format is invalid.
            NotFoundError: If session doesn't exist.

        Example:
            >>> memories = client.sessions.get_memories("sess_123")
            >>> for memory in memories["data"]:
            ...     print(memory["content"])
        """
        validate_id(id, "session")
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        response = self._request(
            "GET",
            f"/cli-sessions/{id}/memories",
            params=params
        )
        return response


class AsyncSessionsResource(BaseAsyncResource):
    """Async resource for managing CLI sessions.

    Sessions provide lifecycle management for conversations, projects, and tasks
    with features like pause/resume, completion tracking, and retention policies.

    Example:
        >>> # Create a session
        >>> session = await client.sessions.create(
        ...     name="My Project",
        ...     type=SessionType.PROJECT
        ... )
        >>>
        >>> # List all sessions
        >>> sessions = await client.sessions.list()
        >>>
        >>> # Complete a session
        >>> await client.sessions.complete("sess_123")
    """

    async def create(
        self,
        name: str,
        description: Optional[str] = None,
        type: SessionType = SessionType.CONVERSATION,
        space_id: Optional[str] = None,
        origin_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        retention_policy: RetentionPolicy = RetentionPolicy.PERMANENT,
        retention_days: Optional[int] = None,
        is_private: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Session:
        """Create a new session (async).

        Args:
            name: Session name (required).
            description: Optional session description.
            type: Session type (default: conversation).
            space_id: Optional space to associate with.
            origin_type: Optional origin context.
            tags: List of tags for categorization.
            retention_policy: Retention policy (default: permanent).
            retention_days: Days to retain data (for auto_delete policy).
            is_private: Whether session is private to user.
            metadata: Additional custom metadata.

        Returns:
            Created session object.
        """
        data = CreateSessionParams(
            name=name,
            description=description,
            type=type,
            space_id=space_id,
            origin_type=origin_type,
            tags=tags,
            retention_policy=retention_policy,
            retention_days=retention_days,
            is_private=is_private,
            metadata=metadata,
        )
        response = await self._request(
            "POST",
            "/cli-sessions",
            json=data.model_dump(exclude_none=True)
        )
        return Session.model_validate(response)

    async def list(
        self,
        status: Optional[SessionStatus] = None,
        type: Optional[SessionType] = None,
        space_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        search: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> SessionsResponse:
        """List sessions with optional filtering (async).

        Args:
            status: Filter by session status.
            type: Filter by session type.
            space_id: Filter by space ID.
            tags: Filter by tags.
            search: Search query for name/description.
            limit: Maximum number of results (default: 100).
            offset: Offset for pagination (default: 0).

        Returns:
            Paginated list of sessions.
        """
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status.value
        if type:
            params["type"] = type.value
        if space_id:
            params["space_id"] = space_id
        if tags:
            params["tags"] = ",".join(tags)
        if search:
            params["search"] = search

        response = await self._request("GET", "/cli-sessions", params=params)
        return SessionsResponse.model_validate(response)

    async def get(self, id: str) -> Session:
        """Get a session by ID (async).

        Args:
            id: Session ID.

        Returns:
            Session object.
        """
        validate_id(id, "session")
        response = await self._request("GET", f"/cli-sessions/{id}")
        return Session.model_validate(response)

    async def update(
        self,
        id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        retention_policy: Optional[RetentionPolicy] = None,
        retention_days: Optional[int] = None,
        is_private: Optional[bool] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Session:
        """Update a session (async).

        Args:
            id: Session ID.
            name: New session name.
            description: New description.
            tags: New tags list.
            retention_policy: New retention policy.
            retention_days: New retention days.
            is_private: New privacy setting.
            metadata: New metadata.

        Returns:
            Updated session object.
        """
        validate_id(id, "session")
        data = UpdateSessionParams(
            name=name,
            description=description,
            tags=tags,
            retention_policy=retention_policy,
            retention_days=retention_days,
            is_private=is_private,
            metadata=metadata,
        )
        response = await self._request(
            "PATCH",
            f"/cli-sessions/{id}",
            json=data.model_dump(exclude_none=True)
        )
        return Session.model_validate(response)

    async def delete(self, id: str) -> None:
        """Delete a session (async).

        Args:
            id: Session ID.
        """
        validate_id(id, "session")
        await self._request("DELETE", f"/cli-sessions/{id}")

    async def get_active(self) -> SessionsResponse:
        """Get all active sessions (async).

        Returns:
            List of active sessions.
        """
        response = await self._request("GET", "/cli-sessions/active")
        return SessionsResponse.model_validate(response)

    async def pause(self, id: str) -> Session:
        """Pause an active session (async).

        Args:
            id: Session ID.

        Returns:
            Updated session object with paused status.
        """
        validate_id(id, "session")
        response = await self._request("POST", f"/cli-sessions/{id}/pause")
        return Session.model_validate(response)

    async def resume(self, id: str) -> Session:
        """Resume a paused session (async).

        Args:
            id: Session ID.

        Returns:
            Updated session object with active status.
        """
        validate_id(id, "session")
        response = await self._request("POST", f"/cli-sessions/{id}/resume")
        return Session.model_validate(response)

    async def complete(
        self,
        id: str,
        summary: Optional[str] = None,
    ) -> Session:
        """Complete a session (async).

        Args:
            id: Session ID.
            summary: Optional completion summary.

        Returns:
            Updated session object with completed status.
        """
        validate_id(id, "session")
        data = CompleteSessionParams(summary=summary)
        response = await self._request(
            "POST",
            f"/cli-sessions/{id}/complete",
            json=data.model_dump(exclude_none=True)
        )
        return Session.model_validate(response)

    async def get_memories(
        self,
        id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Get memories associated with a session (async).

        Args:
            id: Session ID.
            limit: Maximum number of results (default: 100).
            offset: Offset for pagination (default: 0).

        Returns:
            Dictionary containing list of memories with pagination info.
        """
        validate_id(id, "session")
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        response = await self._request(
            "GET",
            f"/cli-sessions/{id}/memories",
            params=params
        )
        return response
