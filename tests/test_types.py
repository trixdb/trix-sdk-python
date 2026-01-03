"""Tests for Trix types."""

from datetime import datetime

from trix.types import (
    ContentSafetyLabel,
    Memory,
    MemoryCreate,
    MemoryType,
    RelationshipType,
    SearchMode,
    TimestampRange,
    Transcript,
    TranscriptChapter,
    TranscriptEntity,
    TranscriptSegment,
    WordTimestamp,
)


def test_memory_create_validation():
    """Test MemoryCreate validation."""
    memory = MemoryCreate(
        content="Test content",
        type=MemoryType.TEXT,
        tags=["test"],
    )
    assert memory.content == "Test content"
    assert memory.type == MemoryType.TEXT
    assert memory.tags == ["test"]


def test_memory_type_enum():
    """Test MemoryType enum values."""
    assert MemoryType.TEXT == "text"
    assert MemoryType.MARKDOWN == "markdown"
    assert MemoryType.URL == "url"
    assert MemoryType.AUDIO == "audio"


def test_relationship_type_enum():
    """Test RelationshipType enum values."""
    assert RelationshipType.RELATED_TO == "related_to"
    assert RelationshipType.SUPPORTS == "supports"
    assert RelationshipType.CONTRADICTS == "contradicts"


def test_search_mode_enum():
    """Test SearchMode enum values."""
    assert SearchMode.SEMANTIC == "semantic"
    assert SearchMode.KEYWORD == "keyword"
    assert SearchMode.HYBRID == "hybrid"


def test_memory_model_parsing():
    """Test Memory model parsing from dict."""
    data = {
        "id": "mem_123",
        "content": "Test content",
        "type": "text",
        "tags": ["test"],
        "metadata": {},
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z",
        "access_count": 0,
    }
    memory = Memory.model_validate(data)
    assert memory.id == "mem_123"
    assert memory.content == "Test content"
    assert isinstance(memory.created_at, datetime)


def test_timestamp_range_parsing():
    """Test TimestampRange model parsing."""
    data = {"start": 1.5, "end": 2.0}
    timestamp = TimestampRange.model_validate(data)
    assert timestamp.start == 1.5
    assert timestamp.end == 2.0


def test_content_safety_label_parsing():
    """Test ContentSafetyLabel model parsing."""
    data = {
        "label": "profanity",
        "confidence": 0.85,
        "severity": "low",
        "timestamp": {"start": 1.5, "end": 2.0},
    }
    label = ContentSafetyLabel.model_validate(data)
    assert label.label == "profanity"
    assert label.confidence == 0.85
    assert label.severity == "low"
    assert label.timestamp is not None
    assert label.timestamp.start == 1.5
    assert label.timestamp.end == 2.0


def test_word_timestamp_parsing():
    """Test WordTimestamp model parsing."""
    data = {
        "word": "Hello",
        "start": 0.0,
        "end": 0.5,
        "confidence": 0.95,
        "speaker": "A",
    }
    word = WordTimestamp.model_validate(data)
    assert word.word == "Hello"
    assert word.start == 0.0
    assert word.end == 0.5
    assert word.confidence == 0.95
    assert word.speaker == "A"


def test_transcript_segment_parsing():
    """Test TranscriptSegment model parsing."""
    data = {
        "id": "seg_1",
        "start_time": 0.0,
        "end_time": 5.5,
        "text": "This is a segment",
        "segment_index": 0,
        "confidence": 0.92,
        "speaker": "A",
        "words": [
            {
                "word": "This",
                "start": 0.0,
                "end": 0.2,
                "confidence": 0.95,
                "speaker": "A",
            }
        ],
        "word_confidence_avg": 0.93,
    }
    segment = TranscriptSegment.model_validate(data)
    assert segment.id == "seg_1"
    assert segment.start_time == 0.0
    assert segment.end_time == 5.5
    assert segment.text == "This is a segment"
    assert segment.segment_index == 0
    assert segment.confidence == 0.92
    assert segment.speaker == "A"
    assert segment.words is not None
    assert len(segment.words) == 1
    assert segment.words[0].word == "This"
    assert segment.word_confidence_avg == 0.93


def test_transcript_entity_parsing():
    """Test TranscriptEntity model parsing."""
    data = {
        "id": "ent_123",
        "entity_type": "organization",
        "text": "Acme Corp",
        "start_time": 2.5,
        "end_time": 3.0,
        "confidence": 0.88,
        "metadata": {"industry": "technology"},
    }
    entity = TranscriptEntity.model_validate(data)
    assert entity.id == "ent_123"
    assert entity.entity_type == "organization"
    assert entity.text == "Acme Corp"
    assert entity.start_time == 2.5
    assert entity.end_time == 3.0
    assert entity.confidence == 0.88
    assert entity.metadata is not None
    assert entity.metadata["industry"] == "technology"


