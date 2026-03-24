"""Tests for WebhooksResource."""

from unittest.mock import Mock

from trix.resources.webhooks import WebhooksResource
from trix.types import WebhookEvent


WEBHOOK_RESPONSE = {
    "id": "webhook_123",
    "name": "Memory Updates",
    "url": "https://example.com/webhook",
    "events": ["memory.created", "memory.updated"],
    "space_id": None,
    "headers": {},
    "filters": None,
    "active": True,
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z",
}

WEBHOOK_LIST_RESPONSE = {
    "data": [WEBHOOK_RESPONSE],
}


class TestWebhooksCreate:
    """Tests for webhooks.create()."""

    def test_create_basic(self):
        """Test creating a webhook with required fields."""
        mock_client = Mock()
        mock_client._request.return_value = WEBHOOK_RESPONSE

        resource = WebhooksResource(mock_client)
        result = resource.create(
            name="Memory Updates",
            url="https://example.com/webhook",
            events=[WebhookEvent.MEMORY_CREATED, WebhookEvent.MEMORY_UPDATED],
        )

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/webhooks")
        assert result.id == "webhook_123"
        assert result.name == "Memory Updates"
        assert result.url == "https://example.com/webhook"

    def test_create_with_options(self):
        """Test creating a webhook with all options."""
        mock_client = Mock()
        mock_client._request.return_value = WEBHOOK_RESPONSE

        resource = WebhooksResource(mock_client)
        resource.create(
            name="Memory Updates",
            url="https://example.com/webhook",
            events=[WebhookEvent.MEMORY_CREATED],
            space_id="space_abc",
            headers={"Authorization": "Bearer token"},
        )

        call_args = mock_client._request.call_args
        body = call_args[1]["json"]
        assert body["name"] == "Memory Updates"
        assert body["events"] == ["memory.created"]
        assert body["space_id"] == "space_abc"
        assert body["headers"] == {"Authorization": "Bearer token"}


class TestWebhooksGet:
    """Tests for webhooks.get()."""

    def test_get_by_id(self):
        """Test getting a webhook by ID."""
        mock_client = Mock()
        mock_client._request.return_value = WEBHOOK_RESPONSE

        resource = WebhooksResource(mock_client)
        result = resource.get("webhook_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/webhooks/webhook_123")
        assert result.id == "webhook_123"
        assert result.active is True


class TestWebhooksList:
    """Tests for webhooks.list()."""

    def test_list_all(self):
        """Test listing all webhooks."""
        mock_client = Mock()
        mock_client._request.return_value = WEBHOOK_LIST_RESPONSE

        resource = WebhooksResource(mock_client)
        result = resource.list()

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/webhooks")
        assert len(result.data) == 1
        assert result.data[0].id == "webhook_123"

    def test_list_empty(self):
        """Test listing when no webhooks exist."""
        mock_client = Mock()
        mock_client._request.return_value = {"data": []}

        resource = WebhooksResource(mock_client)
        result = resource.list()

        assert len(result.data) == 0


class TestWebhooksUpdate:
    """Tests for webhooks.update()."""

    def test_update_name(self):
        """Test updating a webhook name."""
        mock_client = Mock()
        updated = {**WEBHOOK_RESPONSE, "name": "Updated Name"}
        mock_client._request.return_value = updated

        resource = WebhooksResource(mock_client)
        result = resource.update("webhook_123", name="Updated Name")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("PATCH", "/webhooks/webhook_123")
        assert result.name == "Updated Name"

    def test_update_active_status(self):
        """Test disabling a webhook."""
        mock_client = Mock()
        updated = {**WEBHOOK_RESPONSE, "active": False}
        mock_client._request.return_value = updated

        resource = WebhooksResource(mock_client)
        result = resource.update("webhook_123", active=False)

        call_args = mock_client._request.call_args
        body = call_args[1]["json"]
        assert body["active"] is False
        assert result.active is False


class TestWebhooksDelete:
    """Tests for webhooks.delete()."""

    def test_delete_by_id(self):
        """Test deleting a webhook."""
        mock_client = Mock()
        mock_client._request.return_value = None

        resource = WebhooksResource(mock_client)
        resource.delete("webhook_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("DELETE", "/webhooks/webhook_123")


class TestWebhooksTest:
    """Tests for webhooks.test()."""

    def test_send_test_event(self):
        """Test sending a test webhook event."""
        mock_client = Mock()
        mock_client._request.return_value = {
            "success": True,
            "status_code": 200,
        }

        resource = WebhooksResource(mock_client)
        result = resource.test("webhook_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/webhooks/webhook_123/test")
        assert result["success"] is True

    def test_send_test_event_with_type(self):
        """Test sending a specific event type."""
        mock_client = Mock()
        mock_client._request.return_value = {
            "success": True,
            "status_code": 200,
        }

        resource = WebhooksResource(mock_client)
        resource.test("webhook_123", event_type=WebhookEvent.MEMORY_CREATED)

        call_args = mock_client._request.call_args
        assert call_args[1]["params"]["event_type"] == "memory.created"


class TestWebhooksDeliveries:
    """Tests for webhooks.get_deliveries()."""

    def test_get_deliveries(self):
        """Test getting webhook delivery history."""
        mock_client = Mock()
        mock_client._request.return_value = {
            "data": [
                {
                    "id": "del_123",
                    "webhook_id": "webhook_123",
                    "event_type": "memory.created",
                    "success": True,
                    "status_code": 200,
                    "payload": {"memory_id": "mem_123"},
                    "attempted_at": "2025-01-01T00:00:00Z",
                }
            ],
        }

        resource = WebhooksResource(mock_client)
        result = resource.get_deliveries("webhook_123", limit=50)

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/webhooks/webhook_123/deliveries")
        assert call_args[1]["params"]["limit"] == 50
        assert len(result.data) == 1
        assert result.data[0].id == "del_123"
