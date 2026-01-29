"""
Progress tracker service for binary analysis progress tracking.

This module provides the ProgressTracker class that manages progress tracking
and Rich terminal display for the 5-stage binary analysis pipeline.

Communication is via direct function calls (not WebSocket/SSE) since this is
a single-process CLI tool using synchronous execution.
"""

import dataclasses
import threading
import time
from datetime import datetime
from typing import TYPE_CHECKING, Any, Callable, Optional, Protocol

# Try to import Rich library for terminal UI
# If unavailable, fall back to simple text output
try:
    from rich.console import Console
    from rich.live import Live
    from rich.panel import Panel
    from rich.progress import (
        BarColumn,
        Progress,
        SpinnerColumn,
        TaskProgressColumn,
        TextColumn,
        TimeElapsedColumn,
        TimeRemainingColumn,
        TransferSpeedColumn,
    )
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    # Rich not available - will use text-only fallback
    RICH_AVAILABLE = False
    if TYPE_CHECKING:
        from rich.console import Console
        from rich.live import Live
        from rich.panel import Panel
    else:
        Console = None  # type: ignore
        Live = None  # type: ignore
        Panel = None  # type: ignore

import click

from .config import ProgressConfig
from .eta_estimator import ETAEstimator
from .progress_state import AnalysisMetrics, ProgressState, StageState


class ProgressCallback(Protocol):
    """
    Protocol defining the interface for progress callbacks.

    The analyzer functions call this callback to report progress updates.
    """

    def __call__(
        self,
        stage_id: int,
        state: StageState,
        progress: Optional[int] = None,
        processed_items: Optional[int] = None,
        total_items: Optional[int] = None,
        result: Optional[str] = None,
        error_message: Optional[str] = None,
    ) -> None:
        """
        Update progress for a specific stage.

        Args:
            stage_id: Stage identifier (1-5)
            state: New stage state (PENDING/ACTIVE/COMPLETE/FAILED)
            progress: Progress percentage (0-100), None for indeterminate
            processed_items: Number of items processed (e.g., sections analyzed)
            total_items: Total items to process (e.g., total sections)
            result: Result summary (e.g., "Found 24 sections")
            error_message: Error message if stage failed
        """
        ...


