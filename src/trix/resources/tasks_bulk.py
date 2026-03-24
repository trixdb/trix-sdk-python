"""Bulk and extended task operations for Trix SDK."""

from typing import Any, Dict, List, Optional

from .base import BaseSyncResource
from ..types.task import (
    BulkDeleteResult,
    BulkTaskCreate,
    BulkTaskResult,
    BulkTaskUpdate,
    SuggestedTasksResult,
    Task,
    TaskHandoffResult,
)
from ..utils.security import validate_id


class TasksBulkMixin(BaseSyncResource):
    """Mixin providing bulk, suggested, subtask, and handoff operations for tasks."""

    def bulk_create(self, tasks: List[BulkTaskCreate]) -> BulkTaskResult:
        """Create multiple tasks in a single request.

        Args:
            tasks: List of tasks to create

        Returns:
            Bulk operation result with created tasks

        Example:
            >>> from trix.types import BulkTaskCreate
            >>> result = client.tasks.bulk_create([
            ...     BulkTaskCreate(title="Task 1", space_id="space_123"),
            ...     BulkTaskCreate(title="Task 2", space_id="space_123"),
            ... ])
        """
        data = [t.model_dump(exclude_none=True) for t in tasks]
        response = self._request("POST", "/tasks/bulk", json={"tasks": data})
        return BulkTaskResult.model_validate(response)

    def bulk_update(self, tasks: List[BulkTaskUpdate]) -> BulkTaskResult:
        """Update multiple tasks in a single request.

        Args:
            tasks: List of task updates (each must include 'id')

        Returns:
            Bulk operation result with updated tasks

        Example:
            >>> from trix.types import BulkTaskUpdate
            >>> result = client.tasks.bulk_update([
            ...     BulkTaskUpdate(id="task_1", status="done"),
            ...     BulkTaskUpdate(id="task_2", priority=4),
            ... ])
        """
        if not tasks or len(tasks) > 100:
            raise ValueError("tasks must be a non-empty list with at most 100 items")
        for i, task in enumerate(tasks):
            if not task.id:
                raise ValueError(f"Task at index {i} is missing an id")
            validate_id(task.id, f"task[{i}]")
        data = [t.model_dump(exclude_none=True) for t in tasks]
        response = self._request("PATCH", "/tasks/bulk", json={"tasks": data})
        return BulkTaskResult.model_validate(response)

    def bulk_delete(self, ids: List[str], cascade: bool = True) -> BulkDeleteResult:
        """Delete multiple tasks in a single request.

        Args:
            ids: List of task IDs to delete (max 100)
            cascade: Whether to cascade delete subtasks (default True)

        Returns:
            Bulk delete result
        """
        if not ids or len(ids) > 100:
            raise ValueError("ids must be a non-empty list with at most 100 items")
        for i, task_id in enumerate(ids):
            validate_id(task_id, f"task[{i}]")
        response = self._request("DELETE", "/tasks/bulk", json={"ids": ids, "cascade": cascade})
        return BulkDeleteResult.model_validate(response)

    def suggested(
        self,
        context: Optional[str] = None,
        space_id: Optional[str] = None,
        limit: int = 5,
    ) -> SuggestedTasksResult:
        """Get AI-suggested tasks based on context.

        Uses AI prioritization to recommend tasks based on:
        - Current context/query
        - Linked memory importance
        - Due dates and priority
        - Assignment status

        Args:
            context: Optional context string for relevance scoring
            space_id: Optional space to limit suggestions
            limit: Maximum suggestions to return (default 5)

        Returns:
            Suggested tasks with scores and reasons

        Example:
            >>> suggestions = client.tasks.suggested(
            ...     context="preparing for quarterly review",
            ...     limit=3
            ... )
        """
        params: Dict[str, Any] = {"limit": limit}
        if context is not None:
            params["context"] = context
        if space_id is not None:
            params["space_id"] = space_id

        response = self._request("GET", "/tasks/suggested", params=params)
        return SuggestedTasksResult.model_validate(response)

    def get_subtasks(self, parent_id: str) -> List[Task]:
        """Get subtasks for a parent task.

        Args:
            parent_id: ID of the parent task

        Returns:
            List of subtasks
        """
        validate_id(parent_id, "task")
        response = self._request("GET", f"/tasks/{parent_id}/subtasks")
        subtasks_data = response.get("subtasks", [])
        return [Task.model_validate(s) for s in subtasks_data]

    def handoff(
        self,
        task_id: str,
        target_agent_id: str,
        handoff_notes: Optional[str] = None,
        checkpoint_data: Optional[Dict[str, Any]] = None,
    ) -> TaskHandoffResult:
        """Hand off a task to another agent.

        Args:
            task_id: ID of the task to hand off
            target_agent_id: ID of the agent to hand off to
            handoff_notes: Optional notes about the handoff
            checkpoint_data: Optional checkpoint data to store

        Returns:
            Handoff result with task and metadata

        Example:
            >>> result = client.tasks.handoff(
            ...     "task_123",
            ...     target_agent_id="agent_456",
            ...     handoff_notes="Completed research phase"
            ... )
        """
        validate_id(task_id, "task")
        data: Dict[str, Any] = {"target_agent_id": target_agent_id}
        if handoff_notes is not None:
            data["handoff_notes"] = handoff_notes
        if checkpoint_data is not None:
            data["checkpoint_data"] = checkpoint_data
        response = self._request("POST", f"/tasks/{task_id}/handoff", json=data)
        return TaskHandoffResult.model_validate(response)
