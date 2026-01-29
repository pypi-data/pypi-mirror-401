"""
Unit tests for the ETA estimator module.

Tests processing records, EMA estimates, and time estimation functionality.
"""

import json
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from binary_sbom.eta_estimator import (
    DEFAULT_ALPHA,
    DEFAULT_HISTORY_SIZE,
    EMAEstimate,
    ETAEstimator,
    MIN_SAMPLES_FOR_PREDICTION,
    ProcessingRecord,
    SIZE_BUCKET_THRESHOLD,
)


class TestProcessingRecord:
    """Test ProcessingRecord dataclass functionality."""

    def test_processing_record_creation_valid(self):
        """Test creating a valid processing record."""
        record = ProcessingRecord(
            file_size_bytes=1024 * 1024,  # 1 MB
            processing_time_seconds=2.5,
            timestamp=datetime.now(),
            file_type="ELF",
            architecture="x86_64",
        )

        assert record.file_size_bytes == 1024 * 1024
        assert record.processing_time_seconds == 2.5
        assert record.file_type == "ELF"
        assert record.architecture == "x86_64"

    def test_processing_record_invalid_file_size(self):
        """Test that negative file size raises ValueError."""
        with pytest.raises(ValueError, match="file_size_bytes must be >= 0"):
            ProcessingRecord(
                file_size_bytes=-1,
                processing_time_seconds=1.0,
                timestamp=datetime.now(),
            )

    def test_processing_record_invalid_processing_time(self):
        """Test that negative processing time raises ValueError."""
        with pytest.raises(ValueError, match="processing_time_seconds must be >= 0"):
            ProcessingRecord(
                file_size_bytes=1024,
                processing_time_seconds=-1.0,
                timestamp=datetime.now(),
            )

    def test_processing_record_file_size_mb(self):
        """Test file_size_mb property."""
        record = ProcessingRecord(
            file_size_bytes=2 * 1024 * 1024,  # 2 MB
            processing_time_seconds=1.0,
            timestamp=datetime.now(),
        )

        assert record.file_size_mb == 2.0

    def test_processing_record_processing_rate_bytes_per_sec(self):
        """Test processing_rate_bytes_per_sec property."""
        record = ProcessingRecord(
            file_size_bytes=1024 * 1024,  # 1 MB
            processing_time_seconds=2.0,  # 2 seconds
            timestamp=datetime.now(),
        )

        expected_rate = (1024 * 1024) / 2.0
        assert record.processing_rate_bytes_per_sec == expected_rate

    def test_processing_rate_zero_time(self):
        """Test processing rate when time is zero."""
        record = ProcessingRecord(
            file_size_bytes=1024,
            processing_time_seconds=0.0,
            timestamp=datetime.now(),
        )

        assert record.processing_rate_bytes_per_sec == 0.0

    def test_processing_rate_mb_per_sec(self):
        """Test processing_rate_mb_per_sec property."""
        record = ProcessingRecord(
            file_size_bytes=10 * 1024 * 1024,  # 10 MB
            processing_time_seconds=2.0,  # 2 seconds
            timestamp=datetime.now(),
        )

        expected_rate_mb = 10.0 / 2.0  # 5 MB/sec
        assert record.processing_rate_mb_per_sec == expected_rate_mb

    def test_processing_record_to_dict(self):
        """Test converting record to dictionary."""
        timestamp = datetime.now()
        record = ProcessingRecord(
            file_size_bytes=1024 * 1024,
            processing_time_seconds=2.5,
            timestamp=timestamp,
            file_type="ELF",
            architecture="x86_64",
        )

        record_dict = record.to_dict()

        assert record_dict["file_size_bytes"] == 1024 * 1024
        assert record_dict["file_size_mb"] == 1.0
        assert record_dict["processing_time_seconds"] == 2.5
        assert "processing_rate_bytes_per_sec" in record_dict
        assert "processing_rate_mb_per_sec" in record_dict
        assert record_dict["timestamp"] == timestamp.isoformat()
        assert record_dict["file_type"] == "ELF"
        assert record_dict["architecture"] == "x86_64"


