"""Telemetry and metrics collection for Monora SDK.

Supports Prometheus and StatsD backends for observability.
All metrics are optional - gracefully degrades if backends are unavailable.
"""
from __future__ import annotations

import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, TypeVar

from .logger import logger

# Optional prometheus_client import
try:
    import prometheus_client
    from prometheus_client import Counter, Gauge, Histogram, REGISTRY
    PROMETHEUS_AVAILABLE = True
except ImportError:
    prometheus_client = None  # type: ignore
    PROMETHEUS_AVAILABLE = False

# Optional statsd import
try:
    import statsd
    STATSD_AVAILABLE = True
except ImportError:
    statsd = None  # type: ignore
    STATSD_AVAILABLE = False


class MetricType(Enum):
    """Metric types supported by telemetry."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"


@dataclass
class MetricDefinition:
    """Definition of a metric."""
    name: str
    type: MetricType
    description: str
    labels: List[str] = field(default_factory=list)
    buckets: Optional[List[float]] = None  # For histograms


# Standard Monora metrics
MONORA_METRICS = {
    # Event metrics
    "monora_events_total": MetricDefinition(
        name="monora_events_total",
        type=MetricType.COUNTER,
        description="Total number of events processed",
        labels=["event_type", "status"],
    ),
    "monora_events_emitted_total": MetricDefinition(
        name="monora_events_emitted_total",
        type=MetricType.COUNTER,
        description="Total number of events emitted to sinks",
        labels=["sink_type"],
    ),
    "monora_api_calls_total": MetricDefinition(
        name="monora_api_calls_total",
        type=MetricType.COUNTER,
        description="Total API call events by type and status",
        labels=["event_type", "status"],
    ),
    # Queue metrics
    "monora_queue_depth": MetricDefinition(
        name="monora_queue_depth",
        type=MetricType.GAUGE,
        description="Current event queue depth",
    ),
    "monora_queue_full_total": MetricDefinition(
        name="monora_queue_full_total",
        type=MetricType.COUNTER,
        description="Total queue full events",
    ),
    # Batch metrics
    "monora_batch_size": MetricDefinition(
        name="monora_batch_size",
        type=MetricType.GAUGE,
        description="Current effective batch size",
    ),
    # Violation metrics
    "monora_violations_total": MetricDefinition(
        name="monora_violations_total",
        type=MetricType.COUNTER,
        description="Total policy violations",
        labels=["policy_type", "model"],
    ),
    # Sink metrics
    "monora_sink_errors_total": MetricDefinition(
        name="monora_sink_errors_total",
        type=MetricType.COUNTER,
        description="Total sink errors",
        labels=["sink_type"],
    ),
    "monora_sink_write_duration_seconds": MetricDefinition(
        name="monora_sink_write_duration_seconds",
        type=MetricType.HISTOGRAM,
        description="Sink write duration in seconds",
        labels=["sink_type"],
        buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5],
    ),
    # Circuit breaker metrics
    "monora_circuit_breaker_state": MetricDefinition(
        name="monora_circuit_breaker_state",
        type=MetricType.GAUGE,
        description="Circuit breaker state (0=closed, 1=open, 2=half_open)",
        labels=["name"],
    ),
    "monora_circuit_breaker_trips_total": MetricDefinition(
        name="monora_circuit_breaker_trips_total",
        type=MetricType.COUNTER,
        description="Total circuit breaker trips",
        labels=["name"],
    ),
    # Token usage
    "monora_tokens_total": MetricDefinition(
        name="monora_tokens_total",
        type=MetricType.COUNTER,
        description="Total tokens processed",
        labels=["model", "token_type"],
    ),
    # Latency metrics
    "monora_event_latency_seconds": MetricDefinition(
        name="monora_event_latency_seconds",
        type=MetricType.HISTOGRAM,
        description="Event processing latency in seconds",
        labels=["event_type"],
        buckets=[0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0],
    ),
    # WAL metrics
    "monora_wal_writes_total": MetricDefinition(
        name="monora_wal_writes_total",
        type=MetricType.COUNTER,
        description="Total WAL write operations",
    ),
    "monora_wal_commits_total": MetricDefinition(
        name="monora_wal_commits_total",
        type=MetricType.COUNTER,
        description="Total WAL commit operations",
    ),
    "monora_wal_recoveries_total": MetricDefinition(
        name="monora_wal_recoveries_total",
        type=MetricType.COUNTER,
        description="Total events recovered from WAL",
    ),
}


class MetricsBackend(ABC):
    """Abstract base class for metrics backends."""

    @abstractmethod
    def increment(
        self, name: str, value: float = 1, labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Increment a counter."""
        pass

    @abstractmethod
    def gauge(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Set a gauge value."""
        pass

    @abstractmethod
    def observe(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Observe a histogram value."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the backend."""
        pass


class NoopBackend(MetricsBackend):
    """No-op backend when no metrics system is configured."""

    def increment(
        self, name: str, value: float = 1, labels: Optional[Dict[str, str]] = None
    ) -> None:
        pass

    def gauge(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ) -> None:
        pass

    def observe(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ) -> None:
        pass

    def close(self) -> None:
        pass


class PrometheusBackend(MetricsBackend):
    """Prometheus metrics backend.

    Requires: pip install prometheus_client
    """

    def __init__(
        self,
        port: int = 9090,
        start_server: bool = True,
        push_gateway: Optional[str] = None,
        job_name: str = "monora",
    ):
        if not PROMETHEUS_AVAILABLE:
            raise RuntimeError(
                "prometheus_client is required for PrometheusBackend. "
                "Install with: pip install prometheus_client"
            )

        self.push_gateway = push_gateway
        self.job_name = job_name
        self._metrics: Dict[str, Any] = {}
        self._lock = threading.Lock()

        # Register metrics
        self._register_metrics()

        # Start HTTP server for scraping (if not using push gateway)
        if start_server and not push_gateway:
            try:
                prometheus_client.start_http_server(port)
                logger.info("Prometheus metrics server started on port %d", port)
            except Exception as exc:
                logger.warning("Failed to start Prometheus server: %s", exc)

    def _register_metrics(self) -> None:
        """Register all Monora metrics with Prometheus."""
        for name, definition in MONORA_METRICS.items():
            try:
                if definition.type == MetricType.COUNTER:
                    self._metrics[name] = Counter(
                        name,
                        definition.description,
                        definition.labels,
                    )
                elif definition.type == MetricType.GAUGE:
                    self._metrics[name] = Gauge(
                        name,
                        definition.description,
                        definition.labels,
                    )
                elif definition.type == MetricType.HISTOGRAM:
                    self._metrics[name] = Histogram(
                        name,
                        definition.description,
                        definition.labels,
                        buckets=definition.buckets or Histogram.DEFAULT_BUCKETS,
                    )
            except ValueError:
                # Metric already registered (e.g., from previous init)
                self._metrics[name] = REGISTRY._names_to_collectors.get(name)

    def increment(
        self, name: str, value: float = 1, labels: Optional[Dict[str, str]] = None
    ) -> None:
        metric = self._metrics.get(name)
        if metric is None:
            return
        if labels:
            metric.labels(**labels).inc(value)
        else:
            metric.inc(value)

    def gauge(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ) -> None:
        metric = self._metrics.get(name)
        if metric is None:
            return
        if labels:
            metric.labels(**labels).set(value)
        else:
            metric.set(value)

    def observe(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ) -> None:
        metric = self._metrics.get(name)
        if metric is None:
            return
        if labels:
            metric.labels(**labels).observe(value)
        else:
            metric.observe(value)

    def push(self) -> None:
        """Push metrics to Prometheus Pushgateway."""
        if not self.push_gateway:
            return
        try:
            from prometheus_client import push_to_gateway
            push_to_gateway(self.push_gateway, job=self.job_name, registry=REGISTRY)
        except Exception as exc:
            logger.warning("Failed to push metrics to gateway: %s", exc)

    def close(self) -> None:
        if self.push_gateway:
            self.push()


class StatsdBackend(MetricsBackend):
    """StatsD metrics backend.

    Requires: pip install statsd
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8125,
        prefix: str = "monora",
    ):
        if not STATSD_AVAILABLE:
            raise RuntimeError(
                "statsd is required for StatsdBackend. "
                "Install with: pip install statsd"
            )

        self.client = statsd.StatsClient(host, port, prefix=prefix)
        logger.info("StatsD client connected to %s:%d", host, port)

    def _format_name(self, name: str, labels: Optional[Dict[str, str]]) -> str:
        """Format metric name with labels as tags."""
        if not labels:
            return name
        # Format: metric_name.label1_value1.label2_value2
        tag_parts = [f"{k}_{v}" for k, v in sorted(labels.items())]
        return f"{name}.{'.'.join(tag_parts)}"

    def increment(
        self, name: str, value: float = 1, labels: Optional[Dict[str, str]] = None
    ) -> None:
        formatted = self._format_name(name, labels)
        self.client.incr(formatted, count=int(value))

    def gauge(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ) -> None:
        formatted = self._format_name(name, labels)
        self.client.gauge(formatted, value)

    def observe(
        self, name: str, value: float, labels: Optional[Dict[str, str]] = None
    ) -> None:
        formatted = self._format_name(name, labels)
        # Convert seconds to milliseconds for timing
        self.client.timing(formatted, value * 1000)

    def close(self) -> None:
        # StatsD client doesn't need explicit close
        pass


class MetricsCollector:
    """Central metrics collector for Monora SDK.

    Usage:
        collector = MetricsCollector(config)
        collector.increment("monora_events_total", labels={"event_type": "llm_call"})
        collector.gauge("monora_queue_depth", 42)
        with collector.timer("monora_sink_write_duration_seconds", labels={"sink_type": "file"}):
            # do work
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._backend: MetricsBackend = NoopBackend()
        self._lock = threading.Lock()
        self._enabled = False

        self._init_backend()

    def _init_backend(self) -> None:
        """Initialize metrics backend based on config."""
        telemetry_config = self.config.get("telemetry", {})

        if not telemetry_config.get("enabled", False):
            return

        backend_type = telemetry_config.get("backend", "prometheus")

        try:
            if backend_type == "prometheus":
                prometheus_config = telemetry_config.get("prometheus", {})
                self._backend = PrometheusBackend(
                    port=prometheus_config.get("port", 9090),
                    start_server=prometheus_config.get("start_server", True),
                    push_gateway=prometheus_config.get("push_gateway"),
                    job_name=prometheus_config.get("job_name", "monora"),
                )
                self._enabled = True
            elif backend_type == "statsd":
                statsd_config = telemetry_config.get("statsd", {})
                self._backend = StatsdBackend(
                    host=statsd_config.get("host", "localhost"),
                    port=statsd_config.get("port", 8125),
                    prefix=statsd_config.get("prefix", "monora"),
                )
                self._enabled = True
            else:
                logger.warning("Unknown telemetry backend: %s", backend_type)
        except Exception as exc:
            logger.warning("Failed to initialize telemetry backend: %s", exc)

    @property
    def enabled(self) -> bool:
        """Check if metrics collection is enabled."""
        return self._enabled

    def increment(
        self,
        name: str,
        value: float = 1,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Increment a counter metric."""
        self._backend.increment(name, value, labels)

    def gauge(
        self,
        name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Set a gauge metric value."""
        self._backend.gauge(name, value, labels)

    def observe(
        self,
        name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Record a histogram observation."""
        self._backend.observe(name, value, labels)

    def timer(
        self,
        name: str,
        labels: Optional[Dict[str, str]] = None,
    ) -> "Timer":
        """Create a timer context manager for measuring duration."""
        return Timer(self, name, labels)

    def close(self) -> None:
        """Close the metrics collector."""
        self._backend.close()


class Timer:
    """Context manager for timing operations."""

    def __init__(
        self,
        collector: MetricsCollector,
        name: str,
        labels: Optional[Dict[str, str]] = None,
    ):
        self.collector = collector
        self.name = name
        self.labels = labels
        self._start: Optional[float] = None

    def __enter__(self) -> "Timer":
        self._start = time.perf_counter()
        return self

    def __exit__(self, *args: Any) -> None:
        if self._start is not None:
            duration = time.perf_counter() - self._start
            self.collector.observe(self.name, duration, self.labels)


# Global metrics collector instance
_collector: Optional[MetricsCollector] = None
_collector_lock = threading.Lock()


def get_metrics_collector() -> MetricsCollector:
    """Get the global metrics collector instance."""
    global _collector
    if _collector is None:
        with _collector_lock:
            if _collector is None:
                _collector = MetricsCollector()
    return _collector


def init_metrics(config: Dict[str, Any]) -> MetricsCollector:
    """Initialize the global metrics collector with config."""
    global _collector
    with _collector_lock:
        if _collector is not None:
            _collector.close()
        _collector = MetricsCollector(config)
    return _collector


def close_metrics() -> None:
    """Close the global metrics collector."""
    global _collector
    with _collector_lock:
        if _collector is not None:
            _collector.close()
            _collector = None


# Convenience functions for common metrics
def record_event(event_type: str, status: str = "success") -> None:
    """Record an event metric."""
    collector = get_metrics_collector()
    collector.increment(
        "monora_events_total",
        labels={"event_type": event_type, "status": status},
    )


def record_api_call(event_type: str, status: str = "unknown") -> None:
    """Record API call success/error metrics."""
    collector = get_metrics_collector()
    collector.increment(
        "monora_api_calls_total",
        labels={"event_type": event_type, "status": status},
    )


def record_violation(policy_type: str, model: str = "unknown") -> None:
    """Record a policy violation metric."""
    collector = get_metrics_collector()
    collector.increment(
        "monora_violations_total",
        labels={"policy_type": policy_type, "model": model},
    )


def record_sink_error(sink_type: str) -> None:
    """Record a sink error metric."""
    collector = get_metrics_collector()
    collector.increment(
        "monora_sink_errors_total",
        labels={"sink_type": sink_type},
    )


def record_queue_depth(depth: int) -> None:
    """Record current queue depth."""
    collector = get_metrics_collector()
    collector.gauge("monora_queue_depth", depth)


def record_tokens(model: str, prompt_tokens: int, completion_tokens: int) -> None:
    """Record token usage metrics."""
    collector = get_metrics_collector()
    if prompt_tokens > 0:
        collector.increment(
            "monora_tokens_total",
            value=prompt_tokens,
            labels={"model": model, "token_type": "prompt"},
        )
    if completion_tokens > 0:
        collector.increment(
            "monora_tokens_total",
            value=completion_tokens,
            labels={"model": model, "token_type": "completion"},
        )


def record_circuit_breaker_state(name: str, state: str) -> None:
    """Record circuit breaker state (0=closed, 1=open, 2=half_open)."""
    collector = get_metrics_collector()
    state_map = {"closed": 0, "open": 1, "half_open": 2}
    collector.gauge(
        "monora_circuit_breaker_state",
        state_map.get(state, 0),
        labels={"name": name},
    )


def record_circuit_breaker_trip(name: str) -> None:
    """Record a circuit breaker trip event."""
    collector = get_metrics_collector()
    collector.increment(
        "monora_circuit_breaker_trips_total",
        labels={"name": name},
    )


__all__ = [
    # Availability flags
    "PROMETHEUS_AVAILABLE",
    "STATSD_AVAILABLE",
    # Classes
    "MetricsCollector",
    "MetricsBackend",
    "PrometheusBackend",
    "StatsdBackend",
    "NoopBackend",
    "Timer",
    "MetricType",
    "MetricDefinition",
    # Functions
    "get_metrics_collector",
    "init_metrics",
    "close_metrics",
    # Convenience functions
    "record_event",
    "record_api_call",
    "record_violation",
    "record_sink_error",
    "record_queue_depth",
    "record_tokens",
    "record_circuit_breaker_state",
    "record_circuit_breaker_trip",
    # Metrics definitions
    "MONORA_METRICS",
]