class ProgressTracker:
    """
    Tracks and displays analysis progress using Rich library.

    This class manages the communication between the analysis pipeline
    and the terminal display. It receives progress updates via callbacks,
    maintains thread-safe state, and updates the Rich display at configurable rate.

    Attributes:
        filename: Name of the file being analyzed
        file_size_bytes: Size of the file in bytes
        verbose: Whether to display progress (False = silent mode)
        config: ProgressConfig object with display settings
    """

    def __init__(
        self,
        filename: str,
        file_size_bytes: int,
        verbose: bool = True,
        config: Optional[ProgressConfig] = None,
        eta_estimator: Optional[ETAEstimator] = None,
    ):
        """
        Initialize ProgressTracker.

        Args:
            filename: Name of the file being analyzed
            file_size_bytes: Size of the file in bytes
            verbose: Whether to display progress (False for silent mode)
            config: ProgressConfig object (uses defaults if None)
            eta_estimator: Optional ETA estimator for enhanced time predictions
        """
        self.filename = filename
        self.file_size_bytes = file_size_bytes
        self.verbose = verbose
        self.config = config or ProgressConfig()
        self._eta_estimator = eta_estimator

        # Initialize progress state with ETA estimator
        self._state = ProgressState.initial(filename, file_size_bytes)
        if self._eta_estimator is not None:
            self._state = dataclasses.replace(
                self._state, eta_estimator=self._eta_estimator
            )

        # Thread safety
        self._lock = threading.Lock()
        self._last_update_time = 0.0
        self._min_update_interval = 1.0 / self.config.refresh_per_second

        # Rich components (initialized in start())
        self._rich_progress: Optional[Any] = None
        self._rich_live: Optional[Any] = None
        self._console: Optional[Any] = None

        # Task IDs for Rich progress (populated in start())
        self._task_ids: dict[int, Any] = {}

        # Track if Rich is available or if text mode is forced
        self._rich_available = RICH_AVAILABLE and not self.config.force_text_mode

        # Track if we've shown the Rich warning
        self._rich_warning_shown = False

    def start(self) -> None:
        """
        Initialize Rich display and start tracking.

        Creates the Rich Progress and Live objects, starts the Live display,
        and initializes all stage progress bars.

        If Rich library is unavailable or text mode is forced, shows a warning
        and uses text-only mode.
        """
        if not self.verbose:
            return

        # Check if Rich is available
        if not self._rich_available:
            if not self._rich_warning_shown:
                if self.config.force_text_mode:
                    click.echo(
                        "Text-only mode enabled via configuration.",
                        err=True,
                    )
                elif not RICH_AVAILABLE:
                    click.echo(
                        "Warning: Rich library not found. Using text-only progress mode.\n"
                        "  For animated progress, install: pip install rich>=13.0.0",
                        err=True,
                    )
                self._rich_warning_shown = True
            return

        # Create Rich Progress with columns
        self._console = Console()
        self._rich_progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            TransferSpeedColumn(),
            console=self._console,
            refresh_per_second=self.config.refresh_per_second,
        )

        # Create Live display for dashboard
        self._rich_live = Live(
            self._render_dashboard(),
            console=self._console,
            refresh_per_second=self.config.refresh_per_second,
        )

        # Start the live display
        if self._rich_live:
            self._rich_live.start()

        # Initialize progress bars for each stage
        if self._rich_progress:
            for stage in self._state.stages:
                # Use None for stages with indeterminate progress (Stage 1)
                total = 100 if stage.stage_id != 1 else None
                task_id = self._rich_progress.add_task(
                    f"[{stage.color}]{stage.name}[/]",
                    total=total,
                )
                self._task_ids[stage.stage_id] = task_id

    def update(
        self,
        stage_id: int,
        state: StageState,
        progress: Optional[int] = None,
        processed_items: Optional[int] = None,
        total_items: Optional[int] = None,
        result: Optional[str] = None,
        error_message: Optional[str] = None,
    ) -> None:
        """
        Update progress for a specific stage.

        This method is called by the analyzer functions via the callback.
        It updates internal state and triggers a UI refresh if throttling allows.

        Thread-safe: Can be called from multiple threads.

        Args:
            stage_id: Stage identifier (1-5)
            state: New stage state
            progress: Progress percentage (0-100)
            processed_items: Number of items processed
            total_items: Total items to process
            result: Result summary
            error_message: Error message if stage failed
        """
        with self._lock:
            # Always update internal state (immutable - creates new instance)
            # Even when verbose=False, we maintain state for testing/monitoring
            self._state = self._state.with_stage_update(
                stage_id=stage_id,
                state=state,
                progress=progress,
                processed_items=processed_items,
                total_items=total_items,
                result=result,
                error_message=error_message,
            )

            # Skip UI updates if not verbose
            if not self.verbose:
                return

            # Text-only fallback mode
            if not self._rich_available:
                self._update_text_display(state, stage_id, progress)
                return

            # Throttle UI updates to prevent flicker (max refresh_per_second)
            current_time = time.time()
            time_since_last_update = current_time - self._last_update_time

            # Stage transitions always trigger immediate update (bypass throttling)
            if state in (StageState.ACTIVE, StageState.COMPLETE, StageState.FAILED):
                should_update = True  # Instant visual feedback
            else:
                # Progress updates are throttled to avoid overwhelming terminal
                should_update = time_since_last_update >= self._min_update_interval

            if should_update:
                self._update_rich_display()
                self._last_update_time = current_time

    def complete(self) -> None:
        """
        Mark analysis as complete and stop tracking.

        Stops the Rich Live display and marks all stages as complete.
        If Rich library is unavailable, shows completion message in text mode.
        """
        with self._lock:
            # Always update state (even when verbose=False)
            self._state = self._state.complete()

        # Stop the live display if verbose
        if not self.verbose:
            return

        # Stop Rich display if available
        if self._rich_available and self._rich_live:
            self._rich_live.stop()
            self._rich_live = None
        elif not self._rich_available and self.verbose:
            # Text-only fallback: show final message
            click.echo("\n✓ Analysis complete")

    def get_callback(self) -> ProgressCallback:
        """
        Get a callback function for progress updates.

        Returns a callable that can be passed to analyzer functions.

        Returns:
            ProgressCallback callable
        """
        return self.update

    def get_state(self) -> ProgressState:
        """
        Get current progress state.

        Thread-safe: Returns immutable snapshot of current state.

        Returns:
            Current ProgressState
        """
        with self._lock:
            return self._state

    def _update_rich_display(self) -> None:
        """Update the Rich display with current state."""
        if self._rich_live:
            self._rich_live.update(self._render_dashboard())

        # Update progress bars
        if self._rich_progress:
            for stage in self._state.stages:
                task_id = self._task_ids.get(stage.stage_id)
                if task_id is None:
                    continue

                # Update progress bar
                if stage.is_complete:
                    self._rich_progress.update(task_id, completed=100)
                elif stage.is_active and stage.progress is not None:
                    self._rich_progress.update(task_id, completed=stage.progress)
                elif stage.is_failed:
                    # Mark as failed with no progress
                    self._rich_progress.update(task_id, completed=0)

    def _update_text_display(
        self,
        state: StageState,
        stage_id: int,
        progress: Optional[int] = None,
    ) -> None:
        """
        Update text-only display when Rich library is unavailable.

        Shows simple progress messages for stage transitions.

        Args:
            state: Current stage state
            stage_id: Stage identifier (1-5)
            progress: Progress percentage (optional)
        """
        # Get the stage
        stage = self._state.stages[stage_id - 1]

        # Only show messages on state transitions (not for every progress update)
        if state == StageState.ACTIVE:
            click.echo(f"→ {stage.name}...")
        elif state == StageState.COMPLETE:
            result_text = stage.result or "Complete"
            click.echo(f"✓ {stage.name}: {result_text}")
        elif state == StageState.FAILED:
            error_text = stage.error_message or "Failed"
            click.echo(f"✗ {stage.name}: {error_text}", err=True)

    def _render_dashboard(self) -> Panel:
        """
        Render the dashboard layout for Rich display.

        Respects configuration settings for:
        - Which metrics to display
        - Dashboard mode (full, compact, minimal)

        Returns:
            Rich Panel with dashboard content
        """
        # Build metrics table based on config
        metrics_table = Table(show_header=False, show_edge=False, padding=(0, 2))
        metrics_table.add_column("Metric", style="cyan")
        metrics_table.add_column("Value", style="white")

        # Add metrics rows based on config
        if self.config.show_file_metric:
            metrics_table.add_row(
                "File", f"{self._state.filename} ({self._state.metrics.file_size_human})"
            )
        if self.config.show_elapsed_metric:
            metrics_table.add_row(
                "Elapsed", self._state.metrics.time_elapsed_human
            )
        if self.config.show_speed_metric:
            metrics_table.add_row(
                "Speed", self._state.metrics.processing_rate_human
            )
        if self.config.show_eta_metric:
            metrics_table.add_row(
                "ETA", self._state.metrics.eta_human
            )

        # Build stages table
        stages_table = Table(show_header=True, box=None)
        stages_table.add_column("Stage", style="white", width=25)
        stages_table.add_column("Status", style="white", width=10)

        # Add Progress and Details columns only for full mode
        if self.config.dashboard_mode == "full":
            stages_table.add_column("Progress", style="white", width=15)
            stages_table.add_column("Details", style="white", width=30)
        elif self.config.dashboard_mode == "compact":
            stages_table.add_column("Progress", style="white", width=15)

        # Add rows for each stage
        for stage in self._state.stages:
            # Status symbol
            if self.config.enable_unicode:
                status_symbol = stage.visual_symbol
            else:
                # ASCII fallback
                if stage.is_complete:
                    status_symbol = "[green]✓[/]"
                elif stage.is_active:
                    status_symbol = "[yellow]>[/]"
                elif stage.is_failed:
                    status_symbol = "[red]X[/]"
                else:
                    status_symbol = " "

            # Progress bar
            if stage.is_complete:
                progress_str = "[green]100%[/]" if self.config.enable_colors else "100%"
            elif stage.is_active:
                if stage.progress is not None:
                    progress_str = f"[yellow]{stage.progress}%[/]" if self.config.enable_colors else f"{stage.progress}%"
                else:
                    progress_str = "[yellow]⠳[/]" if self.config.enable_unicode else "..."
            elif stage.is_failed:
                progress_str = "[red]Failed[/]" if self.config.enable_colors else "Failed"
            else:
                progress_str = "☐"

            # Details (only in full mode)
            if self.config.dashboard_mode == "full":
                if stage.is_failed and stage.error_message:
                    details = f"[red]{stage.error_message}[/]" if self.config.enable_colors else stage.error_message
                elif stage.result:
                    details = f"[green]{stage.result}[/]" if self.config.enable_colors else stage.result
                elif stage.processed_items and stage.total_items:
                    details = f"{stage.processed_items}/{stage.total_items} items"
                else:
                    details = stage.description

                stages_table.add_row(
                    f"[{stage.color}]{stage.name}[/]" if self.config.enable_colors else stage.name,
                    status_symbol,
                    progress_str,
                    details,
                )
            elif self.config.dashboard_mode == "compact":
                stages_table.add_row(
                    f"[{stage.color}]{stage.name}[/]" if self.config.enable_colors else stage.name,
                    status_symbol,
                    progress_str,
                )
            else:  # minimal mode
                stages_table.add_row(
                    f"[{stage.color}]{stage.name}[/]" if self.config.enable_colors else stage.name,
                    status_symbol,
                )

        # Combine into dashboard based on mode
        if self.config.dashboard_mode == "full":
            dashboard = Table.grid(padding=1)
            dashboard.add_row(
                Panel(
                    metrics_table,
                    title="[bold cyan]Analysis Metrics[/]",
                    border_style="cyan",
                )
            )
            dashboard.add_row(
                Panel(
                    stages_table,
                    title=f"[bold cyan]Analysis Progress[/] - {self._state.overall_progress:.1f}%",
                    border_style="cyan",
                )
            )
        elif self.config.dashboard_mode == "compact":
            dashboard = Table.grid(padding=1)
            dashboard.add_row(
                Panel(
                    stages_table,
                    title=f"[bold cyan]Analysis Progress[/] - {self._state.overall_progress:.1f}%",
                    border_style="cyan",
                )
            )
        else:  # minimal mode
            dashboard = Table.grid(padding=0)
            dashboard.add_row(stages_table)

        # Only wrap in Panel for full and compact modes
        if self.config.dashboard_mode in ["full", "compact"]:
            return Panel(dashboard, title="[bold]Binary Analysis Progress[/]", border_style="bright_blue")
        else:
            # Minimal mode returns just the stages table
            return Panel(dashboard, border_style="bright_blue")


