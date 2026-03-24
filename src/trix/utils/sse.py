"""SSE (Server-Sent Events) parsing utilities."""

import json
import logging
from typing import Any, Dict, Iterator, Optional

logger = logging.getLogger(__name__)

MAX_SSE_LINE_SIZE = 1_048_576  # 1MB


def parse_sse_line(line: str) -> Optional[Dict[str, Any]]:
    """Parse a single SSE event line into a dict.

    SSE format:
        event: <event_type>
        data: <json_payload>

    Args:
        line: Raw SSE line (should start with "data: ")

    Returns:
        Parsed JSON dict, or None if line is empty/comment
    """
    stripped = line.strip()
    if not stripped or stripped.startswith(":"):
        return None

    if stripped.startswith("data: "):
        payload = stripped[6:]
        if payload == "[DONE]":
            return None
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse SSE data: {payload[:100]}")
            return None

    return None


def iter_sse_lines(raw_iter: Iterator[bytes]) -> Iterator[str]:
    """Convert a byte chunk iterator into SSE line iterator.

    Handles buffering across chunk boundaries.

    Args:
        raw_iter: Iterator of raw byte chunks

    Yields:
        Complete SSE lines (without trailing newline)
    """
    buffer = ""
    for chunk in raw_iter:
        buffer += chunk.decode("utf-8", errors="replace")
        if len(buffer) > MAX_SSE_LINE_SIZE:
            raise ValueError(f"SSE line exceeds maximum size of {MAX_SSE_LINE_SIZE} bytes")
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            if line.strip():
                yield line
    # Yield any remaining data in buffer after stream ends
    if buffer.strip():
        yield buffer