class TestEMAEstimate:
    """Test EMAEstimate dataclass functionality."""

    def test_ema_estimate_creation_default(self):
        """Test creating EMA estimate with defaults."""
        ema = EMAEstimate()

        assert ema.current_estimate == 0.0
        assert ema.alpha == DEFAULT_ALPHA
        assert ema.sample_count == 0
        assert ema.last_updated is None

    def test_ema_estimate_creation_custom(self):
        """Test creating EMA estimate with custom values."""
        timestamp = datetime.now()
        ema = EMAEstimate(
            current_estimate=1000000.0,
            alpha=0.5,
            sample_count=10,
            last_updated=timestamp,
        )

        assert ema.current_estimate == 1000000.0
        assert ema.alpha == 0.5
        assert ema.sample_count == 10
        assert ema.last_updated == timestamp

    def test_ema_estimate_invalid_alpha_zero(self):
        """Test that alpha of 0 raises ValueError."""
        with pytest.raises(ValueError, match="alpha must be 0-1"):
            EMAEstimate(alpha=0.0)

    def test_ema_estimate_invalid_alpha_negative(self):
        """Test that negative alpha raises ValueError."""
        with pytest.raises(ValueError, match="alpha must be 0-1"):
            EMAEstimate(alpha=-0.1)

    def test_ema_estimate_invalid_alpha_greater_than_one(self):
        """Test that alpha > 1 raises ValueError."""
        with pytest.raises(ValueError, match="alpha must be 0-1"):
            EMAEstimate(alpha=1.5)

    def test_ema_estimate_invalid_current_estimate(self):
        """Test that negative current_estimate raises ValueError."""
        with pytest.raises(ValueError, match="current_estimate must be >= 0"):
            EMAEstimate(current_estimate=-1.0)

    def test_ema_estimate_invalid_sample_count(self):
        """Test that negative sample_count raises ValueError."""
        with pytest.raises(ValueError, match="sample_count must be >= 0"):
            EMAEstimate(sample_count=-1)

    def test_ema_estimate_update_first_sample(self):
        """Test EMA update with first sample."""
        ema = EMAEstimate(alpha=0.3)

        ema.update(1000000.0)  # 1 MB/sec

        assert ema.current_estimate == 1000000.0
        assert ema.sample_count == 1
        assert ema.last_updated is not None

    def test_ema_estimate_update_second_sample(self):
        """Test EMA update with second sample applies smoothing."""
        ema = EMAEstimate(alpha=0.3)
        ema.update(1000000.0)  # First sample: 1 MB/sec

        ema.update(2000000.0)  # Second sample: 2 MB/sec

        # EMA = 0.3 * 2,000,000 + 0.7 * 1,000,000 = 1,300,000
        expected = 0.3 * 2000000.0 + 0.7 * 1000000.0
        assert ema.current_estimate == expected
        assert ema.sample_count == 2

    def test_ema_estimate_update_invalid_value(self):
        """Test that invalid measurement doesn't update estimate."""
        ema = EMAEstimate(alpha=0.3)
        ema.update(1000000.0)

        ema.update(0.0)  # Invalid (zero)
        assert ema.current_estimate == 1000000.0
        assert ema.sample_count == 1

        ema.update(-1.0)  # Invalid (negative)
        assert ema.current_estimate == 1000000.0
        assert ema.sample_count == 1

    def test_ema_estimate_is_reliable(self):
        """Test is_reliable method."""
        ema = EMAEstimate(alpha=0.3)

        # Not enough samples
        assert not ema.is_reliable()

        # Add minimum samples
        for _ in range(MIN_SAMPLES_FOR_PREDICTION):
            ema.update(1000000.0)

        assert ema.is_reliable()

    def test_ema_estimate_get_confidence(self):
        """Test get_confidence method."""
        ema = EMAEstimate(alpha=0.3)

        # No samples
        assert ema.get_confidence() == 0.0

        # Add some samples
        ema.update(1000000.0)
        confidence_1 = ema.get_confidence()
        assert 0.0 < confidence_1 < 1.0

        # Add more samples, confidence should increase
        for _ in range(9):
            ema.update(1000000.0)

        confidence_10 = ema.get_confidence()
        assert confidence_10 > confidence_1
        assert confidence_10 == 1.0  # Should reach max at 10 samples

        # More samples should keep confidence at 1.0
        ema.update(1000000.0)
        assert ema.get_confidence() == 1.0


