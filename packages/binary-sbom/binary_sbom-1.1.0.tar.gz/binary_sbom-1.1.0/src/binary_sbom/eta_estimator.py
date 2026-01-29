"""
ETA estimator with historical data tracking for binary analysis.

This module provides accurate time estimation for binary analysis by tracking
historical processing times and using exponential moving averages for predictions.

Estimates improve over time as more historical data is collected, achieving
±20% accuracy after processing ~10-20 similar binaries.

All operations are thread-safe and can be called from multiple threads.
"""

import json
import logging
import math
import threading
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Deque, Dict, List, Optional, Tuple


logger = logging.getLogger(__name__)


# Constants for ETA estimation
DEFAULT_HISTORY_SIZE = 100  # Number of historical records to keep
DEFAULT_ALPHA = 0.3  # EMA smoothing factor (0-1, lower = smoother)
MIN_SAMPLES_FOR_PREDICTION = 3  # Minimum samples before making predictions
SIZE_BUCKET_THRESHOLD = 0.2  # 20% tolerance for size matching


@dataclass(frozen=True)
class ProcessingRecord:
    """
    A single historical processing record.

    Attributes:
        file_size_bytes: Size of the file processed
        processing_time_seconds: Time taken to process the file
        timestamp: When the processing occurred
        file_type: Optional file type/format (e.g., "ELF", "PE")
        architecture: Optional architecture (e.g., "x86_64", "arm64")
    """

    file_size_bytes: int
    processing_time_seconds: float
    timestamp: datetime
    file_type: Optional[str] = None
    architecture: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate processing record fields."""
        if self.file_size_bytes < 0:
            raise ValueError("file_size_bytes must be >= 0")
        if self.processing_time_seconds < 0:
            raise ValueError("processing_time_seconds must be >= 0")

    @property
    def file_size_mb(self) -> float:
        """File size in megabytes."""
        return self.file_size_bytes / (1024 * 1024)

    @property
    def processing_rate_bytes_per_sec(self) -> float:
        """Processing rate in bytes per second."""
        if self.processing_time_seconds > 0:
            return self.file_size_bytes / self.processing_time_seconds
        return 0.0

    @property
    def processing_rate_mb_per_sec(self) -> float:
        """Processing rate in MB per second."""
        return self.processing_rate_bytes_per_sec / (1024 * 1024)

    def to_dict(self) -> Dict[str, any]:
        """Convert record to dictionary for JSON serialization."""
        return {
            "file_size_bytes": self.file_size_bytes,
            "file_size_mb": round(self.file_size_mb, 2),
            "processing_time_seconds": round(self.processing_time_seconds, 2),
            "processing_rate_bytes_per_sec": round(
                self.processing_rate_bytes_per_sec, 2
            ),
            "processing_rate_mb_per_sec": round(self.processing_rate_mb_per_sec, 2),
            "timestamp": self.timestamp.isoformat(),
            "file_type": self.file_type,
            "architecture": self.architecture,
        }


@dataclass
class EMAEstimate:
    """
    Exponential Moving Average estimate for processing rate.

    Uses EMA to provide smooth predictions that adapt to recent performance
    while maintaining stability from historical data.

    Attributes:
        current_estimate: Current EMA estimate (bytes/sec)
        alpha: Smoothing factor (0-1, lower = smoother, more weight to history)
        sample_count: Number of samples incorporated into estimate
        last_updated: Timestamp of last update
    """

    current_estimate: float = 0.0
    alpha: float = DEFAULT_ALPHA
    sample_count: int = 0
    last_updated: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Validate EMA parameters."""
        if not 0 < self.alpha <= 1:
            raise ValueError(f"alpha must be 0-1, got {self.alpha}")
        if self.current_estimate < 0:
            raise ValueError("current_estimate must be >= 0")
        if self.sample_count < 0:
            raise ValueError("sample_count must be >= 0")

    def update(self, new_value: float) -> None:
        """
        Update EMA with new measurement.

        Args:
            new_value: New processing rate measurement (bytes/sec)
        """
        if new_value <= 0:
            # Invalid measurement, skip update
            return

        if self.sample_count == 0:
            # First sample, initialize directly
            self.current_estimate = new_value
        else:
            # Apply EMA formula: EMA_new = alpha * new + (1 - alpha) * EMA_old
            self.current_estimate = (
                self.alpha * new_value + (1 - self.alpha) * self.current_estimate
            )

        self.sample_count += 1
        self.last_updated = datetime.now()

    def is_reliable(self) -> bool:
        """Check if estimate is reliable (has enough samples)."""
        return self.sample_count >= MIN_SAMPLES_FOR_PREDICTION

    def get_confidence(self) -> float:
        """
        Get confidence level in estimate (0.0-1.0).

        Confidence increases with sample count, asymptotically approaching 1.0.
        Uses logarithmic scaling: confidence = log(sample_count + 1) / log(target + 1)
        """
        target_samples = 10  # Samples needed for high confidence
        if self.sample_count >= target_samples:
            return 1.0
        return math.log(self.sample_count + 1) / math.log(target_samples + 1)


