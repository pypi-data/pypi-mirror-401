"""
Unit tests for ProgressTracker class.

Tests progress tracking functionality, thread-safety, and Rich display integration.
"""

import time
from datetime import datetime
from threading import Thread
from typing import Optional

import pytest

from src.binary_sbom.progress_state import StageState
from src.binary_sbom.progress_tracker import ProgressTracker, create_progress_tracker


class TestProgressTrackerBasics:
    """Test basic ProgressTracker functionality."""

    def test_initialization(self):
        """Test ProgressTracker initialization."""
        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,  # 1MB
            verbose=False,  # Disable Rich display for tests
        )

        assert tracker.filename == "test.bin"
        assert tracker.file_size_bytes == 1024 * 1024
        assert tracker.verbose is False
        assert tracker.refresh_per_second == 10

    def test_initial_state(self):
        """Test initial progress state."""
        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=False,
        )

        state = tracker.get_state()

        assert state.filename == "test.bin"
        assert state.is_complete is False
        assert state.is_failed is False
        assert state.overall_progress == 0.0
        assert len(state.stages) == 5
        assert all(s.state == StageState.PENDING for s in state.stages)

    def test_factory_function(self):
        """Test create_progress_tracker factory function."""
        tracker = create_progress_tracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=False,
        )

        assert isinstance(tracker, ProgressTracker)
        assert tracker.filename == "test.bin"


class TestProgressUpdates:
    """Test progress update functionality."""

    def test_start_stage(self):
        """Test starting a stage."""
        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=False,
        )

        tracker.update(stage_id=1, state=StageState.ACTIVE)

        state = tracker.get_state()
        assert state.stages[0].state == StageState.ACTIVE
        assert state.stages[0].started_at is not None

    def test_complete_stage(self):
        """Test completing a stage."""
        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=False,
        )

        tracker.update(stage_id=1, state=StageState.ACTIVE)
        tracker.update(
            stage_id=1,
            state=StageState.COMPLETE,
            result="Parsing complete",
        )

        state = tracker.get_state()
        assert state.stages[0].state == StageState.COMPLETE
        assert state.stages[0].result == "Parsing complete"
        assert state.stages[0].completed_at is not None

    def test_fail_stage(self):
        """Test failing a stage."""
        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=False,
        )

        tracker.update(
            stage_id=1,
            state=StageState.FAILED,
            error_message="Parse error",
        )

        state = tracker.get_state()
        assert state.stages[0].state == StageState.FAILED
        assert state.stages[0].error_message == "Parse error"
        assert state.is_failed is True

    def test_progress_update(self):
        """Test progress percentage updates."""
        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=False,
        )

        tracker.update(stage_id=2, state=StageState.ACTIVE)
        tracker.update(stage_id=2, state=StageState.ACTIVE, progress=50)

        state = tracker.get_state()
        assert state.stages[1].progress == 50

    def test_item_count_update(self):
        """Test processed/total items updates."""
        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=False,
        )

        tracker.update(
            stage_id=3,
            state=StageState.ACTIVE,
            total_items=100,
            processed_items=25,
        )

        state = tracker.get_state()
        assert state.stages[2].total_items == 100
        assert state.stages[2].processed_items == 25


class TestThrottling:
    """Test update throttling functionality."""

    def test_throttling_respects_interval(self):
        """Test that updates are throttled correctly."""
        refresh_rate = 10  # 10fps = 100ms interval
        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=False,
            refresh_per_second=refresh_rate,
        )

        # First update should trigger display update
        start_time = time.time()
        tracker.update(stage_id=1, state=StageState.ACTIVE)
        first_update_time = time.time() - start_time

        # Immediate second update should be throttled
        tracker.update(stage_id=1, state=StageState.ACTIVE, progress=50)

        # Wait for throttle interval
        time.sleep(1.0 / refresh_rate)

        # Third update should trigger display update
        tracker.update(stage_id=1, state=StageState.ACTIVE, progress=75)

        # State should be updated despite throttling
        state = tracker.get_state()
        assert state.stages[0].progress == 75

    def test_stage_transitions_bypass_throttling(self):
        """Test that stage transitions trigger immediate updates."""
        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=False,
            refresh_per_second=1,  # 1fps = 1s interval
        )

        # Rapid stage transitions should all trigger updates
        tracker.update(stage_id=1, state=StageState.ACTIVE)
        tracker.update(stage_id=1, state=StageState.COMPLETE)
        tracker.update(stage_id=2, state=StageState.ACTIVE)

        state = tracker.get_state()
        assert state.stages[0].is_complete
        assert state.stages[1].is_active


