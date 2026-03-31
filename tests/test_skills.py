"""Skill resource tests."""

from unittest.mock import Mock, patch

import pytest

from trix import AsyncTrix
from trix.resources.skills import SkillsResource
from trix.types.skill import BotSkillAttachment, Skill

NOW = "2026-03-20T00:00:00Z"

SKILL_DATA = {
    "id": "sk-1",
    "name": "code-review",
    "slug": "code-review",
    "description": "Review code for best practices.",
    "content": "# Instructions",
    "status": "draft",
    "created_at": NOW,
    "updated_at": NOW,
}

ATTACHMENT_DATA = {
    "skill_id": "sk-1",
    "bot_id": "bot-1",
    "enabled": True,
    "priority": 1,
}


def _make_resource() -> tuple[SkillsResource, Mock]:
    mock_client = Mock()
    resource = SkillsResource(mock_client)
    return resource, mock_client


class TestSkillsCreate:
    def test_create(self):
        resource, mock = _make_resource()
        mock._request.return_value = SKILL_DATA

        result = resource.create(name="code-review", description="Review code.")

        assert isinstance(result, Skill)
        assert result.id == "sk-1"
        args = mock._request.call_args
        assert args[0] == ("POST", "/skills")
        assert args[1]["json"]["name"] == "code-review"

    @pytest.mark.asyncio
    async def test_create_async(self):
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = SKILL_DATA
            client = AsyncTrix(api_key="test_key")

            result = await client.skills.create(name="code-review")

            assert isinstance(result, Skill)
            assert result.name == "code-review"
            await client.close()


class TestSkillsList:
    def test_list(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"skills": [SKILL_DATA]}

        result = resource.list()

        assert len(result) == 1
        assert isinstance(result[0], Skill)
        args = mock._request.call_args
        assert args[0] == ("GET", "/skills")


class TestSkillsGet:
    def test_get_by_id(self):
        resource, mock = _make_resource()
        mock._request.return_value = SKILL_DATA

        result = resource.get("sk-1")

        assert isinstance(result, Skill)
        assert result.id == "sk-1"
        args = mock._request.call_args
        assert args[0] == ("GET", "/skills/sk-1")

    def test_get_by_slug(self):
        resource, mock = _make_resource()
        mock._request.return_value = SKILL_DATA

        result = resource.get("code-review")

        assert isinstance(result, Skill)
        args = mock._request.call_args
        assert args[0] == ("GET", "/skills/code-review")


class TestSkillsUpdate:
    def test_update(self):
        resource, mock = _make_resource()
        mock._request.return_value = {**SKILL_DATA, "name": "updated"}

        result = resource.update("sk-1", name="updated")

        assert result.name == "updated"
        args = mock._request.call_args
        assert args[0] == ("PATCH", "/skills/sk-1")
        assert args[1]["json"]["name"] == "updated"

    def test_update_validates_id(self):
        resource, _ = _make_resource()
        with pytest.raises(ValueError):
            resource.update("", name="x")


class TestSkillsDelete:
    def test_delete(self):
        resource, mock = _make_resource()
        mock._request.return_value = None

        resource.delete("sk-1")

        args = mock._request.call_args
        assert args[0] == ("DELETE", "/skills/sk-1")

    def test_delete_validates_id(self):
        resource, _ = _make_resource()
        with pytest.raises(ValueError):
            resource.delete("")


class TestSkillsPublish:
    def test_publish(self):
        resource, mock = _make_resource()
        mock._request.return_value = {**SKILL_DATA, "status": "published"}

        result = resource.publish("sk-1")

        assert isinstance(result, Skill)
        args = mock._request.call_args
        assert args[0] == ("POST", "/skills/sk-1/publish")


class TestSkillsInstall:
    def test_install(self):
        resource, mock = _make_resource()
        mock._request.return_value = SKILL_DATA

        result = resource.install("sk-1")

        assert isinstance(result, Skill)
        args = mock._request.call_args
        assert args[0] == ("POST", "/skills/sk-1/install")


class TestSkillsMarketplace:
    def test_marketplace_search(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"skills": [SKILL_DATA]}

        result = resource.marketplace(q="code")

        assert len(result) == 1
        args = mock._request.call_args
        assert args[0] == ("GET", "/skills/marketplace")
        assert args[1]["params"]["q"] == "code"


class TestSkillsBotAttachments:
    def test_attach_to_bot(self):
        resource, mock = _make_resource()
        mock._request.return_value = ATTACHMENT_DATA

        result = resource.attach_to_bot("sk-1", bot_id="bot-1")

        assert isinstance(result, BotSkillAttachment)
        assert result.bot_id == "bot-1"
        args = mock._request.call_args
        assert args[0] == ("POST", "/skills/sk-1/bots")

    def test_detach_from_bot(self):
        resource, mock = _make_resource()
        mock._request.return_value = None

        resource.detach_from_bot("sk-1", "bot-1")

        args = mock._request.call_args
        assert args[0] == ("DELETE", "/skills/sk-1/bots/bot-1")

    def test_list_bots(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"bots": [ATTACHMENT_DATA]}

        result = resource.list_bots("sk-1")

        assert len(result) == 1
        assert isinstance(result[0], BotSkillAttachment)
