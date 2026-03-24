"""Tests for HubsResource."""

from unittest.mock import Mock

from trix.resources.hubs import HubsResource


MEMBER_RESPONSE = {
    "id": "hm_001",
    "hub_id": "hub_123",
    "user_id": "user_456",
    "role": "member",
    "permissions": None,
    "name": "Alice",
    "email": "alice@example.com",
}

MEMBER_LIST_RESPONSE = {
    "data": [MEMBER_RESPONSE],
}

UPDATED_MEMBER_RESPONSE = {
    **MEMBER_RESPONSE,
    "role": "admin",
    "permissions": {"manage_members": True},
}


class TestHubsListMembers:
    """Tests for hubs.list_members()."""

    def test_list_members(self):
        """Test listing all hub members."""
        mock_client = Mock()
        mock_client._request.return_value = MEMBER_LIST_RESPONSE

        resource = HubsResource(mock_client)
        result = resource.list_members("hub_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/hubs/hub_123/members")
        assert len(result) == 1
        assert result[0].id == "hm_001"
        assert result[0].user_id == "user_456"
        assert result[0].role == "member"

    def test_list_members_empty(self):
        """Test listing when no members exist."""
        mock_client = Mock()
        mock_client._request.return_value = {"data": []}

        resource = HubsResource(mock_client)
        result = resource.list_members("hub_123")

        assert len(result) == 0


class TestHubsAddMember:
    """Tests for hubs.add_member()."""

    def test_add_member_default_role(self):
        """Test adding a member with default role."""
        mock_client = Mock()
        mock_client._request.return_value = MEMBER_RESPONSE

        resource = HubsResource(mock_client)
        result = resource.add_member("hub_123", user_id="user_456")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/hubs/hub_123/members")
        body = call_args[1]["json"]
        assert body["user_id"] == "user_456"
        assert body["role"] == "member"
        assert result.user_id == "user_456"

    def test_add_member_with_role_and_permissions(self):
        """Test adding a member with custom role and permissions."""
        mock_client = Mock()
        mock_client._request.return_value = UPDATED_MEMBER_RESPONSE

        resource = HubsResource(mock_client)
        resource.add_member(
            "hub_123",
            user_id="user_456",
            role="admin",
            permissions={"manage_members": True},
        )

        call_args = mock_client._request.call_args
        body = call_args[1]["json"]
        assert body["role"] == "admin"
        assert body["permissions"] == {"manage_members": True}


class TestHubsUpdateMember:
    """Tests for hubs.update_member()."""

    def test_update_member_role(self):
        """Test updating a hub member's role."""
        mock_client = Mock()
        mock_client._request.return_value = UPDATED_MEMBER_RESPONSE

        resource = HubsResource(mock_client)
        result = resource.update_member("hub_123", "user_456", role="admin")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("PATCH", "/hubs/hub_123/members/user_456")
        body = call_args[1]["json"]
        assert body["role"] == "admin"
        assert result.role == "admin"


class TestHubsRemoveMember:
    """Tests for hubs.remove_member()."""

    def test_remove_member(self):
        """Test removing a member from a hub."""
        mock_client = Mock()
        mock_client._request.return_value = None

        resource = HubsResource(mock_client)
        resource.remove_member("hub_123", "user_456")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("DELETE", "/hubs/hub_123/members/user_456")


class TestHubsConversationMembers:
    """Tests for conversation member operations."""

    def test_list_conversation_members(self):
        """Test listing conversation members."""
        mock_client = Mock()
        mock_client._request.return_value = {
            "data": [
                {
                    "id": "cm_001",
                    "conversation_id": "conv_123",
                    "user_id": "user_456",
                    "role": "participant",
                    "is_agent": False,
                }
            ],
        }

        resource = HubsResource(mock_client)
        result = resource.list_conversation_members("conv_123")

        call_args = mock_client._request.call_args
        assert call_args[0] == ("GET", "/conversations/conv_123/members")
        assert len(result) == 1
        assert result[0].role == "participant"
