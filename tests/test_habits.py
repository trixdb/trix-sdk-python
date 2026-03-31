"""Habit resource tests (ADR-034)."""

from datetime import datetime
from unittest.mock import Mock

import pytest

from trix.resources.habits import HabitsResource
from trix.types.habit import (
    CheckInResult,
    DueHabitsResult,
    Habit,
    HabitHistoryResult,
    HabitList,
    StreakInfo,
)

NOW = datetime.utcnow().isoformat() + "Z"

HABIT_DATA = {
    "id": "h-1",
    "account_id": "acc-1",
    "name": "Meditate",
    "habit_type": "boolean",
    "frequency": "daily",
    "status": "active",
    "timezone": "UTC",
    "grace_days": 1,
    "streak": {"current": 5, "longest": 12},
    "created_at": NOW,
    "updated_at": NOW,
}

COMPLETION_DATA = {
    "id": "c-1",
    "habit_id": "h-1",
    "completed_date": "2026-02-24",
    "value": 1.0,
    "source": "explicit",
    "created_at": NOW,
}

STREAK_DATA = {"current": 5, "longest": 12}


def _make_resource() -> tuple[HabitsResource, Mock]:
    mock_client = Mock()
    resource = HabitsResource(mock_client)
    return resource, mock_client


class TestHabitsCreate:
    def test_create_basic(self):
        resource, mock = _make_resource()
        mock._request.return_value = HABIT_DATA

        result = resource.create(name="Meditate")

        assert isinstance(result, Habit)
        assert result.id == "h-1"
        assert result.name == "Meditate"
        mock._request.assert_called_once()
        args = mock._request.call_args
        assert args[0] == ("POST", "/habits")

    def test_create_with_options(self):
        resource, mock = _make_resource()
        mock._request.return_value = HABIT_DATA

        resource.create(
            name="Water",
            habit_type="numeric",
            target_value=8,
            target_unit="glasses",
            grace_days=2,
        )

        args = mock._request.call_args
        body = args[1]["json"]
        assert body["name"] == "Water"
        assert body["habit_type"] == "numeric"
        assert body["target_value"] == 8
        assert body["grace_days"] == 2


class TestHabitsList:
    def test_list_default(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"habits": [HABIT_DATA], "pagination": {"total": 1}}

        result = resource.list()

        assert isinstance(result, HabitList)
        assert len(result.habits) == 1
        args = mock._request.call_args
        assert args[1]["params"]["limit"] == 50

    def test_list_with_filters(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"habits": [], "pagination": {"total": 0}}

        resource.list(status="paused", space_id="sp-1")

        args = mock._request.call_args
        assert args[1]["params"]["status"] == "paused"
        assert args[1]["params"]["space_id"] == "sp-1"


class TestHabitsGet:
    def test_get(self):
        resource, mock = _make_resource()
        mock._request.return_value = HABIT_DATA

        result = resource.get("h-1")

        assert isinstance(result, Habit)
        assert result.id == "h-1"
        mock._request.assert_called_once()
        args = mock._request.call_args
        assert args[0] == ("GET", "/habits/h-1")

    def test_get_validates_id(self):
        resource, _ = _make_resource()
        with pytest.raises(ValueError):
            resource.get("")


class TestHabitsUpdate:
    def test_update(self):
        resource, mock = _make_resource()
        mock._request.return_value = {**HABIT_DATA, "name": "Morning Meditation"}

        result = resource.update("h-1", name="Morning Meditation", grace_days=2)

        assert result.name == "Morning Meditation"
        args = mock._request.call_args
        assert args[0] == ("PATCH", "/habits/h-1")
        body = args[1]["json"]
        assert body["name"] == "Morning Meditation"
        assert body["grace_days"] == 2


class TestHabitsDelete:
    def test_delete(self):
        resource, mock = _make_resource()
        mock._request.return_value = None

        resource.delete("h-1")

        mock._request.assert_called_once()
        args = mock._request.call_args
        assert args[0] == ("DELETE", "/habits/h-1")


class TestHabitsCheckIn:
    def test_check_in(self):
        resource, mock = _make_resource()
        mock._request.return_value = {
            "completion": COMPLETION_DATA,
            "streak": STREAK_DATA,
        }

        result = resource.check_in("h-1", value=1.0)

        assert isinstance(result, CheckInResult)
        assert isinstance(result.streak, StreakInfo)
        assert result.streak.current == 5
        args = mock._request.call_args
        assert "/habits/h-1/check-in" in args[0][1]

    def test_check_in_with_date(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"completion": COMPLETION_DATA, "streak": STREAK_DATA}

        resource.check_in("h-1", date="2026-02-23", note="Morning session")

        args = mock._request.call_args
        body = args[1]["json"]
        assert body["date"] == "2026-02-23"
        assert body["note"] == "Morning session"


class TestHabitsUncheck:
    def test_uncheck(self):
        resource, mock = _make_resource()
        mock._request.return_value = None

        resource.uncheck("h-1", "2026-02-23")

        mock._request.assert_called_once()
        args = mock._request.call_args
        assert args[0] == ("DELETE", "/habits/h-1/check-in/2026-02-23")


class TestHabitsHistory:
    def test_history(self):
        resource, mock = _make_resource()
        mock._request.return_value = {
            "completions": [COMPLETION_DATA],
            "streak": STREAK_DATA,
        }

        result = resource.history("h-1")

        assert isinstance(result, HabitHistoryResult)
        assert len(result.completions) == 1
        args = mock._request.call_args
        assert "/habits/h-1/history" in args[0][1]

    def test_history_with_date_range(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"completions": [], "streak": STREAK_DATA}

        resource.history("h-1", start_date="2026-01-01", end_date="2026-02-24")

        args = mock._request.call_args
        assert args[1]["params"]["start_date"] == "2026-01-01"


class TestHabitsDue:
    def test_due_today(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"habits": [HABIT_DATA], "date": "2026-02-24"}

        result = resource.due()

        assert isinstance(result, DueHabitsResult)
        assert len(result.habits) == 1
        args = mock._request.call_args
        assert args[1].get("params") is None

    def test_due_specific_date(self):
        resource, mock = _make_resource()
        mock._request.return_value = {"habits": [], "date": "2026-03-01"}

        resource.due(date="2026-03-01")

        args = mock._request.call_args
        assert args[1]["params"]["date"] == "2026-03-01"


class TestHabitsPauseResume:
    def test_pause(self):
        resource, mock = _make_resource()
        mock._request.return_value = {**HABIT_DATA, "status": "paused"}

        result = resource.pause("h-1")

        assert result.status == "paused"
        mock._request.assert_called_once()
        args = mock._request.call_args
        assert args[0] == ("POST", "/habits/h-1/pause")

    def test_resume(self):
        resource, mock = _make_resource()
        mock._request.return_value = HABIT_DATA

        result = resource.resume("h-1")

        assert result.status == "active"
        mock._request.assert_called_once()
        args = mock._request.call_args
        assert args[0] == ("POST", "/habits/h-1/resume")
