"""Workflow-related types for Trix SDK."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .base import BaseResponse


class WorkflowCreate(BaseModel):
    """Request to create a workflow."""

    name: str
    description: Optional[str] = None
    space_id: Optional[str] = None
    steps: List[Dict[str, Any]] = []
    trigger: Optional[Dict[str, Any]] = None


class WorkflowUpdate(BaseModel):
    """Request to update a workflow."""

    version: int
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    trigger: Optional[Dict[str, Any]] = None
    steps: Optional[List[Dict[str, Any]]] = None


class Workflow(BaseResponse):
    """Workflow object - represents an automation workflow."""

    id: str
    account_id: str
    space_id: Optional[str] = None
    name: str
    description: Optional[str] = None
    trigger: Optional[Dict[str, Any]] = None
    steps: List[Dict[str, Any]] = []
    status: str
    version: int
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: str
    updated_at: str


class WorkflowList(BaseResponse):
    """List of workflows with pagination."""

    workflows: List[Workflow]
    total: int = 0
    limit: int = 20
    offset: int = 0


class WorkflowRun(BaseResponse):
    """A single workflow run execution."""

    id: str
    workflow_id: str
    account_id: str
    status: str
    triggered_by: Optional[str] = None
    triggered_by_id: Optional[str] = None
    step_states: Optional[Dict[str, Any]] = None
    input: Optional[Dict[str, Any]] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None
    created_at: str


class WorkflowRunList(BaseResponse):
    """List of workflow runs with pagination."""

    runs: List[WorkflowRun]
    total: int = 0
    limit: int = 20
    offset: int = 0


class WorkflowTrigger(BaseResponse):
    """A workflow trigger configuration."""

    id: str
    workflow_id: str
    type: str
    cron_expression: Optional[str] = None
    timezone: Optional[str] = None
    event_types: Optional[List[str]] = None
    event_filter: Optional[Dict[str, Any]] = None
    enabled: bool = True
    last_triggered_at: Optional[str] = None
    created_at: str


class TriggerCreate(BaseModel):
    """Request to create a workflow trigger."""

    type: str
    cron_expression: Optional[str] = None
    timezone: Optional[str] = None
    event_types: Optional[List[str]] = None
    event_filter: Optional[Dict[str, Any]] = None
    enabled: Optional[bool] = None


class TriggerUpdate(BaseModel):
    """Request to update a workflow trigger."""

    cron_expression: Optional[str] = None
    timezone: Optional[str] = None
    event_types: Optional[List[str]] = None
    event_filter: Optional[Dict[str, Any]] = None
    enabled: Optional[bool] = None
