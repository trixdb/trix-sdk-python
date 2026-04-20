"""ADR-121: Rich agent streaming event types for the Python SDK.

Mirrors the TypeScript SDK's AgentStreamEvent and the Go CLI's
AgentStreamEvent. Consumers iterate these as:

    async for event in client.agents.stream(opts):
        if event.type == "content_delta":
            print(event.delta, end="")
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field


class AgentMessageRef(BaseModel):
    """Reference to the assistant message being streamed."""

    id: str
    model: str


class AgentUsage(BaseModel):
    """Token usage statistics for a message."""

    input_tokens: int
    output_tokens: int
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    thinking_tokens: int = 0


# ── Event payloads ──────────────────────────────────────────


class MessageStartEvent(BaseModel):
    type: Literal["message_start"] = "message_start"
    message: AgentMessageRef
    usage: AgentUsage


class ContentDeltaEvent(BaseModel):
    type: Literal["content_delta"] = "content_delta"
    delta: str
    content_index: int = Field(alias="contentIndex", default=0)


class ThinkingDeltaEvent(BaseModel):
    type: Literal["thinking_delta"] = "thinking_delta"
    delta: str


class ToolUseStartEvent(BaseModel):
    type: Literal["tool_use_start"] = "tool_use_start"
    tool_use_id: str = Field(alias="toolUseId")
    name: str


class ToolUseDeltaEvent(BaseModel):
    type: Literal["tool_use_delta"] = "tool_use_delta"
    tool_use_id: str = Field(alias="toolUseId")
    input_delta: str = Field(alias="inputDelta")


class ToolResultEvent(BaseModel):
    type: Literal["tool_result"] = "tool_result"
    tool_use_id: str = Field(alias="toolUseId")
    output: Any = None
    is_error: bool = Field(alias="isError", default=False)


class MessageStopEvent(BaseModel):
    type: Literal["message_stop"] = "message_stop"
    stop_reason: str = Field(alias="stopReason")
    usage: AgentUsage


class MemoryRetrievedEvent(BaseModel):
    type: Literal["memory_retrieved"] = "memory_retrieved"
    memory_ids: List[str] = Field(alias="memoryIds")
    latency_ms: int = Field(alias="latencyMs")
    timed_out: bool = Field(alias="timedOut")


class MemoryCitedEvent(BaseModel):
    type: Literal["memory_cited"] = "memory_cited"
    memory_id: str = Field(alias="memoryId")


class MemoryConsolidatedEvent(BaseModel):
    type: Literal["memory_consolidated"] = "memory_consolidated"
    new_facts: int = Field(alias="newFacts")
    reinforced: int
    weakened: int


class StageStartEvent(BaseModel):
    type: Literal["stage_start"] = "stage_start"
    stage: str


class StageEndEvent(BaseModel):
    type: Literal["stage_end"] = "stage_end"
    stage: str
    status: Literal["ok", "error"]


class BudgetSpent(BaseModel):
    tokens: int
    usd: float


class BudgetStateEvent(BaseModel):
    type: Literal["budget_state"] = "budget_state"
    spent: BudgetSpent
    band: Literal["ok", "warn", "over"]
    pct: float


class BudgetWarningEvent(BaseModel):
    type: Literal["budget_warning"] = "budget_warning"
    remaining: Dict[str, Any]


class CacheReportEvent(BaseModel):
    type: Literal["cache_report"] = "cache_report"
    hit: bool
    hit_rate: float = Field(alias="hitRate")


class RetryAttemptEvent(BaseModel):
    type: Literal["retry_attempt"] = "retry_attempt"
    provider: str
    attempt: int
    reason: str


class PermissionRequestEvent(BaseModel):
    type: Literal["permission_request"] = "permission_request"
    tool: str
    input: Any = None


class WebSearchStatusEvent(BaseModel):
    type: Literal["web_search_status"] = "web_search_status"
    status: Literal["started", "done"]
    query: Optional[str] = None


class SourceItem(BaseModel):
    uri: str
    title: Optional[str] = None


class SourcesEvent(BaseModel):
    type: Literal["sources"] = "sources"
    sources: List[SourceItem]


class StopEvent(BaseModel):
    type: Literal["stop"] = "stop"
    reason: str


class StreamErrorEvent(BaseModel):
    type: Literal["error"] = "error"
    error: Dict[str, str]


AgentStreamEvent = Union[
    MessageStartEvent,
    ContentDeltaEvent,
    ThinkingDeltaEvent,
    ToolUseStartEvent,
    ToolUseDeltaEvent,
    ToolResultEvent,
    MessageStopEvent,
    MemoryRetrievedEvent,
    MemoryCitedEvent,
    MemoryConsolidatedEvent,
    StageStartEvent,
    StageEndEvent,
    BudgetStateEvent,
    BudgetWarningEvent,
    CacheReportEvent,
    RetryAttemptEvent,
    PermissionRequestEvent,
    WebSearchStatusEvent,
    SourcesEvent,
    StopEvent,
    StreamErrorEvent,
]

ALL_EVENT_TYPES = [
    "message_start",
    "content_delta",
    "thinking_delta",
    "tool_use_start",
    "tool_use_delta",
    "tool_result",
    "message_stop",
    "memory_retrieved",
    "memory_cited",
    "memory_consolidated",
    "stage_start",
    "stage_end",
    "budget_state",
    "budget_warning",
    "cache_report",
    "retry_attempt",
    "permission_request",
    "web_search_status",
    "sources",
    "stop",
    "error",
]


def parse_agent_event(data: Dict[str, Any]) -> AgentStreamEvent:
    """Parse a raw SSE JSON dict into a typed AgentStreamEvent."""
    event_type = data.get("type", "")
    _type_map = {
        "message_start": MessageStartEvent,
        "content_delta": ContentDeltaEvent,
        "thinking_delta": ThinkingDeltaEvent,
        "tool_use_start": ToolUseStartEvent,
        "tool_use_delta": ToolUseDeltaEvent,
        "tool_result": ToolResultEvent,
        "message_stop": MessageStopEvent,
        "memory_retrieved": MemoryRetrievedEvent,
        "memory_cited": MemoryCitedEvent,
        "memory_consolidated": MemoryConsolidatedEvent,
        "stage_start": StageStartEvent,
        "stage_end": StageEndEvent,
        "budget_state": BudgetStateEvent,
        "budget_warning": BudgetWarningEvent,
        "cache_report": CacheReportEvent,
        "retry_attempt": RetryAttemptEvent,
        "permission_request": PermissionRequestEvent,
        "web_search_status": WebSearchStatusEvent,
        "sources": SourcesEvent,
        "stop": StopEvent,
        "error": StreamErrorEvent,
    }
    cls = _type_map.get(event_type)
    if cls is None:
        raise ValueError(f"Unknown agent stream event type: {event_type}")
    return cls.model_validate(data)
