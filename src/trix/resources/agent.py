"""Agent resource for Trix SDK."""

from typing import Any, Dict, List, Optional

from ..protocols import AsyncClientProtocol, SyncClientProtocol
from ..types import (
    AgentContext,
    AgentSession,
    SessionMemory,
    SessionMemoryList,
    SessionMessage,
    SessionList,
)
from ..utils.security import validate_id, validate_limit, validate_offset


class AgentResource:
    """Resource for agent sessions."""

    def __init__(self, client: SyncClientProtocol) -> None:
        """Initialize agent resource with client."""
        self._client = client

    def create_session(
        self,
        session_id: str,
        space_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AgentSession:
        """
        Create a new agent session.

        Args:
            session_id: Unique session identifier
            space_id: Optional space for session
            metadata: Additional session metadata

        Returns:
            Created session object

        Example:
            >>> session = client.agent.create_session(
            ...     session_id="chat_123",
            ...     metadata={"user_id": "user_456"}
            ... )
        """
        validate_id(session_id, "session")
        if space_id:
            validate_id(space_id, "space")
        data: Dict[str, Any] = {"session_id": session_id}
        if space_id:
            data["space_id"] = space_id
        if metadata:
            data["metadata"] = metadata

        response = self._client._request("POST", "/agent/sessions", json=data)
        return AgentSession.model_validate(response)

    def add_session_memory(
        self,
        session_id: str,
        content: str,
        role: Optional[str] = None,
        importance: Optional[float] = None,
    ) -> SessionMemory:
        """
        Add a memory to an agent session.

        Args:
            session_id: Session ID
            content: Memory content
            role: Role (e.g., "user", "assistant")
            importance: Importance score

        Returns:
            Created session memory

        Example:
            >>> memory = client.agent.add_session_memory(
            ...     session_id="chat_123",
            ...     content="User asked about Python",
            ...     role="user",
            ...     importance=0.8
            ... )
        """
        validate_id(session_id, "session")
        data: Dict[str, Any] = {"content": content}
        if role:
            data["role"] = role
        if importance is not None:
            data["importance"] = importance

        response = self._client._request(
            "POST", f"/agent/sessions/{session_id}/memories", json=data
        )
        return SessionMemory.model_validate(response)

    def add_session_message(
        self,
        session_id: str,
        content: str,
        role: str = "user",
    ) -> SessionMessage:
        """
        Add a simple message to an agent session.

        This is a simpler alternative to add_session_memory for basic chat messages.

        Args:
            session_id: Session ID
            content: Message content
            role: Role (e.g., "user", "assistant")

        Returns:
            Created session message with turn number

        Example:
            >>> msg = client.agent.add_session_message(
            ...     session_id="chat_123",
            ...     content="What is the weather today?",
            ...     role="user"
            ... )
        """
        validate_id(session_id, "session")
        data: Dict[str, Any] = {"content": content, "role": role}

        response = self._client._request("POST", f"/agent/sessions/{session_id}/message", json=data)
        return SessionMessage.model_validate(response)

    def get_session(self, session_id: str, limit: int = 100, offset: int = 0) -> SessionMemoryList:
        """
        Get memories from an agent session.

        Args:
            session_id: Session ID
            limit: Maximum number of memories (1-1000)
            offset: Offset for pagination (>= 0)

        Returns:
            List of session memories

        Example:
            >>> memories = client.agent.get_session("chat_123", limit=50)
        """
        validate_id(session_id, "session")
        validate_limit(limit)
        validate_offset(offset)
        params = {"limit": limit, "offset": offset}
        response = self._client._request("GET", f"/agent/sessions/{session_id}", params=params)
        return SessionMemoryList.model_validate(response)

    def list_sessions(self, limit: int = 100, space_id: Optional[str] = None) -> SessionList:
        """
        List agent sessions.

        Args:
            limit: Maximum number of sessions (1-1000)
            space_id: Filter by space

        Returns:
            List of sessions

        Example:
            >>> sessions = client.agent.list_sessions(limit=20)
        """
        validate_limit(limit)
        if space_id:
            validate_id(space_id, "space")
        params: Dict[str, Any] = {"limit": limit}
        if space_id:
            params["space_id"] = space_id

        response = self._client._request("GET", "/agent/sessions", params=params)
        return SessionList.model_validate(response)

    def get_context(
        self, query: str, session_id: Optional[str] = None, limit: int = 10
    ) -> AgentContext:
        """
        Get contextual information for an agent query.

        Args:
            query: Agent query
            session_id: Optional session for context
            limit: Maximum number of memories (1-100)

        Returns:
            Agent context with relevant memories

        Example:
            >>> context = client.agent.get_context(
            ...     query="Tell me about our previous discussions",
            ...     session_id="chat_123"
            ... )
        """
        validate_limit(limit, max_limit=100)
        if session_id:
            validate_id(session_id, "session")
        data: Dict[str, Any] = {"query": query, "limit": limit}
        if session_id:
            data["session_id"] = session_id

        response = self._client._request("POST", "/agent/context", json=data)
        return AgentContext.model_validate(response)

    def end_session(
        self,
        session_id: str,
        summary: Optional[str] = None,
        key_insights: Optional[List[str]] = None,
    ) -> AgentSession:
        """
        End an agent session with optional summary.

        Args:
            session_id: Session ID
            summary: Optional session summary
            key_insights: Optional list of key insights

        Returns:
            Updated session object

        Example:
            >>> session = client.agent.end_session(
            ...     session_id="chat_123",
            ...     summary="Discussion about Python best practices"
            ... )
        """
        validate_id(session_id, "session")
        data: Dict[str, Any] = {}
        if summary:
            data["summary"] = summary
        if key_insights:
            data["key_insights"] = key_insights

        response = self._client._request("POST", f"/agent/sessions/{session_id}/end", json=data)
        return AgentSession.model_validate(response)

    # ==================== ADR-112 P10 — Ingestion-pipeline triggers ====================

    def summarize_session(
        self, session_id: str, pipeline: Optional[str] = None
    ) -> Dict[str, Any]:
        """Enqueue a session_summary job for the given session.

        Returns the trigger response (`{session_id, enqueued, job_id, pipeline}`).
        """
        validate_id(session_id, "session")
        data: Dict[str, Any] = {}
        if pipeline:
            data["pipeline"] = pipeline
        return self._client._request(
            "POST", f"/agent/sessions/{session_id}/summarize", json=data
        )

    def trigger_mega_summary(
        self,
        scope_id: str,
        scope_type: str = "account",
        pipeline: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Enqueue a cross-session mega_summary generation job."""
        data: Dict[str, Any] = {"scope_id": scope_id, "scope_type": scope_type}
        if pipeline:
            data["pipeline"] = pipeline
        return self._client._request("POST", "/agent/mega-summary/trigger", json=data)

    def trigger_scoped_facts(
        self,
        scope_id: str,
        scope_type: str = "session",
        pipeline: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Enqueue a scoped_fact harvest job."""
        data: Dict[str, Any] = {"scope_id": scope_id, "scope_type": scope_type}
        if pipeline:
            data["pipeline"] = pipeline
        return self._client._request("POST", "/agent/scoped-facts/harvest", json=data)

    # ADR-109a — Account-level default pipeline preset
    # (Placed here pragmatically; pipeline-presets has no dedicated SDK
    # resource yet. Thin wrappers over /v1/pipeline-presets/_default.)

    def get_default_pipeline(self) -> Optional[str]:
        """Return the account's current default pipeline preset name (or None)."""
        resp = self._client._request("GET", "/pipeline-presets/_default")
        return resp.get("name") if isinstance(resp, dict) else None

    def set_default_pipeline(self, name: str) -> str:
        """Set the account default pipeline preset. Raises on unknown name."""
        resp = self._client._request(
            "POST", f"/pipeline-presets/{name}/set-default", json={}
        )
        return resp["name"] if isinstance(resp, dict) else name

    def clear_default_pipeline(self) -> None:
        """Clear the account default pipeline preset."""
        self._client._request("DELETE", "/pipeline-presets/_default")


class AsyncAgentResource:
    """Async resource for agent sessions."""

    def __init__(self, client: AsyncClientProtocol) -> None:
        """Initialize async agent resource with client."""
        self._client = client

    async def create_session(
        self,
        session_id: str,
        space_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AgentSession:
        """Create a new agent session (async)."""
        validate_id(session_id, "session")
        if space_id:
            validate_id(space_id, "space")
        data: Dict[str, Any] = {"session_id": session_id}
        if space_id:
            data["space_id"] = space_id
        if metadata:
            data["metadata"] = metadata

        response = await self._client._request("POST", "/agent/sessions", json=data)
        return AgentSession.model_validate(response)

    async def add_session_memory(
        self,
        session_id: str,
        content: str,
        role: Optional[str] = None,
        importance: Optional[float] = None,
    ) -> SessionMemory:
        """Add a memory to an agent session (async)."""
        validate_id(session_id, "session")
        data: Dict[str, Any] = {"content": content}
        if role:
            data["role"] = role
        if importance is not None:
            data["importance"] = importance

        response = await self._client._request(
            "POST", f"/agent/sessions/{session_id}/memories", json=data
        )
        return SessionMemory.model_validate(response)

    async def add_session_message(
        self,
        session_id: str,
        content: str,
        role: str = "user",
    ) -> SessionMessage:
        """Add a simple message to an agent session (async)."""
        validate_id(session_id, "session")
        data: Dict[str, Any] = {"content": content, "role": role}

        response = await self._client._request(
            "POST", f"/agent/sessions/{session_id}/message", json=data
        )
        return SessionMessage.model_validate(response)

    async def get_session(
        self, session_id: str, limit: int = 100, offset: int = 0
    ) -> SessionMemoryList:
        """Get memories from an agent session (async)."""
        validate_id(session_id, "session")
        validate_limit(limit)
        validate_offset(offset)
        params = {"limit": limit, "offset": offset}
        response = await self._client._request(
            "GET", f"/agent/sessions/{session_id}", params=params
        )
        return SessionMemoryList.model_validate(response)

    async def list_sessions(self, limit: int = 100, space_id: Optional[str] = None) -> SessionList:
        """List agent sessions (async)."""
        validate_limit(limit)
        if space_id:
            validate_id(space_id, "space")
        params: Dict[str, Any] = {"limit": limit}
        if space_id:
            params["space_id"] = space_id

        response = await self._client._request("GET", "/agent/sessions", params=params)
        return SessionList.model_validate(response)

    async def get_context(
        self, query: str, session_id: Optional[str] = None, limit: int = 10
    ) -> AgentContext:
        """Get contextual information for an agent query (async)."""
        validate_limit(limit, max_limit=100)
        if session_id:
            validate_id(session_id, "session")
        data: Dict[str, Any] = {"query": query, "limit": limit}
        if session_id:
            data["session_id"] = session_id

        response = await self._client._request("POST", "/agent/context", json=data)
        return AgentContext.model_validate(response)

    async def end_session(
        self,
        session_id: str,
        summary: Optional[str] = None,
        key_insights: Optional[List[str]] = None,
    ) -> AgentSession:
        """End an agent session with optional summary (async)."""
        validate_id(session_id, "session")
        data: Dict[str, Any] = {}
        if summary:
            data["summary"] = summary
        if key_insights:
            data["key_insights"] = key_insights

        response = await self._client._request(
            "POST", f"/agent/sessions/{session_id}/end", json=data
        )
        return AgentSession.model_validate(response)

    # ==================== ADR-112 P10 — Ingestion-pipeline triggers ====================

    async def summarize_session(
        self, session_id: str, pipeline: Optional[str] = None
    ) -> Dict[str, Any]:
        """Enqueue a session_summary job for the given session (async)."""
        validate_id(session_id, "session")
        data: Dict[str, Any] = {}
        if pipeline:
            data["pipeline"] = pipeline
        return await self._client._request(
            "POST", f"/agent/sessions/{session_id}/summarize", json=data
        )

    async def trigger_mega_summary(
        self,
        scope_id: str,
        scope_type: str = "account",
        pipeline: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Enqueue a cross-session mega_summary generation job (async)."""
        data: Dict[str, Any] = {"scope_id": scope_id, "scope_type": scope_type}
        if pipeline:
            data["pipeline"] = pipeline
        return await self._client._request("POST", "/agent/mega-summary/trigger", json=data)

    async def trigger_scoped_facts(
        self,
        scope_id: str,
        scope_type: str = "session",
        pipeline: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Enqueue a scoped_fact harvest job (async)."""
        data: Dict[str, Any] = {"scope_id": scope_id, "scope_type": scope_type}
        if pipeline:
            data["pipeline"] = pipeline
        return await self._client._request("POST", "/agent/scoped-facts/harvest", json=data)

    # ADR-109a — Account-level default pipeline preset (async)

    async def get_default_pipeline(self) -> Optional[str]:
        """Return the account's current default pipeline preset name (or None)."""
        resp = await self._client._request("GET", "/pipeline-presets/_default")
        return resp.get("name") if isinstance(resp, dict) else None

    async def set_default_pipeline(self, name: str) -> str:
        """Set the account default pipeline preset. Raises on unknown name."""
        resp = await self._client._request(
            "POST", f"/pipeline-presets/{name}/set-default", json={}
        )
        return resp["name"] if isinstance(resp, dict) else name

    async def clear_default_pipeline(self) -> None:
        """Clear the account default pipeline preset."""
        await self._client._request("DELETE", "/pipeline-presets/_default")
