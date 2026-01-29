"""
Progress state data structures for binary analysis progress tracking.

This module defines immutable data structures for tracking progress through the
5-stage binary analysis pipeline (File Parsing → Metadata Extraction → Section
Analysis → Dependency Resolution → SPDX Generation).

All data structures use frozen dataclasses for immutability and thread safety.
"""

import dataclasses
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from .eta_estimator import ETAEstimator

# Stage weight constants for overall progress calculation
# Weights based on typical stage durations for large binary files (10MB+)
STAGE_WEIGHTS = {
    1: 0.70,  # File Parsing: 70% (LIEF parsing is slowest)
    2: 0.10,  # Metadata Extraction: 10% (format detection, entrypoint)
    3: 0.10,  # Section Analysis: 10% (can be many sections)
    4: 0.05,  # Dependency Resolution: 5% (typically fewer than sections)
    5: 0.05,  # SPDX Generation: 5% (document creation)
}


class StageState(Enum):
    """Represents the current state of an analysis stage."""

    PENDING = "pending"  # Stage not started
    ACTIVE = "active"  # Stage currently running
    COMPLETE = "complete"  # Stage finished successfully
    FAILED = "failed"  # Stage encountered error

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class StageProgress:
    """
    Tracks progress for a single analysis stage.

    Attributes:
        stage_id: Unique stage identifier (1-5)
        name: Human-readable stage name
        state: Current stage state (pending/active/complete/failed)
        progress: Progress percentage (0-100), None for indeterminate
        current_item: Current item being processed (e.g., "section 12 of 24")
        total_items: Total items to process (e.g., 24 sections)
        processed_items: Number of items processed (e.g., 12 sections)
        result: Result summary after completion (e.g., "Found 24 sections")
        error_message: Error message if stage failed
        started_at: Timestamp when stage started
        completed_at: Timestamp when stage completed (None if not complete)
        color: Rich console color for this stage
        description: Brief description of stage activities
    """

    stage_id: int
    name: str
    state: StageState
    progress: Optional[int] = None  # None = indeterminate progress
    current_item: Optional[str] = None
    total_items: Optional[int] = None
    processed_items: Optional[int] = None
    result: Optional[str] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    color: str = "white"
    description: str = ""

    def __post_init__(self) -> None:
        """Validate progress percentage."""
        if self.progress is not None and not 0 <= self.progress <= 100:
            raise ValueError(f"Progress must be 0-100, got {self.progress}")

    @property
    def is_active(self) -> bool:
        """Check if stage is currently active."""
        return self.state == StageState.ACTIVE

    @property
    def is_complete(self) -> bool:
        """Check if stage has completed successfully."""
        return self.state == StageState.COMPLETE

    @property
    def is_failed(self) -> bool:
        """Check if stage has failed."""
        return self.state == StageState.FAILED

    @property
    def duration_seconds(self) -> Optional[float]:
        """Calculate stage duration in seconds."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

    @property
    def visual_symbol(self) -> str:
        """Get visual symbol for current state."""
        symbols = {
            StageState.PENDING: "☐",
            StageState.ACTIVE: "⠳",
            StageState.COMPLETE: "✓",
            StageState.FAILED: "✗",
        }
        return symbols.get(self.state, "?")

    def with_progress(
        self,
        progress: Optional[int] = None,
        processed_items: Optional[int] = None,
        current_item: Optional[str] = None,
    ) -> "StageProgress":
        """
        Create updated StageProgress with new progress values.

        Returns new immutable instance (functional update pattern).

        Args:
            progress: New progress percentage (0-100)
            processed_items: New number of items processed
            current_item: New current item description

        Returns:
            New StageProgress instance with updated values
        """
        return dataclasses.replace(
            self,
            progress=progress if progress is not None else self.progress,
            processed_items=processed_items if processed_items is not None else self.processed_items,
            current_item=current_item if current_item is not None else self.current_item,
        )

    def start(self) -> "StageProgress":
        """Mark stage as started (ACTIVE)."""
        return dataclasses.replace(
            self, state=StageState.ACTIVE, started_at=datetime.now()
        )

    def complete(self, result: Optional[str] = None) -> "StageProgress":
        """Mark stage as completed."""
        return dataclasses.replace(
            self,
            state=StageState.COMPLETE,
            progress=100,
            completed_at=datetime.now(),
            result=result,
        )

    def fail(self, error_message: str) -> "StageProgress":
        """Mark stage as failed."""
        return dataclasses.replace(
            self,
            state=StageState.FAILED,
            completed_at=datetime.now(),
            error_message=error_message,
        )


@dataclass(frozen=True)
class AnalysisMetrics:
    """
    Real-time metrics during binary analysis.

    All metrics are calculated and updated periodically (throttled to ~5-10Hz).

    Attributes:
        file_size_bytes: Input file size in bytes
        bytes_processed: Number of bytes processed so far
        processing_rate_bytes_per_sec: Current processing speed (bytes/sec)
        time_elapsed_seconds: Time since analysis started (seconds)
        estimated_time_remaining_seconds: Estimated time to completion (seconds)
        stage_specific_metrics: Dynamic metrics for current stage (e.g., section count)
    """

    file_size_bytes: int
    bytes_processed: int
    processing_rate_bytes_per_sec: float
    time_elapsed_seconds: float
    estimated_time_remaining_seconds: Optional[float]
    stage_specific_metrics: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate metric values."""
        if self.file_size_bytes < 0:
            raise ValueError("file_size_bytes must be >= 0")
        if self.bytes_processed < 0:
            raise ValueError("bytes_processed must be >= 0")
        if self.bytes_processed > self.file_size_bytes:
            raise ValueError("bytes_processed cannot exceed file_size_bytes")

    @property
    def file_size_mb(self) -> float:
        """File size in megabytes."""
        return self.file_size_bytes / (1024 * 1024)

    @property
    def file_size_human(self) -> str:
        """Human-readable file size (auto-scaled)."""
        return self._format_bytes(self.file_size_bytes)

    @property
    def processing_rate_mb_per_sec(self) -> float:
        """Processing rate in MB/sec."""
        return self.processing_rate_bytes_per_sec / (1024 * 1024)

    @property
    def processing_rate_human(self) -> str:
        """Human-readable processing rate."""
        return f"{self.processing_rate_mb_per_sec:.1f} MB/s"

    @property
    def time_elapsed_human(self) -> str:
        """Human-readable elapsed time (HH:MM:SS)."""
        return self._format_seconds(self.time_elapsed_seconds)

    @property
    def eta_human(self) -> str:
        """Human-readable ETA (HH:MM:SS or 'Calculating...')."""
        if self.estimated_time_remaining_seconds is None:
            return "Calculating..."
        return f"~{self._format_seconds(self.estimated_time_remaining_seconds)}"

    @property
    def progress_percentage(self) -> float:
        """Overall progress percentage (0-100)."""
        if self.file_size_bytes == 0:
            return 0.0
        return (self.bytes_processed / self.file_size_bytes) * 100

    @staticmethod
    def _format_bytes(bytes_count: int) -> str:
        """Format bytes to human-readable string (KB, MB, GB)."""
        for unit in ["B", "KB", "MB", "GB"]:
            if bytes_count < 1024.0:
                return f"{bytes_count:.1f} {unit}"
            bytes_count /= 1024.0
        return f"{bytes_count:.1f} TB"

    @staticmethod
    def _format_seconds(seconds: float) -> str:
        """Format seconds to HH:MM:SS string."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary for JSON serialization."""
        return {
            "file_size_bytes": self.file_size_bytes,
            "file_size_mb": round(self.file_size_mb, 2),
            "file_size_human": self.file_size_human,
            "bytes_processed": self.bytes_processed,
            "processing_rate_bytes_per_sec": round(self.processing_rate_bytes_per_sec, 2),
            "processing_rate_mb_per_sec": round(self.processing_rate_mb_per_sec, 2),
            "processing_rate_human": self.processing_rate_human,
            "time_elapsed_seconds": round(self.time_elapsed_seconds, 2),
            "time_elapsed_human": self.time_elapsed_human,
            "estimated_time_remaining_seconds": (
                round(self.estimated_time_remaining_seconds, 2)
                if self.estimated_time_remaining_seconds is not None
                else None
            ),
            "eta_human": self.eta_human,
            "progress_percentage": round(self.progress_percentage, 2),
            "stage_specific_metrics": self.stage_specific_metrics,
        }


