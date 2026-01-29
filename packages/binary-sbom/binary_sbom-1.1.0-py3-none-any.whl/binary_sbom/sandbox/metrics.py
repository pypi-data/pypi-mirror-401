"""
Metrics collection for sandbox operations.

This module provides a thread-safe metrics collection system for monitoring
sandboxed binary processing operations. Metrics track:
- Sandbox spawn rate
- Resource limit violations (timeouts, memory limits)
- Average processing time
- Failure rate
- Security violations

Metrics can be exported in various formats (dict, JSON, Prometheus) for
integration with monitoring and alerting systems.

Example:
    >>> from binary_sbom.sandbox import SandboxMetrics
    >>> metrics = SandboxMetrics()
    >>> metrics.record_spawn("/path/to/binary", 1024*1024)
    >>> metrics.record_completion("/path/to/binary", 0.5, {"memory_mb": 50.0})
    >>> print(metrics.get_summary())
    {'spawn_count': 1, 'completion_count': 1, ...}
"""

import json
import logging
import threading
import time
from collections import defaultdict
from typing import Any, Dict, List, Optional


logger = logging.getLogger(__name__)


class SandboxMetrics:
    """
    Thread-safe metrics collector for sandbox operations.

    This class tracks various metrics about sandbox operations including
    spawn counts, processing times, resource limit violations, and failures.

    All methods are thread-safe and can be called from multiple threads.

    Attributes:
        spawn_count: Total number of sandbox spawns.
        completion_count: Total number of successful completions.
        timeout_count: Total number of timeouts.
        memory_limit_count: Total number of memory limit violations.
        security_violation_count: Total number of security violations.
        crash_count: Total number of process crashes.
        total_processing_time_ms: Accumulated processing time in milliseconds.
    """

    def __init__(self):
        """Initialize metrics collector with zero values."""
        self._lock = threading.Lock()

        # Counters
        self._spawn_count = 0
        self._completion_count = 0
        self._timeout_count = 0
        self._memory_limit_count = 0
        self._security_violation_count = 0
        self._crash_count = 0
        self._file_error_count = 0

        # Timing
        self._total_processing_time_ms = 0.0

        # Detailed tracking (per-operation type)
        self._timeout_by_type = defaultdict(int)  # wall_clock, cpu_time
        self._security_violation_by_type = defaultdict(int)  # symlink, path_traversal

        # Per-file tracking (last N operations for debugging)
        self._recent_operations: List[Dict[str, Any]] = []
        self._max_recent_operations = 100

    def record_spawn(self, file_path: str, file_size_bytes: int) -> None:
        """
        Record a sandbox spawn event.

        Args:
            file_path: Path to binary being processed.
            file_size_bytes: Size of binary file in bytes.
        """
        with self._lock:
            self._spawn_count += 1

            # Track recent operation
            self._add_recent_operation(
                {
                    "operation": "spawn",
                    "file": self._sanitize_path(file_path),
                    "file_size_bytes": file_size_bytes,
                    "timestamp": time.time(),
                }
            )

        logger.debug(f"Metrics: Recorded spawn (total: {self._spawn_count})")

    def record_completion(
        self,
        file_path: str,
        processing_time_seconds: float,
        resource_usage: Optional[Dict[str, float]] = None,
    ) -> None:
        """
        Record a successful completion event.

        Args:
            file_path: Path to processed binary.
            processing_time_seconds: Processing time in seconds.
            resource_usage: Optional resource usage statistics.
        """
        with self._lock:
            self._completion_count += 1
            self._total_processing_time_ms += processing_time_seconds * 1000

            # Track recent operation
            operation = {
                "operation": "completion",
                "file": self._sanitize_path(file_path),
                "processing_time_ms": round(processing_time_seconds * 1000, 2),
                "timestamp": time.time(),
            }

            if resource_usage:
                operation["resource_usage"] = {
                    "memory_mb": round(resource_usage.get("memory_mb", 0), 2),
                    "cpu_time_seconds": round(resource_usage.get("cpu_time_seconds", 0), 2),
                }

            self._add_recent_operation(operation)

        logger.debug(f"Metrics: Recorded completion (total: {self._completion_count})")

    def record_timeout(
        self, file_path: str, timeout_type: str, timeout_value: int
    ) -> None:
        """
        Record a timeout event.

        Args:
            file_path: Path to binary being processed.
            timeout_type: Type of timeout ("wall_clock" or "cpu_time").
            timeout_value: Timeout limit in seconds.
        """
        with self._lock:
            self._timeout_count += 1
            self._timeout_by_type[timeout_type] += 1

            # Track recent operation
            self._add_recent_operation(
                {
                    "operation": "timeout",
                    "file": self._sanitize_path(file_path),
                    "timeout_type": timeout_type,
                    "timeout_value_seconds": timeout_value,
                    "timestamp": time.time(),
                }
            )

        logger.debug(f"Metrics: Recorded timeout (total: {self._timeout_count})")

    def record_memory_limit(
        self, file_path: str, memory_limit_mb: int
    ) -> None:
        """
        Record a memory limit violation.

        Args:
            file_path: Path to binary being processed.
            memory_limit_mb: Memory limit in megabytes.
        """
        with self._lock:
            self._memory_limit_count += 1

            # Track recent operation
            self._add_recent_operation(
                {
                    "operation": "memory_limit",
                    "file": self._sanitize_path(file_path),
                    "memory_limit_mb": memory_limit_mb,
                    "timestamp": time.time(),
                }
            )

        logger.debug(f"Metrics: Recorded memory limit (total: {self._memory_limit_count})")

    def record_security_violation(
        self, file_path: str, violation_type: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Record a security violation event.

        Args:
            file_path: Path to binary being processed.
            violation_type: Type of violation ("symlink", "path_traversal", etc.).
            details: Optional additional details about the violation.
        """
        with self._lock:
            self._security_violation_count += 1
            self._security_violation_by_type[violation_type] += 1

            # Track recent operation
            operation = {
                "operation": "security_violation",
                "file": self._sanitize_path(file_path),
                "violation_type": violation_type,
                "timestamp": time.time(),
            }

            if details:
                # Sanitize details
                sanitized_details = {}
                for key, value in details.items():
                    if key.lower() in ["path", "file", "filename", "directory"]:
                        sanitized_details[key] = self._sanitize_path(str(value))
                    elif isinstance(value, str):
                        # Truncate long strings
                        sanitized_details[key] = value[:200]
                    else:
                        sanitized_details[key] = value
                operation["details"] = sanitized_details

            self._add_recent_operation(operation)

        logger.debug(f"Metrics: Recorded security violation (total: {self._security_violation_count})")

    def record_crash(self, file_path: str, exit_code: Optional[int] = None) -> None:
        """
        Record a process crash event.

        Args:
            file_path: Path to binary being processed.
            exit_code: Optional process exit code.
        """
        with self._lock:
            self._crash_count += 1

            # Track recent operation
            operation = {
                "operation": "crash",
                "file": self._sanitize_path(file_path),
                "timestamp": time.time(),
            }

            if exit_code is not None:
                operation["exit_code"] = exit_code

            self._add_recent_operation(operation)

        logger.debug(f"Metrics: Recorded crash (total: {self._crash_count})")

    def record_file_error(self, file_path: str, error_type: str) -> None:
        """
        Record a file system error event.

        Args:
            file_path: Path to binary being processed.
            error_type: Type of file error.
        """
        with self._lock:
            self._file_error_count += 1

            # Track recent operation
            self._add_recent_operation(
                {
                    "operation": "file_error",
                    "file": self._sanitize_path(file_path),
                    "error_type": error_type,
                    "timestamp": time.time(),
                }
            )

        logger.debug(f"Metrics: Recorded file error (total: {self._file_error_count})")

    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all metrics.

        Returns:
            Dictionary containing:
            - spawn_count: Total sandbox spawns
            - completion_count: Total successful completions
            - timeout_count: Total timeouts
            - memory_limit_count: Total memory limit violations
            - security_violation_count: Total security violations
            - crash_count: Total crashes
            - file_error_count: Total file errors
            - average_processing_time_ms: Average processing time in milliseconds
            - failure_rate: Failure rate as percentage (0-100)
            - spawn_rate_per_minute: Estimated spawns per minute (based on recent operations)
        """
        with self._lock:
            # Calculate average processing time
            if self._completion_count > 0:
                avg_processing_time_ms = self._total_processing_time_ms / self._completion_count
            else:
                avg_processing_time_ms = 0.0

            # Calculate failure rate
            if self._spawn_count > 0:
                failures = (
                    self._timeout_count
                    + self._memory_limit_count
                    + self._security_violation_count
                    + self._crash_count
                    + self._file_error_count
                )
                failure_rate = (failures / self._spawn_count) * 100
            else:
                failure_rate = 0.0

            # Calculate spawn rate (based on recent operations in last minute)
            spawn_rate_per_minute = self._calculate_spawn_rate()

            return {
                "spawn_count": self._spawn_count,
                "completion_count": self._completion_count,
                "timeout_count": self._timeout_count,
                "memory_limit_count": self._memory_limit_count,
                "security_violation_count": self._security_violation_count,
                "crash_count": self._crash_count,
                "file_error_count": self._file_error_count,
                "average_processing_time_ms": round(avg_processing_time_ms, 2),
                "failure_rate": round(failure_rate, 2),
                "spawn_rate_per_minute": round(spawn_rate_per_minute, 2),
            }

    def get_detailed_metrics(self) -> Dict[str, Any]:
        """
        Get detailed metrics including breakdowns by type.

        Returns:
            Dictionary containing all metrics plus detailed breakdowns.
        """
        with self._lock:
            summary = self.get_summary()

            # Add breakdowns
            summary["timeout_by_type"] = dict(self._timeout_by_type)
            summary["security_violation_by_type"] = dict(self._security_violation_by_type)

            # Add recent operations (limited list)
            summary["recent_operations"] = list(self._recent_operations)

            return summary

    def to_prometheus(self) -> str:
        """
        Export metrics in Prometheus text format.

        Returns:
            String containing metrics in Prometheus text exposition format.

        Example output:
            ```
            # HELP sandbox_spawn_total Total number of sandbox spawns
            # TYPE sandbox_spawn_total counter
            sandbox_spawn_total 42

            # HELP sandbox_completion_total Total number of successful completions
            # TYPE sandbox_completion_total counter
            sandbox_completion_total 38

            # HELP sandbox_timeout_total Total number of timeouts
            # TYPE sandbox_timeout_total counter
            sandbox_timeout_total 2
            ...
            ```
        """
        with self._lock:
            summary = self.get_summary()

            lines = []

            # Helper to add metric
            def add_metric(name: str, value: Any, help_text: str, metric_type: str = "gauge"):
                lines.append(f"# HELP sandbox_{name} {help_text}")
                lines.append(f"# TYPE sandbox_{name} {metric_type}")
                lines.append(f"sandbox_{name} {value}")
                lines.append("")

            # Add all metrics
            add_metric("spawn_total", summary["spawn_count"], "Total number of sandbox spawns", "counter")
            add_metric(
                "completion_total",
                summary["completion_count"],
                "Total number of successful completions",
                "counter",
            )
            add_metric("timeout_total", summary["timeout_count"], "Total number of timeouts", "counter")
            add_metric(
                "timeout_wall_clock_total",
                self._timeout_by_type.get("wall_clock", 0),
                "Total number of wall-clock timeouts",
                "counter",
            )
            add_metric(
                "timeout_cpu_time_total",
                self._timeout_by_type.get("cpu_time", 0),
                "Total number of CPU time timeouts",
                "counter",
            )
            add_metric(
                "memory_limit_total",
                summary["memory_limit_count"],
                "Total number of memory limit violations",
                "counter",
            )
            add_metric(
                "security_violation_total",
                summary["security_violation_count"],
                "Total number of security violations",
                "counter",
            )
            add_metric(
                "security_violation_symlink_total",
                self._security_violation_by_type.get("symlink", 0),
                "Total number of symlink attack attempts",
                "counter",
            )
            add_metric(
                "security_violation_path_traversal_total",
                self._security_violation_by_type.get("path_traversal", 0),
                "Total number of path traversal attempts",
                "counter",
            )
            add_metric("crash_total", summary["crash_count"], "Total number of process crashes", "counter")
            add_metric(
                "file_error_total",
                summary["file_error_count"],
                "Total number of file system errors",
                "counter",
            )
            add_metric(
                "processing_time_ms",
                summary["average_processing_time_ms"],
                "Average processing time in milliseconds",
            )
            add_metric("failure_rate", summary["failure_rate"], "Failure rate percentage")
            add_metric(
                "spawn_rate_per_minute",
                summary["spawn_rate_per_minute"],
                "Estimated spawns per minute",
            )

            return "\n".join(lines)

    def to_json(self, pretty: bool = True) -> str:
        """
        Export metrics as JSON string.

        Args:
            pretty: If True, format JSON with indentation. If False, compact format.

        Returns:
            JSON string containing all metrics.
        """
        with self._lock:
            metrics = self.get_detailed_metrics()

            if pretty:
                return json.dumps(metrics, indent=2)
            else:
                return json.dumps(metrics)

    def reset(self) -> None:
        """Reset all metrics to zero."""
        with self._lock:
            self._spawn_count = 0
            self._completion_count = 0
            self._timeout_count = 0
            self._memory_limit_count = 0
            self._security_violation_count = 0
            self._crash_count = 0
            self._file_error_count = 0
            self._total_processing_time_ms = 0.0
            self._timeout_by_type = defaultdict(int)
            self._security_violation_by_type = defaultdict(int)
            self._recent_operations = []

        logger.info("Metrics: Reset all metrics to zero")

    def _sanitize_path(self, file_path: str) -> str:
        """
        Sanitize file path for metrics (hide system structure).

        Args:
            file_path: Original file path.

        Returns:
            Sanitized path showing only filename and parent directory.
        """
        try:
            from pathlib import Path

            path = Path(file_path)
            filename = path.name
            parent = path.parent.name if path.parent.name else ""

            if parent:
                return f".../{parent}/{filename}"
            else:
                return f".../{filename}"
        except Exception:
            # If path parsing fails, return safe placeholder
            return "<sanitized_path>"

    def _add_recent_operation(self, operation: Dict[str, Any]) -> None:
        """
        Add operation to recent operations list, maintaining max size.

        Args:
            operation: Operation dictionary to add.
        """
        self._recent_operations.append(operation)

        # Keep only the most recent operations
        if len(self._recent_operations) > self._max_recent_operations:
            self._recent_operations = self._recent_operations[-self._max_recent_operations:]

    def _calculate_spawn_rate(self) -> float:
        """
        Calculate spawn rate per minute based on recent operations.

        Returns:
            Estimated spawns per minute.
        """
        if not self._recent_operations:
            return 0.0

        now = time.time()
        one_minute_ago = now - 60

        # Count spawns in last minute
        recent_spawns = sum(
            1 for op in self._recent_operations if op.get("operation") == "spawn" and op.get("timestamp", 0) >= one_minute_ago
        )

        return float(recent_spawns)


# Global metrics instance
_global_metrics: Optional[SandboxMetrics] = None
_global_metrics_lock = threading.Lock()


def get_global_metrics() -> SandboxMetrics:
    """
    Get the global metrics instance.

    This function returns a singleton SandboxMetrics instance that can be
    shared across all SandboxManager instances in the process.

    Returns:
        The global SandboxMetrics instance.
    """
    global _global_metrics

    with _global_metrics_lock:
        if _global_metrics is None:
            _global_metrics = SandboxMetrics()
            logger.debug("Created global metrics instance")

        return _global_metrics


def reset_global_metrics() -> None:
    """Reset the global metrics instance to zero."""
    with _global_metrics_lock:
        if _global_metrics is not None:
            _global_metrics.reset()
