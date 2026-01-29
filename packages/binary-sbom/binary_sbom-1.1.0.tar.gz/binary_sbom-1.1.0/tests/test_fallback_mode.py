"""
Test graceful degradation when Rich library is unavailable.

This test verifies that ProgressTracker falls back to text-only mode
when Rich library is not installed.
"""

import sys
import unittest
from unittest.mock import MagicMock, patch

# Temporarily hide Rich library to simulate it being unavailable
class TestFallbackMode(unittest.TestCase):
    """Test fallback mode when Rich library is unavailable."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock imports to simulate Rich being unavailable
        self.rich_patcher = patch.dict(
            "sys.modules",
            {
                "rich": MagicMock(),
                "rich.console": MagicMock(),
                "rich.live": MagicMock(),
                "rich.panel": MagicMock(),
                "rich.progress": MagicMock(),
                "rich.table": MagicMock(),
            },
        )
        self.mock_rich = self.rich_patcher.start()

        # Make Rich imports fail
        self.mock_rich["rich"].ImportError = ImportError
        sys.modules["rich"].console = MagicMock(side_effect=ImportError)
        sys.modules["rich"].live = MagicMock(side_effect=ImportError)
        sys.modules["rich"].panel = MagicMock(side_effect=ImportError)
        sys.modules["rich"].progress = MagicMock(side_effect=ImportError)
        sys.modules["rich"].table = MagicMock(side_effect=ImportError)

    def tearDown(self):
        """Clean up after tests."""
        self.rich_patcher.stop()

    def test_fallback_mode_initialization(self):
        """Test that ProgressTracker initializes when Rich is unavailable."""
        # Import after mocking Rich
        from src.binary_sbom.progress_tracker import ProgressTracker, RICH_AVAILABLE

        # RICH_AVAILABLE should be False
        self.assertFalse(RICH_AVAILABLE)

        # ProgressTracker should still initialize
        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,  # 1MB
            verbose=True,
        )

        # Tracker should know Rich is unavailable
        self.assertFalse(tracker._rich_available)

    def test_fallback_mode_start(self):
        """Test that start() doesn't crash when Rich is unavailable."""
        from src.binary_sbom.progress_tracker import ProgressTracker

        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=True,
        )

        # Should not raise exception
        tracker.start()

        # Rich components should not be initialized
        self.assertIsNone(tracker._rich_progress)
        self.assertIsNone(tracker._rich_live)
        self.assertIsNone(tracker._console)

    def test_fallback_mode_update(self):
        """Test that update() works when Rich is unavailable."""
        from src.binary_sbom.progress_tracker import ProgressTracker, StageState

        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=True,
        )

        tracker.start()

        # Should not raise exception
        tracker.update(
            stage_id=1,
            state=StageState.ACTIVE,
        )

        tracker.update(
            stage_id=1,
            state=StageState.COMPLETE,
            progress=100,
            result="Test complete",
        )

    def test_fallback_mode_complete(self):
        """Test that complete() works when Rich is unavailable."""
        from src.binary_sbom.progress_tracker import ProgressTracker

        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=True,
        )

        tracker.start()

        # Should not raise exception
        tracker.complete()

    def test_fallback_mode_silent(self):
        """Test that silent mode works when Rich is unavailable."""
        from src.binary_sbom.progress_tracker import ProgressTracker

        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=False,  # Silent mode
        )

        # Should not raise exception
        tracker.start()
        tracker.complete()

    def test_fallback_mode_state_tracking(self):
        """Test that state is tracked even when Rich is unavailable."""
        from src.binary_sbom.progress_tracker import ProgressTracker, StageState

        tracker = ProgressTracker(
            filename="test.bin",
            file_size_bytes=1024 * 1024,
            verbose=True,
        )

        tracker.start()

        # Update some stages
        tracker.update(
            stage_id=1,
            state=StageState.ACTIVE,
        )
        tracker.update(
            stage_id=1,
            state=StageState.COMPLETE,
        )

        # State should still be tracked
        state = tracker.get_state()
        self.assertEqual(state.stages[0].state, StageState.COMPLETE)


class TestWithRich(unittest.TestCase):
    """Test that Rich mode still works when Rich is available."""

    def test_rich_mode_initialization(self):
        """Test that ProgressTracker uses Rich when available."""
        from src.binary_sbom.progress_tracker import ProgressTracker, RICH_AVAILABLE

        # If Rich is actually installed, test with it
        if RICH_AVAILABLE:
            tracker = ProgressTracker(
                filename="test.bin",
                file_size_bytes=1024 * 1024,
                verbose=True,
            )

            # Tracker should know Rich is available
            self.assertTrue(tracker._rich_available)


if __name__ == "__main__":
    unittest.main()
