"""
Cancellation context for long-running API operations.

This module provides context-based cancellation support for vulnerability
scanning operations, allowing graceful interruption of long-running API calls.
"""

import logging
import threading
import time
from contextlib import contextmanager
from typing import Optional

from binary_sbom.vulnscan.exceptions import CancellationError

logger = logging.getLogger(__name__)


class CancellationContext:
    """
    Context manager for cancellable operations.

    Provides a mechanism to cancel long-running operations by setting
    a cancellation flag that can be checked during execution.

    This is particularly useful for vulnerability scanning operations
    that may take a long time to complete, allowing users to interrupt
    them gracefully.

    Attributes:
        cancelled: Flag indicating if operation has been cancelled
        reason: Reason for cancellation (if cancelled)

    Example:
        >>> ctx = CancellationContext()
        >>> with ctx:
        ...     # Long operation that checks ctx.is_cancelled()
        ...     if not ctx.is_cancelled():
        ...         # Continue operation
        ...         pass
        >>> ctx.cancel()  # Cancel from another thread if needed
    """

    def __init__(self):
        """
        Initialize cancellation context.
        """
        self._cancelled = False
        self._lock = threading.Lock()
        self._reason: Optional[str] = None

    def cancel(self, reason: str = "Operation cancelled"):
        """
        Cancel the operation.

        Sets the cancellation flag and stores the reason for cancellation.
        This method is thread-safe and can be called from any thread.

        Args:
            reason: Reason for cancellation (default: "Operation cancelled")

        Example:
            >>> ctx = CancellationContext()
            >>> ctx.cancel("User requested cancellation")
            >>> ctx.is_cancelled()
            True
            >>> ctx.reason
            'User requested cancellation'
        """
        with self._lock:
            self._cancelled = True
            self._reason = reason
        logger.debug(f"Operation cancelled: {reason}")

    def is_cancelled(self) -> bool:
        """
        Check if operation has been cancelled.

        Thread-safe check of the cancellation flag.

        Returns:
            True if operation has been cancelled, False otherwise

        Example:
            >>> ctx = CancellationContext()
            >>> ctx.is_cancelled()
            False
            >>> ctx.cancel()
            >>> ctx.is_cancelled()
            True
        """
        with self._lock:
            return self._cancelled

    def raise_if_cancelled(self):
        """
        Raise CancellationError if operation has been cancelled.

        This is a convenience method that can be called at strategic
        points during long-running operations to check for cancellation
        and exit early.

        Raises:
            CancellationError: If operation has been cancelled

        Example:
            >>> ctx = CancellationContext()
            >>> ctx.cancel()
            >>> ctx.raise_if_cancelled()
            Traceback (most recent call last):
                ...
            CancellationError: Operation cancelled
        """
        if self.is_cancelled():
            reason = self._reason or "Operation cancelled"
            logger.debug(f"Raising CancellationError: {reason}")
            raise CancellationError(message=reason)

    @property
    def reason(self) -> Optional[str]:
        """
        Get the reason for cancellation.

        Returns:
            Cancellation reason if cancelled, None otherwise

        Example:
            >>> ctx = CancellationContext()
            >>> ctx.reason
            None
            >>> ctx.cancel("Timeout")
            >>> ctx.reason
            'Timeout'
        """
        with self._lock:
            return self._reason

    def __enter__(self):
        """
        Enter the cancellation context.

        Returns:
            Self for use in with statements

        Example:
            >>> with CancellationContext() as ctx:
            ...     # Operation here
            ...     pass
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the cancellation context.

        Args:
            exc_type: Exception type if an exception was raised
            exc_val: Exception value if an exception was raised
            exc_tb: Exception traceback if an exception was raised

        Returns:
            False to propagate exceptions
        """
        # Clean up resources if needed
        return False


@contextmanager
def with_timeout(
    timeout_seconds: float, cancellation_context: Optional[CancellationContext] = None
):
    """
    Context manager that cancels operation after timeout.

    This context manager monitors the elapsed time and cancels the
    operation if it exceeds the specified timeout. The cancellation
    is communicated through the CancellationContext.

    Args:
        timeout_seconds: Maximum duration in seconds (must be positive)
        cancellation_context: Optional existing cancellation context
                             (creates new one if None)

    Yields:
        CancellationContext that will be cancelled on timeout

    Raises:
        ValueError: If timeout_seconds is not positive
        CancellationError: If operation times out

    Example:
        >>> with with_timeout(5.0) as ctx:
        ...     # Operation that completes within 5 seconds
        ...     while not ctx.is_cancelled():
        ...         # Do work
        ...         pass
    """
    if timeout_seconds <= 0:
        raise ValueError(f"timeout_seconds must be positive, got {timeout_seconds}")

    ctx = cancellation_context or CancellationContext()
    start_time = time.time()

    def timeout_monitor():
        """Monitor thread that cancels on timeout."""
        elapsed = time.time() - start_time
        if elapsed >= timeout_seconds and not ctx.is_cancelled():
            ctx.cancel(f"Operation timed out after {timeout_seconds:.1f} seconds")

    # Start timeout monitor thread
    monitor_thread = threading.Thread(target=timeout_monitor, daemon=True)
    monitor_thread.start()

    try:
        yield ctx
    finally:
        # Wait for monitor thread to complete
        monitor_thread.join(timeout=0.1)

        # Check if we timed out
        if ctx.is_cancelled() and ctx.reason and "timed out" in ctx.reason.lower():
            logger.warning(f"Operation timed out after {timeout_seconds:.1f} seconds")
            raise CancellationError(message=ctx.reason)


def check_cancellation(cancellation_context: Optional[CancellationContext]):
    """
    Check for cancellation and raise CancellationError if cancelled.

    This is a convenience function for checking cancellation at strategic
    points during long-running operations.

    Args:
        cancellation_context: Cancellation context to check (None is ignored)

    Raises:
        CancellationError: If context exists and is cancelled

    Example:
        >>> ctx = CancellationContext()
        >>> ctx.cancel("User interrupted")
        >>> check_cancellation(ctx)  # Raises CancellationError
    """
    if cancellation_context:
        cancellation_context.raise_if_cancelled()
