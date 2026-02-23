"""Task-related types for Trix SDK."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseResponse


class TaskStatus(str):
    """Task status values."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"
    STALE = "stale"


class AssigneeType(str):
    """Assignee type values."""

    USER = "user"
    AGENT = "agent"


class TaskLinkType(str):
    """Task link relationship types."""

    DERIVED_FROM = "derived_from"
    PRODUCES = "produces"
    RELATED_TO = "related_to"
    REFERENCES = "references"


class Label(BaseResponse):
    """Task label."""

    id: str
    space_id: Optional[str] = None
    account_id: str
    name: str
    color: Optional[str] = None
    created_at: datetime


class Task(BaseResponse):
    """Task object."""

    id: str
    space_id: Optional[str] = None
    section_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    status: str = TaskStatus.PENDING
    priority: int = 0
    estimated_minutes: Optional[int] = None
    start_at: Optional[datetime] = None
    due_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    parent_task_id: Optional[str] = None
    child_order: int = 0
    created_by: Optional[str] = None
    assignee_id: Optional[str] = None
    assignee_type: Optional[str] = None
    delegated_by: Optional[str] = None
    delegated_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    labels: List[Label] = Field(default_factory=list)
    version: int = 1
    pinned_at: Optional[datetime] = None
    stale_after_days: Optional[int] = None
    last_activity_at: Optional[datetime] = None


class TaskCreate(BaseModel):
    """Request to create a task."""

    title: str
    space_id: str
    section_id: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    estimated_minutes: Optional[int] = None
    start_at: Optional[str] = None
    due_at: Optional[str] = None
    parent_task_id: Optional[str] = None
    assignee_id: Optional[str] = None
    assignee_type: Optional[str] = None
    labels: Optional[List[str]] = None
    stale_after_days: Optional[int] = None


class TaskUpdate(BaseModel):
    """Request to update a task."""

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    estimated_minutes: Optional[int] = None
    start_at: Optional[str] = None
    due_at: Optional[str] = None
    section_id: Optional[str] = None
    assignee_id: Optional[str] = None
    assignee_type: Optional[str] = None
    labels: Optional[List[str]] = None
    stale_after_days: Optional[int] = None
    version: Optional[int] = None


class TaskList(BaseResponse):
    """List of tasks with pagination."""

    data: List[Task]
    total: int
    limit: int
    offset: int
    has_more: bool = False


class TaskLink(BaseResponse):
    """Link between a task and another entity."""

    id: str
    task_id: str
    entity_type: str
    entity_id: str
    link_type: str
    created_at: datetime


class TaskLinkCreate(BaseModel):
    """Request to create a task link."""

    entity_type: str
    entity_id: str
    link_type: str = TaskLinkType.RELATED_TO


class SubtaskCreate(BaseModel):
    """Request to create a subtask."""

    title: str
    description: Optional[str] = None
    priority: Optional[int] = None
    estimated_minutes: Optional[int] = None
    due_at: Optional[str] = None
    assignee_id: Optional[str] = None
    assignee_type: Optional[str] = None
    labels: Optional[List[str]] = None


class BulkTaskCreate(BaseModel):
    """Single task in a bulk create request."""

    title: str
    space_id: Optional[str] = None
    section_id: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    estimated_minutes: Optional[int] = None
    start_at: Optional[str] = None
    due_at: Optional[str] = None
    parent_task_id: Optional[str] = None
    assignee_id: Optional[str] = None
    assignee_type: Optional[str] = None
    labels: Optional[List[str]] = None


class BulkTaskUpdate(BaseModel):
    """Single task in a bulk update request."""

    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    estimated_minutes: Optional[int] = None
    start_at: Optional[str] = None
    due_at: Optional[str] = None
    section_id: Optional[str] = None
    assignee_id: Optional[str] = None
    assignee_type: Optional[str] = None
    labels: Optional[List[str]] = None
    version: Optional[int] = None


class BulkTaskResult(BaseResponse):
    """Result of a bulk task operation."""

    success: int
    failed: int
    errors: List[Dict[str, Any]] = Field(default_factory=list)
    created: List[Task] = Field(default_factory=list)
    updated: List[Task] = Field(default_factory=list)


class BulkTaskFailure(BaseModel):
    """Details of a failed bulk task operation."""

    index: int
    id: Optional[str] = None
    error: str
    suggestion: Optional[str] = None


class BulkDeleteResult(BaseResponse):
    """Result of a bulk delete operation."""

    success: bool
    deleted_count: int = Field(alias="deletedCount")
    deleted_ids: List[str] = Field(default_factory=list, alias="deletedIds")
    failed: List[BulkTaskFailure] = Field(default_factory=list)


class SuggestedTask(BaseResponse):
    """A task with priority score for suggestions."""

    task: Task
    score: float
    reasons: List[str] = Field(default_factory=list)


class SuggestedTasksResult(BaseResponse):
    """Result of suggested tasks query."""

    data: List[SuggestedTask]
    context: Optional[str] = None


class TaskHandoffParams(BaseModel):
    """Parameters for handing off a task to another agent."""

    target_agent_id: str
    handoff_notes: Optional[str] = None
    checkpoint_data: Optional[Dict[str, Any]] = None


class TaskHandoffResult(BaseResponse):
    """Result of a task handoff operation."""

    handoff_id: str
    task: Task
    previous_assignee_id: Optional[str] = None
    new_assignee_id: str
    checkpoint_stored: bool = False
