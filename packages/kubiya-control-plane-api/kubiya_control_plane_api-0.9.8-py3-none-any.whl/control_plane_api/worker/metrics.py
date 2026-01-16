"""
Prometheus Metrics Collection for Agent Runtime

Collects and exposes metrics for monitoring agent-runtime executions.
"""

import time
import structlog
from typing import Optional

logger = structlog.get_logger(__name__)

# Try to import prometheus_client, but make it optional
try:
    from prometheus_client import Counter, Histogram, Gauge, Info
    PROMETHEUS_AVAILABLE = True
except ImportError:
    logger.warning("prometheus_client_not_installed", message="Metrics collection disabled. Install with: pip install prometheus-client")
    PROMETHEUS_AVAILABLE = False


# Metrics definitions (only if prometheus available)
if PROMETHEUS_AVAILABLE:
    # Execution counter
    execution_count = Counter(
        "agent_runtime_executions_total",
        "Total number of agent executions",
        ["status", "runtime_type"],
    )

    # Execution duration histogram
    execution_duration = Histogram(
        "agent_runtime_execution_duration_seconds",
        "Execution duration in seconds",
        buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0],
    )

    # Active executions gauge
    active_executions = Gauge(
        "agent_runtime_active_executions",
        "Number of currently active executions",
    )

    # Token usage counter
    token_usage = Counter(
        "agent_runtime_tokens_total",
        "Total number of tokens used",
        ["type"],  # input, output
    )

    # Tool execution counter
    tool_executions = Counter(
        "agent_runtime_tool_executions_total",
        "Total number of tool executions",
        ["tool_name", "status"],
    )

    # Agent runtime info
    runtime_info = Info(
        "agent_runtime",
        "Agent runtime information",
    )

    # Health check counter
    health_checks = Counter(
        "agent_runtime_health_checks_total",
        "Total number of health checks",
        ["status"],  # healthy, unhealthy
    )

    # Restart counter
    restarts = Counter(
        "agent_runtime_restarts_total",
        "Total number of agent-runtime server restarts",
    )


class MetricsCollector:
    """Collects metrics for agent-runtime executions."""

    def __init__(self, enabled: bool = True):
        """
        Initialize metrics collector.

        Args:
            enabled: Enable metrics collection (default: True)
        """
        self.enabled = enabled and PROMETHEUS_AVAILABLE

        if self.enabled:
            logger.info("metrics_collector_enabled")
            # Set runtime info
            runtime_info.info({
                "version": "0.1.0",  # TODO: Get from version module
                "runtime_type": "agent_runtime",
            })
        else:
            if not PROMETHEUS_AVAILABLE:
                logger.info("metrics_collector_disabled_prometheus_not_available")
            else:
                logger.info("metrics_collector_disabled")

    def record_execution_start(self):
        """Record the start of an execution."""
        if not self.enabled:
            return

        active_executions.inc()

    def record_execution_end(
        self,
        duration: float,
        status: str,
        runtime_type: str = "agent_runtime",
    ):
        """
        Record the end of an execution.

        Args:
            duration: Execution duration in seconds
            status: Execution status (success, error)
            runtime_type: Runtime type (default: agent_runtime)
        """
        if not self.enabled:
            return

        active_executions.dec()
        execution_count.labels(status=status, runtime_type=runtime_type).inc()
        execution_duration.observe(duration)

    def record_token_usage(self, input_tokens: int, output_tokens: int):
        """
        Record token usage.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
        """
        if not self.enabled:
            return

        token_usage.labels(type="input").inc(input_tokens)
        token_usage.labels(type="output").inc(output_tokens)

    def record_tool_execution(self, tool_name: str, status: str):
        """
        Record a tool execution.

        Args:
            tool_name: Name of the tool
            status: Execution status (success, error)
        """
        if not self.enabled:
            return

        tool_executions.labels(tool_name=tool_name, status=status).inc()

    def record_health_check(self, is_healthy: bool):
        """
        Record a health check.

        Args:
            is_healthy: Whether the health check passed
        """
        if not self.enabled:
            return

        status = "healthy" if is_healthy else "unhealthy"
        health_checks.labels(status=status).inc()

    def record_restart(self):
        """Record an agent-runtime server restart."""
        if not self.enabled:
            return

        restarts.inc()


class ExecutionMetricsContext:
    """Context manager for collecting execution metrics."""

    def __init__(
        self,
        collector: MetricsCollector,
        runtime_type: str = "agent_runtime",
    ):
        """
        Initialize context manager.

        Args:
            collector: MetricsCollector instance
            runtime_type: Runtime type (default: agent_runtime)
        """
        self.collector = collector
        self.runtime_type = runtime_type
        self.start_time: Optional[float] = None
        self.status: str = "error"  # Default to error, set to success explicitly

    def __enter__(self):
        """Enter context - start metrics collection."""
        self.start_time = time.time()
        self.collector.record_execution_start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context - record metrics."""
        if self.start_time is not None:
            duration = time.time() - self.start_time
            self.collector.record_execution_end(
                duration=duration,
                status=self.status,
                runtime_type=self.runtime_type,
            )

    def set_success(self):
        """Mark execution as successful."""
        self.status = "success"

    def set_error(self):
        """Mark execution as error."""
        self.status = "error"


# Global metrics collector instance
_global_collector: Optional[MetricsCollector] = None


def get_metrics_collector() -> MetricsCollector:
    """Get or create global metrics collector."""
    global _global_collector

    if _global_collector is None:
        import os
        enabled = os.environ.get("AGENT_RUNTIME_METRICS_ENABLED", "true").lower() in ("true", "1", "yes")
        _global_collector = MetricsCollector(enabled=enabled)

    return _global_collector
