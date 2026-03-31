"""Tests for Workflows resource."""

from unittest.mock import Mock

from trix.resources.workflows import WorkflowsResource

WORKFLOW_RESPONSE = {
    "id": "wf_123",
    "account_id": "acc_1",
    "name": "Daily Summary",
    "status": "active",
    "version": 1,
    "steps": [{"type": "summarize", "config": {}}],
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
}

RUN_RESPONSE = {
    "id": "run_789",
    "workflow_id": "wf_123",
    "account_id": "acc_1",
    "status": "running",
    "created_at": "2024-01-01T00:00:00Z",
}


class TestWorkflowsResource:
    """Tests for WorkflowsResource (sync)."""

    def test_create_workflow(self):
        """Test creating a workflow."""
        mock_client = Mock()
        mock_client._request.return_value = WORKFLOW_RESPONSE

        resource = WorkflowsResource(mock_client)
        result = resource.create(
            name="Daily Summary",
            steps=[{"type": "summarize", "config": {}}],
        )

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/workflows")
        assert result.id == "wf_123"
        assert result.name == "Daily Summary"

    def test_list_workflows(self):
        """Test listing workflows."""
        mock_client = Mock()
        mock_client._request.return_value = {
            "workflows": [WORKFLOW_RESPONSE],
            "total": 1,
            "limit": 20,
            "offset": 0,
        }

        resource = WorkflowsResource(mock_client)
        result = resource.list()

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/workflows")
        assert len(result.workflows) == 1

    def test_list_workflows_with_filter(self):
        """Test listing workflows filtered by status."""
        mock_client = Mock()
        mock_client._request.return_value = {
            "workflows": [],
            "total": 0,
            "limit": 20,
            "offset": 0,
        }

        resource = WorkflowsResource(mock_client)
        resource.list(status="active")

        call_args = mock_client._request.call_args
        assert call_args[1]["params"]["status"] == "active"

    def test_get_workflow(self):
        """Test getting a workflow by ID."""
        mock_client = Mock()
        mock_client._request.return_value = WORKFLOW_RESPONSE

        resource = WorkflowsResource(mock_client)
        result = resource.get("wf_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/workflows/wf_123")
        assert result.id == "wf_123"

    def test_update_workflow(self):
        """Test updating a workflow."""
        mock_client = Mock()
        mock_client._request.return_value = {
            **WORKFLOW_RESPONSE,
            "name": "Weekly Summary",
            "version": 2,
        }

        resource = WorkflowsResource(mock_client)
        result = resource.update("wf_123", version=1, name="Weekly Summary")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("PATCH", "/workflows/wf_123")
        assert result.name == "Weekly Summary"

    def test_delete_workflow(self):
        """Test deleting a workflow."""
        mock_client = Mock()
        mock_client._request.return_value = None

        resource = WorkflowsResource(mock_client)
        resource.delete("wf_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("DELETE", "/workflows/wf_123")

    def test_trigger_workflow(self):
        """Test triggering a workflow run."""
        mock_client = Mock()
        mock_client._request.return_value = RUN_RESPONSE

        resource = WorkflowsResource(mock_client)
        result = resource.trigger("wf_123", input={"query": "recent"})

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/workflows/wf_123/trigger")
        assert result.id == "run_789"
        assert result.status == "running"

    def test_list_runs(self):
        """Test listing workflow runs."""
        mock_client = Mock()
        mock_client._request.return_value = {
            "runs": [{**RUN_RESPONSE, "status": "completed"}],
            "total": 1,
            "limit": 20,
            "offset": 0,
        }

        resource = WorkflowsResource(mock_client)
        result = resource.list_runs("wf_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/workflows/wf_123/runs")
        assert len(result.runs) == 1

    def test_create_trigger(self):
        """Test creating a workflow trigger."""
        mock_client = Mock()
        mock_client._request.return_value = {
            "id": "trigger_456",
            "workflow_id": "wf_123",
            "type": "cron",
            "cron_expression": "0 9 * * *",
            "enabled": True,
            "created_at": "2024-01-01T00:00:00Z",
        }

        resource = WorkflowsResource(mock_client)
        resource.create_trigger("wf_123", type="cron", cron_expression="0 9 * * *")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/workflows/wf_123/triggers")

    def test_delete_trigger(self):
        """Test deleting a workflow trigger."""
        mock_client = Mock()
        mock_client._request.return_value = None

        resource = WorkflowsResource(mock_client)
        resource.delete_trigger("wf_123", "trigger_456")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("DELETE", "/workflows/wf_123/triggers/trigger_456")
