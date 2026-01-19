"""Session-related types for Trix SDK."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .base import BaseResponse
from .enums import RetentionPolicy, SessionStatus, SessionType


class Session(BaseResponse):
    """CLI session for managing conversation/project/task contexts."""

    id: str
    account_id: str
    user_id: str
    created_by: str
    name: str
    description: Optional[str] = None
    type: SessionType
    status: SessionStatus
    space_id: Optional[str] = None
    origin_type: Optional[str] = None
    tags: Optional[List[str]] = None
    retention_policy: RetentionPolicy
    retention_days: Optional[int] = None
    summary: Optional[str] = None
    is_private: bool = False
    message_count: int = 0
    memory_count: int = 0
    metadata: Optional[Dict[str, Any]] = None
    created_at: str
    updated_at: str
    last_active_at: str
    paused_at: Optional[str] = None
    completed_at: Optional[str] = None
    archived_at: Optional[str] = None


class CreateSessionParams(BaseModel):
    """Parameters for creating a new session."""

    name: str
    description: Optional[str] = None
    type: SessionType = SessionType.CONVERSATION
    space_id: Optional[str] = None
    origin_type: Optional[str] = None
    tags: Optional[List[str]] = None
    retention_policy: RetentionPolicy = RetentionPolicy.PERMANENT
    retention_days: Optional[int] = None
    is_private: bool = False
    metadata: Optional[Dict[str, Any]] = None


class UpdateSessionParams(BaseModel):
    """Parameters for updating a session."""

    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    retention_policy: Optional[RetentionPolicy] = None
    retention_days: Optional[int] = None
    is_private: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None


class CompleteSessionParams(BaseModel):
    """Parameters for completing a session."""

    summary: Optional[str] = None


class SessionsResponse(BaseResponse):
    """Paginated list of sessions."""

    data: List[Session]
    total: int
    limit: int
    offset: int


class SessionStats(BaseResponse):
    """Session statistics."""

    total: int
    active: int
    paused: int
    completed: int
    archived: int
    by_type: Dict[str, int]
    total_messages: int
    total_memories: int