class TestETAEstimatorInit:
    """Test ETAEstimator initialization."""

    def test_estimator_init_default(self):
        """Test estimator initialization with defaults."""
        estimator = ETAEstimator()

        assert estimator.history_size == DEFAULT_HISTORY_SIZE
        assert len(estimator) == 0
        assert estimator.ema_estimate.alpha == DEFAULT_ALPHA
        assert estimator.persistence_path is None

    def test_estimator_init_custom_params(self):
        """Test estimator initialization with custom parameters."""
        estimator = ETAEstimator(
            history_size=50,
            alpha=0.5,
        )

        assert estimator.history_size == 50
        assert estimator.ema_estimate.alpha == 0.5

    def test_estimator_init_invalid_history_size(self):
        """Test that invalid history_size raises ValueError."""
        with pytest.raises(ValueError, match="history_size must be > 0"):
            ETAEstimator(history_size=0)

        with pytest.raises(ValueError, match="history_size must be > 0"):
            ETAEstimator(history_size=-1)

    def test_estimator_init_invalid_alpha(self):
        """Test that invalid alpha raises ValueError."""
        with pytest.raises(ValueError, match="alpha must be 0-1"):
            ETAEstimator(alpha=0.0)

        with pytest.raises(ValueError, match="alpha must be 0-1"):
            ETAEstimator(alpha=1.5)

    def test_estimator_init_with_persistence_path(self):
        """Test estimator initialization with persistence path."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
            temp_path = Path(f.name)

        try:
            # Create a valid history file
            data = {
                "history": [
                    {
                        "file_size_bytes": 1024 * 1024,
                        "processing_time_seconds": 1.0,
                        "timestamp": datetime.now().isoformat(),
                        "file_type": "ELF",
                        "architecture": "x86_64",
                    }
                ],
                "ema_estimate": {
                    "current_estimate": 1000000.0,
                    "alpha": 0.3,
                    "sample_count": 1,
                    "last_updated": datetime.now().isoformat(),
                },
            }

            with open(temp_path, "w") as f:
                json.dump(data, f)

            # Initialize estimator with persistence path
            estimator = ETAEstimator(persistence_path=temp_path)

            # Should load the history
            assert len(estimator) == 1

        finally:
            if temp_path.exists():
                temp_path.unlink()


class TestETAEstimatorRecordProcessing:
    """Test ETAEstimator.record_processing method."""

    def test_record_processing_valid(self):
        """Test recording a valid processing event."""
        estimator = ETAEstimator()

        record = estimator.record_processing(
            file_size_bytes=1024 * 1024,  # 1 MB
            processing_time_seconds=2.0,
            file_type="ELF",
            architecture="x86_64",
        )

        assert len(estimator) == 1
        assert record.file_size_bytes == 1024 * 1024
        assert record.processing_time_seconds == 2.0
        assert record.file_type == "ELF"
        assert record.architecture == "x86_64"

    def test_record_processing_invalid_file_size(self):
        """Test that negative file_size raises ValueError."""
        estimator = ETAEstimator()

        with pytest.raises(ValueError, match="file_size_bytes must be >= 0"):
            estimator.record_processing(
                file_size_bytes=-1,
                processing_time_seconds=1.0,
            )

    def test_record_processing_invalid_time(self):
        """Test that negative processing_time raises ValueError."""
        estimator = ETAEstimator()

        with pytest.raises(ValueError, match="processing_time_seconds must be >= 0"):
            estimator.record_processing(
                file_size_bytes=1024,
                processing_time_seconds=-1.0,
            )

    def test_record_processing_updates_ema(self):
        """Test that recording updates EMA estimate."""
        estimator = ETAEstimator(alpha=0.3)

        estimator.record_processing(
            file_size_bytes=1024 * 1024,  # 1 MB
            processing_time_seconds=1.0,  # 1 MB/sec
        )

        assert estimator.ema_estimate.sample_count == 1
        assert estimator.ema_estimate.current_estimate == (1024 * 1024) / 1.0

    def test_record_processing_respects_history_size(self):
        """Test that history respects max size."""
        estimator = ETAEstimator(history_size=3)

        # Add 5 records
        for i in range(5):
            estimator.record_processing(
                file_size_bytes=1024 * (i + 1),
                processing_time_seconds=1.0,
            )

        # Should only keep last 3
        assert len(estimator) == 3

    def test_record_processing_with_persistence(self):
        """Test recording with persistence saves to file."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
            temp_path = Path(f.name)

        try:
            estimator = ETAEstimator(persistence_path=temp_path)

            estimator.record_processing(
                file_size_bytes=1024 * 1024,
                processing_time_seconds=2.0,
                file_type="ELF",
                architecture="x86_64",
            )

            # Verify file was saved
            assert temp_path.exists()

            with open(temp_path, "r") as f:
                data = json.load(f)

            assert len(data["history"]) == 1
            assert data["history"][0]["file_size_bytes"] == 1024 * 1024

        finally:
            if temp_path.exists():
                temp_path.unlink()


