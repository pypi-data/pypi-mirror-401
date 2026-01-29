"""
Resource limit configuration and enforcement.

This module handles resource limits for sandboxed processes using the
Python resource module (stdlib). Limits are enforced at the kernel level.

Resource limits are enforced using setrlimit():
- RLIMIT_AS: Maximum address space (memory) in bytes
- RLIMIT_CPU: Maximum CPU time in seconds

When a process exceeds these limits, the kernel terminates it with SIGSEGV
(for memory) or SIGXCPU (for CPU time).
"""

import logging
import os
import sys
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Default resource limits (can be overridden via environment variables)
DEFAULT_RESOURCE_LIMITS = {
    "memory_mb": int(os.getenv("SANDBOX_MAX_MEMORY_MB", "500")),
    "cpu_time_seconds": int(os.getenv("SANDBOX_MAX_CPU_TIME", "30")),
    "wall_clock_timeout": int(os.getenv("SANDBOX_WALL_CLOCK_TIMEOUT", "60")),
}


def check_platform_support() -> bool:
    """
    Check if resource limiting is supported on current platform.

    Returns:
        True if resource module is available (Unix), False otherwise (Windows).

    Note:
        On Windows, resource limits cannot be enforced at the kernel level.
        A warning will be logged but the sandbox will still function with
        wall-clock timeout enforcement only.
    """
    return sys.platform != "win32"


