"""Transcript-related types for Trix SDK."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .base import BaseResponse


class TimestampRange(BaseModel):
    """Timestamp range for content safety labels."""

    start: float
    end: float


class ContentSafetyLabel(BaseModel):
    """Content safety detection result."""

    label: str
    confidence: float
    severity: str
    timestamp: Optional[TimestampRange] = None


class WordTimestamp(BaseModel):
    """Word-level timestamp with optional speaker label."""

    word: str
    start: float
    end: float
    confidence: Optional[float] = None
    speaker: Optional[str] = None


class TranscriptSegment(BaseModel):
    """Transcript segment with speaker information and word-level details."""

    id: Optional[str] = None
    start_time: float
    end_time: float
    text: str
    segment_index: int
    confidence: Optional[float] = None
    speaker: Optional[str] = None
    words: Optional[List[WordTimestamp]] = None
    word_confidence_avg: Optional[float] = None


class TranscriptEntity(BaseModel):
    """Detected entity in transcript."""

    id: Optional[str] = None
    entity_type: str
    text: str
    start_time: float
    end_time: float
    confidence: float
    metadata: Optional[Dict[str, Any]] = None


class TranscriptChapter(BaseModel):
    """Auto-generated chapter."""

    id: Optional[str] = None
    chapter_index: int
    headline: str
    summary: str
    gist: str
    start_time: float
    end_time: float


class Transcript(BaseResponse):
    """Full transcript with metadata, segments, entities, and chapters."""

    memory_id: str
    audio_file_id: Optional[str] = None
    text: str
    duration: Optional[float] = None
    language: Optional[str] = None
    language_confidence: Optional[float] = None
    provider: Optional[str] = None
    summary: Optional[str] = None
    content_safety_labels: Optional[List[ContentSafetyLabel]] = None
    provider_metadata: Optional[Dict[str, Any]] = None
    segments: Optional[List[TranscriptSegment]] = None
    entities: Optional[List[TranscriptEntity]] = None
    chapters: Optional[List[TranscriptChapter]] = None
    words: Optional[List[WordTimestamp]] = None