class TestETAEstimatorEstimateTime:
    """Test ETAEstimator.estimate_time method."""

    def test_estimate_time_no_history(self):
        """Test estimation with no historical data."""
        estimator = ETAEstimator()

        eta = estimator.estimate_time(file_size_bytes=1024 * 1024)

        # Should return None when no reliable estimate
        assert eta is None

    def test_estimate_time_with_realtime_data(self):
        """Test estimation with real-time progress data."""
        estimator = ETAEstimator()

        # Simulate processing 50% of a 1 MB file in 1 second
        eta = estimator.estimate_time(
            file_size_bytes=1024 * 1024,
            bytes_processed=512 * 1024,  # 50% processed
            elapsed_seconds=1.0,
        )

        # Should estimate remaining 50% takes 1 second
        assert eta == 1.0

    def test_estimate_time_realtime_complete(self):
        """Test estimation when processing is complete."""
        estimator = ETAEstimator()

        eta = estimator.estimate_time(
            file_size_bytes=1024 * 1024,
            bytes_processed=1024 * 1024,  # 100% processed
            elapsed_seconds=2.0,
        )

        # Should return 0 when complete
        assert eta == 0.0

    def test_estimate_time_with_similar_history(self):
        """Test estimation using similar-sized files from history."""
        estimator = ETAEstimator()

        # Add some historical records
        estimator.record_processing(
            file_size_bytes=1024 * 1024,  # 1 MB
            processing_time_seconds=1.0,  # 1 MB/sec
            file_type="ELF",
            architecture="x86_64",
        )

        eta = estimator.estimate_time(
            file_size_bytes=1024 * 1024,  # Similar size
            file_type="ELF",
            architecture="x86_64",
        )

        # Should estimate based on historical rate
        assert eta is not None
        assert eta > 0

    def test_estimate_time_with_ema(self):
        """Test estimation using EMA when no similar records found."""
        estimator = ETAEstimator(alpha=0.3)

        # Add records to build reliable EMA
        for _ in range(MIN_SAMPLES_FOR_PREDICTION):
            estimator.record_processing(
                file_size_bytes=1024 * 1024,
                processing_time_seconds=1.0,
            )

        # Estimate for different size (no exact match)
        eta = estimator.estimate_time(file_size_bytes=2 * 1024 * 1024)

        # Should use EMA estimate
        assert eta is not None
        assert eta > 0

    def test_estimate_time_invalid_file_size(self):
        """Test estimation with invalid file size."""
        estimator = ETAEstimator()

        eta = estimator.estimate_time(file_size_bytes=0)
        assert eta is None

        eta = estimator.estimate_time(file_size_bytes=-1)
        assert eta is None


class TestETAEstimatorEstimateRemaining:
    """Test ETAEstimator.estimate_remaining method."""

    def test_estimate_remaining_complete(self):
        """Test estimate_remaining when processing is complete."""
        estimator = ETAEstimator()

        eta = estimator.estimate_remaining(
            file_size_bytes=1024 * 1024,
            bytes_processed=1024 * 1024,  # 100%
            elapsed_seconds=2.0,
        )

        assert eta == 0.0

    def test_estimate_remaining_in_progress(self):
        """Test estimate_remaining during processing."""
        estimator = ETAEstimator()

        eta = estimator.estimate_remaining(
            file_size_bytes=1024 * 1024,
            bytes_processed=512 * 1024,  # 50%
            elapsed_seconds=1.0,
        )

        # Should estimate remaining time
        assert eta == 1.0

    def test_estimate_remaining_overprocessed(self):
        """Test estimate_remaining when bytes_processed > file_size."""
        estimator = ETAEstimator()

        eta = estimator.estimate_remaining(
            file_size_bytes=1024 * 1024,
            bytes_processed=2 * 1024 * 1024,  # 200%
            elapsed_seconds=2.0,
        )

        assert eta == 0.0