class MultiFileProgressTracker:
    """
    Tracks and displays progress for parallel processing of multiple files.

    This class manages multiple ProgressTracker instances and provides
    aggregate progress tracking across all files being processed in parallel.

    Attributes:
        file_count: Total number of files to process
        verbose: Whether to display progress
        config: ProgressConfig object with display settings
    """

    def __init__(
        self,
        file_count: int,
        verbose: bool = True,
        config: Optional[ProgressConfig] = None,
    ):
        """
        Initialize MultiFileProgressTracker.

        Args:
            file_count: Total number of files to process
            verbose: Whether to display progress (False for silent mode)
            config: ProgressConfig object (uses defaults if None)
        """
        self.file_count = file_count
        self.verbose = verbose
        self.config = config or ProgressConfig()

        # Thread safety
        self._lock = threading.Lock()
        self._completed_files: Dict[str, ProgressState] = {}
        self._failed_files: Dict[str, str] = {}  # file_path -> error_message
        self._active_files: Dict[str, ProgressState] = {}
        self._last_update_time = 0.0
        self._min_update_interval = 1.0 / self.config.refresh_per_second

        # Rich components (initialized in start())
        self._rich_progress: Optional[Any] = None
        self._rich_live: Optional[Any] = None
        self._console: Optional[Any] = None
        self._overall_task_id: Optional[Any] = None

        # Track if Rich is available
        self._rich_available = RICH_AVAILABLE and not self.config.force_text_mode
        self._rich_warning_shown = False

        # Track start time
        self._start_time: Optional[float] = None

    def start(self) -> None:
        """Initialize Rich display and start tracking."""
        if not self.verbose:
            return

        self._start_time = time.time()

        # Check if Rich is available
        if not self._rich_available:
            if not self._rich_warning_shown:
                if self.config.force_text_mode:
                    click.echo(
                        "Text-only mode enabled via configuration.",
                        err=True,
                    )
                elif not RICH_AVAILABLE:
                    click.echo(
                        "Warning: Rich library not found. Using text-only progress mode.\n"
                        "  For animated progress, install: pip install rich>=13.0.0",
                        err=True,
                    )
                self._rich_warning_shown = True
            return

        # Create Rich Progress with columns
        self._console = Console()
        self._rich_progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=self._console,
            refresh_per_second=self.config.refresh_per_second,
        )

        # Create Live display for dashboard
        self._rich_live = Live(
            self._render_dashboard(),
            console=self._console,
            refresh_per_second=self.config.refresh_per_second,
        )

        # Start the live display
        if self._rich_live:
            self._rich_live.start()

        # Initialize overall progress bar
        if self._rich_progress:
            self._overall_task_id = self._rich_progress.add_task(
                f"[cyan]Processing {self.file_count} files[/]",
                total=self.file_count,
            )

    def update_file_progress(
        self,
        file_path: str,
        state: ProgressState,
    ) -> None:
        """
        Update progress for a specific file.

        Thread-safe: Can be called from multiple worker processes.

        Args:
            file_path: Path to the file being processed
            state: Current progress state for this file
        """
        with self._lock:
            # Update tracking dictionaries
            if state.is_complete:
                self._completed_files[file_path] = state
                if file_path in self._active_files:
                    del self._active_files[file_path]
            elif state.is_failed:
                self._failed_files[file_path] = state.failed_stage.error_message if state.failed_stage else "Unknown error"
                if file_path in self._active_files:
                    del self._active_files[file_path]
            else:
                self._active_files[file_path] = state

            # Skip UI updates if not verbose
            if not self.verbose:
                return

            # Text-only fallback mode
            if not self._rich_available:
                self._update_text_display(file_path, state)
                return

            # Throttle UI updates
            current_time = time.time()
            time_since_last_update = current_time - self._last_update_time

            if time_since_last_update >= self._min_update_interval:
                self._update_rich_display()
                self._last_update_time = current_time

    def complete(self) -> None:
        """Mark all processing as complete and stop tracking."""
        with self._lock:
            # Stop Rich display
            if not self.verbose:
                return

            if self._rich_available and self._rich_live:
                self._rich_live.stop()
                self._rich_live = None
            elif not self._rich_available and self.verbose:
                # Text-only fallback: show final message
                completed = len(self._completed_files)
                failed = len(self._failed_files)
                click.echo(
                    f"\n✓ Processing complete: {completed} successful, {failed} failed"
                )

    def _update_rich_display(self) -> None:
        """Update the Rich display with current state."""
        if not self._rich_progress or not self._rich_live:
            return

        # Update overall progress bar
        completed_count = len(self._completed_files)
        if self._overall_task_id is not None:
            self._rich_progress.update(
                self._overall_task_id,
                completed=completed_count,
            )

        # Update dashboard
        self._rich_live.update(self._render_dashboard())

    def _update_text_display(
        self,
        file_path: str,
        state: ProgressState,
    ) -> None:
        """
        Update text-only display when Rich library is unavailable.

        Shows simple progress messages for file completions.

        Args:
            file_path: Path to the file
            state: Current progress state
        """
        # Show message on completion
        if state.is_complete and file_path not in self._completed_files:
            # Shorten filename for display
            filename = file_path if len(file_path) <= 60 else "..." + file_path[-57:]
            click.echo(f"✓ Completed: {filename}")

    def _render_dashboard(self) -> Panel:
        """
        Render the dashboard layout for Rich display.

        Returns:
            Rich Panel with dashboard content
        """
        completed_count = len(self._completed_files)
        failed_count = len(self._failed_files)
        active_count = len(self._active_files)
        overall_progress = (completed_count / self.file_count * 100) if self.file_count > 0 else 0

        # Build summary table
        summary_table = Table(show_header=False, show_edge=False, padding=(0, 2))
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="white")

        # Calculate elapsed time
        elapsed_time = None
        if self._start_time:
            elapsed_time = time.time() - self._start_time

        summary_table.add_row("Total Files", str(self.file_count))
        summary_table.add_row("Completed", str(completed_count))
        summary_table.add_row("Active", str(active_count))
        summary_table.add_row("Failed", str(failed_count))

        if elapsed_time:
            elapsed_str = f"{elapsed_time:.1f}s"
            summary_table.add_row("Elapsed", elapsed_str)

        # Build active files table
        active_table = Table(show_header=True, box=None)
        active_table.add_column("File", style="white", width=50)
        active_table.add_column("Progress", style="yellow", width=15)
        active_table.add_column("Stage", style="cyan", width=25)

        # Add rows for active files
        for file_path, state in self._active_files.items():
            # Shorten filename for display
            filename = file_path if len(file_path) <= 50 else "..." + file_path[-47:]
            progress_str = f"{state.overall_progress:.1f}%"

            # Get current stage
            if state.current_stage:
                stage_str = state.current_stage.name
            else:
                stage_str = "Initializing"

            active_table.add_row(filename, progress_str, stage_str)

        # Combine into dashboard
        dashboard = Table.grid(padding=1)
        dashboard.add_row(
            Panel(
                summary_table,
                title=f"[bold cyan]Overall Progress[/] - {overall_progress:.1f}%",
                border_style="cyan",
            )
        )

        if active_count > 0:
            dashboard.add_row(
                Panel(
                    active_table,
                    title=f"[bold cyan]Active Files[/] ({active_count})",
                    border_style="yellow",
                )
            )

        return Panel(dashboard, title="[bold]Multi-File Processing Progress[/]", border_style="bright_blue")

    @property
    def completed_count(self) -> int:
        """Get number of completed files."""
        with self._lock:
            return len(self._completed_files)

    @property
    def failed_count(self) -> int:
        """Get number of failed files."""
        with self._lock:
            return len(self._failed_files)

    @property
    def active_count(self) -> int:
        """Get number of active files."""
        with self._lock:
            return len(self._active_files)


