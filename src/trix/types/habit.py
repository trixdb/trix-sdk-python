"""Habit-related types for Trix SDK (ADR-034)."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseResponse


class HabitType(str):
    """Habit type values."""

    BOOLEAN = "boolean"
    NUMERIC = "numeric"
    DURATION = "duration"


class HabitFrequency(str):
    """Habit frequency values."""

    DAILY = "daily"
    WEEKLY = "weekly"
    SPECIFIC = "specific"
    INTERVAL = "interval"


class HabitStatus(str):
    """Habit status values."""

    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


class StreakInfo(BaseModel):
    """Streak information for a habit."""

    current: int = 0
    longest: int = 0
    last_completed_date: Optional[str] = None


class HabitCompletion(BaseResponse):
    """Habit completion record."""

    id: str
    habit_id: str
    completed_date: str
    value: Optional[float] = None
    note: Optional[str] = None
    source: str = "manual"
    created_at: datetime


class Habit(BaseResponse):
    """Habit object."""

    id: str
    account_id: str
    persona_id: Optional[str] = None
    space_id: Optional[str] = None
    name: str
    description: Optional[str] = None
    emoji: Optional[str] = None
    color: Optional[str] = None
    habit_type: str = HabitType.BOOLEAN
    frequency: str = HabitFrequency.DAILY
    frequency_days: Optional[List[int]] = None
    frequency_interval: Optional[int] = None
    target_value: Optional[float] = None
    target_unit: Optional[str] = None
    timezone: str = "UTC"
    grace_days: int = 1
    status: str = HabitStatus.ACTIVE
    streak: Optional[StreakInfo] = None
    paused_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class HabitCreate(BaseModel):
    """Parameters for creating a habit."""

    name: str
    description: Optional[str] = None
    emoji: Optional[str] = None
    color: Optional[str] = None
    habit_type: Optional[str] = None
    frequency: Optional[str] = None
    frequency_days: Optional[List[int]] = None
    frequency_interval: Optional[int] = None
    target_value: Optional[float] = None
    target_unit: Optional[str] = None
    timezone: Optional[str] = None
    space_id: Optional[str] = None
    grace_days: Optional[int] = None


class HabitUpdate(BaseModel):
    """Parameters for updating a habit."""

    name: Optional[str] = None
    description: Optional[str] = None
    emoji: Optional[str] = None
    color: Optional[str] = None
    target_value: Optional[float] = None
    target_unit: Optional[str] = None
    grace_days: Optional[int] = None


class CheckIn(BaseModel):
    """Parameters for checking in a habit."""

    date: Optional[str] = None
    value: Optional[float] = None
    note: Optional[str] = None
    source: Optional[str] = None


class HabitList(BaseModel):
    """Paginated list of habits."""

    habits: List[Habit] = Field(default_factory=list)
    pagination: Dict[str, Any] = Field(default_factory=dict)


class CheckInResult(BaseModel):
    """Result of a check-in operation."""

    completion: HabitCompletion
    streak: StreakInfo


class HabitHistoryResult(BaseModel):
    """Habit history with completions."""

    completions: List[HabitCompletion] = Field(default_factory=list)
    streak: StreakInfo


class DueHabitsResult(BaseModel):
    """Result of due habits query."""

    habits: List[Habit] = Field(default_factory=list)
    date: str


class BestDay(BaseModel):
    """Best day of week for completions."""

    day: str
    count: int


class WeeklyTrendEntry(BaseModel):
    """Weekly completion count."""

    week_start: str
    count: int


class HabitAnalytics(BaseModel):
    """Analytics for a single habit."""

    habit_id: str
    completion_rate: Optional[float] = None
    current_streak: int = 0
    longest_streak: int = 0
    total_completions: int = 0
    best_day: Optional[BestDay] = None
    consistency_score: float = 0
    weekly_trend: List[WeeklyTrendEntry] = Field(default_factory=list)
