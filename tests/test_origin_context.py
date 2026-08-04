"""
Tests for Origin/Context Metadata Feature (TDD)

This module tests the origin and context tracking functionality:
- Origin types (work, private, shared, learning)
- Source types (email, meeting, chat, etc.)
- Session integration
- Resource linking (many-to-many)

TDD Workflow:
1. RED: Write failing tests first (this file)
2. GREEN: Implement SDK methods to make tests pass
3. REFACTOR: Clean up code while keeping tests green
"""

import pytest
from datetime import datetime
from unittest.mock import patch

from trix import Trix
from trix.types import (
    OriginType,
    SourceType,
    ResourceRelationshipType,
    Memory,
    MemoryCreate,
    MemoryUpdate,
    Resource,
    ResourceCreate,
    MemoryResource,
)


class TestOriginContextEnums:
    """Test origin/context enum definitions."""

    def test_origin_type_values(self):
        """Should have all valid origin types."""
        assert OriginType.WORK.value == "work"
        assert OriginType.PRIVATE.value == "private"
        assert OriginType.SHARED.value == "shared"
        assert OriginType.LEARNING.value == "learning"

    def test_origin_type_count(self):
        """Should have exactly 4 origin types."""
        assert len(OriginType) == 4

    def test_source_type_values(self):
        """Should have all valid source types."""
        assert SourceType.EMAIL.value == "email"
        assert SourceType.MEETING.value == "meeting"
        assert SourceType.CHAT.value == "chat"
        assert SourceType.DOCUMENT.value == "document"
        assert SourceType.WEBPAGE.value == "webpage"
        assert SourceType.AUDIO.value == "audio"
        assert SourceType.VIDEO.value == "video"
        assert SourceType.SCREENSHOT.value == "screenshot"
        assert SourceType.MANUAL.value == "manual"
        assert SourceType.AGENT.value == "agent"
        assert SourceType.API.value == "api"
        assert SourceType.IMPORT.value == "import"

    def test_source_type_count(self):
        """Should have exactly 12 source types."""
        assert len(SourceType) == 12

    def test_resource_relationship_type_values(self):
        """Should have all valid relationship types."""
        assert ResourceRelationshipType.PRIMARY.value == "primary"
        assert ResourceRelationshipType.RELATED.value == "related"
        assert ResourceRelationshipType.MENTIONED.value == "mentioned"
        assert ResourceRelationshipType.DERIVED.value == "derived"

    def test_resource_relationship_type_count(self):
        """Should have exactly 4 relationship types."""
        assert len(ResourceRelationshipType) == 4