class TestThreadSafety:
    """Test thread-safety of ProgressTracker."""

    def test_concurrent_updates(self):
        """Test that concurrent updates are handled safely."""
        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=False,
        )

        def update_stage(stage_id: int, count: int):
            """Update a stage multiple times."""
            for i in range(count):
                progress = int((i + 1) / count * 100)
                tracker.update(
                    stage_id=stage_id,
                    state=StageState.ACTIVE,
                    progress=progress,
                )

        # Spawn multiple threads updating different stages
        threads = [
            Thread(target=update_stage, args=(1, 10)),
            Thread(target=update_stage, args=(2, 20)),
            Thread(target=update_stage, args=(3, 30)),
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # All updates should be reflected in final state
        state = tracker.get_state()
        assert state.stages[0].progress == 100
        assert state.stages[1].progress == 100
        assert state.stages[2].progress == 100

    def test_get_state_is_thread_safe(self):
        """Test that get_state returns consistent snapshots."""
        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=False,
        )

        def rapid_updates():
            """Perform rapid updates."""
            for i in range(100):
                tracker.update(
                    stage_id=1,
                    state=StageState.ACTIVE,
                    progress=i % 101,
                )

        def rapid_reads():
            """Perform rapid state reads."""
            for _ in range(100):
                state = tracker.get_state()
                # State should always be valid
                assert 0 <= state.overall_progress <= 100
                assert len(state.stages) == 5

        # Run concurrent updates and reads
        updater = Thread(target=rapid_updates)
        reader = Thread(target=rapid_reads)

        updater.start()
        reader.start()

        updater.join()
        reader.join()


class TestCompletion:
    """Test completion functionality."""

    def test_complete_all_stages(self):
        """Test completing all stages marks analysis as complete."""
        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=False,
        )

        # Complete all 5 stages
        for i in range(1, 6):
            tracker.update(stage_id=i, state=StageState.COMPLETE)

        state = tracker.get_state()
        assert state.is_complete is True
        assert state.is_failed is False
        assert state.overall_progress == 100.0

    def test_complete_method(self):
        """Test the complete() method."""
        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=False,
        )

        tracker.update(stage_id=1, state=StageState.ACTIVE)
        tracker.complete()

        state = tracker.get_state()
        assert state.is_complete is True

    def test_failed_stage_prevents_completion(self):
        """Test that a failed stage marks analysis as failed."""
        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=False,
        )

        # Complete stage 1
        tracker.update(stage_id=1, state=StageState.COMPLETE)

        # Fail stage 2
        tracker.update(
            stage_id=2,
            state=StageState.FAILED,
            error_message="Error",
        )

        state = tracker.get_state()
        assert state.is_failed is True
        assert state.is_complete is False


class TestCallback:
    """Test callback functionality."""

    def test_get_callback(self):
        """Test get_callback returns callable."""
        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=False,
        )

        callback = tracker.get_callback()
        assert callable(callback)

    def test_callback_updates_progress(self):
        """Test that callback updates progress correctly."""
        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=False,
        )

        callback = tracker.get_callback()

        # Use callback to update progress
        callback(
            stage_id=1,
            state=StageState.ACTIVE,
            progress=50,
        )

        state = tracker.get_state()
        assert state.stages[0].state == StageState.ACTIVE
        assert state.stages[0].progress == 50


class TestMetrics:
    """Test metrics calculation."""

    def test_metrics_initial_values(self):
        """Test initial metrics values."""
        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,  # 1MB
            verbose=False,
        )

        state = tracker.get_state()
        metrics = state.metrics

        assert metrics.file_size_bytes == 1024 * 1024
        assert metrics.file_size_mb == 1.0
        assert metrics.bytes_processed == 0
        assert metrics.processing_rate_bytes_per_sec == 0.0

    def test_metrics_update_with_progress(self):
        """Test metrics update as progress increases."""
        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,  # 1MB
            verbose=False,
        )

        # Complete stage 1 (70% weight)
        tracker.update(stage_id=1, state=StageState.COMPLETE)

        state = tracker.get_state()
        metrics = state.metrics

        # Should have processed 70% of file
        expected_bytes = int(1024 * 1024 * 0.70)
        assert metrics.bytes_processed == expected_bytes


class TestVerboseMode:
    """Test verbose mode functionality."""

    def test_verbose_false_skips_display(self):
        """Test that verbose=False skips display updates."""
        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=False,
        )

        # Should not raise errors even without Rich display
        tracker.start()
        tracker.update(stage_id=1, state=StageState.ACTIVE)
        tracker.update(stage_id=1, state=StageState.COMPLETE)
        tracker.complete()

        # State should still be updated
        state = tracker.get_state()
        assert state.stages[0].is_complete


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
