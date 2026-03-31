"""Tests for SSE (Server-Sent Events) parsing utilities."""

import pytest

from trix.utils.sse import MAX_SSE_LINE_SIZE, iter_sse_lines, parse_sse_line


class TestParseSSELine:
    """Tests for parse_sse_line function."""

    def test_valid_json_data(self):
        """Test parsing a valid JSON data line."""
        result = parse_sse_line('data: {"event": "message", "content": "hello"}')
        assert result == {"event": "message", "content": "hello"}

    def test_nested_json_data(self):
        """Test parsing nested JSON data."""
        result = parse_sse_line('data: {"user": {"name": "test"}, "count": 42}')
        assert result == {"user": {"name": "test"}, "count": 42}

    def test_invalid_json_returns_none(self):
        """Test invalid JSON data returns None."""
        result = parse_sse_line("data: {not valid json}")
        assert result is None

    def test_done_signal_returns_none(self):
        """Test [DONE] signal returns None."""
        result = parse_sse_line("data: [DONE]")
        assert result is None

    def test_empty_line_returns_none(self):
        """Test empty line returns None."""
        assert parse_sse_line("") is None
        assert parse_sse_line("   ") is None

    def test_comment_line_returns_none(self):
        """Test SSE comment (colon prefix) returns None."""
        assert parse_sse_line(": this is a comment") is None

    def test_non_data_line_returns_none(self):
        """Test non-data lines return None."""
        assert parse_sse_line("event: message") is None
        assert parse_sse_line("id: 123") is None
        assert parse_sse_line("retry: 5000") is None

    def test_data_with_non_dict_json_returns_none(self):
        """Test data with non-dict JSON (e.g. array) returns None."""
        assert parse_sse_line("data: [1, 2, 3]") is None
        assert parse_sse_line('data: "just a string"') is None

    def test_whitespace_around_line(self):
        """Test line with surrounding whitespace is handled."""
        result = parse_sse_line('  data: {"key": "value"}  ')
        assert result == {"key": "value"}


class TestIterSSELines:
    """Tests for iter_sse_lines function."""

    def test_normal_data(self):
        """Test iterating over normal SSE data chunks."""
        chunks = [b'data: {"a": 1}\n', b'data: {"b": 2}\n']
        lines = list(iter_sse_lines(iter(chunks)))
        assert lines == ['data: {"a": 1}', 'data: {"b": 2}']

    def test_multi_chunk_lines(self):
        """Test lines split across multiple chunks."""
        chunks = [b'data: {"ke', b'y": "val', b'ue"}\n']
        lines = list(iter_sse_lines(iter(chunks)))
        assert lines == ['data: {"key": "value"}']

    def test_multiple_lines_in_single_chunk(self):
        """Test multiple lines within a single chunk."""
        chunks = [b'data: {"a": 1}\ndata: {"b": 2}\n']
        lines = list(iter_sse_lines(iter(chunks)))
        assert lines == ['data: {"a": 1}', 'data: {"b": 2}']

    def test_empty_lines_skipped(self):
        """Test empty lines are skipped."""
        chunks = [b'data: {"a": 1}\n\n\ndata: {"b": 2}\n']
        lines = list(iter_sse_lines(iter(chunks)))
        assert lines == ['data: {"a": 1}', 'data: {"b": 2}']

    def test_trailing_data_without_newline(self):
        """Test remaining buffer data is yielded at stream end."""
        chunks = [b'data: {"final": true}']
        lines = list(iter_sse_lines(iter(chunks)))
        assert lines == ['data: {"final": true}']

    def test_empty_iterator(self):
        """Test empty iterator yields nothing."""
        lines = list(iter_sse_lines(iter([])))
        assert lines == []

    def test_buffer_overflow_protection(self):
        """Test buffer overflow raises ValueError."""
        # Create a chunk larger than MAX_SSE_LINE_SIZE
        huge_chunk = b"x" * (MAX_SSE_LINE_SIZE + 1)
        with pytest.raises(ValueError, match="exceeds maximum size"):
            list(iter_sse_lines(iter([huge_chunk])))

    def test_unicode_handling(self):
        """Test UTF-8 encoded data is decoded correctly."""
        chunks = [b'data: {"emoji": "\xe2\x9c\x93"}\n']
        lines = list(iter_sse_lines(iter(chunks)))
        assert lines == ['data: {"emoji": "\u2713"}']
