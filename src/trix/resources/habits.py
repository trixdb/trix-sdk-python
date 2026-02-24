"""Habits resource for Trix SDK (ADR-034)."""

from typing import Any, Dict, List, Optional

from .base import BaseSyncResource
from ..types.habit import (
    CheckIn,
    CheckInResult,
    DueHabitsResult,
    Habit,
    HabitCreate,
    HabitHistoryResult,
    HabitList,
    HabitUpdate,
)
from ..utils.security import validate_id


class HabitsResource(BaseSyncResource):
    """Resource for managing personal habits.

    Example:
        >>> habit = client.habits.create(
        ...     name="Read for 30 minutes",
        ...     habit_type="duration",
        ...     target_value=30,
        ...     target_unit="minutes",
        ... )
        >>> client.habits.check_in(habit.id, value=45)
    """

    def create(
        self,
        name: str,
        description: Optional[str] = None,
        emoji: Optional[str] = None,
        color: Optional[str] = None,
        habit_type: Optional[str] = None,
        frequency: Optional[str] = None,
        frequency_days: Optional[List[int]] = None,
        frequency_interval: Optional[int] = None,
        target_value: Optional[float] = None,
        target_unit: Optional[str] = None,
        timezone: Optional[str] = None,
        space_id: Optional[str] = None,
        grace_days: Optional[int] = None,
    ) -> Habit:
        """Create a new habit."""
        data = HabitCreate(
            name=name,
            description=description,
            emoji=emoji,
            color=color,
            habit_type=habit_type,
            frequency=frequency,
            frequency_days=frequency_days,
            frequency_interval=frequency_interval,
            target_value=target_value,
            target_unit=target_unit,
            timezone=timezone,
            space_id=space_id,
            grace_days=grace_days,
        )
        response = self._request("POST", "/habits", json=data.model_dump(exclude_none=True))
        return Habit.model_validate(response)

    def list(
        self,
        status: Optional[str] = None,
        space_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> HabitList:
        """List habits with optional filtering."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if status is not None:
            params["status"] = status
        if space_id is not None:
            params["space_id"] = space_id
        response = self._request("GET", "/habits", params=params)
        return HabitList.model_validate(response)

    def get(self, habit_id: str) -> Habit:
        """Get a habit by ID."""
        validate_id(habit_id, "habit")
        response = self._request("GET", f"/habits/{habit_id}")
        return Habit.model_validate(response)

    def update(
        self,
        habit_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        emoji: Optional[str] = None,
        color: Optional[str] = None,
        target_value: Optional[float] = None,
        target_unit: Optional[str] = None,
        grace_days: Optional[int] = None,
    ) -> Habit:
        """Update a habit."""
        validate_id(habit_id, "habit")
        data = HabitUpdate(
            name=name,
            description=description,
            emoji=emoji,
            color=color,
            target_value=target_value,
            target_unit=target_unit,
            grace_days=grace_days,
        )
        response = self._request(
            "PATCH", f"/habits/{habit_id}", json=data.model_dump(exclude_none=True)
        )
        return Habit.model_validate(response)

    def delete(self, habit_id: str) -> None:
        """Archive a habit (soft delete)."""
        validate_id(habit_id, "habit")
        self._request("DELETE", f"/habits/{habit_id}")

    def check_in(
        self,
        habit_id: str,
        date: Optional[str] = None,
        value: Optional[float] = None,
        note: Optional[str] = None,
        source: Optional[str] = None,
    ) -> CheckInResult:
        """Record a habit completion."""
        validate_id(habit_id, "habit")
        data = CheckIn(date=date, value=value, note=note, source=source)
        response = self._request(
            "POST", f"/habits/{habit_id}/check-in", json=data.model_dump(exclude_none=True)
        )
        return CheckInResult.model_validate(response)

    def uncheck(self, habit_id: str, date: str) -> None:
        """Remove a habit completion for a date."""
        validate_id(habit_id, "habit")
        self._request("DELETE", f"/habits/{habit_id}/check-in/{date}")

    def history(
        self,
        habit_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 30,
    ) -> HabitHistoryResult:
        """Get completion history for a habit."""
        validate_id(habit_id, "habit")
        params: Dict[str, Any] = {"limit": limit}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        response = self._request("GET", f"/habits/{habit_id}/history", params=params)
        return HabitHistoryResult.model_validate(response)

    def due(self, date: Optional[str] = None) -> DueHabitsResult:
        """Get habits due on a date (defaults to today)."""
        params: Dict[str, Any] = {}
        if date is not None:
            params["date"] = date
        response = self._request("GET", "/habits/due", params=params if params else None)
        return DueHabitsResult.model_validate(response)

    def pause(self, habit_id: str) -> Habit:
        """Pause a habit."""
        validate_id(habit_id, "habit")
        response = self._request("POST", f"/habits/{habit_id}/pause")
        return Habit.model_validate(response)

    def resume(self, habit_id: str) -> Habit:
        """Resume a paused habit."""
        validate_id(habit_id, "habit")
        response = self._request("POST", f"/habits/{habit_id}/resume")
        return Habit.model_validate(response)
