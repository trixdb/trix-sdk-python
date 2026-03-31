"""Tests for Tasks resource."""

from unittest.mock import Mock

from trix.resources.tasks import TasksResource

TASK_RESPONSE = {
    "id": "task_123",
    "title": "Review quarterly report",
    "space_id": "space_abc",
    "status": "pending",
    "priority": 3,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
}


class TestTasksResource:
    """Tests for TasksResource (sync)."""

    def test_create_task(self):
        """Test creating a task."""
        mock_client = Mock()
        mock_client._request.return_value = TASK_RESPONSE

        resource = TasksResource(mock_client)
        result = resource.create(title="Review quarterly report", space_id="space_abc", priority=3)

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/tasks")
        assert result.id == "task_123"
        assert result.title == "Review quarterly report"

    def test_list_tasks(self):
        """Test listing tasks."""
        mock_client = Mock()
        mock_client._request.return_value = {
            "data": [TASK_RESPONSE],
            "total": 1,
            "limit": 50,
            "offset": 0,
        }

        resource = TasksResource(mock_client)
        result = resource.list(space_id="space_abc")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/tasks")
        assert call_args[1]["params"]["space_id"] == "space_abc"
        assert len(result.data) == 1

    def test_list_tasks_with_status_filter(self):
        """Test listing tasks filtered by status."""
        mock_client = Mock()
        mock_client._request.return_value = {
            "data": [],
            "total": 0,
            "limit": 50,
            "offset": 0,
        }

        resource = TasksResource(mock_client)
        resource.list(status="pending")

        call_args = mock_client._request.call_args
        assert call_args[1]["params"]["status"] == "pending"

    def test_get_task(self):
        """Test getting a task by ID."""
        mock_client = Mock()
        mock_client._request.return_value = TASK_RESPONSE

        resource = TasksResource(mock_client)
        result = resource.get("task_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/tasks/task_123")
        assert result.id == "task_123"

    def test_update_task(self):
        """Test updating a task."""
        mock_client = Mock()
        mock_client._request.return_value = {**TASK_RESPONSE, "status": "in_progress"}

        resource = TasksResource(mock_client)
        result = resource.update("task_123", status="in_progress")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("PATCH", "/tasks/task_123")
        assert result.status == "in_progress"

    def test_complete_task(self):
        """Test completing a task."""
        mock_client = Mock()
        mock_client._request.return_value = {
            **TASK_RESPONSE,
            "status": "done",
            "completed_at": "2024-01-02T00:00:00Z",
        }

        resource = TasksResource(mock_client)
        result = resource.complete("task_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/tasks/task_123/complete")
        assert result.status == "done"

    def test_delete_task(self):
        """Test deleting a task."""
        mock_client = Mock()
        mock_client._request.return_value = None

        resource = TasksResource(mock_client)
        resource.delete("task_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("DELETE", "/tasks/task_123")

    def test_create_subtask(self):
        """Test creating a subtask."""
        mock_client = Mock()
        mock_client._request.return_value = {
            **TASK_RESPONSE,
            "id": "task_456",
            "title": "Review section 1",
            "parent_task_id": "task_123",
        }

        resource = TasksResource(mock_client)
        result = resource.create_subtask("task_123", title="Review section 1")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/tasks/task_123/subtasks")
        assert result.title == "Review section 1"

    def test_handoff_task(self):
        """Test handing off a task to another agent."""
        mock_client = Mock()
        mock_client._request.return_value = {
            "handoff_id": "handoff_789",
            "task": TASK_RESPONSE,
            "new_assignee_id": "agent_456",
        }

        resource = TasksResource(mock_client)
        result = resource.handoff(
            "task_123",
            target_agent_id="agent_456",
            handoff_notes="Completed research phase",
        )

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/tasks/task_123/handoff")
        assert result.new_assignee_id == "agent_456"

    def test_suggested_tasks(self):
        """Test getting AI-suggested tasks."""
        mock_client = Mock()
        mock_client._request.return_value = {
            "data": [
                {
                    "task": TASK_RESPONSE,
                    "score": 0.9,
                    "reasons": ["High priority"],
                },
            ],
        }

        resource = TasksResource(mock_client)
        result = resource.suggested(context="quarterly review")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/tasks/suggested")
        assert call_args[1]["params"]["context"] == "quarterly review"
        assert len(result.data) == 1
