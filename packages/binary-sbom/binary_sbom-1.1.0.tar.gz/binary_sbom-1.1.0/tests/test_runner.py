"""
Simple test runner for ProgressTracker tests.

This script runs tests without requiring pytest.
"""

import sys
import traceback
from datetime import datetime

# Add src to path
sys.path.insert(0, ".")

from src.binary_sbom.progress_state import StageState
from src.binary_sbom.progress_tracker import (
    ProgressTracker,
    create_progress_tracker,
)


class TestRunner:
    """Simple test runner."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.failures = []

    def test(self, func):
        """Run a test function."""
        try:
            func()
            self.passed += 1
            print(f"✓ {func.__name__}")
            return True
        except AssertionError as e:
            self.failed += 1
            error_msg = str(e) if str(e) else traceback.format_exc()
            self.failures.append((func.__name__, error_msg))
            print(f"✗ {func.__name__}: {e}")
            return False
        except Exception as e:
            self.failed += 1
            error_msg = traceback.format_exc()
            self.failures.append((func.__name__, error_msg))
            print(f"✗ {func.__name__}: {type(e).__name__}: {e}")
            print(f"  {error_msg}")
            return False

    def summary(self):
        """Print test summary."""
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Tests run: {total}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"{'='*60}")

        if self.failures:
            print("\nFailures:")
            for name, error in self.failures:
                print(f"\n{name}:")
                print(error)

        return self.failed == 0


# Test functions
def test_initialization():
    """Test ProgressTracker initialization."""
    tracker = ProgressTracker(
        filename="test.bin",
        file_size_bytes=1024 * 1024,
        verbose=False,
    )
    assert tracker.filename == "test.bin"
    assert tracker.file_size_bytes == 1024 * 1024
    assert tracker.verbose is False


def test_initial_state():
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


def test_start_stage():
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


def test_complete_stage():
    """Test completing a stage."""
    tracker = ProgressTracker(
        filename="test.bin",
        file_size_bytes=1024 * 1024,
        verbose=False,
    )
    tracker.update(stage_id=1, state=StageState.ACTIVE)
    tracker.update(stage_id=1, state=StageState.COMPLETE, result="Parsing complete")
    state = tracker.get_state()
    assert state.stages[0].state == StageState.COMPLETE
    assert state.stages[0].result == "Parsing complete"
    assert state.stages[0].completed_at is not None


def test_fail_stage():
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


def test_progress_update():
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


def test_item_count_update():
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


def test_complete_all_stages():
    """Test completing all stages marks analysis as complete."""
    tracker = ProgressTracker(
        filename="test.bin",
        file_size_bytes=1024 * 1024,
        verbose=False,
    )
    for i in range(1, 6):
        tracker.update(stage_id=i, state=StageState.COMPLETE)
    state = tracker.get_state()
    assert state.is_complete is True
    assert state.is_failed is False
    assert state.overall_progress == 100.0


def test_failed_stage_prevents_completion():
    """Test that a failed stage marks analysis as failed."""
    tracker = ProgressTracker(
        filename="test.bin",
        file_size_bytes=1024 * 1024,
        verbose=False,
    )
    tracker.update(stage_id=1, state=StageState.COMPLETE)
    tracker.update(
        stage_id=2,
        state=StageState.FAILED,
        error_message="Error",
    )
    state = tracker.get_state()
    assert state.is_failed is True
    assert state.is_complete is False


def test_get_callback():
    """Test get_callback returns callable."""
    tracker = ProgressTracker(
        filename="test.bin",
        file_size_bytes=1024 * 1024,
        verbose=False,
    )
    callback = tracker.get_callback()
    assert callable(callback)


def test_callback_updates_progress():
    """Test that callback updates progress correctly."""
    tracker = ProgressTracker(
        filename="test.bin",
        file_size_bytes=1024 * 1024,
        verbose=False,
    )
    callback = tracker.get_callback()
    callback(stage_id=1, state=StageState.ACTIVE, progress=50)
    state = tracker.get_state()
    assert state.stages[0].state == StageState.ACTIVE
    assert state.stages[0].progress == 50


def test_factory_function():
    """Test create_progress_tracker factory function."""
    tracker = create_progress_tracker(
        filename="test.bin",
        file_size_bytes=1024 * 1024,
        verbose=False,
    )
    assert isinstance(tracker, ProgressTracker)


def test_verbose_false_skips_display():
    """Test that verbose=False skips display updates."""
    tracker = ProgressTracker(
        filename="test.bin",
        file_size_bytes=1024 * 1024,
        verbose=False,
    )
    tracker.start()
    tracker.update(stage_id=1, state=StageState.ACTIVE)
    tracker.update(stage_id=1, state=StageState.COMPLETE)
    tracker.complete()
    state = tracker.get_state()
    assert state.stages[0].is_complete


# Run all tests
if __name__ == "__main__":
    print("Running ProgressTracker tests...\n")
    runner = TestRunner()

    # Run all test functions
    test_functions = [
        test_initialization,
        test_initial_state,
        test_start_stage,
        test_complete_stage,
        test_fail_stage,
        test_progress_update,
        test_item_count_update,
        test_complete_all_stages,
        test_failed_stage_prevents_completion,
        test_get_callback,
        test_callback_updates_progress,
        test_factory_function,
        test_verbose_false_skips_display,
    ]

    for test_func in test_functions:
        runner.test(test_func)

    # Print summary
    success = runner.summary()
    sys.exit(0 if success else 1)
