"""Crew resource tests."""

from unittest.mock import Mock

import pytest

from trix.resources.crews import CrewsResource
from trix.types.crew import Crew, CrewList

NOW = "2026-03-20T00:00:00Z"

CREW_DATA = {
    "id": "crew-1",
    "account_id": "acc-1",
    "name": "Research Team",
    "slug": "research-team",
    "description": "A team of research bots",
    "strategy": "sequential",
    "members": [],
    "settings": {},
    "metadata": {},
    "status": "active",
    "created_at": NOW,
    "updated_at": NOW,
}


def _make_resource() -> tuple[CrewsResource, Mock]:
    mock_client = Mock()
    resource = CrewsResource(mock_client)
    return resource, mock_client


class TestCrewsList:
    def test_list(self):
        resource, mock = _make_resource()
        mock._request.return_value = {
            "crews": [CREW_DATA],
            "total": 1,
            "limit": 20,
            "offset": 0,
        }

        result = resource.list()

        assert isinstance(result, CrewList)
        assert len(result.crews) == 1
        assert isinstance(result.crews[0], Crew)
        args = mock._request.call_args
        assert args[0] == ("GET", "/crews")
        assert args[1]["params"]["limit"] == 20
        assert args[1]["params"]["offset"] == 0

    def test_list_with_status_filter(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"crews": [], "total": 0}

        resource.list(status="archived")

        args = mock._request.call_args
        assert args[1]["params"]["status"] == "archived"


class TestCrewsGet:
    def test_get(self):
        resource, mock = _make_resource()
        mock._request.return_value = CREW_DATA

        result = resource.get("crew-1")

        assert isinstance(result, Crew)
        assert result.id == "crew-1"
        assert result.name == "Research Team"
        args = mock._request.call_args
        assert args[0] == ("GET", "/crews/crew-1")

    def test_get_validates_id(self):
        resource, _ = _make_resource()
        with pytest.raises(ValueError):
            resource.get("")


class TestCrewsCreate:
    def test_create(self):
        resource, mock = _make_resource()
        mock._request.return_value = CREW_DATA

        result = resource.create(name="Research Team", description="A team of research bots")

        assert isinstance(result, Crew)
        assert result.name == "Research Team"
        args = mock._request.call_args
        assert args[0] == ("POST", "/crews")
        assert args[1]["json"]["name"] == "Research Team"
        assert args[1]["json"]["description"] == "A team of research bots"

    def test_create_minimal(self):
        resource, mock = _make_resource()
        mock._request.return_value = CREW_DATA

        result = resource.create(name="Research Team")

        assert isinstance(result, Crew)
        args = mock._request.call_args
        assert args[1]["json"]["name"] == "Research Team"


class TestCrewsUpdate:
    def test_update(self):
        resource, mock = _make_resource()
        mock._request.return_value = {**CREW_DATA, "name": "Updated Team"}

        result = resource.update("crew-1", name="Updated Team")

        assert result.name == "Updated Team"
        args = mock._request.call_args
        assert args[0] == ("PATCH", "/crews/crew-1")
        assert args[1]["json"]["name"] == "Updated Team"

    def test_update_validates_id(self):
        resource, _ = _make_resource()
        with pytest.raises(ValueError):
            resource.update("", name="x")


class TestCrewsDelete:
    def test_delete(self):
        resource, mock = _make_resource()
        mock._request.return_value = None

        resource.delete("crew-1")

        args = mock._request.call_args
        assert args[0] == ("DELETE", "/crews/crew-1")

    def test_delete_validates_id(self):
        resource, _ = _make_resource()
        with pytest.raises(ValueError):
            resource.delete("")
