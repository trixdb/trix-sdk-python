"""Tests for enrichments resource."""

import pytest
from unittest.mock import patch

from trix import Trix, AsyncTrix, EnrichmentOperation, EnrichmentResult, EnrichmentStatus
from trix.types import Enrichment


@pytest.fixture
def mock_enrichment_data():
    """Mock enrichment response data."""
    return {
        "type": "entities",
        "status": "completed",
        "data": {"entities": [{"name": "Python", "type": "technology"}]},
        "error": None,
        "processed_at": "2025-01-01T00:00:00Z",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z",
    }


@pytest.fixture
def mock_enrichment_list_data(mock_enrichment_data):
    """Mock enrichment list response data."""
    return {"data": [mock_enrichment_data]}


@pytest.fixture
def mock_enrichment_result_data():
    """Mock enrichment result (trigger/retry) response data."""
    return {
        "memory_id": "mem_123",
        "triggered": ["entities", "summary"],
        "job_ids": ["job_001", "job_002"],
        "status": "processing",
    }


class TestEnrichmentsList:
    """Tests for enrichments.list()."""

    def test_list_basic(self, mock_enrichment_list_data):
        """Test listing enrichments for a memory."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_enrichment_list_data
            client = Trix(api_key="test_key")

            result = client.enrichments.list("mem_123")

            assert len(result) == 1
            assert isinstance(result[0], Enrichment)
            assert result[0].type == "entities"
            assert result[0].status == EnrichmentStatus.COMPLETED
            call_args = mock_request.call_args
            assert call_args[0][1] == "/memories/mem_123/enrichments"
            client.close()

    def test_list_with_status_filter(self, mock_enrichment_list_data):
        """Test listing enrichments filtered by status."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_enrichment_list_data
            client = Trix(api_key="test_key")

            client.enrichments.list("mem_123", status=EnrichmentStatus.COMPLETED)

            call_args = mock_request.call_args
            assert call_args[1]["params"]["status"] == "completed"
            client.close()


class TestEnrichmentsGet:
    """Tests for enrichments.get()."""

    def test_get_by_type(self, mock_enrichment_data):
        """Test getting a specific enrichment by type."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_enrichment_data
            client = Trix(api_key="test_key")

            enrichment = client.enrichments.get("mem_123", "entities")

            assert isinstance(enrichment, Enrichment)
            assert enrichment.type == "entities"
            assert enrichment.data is not None
            mock_request.assert_called_with(
                "GET", "/memories/mem_123/enrichments/entities"
            )
            client.close()

    def test_get_invalid_type_raises(self):
        """Test that empty enrichment type raises ValueError."""
        client = Trix(api_key="test_key")

        with pytest.raises(ValueError, match="Enrichment type is required"):
            client.enrichments.get("mem_123", "")

        client.close()


class TestEnrichmentsTrigger:
    """Tests for enrichments.trigger()."""

    def test_trigger_basic(self, mock_enrichment_result_data):
        """Test triggering enrichments."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_enrichment_result_data
            client = Trix(api_key="test_key")

            result = client.enrichments.trigger("mem_123")

            assert isinstance(result, EnrichmentResult)
            assert result.memory_id == "mem_123"
            assert result.status == "processing"
            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/memories/mem_123/enrichments"
            client.close()

    def test_trigger_with_types(self, mock_enrichment_result_data):
        """Test triggering specific enrichment types."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_enrichment_result_data
            client = Trix(api_key="test_key")

            result = client.enrichments.trigger(
                "mem_123",
                types=["entities", "summary"],
                priority="high",
            )

            call_args = mock_request.call_args
            body = call_args[1]["json"]
            assert body["types"] == ["entities", "summary"]
            assert body["priority"] == "high"
            assert result.triggered == ["entities", "summary"]
            client.close()

    def test_trigger_with_force(self, mock_enrichment_result_data):
        """Test force-triggering enrichments."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_enrichment_result_data
            client = Trix(api_key="test_key")

            client.enrichments.trigger("mem_123", force=True)

            call_args = mock_request.call_args
            body = call_args[1]["json"]
            assert body["force"] is True
            client.close()


class TestEnrichmentsRetry:
    """Tests for enrichments.retry()."""

    def test_retry_basic(self, mock_enrichment_result_data):
        """Test retrying failed enrichments."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_enrichment_result_data
            client = Trix(api_key="test_key")

            result = client.enrichments.retry("mem_123")

            assert isinstance(result, EnrichmentResult)
            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/memories/mem_123/enrichments/retry"
            client.close()

    def test_retry_specific_types(self, mock_enrichment_result_data):
        """Test retrying specific enrichment types."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_enrichment_result_data
            client = Trix(api_key="test_key")

            client.enrichments.retry("mem_123", types=["entities"])

            call_args = mock_request.call_args
            body = call_args[1]["json"]
            assert body["types"] == ["entities"]
            client.close()


class TestEnrichmentsEnrich:
    """Tests for enrichments.enrich() convenience method."""

    def test_enrich_with_operations(self, mock_enrichment_result_data):
        """Test enrich with EnrichmentOperation enums."""
        with patch.object(Trix, "_request") as mock_request:
            mock_request.return_value = mock_enrichment_result_data
            client = Trix(api_key="test_key")

            result = client.enrichments.enrich(
                "mem_123",
                operations=[EnrichmentOperation.TOPICS, EnrichmentOperation.SUMMARY],
            )

            assert isinstance(result, EnrichmentResult)
            call_args = mock_request.call_args
            body = call_args[1]["json"]
            assert "types" in body
            client.close()


class TestAsyncEnrichments:
    """Tests for async enrichments operations."""

    @pytest.mark.asyncio
    async def test_async_list(self, mock_enrichment_list_data):
        """Test async enrichment listing."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_enrichment_list_data
            async with AsyncTrix(api_key="test_key") as client:
                result = await client.enrichments.list("mem_123")
                assert len(result) == 1

    @pytest.mark.asyncio
    async def test_async_trigger(self, mock_enrichment_result_data):
        """Test async enrichment trigger."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_enrichment_result_data
            async with AsyncTrix(api_key="test_key") as client:
                result = await client.enrichments.trigger("mem_123")
                assert result.memory_id == "mem_123"

    @pytest.mark.asyncio
    async def test_async_retry(self, mock_enrichment_result_data):
        """Test async enrichment retry."""
        with patch.object(AsyncTrix, "_request") as mock_request:
            mock_request.return_value = mock_enrichment_result_data
            async with AsyncTrix(api_key="test_key") as client:
                result = await client.enrichments.retry("mem_123")
                assert result.status == "processing"