class ResourceLimits:
    """
    Manage resource limits for sandboxed processes.

    This class provides methods to apply resource limits to the current
    process. Limits are enforced using the resource module (Unix-only).

    Example:
        >>> limits = ResourceLimits(memory_mb=500, cpu_time_seconds=30)
        >>> limits.apply()  # Apply to current process
    """

    def __init__(
        self,
        memory_mb: Optional[int] = None,
        cpu_time_seconds: Optional[int] = None,
        wall_clock_timeout: Optional[int] = None,
    ):
        """
        Initialize resource limits.

        Args:
            memory_mb: Maximum memory in megabytes (default: from env or 500).
            cpu_time_seconds: Maximum CPU time in seconds (default: from env or 30).
            wall_clock_timeout: Wall-clock timeout in seconds (default: from env or 60).
        """
        self.memory_mb = memory_mb if memory_mb is not None else DEFAULT_RESOURCE_LIMITS["memory_mb"]
        self.cpu_time_seconds = cpu_time_seconds if cpu_time_seconds is not None else DEFAULT_RESOURCE_LIMITS["cpu_time_seconds"]
        self.wall_clock_timeout = wall_clock_timeout if wall_clock_timeout is not None else DEFAULT_RESOURCE_LIMITS["wall_clock_timeout"]

    def apply(self) -> None:
        """
        Apply resource limits to the current process.

        This method sets kernel-enforced resource limits using setrlimit():
        - RLIMIT_AS: Maximum address space (memory) in bytes
        - RLIMIT_CPU: Maximum CPU time in seconds

        These limits are enforced by the kernel. When exceeded:
        - Memory limit: Process terminated with SIGSEGV or SIGBUS
        - CPU limit: Process sent SIGXCPU, then SIGKILL if it continues

        Raises:
            OSError: If setrlimit fails (e.g., insufficient permissions).
            NotImplementedError: On platforms without resource module (Windows).

        Example:
            >>> limits = ResourceLimits(memory_mb=500, cpu_time_seconds=30)
            >>> limits.apply()  # Apply to current process
            >>> # Do work with enforced limits
        """
        if not check_platform_support():
            logger.warning(
                "Resource limits not supported on Windows. "
                "Only wall-clock timeout will be enforced."
            )
            return

        try:
            import resource
        except ImportError:
            logger.error("Resource module not available")
            raise NotImplementedError(
                "Resource limiting requires the 'resource' module, "
                "which is not available on this platform"
            )

        try:
            # Set memory limit (RLIMIT_AS)
            # Convert MB to bytes
            memory_bytes = self.memory_mb * 1024 * 1024
            soft_memory, hard_memory = resource.getrlimit(resource.RLIMIT_AS)

            # Set new limit (keep hard limit if it's lower)
            new_hard = hard_memory if hard_memory != resource.RLIM_INFINITY and hard_memory < memory_bytes else memory_bytes
            resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, new_hard))

            logger.debug(
                f"Set memory limit: {self.memory_mb} MB "
                f"(soft={memory_bytes}, hard={new_hard})"
            )

        except (OSError, ValueError) as e:
            logger.error(f"Failed to set memory limit: {e}")
            raise OSError(f"Cannot set memory limit: {e}") from e

        try:
            # Set CPU time limit (RLIMIT_CPU)
            soft_cpu, hard_cpu = resource.getrlimit(resource.RLIMIT_CPU)

            # Set new limit (keep hard limit if it's lower)
            new_hard_cpu = hard_cpu if hard_cpu != resource.RLIM_INFINITY and hard_cpu < self.cpu_time_seconds else self.cpu_time_seconds
            resource.setrlimit(resource.RLIMIT_CPU, (self.cpu_time_seconds, new_hard_cpu))

            logger.debug(
                f"Set CPU time limit: {self.cpu_time_seconds} seconds "
                f"(soft={self.cpu_time_seconds}, hard={new_hard_cpu})"
            )

        except (OSError, ValueError) as e:
            logger.error(f"Failed to set CPU time limit: {e}")
            raise OSError(f"Cannot set CPU time limit: {e}") from e

        logger.info(
            f"Resource limits applied: memory={self.memory_mb}MB, "
            f"cpu_time={self.cpu_time_seconds}s"
        )

    def to_dict(self) -> Dict[str, int]:
        """
        Convert limits to dictionary.

        Returns:
            Dictionary with limit values.
        """
        return {
            "memory_mb": self.memory_mb,
            "cpu_time_seconds": self.cpu_time_seconds,
            "wall_clock_timeout": self.wall_clock_timeout,
        }

    @classmethod
    def from_dict(cls, config: Dict[str, int]) -> "ResourceLimits":
        """
        Create ResourceLimits from dictionary.

        Args:
            config: Dictionary with limit values.

        Returns:
            ResourceLimits instance.
        """
        return cls(
            memory_mb=config.get("memory_mb"),
            cpu_time_seconds=config.get("cpu_time_seconds"),
            wall_clock_timeout=config.get("wall_clock_timeout"),
        )

    def get_current_usage(self) -> Dict[str, float]:
        """
        Get current resource usage of this process.

        Returns:
            Dictionary with current usage:
            - memory_mb: Current memory usage in MB
            - cpu_time_seconds: Current CPU time in seconds

        Note:
            On Windows, returns zeros for all values.
        """
        if not check_platform_support():
            return {"memory_mb": 0.0, "cpu_time_seconds": 0.0}

        try:
            import resource

            # Get current resource usage
            # ru_maxrss: maximum resident set size (in KB on Linux, bytes on macOS)
            # ru_utime + ru_stime: user + system CPU time
            usage = resource.getrusage(resource.RUSAGE_SELF)

            # Handle platform differences in ru_maxrss
            # Linux: KB, macOS: bytes
            max_rss = usage.ru_maxrss
            if sys.platform == "darwin":
                # macOS reports bytes
                memory_mb = max_rss / (1024 * 1024)
            else:
                # Linux reports KB
                memory_mb = max_rss / 1024

            # CPU time in seconds (user + system)
            cpu_time = usage.ru_utime + usage.ru_stime

            return {
                "memory_mb": round(memory_mb, 2),
                "cpu_time_seconds": round(cpu_time, 2),
            }

        except (OSError, ImportError) as e:
            logger.warning(f"Failed to get resource usage: {e}")
            return {"memory_mb": 0.0, "cpu_time_seconds": 0.0}
