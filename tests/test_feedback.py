"""Tests for FeedbackResource."""

from unittest.mock import Mock

from trix.resources.feedback import FeedbackResource
from trix.types import FeedbackResult

FEEDBACK_RESPONSE = {
    "relationships_created": 2,
    "memories_boosted": 3,
}


class TestFeedbackSubmit:
    """Tests for feedback.submit()."""

    def test_submit_basic(self):
        """Test submitting detailed feedback on search results."""
        mock_client = Mock()
        mock_client._request.return_value = FEEDBACK_RESPONSE

        resource = FeedbackResource(mock_client)
        result = resource.submit(
            query_context="machine learning",
            results=[
                FeedbackResult(memory_id="mem_123", score=0.9, rank=1),
                FeedbackResult(memory_id="mem_456", score=0.8, rank=2),
            ],
        )

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/feedback")
        body = call_args[1]["json"]
        assert body["query_context"] == "machine learning"
        assert len(body["results"]) == 2
        assert result.relationships_created == 2
        assert result.memories_boosted == 3

    def test_submit_with_boost_and_relationships(self):
        """Test submitting feedback with boost amount and relationship flag."""
        mock_client = Mock()
        mock_client._request.return_value = FEEDBACK_RESPONSE

        resource = FeedbackResource(mock_client)
        resource.submit(
            query_context="AI research",
            results=[
                FeedbackResult(memory_id="mem_123", score=0.95, rank=1),
            ],
            boost_amount=0.5,
            create_relationships=False,
        )

        call_args = mock_client._request.call_args
        body = call_args[1]["json"]
        assert body["boost_amount"] == 0.5
        assert body["create_relationships"] is False


class TestFeedbackQuick:
    """Tests for feedback.quick()."""

    def test_quick_useful(self):
        """Test submitting quick positive feedback."""
        mock_client = Mock()
        mock_client._request.return_value = FEEDBACK_RESPONSE

        resource = FeedbackResource(mock_client)
        result = resource.quick(memory_id="mem_123", useful=True)

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/feedback/quick")
        body = call_args[1]["json"]
        assert body["memory_id"] == "mem_123"
        assert body["useful"] is True
        assert result.relationships_created == 2

    def test_quick_with_source(self):
        """Test quick feedback with source memory ID."""
        mock_client = Mock()
        mock_client._request.return_value = FEEDBACK_RESPONSE

        resource = FeedbackResource(mock_client)
        resource.quick(
            memory_id="mem_123",
            useful=False,
            source_memory_id="mem_789",
        )

        call_args = mock_client._request.call_args
        body = call_args[1]["json"]
        assert body["useful"] is False
        assert body["source_memory_id"] == "mem_789"


class TestFeedbackBatch:
    """Tests for feedback.batch()."""

    def test_batch_feedback(self):
        """Test submitting batch feedback with useful and not useful IDs."""
        mock_client = Mock()
        mock_client._request.return_value = FEEDBACK_RESPONSE

        resource = FeedbackResource(mock_client)
        result = resource.batch(
            useful_ids=["mem_123", "mem_456"],
            not_useful_ids=["mem_789"],
        )

        call_args = mock_client._request.call_args
        assert call_args[0] == ("POST", "/feedback/batch")
        body = call_args[1]["json"]
        assert body["useful_ids"] == ["mem_123", "mem_456"]
        assert body["not_useful_ids"] == ["mem_789"]
        assert result.memories_boosted == 3
