"""Concrete metrics implementation with Counter, Gauge, and Histogram support.

This module provides thread-safe metrics primitives that can be used for
application monitoring and observability.
"""

import json
import logging
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .metrics import MetricsCollector, RequestMetrics

logger = logging.getLogger(__name__)


@dataclass
class MetricValue:
    """A single metric value with labels."""

    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class Counter:
    """Thread-safe counter metric that can only increase.

    Example:
        >>> counter = Counter("requests_total", "Total number of requests")
        >>> counter.inc()
        >>> counter.inc(labels={"method": "GET"})
        >>> counter.add(5, labels={"method": "POST"})
    """

    def __init__(self, name: str, description: str = "") -> None:
        self.name = name
        self.description = description
        self._values: Dict[Tuple[Tuple[str, str], ...], float] = {}
        self._lock = threading.Lock()

    def _label_key(self, labels: Optional[Dict[str, str]]) -> Tuple[Tuple[str, str], ...]:
        """Convert labels dict to a hashable key."""
        if not labels:
            return ()
        return tuple(sorted(labels.items()))

    def inc(self, labels: Optional[Dict[str, str]] = None) -> None:
        """Increment the counter by 1."""
        self.add(1, labels)

    def add(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Add a value to the counter. Value must be non-negative."""
        if value < 0:
            raise ValueError("Counter value cannot be negative")
        key = self._label_key(labels)
        with self._lock:
            self._values[key] = self._values.get(key, 0) + value

    def get(self, labels: Optional[Dict[str, str]] = None) -> float:
        """Get the current counter value for the given labels."""
        key = self._label_key(labels)
        with self._lock:
            return self._values.get(key, 0)

    def get_all(self) -> List[MetricValue]:
        """Get all counter values with their labels."""
        with self._lock:
            return [MetricValue(value=v, labels=dict(k)) for k, v in self._values.items()]

    def reset(self) -> None:
        """Reset all counter values."""
        with self._lock:
            self._values.clear()


class Gauge:
    """Thread-safe gauge metric that can increase or decrease.

    Example:
        >>> gauge = Gauge("active_connections", "Number of active connections")
        >>> gauge.set(10)
        >>> gauge.inc()
        >>> gauge.dec()
    """

    def __init__(self, name: str, description: str = "") -> None:
        self.name = name
        self.description = description
        self._values: Dict[Tuple[Tuple[str, str], ...], float] = {}
        self._lock = threading.Lock()

    def _label_key(self, labels: Optional[Dict[str, str]]) -> Tuple[Tuple[str, str], ...]:
        """Convert labels dict to a hashable key."""
        if not labels:
            return ()
        return tuple(sorted(labels.items()))

    def set(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Set the gauge to a specific value."""
        key = self._label_key(labels)
        with self._lock:
            self._values[key] = value

    def inc(self, value: float = 1, labels: Optional[Dict[str, str]] = None) -> None:
        """Increment the gauge."""
        key = self._label_key(labels)
        with self._lock:
            self._values[key] = self._values.get(key, 0) + value

    def dec(self, value: float = 1, labels: Optional[Dict[str, str]] = None) -> None:
        """Decrement the gauge."""
        self.inc(-value, labels)

    def get(self, labels: Optional[Dict[str, str]] = None) -> float:
        """Get the current gauge value for the given labels."""
        key = self._label_key(labels)
        with self._lock:
            return self._values.get(key, 0)

    def get_all(self) -> List[MetricValue]:
        """Get all gauge values with their labels."""
        with self._lock:
            return [MetricValue(value=v, labels=dict(k)) for k, v in self._values.items()]

    def reset(self) -> None:
        """Reset all gauge values."""
        with self._lock:
            self._values.clear()


@dataclass
class HistogramBucket:
    """A histogram bucket with upper bound and count."""

    upper_bound: float
    count: int


class Histogram:
    """Thread-safe histogram metric for measuring distributions.

    Example:
        >>> histogram = Histogram("request_duration_ms", "Request duration")
        >>> histogram.observe(150.5)
        >>> histogram.observe(200.0, labels={"endpoint": "/api"})
    """

    DEFAULT_BUCKETS = (10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000)

    def __init__(
        self,
        name: str,
        description: str = "",
        buckets: Optional[Tuple[float, ...]] = None,
    ) -> None:
        self.name = name
        self.description = description
        self.buckets = buckets or self.DEFAULT_BUCKETS
        self._data: Dict[Tuple[Tuple[str, str], ...], Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def _label_key(self, labels: Optional[Dict[str, str]]) -> Tuple[Tuple[str, str], ...]:
        """Convert labels dict to a hashable key."""
        if not labels:
            return ()
        return tuple(sorted(labels.items()))

    def _init_data(self, key: Tuple[Tuple[str, str], ...]) -> Dict[str, Any]:
        """Initialize histogram data for a label set."""
        return {
            "sum": 0.0,
            "count": 0,
            "buckets": {b: 0 for b in self.buckets},
        }

    def observe(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Record an observation."""
        key = self._label_key(labels)
        with self._lock:
            if key not in self._data:
                self._data[key] = self._init_data(key)
            data = self._data[key]
            data["sum"] += value
            data["count"] += 1
            for bucket in self.buckets:
                if value <= bucket:
                    data["buckets"][bucket] += 1

    def get_sum(self, labels: Optional[Dict[str, str]] = None) -> float:
        """Get the sum of observations for the given labels."""
        key = self._label_key(labels)
        with self._lock:
            if key not in self._data:
                return 0.0
            return float(self._data[key]["sum"])

    def get_count(self, labels: Optional[Dict[str, str]] = None) -> int:
        """Get the count of observations for the given labels."""
        key = self._label_key(labels)
        with self._lock:
            if key not in self._data:
                return 0
            return int(self._data[key]["count"])

    def get_total_sum(self) -> float:
        """Get the sum of all observations across all label combinations."""
        with self._lock:
            return float(sum(data["sum"] for data in self._data.values()))

    def get_total_count(self) -> int:
        """Get the count of all observations across all label combinations."""
        with self._lock:
            return int(sum(data["count"] for data in self._data.values()))

    def get_buckets(self, labels: Optional[Dict[str, str]] = None) -> List[HistogramBucket]:
        """Get histogram buckets with counts."""
        key = self._label_key(labels)
        with self._lock:
            if key not in self._data:
                return [HistogramBucket(b, 0) for b in self.buckets]
            buckets_data = self._data[key]["buckets"]
            return [HistogramBucket(b, buckets_data[b]) for b in self.buckets]

    def reset(self) -> None:
        """Reset all histogram data."""
        with self._lock:
            self._data.clear()


class SimpleMetricsCollector(MetricsCollector):
    """Concrete metrics collector with Counter, Gauge, and Histogram support.

    Provides thread-safe metrics collection with support for labels/tags
    and export to logs or file.

    Example:
        >>> collector = SimpleMetricsCollector()
        >>> # Use with timed_request or manually
        >>> collector.requests_total.inc(labels={"method": "GET"})
        >>> collector.export_to_log()
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()

        # Pre-defined metrics for HTTP requests
        self.requests_total = Counter("trix_requests_total", "Total HTTP requests")
        self.requests_success = Counter("trix_requests_success", "Successful HTTP requests")
        self.requests_failed = Counter("trix_requests_failed", "Failed HTTP requests")
        self.retries_total = Counter("trix_retries_total", "Total retry attempts")

        self.request_duration_ms = Histogram(
            "trix_request_duration_ms",
            "HTTP request duration in milliseconds",
        )
        self.request_size_bytes = Histogram(
            "trix_request_size_bytes",
            "HTTP request body size in bytes",
            buckets=(100, 500, 1000, 5000, 10000, 50000, 100000),
        )
        self.response_size_bytes = Histogram(
            "trix_response_size_bytes",
            "HTTP response body size in bytes",
            buckets=(100, 500, 1000, 5000, 10000, 50000, 100000),
        )

        self.in_flight_requests = Gauge(
            "trix_in_flight_requests",
            "Number of currently in-flight requests",
        )

    def on_request_start(
        self, method: str, path: str, labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Track request start by incrementing in-flight gauge."""
        metric_labels = {"method": method}
        if labels:
            metric_labels.update(labels)
        self.in_flight_requests.inc(labels=metric_labels)

    def on_request_complete(self, metrics: RequestMetrics) -> None:
        """Record metrics when a request completes."""
        labels = {"method": metrics.method, "path": metrics.path}
        if metrics.status_code:
            labels["status"] = str(metrics.status_code)
        labels.update(metrics.labels)

        self.requests_total.inc(labels=labels)

        if metrics.success:
            self.requests_success.inc(labels=labels)
        else:
            self.requests_failed.inc(labels=labels)

        self.request_duration_ms.observe(metrics.duration_ms, labels=labels)

        if metrics.request_size is not None:
            self.request_size_bytes.observe(metrics.request_size, labels=labels)

        if metrics.response_size is not None:
            self.response_size_bytes.observe(metrics.response_size, labels=labels)

        # Decrement in-flight requests
        self.in_flight_requests.dec(labels={"method": metrics.method})

    def on_retry(
        self,
        method: str,
        path: str,
        attempt: int,
        error: Exception,
        delay_ms: float,
    ) -> None:
        """Record retry attempts."""
        labels = {
            "method": method,
            "path": path,
            "error_type": type(error).__name__,
        }
        self.retries_total.inc(labels=labels)

    def get_snapshot(self) -> Dict[str, Any]:
        """Get a snapshot of all metrics as a dictionary."""
        return {
            "requests_total": [
                {"value": m.value, "labels": m.labels} for m in self.requests_total.get_all()
            ],
            "requests_success": [
                {"value": m.value, "labels": m.labels} for m in self.requests_success.get_all()
            ],
            "requests_failed": [
                {"value": m.value, "labels": m.labels} for m in self.requests_failed.get_all()
            ],
            "retries_total": [
                {"value": m.value, "labels": m.labels} for m in self.retries_total.get_all()
            ],
            "in_flight_requests": [
                {"value": m.value, "labels": m.labels} for m in self.in_flight_requests.get_all()
            ],
            "request_duration_ms": {
                "sum": self.request_duration_ms.get_total_sum(),
                "count": self.request_duration_ms.get_total_count(),
            },
            "timestamp": time.time(),
        }

    def export_to_log(self, level: int = logging.INFO) -> None:
        """Export metrics to the logger."""
        snapshot = self.get_snapshot()
        logger.log(level, "Metrics snapshot: %s", json.dumps(snapshot, default=str))

    def export_to_file(self, path: Path) -> None:
        """Export metrics to a JSON file."""
        snapshot = self.get_snapshot()
        path.write_text(json.dumps(snapshot, indent=2, default=str))

    def reset(self) -> None:
        """Reset all metrics."""
        self.requests_total.reset()
        self.requests_success.reset()
        self.requests_failed.reset()
        self.retries_total.reset()
        self.request_duration_ms.reset()
        self.request_size_bytes.reset()
        self.response_size_bytes.reset()
        self.in_flight_requests.reset()
