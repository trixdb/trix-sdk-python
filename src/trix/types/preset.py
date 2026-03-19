"""Agent preset types for Trix SDK."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .base import BaseResponse


class AgentPreset(BaseResponse):
    """Agent execution preset configuration."""

    id: str
    account_id: Optional[str] = None
    name: str
    slug: str
    description: Optional[str] = None
    is_system: bool = False
    provider: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    step_overrides: Optional[Dict[str, Any]] = None
    tools_allowed: Optional[List[str]] = None
    tools_blocked: Optional[List[str]] = None
    memory_strategy: Optional[str] = None
    search_limit: Optional[int] = None
    context_window: Optional[int] = None
    retrieval_preset: Optional[str] = None
    guardrails: Optional[List[str]] = None
    autonomy_level: Optional[str] = None
    max_cost_per_run: Optional[float] = None
    max_budget_usd: Optional[float] = None
    budget_period: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AgentPresetCreate(BaseModel):
    """Request to create an agent preset."""

    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    step_overrides: Optional[Dict[str, Any]] = None
    tools_allowed: Optional[List[str]] = None
    tools_blocked: Optional[List[str]] = None
    memory_strategy: Optional[str] = None
    search_limit: Optional[int] = None
    context_window: Optional[int] = None
    retrieval_preset: Optional[str] = None
    guardrails: Optional[List[str]] = None
    autonomy_level: Optional[str] = None
    max_cost_per_run: Optional[float] = None
    max_budget_usd: Optional[float] = None
    budget_period: Optional[str] = None


class AgentPresetUpdate(BaseModel):
    """Request to update an agent preset."""

    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    step_overrides: Optional[Dict[str, Any]] = None
    tools_allowed: Optional[List[str]] = None
    tools_blocked: Optional[List[str]] = None
    memory_strategy: Optional[str] = None
    search_limit: Optional[int] = None
    context_window: Optional[int] = None
    retrieval_preset: Optional[str] = None
    guardrails: Optional[List[str]] = None
    autonomy_level: Optional[str] = None
    max_cost_per_run: Optional[float] = None
    max_budget_usd: Optional[float] = None
    budget_period: Optional[str] = None


class AgentPresetList(BaseResponse):
    """List of agent presets."""

    presets: List[AgentPreset]
