"""Agent-related types for Trix SDK."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import Field

from .base import BaseResponse
from .memory import Memory


class AgentSession(BaseResponse):
    """Agent conversation session."""

    session_id: str
    space_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    ended_at: Optional[datetime] = None
    summary: Optional[str] = None


class SessionMemory(BaseResponse):
    """Memory within an agent session."""

    id: str
    session_id: str
    content: str
    role: Optional[str] = None
    importance: Optional[float] = None
    created_at: datetime


class SessionMemoryList(BaseResponse):
    """List of session memories."""

    data: List[SessionMemory]
    total: int


class SessionList(BaseResponse):
    """List of agent sessions."""

    data: List[AgentSession]


class AgentContext(BaseResponse):
    """Contextual information for agent."""

    query: str
    memories: List[Memory]
    session_memories: List[SessionMemory]
    relevance_scores: Dict[str, float] = Field(default_factory=dict)
