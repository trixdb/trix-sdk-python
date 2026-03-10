"""Bot run step types for streaming SSE events."""

from typing import Any, Dict, Optional

from pydantic import BaseModel

from .base import BaseResponse


class BotRunStep(BaseResponse):
    """A single step event from a bot run stream."""

    event: str
    run_id: Optional[str] = None
    step_index: Optional[int] = None
    tool: Optional[str] = None
    args: Optional[Dict[str, Any]] = None
    result: Optional[Any] = None
    message: Optional[str] = None
    status: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}


class BotRunStreamRequest(BaseModel):
    """Request to trigger a streaming bot run."""

    message: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    stream: bool = True
