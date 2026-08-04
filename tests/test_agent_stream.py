"""ADR-121 agent streaming event type tests — iter 104."""

import pytest

from trix.types.agent_stream import (
    ALL_EVENT_TYPES,
    AgentStreamEvent,
    BudgetStateEvent,
    ContentDeltaEvent,
    MessageStopEvent,
    StopEvent,
    StreamErrorEvent,
    ToolResultEvent,
    ToolUseStartEvent,
    parse_agent_event,
)


class TestParseContentDelta:
    def test_basic(self):
        ev = parse_agent_event({"type": "content_delta", "delta": "hello", "contentIndex": 0})
        assert isinstance(ev, ContentDeltaEvent)
        assert ev.delta == "hello"

    def test_default_content_index(self):
        ev = parse_agent_event({"type": "content_delta", "delta": "x"})
        assert isinstance(ev, ContentDeltaEvent)
        assert ev.content_index == 0


class TestParseMessageStop:
    def test_basic(self):
        ev = parse_agent_event(
            {
                "type": "message_stop",
                "stopReason": "end_turn",
                "usage": {"input_tokens": 100, "output_tokens": 50},
            }
        )
        assert isinstance(ev, MessageStopEvent)
        assert ev.stop_reason == "end_turn"
        assert ev.usage.output_tokens == 50


class TestParseBudgetState:
    def test_basic(self):
        ev = parse_agent_event(
            {
                "type": "budget_state",
                "spent": {"tokens": 5000, "usd": 0.25},
                "band": "ok",
                "pct": 0.1,
            }
        )
        assert isinstance(ev, BudgetStateEvent)
        assert ev.band == "ok"
        assert ev.spent.tokens == 5000

    def test_warn_band(self):
        ev = parse_agent_event(
            {
                "type": "budget_state",
                "spent": {"tokens": 8000, "usd": 4.5},
                "band": "warn",
                "pct": 0.85,
            }
        )
        assert ev.band == "warn"
        assert ev.pct == pytest.approx(0.85)


class TestParseToolResult:
    def test_basic(self):
        ev = parse_agent_event(
            {
                "type": "tool_result",
                "toolUseId": "t1",
                "output": "file content",
                "isError": False,
            }
        )
        assert isinstance(ev, ToolResultEvent)
        assert ev.tool_use_id == "t1"
        assert ev.output == "file content"
        assert ev.is_error is False

    def test_error_result(self):
        ev = parse_agent_event(
            {
                "type": "tool_result",
                "toolUseId": "t2",
                "output": "command not found",
                "isError": True,
            }
        )
        assert ev.is_error is True


class TestParseError:
    def test_basic(self):
        ev = parse_agent_event(
            {
                "type": "error",
                "error": {"code": "E001", "message": "something bad"},
            }
        )
        assert isinstance(ev, StreamErrorEvent)
        assert ev.error["message"] == "something bad"


class TestParseStop:
    def test_basic(self):
        ev = parse_agent_event({"type": "stop", "reason": "end_turn"})
        assert isinstance(ev, StopEvent)
        assert ev.reason == "end_turn"


class TestParseToolUseStart:
    def test_basic(self):
        ev = parse_agent_event({"type": "tool_use_start", "toolUseId": "t1", "name": "Read"})
        assert isinstance(ev, ToolUseStartEvent)
        assert ev.name == "Read"
        assert ev.tool_use_id == "t1"


class TestUnknownEvent:
    def test_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown"):
            parse_agent_event({"type": "not_a_real_event"})


class TestAllEventTypes:
    def test_exhaustive_count(self):
        assert len(ALL_EVENT_TYPES) == 21

    def test_no_duplicates(self):
        assert len(set(ALL_EVENT_TYPES)) == 21

    def test_each_parseable(self):
        """Every event type in ALL_EVENT_TYPES has a parser entry."""
        # Minimal payloads per type to exercise the parser map.
        minimal = {
            "message_start": {
                "message": {"id": "1", "model": "m"},
                "usage": {"input_tokens": 0, "output_tokens": 0},
            },
            "content_delta": {"delta": "x"},
            "thinking_delta": {"delta": "x"},
            "tool_use_start": {"toolUseId": "t", "name": "n"},
            "tool_use_delta": {"toolUseId": "t", "inputDelta": "x"},
            "tool_result": {"toolUseId": "t", "output": None},
            "message_stop": {
                "stopReason": "end_turn",
                "usage": {"input_tokens": 0, "output_tokens": 0},
            },
            "memory_retrieved": {"memoryIds": [], "latencyMs": 0, "timedOut": False},
            "memory_cited": {"memoryId": "m"},
            "memory_consolidated": {"newFacts": 0, "reinforced": 0, "weakened": 0},
            "stage_start": {"stage": "x"},
            "stage_end": {"stage": "x", "status": "ok"},
            "budget_state": {"spent": {"tokens": 0, "usd": 0}, "band": "ok", "pct": 0},
            "budget_warning": {"remaining": {}},
            "cache_report": {"hit": True, "hitRate": 0.5},
            "retry_attempt": {"provider": "p", "attempt": 1, "reason": "r"},
            "permission_request": {"tool": "t", "input": None},
            "web_search_status": {"status": "started"},
            "sources": {"sources": []},
            "stop": {"reason": "end_turn"},
            "error": {"error": {"code": "E", "message": "m"}},
        }
        for et in ALL_EVENT_TYPES:
            payload = {"type": et, **minimal[et]}
            ev = parse_agent_event(payload)
            assert ev.type == et