def create_progress_tracker(
    filename: str,
    file_size_bytes: int,
    verbose: bool = True,
    config: Optional[ProgressConfig] = None,
    refresh_per_second: Optional[int] = None,
    eta_estimator: Optional[ETAEstimator] = None,
) -> ProgressTracker:
    """
    Factory function to create a ProgressTracker.

    Args:
        filename: Name of the file being analyzed
        file_size_bytes: Size of the file in bytes
        verbose: Whether to display progress
        config: ProgressConfig object (uses defaults if None)
        refresh_per_second: Refresh rate for progress updates (1-60 fps).
                           If provided, overrides config.refresh_per_second
        eta_estimator: Optional ETA estimator for enhanced time predictions

    Returns:
        ProgressTracker instance
    """
    # If refresh_per_second provided, override config
    if config is None:
        config = ProgressConfig()
    if refresh_per_second is not None:
        # Create a new config with overridden refresh rate
        config = dataclasses.replace(config, refresh_per_second=refresh_per_second)

    return ProgressTracker(
        filename=filename,
        file_size_bytes=file_size_bytes,
        verbose=verbose,
        config=config,
        eta_estimator=eta_estimator,
    )


def create_multi_file_progress_tracker(
    file_count: int,
    verbose: bool = True,
    config: Optional[ProgressConfig] = None,
) -> MultiFileProgressTracker:
    """
    Factory function to create a MultiFileProgressTracker.

    Args:
        file_count: Total number of files to process
        verbose: Whether to display progress
        config: ProgressConfig object (uses defaults if None)

    Returns:
        MultiFileProgressTracker instance
    """
    return MultiFileProgressTracker(
        file_count=file_count,
        verbose=verbose,
        config=config,
    )