@dataclass(frozen=True)
class ProgressState:
    """
    Overall progress state for binary analysis.

    This is the main state container that tracks all 5 stages and metrics.
    It is immutable - updates create new instances to prevent race conditions.

    Attributes:
        filename: Name of the file being analyzed
        stages: Tuple of 5 StageProgress objects
        metrics: AnalysisMetrics object with real-time metrics
        current_stage_index: Index of currently active stage (0-4)
        overall_progress: Overall progress percentage (0.0-100.0)
        is_complete: Whether analysis is complete
        is_failed: Whether analysis has failed
        started_at: Timestamp when analysis started
        completed_at: Timestamp when analysis completed (None if not complete)
        eta_estimator: Optional ETA estimator for enhanced time predictions
    """

    filename: str
    stages: Tuple[StageProgress, ...]  # Fixed-length tuple of 5 stages
    metrics: AnalysisMetrics
    current_stage_index: int
    overall_progress: float
    is_complete: bool
    is_failed: bool
    started_at: datetime
    completed_at: Optional[datetime] = None
    eta_estimator: Optional["ETAEstimator"] = None

    def __post_init__(self) -> None:
        """Validate progress state."""
        if len(self.stages) != 5:
            raise ValueError("stages must contain exactly 5 stages")
        if not 0 <= self.current_stage_index <= 4:
            raise ValueError("current_stage_index must be 0-4")
        if not 0.0 <= self.overall_progress <= 100.0:
            raise ValueError("overall_progress must be 0.0-100.0")

    @property
    def current_stage(self) -> Optional[StageProgress]:
        """Get the currently active stage."""
        if 0 <= self.current_stage_index < len(self.stages):
            return self.stages[self.current_stage_index]
        return None

    @property
    def completed_stages(self) -> Tuple[StageProgress, ...]:
        """Get all completed stages."""
        return tuple(s for s in self.stages if s.is_complete)

    @property
    def failed_stage(self) -> Optional[StageProgress]:
        """Get the failed stage if any."""
        for stage in self.stages:
            if stage.is_failed:
                return stage
        return None

    @property
    def duration_seconds(self) -> Optional[float]:
        """Calculate total analysis duration in seconds."""
        if self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return (datetime.now() - self.started_at).total_seconds()

    @property
    def failed_stage(self) -> Optional[StageProgress]:
        """Get the failed stage if any."""
        for stage in self.stages:
            if stage.is_failed:
                return stage
        return None

    @classmethod
    def initial(cls, filename: str, file_size_bytes: int) -> "ProgressState":
        """
        Create initial progress state with all stages in PENDING state.

        Args:
            filename: Name of the file to analyze
            file_size_bytes: Size of the file in bytes

        Returns:
            New ProgressState with all stages pending
        """
        # Define the 5 analysis stages
        stages = (
            StageProgress(
                stage_id=1,
                name="Parsing binary file",
                state=StageState.PENDING,
                color="cyan",
                description="LIEF parser loading binary structure",
            ),
            StageProgress(
                stage_id=2,
                name="Extracting metadata",
                state=StageState.PENDING,
                color="yellow",
                description="Detecting format, architecture, entrypoint",
            ),
            StageProgress(
                stage_id=3,
                name="Analyzing sections",
                state=StageState.PENDING,
                color="green",
                description="Processing binary sections (.text, .data, etc.)",
            ),
            StageProgress(
                stage_id=4,
                name="Resolving dependencies",
                state=StageState.PENDING,
                color="blue",
                description="Extracting imported libraries and symbols",
            ),
            StageProgress(
                stage_id=5,
                name="Generating SPDX document",
                state=StageState.PENDING,
                color="magenta",
                description="Creating SBOM in SPDX format",
            ),
        )

        # Create initial metrics
        metrics = AnalysisMetrics(
            file_size_bytes=file_size_bytes,
            bytes_processed=0,
            processing_rate_bytes_per_sec=0.0,
            time_elapsed_seconds=0.0,
            estimated_time_remaining_seconds=None,
        )

        return cls(
            filename=filename,
            stages=stages,
            metrics=metrics,
            current_stage_index=0,
            overall_progress=0.0,
            is_complete=False,
            is_failed=False,
            started_at=datetime.now(),
        )

    def with_stage_update(
        self,
        stage_id: int,
        state: StageState,
        progress: Optional[int] = None,
        processed_items: Optional[int] = None,
        total_items: Optional[int] = None,
        result: Optional[str] = None,
        error_message: Optional[str] = None,
    ) -> "ProgressState":
        """
        Create new ProgressState with updated stage.

        Args:
            stage_id: Stage identifier (1-5)
            state: New stage state
            progress: New progress percentage (0-100)
            processed_items: Number of items processed
            total_items: Total items to process
            result: Result summary
            error_message: Error message if failed

        Returns:
            New ProgressState with updated stage
        """
        # Convert stage_id to index
        stage_idx = stage_id - 1

        # Get the current stage
        current_stage = self.stages[stage_idx]

        # Update the stage with new values
        if state == StageState.ACTIVE:
            new_stage = current_stage.start()
        elif state == StageState.COMPLETE:
            new_stage = current_stage.complete(result=result)
        elif state == StageState.FAILED:
            new_stage = current_stage.fail(error_message=error_message)
        else:
            new_stage = current_stage

        # Update progress and items if provided
        if progress is not None or processed_items is not None:
            new_stage = new_stage.with_progress(
                progress=progress, processed_items=processed_items
            )

        if total_items is not None:
            new_stage = dataclasses.replace(new_stage, total_items=total_items)

        # Create new stages tuple
        new_stages = list(self.stages)
        new_stages[stage_idx] = new_stage
        new_stages_tuple = tuple(new_stages)

        # Update current stage index
        new_current_stage_index = self.current_stage_index
        if state == StageState.ACTIVE:
            new_current_stage_index = stage_idx
        elif state == StageState.COMPLETE and stage_idx == self.current_stage_index:
            # Move to next stage
            if stage_idx + 1 < len(self.stages):
                new_current_stage_index = stage_idx + 1

        # Calculate overall progress
        new_overall_progress = self._calculate_overall_progress(new_stages_tuple)

        # Update metrics
        new_metrics = self._update_metrics(new_stages_tuple)

        # Check if complete or failed
        is_complete = all(s.is_complete for s in new_stages_tuple)
        is_failed = any(s.is_failed for s in new_stages_tuple)

        return dataclasses.replace(
            self,
            stages=new_stages_tuple,
            current_stage_index=new_current_stage_index,
            overall_progress=new_overall_progress,
            metrics=new_metrics,
            is_complete=is_complete,
            is_failed=is_failed,
            completed_at=datetime.now() if (is_complete or is_failed) else None,
        )

    def _calculate_overall_progress(
        self, stages: Tuple[StageProgress, ...]
    ) -> float:
        """
        Calculate overall progress from all stages.

        Uses weighted progress based on typical stage durations:
        - Stage 1 (File Parsing): 70% (slowest)
        - Stage 2 (Metadata): 10%
        - Stage 3 (Sections): 10%
        - Stage 4 (Dependencies): 5%
        - Stage 5 (SPDX): 5%

        Weights are defined in STAGE_WEIGHTS constant.
        """
        total_progress = 0.0

        # Sum weighted progress from each stage
        for stage in stages:
            weight = STAGE_WEIGHTS.get(stage.stage_id, 0.0)
            if stage.is_complete:
                # Complete stages contribute full weight * 100%
                total_progress += weight * 100.0
            elif stage.is_active and stage.progress is not None:
                # Active stages contribute weighted progress percentage
                total_progress += weight * stage.progress
            # Pending stages contribute 0%

        return total_progress

    def _update_metrics(self, stages: Tuple[StageProgress, ...]) -> AnalysisMetrics:
        """Update metrics based on current stage progress."""
        # Calculate time elapsed since analysis started
        time_elapsed = self.duration_seconds or 0.0

        # Calculate bytes processed based on overall progress percentage
        bytes_processed = int(
            self.metrics.file_size_bytes * (self.overall_progress / 100.0)
        )

        # Calculate processing rate (bytes per second)
        if time_elapsed > 0:
            processing_rate = bytes_processed / time_elapsed
        else:
            processing_rate = 0.0

        # Estimate time remaining using ETA estimator if available
        eta = None
        if self.eta_estimator is not None:
            # Use ETA estimator for enhanced prediction
            eta = self.eta_estimator.estimate_remaining(
                file_size_bytes=self.metrics.file_size_bytes,
                bytes_processed=bytes_processed,
                elapsed_seconds=time_elapsed,
            )
        else:
            # Fall back to simple calculation
            if processing_rate > 0:
                bytes_remaining = self.metrics.file_size_bytes - bytes_processed
                eta = bytes_remaining / processing_rate

        # Collect stage-specific metrics (e.g., item counts, results)
        stage_metrics = {}
        for stage in stages:
            if stage.is_active or stage.is_complete:
                stage_metrics[f"stage_{stage.stage_id}"] = {
                    "name": stage.name,
                    "processed_items": stage.processed_items,
                    "total_items": stage.total_items,
                    "result": stage.result,
                }

        # Return new immutable metrics object with updated values
        return dataclasses.replace(
            self.metrics,
            bytes_processed=bytes_processed,
            processing_rate_bytes_per_sec=processing_rate,
            time_elapsed_seconds=time_elapsed,
            estimated_time_remaining_seconds=eta,
            stage_specific_metrics=stage_metrics,
        )

    def complete(self) -> "ProgressState":
        """Mark analysis as complete."""
        # Record processing time in ETA estimator if available
        if self.eta_estimator is not None:
            duration = self.duration_seconds
            if duration is not None and duration > 0:
                try:
                    self.eta_estimator.record_processing(
                        file_size_bytes=self.metrics.file_size_bytes,
                        processing_time_seconds=duration,
                    )
                except Exception as e:
                    # Don't fail analysis if ETA recording fails
                    # Log will be handled by ETA estimator internally
                    pass

        return dataclasses.replace(
            self,
            is_complete=True,
            overall_progress=100.0,
            completed_at=datetime.now(),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert progress state to dictionary for JSON serialization."""
        return {
            "filename": self.filename,
            "stages": [
                {
                    "stage_id": s.stage_id,
                    "name": s.name,
                    "state": str(s.state),
                    "progress": s.progress,
                    "total_items": s.total_items,
                    "processed_items": s.processed_items,
                    "result": s.result,
                    "error_message": s.error_message,
                    "duration_seconds": s.duration_seconds,
                }
                for s in self.stages
            ],
            "metrics": self.metrics.to_dict(),
            "current_stage_index": self.current_stage_index,
            "overall_progress": round(self.overall_progress, 2),
            "is_complete": self.is_complete,
            "is_failed": self.is_failed,
            "duration_seconds": self.duration_seconds,
            "started_at": self.started_at.isoformat(),
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
        }
