"""
Progress tracking module for Binary SBOM Generator.

This module provides progress bar functionality using tqdm for long-running operations,
with automatic TTY detection and configurable enable/disable logic.
"""

import sys
import threading
from typing import Dict, Any, Optional

try:
    from tqdm import tqdm  # noqa: F401
except ImportError:
    tqdm = None  # type: ignore[assignment]  # pragma: no cover

from .config import load_config, is_progress_enabled, get_min_file_size_mb


class ProgressTracker:
    """
    Progress tracker for managing progress bars during file processing.

    This class provides a thread-safe interface to tqdm progress bars,
    with automatic TTY detection and file size threshold checking.

    Attributes:
        file_size: Size of the file being processed in bytes.
        min_size: Minimum file size in bytes for showing progress.
        enabled: Whether progress tracking is enabled.
        force: Force override (True=force enable, False=force disable, None=auto).
        _current_bar: Current tqdm progress bar instance.
        _lock: Thread lock for progress updates.

    Example:
        >>> tracker = ProgressTracker(file_size=150*1024*1024, min_size=100*1024*1024)
        >>> if tracker.is_enabled():
        ...     tracker.start_operation("Parsing binary...")
        ...     tracker.update_progress(75)
        ...     tracker.finish_operation()
    """

    def __init__(
        self,
        file_size: int,
        min_size: Optional[int] = None,
        config: Optional[Dict[str, Any]] = None,
        force: Optional[bool] = None
    ):
        """
        Initialize the progress tracker.

        Args:
            file_size: Size of the file being processed in bytes.
            min_size: Minimum file size in bytes for showing progress.
                     If None, uses config value (default: 100MB).
            config: Optional configuration dictionary. If not provided, loads default config.
            force: Optional boolean to override all other settings.
                   True forces enable, False forces disable, None uses config settings.

        Example:
            >>> tracker = ProgressTracker(file_size=200*1024*1024)  # 200MB file
            >>> tracker.is_enabled()
            True  # If TTY and file >= 100MB threshold
        """
        self.file_size = file_size
        self.min_size = min_size or (get_min_file_size_mb(config) * 1024 * 1024)
        self.enabled = is_progress_enabled(config, force)
        self.force = force
        self._current_bar: Optional[tqdm] = None
        self._lock = threading.Lock()

        # Check if file size meets threshold
        if file_size < self.min_size:
            self.enabled = False

        # Check if tqdm is available
        if tqdm is None:
            self.enabled = False

    def is_enabled(self) -> bool:
        """
        Check if progress tracking is enabled.

        Returns:
            True if progress tracking is enabled and available, False otherwise.

        Example:
            >>> tracker = ProgressTracker(file_size=150*1024*1024)
            >>> tracker.is_enabled()
            True  # If conditions are met
        """
        return self.enabled

    def start_operation(
        self,
        operation: str,
        total: Optional[int] = None,
        unit: str = "B",
        unit_scale: bool = True
    ) -> None:
        """
        Start a new progress bar for an operation.

        Args:
            operation: Description of the operation being tracked.
            total: Total units for the progress bar. If None, uses file_size.
            unit: Unit of progress (default: "B" for bytes).
            unit_scale: Whether to scale units (e.g., KB, MB, GB).

        Example:
            >>> tracker = ProgressTracker(file_size=150*1024*1024)
            >>> tracker.start_operation("Parsing MachO binary...")
        """
        if not self.enabled:
            return

        with self._lock:
            # Close any existing bar
            if self._current_bar is not None:
                self._current_bar.close()

            # Create new progress bar
            # Use stderr for progress bar to avoid conflicts with verbose output on stdout
            total_units = total or self.file_size
            self._current_bar = tqdm(
                total=total_units,
                desc=operation,
                unit=unit,
                unit_scale=unit_scale,
                disable=not self.enabled,
                file=sys.stderr
            )

    def update_progress(self, n: int = 1) -> None:
        """
        Update the progress bar by n units.

        Thread-safe method to update progress. If progress tracking is disabled
        or no bar is active, this method does nothing.

        Args:
            n: Number of units to increment progress by (default: 1).

        Example:
            >>> tracker = ProgressTracker(file_size=150*1024*1024)
            >>> tracker.start_operation("Reading file...")
            >>> tracker.update_progress(1024)  # Added 1KB
        """
        if not self.enabled or self._current_bar is None:
            return

        with self._lock:
            if self._current_bar is not None:
                self._current_bar.update(n)

    def set_progress(self, n: int) -> None:
        """
        Set the progress to a specific value.

        Thread-safe method to set progress to a specific value rather than
        incrementing. Useful when you know the absolute progress position.

        Args:
            n: Absolute value to set progress to.

        Example:
            >>> tracker = ProgressTracker(file_size=150*1024*1024)
            >>> tracker.start_operation("Processing...")
            >>> tracker.set_progress(50*1024*1024)  # Set to 50MB
        """
        if not self.enabled or self._current_bar is None:
            return

        with self._lock:
            if self._current_bar is not None:
                # Calculate the difference to update
                current = self._current_bar.n
                diff = n - current
                if diff > 0:
                    self._current_bar.update(diff)

    def finish_operation(self) -> None:
        """
        Finish the current progress bar operation.

        Closes the progress bar and cleans up resources. Thread-safe.

        Example:
            >>> tracker = ProgressTracker(file_size=150*1024*1024)
            >>> tracker.start_operation("Parsing...")
            >>> # ... do work ...
            >>> tracker.finish_operation()
        """
        if not self.enabled:
            return

        with self._lock:
            if self._current_bar is not None:
                self._current_bar.close()
                self._current_bar = None

    def set_description(self, description: str) -> None:
        """
        Update the description of the current progress bar.

        Thread-safe method to change the progress bar description
        without closing and reopening it.

        Args:
            description: New description for the progress bar.

        Example:
            >>> tracker = ProgressTracker(file_size=150*1024*1024)
            >>> tracker.start_operation("Reading...")
            >>> tracker.set_description("Parsing...")
        """
        if not self.enabled or self._current_bar is None:
            return

        with self._lock:
            if self._current_bar is not None:
                self._current_bar.set_description(description)

    def __enter__(self):
        """
        Context manager entry.

        Example:
            >>> with ProgressTracker(file_size=150*1024*1024) as tracker:
            ...     tracker.start_operation("Processing...")
            ...     # ... do work ...
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit - ensures progress bar is closed.

        Example:
            >>> with ProgressTracker(file_size=150*1024*1024) as tracker:
            ...     tracker.start_operation("Processing...")
            ...     # Progress bar automatically closed on exit
        """
        self.finish_operation()
        return False

    def __del__(self):
        """
        Destructor - ensures progress bar is closed.

        Provides cleanup in case finish_operation() was not called.
        """
        if self._current_bar is not None:
            try:
                self._current_bar.close()
            except Exception:  # pragma: no cover
                # Ignore errors during cleanup
                pass


def should_show_progress(
    file_size: int,
    config: Optional[Dict[str, Any]] = None,
    force: Optional[bool] = None
) -> bool:
    """
    Determine if progress should be shown for a given file size.

    Convenience function that combines file size checking with TTY detection
    and configuration settings.

    Args:
        file_size: Size of the file in bytes.
        config: Optional configuration dictionary.
        force: Optional boolean to override all settings.

    Returns:
        True if progress should be shown, False otherwise.

    Example:
        >>> should_show_progress(150*1024*1024)  # 150MB file
        True  # If TTY and threshold met
        >>> should_show_progress(50*1024*1024)  # 50MB file
        False  # Below default 100MB threshold
    """
    tracker = ProgressTracker(file_size=file_size, config=config, force=force)
    return tracker.is_enabled()


__all__ = [
    'ProgressTracker',
    'should_show_progress',
]