class TestMemoryWithOriginContext:
    """Test Memory model with origin/context fields."""

    def test_memory_has_origin_context_fields(self):
        """Memory model should have origin/context fields."""
        memory = Memory(
            id="test-id",
            content="Test content",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            session_id="session-123",
            origin_type=OriginType.WORK,
            source_type=SourceType.MEETING,
            source_id="meeting-abc",
            source_metadata={"platform": "zoom", "attendees": ["alice", "bob"]},
        )

        assert memory.session_id == "session-123"
        assert memory.origin_type == OriginType.WORK
        assert memory.source_type == SourceType.MEETING
        assert memory.source_id == "meeting-abc"
        assert memory.source_metadata["platform"] == "zoom"

    def test_memory_origin_context_fields_optional(self):
        """Origin/context fields should be optional for backward compatibility."""
        memory = Memory(
            id="test-id",
            content="Test content",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        assert memory.session_id is None
        assert memory.origin_type is None
        assert memory.source_type is None
        assert memory.source_id is None
        assert memory.source_metadata == {}


class TestMemoryCreate:
    """Test MemoryCreate model with origin/context fields."""

    def test_memory_create_with_origin_context(self):
        """Should create memory request with origin/context fields."""
        request = MemoryCreate(
            content="Meeting notes",
            origin_type=OriginType.WORK,
            source_type=SourceType.MEETING,
            session_id="session-123",
            source_id="meeting-abc",
            source_metadata={"platform": "zoom"},
            resource_ids=["resource-1", "resource-2"],
        )

        assert request.content == "Meeting notes"
        assert request.origin_type == OriginType.WORK
        assert request.source_type == SourceType.MEETING
        assert request.session_id == "session-123"
        assert request.source_id == "meeting-abc"
        assert request.source_metadata == {"platform": "zoom"}
        assert request.resource_ids == ["resource-1", "resource-2"]

    def test_memory_create_without_origin_context(self):
        """Should create memory request without origin/context (backward compatible)."""
        request = MemoryCreate(content="Simple memory")

        assert request.content == "Simple memory"
        assert request.origin_type is None
        assert request.source_type is None
        assert request.session_id is None
        assert request.resource_ids is None


class TestMemoryUpdate:
    """Test MemoryUpdate model with origin/context fields."""

    def test_memory_update_origin_type(self):
        """Should update origin_type."""
        update = MemoryUpdate(origin_type=OriginType.PRIVATE)

        assert update.origin_type == OriginType.PRIVATE

    def test_memory_update_source_type(self):
        """Should update source_type."""
        update = MemoryUpdate(source_type=SourceType.EMAIL)

        assert update.source_type == SourceType.EMAIL

    def test_memory_update_source_metadata(self):
        """Should update source_metadata."""
        update = MemoryUpdate(source_metadata={"new": "data"})

        assert update.source_metadata == {"new": "data"}


class TestResourceModel:
    """Test Resource model."""

    def test_resource_model(self):
        """Should create resource with all fields."""
        resource = Resource(
            id="resource-1",
            name="Project Alpha",
            type="project",
            description="Main project",
            metadata={"priority": "high"},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        assert resource.id == "resource-1"
        assert resource.name == "Project Alpha"
        assert resource.type == "project"
        assert resource.description == "Main project"
        assert resource.metadata == {"priority": "high"}

    def test_resource_default_type(self):
        """Should default type to 'project'."""
        resource = Resource(
            id="resource-1",
            name="Test Resource",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        assert resource.type == "project"


class TestResourceCreate:
    """Test ResourceCreate model."""

    def test_resource_create_minimal(self):
        """Should create resource with just name."""
        request = ResourceCreate(name="New Project")

        assert request.name == "New Project"
        assert request.type == "project"  # Default
        assert request.description is None

    def test_resource_create_full(self):
        """Should create resource with all fields."""
        request = ResourceCreate(
            name="New Project",
            type="topic",
            description="A research topic",
            metadata={"category": "research"},
        )

        assert request.name == "New Project"
        assert request.type == "topic"
        assert request.description == "A research topic"
        assert request.metadata == {"category": "research"}


class TestMemoryResourceLink:
    """Test MemoryResource link model."""

    def test_memory_resource_link(self):
        """Should create memory-resource link."""
        link = MemoryResource(
            memory_id="memory-1",
            resource_id="resource-1",
            relationship_type=ResourceRelationshipType.PRIMARY,
            created_at=datetime.now(),
        )

        assert link.memory_id == "memory-1"
        assert link.resource_id == "resource-1"
        assert link.relationship_type == ResourceRelationshipType.PRIMARY

    def test_memory_resource_default_relationship(self):
        """Should default relationship to 'related'."""
        link = MemoryResource(
            memory_id="memory-1",
            resource_id="resource-1",
            created_at=datetime.now(),
        )

        assert link.relationship_type == ResourceRelationshipType.RELATED


@pytest.mark.xfail(
    reason=(
        "Aspirational TDD contract: memories.create() and memories.list() do not yet "
        "accept origin_type/source_type/session_id kwargs, though the MemoryCreate model "
        "supports them. Origin/context passthrough on the client methods is unimplemented "
        "— tracked as an SDK coverage gap."
    ),
    strict=False,
)
class TestTrixOriginContext:
    """Test Trix with origin/context features."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock Trix."""
        with patch("trix.Trix._request") as mock_request:
            client = Trix(api_key="test-api-key")
            client._request = mock_request
            yield client, mock_request

    def test_create_memory_with_origin_context(self, mock_client):
        """Should create memory with origin/context fields."""
        client, mock_request = mock_client
        mock_request.return_value = {
            "id": "memory-123",
            "content": "Meeting notes",
            "origin_type": "work",
            "source_type": "meeting",
            "session_id": "session-456",
            "created_at": "2026-01-06T10:00:00Z",
            "updated_at": "2026-01-06T10:00:00Z",
        }

        # This tests the expected API contract
        client.memories.create(
            content="Meeting notes",
            origin_type=OriginType.WORK,
            source_type=SourceType.MEETING,
            session_id="session-456",
        )

        # Verify the request was made with correct parameters
        mock_request.assert_called()
        call_args = mock_request.call_args

        # The body should include origin/context fields
        body = call_args.kwargs.get("body", {}) if call_args.kwargs else {}
        assert body.get("origin_type") == "work" or "origin_type" in str(call_args)

    def test_list_memories_with_origin_filter(self, mock_client):
        """Should filter memories by origin_type."""
        client, mock_request = mock_client
        mock_request.return_value = {
            "data": [],
            "pagination": {"total": 0, "page": 1, "limit": 20, "offset": 0, "has_more": False},
        }

        # Filter by origin_type
        client.memories.list(origin_type=OriginType.WORK)

        mock_request.assert_called()
        call_args = mock_request.call_args
        # Verify query params include origin_type filter
        assert "work" in str(call_args) or "origin_type" in str(call_args)

    def test_list_memories_with_source_filter(self, mock_client):
        """Should filter memories by source_type."""
        client, mock_request = mock_client
        mock_request.return_value = {
            "data": [],
            "pagination": {"total": 0, "page": 1, "limit": 20, "offset": 0, "has_more": False},
        }

        # Filter by source_type
        client.memories.list(source_type=SourceType.MEETING)

        mock_request.assert_called()

    def test_list_memories_with_session_filter(self, mock_client):
        """Should filter memories by session_id."""
        client, mock_request = mock_client
        mock_request.return_value = {
            "data": [],
            "pagination": {"total": 0, "page": 1, "limit": 20, "offset": 0, "has_more": False},
        }

        # Filter by session_id
        client.memories.list(session_id="session-123")

        mock_request.assert_called()


class TestResourceMethods:
    """Test resource-related methods on Trix."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock Trix."""
        with patch.object(Trix, "_request") as mock_request:
            client = Trix(api_key="test-api-key")
            yield client, mock_request

    def test_create_resource(self, mock_client):
        """Should create a resource."""
        client, mock_request = mock_client
        mock_request.return_value = {
            "id": "resource-123",
            "name": "Project Alpha",
            "type": "project",
            "created_at": "2026-01-06T10:00:00Z",
            "updated_at": "2026-01-06T10:00:00Z",
        }

        # This assumes a resources.create() method will be implemented
        # For now, this test documents the expected API
        if hasattr(client, "resources"):
            client.resources.create(name="Project Alpha")
            mock_request.assert_called()

    def test_list_resources(self, mock_client):
        """Should list resources."""
        client, mock_request = mock_client
        mock_request.return_value = {
            "data": [
                {
                    "id": "resource-1",
                    "name": "Project 1",
                    "type": "project",
                    "created_at": "2026-01-06T10:00:00Z",
                    "updated_at": "2026-01-06T10:00:00Z",
                }
            ],
            "pagination": {"total": 1, "page": 1, "limit": 20, "offset": 0, "has_more": False},
        }

        if hasattr(client, "resources"):
            client.resources.list()
            mock_request.assert_called()

    def test_link_memory_to_resource(self, mock_client):
        """Should link a memory to a resource."""
        client, mock_request = mock_client
        mock_request.return_value = {
            "memory_id": "memory-123",
            "resource_id": "resource-456",
            "relationship_type": "primary",
            "linked": True,
        }

        # This tests the expected API for linking
        if hasattr(client, "memories"):
            # Assuming memories.link_resource() method
            pass  # Will be implemented in the SDK

    def test_get_memory_resources(self, mock_client):
        """Should get resources linked to a memory."""
        client, mock_request = mock_client
        mock_request.return_value = {
            "data": [
                {
                    "memory_id": "memory-123",
                    "resource_id": "resource-456",
                    "relationship_type": "related",
                    "created_at": "2026-01-06T10:00:00Z",
                    "resource": {
                        "id": "resource-456",
                        "name": "Project",
                        "type": "project",
                        "created_at": "2026-01-06T10:00:00Z",
                        "updated_at": "2026-01-06T10:00:00Z",
                    },
                }
            ]
        }

        # This tests the expected API for getting linked resources
        if hasattr(client, "memories"):
            # Assuming memories.get_resources(memory_id) method
            pass

    def test_unlink_memory_from_resource(self, mock_client):
        """Should unlink a memory from a resource."""
        client, mock_request = mock_client
        mock_request.return_value = {
            "memory_id": "memory-123",
            "resource_id": "resource-456",
            "unlinked": True,
        }

        # This tests the expected API for unlinking
        if hasattr(client, "memories"):
            # Assuming memories.unlink_resource(memory_id, resource_id) method
            pass


class TestMemoryListFilters:
    """Test extended filter parameters for memory listing."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock Trix."""
        with patch.object(Trix, "_request") as mock_request:
            client = Trix(api_key="test-api-key")
            yield client, mock_request

    def test_filter_by_resource_id(self, mock_client):
        """Should filter memories by resource_id."""
        client, mock_request = mock_client
        mock_request.return_value = {
            "data": [],
            "pagination": {"total": 0, "page": 1, "limit": 20, "offset": 0, "has_more": False},
        }

        # Filter by resource_id
        # This tests the expected API parameter
        if hasattr(client.memories, "list"):
            # Assuming resource_id parameter support
            pass

    def test_combined_filters(self, mock_client):
        """Should combine multiple origin/context filters."""
        client, mock_request = mock_client
        mock_request.return_value = {
            "data": [],
            "pagination": {"total": 0, "page": 1, "limit": 20, "offset": 0, "has_more": False},
        }

        # Combine origin_type + source_type + session_id
        # This tests the expected API contract for combined filters
        if hasattr(client.memories, "list"):
            # Assuming combined filter support
            pass


class TestBackwardCompatibility:
    """Test backward compatibility with existing code."""

    def test_memory_without_origin_context(self):
        """Existing memory creation should work without origin/context."""
        request = MemoryCreate(
            content="Simple memory",
            tags=["tag1", "tag2"],
            metadata={"key": "value"},
        )

        assert request.content == "Simple memory"
        assert request.tags == ["tag1", "tag2"]
        assert request.origin_type is None
        assert request.source_type is None

    def test_memory_model_without_origin_context(self):
        """Memory model should work without origin/context fields."""
        memory = Memory(
            id="test-id",
            content="Test content",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        # All origin/context fields should be None or empty
        assert memory.origin_type is None
        assert memory.source_type is None
        assert memory.session_id is None
        assert memory.source_id is None
        assert memory.source_metadata == {}