def test_transcript_chapter_parsing():
    """Test TranscriptChapter model parsing."""
    data = {
        "id": "ch_1",
        "chapter_index": 0,
        "headline": "Opening Remarks",
        "summary": "The speaker introduces the main topic",
        "gist": "Introduction",
        "start_time": 0.0,
        "end_time": 60.0,
    }
    chapter = TranscriptChapter.model_validate(data)
    assert chapter.id == "ch_1"
    assert chapter.chapter_index == 0
    assert chapter.headline == "Opening Remarks"
    assert chapter.summary == "The speaker introduces the main topic"
    assert chapter.gist == "Introduction"
    assert chapter.start_time == 0.0
    assert chapter.end_time == 60.0


def test_transcript_basic_parsing():
    """Test basic Transcript model parsing without advanced features."""
    data = {
        "memory_id": "mem_123",
        "text": "Hello world",
        "duration": 5.5,
        "language": "en",
        "provider": "assemblyai",
    }
    transcript = Transcript.model_validate(data)
    assert transcript.memory_id == "mem_123"
    assert transcript.text == "Hello world"
    assert transcript.duration == 5.5
    assert transcript.language == "en"
    assert transcript.provider == "assemblyai"


def test_transcript_full_parsing():
    """Test full Transcript model parsing with all advanced features."""
    data = {
        "memory_id": "mem_123",
        "audio_file_id": "file_456",
        "text": "Speaker A: Hello. Speaker B: Hi there.",
        "duration": 10.5,
        "language": "en",
        "language_confidence": 0.98,
        "provider": "assemblyai",
        "summary": "A greeting conversation between two people.",
        "content_safety_labels": [
            {
                "label": "profanity",
                "confidence": 0.85,
                "severity": "low",
                "timestamp": {"start": 1.5, "end": 2.0},
            }
        ],
        "provider_metadata": {"model_version": "v2.1", "processing_time": 3.2},
        "segments": [
            {
                "id": "seg_1",
                "start_time": 0.0,
                "end_time": 2.5,
                "text": "Hello",
                "segment_index": 0,
                "confidence": 0.95,
                "speaker": "A",
                "words": [
                    {
                        "word": "Hello",
                        "start": 0.0,
                        "end": 0.5,
                        "confidence": 0.95,
                        "speaker": "A",
                    }
                ],
                "word_confidence_avg": 0.95,
            }
        ],
        "entities": [
            {
                "id": "ent_1",
                "entity_type": "person",
                "text": "John Smith",
                "start_time": 1.0,
                "end_time": 2.0,
                "confidence": 0.92,
                "metadata": {"category": "name"},
            }
        ],
        "chapters": [
            {
                "id": "ch_1",
                "chapter_index": 0,
                "headline": "Introduction",
                "summary": "Initial greetings",
                "gist": "Greetings",
                "start_time": 0.0,
                "end_time": 5.0,
            }
        ],
        "words": [
            {
                "word": "Hello",
                "start": 0.0,
                "end": 0.5,
                "confidence": 0.95,
                "speaker": "A",
            }
        ],
    }
    transcript = Transcript.model_validate(data)

    # Basic fields
    assert transcript.memory_id == "mem_123"
    assert transcript.audio_file_id == "file_456"
    assert "Speaker A" in transcript.text
    assert transcript.duration == 10.5
    assert transcript.language == "en"
    assert transcript.language_confidence == 0.98
    assert transcript.provider == "assemblyai"
    assert transcript.summary == "A greeting conversation between two people."

    # Content safety
    assert transcript.content_safety_labels is not None
    assert len(transcript.content_safety_labels) == 1
    assert transcript.content_safety_labels[0].label == "profanity"
    assert transcript.content_safety_labels[0].confidence == 0.85
    assert transcript.content_safety_labels[0].severity == "low"

    # Provider metadata
    assert transcript.provider_metadata is not None
    assert transcript.provider_metadata["model_version"] == "v2.1"

    # Segments with speaker diarization
    assert transcript.segments is not None
    assert len(transcript.segments) == 1
    assert transcript.segments[0].id == "seg_1"
    assert transcript.segments[0].speaker == "A"
    assert transcript.segments[0].text == "Hello"
    assert transcript.segments[0].confidence == 0.95
    assert transcript.segments[0].words is not None
    assert len(transcript.segments[0].words) == 1
    assert transcript.segments[0].words[0].speaker == "A"

    # Entities
    assert transcript.entities is not None
    assert len(transcript.entities) == 1
    assert transcript.entities[0].id == "ent_1"
    assert transcript.entities[0].entity_type == "person"
    assert transcript.entities[0].text == "John Smith"
    assert transcript.entities[0].confidence == 0.92

    # Chapters
    assert transcript.chapters is not None
    assert len(transcript.chapters) == 1
    assert transcript.chapters[0].id == "ch_1"
    assert transcript.chapters[0].headline == "Introduction"
    assert transcript.chapters[0].summary == "Initial greetings"
    assert transcript.chapters[0].gist == "Greetings"

    # Words
    assert transcript.words is not None
    assert len(transcript.words) == 1
    assert transcript.words[0].word == "Hello"
    assert transcript.words[0].speaker == "A"