class TestETAEstimatorFindSimilarRecords:
    """Test ETAEstimator._find_similar_records method."""

    def test_find_similar_records_empty_history(self):
        """Test finding similar records with empty history."""
        estimator = ETAEstimator()

        similar = estimator._find_similar_records(
            file_size_bytes=1024 * 1024,
        )

        assert similar == []

    def test_find_similar_records_by_size(self):
        """Test finding similar records by size."""
        estimator = ETAEstimator()

        # Add records with different sizes
        estimator.record_processing(
            file_size_bytes=1000 * 1024,  # ~1 MB
            processing_time_seconds=1.0,
        )
        estimator.record_processing(
            file_size_bytes=2000 * 1024,  # ~2 MB
            processing_time_seconds=2.0,
        )

        # Find similar to 1 MB
        similar = estimator._find_similar_records(file_size_bytes=1024 * 1024)

        # Should find the 1 MB record as most similar
        assert len(similar) > 0
        # First record should be most similar (highest proximity)
        assert similar[0][1] >= similar[1][1] if len(similar) > 1 else True

    def test_find_similar_records_with_filters(self):
        """Test finding similar records with type/architecture filters."""
        estimator = ETAEstimator()

        # Add records with different types
        estimator.record_processing(
            file_size_bytes=1024 * 1024,
            processing_time_seconds=1.0,
            file_type="ELF",
            architecture="x86_64",
        )
        estimator.record_processing(
            file_size_bytes=1024 * 1024,
            processing_time_seconds=1.0,
            file_type="PE",
            architecture="AMD64",
        )

        # Find similar with ELF filter
        similar = estimator._find_similar_records(
            file_size_bytes=1024 * 1024,
            file_type="ELF",
            architecture="x86_64",
        )

        # Should only return ELF records
        assert len(similar) == 1
        assert similar[0][0].file_type == "ELF"

    def test_find_similar_records_size_threshold(self):
        """Test that size threshold filters out dissimilar records."""
        estimator = ETAEstimator()

        # Add very small and very large records
        estimator.record_processing(
            file_size_bytes=1 * 1024,  # 1 KB
            processing_time_seconds=0.1,
        )
        estimator.record_processing(
            file_size_bytes=100 * 1024 * 1024,  # 100 MB
            processing_time_seconds=10.0,
        )

        # Try to find similar to 1 MB (should not match within 20% threshold)
        similar = estimator._find_similar_records(
            file_size_bytes=1024 * 1024,  # 1 MB
        )

        # Should not match records that are too different in size
        for record, proximity in similar:
            size_ratio = min(1024 * 1024, record.file_size_bytes) / max(
                1024 * 1024, record.file_size_bytes
            )
            assert proximity >= 1.0 - SIZE_BUCKET_THRESHOLD


class TestETAEstimatorGetStatistics:
    """Test ETAEstimator.get_statistics method."""

    def test_get_statistics_empty(self):
        """Test getting statistics with empty history."""
        estimator = ETAEstimator()

        stats = estimator.get_statistics()

        assert stats["total_records"] == 0
        assert stats["avg_processing_rate"] == 0.0
        assert stats["ema_estimate"] == 0.0
        assert stats["ema_confidence"] == 0.0

    def test_get_statistics_with_data(self):
        """Test getting statistics with historical data."""
        estimator = ETAEstimator()

        # Add some records
        estimator.record_processing(
            file_size_bytes=1024 * 1024,  # 1 MB
            processing_time_seconds=1.0,
        )
        estimator.record_processing(
            file_size_bytes=2 * 1024 * 1024,  # 2 MB
            processing_time_seconds=2.0,
        )

        stats = estimator.get_statistics()

        assert stats["total_records"] == 2
        assert stats["avg_processing_rate"] > 0
        assert stats["avg_processing_rate_mb_per_sec"] > 0
        assert stats["ema_estimate"] > 0
        assert stats["ema_confidence"] > 0
        assert stats["smallest_file_bytes"] == 1024 * 1024
        assert stats["largest_file_bytes"] == 2 * 1024 * 1024
        assert stats["fastest_rate_bytes_per_sec"] > 0
        assert stats["slowest_rate_bytes_per_sec"] > 0


