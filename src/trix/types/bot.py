"""Bot-related types for Trix SDK."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .base import BaseResponse


class BotTool(BaseModel):
    """Tool configuration for a bot."""

    server: str
    tools: Optional[List[str]] = None


class BotSpace(BaseModel):
    """Bot space access."""

    space_id: str
    permission: str = "read"
    space_name: Optional[str] = None


class BotTrigger(BaseModel):
    """Bot trigger definition."""

    id: str
    bot_id: str
    type: str
    cron_expression: Optional[str] = None
    timezone: Optional[str] = "UTC"
    event_types: Optional[List[str]] = None
    event_filter: Optional[Dict[str, Any]] = None
    enabled: bool = True
    last_triggered_at: Optional[datetime] = None
    created_at: datetime


class BotAction(BaseModel):
    """Action taken during a bot run."""

    tool: str
    args: Dict[str, Any] = {}
    result: Any = None


class Bot(BaseResponse):
    """Bot/agent definition."""

    id: str
    account_id: str
    persona_id: Optional[str] = None
    name: str
    slug: str
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    status: str = "active"
    model: str = "gpt-4.1"
    provider: str = "openai"
    temperature: float = 0.7
    max_tokens: int = 2048
    system_prompt: str
    memory_strategy: str = "search"
    search_limit: int = 20
    tools: List[BotTool] = []
    max_turns_per_run: int = 5
    require_approval: List[str] = []
    settings: Dict[str, Any] = {}
    metadata: Dict[str, Any] = {}
    is_builtin: bool = False
    spaces: Optional[List[BotSpace]] = None
    triggers: Optional[List[BotTrigger]] = None
    created_at: datetime
    updated_at: datetime


class BotRun(BaseResponse):
    """Bot execution run."""

    id: str
    bot_id: str
    account_id: str
    trigger_type: str
    trigger_id: Optional[str] = None
    status: str = "queued"
    input_message: Optional[str] = None
    input_context: Optional[Dict[str, Any]] = None
    output_message: Optional[str] = None
    output_actions: List[BotAction] = []
    memories_stored: int = 0
    memories_searched: int = 0
    llm_tokens_used: Optional[int] = None
    llm_model: Optional[str] = None
    duration_ms: Optional[int] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = {}
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime


class BotCreate(BaseModel):
    """Request to create a bot."""

    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    model: Optional[str] = None
    provider: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    system_prompt: str
    memory_strategy: Optional[str] = None
    search_limit: Optional[int] = None
    tools: Optional[List[BotTool]] = None
    max_turns_per_run: Optional[int] = None
    require_approval: Optional[List[str]] = None
    persona_id: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class BotUpdate(BaseModel):
    """Request to update a bot."""

    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    status: Optional[str] = None
    model: Optional[str] = None
    provider: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    system_prompt: Optional[str] = None
    memory_strategy: Optional[str] = None
    search_limit: Optional[int] = None
    tools: Optional[List[BotTool]] = None
    max_turns_per_run: Optional[int] = None
    require_approval: Optional[List[str]] = None
    persona_id: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class BotList(BaseResponse):
    """List of bots."""

    bots: List[Bot]


class BotRunList(BaseResponse):
    """List of bot runs."""

    runs: List[BotRun]


class BotAddSpace(BaseModel):
    """Request to add a space to a bot."""

    space_id: str
    permission: str = "read"


class BotTriggerCreate(BaseModel):
    """Request to create a bot trigger."""

    type: str
    cron_expression: Optional[str] = None
    timezone: Optional[str] = None
    event_types: Optional[List[str]] = None
    event_filter: Optional[Dict[str, Any]] = None
    enabled: Optional[bool] = None


class BotRunRequest(BaseModel):
    """Request to trigger a bot run."""

    message: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
