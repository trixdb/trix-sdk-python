"""Async goals resource for Trix SDK (ADR-035)."""

from typing import Any, Dict, List, Optional

from .base import BaseAsyncResource
from ..types.goal import (
    Goal,
    GoalContributor,
    GoalContributorCreate,
    GoalContributorUpdate,
    GoalCreate,
    GoalList,
    GoalMemoryLink,
    GoalMemoryListResponse,
    GoalProgressUpdate,
    GoalStatusTransition,
    GoalUpdate,
    KeyResultCreate,
    PaceAnalysis,
    ProgressHistoryList,
)
from ..utils.security import validate_id


class AsyncGoalsResource(BaseAsyncResource):
    """Async resource for managing goals.

    Example:
        >>> goal = await client.goals.create(
        ...     title="Ship MVP",
        ...     goal_type="outcome",
        ...     target_date="2026-06-01",
        ... )
        >>> await client.goals.update_progress(goal.id, progress=0.5)
    """

    async def create(
        self,
        title: str,
        description: Optional[str] = None,
        goal_type: Optional[str] = None,
        visibility: Optional[str] = None,
        progress_type: Optional[str] = None,
        target_value: Optional[float] = None,
        target_unit: Optional[str] = None,
        priority: Optional[int] = None,
        weight: Optional[float] = None,
        color: Optional[str] = None,
        icon: Optional[str] = None,
        start_date: Optional[str] = None,
        target_date: Optional[str] = None,
        parent_goal_id: Optional[str] = None,
        space_id: Optional[str] = None,
        persona_id: Optional[str] = None,
    ) -> Goal:
        """Create a new goal (async)."""
        data = GoalCreate(
            title=title,
            description=description,
            goal_type=goal_type,
            visibility=visibility,
            progress_type=progress_type,
            target_value=target_value,
            target_unit=target_unit,
            priority=priority,
            weight=weight,
            color=color,
            icon=icon,
            start_date=start_date,
            target_date=target_date,
            parent_goal_id=parent_goal_id,
            space_id=space_id,
            persona_id=persona_id,
        )
        response = await self._request("POST", "/goals", json=data.model_dump(exclude_none=True))
        return Goal.model_validate(response)

    async def list(
        self,
        status: Optional[str] = None,
        goal_type: Optional[str] = None,
        parent_goal_id: Optional[str] = None,
        space_id: Optional[str] = None,
        persona_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> GoalList:
        """List goals with optional filtering (async)."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if status is not None:
            params["status"] = status
        if goal_type is not None:
            params["goalType"] = goal_type
        if parent_goal_id is not None:
            params["parentGoalId"] = parent_goal_id
        if space_id is not None:
            params["spaceId"] = space_id
        if persona_id is not None:
            params["personaId"] = persona_id
        response = await self._request("GET", "/goals", params=params)
        return GoalList.model_validate(response)

    async def get(self, goal_id: str) -> Goal:
        """Get a goal by ID (async)."""
        validate_id(goal_id, "goal")
        response = await self._request("GET", f"/goals/{goal_id}")
        return Goal.model_validate(response)

    async def update(
        self,
        goal_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        goal_type: Optional[str] = None,
        visibility: Optional[str] = None,
        progress_type: Optional[str] = None,
        target_value: Optional[float] = None,
        target_unit: Optional[str] = None,
        priority: Optional[int] = None,
        weight: Optional[float] = None,
        color: Optional[str] = None,
        icon: Optional[str] = None,
        start_date: Optional[str] = None,
        target_date: Optional[str] = None,
        parent_goal_id: Optional[str] = None,
    ) -> Goal:
        """Update a goal (async)."""
        validate_id(goal_id, "goal")
        data = GoalUpdate(
            title=title,
            description=description,
            goal_type=goal_type,
            visibility=visibility,
            progress_type=progress_type,
            target_value=target_value,
            target_unit=target_unit,
            priority=priority,
            weight=weight,
            color=color,
            icon=icon,
            start_date=start_date,
            target_date=target_date,
            parent_goal_id=parent_goal_id,
        )
        response = await self._request(
            "PATCH", f"/goals/{goal_id}", json=data.model_dump(exclude_none=True)
        )
        return Goal.model_validate(response)

    async def delete(self, goal_id: str) -> None:
        """Delete a goal (async)."""
        validate_id(goal_id, "goal")
        await self._request("DELETE", f"/goals/{goal_id}")

    async def update_progress(
        self,
        goal_id: str,
        progress: float,
        source: Optional[str] = None,
        persona_id: Optional[str] = None,
        note: Optional[str] = None,
    ) -> Goal:
        """Update goal progress (async)."""
        validate_id(goal_id, "goal")
        data = GoalProgressUpdate(
            progress=progress,
            source=source,
            persona_id=persona_id,
            note=note,
        )
        response = await self._request(
            "POST", f"/goals/{goal_id}/progress", json=data.model_dump(exclude_none=True)
        )
        return Goal.model_validate(response)

    async def transition_status(self, goal_id: str, status: str) -> Goal:
        """Transition goal status (async)."""
        validate_id(goal_id, "goal")
        data = GoalStatusTransition(status=status)
        response = await self._request(
            "POST", f"/goals/{goal_id}/status", json=data.model_dump(exclude_none=True)
        )
        return Goal.model_validate(response)

    async def get_progress_history(
        self,
        goal_id: str,
        limit: int = 50,
        offset: int = 0,
    ) -> ProgressHistoryList:
        """Get progress history for a goal (async)."""
        validate_id(goal_id, "goal")
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        response = await self._request("GET", f"/goals/{goal_id}/progress-history", params=params)
        return ProgressHistoryList.model_validate(response)

    async def list_contributors(self, goal_id: str) -> List[GoalContributor]:
        """List contributors for a goal (async)."""
        validate_id(goal_id, "goal")
        response = await self._request("GET", f"/goals/{goal_id}/contributors")
        return [GoalContributor.model_validate(c) for c in response]

    async def add_contributor(
        self,
        goal_id: str,
        persona_id: str,
        role: Optional[str] = None,
        can_update_progress: Optional[bool] = None,
    ) -> GoalContributor:
        """Add a contributor to a goal (async)."""
        validate_id(goal_id, "goal")
        data = GoalContributorCreate(
            persona_id=persona_id,
            role=role,
            can_update_progress=can_update_progress,
        )
        response = await self._request(
            "POST", f"/goals/{goal_id}/contributors", json=data.model_dump(exclude_none=True)
        )
        return GoalContributor.model_validate(response)

    async def update_contributor(
        self,
        goal_id: str,
        persona_id: str,
        role: Optional[str] = None,
        can_update_progress: Optional[bool] = None,
    ) -> GoalContributor:
        """Update a goal contributor (async)."""
        validate_id(goal_id, "goal")
        data = GoalContributorUpdate(
            role=role,
            can_update_progress=can_update_progress,
        )
        response = await self._request(
            "PATCH",
            f"/goals/{goal_id}/contributors/{persona_id}",
            json=data.model_dump(exclude_none=True),
        )
        return GoalContributor.model_validate(response)

    async def remove_contributor(self, goal_id: str, persona_id: str) -> None:
        """Remove a contributor from a goal (async)."""
        validate_id(goal_id, "goal")
        await self._request("DELETE", f"/goals/{goal_id}/contributors/{persona_id}")

    async def add_key_result(
        self,
        goal_id: str,
        title: str,
        *,
        description: Optional[str] = None,
        goal_type: str = "outcome",
        visibility: str = "private",
        progress_type: str = "manual",
        target_value: Optional[float] = None,
        target_unit: Optional[str] = None,
        priority: int = 0,
        weight: float = 1.0,
        start_date: Optional[str] = None,
        target_date: Optional[str] = None,
    ) -> Goal:
        """Add a key result to a goal (async)."""
        validate_id(goal_id, "goal")
        data = KeyResultCreate(
            title=title,
            description=description,
            goal_type=goal_type,
            visibility=visibility,
            progress_type=progress_type,
            target_value=target_value,
            target_unit=target_unit,
            priority=priority,
            weight=weight,
            start_date=start_date,
            target_date=target_date,
        )
        response = await self._request(
            "POST",
            f"/goals/{goal_id}/key-results",
            json=data.model_dump(exclude_none=True),
        )
        return Goal.model_validate(response)

    async def get_tree(self, goal_id: str) -> List[Goal]:
        """Get the full goal hierarchy tree (async)."""
        validate_id(goal_id, "goal")
        response = await self._request("GET", f"/goals/{goal_id}/tree")
        return [Goal.model_validate(g) for g in response]

    async def get_children(self, goal_id: str) -> List[Goal]:
        """Get direct children of a goal (async)."""
        validate_id(goal_id, "goal")
        response = await self._request("GET", f"/goals/{goal_id}/children")
        return [Goal.model_validate(g) for g in response]

    async def get_pace(self, goal_id: str) -> PaceAnalysis:
        """Get pace analysis for a goal (async)."""
        validate_id(goal_id, "goal")
        response = await self._request("GET", f"/goals/{goal_id}/pace")
        return PaceAnalysis.model_validate(response)

    async def link_memory(
        self,
        goal_id: str,
        memory_id: str,
        link_type: str = "related",
    ) -> GoalMemoryLink:
        """Link a memory to a goal (async)."""
        validate_id(goal_id, "goal")
        validate_id(memory_id, "memory")
        response = await self._request(
            "POST",
            f"/goals/{goal_id}/memories",
            json={"memory_id": memory_id, "link_type": link_type},
        )
        return GoalMemoryLink.model_validate(response)

    async def unlink_memory(self, goal_id: str, memory_id: str) -> None:
        """Unlink a memory from a goal (async)."""
        validate_id(goal_id, "goal")
        validate_id(memory_id, "memory")
        await self._request("DELETE", f"/goals/{goal_id}/memories/{memory_id}")

    async def get_memories(
        self,
        goal_id: str,
        limit: int = 20,
        offset: int = 0,
    ) -> GoalMemoryListResponse:
        """Get memories linked to a goal (async)."""
        validate_id(goal_id, "goal")
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        response = await self._request("GET", f"/goals/{goal_id}/memories", params=params)
        return GoalMemoryListResponse.model_validate(response)
