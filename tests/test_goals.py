"""Tests for Goals resource."""

from tests.support import spec_client
from trix.resources.goals import GoalsResource

GOAL_RESPONSE = {
    "id": "goal_123",
    "account_id": "acc_1",
    "title": "Ship MVP",
    "goal_type": "outcome",
    "status": "active",
    "visibility": "private",
    "progress": 0.0,
    "progress_type": "manual",
    "priority": 1,
    "weight": 1.0,
    "depth": 0,
    "version": 1,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
}


class TestGoalsResource:
    """Tests for GoalsResource (sync)."""

    def test_create_goal(self):
        """Test creating a goal."""
        mock_client = spec_client()
        mock_client._request.return_value = GOAL_RESPONSE

        resource = GoalsResource(mock_client)
        result = resource.create(title="Ship MVP", goal_type="outcome")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/goals")
        assert result.id == "goal_123"
        assert result.title == "Ship MVP"

    def test_list_goals(self):
        """Test listing goals."""
        mock_client = spec_client()
        mock_client._request.return_value = {
            "goals": [GOAL_RESPONSE],
            "total": 1,
            "limit": 50,
            "offset": 0,
        }

        resource = GoalsResource(mock_client)
        result = resource.list()

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/goals")
        assert result.total == 1

    def test_list_goals_with_status_filter(self):
        """Test listing goals filtered by status."""
        mock_client = spec_client()
        mock_client._request.return_value = {
            "goals": [],
            "total": 0,
            "limit": 50,
            "offset": 0,
        }

        resource = GoalsResource(mock_client)
        resource.list(status="active")

        call_args = mock_client._request.call_args
        assert call_args[1]["params"]["status"] == "active"

    def test_get_goal(self):
        """Test getting a goal by ID."""
        mock_client = spec_client()
        mock_client._request.return_value = GOAL_RESPONSE

        resource = GoalsResource(mock_client)
        result = resource.get("goal_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/goals/goal_123")
        assert result.id == "goal_123"

    def test_update_goal(self):
        """Test updating a goal."""
        mock_client = spec_client()
        mock_client._request.return_value = {**GOAL_RESPONSE, "title": "Ship MVP v2"}

        resource = GoalsResource(mock_client)
        result = resource.update("goal_123", title="Ship MVP v2")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("PATCH", "/goals/goal_123")
        assert result.title == "Ship MVP v2"

    def test_delete_goal(self):
        """Test deleting a goal."""
        mock_client = spec_client()
        mock_client._request.return_value = None

        resource = GoalsResource(mock_client)
        resource.delete("goal_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("DELETE", "/goals/goal_123")

    def test_update_progress(self):
        """Test updating goal progress."""
        mock_client = spec_client()
        mock_client._request.return_value = {**GOAL_RESPONSE, "progress": 0.5}

        resource = GoalsResource(mock_client)
        result = resource.update_progress("goal_123", progress=0.5)

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/goals/goal_123/progress")
        assert result.progress == 0.5

    def test_transition_status(self):
        """Test transitioning goal status."""
        mock_client = spec_client()
        mock_client._request.return_value = {**GOAL_RESPONSE, "status": "completed"}

        resource = GoalsResource(mock_client)
        result = resource.transition_status("goal_123", status="completed")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/goals/goal_123/status")
        assert result.status == "completed"

    def test_get_progress_history(self):
        """Test getting progress history."""
        mock_client = spec_client()
        mock_client._request.return_value = {
            "entries": [
                {
                    "id": "ph_1",
                    "goal_id": "goal_123",
                    "previous_progress": 0.0,
                    "new_progress": 0.5,
                    "source": "manual",
                    "created_at": "2024-01-02T00:00:00Z",
                },
            ],
            "total": 1,
            "limit": 50,
            "offset": 0,
        }

        resource = GoalsResource(mock_client)
        result = resource.get_progress_history("goal_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/goals/goal_123/progress-history")
        assert result.total == 1

    def test_get_pace(self):
        """Test getting pace analysis."""
        mock_client = spec_client()
        mock_client._request.return_value = {
            "goal_id": "goal_123",
            "status": "on_track",
            "progress": 0.5,
            "expected": 0.45,
        }

        resource = GoalsResource(mock_client)
        result = resource.get_pace("goal_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/goals/goal_123/pace")
        assert result.status == "on_track"

    def test_add_key_result(self):
        """Test adding a key result to a goal."""
        mock_client = spec_client()
        mock_client._request.return_value = {
            **GOAL_RESPONSE,
            "id": "goal_456",
            "title": "Reach 1000 users",
            "parent_goal_id": "goal_123",
            "is_key_result": True,
        }

        resource = GoalsResource(mock_client)
        result = resource.add_key_result("goal_123", title="Reach 1000 users")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/goals/goal_123/key-results")
        assert result.title == "Reach 1000 users"
