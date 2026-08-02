"""Agent preset resource tests."""

from unittest.mock import Mock

import pytest

from tests.support import spec_client
from trix.resources.presets import PresetsResource
from trix.types.preset import AgentPreset, AgentPresetList

NOW = "2026-03-20T00:00:00Z"

PRESET_DATA = {
    "id": "ap-1",
    "name": "Fast Research",
    "slug": "fast-research",
    "description": "Quick research preset",
    "is_system": False,
    "provider": "openai",
    "model": "gpt-4.1",
    "temperature": 0.7,
    "max_tokens": 4096,
    "created_at": NOW,
    "updated_at": NOW,
}


def _make_resource() -> tuple[PresetsResource, Mock]:
    mock_client = spec_client()
    resource = PresetsResource(mock_client)
    return resource, mock_client


class TestPresetsList:
    def test_list(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"presets": [PRESET_DATA]}

        result = resource.list()

        assert isinstance(result, AgentPresetList)
        assert len(result.presets) == 1
        assert isinstance(result.presets[0], AgentPreset)
        args = mock._request.call_args
        assert args[0] == ("GET", "/agent-presets")

    def test_list_with_include_system(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"presets": [PRESET_DATA]}

        resource.list(include_system=False)

        args = mock._request.call_args
        assert args[1]["params"]["include_system"] is False


class TestPresetsGet:
    def test_get_by_id(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"preset": PRESET_DATA}

        result = resource.get("ap-1")

        assert isinstance(result, AgentPreset)
        assert result.id == "ap-1"
        args = mock._request.call_args
        assert args[0] == ("GET", "/agent-presets/ap-1")

    def test_get_by_slug(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"preset": PRESET_DATA}

        result = resource.get("fast-research")

        assert isinstance(result, AgentPreset)
        assert result.slug == "fast-research"
        args = mock._request.call_args
        assert args[0] == ("GET", "/agent-presets/fast-research")


class TestPresetsCreate:
    def test_create(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"preset": PRESET_DATA}

        result = resource.create(name="Fast Research", provider="openai", model="gpt-4.1")

        assert isinstance(result, AgentPreset)
        assert result.name == "Fast Research"
        args = mock._request.call_args
        assert args[0] == ("POST", "/agent-presets")
        assert args[1]["json"]["name"] == "Fast Research"
        assert args[1]["json"]["provider"] == "openai"

    def test_create_minimal(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"preset": PRESET_DATA}

        result = resource.create(name="Fast Research")

        assert isinstance(result, AgentPreset)
        args = mock._request.call_args
        assert args[1]["json"]["name"] == "Fast Research"


class TestPresetsUpdate:
    def test_update(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"preset": {**PRESET_DATA, "name": "Slow Research"}}

        result = resource.update("ap-1", name="Slow Research")

        assert result.name == "Slow Research"
        args = mock._request.call_args
        assert args[0] == ("PATCH", "/agent-presets/ap-1")
        assert args[1]["json"]["name"] == "Slow Research"

    def test_update_validates_id(self):
        resource, _ = _make_resource()
        with pytest.raises(ValueError):
            resource.update("", name="x")


class TestPresetsDelete:
    def test_delete(self):
        resource, mock = _make_resource()
        mock._request.return_value = None

        resource.delete("ap-1")

        args = mock._request.call_args
        assert args[0] == ("DELETE", "/agent-presets/ap-1")

    def test_delete_validates_id(self):
        resource, _ = _make_resource()
        with pytest.raises(ValueError):
            resource.delete("")
