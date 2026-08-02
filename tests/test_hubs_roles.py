"""Hub roles resource tests."""

from unittest.mock import Mock

import pytest

from tests.support import spec_client
from trix.resources.hubs_roles import HubRolesResource
from trix.types.hub import ConvRoleOverride, HubCustomRole

ROLE_DATA = {
    "id": "role-1",
    "hub_id": "hub-1",
    "name": "Moderator",
    "color": "#ff0000",
    "icon": "shield",
    "position": 1,
    "permissions": {"send_messages": "allow", "manage_members": "deny"},
    "is_default": False,
}

OVERRIDE_DATA = {
    "id": "ovr-1",
    "conversation_id": "conv-1",
    "role_id": "role-1",
    "permissions": {"send_messages": "deny"},
}


def _make_resource() -> tuple[HubRolesResource, Mock]:
    mock_client = spec_client()
    resource = HubRolesResource(mock_client)
    return resource, mock_client


class TestHubRolesList:
    def test_list_roles(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"data": [ROLE_DATA]}

        result = resource.list_roles("hub-1")

        assert len(result) == 1
        assert isinstance(result[0], HubCustomRole)
        assert result[0].name == "Moderator"
        args = mock._request.call_args
        assert args[0] == ("GET", "/hubs/hub-1/roles")

    def test_list_roles_validates_id(self):
        resource, _ = _make_resource()
        with pytest.raises(ValueError):
            resource.list_roles("")


class TestHubRolesCreate:
    def test_create_role(self):
        resource, mock = _make_resource()
        mock._request.return_value = ROLE_DATA

        result = resource.create_role("hub-1", name="Moderator", color="#ff0000")

        assert isinstance(result, HubCustomRole)
        assert result.id == "role-1"
        args = mock._request.call_args
        assert args[0] == ("POST", "/hubs/hub-1/roles")
        assert args[1]["json"]["name"] == "Moderator"
        assert args[1]["json"]["color"] == "#ff0000"

    def test_create_role_minimal(self):
        resource, mock = _make_resource()
        mock._request.return_value = ROLE_DATA

        result = resource.create_role("hub-1", name="Moderator")

        assert isinstance(result, HubCustomRole)
        args = mock._request.call_args
        assert args[1]["json"]["name"] == "Moderator"

    def test_create_role_validates_hub_id(self):
        resource, _ = _make_resource()
        with pytest.raises(ValueError):
            resource.create_role("", name="Moderator")


class TestHubRolesUpdate:
    def test_update_role(self):
        resource, mock = _make_resource()
        mock._request.return_value = {**ROLE_DATA, "name": "Admin"}

        result = resource.update_role("hub-1", "role-1", name="Admin")

        assert result.name == "Admin"
        args = mock._request.call_args
        assert args[0] == ("PATCH", "/hubs/hub-1/roles/role-1")
        assert args[1]["json"]["name"] == "Admin"

    def test_update_role_validates_hub_id(self):
        resource, _ = _make_resource()
        with pytest.raises(ValueError):
            resource.update_role("", "role-1", name="x")

    def test_update_role_validates_role_id(self):
        resource, _ = _make_resource()
        with pytest.raises(ValueError):
            resource.update_role("hub-1", "", name="x")


class TestHubRolesDelete:
    def test_delete_role(self):
        resource, mock = _make_resource()
        mock._request.return_value = None

        resource.delete_role("hub-1", "role-1")

        args = mock._request.call_args
        assert args[0] == ("DELETE", "/hubs/hub-1/roles/role-1")

    def test_delete_role_validates_hub_id(self):
        resource, _ = _make_resource()
        with pytest.raises(ValueError):
            resource.delete_role("", "role-1")

    def test_delete_role_validates_role_id(self):
        resource, _ = _make_resource()
        with pytest.raises(ValueError):
            resource.delete_role("hub-1", "")


class TestConversationRoleOverrides:
    def test_list_role_overrides(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"data": [OVERRIDE_DATA]}

        result = resource.list_role_overrides("conv-1")

        assert len(result) == 1
        assert isinstance(result[0], ConvRoleOverride)
        assert result[0].permissions == {"send_messages": "deny"}
        args = mock._request.call_args
        assert args[0] == ("GET", "/conversations/conv-1/role-overrides")

    def test_upsert_role_override(self):
        resource, mock = _make_resource()
        mock._request.return_value = OVERRIDE_DATA

        result = resource.upsert_role_override(
            "conv-1", "role-1", permissions={"send_messages": "deny"}
        )

        assert isinstance(result, ConvRoleOverride)
        assert result.role_id == "role-1"
        args = mock._request.call_args
        assert args[0] == ("PUT", "/conversations/conv-1/role-overrides/role-1")
        assert args[1]["json"]["permissions"]["send_messages"] == "deny"

    def test_delete_role_override(self):
        resource, mock = _make_resource()
        mock._request.return_value = None

        resource.delete_role_override("conv-1", "role-1")

        args = mock._request.call_args
        assert args[0] == ("DELETE", "/conversations/conv-1/role-overrides/role-1")
