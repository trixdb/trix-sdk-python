"""Tests for SpaceConfigResource."""

from unittest.mock import Mock

from trix.resources.space_config import SpaceConfigResource

CONFIG_RESPONSE = {
    "config": {
        "memory": {
            "defaults": {"max_size": 1000},
            "overrides": {},
            "effective": {"max_size": 1000},
        },
        "llm": {
            "defaults": {"model": "gpt-4"},
            "overrides": {"model": "claude-3"},
            "effective": {"model": "claude-3"},
        },
        "retrieval": {
            "defaults": {"top_k": 10},
            "overrides": {"top_k": 20},
            "effective": {"top_k": 20},
        },
        "privacy": {
            "defaults": {"pii_detection": False},
            "overrides": {},
            "effective": {"pii_detection": False},
        },
    },
    "version": 3,
}

VALIDATION_RESPONSE = {
    "valid": True,
    "errors": [],
    "categories": ["retrieval"],
}

VALIDATION_ERROR_RESPONSE = {
    "valid": False,
    "errors": ["top_k must be positive"],
    "categories": ["retrieval"],
}

AUDIT_RESPONSE = {
    "events": [
        {
            "id": "evt_001",
            "space_id": "space_123",
            "category": "retrieval",
            "actor_user_id": "user_456",
            "source": "api",
            "patch": {"top_k": 20},
            "previous_value": {"top_k": 10},
            "created_at": "2025-01-01T00:00:00Z",
        }
    ],
    "total": 1,
    "limit": 50,
    "offset": 0,
}


class TestSpaceConfigGet:
    """Tests for space_config.get()."""

    def test_get_config(self):
        """Test getting full space configuration."""
        mock_client = Mock()
        mock_client._request.return_value = CONFIG_RESPONSE

        resource = SpaceConfigResource(mock_client)
        result = resource.get("space_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/spaces/space_123/config")
        assert result.version == 3
        assert "retrieval" in result.config
        assert result.config["retrieval"].effective == {"top_k": 20}


class TestSpaceConfigUpdate:
    """Tests for space_config.update()."""

    def test_update_config(self):
        """Test updating space configuration."""
        mock_client = Mock()
        mock_client._request.return_value = CONFIG_RESPONSE

        resource = SpaceConfigResource(mock_client)
        result = resource.update("space_123", retrieval={"top_k": 20})

        call_args = mock_client._request.call_args
        assert call_args[0] == ("PATCH", "/spaces/space_123/config")
        body = call_args[1]["json"]
        assert body["retrieval"] == {"top_k": 20}
        assert result.version == 3

    def test_update_with_expected_version(self):
        """Test optimistic concurrency via If-Match header."""
        mock_client = Mock()
        mock_client._request.return_value = CONFIG_RESPONSE

        resource = SpaceConfigResource(mock_client)
        resource.update("space_123", retrieval={"top_k": 20}, expected_version=2)

        call_args = mock_client._request.call_args
        assert call_args[1]["headers"]["If-Match"] == "2"


class TestSpaceConfigValidate:
    """Tests for space_config.validate()."""

    def test_validate_valid_config(self):
        """Test validating a valid configuration patch."""
        mock_client = Mock()
        mock_client._request.return_value = VALIDATION_RESPONSE

        resource = SpaceConfigResource(mock_client)
        result = resource.validate("space_123", retrieval={"top_k": 20})

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/spaces/space_123/config/validate")
        assert result.valid is True
        assert result.errors == []
        assert result.categories == ["retrieval"]

    def test_validate_invalid_config(self):
        """Test validating an invalid configuration patch."""
        mock_client = Mock()
        mock_client._request.return_value = VALIDATION_ERROR_RESPONSE

        resource = SpaceConfigResource(mock_client)
        result = resource.validate("space_123", retrieval={"top_k": -1})

        assert result.valid is False
        assert len(result.errors) == 1


class TestSpaceConfigAudit:
    """Tests for space_config.audit()."""

    def test_audit_log(self):
        """Test getting the configuration audit trail."""
        mock_client = Mock()
        mock_client._request.return_value = AUDIT_RESPONSE

        resource = SpaceConfigResource(mock_client)
        result = resource.audit("space_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/spaces/space_123/config/audit")
        assert call_args[1]["params"]["limit"] == 50
        assert call_args[1]["params"]["offset"] == 0
        assert result.total == 1
        assert len(result.events) == 1
        assert result.events[0].id == "evt_001"
        assert result.events[0].category == "retrieval"

    def test_audit_with_pagination(self):
        """Test audit log with custom pagination."""
        mock_client = Mock()
        mock_client._request.return_value = AUDIT_RESPONSE

        resource = SpaceConfigResource(mock_client)
        resource.audit("space_123", limit=10, offset=5)

        call_args = mock_client._request.call_args
        assert call_args[1]["params"]["limit"] == 10
        assert call_args[1]["params"]["offset"] == 5
