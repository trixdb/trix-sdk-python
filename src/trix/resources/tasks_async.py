"""Async tasks resource for Trix SDK."""

from typing import Any, Dict, List, Optional

from .base import BaseAsyncResource
from ..types.task import (
    BulkDeleteResult,
    BulkTaskCreate,
    BulkTaskResult,
    BulkTaskUpdate,
    SubtaskCreate,
    SuggestedTasksResult,
    Task,
    TaskCreate,
    TaskHandoffResult,
    TaskList,
    TaskUpdate,
)
from ..utils.security import validate_id


class AsyncTasksResource(BaseAsyncResource):
    """Async resource for managing tasks.

    Tasks are actionable items that can be linked to memories, sessions,
    and other Trix entities.

    Example:
        >>> # Create a task
        >>> task = await client.tasks.create(
        ...     title="Review quarterly report",
        ...     space_id="space_123",
        ...     priority=3
        ... )
    """

    async def create(
        self,
        title: str,
        space_id: str,
        section_id: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[int] = None,
        estimated_minutes: Optional[int] = None,
        start_at: Optional[str] = None,
        due_at: Optional[str] = None,
        parent_task_id: Optional[str] = None,
        assignee_id: Optional[str] = None,
        assignee_type: Optional[str] = None,
        labels: Optional[List[str]] = None,
        stale_after_days: Optional[int] = None,
    ) -> Task:
        """Create a new task (async).

        Args:
            title: Task title
            space_id: Space ID to organize the task
            section_id: Optional section ID within the space
            description: Optional task description
            status: Task status (pending, in_progress, done, cancelled)
            priority: Priority level (0-4, higher is more urgent)
            estimated_minutes: Estimated time to complete
            start_at: ISO datetime when task should start
            due_at: ISO datetime when task is due
            parent_task_id: Parent task ID for subtasks
            assignee_id: ID of user or agent assigned to task
            assignee_type: Type of assignee ('user' or 'agent')
            labels: List of label IDs to attach
            stale_after_days: Auto-stale after this many days of inactivity

        Returns:
            Created task object
        """
        data = TaskCreate(
            title=title,
            space_id=space_id,
            section_id=section_id,
            description=description,
            status=status,
            priority=priority,
            estimated_minutes=estimated_minutes,
            start_at=start_at,
            due_at=due_at,
            parent_task_id=parent_task_id,
            assignee_id=assignee_id,
            assignee_type=assignee_type,
            labels=labels,
            stale_after_days=stale_after_days,
        )
        response = await self._request(
            "POST", "/tasks", json=data.model_dump(exclude_none=True)
        )
        return Task.model_validate(response)

    async def list(
        self,
        space_id: Optional[str] = None,
        section_id: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[int] = None,
        assignee_id: Optional[str] = None,
        parent_task_id: Optional[str] = None,
        labels: Optional[List[str]] = None,
        due_before: Optional[str] = None,
        due_after: Optional[str] = None,
        include_subtasks: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> TaskList:
        """List tasks with filtering and pagination (async).

        Args:
            space_id: Filter by space
            section_id: Filter by section
            status: Filter by status (pending, in_progress, done, cancelled, stale)
            priority: Filter by exact priority
            assignee_id: Filter by assignee
            parent_task_id: Filter subtasks of a parent
            labels: Filter by label IDs (any match)
            due_before: Filter tasks due before this ISO datetime
            due_after: Filter tasks due after this ISO datetime
            include_subtasks: Include subtasks in results
            limit: Maximum results to return (default 50, max 100)
            offset: Number of results to skip
            sort_by: Field to sort by (created_at, due_at, priority, title)
            sort_order: Sort order (asc, desc)

        Returns:
            Paginated list of tasks
        """
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if space_id is not None:
            params["space_id"] = space_id
        if section_id is not None:
            params["section_id"] = section_id
        if status is not None:
            params["status"] = status
        if priority is not None:
            params["priority"] = priority
        if assignee_id is not None:
            params["assignee_id"] = assignee_id
        if parent_task_id is not None:
            params["parent_task_id"] = parent_task_id
        if labels is not None:
            params["labels"] = ",".join(labels)
        if due_before is not None:
            params["due_before"] = due_before
        if due_after is not None:
            params["due_after"] = due_after
        if include_subtasks is not None:
            params["include_subtasks"] = include_subtasks
        if sort_by is not None:
            params["sort_by"] = sort_by
        if sort_order is not None:
            params["sort_order"] = sort_order

        response = await self._request("GET", "/tasks", params=params)
        return TaskList.model_validate(response)

    async def get(self, task_id: str, include: Optional[List[str]] = None) -> Task:
        """Get a task by ID (async).

        Args:
            task_id: Task ID
            include: Optional list of relations to include (labels, subtasks, links)

        Returns:
            Task object
        """
        validate_id(task_id, "task")
        params: Dict[str, Any] = {}
        if include is not None:
            params["include"] = ",".join(include)
        response = await self._request(
            "GET", f"/tasks/{task_id}", params=params if params else None
        )
        return Task.model_validate(response)

    async def update(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[int] = None,
        estimated_minutes: Optional[int] = None,
        start_at: Optional[str] = None,
        due_at: Optional[str] = None,
        section_id: Optional[str] = None,
        assignee_id: Optional[str] = None,
        assignee_type: Optional[str] = None,
        labels: Optional[List[str]] = None,
        stale_after_days: Optional[int] = None,
        version: Optional[int] = None,
    ) -> Task:
        """Update a task (async).

        Args:
            task_id: Task ID
            title: New title
            description: New description
            status: New status
            priority: New priority
            estimated_minutes: New time estimate
            start_at: New start datetime
            due_at: New due datetime
            section_id: New section ID
            assignee_id: New assignee ID
            assignee_type: New assignee type
            labels: New label IDs (replaces existing)
            stale_after_days: New stale threshold
            version: Expected version for optimistic locking

        Returns:
            Updated task object
        """
        validate_id(task_id, "task")
        data = TaskUpdate(
            title=title,
            description=description,
            status=status,
            priority=priority,
            estimated_minutes=estimated_minutes,
            start_at=start_at,
            due_at=due_at,
            section_id=section_id,
            assignee_id=assignee_id,
            assignee_type=assignee_type,
            labels=labels,
            stale_after_days=stale_after_days,
            version=version,
        )
        response = await self._request(
            "PATCH", f"/tasks/{task_id}", json=data.model_dump(exclude_none=True)
        )
        return Task.model_validate(response)

    async def complete(self, task_id: str) -> Task:
        """Mark a task as completed (async).

        Args:
            task_id: Task ID

        Returns:
            Updated task object with status='done' and completed_at set
        """
        validate_id(task_id, "task")
        response = await self._request("POST", f"/tasks/{task_id}/complete")
        return Task.model_validate(response)

    async def delete(self, task_id: str) -> None:
        """Delete a task (async).

        Args:
            task_id: Task ID
        """
        validate_id(task_id, "task")
        await self._request("DELETE", f"/tasks/{task_id}")

    async def create_subtask(
        self,
        task_id: str,
        title: str,
        description: Optional[str] = None,
        priority: Optional[int] = None,
        estimated_minutes: Optional[int] = None,
        due_at: Optional[str] = None,
        assignee_id: Optional[str] = None,
        assignee_type: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ) -> Task:
        """Create a subtask under a parent task (async).

        Args:
            task_id: Parent task ID
            title: Subtask title
            description: Optional description
            priority: Priority level
            estimated_minutes: Time estimate
            due_at: Due datetime
            assignee_id: Assignee ID
            assignee_type: Assignee type
            labels: Label IDs

        Returns:
            Created subtask
        """
        validate_id(task_id, "task")
        data = SubtaskCreate(
            title=title,
            description=description,
            priority=priority,
            estimated_minutes=estimated_minutes,
            due_at=due_at,
            assignee_id=assignee_id,
            assignee_type=assignee_type,
            labels=labels,
        )
        response = await self._request(
            "POST", f"/tasks/{task_id}/subtasks", json=data.model_dump(exclude_none=True)
        )
        return Task.model_validate(response)

    async def bulk_create(self, tasks: List[BulkTaskCreate]) -> BulkTaskResult:
        """Create multiple tasks in a single request (async).

        Args:
            tasks: List of tasks to create

        Returns:
            Bulk operation result with created tasks
        """
        data = [t.model_dump(exclude_none=True) for t in tasks]
        response = await self._request("POST", "/tasks/bulk", json={"tasks": data})
        return BulkTaskResult.model_validate(response)

    async def bulk_update(self, tasks: List[BulkTaskUpdate]) -> BulkTaskResult:
        """Update multiple tasks in a single request (async).

        Args:
            tasks: List of task updates (each must include 'id')

        Returns:
            Bulk operation result with updated tasks
        """
        if not tasks or len(tasks) > 100:
            raise ValueError("tasks must be a non-empty list with at most 100 items")
        for i, task in enumerate(tasks):
            if not task.id:
                raise ValueError(f"Task at index {i} is missing an id")
            validate_id(task.id, f"task[{i}]")
        data = [t.model_dump(exclude_none=True) for t in tasks]
        response = await self._request("PATCH", "/tasks/bulk", json={"tasks": data})
        return BulkTaskResult.model_validate(response)

    async def suggested(
        self,
        context: Optional[str] = None,
        space_id: Optional[str] = None,
        limit: int = 5,
    ) -> SuggestedTasksResult:
        """Get AI-suggested tasks based on context (async).

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
        """
        params: Dict[str, Any] = {"limit": limit}
        if context is not None:
            params["context"] = context
        if space_id is not None:
            params["space_id"] = space_id

        response = await self._request("GET", "/tasks/suggested", params=params)
        return SuggestedTasksResult.model_validate(response)

    async def get_subtasks(self, parent_id: str) -> List[Task]:
        """Get subtasks for a parent task (async).

        Args:
            parent_id: ID of the parent task

        Returns:
            List of subtasks
        """
        validate_id(parent_id, "task")
        response = await self._request("GET", f"/tasks/{parent_id}/subtasks")
        subtasks_data = response.get("subtasks", [])
        return [Task.model_validate(s) for s in subtasks_data]

    async def handoff(
        self,
        task_id: str,
        target_agent_id: str,
        handoff_notes: Optional[str] = None,
        checkpoint_data: Optional[Dict[str, Any]] = None,
    ) -> TaskHandoffResult:
        """Hand off a task to another agent (async).

        Args:
            task_id: ID of the task to hand off
            target_agent_id: ID of the agent to hand off to
            handoff_notes: Optional notes about the handoff
            checkpoint_data: Optional checkpoint data to store

        Returns:
            Handoff result with task and metadata

        Example:
            >>> result = await client.tasks.handoff(
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
        response = await self._request("POST", f"/tasks/{task_id}/handoff", json=data)
        return TaskHandoffResult.model_validate(response)

    async def bulk_delete(self, ids: List[str], cascade: bool = True) -> BulkDeleteResult:
        """Delete multiple tasks in a single request (async).

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
        response = await self._request(
            "DELETE", "/tasks/bulk", json={"ids": ids, "cascade": cascade}
        )
        return BulkDeleteResult.model_validate(response)
