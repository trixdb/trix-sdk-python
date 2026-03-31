"""Invite resource tests."""

from unittest.mock import Mock, patch

import pytest

from trix import AsyncTrix
from trix.resources.invites import InvitesResource
from trix.types.invite import InviteCreateResult, InviteList, InviteAcceptResult, InviteRevokeResult

NOW = "2026-03-20T00:00:00Z"

INVITE_DATA = {
    "id": "inv-1",
    "email": "user@example.com",
    "role": "member",
    "token": "tok-abc",
    "expires_at": NOW,
    "accepted_at": None,
    "created_at": NOW,
    "invited_by": "user-1",
}


def _make_resource() -> tuple[InvitesResource, Mock]:
    mock_client = Mock()
    resource = InvitesResource(mock_client)
    return resource, mock_client


class TestInvitesCreate:
    def test_create(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"message": "Invite sent", "invite": INVITE_DATA}

        result = resource.create(email="user@example.com", role="member")

        assert isinstance(result, InviteCreateResult)
        assert result.invite.email == "user@example.com"
        assert result.invite.token == "tok-abc"
        args = mock._request.call_args
        assert args[0] == ("POST", "/accounts/invites")

    def test_create_with_expiry(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"message": "Invite sent", "invite": INVITE_DATA}

        resource.create(email="user@example.com", role="admin", expires_in_days=14)

        args = mock._request.call_args
        body = args[1]["json"]
        assert body["expires_in_days"] == 14
        assert body["role"] == "admin"

    @pytest.mark.asyncio
    async def test_create_async(self):
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = {"message": "Invite sent", "invite": INVITE_DATA}
            client = AsyncTrix(api_key="test_key")

            result = await client.invites.create(email="user@example.com", role="member")

            assert isinstance(result, InviteCreateResult)
            assert result.invite.email == "user@example.com"
            await client.close()


class TestInvitesList:
    def test_list_default(self):
        resource, mock = _make_resource()
        mock._request.return_value = {
            "invites": [INVITE_DATA],
            "pagination": {"limit": 50, "offset": 0, "has_more": False},
        }

        result = resource.list()

        assert isinstance(result, InviteList)
        assert len(result.invites) == 1
        args = mock._request.call_args
        assert args[1]["params"]["limit"] == 50

    def test_list_with_status(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"invites": [], "pagination": None}

        resource.list(status="accepted", limit=10)

        args = mock._request.call_args
        assert args[1]["params"]["status"] == "accepted"
        assert args[1]["params"]["limit"] == 10


class TestInvitesRevoke:
    def test_revoke(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"message": "Revoked", "id": "inv-1"}

        result = resource.revoke("inv-1")

        assert isinstance(result, InviteRevokeResult)
        assert result.id == "inv-1"
        args = mock._request.call_args
        assert args[0] == ("DELETE", "/accounts/invites/inv-1")

    def test_revoke_validates_id(self):
        resource, _ = _make_resource()
        with pytest.raises(ValueError):
            resource.revoke("")


class TestInvitesAccept:
    def test_accept(self):
        resource, mock = _make_resource()
        mock._request.return_value = {
            "message": "Welcome",
            "user": {"id": "u-1", "email": "user@example.com", "name": "User"},
            "account": {"id": "acc-1", "name": "Acme", "role": "member"},
        }

        result = resource.accept("tok-abc", name="User", password="pass123")

        assert isinstance(result, InviteAcceptResult)
        assert result.user["id"] == "u-1"
        args = mock._request.call_args
        assert "/accounts/invites/tok-abc/accept" in args[0][1]

    def test_accept_without_params(self):
        resource, mock = _make_resource()
        mock._request.return_value = {
            "message": "Welcome",
            "user": {"id": "u-1", "email": "user@example.com", "name": "User"},
            "account": {"id": "acc-1", "name": "Acme", "role": "member"},
        }

        resource.accept("tok-abc")

        args = mock._request.call_args
        assert args[1]["json"] is None
