"""
Sandbox manager for orchestrating isolated binary processing.

This module provides the SandboxManager class that orchestrates the entire
lifecycle of sandboxed binary parsing, including:
- Creating isolated temporary directories
- Spawning worker processes with resource limits
- Managing IPC communication
- Handling timeouts and errors
- Cleaning up resources

The SandboxManager is the main public API for sandboxed binary processing.
"""

import logging
import multiprocessing
import os
import queue
import time
from typing import Any, Dict, Optional

from binary_sbom.sandbox.config import SandboxConfig, load_config
from binary_sbom.sandbox.errors import (
    SandboxCrashedError,
    SandboxError,
    SandboxFileError,
    SandboxMemoryError,
    SandboxSecurityError,
    SandboxTimeoutError,
)
from binary_sbom.sandbox.limits import DEFAULT_RESOURCE_LIMITS, ResourceLimits
from binary_sbom.sandbox.metrics import SandboxMetrics, get_global_metrics
from binary_sbom.sandbox.security_logger import (
    log_sandbox_completed,
    log_sandbox_memory_limit,
    log_sandbox_spawn,
    log_sandbox_terminated,
    log_sandbox_timeout,
    log_security_violation,
    log_unusual_error,
)
from binary_sbom.sandbox.tempfile import TempDirectory
from binary_sbom.sandbox.worker import worker_main


logger = logging.getLogger(__name__)