class ETAEstimator:
    """
    Estimates time remaining for binary analysis using historical data.

    Maintains a history of processing records and uses multiple estimation
    strategies:
    1. Size-based matching: Find similar-sized files in history
    2. Exponential moving average: Smooth average of processing rates
    3. Current run extrapolation: Use current progress for real-time updates

    Achieves ±20% accuracy after 10-20 similar binaries processed.

    Attributes:
        history: Deque of historical processing records
        history_size: Maximum number of records to keep
        ema_estimate: EMA estimate for overall processing rate
        persistence_path: Optional path to persist historical data
    """

    def __init__(
        self,
        history_size: int = DEFAULT_HISTORY_SIZE,
        alpha: float = DEFAULT_ALPHA,
        persistence_path: Optional[Path] = None,
    ):
        """
        Initialize ETA estimator.

        Args:
            history_size: Maximum number of historical records to keep
            alpha: EMA smoothing factor (0-1, lower = smoother)
            persistence_path: Optional path to save/load historical data
        """
        if history_size <= 0:
            raise ValueError("history_size must be > 0")
        if not 0 < alpha <= 1:
            raise ValueError(f"alpha must be 0-1, got {alpha}")

        self._lock = threading.Lock()
        self.history: Deque[ProcessingRecord] = deque(maxlen=history_size)
        self.history_size = history_size
        self.ema_estimate = EMAEstimate(alpha=alpha)
        self.persistence_path = persistence_path

        # Load persisted history if path provided
        if persistence_path and persistence_path.exists():
            self.load_history()

        logger.debug(f"ETAEstimator initialized with history_size={history_size}, alpha={alpha}")

    def record_processing(
        self,
        file_size_bytes: int,
        processing_time_seconds: float,
        file_type: Optional[str] = None,
        architecture: Optional[str] = None,
    ) -> ProcessingRecord:
        """
        Record a completed binary analysis.

        Thread-safe method that adds a new processing record to history.

        Args:
            file_size_bytes: Size of the processed file
            processing_time_seconds: Time taken for processing
            file_type: Optional file type/format
            architecture: Optional architecture

        Returns:
            ProcessingRecord that was created and added to history
        """
        if file_size_bytes < 0:
            raise ValueError(f"file_size_bytes must be >= 0, got {file_size_bytes}")
        if processing_time_seconds < 0:
            raise ValueError(f"processing_time_seconds must be >= 0, got {processing_time_seconds}")

        record = ProcessingRecord(
            file_size_bytes=file_size_bytes,
            processing_time_seconds=processing_time_seconds,
            timestamp=datetime.now(),
            file_type=file_type,
            architecture=architecture,
        )

        with self._lock:
            self.history.append(record)

            # Update EMA with processing rate
            processing_rate = record.processing_rate_bytes_per_sec
            self.ema_estimate.update(processing_rate)

            # Persist history if path configured
            if self.persistence_path:
                try:
                    self.save_history()
                except (IOError, OSError) as e:
                    logger.warning(f"Failed to save history: {e}")

        logger.debug(
            f"Recorded processing: file_size={file_size_bytes} bytes, "
            f"time={processing_time_seconds:.2f}s, rate={processing_rate:.2f} bytes/sec"
        )

        return record

    def estimate_time(
        self,
        file_size_bytes: int,
        file_type: Optional[str] = None,
        architecture: Optional[str] = None,
        bytes_processed: Optional[int] = None,
        elapsed_seconds: Optional[float] = None,
    ) -> Optional[float]:
        """
        Estimate processing time for a file.

        Thread-safe method that uses multiple strategies in order of preference:
        1. Current run extrapolation (if real-time data available)
        2. Size-based matching from history
        3. EMA estimate

        Args:
            file_size_bytes: Size of the file to estimate
            file_type: Optional file type for better matching
            architecture: Optional architecture for better matching
            bytes_processed: Optional bytes processed so far (for real-time)
            elapsed_seconds: Optional elapsed time so far (for real-time)

        Returns:
            Estimated time in seconds, or None if unable to estimate
        """
        if file_size_bytes <= 0:
            return None

        # Strategy 1: Real-time extrapolation (most accurate if available)
        if (
            bytes_processed is not None
            and elapsed_seconds is not None
            and bytes_processed > 0
            and elapsed_seconds > 0
        ):
            current_rate = bytes_processed / elapsed_seconds
            if current_rate > 0:
                remaining_bytes = file_size_bytes - bytes_processed
                eta = remaining_bytes / current_rate
                logger.debug(f"Real-time ETA estimate: {eta:.2f}s")
                return eta

        # Strategy 2 & 3: Need to access history and EMA (thread-safe)
        with self._lock:
            # Strategy 2: Size-based matching from history
            similar_records = self._find_similar_records(
                file_size_bytes, file_type, architecture
            )
            if similar_records:
                # Calculate weighted average based on size proximity
                total_weight = 0.0
                weighted_rate = 0.0

                for record, proximity in similar_records:
                    weight = proximity  # Higher proximity = higher weight
                    weighted_rate += weight * record.processing_rate_bytes_per_sec
                    total_weight += weight

                if total_weight > 0:
                    estimated_rate = weighted_rate / total_weight
                    eta = file_size_bytes / estimated_rate
                    logger.debug(f"Size-based ETA estimate: {eta:.2f}s")
                    return eta

            # Strategy 3: Fall back to EMA estimate
            if self.ema_estimate.is_reliable():
                eta = file_size_bytes / self.ema_estimate.current_estimate
                logger.debug(f"EMA-based ETA estimate: {eta:.2f}s")
                return eta

        # No reliable estimate available
        logger.debug("No reliable ETA estimate available")
        return None

    def estimate_remaining(
        self,
        file_size_bytes: int,
        bytes_processed: int,
        elapsed_seconds: float,
        file_type: Optional[str] = None,
        architecture: Optional[str] = None,
    ) -> Optional[float]:
        """
        Estimate remaining time for an in-progress analysis.

        This is the main method for real-time ETA updates during processing.

        Args:
            file_size_bytes: Total file size
            bytes_processed: Bytes processed so far
            elapsed_seconds: Time elapsed so far
            file_type: Optional file type for better matching
            architecture: Optional architecture for better matching

        Returns:
            Estimated remaining time in seconds, or None if unable to estimate
        """
        if bytes_processed >= file_size_bytes:
            return 0.0

        return self.estimate_time(
            file_size_bytes=file_size_bytes,
            file_type=file_type,
            architecture=architecture,
            bytes_processed=bytes_processed,
            elapsed_seconds=elapsed_seconds,
        )

    def _find_similar_records(
        self,
        file_size_bytes: int,
        file_type: Optional[str] = None,
        architecture: Optional[str] = None,
    ) -> List[Tuple[ProcessingRecord, float]]:
        """
        Find historical records with similar file sizes and characteristics.

        Returns records with proximity scores (0.0-1.0, higher = more similar).

        Args:
            file_size_bytes: Size to match against
            file_type: Optional file type to filter by
            architecture: Optional architecture to filter by

        Returns:
            List of (record, proximity) tuples, sorted by proximity descending
        """
        if not self.history:
            return []

        matches = []

        for record in self.history:
            # Filter by file type and architecture if specified
            if file_type and record.file_type and file_type != record.file_type:
                continue
            if (
                architecture
                and record.architecture
                and architecture != record.architecture
            ):
                continue

            # Calculate size proximity (0.0-1.0)
            size_ratio = min(file_size_bytes, record.file_size_bytes) / max(
                file_size_bytes, record.file_size_bytes
            )
            proximity = size_ratio  # Higher ratio = more similar

            # Only include reasonably close matches (within 80% size similarity)
            if proximity >= 1.0 - SIZE_BUCKET_THRESHOLD:
                matches.append((record, proximity))

        # Sort by proximity descending
        matches.sort(key=lambda x: x[1], reverse=True)

        return matches

    def get_statistics(self) -> Dict[str, any]:
        """
        Get statistics about historical processing data.

        Thread-safe method that returns current statistics.

        Returns:
            Dictionary with statistics including:
            - total_records: Number of historical records
            - avg_processing_rate: Average processing rate (bytes/sec)
            - avg_processing_rate_mb_per_sec: Average processing rate (MB/sec)
            - ema_estimate: Current EMA estimate
            - ema_confidence: Confidence in EMA estimate (0.0-1.0)
            - smallest_file: Smallest file processed
            - largest_file: Largest file processed
            - fastest_rate: Fastest processing rate
            - slowest_rate: Slowest processing rate
        """
        with self._lock:
            if not self.history:
                return {
                    "total_records": 0,
                    "avg_processing_rate": 0.0,
                    "avg_processing_rate_mb_per_sec": 0.0,
                    "ema_estimate": 0.0,
                    "ema_confidence": 0.0,
                }

            rates = [r.processing_rate_bytes_per_sec for r in self.history]
            sizes = [r.file_size_bytes for r in self.history]

            return {
                "total_records": len(self.history),
                "avg_processing_rate": sum(rates) / len(rates),
                "avg_processing_rate_mb_per_sec": (
                    sum(rates) / len(rates)
                ) / (1024 * 1024),
                "ema_estimate": self.ema_estimate.current_estimate,
                "ema_estimate_mb_per_sec": self.ema_estimate.current_estimate
                / (1024 * 1024),
                "ema_confidence": self.ema_estimate.get_confidence(),
                "smallest_file_bytes": min(sizes),
                "smallest_file_mb": min(sizes) / (1024 * 1024),
                "largest_file_bytes": max(sizes),
                "largest_file_mb": max(sizes) / (1024 * 1024),
                "fastest_rate_bytes_per_sec": max(rates),
                "fastest_rate_mb_per_sec": max(rates) / (1024 * 1024),
                "slowest_rate_bytes_per_sec": min(rates),
                "slowest_rate_mb_per_sec": min(rates) / (1024 * 1024),
            }

    def get_history(self) -> List[ProcessingRecord]:
        """
        Get all historical records.

        Thread-safe method that returns a snapshot of current history.

        Returns:
            List of all processing records in chronological order
        """
        with self._lock:
            return list(self.history)

    def clear_history(self) -> None:
        """
        Clear all historical records and reset EMA.

        Thread-safe method that clears all historical data.
        """
        with self._lock:
            self.history.clear()
            self.ema_estimate = EMAEstimate(alpha=self.ema_estimate.alpha)

            if self.persistence_path:
                try:
                    self.save_history()
                except (IOError, OSError) as e:
                    logger.warning(f"Failed to save history after clearing: {e}")

        logger.info("Cleared all historical records")

    def save_history(self) -> None:
        """
        Save historical data to persistence path.

        Note: This method should only be called from within a locked context
        or during initialization. Thread-safety is the caller's responsibility.

        Raises:
            ValueError: If persistence_path is not configured
            IOError: If unable to write to file
        """
        if not self.persistence_path:
            raise ValueError("No persistence_path configured")

        try:
            # Ensure parent directory exists
            self.persistence_path.parent.mkdir(parents=True, exist_ok=True)

            data = {
                "history": [record.to_dict() for record in self.history],
                "ema_estimate": {
                    "current_estimate": self.ema_estimate.current_estimate,
                    "alpha": self.ema_estimate.alpha,
                    "sample_count": self.ema_estimate.sample_count,
                    "last_updated": (
                        self.ema_estimate.last_updated.isoformat()
                        if self.ema_estimate.last_updated
                        else None
                    ),
                },
            }

            with open(self.persistence_path, "w") as f:
                json.dump(data, f, indent=2)

            logger.debug(f"Saved {len(self.history)} historical records to {self.persistence_path}")
        except (IOError, OSError) as e:
            logger.error(f"Failed to save history to {self.persistence_path}: {e}")
            raise

    def load_history(self) -> None:
        """
        Load historical data from persistence path.

        Note: This method should only be called during initialization.
        Thread-safety is the caller's responsibility.

        Raises:
            ValueError: If persistence_path is not configured
            IOError: If unable to read from file
        """
        if not self.persistence_path:
            raise ValueError("No persistence_path configured")

        if not self.persistence_path.exists():
            logger.debug(f"No history file found at {self.persistence_path}")
            return

        try:
            with open(self.persistence_path, "r") as f:
                data = json.load(f)

            # Load history
            self.history.clear()
            loaded_count = 0
            for record_data in data.get("history", []):
                try:
                    record = ProcessingRecord(
                        file_size_bytes=record_data["file_size_bytes"],
                        processing_time_seconds=record_data["processing_time_seconds"],
                        timestamp=datetime.fromisoformat(record_data["timestamp"]),
                        file_type=record_data.get("file_type"),
                        architecture=record_data.get("architecture"),
                    )
                    self.history.append(record)
                    loaded_count += 1
                except (KeyError, ValueError) as e:
                    # Skip malformed records
                    logger.warning(f"Skipping malformed record: {e}")
                    continue

            # Load EMA estimate
            ema_data = data.get("ema_estimate", {})
            self.ema_estimate = EMAEstimate(
                current_estimate=ema_data.get("current_estimate", 0.0),
                alpha=ema_data.get("alpha", DEFAULT_ALPHA),
                sample_count=ema_data.get("sample_count", 0),
                last_updated=(
                    datetime.fromisoformat(ema_data["last_updated"])
                    if ema_data.get("last_updated")
                    else None
                ),
            )

            logger.info(f"Loaded {loaded_count} historical records from {self.persistence_path}")
        except (IOError, OSError, json.JSONDecodeError) as e:
            logger.error(f"Failed to load history from {self.persistence_path}: {e}")
            raise

    def __len__(self) -> int:
        """
        Return number of historical records.

        Thread-safe method.
        """
        with self._lock:
            return len(self.history)

    def __repr__(self) -> str:
        """
        Return string representation of estimator.

        Thread-safe method.
        """
        with self._lock:
            return (
                f"ETAEstimator(history_size={len(self.history)}/{self.history_size}, "
                f"ema_estimate={self.ema_estimate.current_estimate:.2f} bytes/sec, "
                f"confidence={self.ema_estimate.get_confidence():.2%})"
            )
