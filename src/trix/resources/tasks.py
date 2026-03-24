"""Tasks resource for Trix SDK."""

from typing import Any, Dict, List, Optional

from .base import BaseSyncResource
from .tasks_bulk import TasksBulkMixin
from ..types.task import (
    SubtaskCreate,
    Task,
    TaskCreate,
    TaskList,
    TaskUpdate,
)
from ..utils.security import validate_id


class TasksResource(TasksBulkMixin):
    """Resource for managing tasks.

    Tasks are actionable items that can be linked to memories, sessions,
    and other Trix entities.

    Example:
        >>> # Create a task
        >>> task = client.tasks.create(
        ...     title="Review quarterly report",
        ...     space_id="space_123",
        ...     priority=3
        ... )
        >>>
        >>> # List tasks
        >>> tasks = client.tasks.list(space_id="space_123", status="pending")
        >>>
        >>> # Complete a task
        >>> client.tasks.complete("task_123")
    """

    def create(
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
        """Create a new task.

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

        Example:
            >>> task = client.tasks.create(
            ...     title="Review PR #123",
            ...     space_id="space_abc",
            ...     priority=3,
            ...     due_at="2026-02-01T17:00:00Z"
            ... )
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
        response = self._request("POST", "/tasks", json=data.model_dump(exclude_none=True))
        return Task.model_validate(response)

    def list(
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
        """List tasks with filtering and pagination.

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

        Example:
            >>> tasks = client.tasks.list(
            ...     space_id="space_123",
            ...     status="pending",
            ...     limit=20
            ... )
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

        response = self._request("GET", "/tasks", params=params)
        return TaskList.model_validate(response)

    def get(self, task_id: str, include: Optional[List[str]] = None) -> Task:
        """Get a task by ID.

        Args:
            task_id: Task ID
            include: Optional list of relations to include (labels, subtasks, links)

        Returns:
            Task object

        Raises:
            ValidationError: If ID format is invalid
            NotFoundError: If task doesn't exist

        Example:
            >>> task = client.tasks.get("task_123")
        """
        validate_id(task_id, "task")
        params: Dict[str, Any] = {}
        if include is not None:
            params["include"] = ",".join(include)
        response = self._request("GET", f"/tasks/{task_id}", params=params if params else None)
        return Task.model_validate(response)

    def update(
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
        """Update a task.

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

        Raises:
            ValidationError: If ID format is invalid
            NotFoundError: If task doesn't exist
            ConflictError: If version mismatch (409)

        Example:
            >>> task = client.tasks.update(
            ...     "task_123",
            ...     status="in_progress",
            ...     priority=4
            ... )
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
        response = self._request(
            "PATCH", f"/tasks/{task_id}", json=data.model_dump(exclude_none=True)
        )
        return Task.model_validate(response)

    def complete(self, task_id: str) -> Task:
        """Mark a task as completed.

        Args:
            task_id: Task ID

        Returns:
            Updated task object with status='done' and completed_at set

        Example:
            >>> task = client.tasks.complete("task_123")
        """
        validate_id(task_id, "task")
        response = self._request("POST", f"/tasks/{task_id}/complete")
        return Task.model_validate(response)

    def delete(self, task_id: str) -> None:
        """Delete a task.

        Args:
            task_id: Task ID

        Raises:
            ValidationError: If ID format is invalid
            NotFoundError: If task doesn't exist

        Example:
            >>> client.tasks.delete("task_123")
        """
        validate_id(task_id, "task")
        self._request("DELETE", f"/tasks/{task_id}")

    def create_subtask(
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
        """Create a subtask under a parent task.

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

        Example:
            >>> subtask = client.tasks.create_subtask(
            ...     "task_123",
            ...     title="Review section 1"
            ... )
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
        response = self._request(
            "POST", f"/tasks/{task_id}/subtasks", json=data.model_dump(exclude_none=True)
        )
        return Task.model_validate(response)