class TestETAEstimatorClearHistory:
    """Test ETAEstimator.clear_history method."""

    def test_clear_history(self):
        """Test clearing history."""
        estimator = ETAEstimator()

        # Add some records
        for _ in range(5):
            estimator.record_processing(
                file_size_bytes=1024 * 1024,
                processing_time_seconds=1.0,
            )

        assert len(estimator) == 5

        # Clear
        estimator.clear_history()

        assert len(estimator) == 0
        assert estimator.ema_estimate.sample_count == 0

    def test_clear_history_with_persistence(self):
        """Test that clearing persists to file."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
            temp_path = Path(f.name)

        try:
            estimator = ETAEstimator(persistence_path=temp_path)

            # Add records
            estimator.record_processing(
                file_size_bytes=1024 * 1024,
                processing_time_seconds=1.0,
            )

            # Clear
            estimator.clear_history()

            # Verify file reflects cleared state
            with open(temp_path, "r") as f:
                data = json.load(f)

            assert len(data["history"]) == 0

        finally:
            if temp_path.exists():
                temp_path.unlink()


class TestETAEstimatorPersistence:
    """Test ETAEstimator persistence methods."""

    def test_save_history_no_path(self):
        """Test that saving without path raises ValueError."""
        estimator = ETAEstimator(persistence_path=None)

        with pytest.raises(ValueError, match="No persistence_path configured"):
            estimator.save_history()

    def test_load_history_no_path(self):
        """Test that loading without path raises ValueError."""
        estimator = ETAEstimator(persistence_path=None)

        with pytest.raises(ValueError, match="No persistence_path configured"):
            estimator.load_history()

    def test_save_and_load_history(self):
        """Test saving and loading history."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
            temp_path = Path(f.name)

        try:
            # Create estimator and add records
            estimator1 = ETAEstimator(persistence_path=temp_path)
            estimator1.record_processing(
                file_size_bytes=1024 * 1024,
                processing_time_seconds=1.0,
                file_type="ELF",
                architecture="x86_64",
            )

            # Create new estimator with same path (should load)
            estimator2 = ETAEstimator(persistence_path=temp_path)

            # Verify loaded data
            assert len(estimator2) == 1
            history = estimator2.get_history()
            assert history[0].file_type == "ELF"
            assert history[0].architecture == "x86_64"

        finally:
            if temp_path.exists():
                temp_path.unlink()

    def test_load_history_missing_file(self):
        """Test loading when history file doesn't exist."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
            temp_path = Path(f.name)

        # Delete the file
        temp_path.unlink()

        try:
            # Should not raise error, just initialize empty
            estimator = ETAEstimator(persistence_path=temp_path)
            assert len(estimator) == 0

        finally:
            if temp_path.exists():
                temp_path.unlink()

    def test_load_history_malformed_record(self):
        """Test loading skips malformed records."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
            temp_path = Path(f.name)

        try:
            # Create history with one valid and one invalid record
            data = {
                "history": [
                    {
                        "file_size_bytes": 1024 * 1024,
                        "processing_time_seconds": 1.0,
                        "timestamp": datetime.now().isoformat(),
                        "file_type": "ELF",
                        "architecture": "x86_64",
                    },
                    {
                        # Missing required fields
                        "file_size_bytes": 1024,
                        # Missing processing_time_seconds and timestamp
                    },
                ],
                "ema_estimate": {
                    "current_estimate": 1000000.0,
                    "alpha": 0.3,
                    "sample_count": 1,
                    "last_updated": datetime.now().isoformat(),
                },
            }

            with open(temp_path, "w") as f:
                json.dump(data, f)

            # Should load only the valid record
            estimator = ETAEstimator(persistence_path=temp_path)
            assert len(estimator) == 1

        finally:
            if temp_path.exists():
                temp_path.unlink()


class TestETAEstimatorDunderMethods:
    """Test ETAEstimator special methods."""

    def test_len(self):
        """Test __len__ method."""
        estimator = ETAEstimator()

        assert len(estimator) == 0

        estimator.record_processing(
            file_size_bytes=1024,
            processing_time_seconds=1.0,
        )

        assert len(estimator) == 1

    def test_repr(self):
        """Test __repr__ method."""
        estimator = ETAEstimator(history_size=50)

        repr_str = repr(estimator)

        assert "ETAEstimator" in repr_str
        assert "history_size=" in repr_str
        assert "ema_estimate=" in repr_str
        assert "confidence=" in repr_str