class SandboxManager:
    """
    Manage sandboxed binary parsing operations.

    The SandboxManager orchestrates the complete lifecycle of sandboxed
    binary processing, from creating isolated environments to cleanup.

    Example:
        >>> # Use defaults (from environment or hardcoded defaults)
        >>> manager = SandboxManager()
        >>> metadata = manager.parse_binary('/path/to/binary')
        >>> print(metadata['type'])
        'ELF'

        >>> # With custom limits
        >>> manager = SandboxManager(
        ...     memory_mb=1000,
        ...     cpu_time_seconds=60,
        ...     wall_clock_timeout=120
        ... )
        >>> metadata = manager.parse_binary('/path/to/binary')

        >>> # With SandboxConfig object
        >>> from binary_sbom.sandbox.config import SandboxConfig
        >>> config = SandboxConfig(memory_mb=1000, cpu_time_seconds=60)
        >>> manager = SandboxManager(sandbox_config=config)
        >>> metadata = manager.parse_binary('/path/to/binary')

        >>> # Load from configuration file
        >>> config = SandboxConfig.from_file('sandbox_config.yaml')
        >>> manager = SandboxManager(sandbox_config=config)
        >>> metadata = manager.parse_binary('/path/to/binary')
    """

    def __init__(
        self,
        memory_mb: Optional[int] = None,
        cpu_time_seconds: Optional[int] = None,
        wall_clock_timeout: Optional[int] = None,
        config: Optional[Dict[str, int]] = None,
        sandbox_config: Optional[SandboxConfig] = None,
        metrics: Optional[SandboxMetrics] = None,
    ):
        """
        Initialize SandboxManager with resource limits.

        Args:
            memory_mb: Maximum memory in megabytes (default: from env or 500).
            cpu_time_seconds: Maximum CPU time in seconds (default: from env or 30).
            wall_clock_timeout: Wall-clock timeout in seconds (default: from env or 60).
            config: (Deprecated) Alternative way to pass all limits as a dictionary.
                    Use sandbox_config instead.
            sandbox_config: SandboxConfig object with all configuration options.
            metrics: Optional SandboxMetrics instance for collecting metrics.
                     If not provided, uses the global metrics instance.

        Raises:
            ValueError: If limit values are invalid (e.g., negative).

        Priority order (highest to lowest):
            1. sandbox_config parameter
            2. Individual parameters (memory_mb, cpu_time_seconds, wall_clock_timeout)
            3. config dict (deprecated, for backward compatibility)
            4. Environment variables
            5. Hardcoded defaults
        """
        # Use sandbox_config if provided
        if sandbox_config is not None:
            self.sandbox_config = sandbox_config
            self.resource_limits = ResourceLimits(
                memory_mb=sandbox_config.memory_mb,
                cpu_time_seconds=sandbox_config.cpu_time_seconds,
                wall_clock_timeout=sandbox_config.wall_clock_timeout,
            )
        elif config:
            # Backward compatibility with old config dict
            self.resource_limits = ResourceLimits.from_dict(config)
            self.sandbox_config = SandboxConfig(
                memory_mb=self.resource_limits.memory_mb,
                cpu_time_seconds=self.resource_limits.cpu_time_seconds,
                wall_clock_timeout=self.resource_limits.wall_clock_timeout,
            )
        else:
            # Create from defaults or environment variables
            self.sandbox_config = SandboxConfig.from_environment()
            # Override with explicit parameters if provided
            if memory_mb is not None:
                self.sandbox_config.memory_mb = memory_mb
            if cpu_time_seconds is not None:
                self.sandbox_config.cpu_time_seconds = cpu_time_seconds
            if wall_clock_timeout is not None:
                self.sandbox_config.wall_clock_timeout = wall_clock_timeout

            # Re-validate after overrides
            self.sandbox_config._validate()

            self.resource_limits = ResourceLimits(
                memory_mb=self.sandbox_config.memory_mb,
                cpu_time_seconds=self.sandbox_config.cpu_time_seconds,
                wall_clock_timeout=self.sandbox_config.wall_clock_timeout,
            )

        self.temp_manager = TempDirectory()
        self.logger = logger

        # Initialize metrics collector (use provided instance or global)
        if metrics is not None:
            self.metrics = metrics
        else:
            self.metrics = get_global_metrics()

        # Validate limits (after logger is initialized)
        self._validate_limits()

    def _validate_limits(self) -> None:
        """
        Validate resource limit values.

        Raises:
            ValueError: If any limit value is invalid.
        """
        if self.resource_limits.memory_mb <= 0:
            raise ValueError(f"Memory limit must be positive: {self.resource_limits.memory_mb} MB")

        if self.resource_limits.cpu_time_seconds <= 0:
            raise ValueError(
                f"CPU time limit must be positive: {self.resource_limits.cpu_time_seconds} s"
            )

        if self.resource_limits.wall_clock_timeout <= 0:
            raise ValueError(
                f"Wall-clock timeout must be positive: {self.resource_limits.wall_clock_timeout} s"
            )

        # Sanity check: wall-clock timeout should be >= CPU time
        if self.resource_limits.wall_clock_timeout < self.resource_limits.cpu_time_seconds:
            self.logger.warning(
                f"Wall-clock timeout ({self.resource_limits.wall_clock_timeout}s) "
                f"is less than CPU time limit ({self.resource_limits.cpu_time_seconds}s). "
                f"This may cause premature timeouts."
            )

    def parse_binary(self, file_path: str, max_file_size_mb: int = 100) -> Dict[str, Any]:
        """
        Parse binary file in sandboxed process.

        This is the main entry point for sandboxed binary processing. It:
        1. Creates an isolated temporary directory
        2. Copies the binary file to the isolated directory
        3. Spawns a worker process with resource limits
        4. Waits for the result with timeout
        5. Cleans up all resources

        Args:
            file_path: Path to the binary file to parse.
            max_file_size_mb: Maximum file size in MB (default: 100).

        Returns:
            Dictionary containing parsed binary metadata with keys:
            - name (str): Binary name
            - type (str): Binary format (ELF, PE, MachO, Raw)
            - architecture (str): Target architecture
            - entrypoint (Optional[str]): Entry point address
            - sections (List[Dict]): Section information
            - dependencies (List[str]): Imported libraries

        Raises:
            SandboxSecurityError: If security validation fails (symlinks, etc.).
            SandboxTimeoutError: If parsing exceeds time limits.
            SandboxMemoryError: If parsing exceeds memory limits.
            SandboxFileError: If file operations fail.
            SandboxCrashedError: If worker process crashes.
            SandboxError: For other sandbox-related errors.
            FileNotFoundError: If input file doesn't exist.
            ValueError: If file is too large or invalid.

        Example:
            >>> manager = SandboxManager()
            >>> metadata = manager.parse_binary('/bin/ls')
            >>> print(f"Format: {metadata['type']}")
            Format: ELF
            >>> print(f"Arch: {metadata['architecture']}")
            Arch: x86_64
        """
        # Validate input file before spawning process
        self._validate_input_file(file_path, max_file_size_mb)

        # Get file size for logging
        try:
            file_size = os.path.getsize(file_path)
        except OSError:
            file_size = None

        temp_dir = None
        process = None
        result_queue = None
        error_queue = None

        try:
            # Step 1: Create isolated temporary directory
            temp_dir = self.temp_manager.create()
            self.logger.debug(f"Created temporary directory: {temp_dir}")

            # Step 2: Copy binary to isolated directory
            isolated_path = self.temp_manager.copy_file(file_path, temp_dir)
            self.logger.debug(f"Copied binary to isolated location: {isolated_path}")

            # Step 3: Setup IPC queues
            result_queue = multiprocessing.Queue()
            error_queue = multiprocessing.Queue()

            # Step 4: Spawn worker process
            process = multiprocessing.Process(
                target=worker_main,
                args=(
                    isolated_path,
                    result_queue,
                    error_queue,
                    self.resource_limits.to_dict(),
                ),
            )

            process.start()

            # Record metrics for sandbox spawn
            self.metrics.record_spawn(file_path, file_size or 0)

            # Log sandbox spawn event
            log_sandbox_spawn(
                pid=process.pid,
                file_path=file_path,
                resource_limits=self.resource_limits.to_dict(),
                file_size_bytes=file_size,
            )

            # Step 5: Wait for result with timeout
            start_time = time.time()
            try:
                result = result_queue.get(timeout=self.resource_limits.wall_clock_timeout)
                elapsed_time = time.time() - start_time

                # Check for errors from worker via error_queue
                # Worker sends errors to error_queue as (error_type, error_msg) tuples
                try:
                    if not error_queue.empty():
                        error_type, error_msg = error_queue.get_nowait()

                        # Check if this is a memory limit error
                        if error_type == "MemoryError":
                            # Record metrics for memory limit violation
                            self.metrics.record_memory_limit(
                                file_path, self.resource_limits.memory_mb
                            )

                            log_sandbox_memory_limit(
                                pid=process.pid,
                                file_path=file_path,
                                memory_limit_mb=self.resource_limits.memory_mb,
                            )

                        self.logger.error(
                            f"Worker process {process.pid} reported error: {error_type}: {error_msg}"
                        )
                        self._handle_worker_error(error_type, error_msg)
                except queue.Empty:
                    # No error in queue, proceed with result
                    pass

                # Log successful completion
                # Extract resource usage from result if available
                resource_usage = None
                if isinstance(result, dict) and "_resource_usage" in result:
                    resource_usage = result.pop("_resource_usage", None)

                # Record metrics for successful completion
                self.metrics.record_completion(file_path, elapsed_time, resource_usage)

                log_sandbox_completed(
                    pid=process.pid,
                    file_path=file_path,
                    resource_usage=resource_usage,
                )

                return result

            except queue.Empty:
                # Timeout - terminate process
                elapsed_time = time.time() - start_time

                # Record metrics for timeout
                self.metrics.record_timeout(
                    file_path, "wall_clock", self.resource_limits.wall_clock_timeout
                )

                log_sandbox_timeout(
                    pid=process.pid,
                    file_path=file_path,
                    timeout_type="wall_clock",
                    timeout_value=self.resource_limits.wall_clock_timeout,
                    elapsed_seconds=elapsed_time,
                )

                self._terminate_process(process)

                # Log forced termination
                log_sandbox_terminated(
                    pid=process.pid,
                    file_path=file_path,
                    termination_type="forced",
                    reason="wall_clock_timeout",
                )

                raise SandboxTimeoutError(
                    f"Sandbox exceeded wall-clock timeout "
                    f"({self.resource_limits.wall_clock_timeout}s)"
                )

        except SandboxSecurityError as e:
            # Record metrics for security violations
            # Extract violation type from error details if available
            violation_type = "unknown"
            if hasattr(e, "details") and isinstance(e.details, dict):
                violation_type = e.details.get("violation_type", "unknown")

            self.metrics.record_security_violation(
                file_path, violation_type, getattr(e, "details", None)
            )

            # Re-raise security error
            raise

        except SandboxError:
            # Re-raise other sandbox errors as-is
            raise

        except (OSError, IOError) as e:
            # File system errors
            raise SandboxFileError(f"File operation failed: {e}") from e

        except Exception as e:
            # Unexpected errors
            self.logger.error(f"Unexpected error in sandbox: {e}", exc_info=True)
            log_unusual_error(
                pid=process.pid if process else None,
                file_path=file_path,
                error_type=type(e).__name__,
                error_message=str(e),
            )
            raise SandboxError(f"Sandbox runtime error: {e}") from e

        finally:
            # Step 6: Always cleanup resources
            cleanup_errors = []

            # Cleanup IPC queues
            if result_queue:
                try:
                    result_queue.close()
                except Exception as e:
                    cleanup_errors.append(f"Failed to close result queue: {e}")

            if error_queue:
                try:
                    error_queue.close()
                except Exception as e:
                    cleanup_errors.append(f"Failed to close error queue: {e}")

            # Terminate process if still alive
            if process and process.is_alive():
                try:
                    self._terminate_process(process)
                    log_sandbox_terminated(
                        pid=process.pid,
                        file_path=file_path,
                        termination_type="forced",
                        reason="cleanup",
                    )
                except Exception as e:
                    cleanup_errors.append(f"Failed to terminate process: {e}")
            elif process and not process.is_alive():
                # Process has already terminated, log the exit
                exit_code = process.exitcode
                if exit_code != 0:
                    # Check if exit_code is an integer (not a Mock)
                    if isinstance(exit_code, int):
                        termination_type = "crashed" if exit_code < 0 else "normal"
                        reason = "process_exited_with_error" if exit_code > 0 else "process_signaled"
                    else:
                        # For testing with Mock objects
                        termination_type = "normal"
                        reason = "process_exited"

                    # Record metrics for crashes
                    if termination_type == "crashed":
                        self.metrics.record_crash(file_path, exit_code)

                    log_sandbox_terminated(
                        pid=process.pid,
                        file_path=file_path,
                        termination_type=termination_type,
                        exit_code=exit_code,
                        reason=reason,
                    )

            # Cleanup temporary directory
            if temp_dir:
                try:
                    self.temp_manager.cleanup(temp_dir)
                    self.logger.debug(f"Cleaned up temporary directory: {temp_dir}")
                except Exception as e:
                    cleanup_errors.append(f"Failed to cleanup temp directory: {e}")

            # Log any cleanup errors (non-fatal)
            if cleanup_errors:
                for error in cleanup_errors:
                    self.logger.warning(f"Cleanup error: {error}")

    def _validate_input_file(self, file_path: str, max_file_size_mb: int) -> None:
        """
        Validate input file before spawning sandbox.

        Args:
            file_path: Path to input file.
            max_file_size_mb: Maximum file size in MB.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If file is invalid or too large.
            SandboxFileError: If file cannot be read.
        """
        import os

        from pathlib import Path

        path = Path(file_path)

        # Check file exists
        if not path.exists():
            raise FileNotFoundError(f"Binary file not found: {file_path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")

        # Check file permissions
        if not os.access(file_path, os.R_OK):
            raise SandboxFileError(f"Permission denied: Cannot read file {file_path}")

        # Check file size
        try:
            file_size = path.stat().st_size
            if file_size == 0:
                raise ValueError(f"File is empty: {file_path}")

            max_size_bytes = max_file_size_mb * 1024 * 1024
            if file_size > max_size_bytes:
                size_mb = file_size / 1024 / 1024
                raise ValueError(
                    f"File too large: {file_path} ({size_mb:.2f} MB). "
                    f"Maximum size is {max_file_size_mb} MB."
                )
        except OSError as e:
            # Record metrics for file error
            self.metrics.record_file_error(file_path, type(e).__name__)
            raise SandboxFileError(f"Cannot access file {file_path}: {e}") from e

    def get_metrics(self) -> SandboxMetrics:
        """
        Get the metrics collector instance.

        Returns:
            The SandboxMetrics instance used by this manager.
        """
        return self.metrics

    def get_metrics_summary(self) -> Dict[str, Any]:
        """
        Get a summary of collected metrics.

        Returns:
            Dictionary containing metrics summary.
        """
        return self.metrics.get_summary()

    def _terminate_process(self, process: multiprocessing.Process) -> None:
        """
        Terminate a process gracefully or forcefully if needed.

        Args:
            process: Process to terminate.
        """
        if not process.is_alive():
            return

        try:
            # Try graceful termination first
            process.terminate()
            process.join(timeout=5)

            if process.is_alive():
                # Force kill if terminate didn't work
                self.logger.warning(
                    f"Process {process.pid} did not terminate gracefully, killing"
                )
                process.kill()
                process.join(timeout=5)

                if process.is_alive():
                    self.logger.error(f"Process {process.pid} could not be killed")
                    log_sandbox_terminated(
                        pid=process.pid,
                        file_path="<unknown>",
                        termination_type="forced",
                        reason="kill_failed",
                    )

        except Exception as e:
            self.logger.error(f"Error terminating process {process.pid}: {e}")
            log_sandbox_terminated(
                pid=process.pid,
                file_path="<unknown>",
                termination_type="forced",
                reason=f"termination_error: {e}",
            )

    def _handle_worker_error(self, error_type: str, error_message: str) -> None:
        """
        Handle error reported by worker process.

        Args:
            error_type: Type of error (e.g., "MemoryError", "TimeoutError").
            error_message: Error message from worker.

        Raises:
            SandboxError: Appropriate error type based on error_type.
        """
        error_map = {
            "MemoryError": SandboxMemoryError,
            "TimeoutError": SandboxTimeoutError,
            "ParseError": SandboxError,
            "SecurityError": SandboxSecurityError,
            "FileError": SandboxFileError,
        }

        error_class = error_map.get(error_type, SandboxError)
        raise error_class(f"Worker process error: {error_message}")

    def get_config(self) -> Dict[str, Any]:
        """
        Get current sandbox configuration.

        Returns:
            Dictionary with all configuration values (resource limits and behavioral settings).
        """
        return self.sandbox_config.to_full_dict()
