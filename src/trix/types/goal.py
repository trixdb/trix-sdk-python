"""Goal-related types for Trix SDK (ADR-035)."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .base import BaseResponse


class GoalContributor(BaseModel):
    """A contributor to a goal."""

    goal_id: str
    persona_id: str
    persona_name: Optional[str] = None
    role: str = "contributor"
    can_update_progress: bool = False
    added_at: datetime


class Goal(BaseResponse):
    """Goal object - represents a structured objective."""

    id: str
    account_id: str
    space_id: Optional[str] = None
    persona_id: Optional[str] = None
    parent_goal_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    goal_type: str  # outcome, process, learning
    status: str  # draft, active, completed, paused, abandoned
    visibility: str  # private, space, account
    progress: float
    progress_type: str  # manual, key_results, tasks, habits
    target_value: Optional[float] = None
    current_value: Optional[float] = None
    target_unit: Optional[str] = None
    priority: int
    weight: float
    depth: int
    is_key_result: bool = False
    color: Optional[str] = None
    icon: Optional[str] = None
    start_date: Optional[str] = None
    target_date: Optional[str] = None
    completed_at: Optional[str] = None
    version: int
    contributors: Optional[List[GoalContributor]] = None
    created_at: str
    updated_at: str


class GoalCreate(BaseModel):
    """Request to create a goal."""

    title: str
    description: Optional[str] = None
    goal_type: Optional[str] = None
    visibility: Optional[str] = None
    progress_type: Optional[str] = None
    target_value: Optional[float] = None
    target_unit: Optional[str] = None
    priority: Optional[int] = None
    weight: Optional[float] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    start_date: Optional[str] = None
    target_date: Optional[str] = None
    parent_goal_id: Optional[str] = None
    space_id: Optional[str] = None
    persona_id: Optional[str] = None


class GoalUpdate(BaseModel):
    """Request to update a goal."""

    title: Optional[str] = None
    description: Optional[str] = None
    goal_type: Optional[str] = None
    visibility: Optional[str] = None
    progress_type: Optional[str] = None
    target_value: Optional[float] = None
    target_unit: Optional[str] = None
    priority: Optional[int] = None
    weight: Optional[float] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    start_date: Optional[str] = None
    target_date: Optional[str] = None
    parent_goal_id: Optional[str] = None


class GoalList(BaseResponse):
    """List of goals with pagination."""

    goals: List[Goal]
    total: int = 0
    limit: int = 50
    offset: int = 0


class GoalProgressUpdate(BaseModel):
    """Request to update goal progress."""

    progress: float
    source: Optional[str] = None
    persona_id: Optional[str] = None
    note: Optional[str] = None


class GoalStatusTransition(BaseModel):
    """Request to transition goal status."""

    status: str


class GoalContributorCreate(BaseModel):
    """Request to add a contributor to a goal."""

    persona_id: str
    role: Optional[str] = None
    can_update_progress: Optional[bool] = None


class GoalContributorUpdate(BaseModel):
    """Request to update a goal contributor."""

    role: Optional[str] = None
    can_update_progress: Optional[bool] = None


class ProgressHistoryEntry(BaseResponse):
    """A single progress history entry."""

    id: str
    goal_id: str
    previous_progress: float
    new_progress: float
    source: str
    persona_id: Optional[str] = None
    note: Optional[str] = None
    created_at: str


class ProgressHistoryList(BaseResponse):
    """List of progress history entries with pagination."""

    entries: List[ProgressHistoryEntry]
    total: int = 0
    limit: int = 50
    offset: int = 0


class KeyResultCreate(BaseModel):
    """Parameters for creating a key result."""

    title: str
    description: Optional[str] = None
    goal_type: str = "outcome"
    visibility: str = "private"
    progress_type: str = "manual"
    target_value: Optional[float] = None
    target_unit: Optional[str] = None
    priority: int = 0
    weight: float = 1.0
    color: Optional[str] = None
    icon: Optional[str] = None
    start_date: Optional[str] = None
    target_date: Optional[str] = None


class PaceAnalysis(BaseModel):
    """Pace analysis result for a goal."""

    goal_id: str
    progress: float
    expected: Optional[float] = None
    delta: Optional[float] = None
    status: str  # on_track, behind, ahead, overdue, no_timeline


class GoalMemoryLink(BaseModel):
    """A link between a goal and a memory."""

    goal_id: str
    memory_id: str
    link_type: str = "related"
    content: Optional[str] = None
    type: Optional[str] = None
    tags: Optional[List[str]] = None
    memory_created_at: Optional[str] = None
    created_at: Optional[str] = None


class GoalMemoryListResponse(BaseResponse):
    """List of goal-memory links with pagination."""

    memories: List[GoalMemoryLink]
    total: int
    limit: int = 20
    offset: int = 0
