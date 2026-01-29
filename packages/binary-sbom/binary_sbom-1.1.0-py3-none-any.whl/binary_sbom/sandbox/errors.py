"""
Sandbox-specific exception classes.

This module defines the exception hierarchy for sandboxed binary processing.
All sandbox exceptions inherit from SandboxError for easy catching.
"""

from typing import Optional


class SandboxError(Exception):
    """
    Base exception for all sandbox-related errors.

    This exception and its subclasses are raised when errors occur during
    sandboxed binary processing, including resource limit violations,
    process crashes, timeouts, and security violations.

    Attributes:
        message: Human-readable error message.
        details: Optional dictionary with additional error context.
    """

    def __init__(self, message: str, details: Optional[dict] = None):
        """
        Initialize sandbox error.

        Args:
            message: Human-readable error message.
            details: Optional dictionary with additional error context.
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.details:
            return f"{self.message} - {self.details}"
        return self.message


class SandboxTimeoutError(SandboxError):
    """
    Raised when sandboxed process exceeds time limits.

    This occurs when:
    - Wall-clock timeout is exceeded during IPC wait
    - CPU time limit (RLIMIT_CPU) is exceeded
    - Process hangs and must be terminated

    The sandboxed process is terminated when this error is raised.
    """

    pass


class SandboxMemoryError(SandboxError):
    """
    Raised when sandboxed process exceeds memory limits.

    This occurs when the process attempts to allocate more memory than
    allowed by RLIMIT_AS. The process is terminated by the kernel when
    the limit is exceeded.

    Typical limit: 500 MB (configurable via SANDBOX_MAX_MEMORY_MB).
    """

    pass


class SandboxSecurityError(SandboxError):
    """
    Raised when a security violation is detected.

    This occurs when:
    - Symlink attacks are detected in input file
    - Path traversal attempts are detected
    - Temporary directory validation fails
    - File permission checks fail

    These errors indicate potentially malicious input.
    """

    pass


class SandboxFileError(SandboxError):
    """
    Raised when file operations fail.

    This occurs when:
    - Input file cannot be read
    - Temporary directory cannot be created
    - File cannot be copied to isolated location
    - Temporary file cleanup fails

    Most file errors are raised before spawning the sandboxed process,
    but some can occur during cleanup.
    """

    pass


class SandboxCrashedError(SandboxError):
    """
    Raised when sandboxed process crashes unexpectedly.

    This occurs when:
    - Process exits with non-zero status
    - Process terminates due to segmentation fault
    - Process is killed by a signal (SIGSEGV, SIGABRT, etc.)
    - Process exits without sending result via IPC

    The crash is contained within the sandboxed process and does not
    affect the main process.
    """

    def __init__(self, message: str, exit_code: Optional[int] = None, details: Optional[dict] = None):
        """
        Initialize crash error.

        Args:
            message: Human-readable error message.
            exit_code: Process exit code if available.
            details: Optional dictionary with additional error context.
        """
        super().__init__(message, details)
        self.exit_code = exit_code
        if exit_code is not None:
            self.details["exit_code"] = exit_code
