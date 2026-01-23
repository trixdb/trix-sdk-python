"""Tests for concrete metrics implementation."""

import json
import tempfile
import threading
from pathlib import Path

import pytest

from trix.utils.metrics import RequestMetrics
from trix.utils.metrics_impl import (
    Counter,
    Gauge,
    Histogram,
    SimpleMetricsCollector,
)


class TestCounter:
    """Tests for Counter metric."""

    def test_increment(self):
        """Test basic increment."""
        counter = Counter("test_counter", "A test counter")
        counter.inc()
        assert counter.get() == 1
        counter.inc()
        assert counter.get() == 2

    def test_add(self):
        """Test adding values."""
        counter = Counter("test_counter")
        counter.add(5)
        assert counter.get() == 5
        counter.add(3)
        assert counter.get() == 8

    def test_negative_value_raises(self):
        """Test that negative values raise an error."""
        counter = Counter("test_counter")
        with pytest.raises(ValueError, match="cannot be negative"):
            counter.add(-1)

    def test_labels(self):
        """Test counter with labels."""
        counter = Counter("test_counter")
        counter.inc(labels={"method": "GET"})
        counter.inc(labels={"method": "GET"})
        counter.inc(labels={"method": "POST"})

        assert counter.get(labels={"method": "GET"}) == 2
        assert counter.get(labels={"method": "POST"}) == 1
        assert counter.get(labels={"method": "PUT"}) == 0

    def test_get_all(self):
        """Test getting all counter values."""
        counter = Counter("test_counter")
        counter.inc(labels={"method": "GET"})
        counter.add(5, labels={"method": "POST"})

        values = counter.get_all()
        assert len(values) == 2

        values_by_method = {tuple(sorted(v.labels.items())): v.value for v in values}
        assert values_by_method[(("method", "GET"),)] == 1
        assert values_by_method[(("method", "POST"),)] == 5

    def test_reset(self):
        """Test resetting counter."""
        counter = Counter("test_counter")
        counter.inc()
        counter.inc(labels={"method": "GET"})
        counter.reset()

        assert counter.get() == 0
        assert counter.get(labels={"method": "GET"}) == 0

    def test_thread_safety(self):
        """Test thread safety of counter operations."""
        counter = Counter("test_counter")
        num_threads = 10
        increments_per_thread = 1000

        def increment_counter():
            for _ in range(increments_per_thread):
                counter.inc()

        threads = [threading.Thread(target=increment_counter) for _ in range(num_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert counter.get() == num_threads * increments_per_thread


class TestGauge:
    """Tests for Gauge metric."""

    def test_set(self):
        """Test setting gauge value."""
        gauge = Gauge("test_gauge", "A test gauge")
        gauge.set(42)
        assert gauge.get() == 42

    def test_inc_dec(self):
        """Test incrementing and decrementing."""
        gauge = Gauge("test_gauge")
        gauge.set(10)
        gauge.inc()
        assert gauge.get() == 11
        gauge.dec()
        assert gauge.get() == 10
        gauge.inc(5)
        assert gauge.get() == 15
        gauge.dec(3)
        assert gauge.get() == 12

    def test_labels(self):
        """Test gauge with labels."""
        gauge = Gauge("test_gauge")
        gauge.set(10, labels={"host": "server1"})
        gauge.set(20, labels={"host": "server2"})

        assert gauge.get(labels={"host": "server1"}) == 10
        assert gauge.get(labels={"host": "server2"}) == 20

    def test_get_all(self):
        """Test getting all gauge values."""
        gauge = Gauge("test_gauge")
        gauge.set(10, labels={"host": "server1"})
        gauge.set(20, labels={"host": "server2"})

        values = gauge.get_all()
        assert len(values) == 2

    def test_reset(self):
        """Test resetting gauge."""
        gauge = Gauge("test_gauge")
        gauge.set(42)
        gauge.reset()
        assert gauge.get() == 0

    def test_thread_safety(self):
        """Test thread safety of gauge operations."""
        gauge = Gauge("test_gauge")
        gauge.set(0)
        num_threads = 10
        operations_per_thread = 100

        def inc_dec_gauge():
            for _ in range(operations_per_thread):
                gauge.inc()
                gauge.dec()

        threads = [threading.Thread(target=inc_dec_gauge) for _ in range(num_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Should end up at 0 since we inc/dec equal times
        assert gauge.get() == 0


class TestHistogram:
    """Tests for Histogram metric."""

    def test_observe(self):
        """Test observing values."""
        histogram = Histogram("test_histogram", "A test histogram")
        histogram.observe(50)
        histogram.observe(150)

        assert histogram.get_count() == 2
        assert histogram.get_sum() == 200

    def test_buckets(self):
        """Test histogram buckets."""
        histogram = Histogram("test_histogram", buckets=(10, 50, 100))

        histogram.observe(5)  # <= 10, <= 50, <= 100
        histogram.observe(25)  # <= 50, <= 100
        histogram.observe(75)  # <= 100
        histogram.observe(200)  # none

        buckets = histogram.get_buckets()
        bucket_counts = {b.upper_bound: b.count for b in buckets}

        assert bucket_counts[10] == 1
        assert bucket_counts[50] == 2
        assert bucket_counts[100] == 3

    def test_labels(self):
        """Test histogram with labels."""
        histogram = Histogram("test_histogram")
        histogram.observe(100, labels={"endpoint": "/api"})
        histogram.observe(200, labels={"endpoint": "/api"})
        histogram.observe(50, labels={"endpoint": "/health"})

        assert histogram.get_count(labels={"endpoint": "/api"}) == 2
        assert histogram.get_sum(labels={"endpoint": "/api"}) == 300
        assert histogram.get_count(labels={"endpoint": "/health"}) == 1

    def test_reset(self):
        """Test resetting histogram."""
        histogram = Histogram("test_histogram")
        histogram.observe(100)
        histogram.reset()

        assert histogram.get_count() == 0
        assert histogram.get_sum() == 0

    def test_default_buckets(self):
        """Test that default buckets are used."""
        histogram = Histogram("test_histogram")
        assert histogram.buckets == Histogram.DEFAULT_BUCKETS


class TestSimpleMetricsCollector:
    """Tests for SimpleMetricsCollector."""

    def test_on_request_complete_success(self):
        """Test recording successful requests."""
        collector = SimpleMetricsCollector()
        metrics = RequestMetrics(
            method="GET",
            path="/memories",
            status_code=200,
            duration_ms=100.5,
            request_size=50,
            response_size=1000,
        )

        collector.on_request_complete(metrics)

        assert (
            collector.requests_total.get(
                labels={"method": "GET", "path": "/memories", "status": "200"}
            )
            == 1
        )
        assert (
            collector.requests_success.get(
                labels={"method": "GET", "path": "/memories", "status": "200"}
            )
            == 1
        )
        assert (
            collector.requests_failed.get(
                labels={"method": "GET", "path": "/memories", "status": "200"}
            )
            == 0
        )

    def test_on_request_complete_failure(self):
        """Test recording failed requests."""
        collector = SimpleMetricsCollector()
        metrics = RequestMetrics(
            method="POST",
            path="/memories",
            status_code=500,
            duration_ms=50.0,
            error="ServerError",
        )

        collector.on_request_complete(metrics)

        labels = {"method": "POST", "path": "/memories", "status": "500"}
        assert collector.requests_total.get(labels=labels) == 1
        assert collector.requests_success.get(labels=labels) == 0
        assert collector.requests_failed.get(labels=labels) == 1

    def test_on_request_start(self):
        """Test tracking request start."""
        collector = SimpleMetricsCollector()
        collector.on_request_start("GET", "/memories")

        assert collector.in_flight_requests.get(labels={"method": "GET"}) == 1

    def test_on_retry(self):
        """Test recording retries."""
        collector = SimpleMetricsCollector()
        collector.on_retry("GET", "/memories", 1, ValueError("test"), 100)

        labels = {"method": "GET", "path": "/memories", "error_type": "ValueError"}
        assert collector.retries_total.get(labels=labels) == 1

    def test_get_snapshot(self):
        """Test getting metrics snapshot."""
        collector = SimpleMetricsCollector()
        metrics = RequestMetrics(
            method="GET",
            path="/test",
            status_code=200,
            duration_ms=50.0,
        )
        collector.on_request_complete(metrics)

        snapshot = collector.get_snapshot()

        assert "requests_total" in snapshot
        assert "requests_success" in snapshot
        assert "request_duration_ms" in snapshot
        assert "timestamp" in snapshot
        assert snapshot["request_duration_ms"]["count"] == 1
        assert snapshot["request_duration_ms"]["sum"] == 50.0

    def test_export_to_file(self):
        """Test exporting metrics to file."""
        collector = SimpleMetricsCollector()
        metrics = RequestMetrics(
            method="GET",
            path="/test",
            status_code=200,
            duration_ms=50.0,
        )
        collector.on_request_complete(metrics)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            path = Path(f.name)

        try:
            collector.export_to_file(path)
            content = json.loads(path.read_text())
            assert "requests_total" in content
            assert "timestamp" in content
        finally:
            path.unlink()

    def test_reset(self):
        """Test resetting all metrics."""
        collector = SimpleMetricsCollector()
        metrics = RequestMetrics(
            method="GET",
            path="/test",
            status_code=200,
            duration_ms=50.0,
        )
        collector.on_request_complete(metrics)
        collector.on_retry("GET", "/test", 1, ValueError("test"), 100)

        collector.reset()

        assert collector.request_duration_ms.get_count() == 0
        assert len(collector.requests_total.get_all()) == 0
        assert len(collector.retries_total.get_all()) == 0

    def test_custom_labels_propagate(self):
        """Test that custom labels from RequestMetrics are included."""
        collector = SimpleMetricsCollector()
        metrics = RequestMetrics(
            method="GET",
            path="/test",
            status_code=200,
            duration_ms=50.0,
            labels={"custom": "value"},
        )
        collector.on_request_complete(metrics)

        # The labels should include both standard and custom labels
        all_values = collector.requests_total.get_all()
        assert len(all_values) == 1
        assert "custom" in all_values[0].labels
        assert all_values[0].labels["custom"] == "value"
