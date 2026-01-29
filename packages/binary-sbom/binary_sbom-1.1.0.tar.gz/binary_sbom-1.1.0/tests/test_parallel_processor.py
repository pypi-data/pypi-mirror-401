"""
Integration tests for parallel processor.

These tests verify that the ParallelProcessor correctly integrates with
ProcessPoolExecutor and other components to provide concurrent binary
analysis with proper error handling, result aggregation, and progress tracking.

This test file focuses on:
- Verifying ProcessPoolExecutor integration
- Testing work distribution and result aggregation
- Error handling and propagation
- Progress tracking functionality
- ETA estimation integration
- Retry logic
- Configuration management
"""

import time
import unittest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, call
from typing import Dict, Any, List

from binary_sbom.parallel_processor import (
    ParallelProcessor,
    ParallelResult,
    AggregatedResults,
    ParallelConfig,
    DEFAULT_MAX_WORKERS,
    DEFAULT_TIMEOUT_SECONDS,
)


class MockProcessFunc:
    """Mock processing function for testing."""

    def __init__(self, results: List[Dict[str, Any]] = None):
        """Initialize with optional results list."""
        self.results = results or []
        self.call_count = 0
        self.called_with = []

    def __call__(self, file_path: str) -> Dict[str, Any]:
        """Mock process function that returns predefined results."""
        self.call_count += 1
        self.called_with.append(file_path)

        if self.results:
            # Return result based on call count (cycle through results)
            result = self.results[(self.call_count - 1) % len(self.results)]
            if isinstance(result, Exception):
                raise result
            return result

        # Default result
        return {
            "name": Path(file_path).name,
            "type": "ELF",
            "architecture": "x86_64",
            "file_path": file_path,
        }


def mock_process_func_success(file_path: str) -> Dict[str, Any]:
    """Mock process function that always succeeds."""
    return {
        "name": Path(file_path).name,
        "type": "ELF",
        "architecture": "x86_64",
        "file_path": file_path,
    }


def mock_process_func_error(file_path: str) -> Dict[str, Any]:
    """Mock process function that always fails."""
    raise FileNotFoundError(f"File not found: {file_path}")


class TestParallelProcessorInitialization(unittest.TestCase):
    """Test ParallelProcessor initialization and configuration."""

    def test_init_with_defaults(self):
        """Test initialization with default parameters."""
        processor = ParallelProcessor()

        self.assertIsNotNone(processor.max_workers)
        self.assertGreater(processor.max_workers, 0)
        self.assertEqual(processor.config.timeout_seconds, DEFAULT_TIMEOUT_SECONDS)
        self.assertTrue(processor.config.enable_eta_estimation)
        self.assertIsNotNone(processor.eta_estimator)

    def test_init_with_custom_workers(self):
        """Test initialization with custom worker count."""
        processor = ParallelProcessor(max_workers=4)

        self.assertEqual(processor.max_workers, 4)
        self.assertEqual(processor.config.max_workers, 4)

    def test_init_with_custom_timeout(self):
        """Test initialization with custom timeout."""
        processor = ParallelProcessor(timeout_seconds=180)

        self.assertEqual(processor.config.timeout_seconds, 180)

    def test_init_with_config_object(self):
        """Test initialization with ParallelConfig object."""
        config = ParallelConfig(max_workers=6, timeout_seconds=240)
        processor = ParallelProcessor(config=config)

        self.assertEqual(processor.max_workers, 6)
        self.assertEqual(processor.config.timeout_seconds, 240)

    def test_init_config_overrides(self):
        """Test that explicit parameters override config values."""
        config = ParallelConfig(max_workers=2, timeout_seconds=60)
        processor = ParallelProcessor(config=config, max_workers=8)

        # Explicit parameter should override config
        self.assertEqual(processor.max_workers, 8)

    def test_init_eta_estimation_disabled(self):
        """Test initialization with ETA estimation disabled."""
        processor = ParallelProcessor(enable_eta_estimation=False)

        self.assertFalse(processor.config.enable_eta_estimation)
        self.assertIsNone(processor.eta_estimator)

    def test_init_invalid_workers(self):
        """Test that invalid worker count raises ValueError."""
        with self.assertRaises(ValueError) as context:
            ParallelConfig(max_workers=0)

        self.assertIn("max_workers must be positive", str(context.exception))

    def test_init_invalid_timeout(self):
        """Test that invalid timeout raises ValueError."""
        with self.assertRaises(ValueError) as context:
            ParallelConfig(timeout_seconds=-1)

        self.assertIn("timeout_seconds must be positive", str(context.exception))

    def test_effective_workers_auto_detect(self):
        """Test that effective_workers auto-detects CPU count."""
        config = ParallelConfig(max_workers=None)
        effective = config.effective_workers

        # Should be capped at 8
        self.assertGreater(effective, 0)
        self.assertLessEqual(effective, 8)

    def test_repr(self):
        """Test string representation of processor."""
        processor = ParallelProcessor(max_workers=4, timeout_seconds=120)
        repr_str = repr(processor)

        self.assertIn("ParallelProcessor", repr_str)
        self.assertIn("workers=4", repr_str)
        self.assertIn("timeout=120s", repr_str)


class TestProcessFiles(unittest.TestCase):
    """Test the process_files method."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_files = ["/path/binary1", "/path/binary2", "/path/binary3"]
        self.processor = ParallelProcessor(max_workers=2)

    @patch("binary_sbom.parallel_processor.ProcessPoolExecutor")
    def test_process_files_all_success(self, mock_executor_class):
        """Test successful parallel processing of all files."""
        # Mock ProcessPoolExecutor
        mock_executor = MagicMock()
        mock_executor_class.return_value.__enter__.return_value = mock_executor

        # Mock futures that complete immediately with results
        mock_future1 = MagicMock()
        mock_future1.result.return_value = {"name": "binary1", "type": "ELF"}

        mock_future2 = MagicMock()
        mock_future2.result.return_value = {"name": "binary2", "type": "PE"}

        mock_future3 = MagicMock()
        mock_future3.result.return_value = {"name": "binary3", "type": "MachO"}

        mock_executor.submit.side_effect = [mock_future1, mock_future2, mock_future3]

        # Mock as_completed to return futures in order
        with patch("binary_sbom.parallel_processor.as_completed") as mock_as_completed:
            mock_as_completed.return_value = [mock_future1, mock_future2, mock_future3]

            # Process files
            results = self.processor.process_files(self.test_files, mock_process_func_success)

            # Verify results
            self.assertEqual(len(results), 3)
            self.assertTrue(all(r.success for r in results))
            self.assertEqual(results[0].result["name"], "binary1")
            self.assertEqual(results[1].result["name"], "binary2")
            self.assertEqual(results[2].result["name"], "binary3")

    @patch("binary_sbom.parallel_processor.ProcessPoolExecutor")
    def test_process_files_partial_failure(self, mock_executor_class):
        """Test processing with some failures."""
        mock_executor = MagicMock()
        mock_executor_class.return_value.__enter__.return_value = mock_executor

        # Mock futures: success, error, success
        mock_future1 = MagicMock()
        mock_future1.result.return_value = {"name": "binary1", "type": "ELF"}

        mock_future2 = MagicMock()
        mock_future2.result.side_effect = FileNotFoundError("File not found")

        mock_future3 = MagicMock()
        mock_future3.result.return_value = {"name": "binary3", "type": "PE"}

        mock_executor.submit.side_effect = [mock_future1, mock_future2, mock_future3]

        with patch("binary_sbom.parallel_processor.as_completed") as mock_as_completed:
            mock_as_completed.return_value = [mock_future1, mock_future2, mock_future3]

            results = self.processor.process_files(self.test_files, mock_process_func_success)

            # Verify mixed results
            self.assertEqual(len(results), 3)
            self.assertTrue(results[0].success)
            self.assertFalse(results[1].success)
            self.assertTrue(results[2].success)
            self.assertIn("FileNotFoundError", results[1].error)

    @patch("binary_sbom.parallel_processor.ProcessPoolExecutor")
    def test_process_files_empty_list(self, mock_executor_class):
        """Test processing with empty file list."""
        results = self.processor.process_files([], mock_process_func_success)

        self.assertEqual(len(results), 0)
        # Should not create executor
        mock_executor_class.assert_not_called()

    def test_process_files_no_process_func(self):
        """Test that missing process_func raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.processor.process_files(self.test_files, None)

        self.assertIn("process_func must be provided", str(context.exception))

    @patch("binary_sbom.parallel_processor.ProcessPoolExecutor")
    def test_process_files_custom_timeout(self, mock_executor_class):
        """Test processing with custom timeout override."""
        mock_executor = MagicMock()
        mock_executor_class.return_value.__enter__.return_value = mock_executor

        mock_future = MagicMock()
        mock_future.result.return_value = {"name": "test", "type": "ELF"}
        mock_executor.submit.return_value = mock_future

        with patch("binary_sbom.parallel_processor.as_completed") as mock_as_completed:
            mock_as_completed.return_value = [mock_future]

            # Process with custom timeout
            self.processor.process_files(
                [self.test_files[0]], mock_process_func_success, timeout=180
            )

            # Verify timeout was passed to as_completed
            mock_as_completed.assert_called_once()
            call_kwargs = mock_as_completed.call_args[1]
            self.assertEqual(call_kwargs.get("timeout"), 180)


class TestProcessFilesWithProgress(unittest.TestCase):
    """Test the process_files_with_progress method."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_files = ["/path/binary1", "/path/binary2", "/path/binary3"]
        self.processor = ParallelProcessor(max_workers=2)

    @patch("binary_sbom.parallel_processor.ProcessPoolExecutor")
    def test_progress_callback_invoked(self, mock_executor_class):
        """Test that progress callback is invoked for each completion."""
        mock_executor = MagicMock()
        mock_executor_class.return_value.__enter__.return_value = mock_executor

        # Mock successful futures
        mock_futures = []
        for i in range(3):
            mock_future = MagicMock()
            mock_future.result.return_value = {"name": f"binary{i+1}", "type": "ELF"}
            mock_futures.append(mock_future)

        mock_executor.submit.side_effect = mock_futures

        with patch("binary_sbom.parallel_processor.as_completed") as mock_as_completed:
            mock_as_completed.return_value = mock_futures

            # Track progress callback invocations
            progress_updates = []

            def progress_callback(completed, total):
                progress_updates.append((completed, total))

            results = self.processor.process_files_with_progress(
                self.test_files, mock_process_func_success, progress_callback=progress_callback
            )

            # Verify callback was called
            self.assertEqual(len(progress_updates), 3)
            self.assertEqual(progress_updates[0], (1, 3))
            self.assertEqual(progress_updates[1], (2, 3))
            self.assertEqual(progress_updates[2], (3, 3))

            # Verify results
            self.assertEqual(len(results), 3)
            self.assertTrue(all(r.success for r in results))

    @patch("binary_sbom.parallel_processor.ProcessPoolExecutor")
    def test_progress_callback_error_handling(self, mock_executor_class):
        """Test that errors in progress callback don't stop processing."""
        mock_executor = MagicMock()
        mock_executor_class.return_value.__enter__.return_value = mock_executor

        mock_futures = []
        for i in range(3):
            mock_future = MagicMock()
            mock_future.result.return_value = {"name": f"binary{i+1}", "type": "ELF"}
            mock_futures.append(mock_future)

        mock_executor.submit.side_effect = mock_futures

        with patch("binary_sbom.parallel_processor.as_completed") as mock_as_completed:
            mock_as_completed.return_value = mock_futures

            # Callback that raises error
            def failing_callback(completed, total):
                if completed == 2:
                    raise ValueError("Callback error")

            results = self.processor.process_files_with_progress(
                self.test_files, mock_process_func_success, progress_callback=failing_callback
            )

            # Should still complete all files despite callback error
            self.assertEqual(len(results), 3)


class TestProcessFilesWithAggregation(unittest.TestCase):
    """Test the process_files_with_aggregation method."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_files = ["/path/binary1", "/path/binary2", "/path/binary3"]
        self.processor = ParallelProcessor(max_workers=2)

    @patch("binary_sbom.parallel_processor.ProcessPoolExecutor")
    @patch("binary_sbom.parallel_processor.time.time")
    def test_aggregation_statistics(self, mock_time, mock_executor_class):
        """Test that aggregation calculates correct statistics."""
        mock_executor = MagicMock()
        mock_executor_class.return_value.__enter__.return_value = mock_executor

        # Mock time to simulate 2 second processing time
        mock_time.side_effect = [0.0, 2.0]

        mock_futures = []
        for i in range(3):
            mock_future = MagicMock()
            mock_future.result.return_value = {"name": f"binary{i+1}", "type": "ELF"}
            mock_futures.append(mock_future)

        mock_executor.submit.side_effect = mock_futures

        with patch("binary_sbom.parallel_processor.as_completed") as mock_as_completed:
            mock_as_completed.return_value = mock_futures

            # Mock process_files to return results with timing
            with patch.object(
                self.processor, "process_files", wraps=self.processor.process_files
            ) as mock_process:
                # Return mock results
                mock_results = [
                    ParallelResult(
                        file_path=f, success=True, result={"name": Path(f).name}, processing_time_seconds=1.0
                    )
                    for f in self.test_files
                ]
                mock_process.return_value = mock_results

                agg_results = self.processor.process_files_with_aggregation(
                    self.test_files, mock_process_func_success
                )

                # Verify aggregation
                self.assertIsInstance(agg_results, AggregatedResults)
                self.assertEqual(agg_results.total_files, 3)
                self.assertEqual(agg_results.successful_count, 3)
                self.assertEqual(agg_results.failed_count, 0)
                self.assertEqual(len(agg_results.results), 3)
                self.assertEqual(agg_results.total_time_seconds, 2.0)

    def test_aggregation_empty_list(self):
        """Test aggregation with empty file list."""
        agg_results = self.processor.process_files_with_aggregation([], mock_process_func_success)

        self.assertEqual(agg_results.total_files, 0)
        self.assertEqual(agg_results.successful_count, 0)
        self.assertEqual(agg_results.failed_count, 0)

    def test_get_successful_results(self):
        """Test filtering successful results from aggregation."""
        results = [
            ParallelResult(file_path="a", success=True, result={"name": "a"}),
            ParallelResult(file_path="b", success=False, error="Error"),
            ParallelResult(file_path="c", success=True, result={"name": "c"}),
        ]

        agg = AggregatedResults(
            total_files=3, successful_count=2, failed_count=1, results=results
        )

        successful = agg.get_successful_results()
        failed = agg.get_failed_results()

        self.assertEqual(len(successful), 2)
        self.assertEqual(len(failed), 1)
        self.assertEqual(successful[0].file_path, "a")
        self.assertEqual(failed[0].file_path, "b")

    def test_aggregation_to_dict(self):
        """Test AggregatedResults serialization."""
        results = [
            ParallelResult(file_path="a", success=True, result={"name": "a"}),
            ParallelResult(file_path="b", success=False, error="Error"),
        ]

        agg = AggregatedResults(
            total_files=2,
            successful_count=1,
            failed_count=1,
            results=results,
            total_time_seconds=5.0,
            average_time_seconds=2.5,
        )

        agg_dict = agg.to_dict()

        self.assertEqual(agg_dict["total_files"], 2)
        self.assertEqual(agg_dict["successful_count"], 1)
        self.assertEqual(agg_dict["failed_count"], 1)
        self.assertEqual(agg_dict["total_time_seconds"], 5.0)
        self.assertIn("success_rate", agg_dict)
        self.assertEqual(agg_dict["success_rate"], 0.5)


class TestProcessFilesWithRetry(unittest.TestCase):
    """Test the process_files_with_retry method."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_files = ["/path/binary1", "/path/binary2", "/path/binary3"]
        self.processor = ParallelProcessor(max_workers=2)

    @patch("binary_sbom.parallel_processor.ProcessPoolExecutor")
    def test_retry_on_failure(self, mock_executor_class):
        """Test that failed tasks are retried."""
        mock_executor = MagicMock()
        mock_executor_class.return_value.__enter__.return_value = mock_executor

        # Use a simple approach: patch process_files to control behavior
        attempt_count = [0]

        def mock_process_files_impl(file_paths, process_func, timeout=None):
            attempt_count[0] += 1
            results = []

            for i, file_path in enumerate(file_paths):
                if attempt_count[0] == 1:  # First attempt
                    # First succeeds, rest fail
                    if i == 0:
                        results.append(
                            ParallelResult(
                                file_path=file_path, success=True, result={"name": "binary1"}
                            )
                        )
                    else:
                        results.append(
                            ParallelResult(
                                file_path=file_path, success=False, error="FileNotFoundError"
                            )
                        )
                else:  # Retry attempt - all succeed
                    results.append(
                        ParallelResult(
                            file_path=file_path, success=True, result={"name": Path(file_path).name}
                        )
                    )

            return results

        with patch.object(
            self.processor, "process_files", side_effect=mock_process_files_impl
        ):
            results = self.processor.process_files_with_retry(
                self.test_files, mock_process_func_success, max_retries=2
            )

            # All should succeed after retry
            self.assertEqual(len(results), 3)
            self.assertTrue(all(r.success for r in results))

            # Check that retry happened
            self.assertEqual(attempt_count[0], 2)  # Initial + 1 retry

            # At least the failed ones should have retry_count > 0
            retried = [r for r in results if r.retry_count > 0]
            self.assertGreater(len(retried), 0)

    def test_retry_empty_list(self):
        """Test retry with empty file list."""
        results = self.processor.process_files_with_retry([], mock_process_func_success)

        self.assertEqual(len(results), 0)


class TestAggregateResults(unittest.TestCase):
    """Test the aggregate_results method."""

    def test_aggregate_results(self):
        """Test result aggregation from list of ParallelResult."""
        processor = ParallelProcessor()

        results = [
            ParallelResult(
                file_path="/path/a",
                success=True,
                result={"name": "a"},
                processing_time_seconds=1.5,
            ),
            ParallelResult(
                file_path="/path/b",
                success=True,
                result={"name": "b"},
                processing_time_seconds=2.5,
            ),
            ParallelResult(
                file_path="/path/c",
                success=False,
                error="Error",
                processing_time_seconds=0.0,
            ),
        ]

        aggregated = processor.aggregate_results(results)

        self.assertEqual(aggregated.total_files, 3)
        self.assertEqual(aggregated.successful_count, 2)
        self.assertEqual(aggregated.failed_count, 1)
        self.assertAlmostEqual(aggregated.average_time_seconds, 2.0)
        self.assertEqual(aggregated.min_time_seconds, 1.5)
        self.assertEqual(aggregated.max_time_seconds, 2.5)

    def test_aggregate_empty_results(self):
        """Test aggregation with empty result list."""
        processor = ParallelProcessor()
        aggregated = processor.aggregate_results([])

        self.assertEqual(aggregated.total_files, 0)
        self.assertEqual(aggregated.successful_count, 0)
        self.assertEqual(aggregated.failed_count, 0)


class TestETAEIntegration(unittest.TestCase):
    """Test ETA estimation integration."""

    def setUp(self):
        """Set up test fixtures."""
        self.processor = ParallelProcessor(max_workers=2, enable_eta_estimation=True)

    @patch("binary_sbom.parallel_processor.Path")
    def test_estimate_total_time(self, mock_path):
        """Test total time estimation for multiple files."""
        # Create a real ETA estimator and record some data
        self.processor.eta_estimator.record_processing(1000000, 1.0)
        self.processor.eta_estimator.record_processing(2000000, 2.0)

        # Mock file sizes
        mock_stat1 = MagicMock()
        mock_stat1.st_size = 1000000  # 1MB

        mock_stat2 = MagicMock()
        mock_stat2.st_size = 2000000  # 2MB

        mock_path_instance1 = MagicMock()
        mock_path_instance1.stat.return_value = mock_stat1

        mock_path_instance2 = MagicMock()
        mock_path_instance2.stat.return_value = mock_stat2

        mock_path.side_effect = [mock_path_instance1, mock_path_instance2]

        file_paths = ["/path/file1", "/path/file2"]
        estimated = self.processor.estimate_total_time(file_paths)

        # Should estimate and adjust for parallelism
        self.assertIsNotNone(estimated)
        self.assertGreater(estimated, 0)

    def test_estimate_total_time_no_estimator(self):
        """Test estimation when ETA estimator is disabled."""
        processor = ParallelProcessor(enable_eta_estimation=False)

        estimated = processor.estimate_total_time(["/path/file1"])

        self.assertIsNone(estimated)

    def test_estimate_total_time_empty_list(self):
        """Test estimation with empty file list."""
        estimated = self.processor.estimate_total_time([])

        self.assertIsNone(estimated)


class TestWorkQueueStatus(unittest.TestCase):
    """Test work queue status reporting."""

    def setUp(self):
        """Set up test fixtures."""
        config = ParallelConfig(max_workers=4, chunk_size=2)
        self.processor = ParallelProcessor(config=config)

    def test_get_work_queue_status(self):
        """Test getting work queue status."""
        file_paths = ["/path/file1", "/path/file2", "/path/file3", "/path/file4", "/path/file5"]

        status = self.processor.get_work_queue_status(file_paths)

        self.assertEqual(status["total_files"], 5)
        self.assertEqual(status["workers"], 4)
        self.assertEqual(status["chunk_size"], 2)
        self.assertIsInstance(status["num_chunks"], int)
        self.assertIn("config", status)

    def test_create_work_chunks(self):
        """Test work chunk creation."""
        file_paths = [f"/path/file{i}" for i in range(10)]

        # Chunk size of 3
        chunks = self.processor._create_work_chunks(file_paths, chunk_size=3)

        self.assertEqual(len(chunks), 4)  # 10 files / 3 = 4 chunks (last has 1)
        self.assertEqual(len(chunks[0]), 3)
        self.assertEqual(len(chunks[3]), 1)

    def test_create_work_chunks_no_chunking(self):
        """Test chunking with chunk_size=1."""
        file_paths = ["/path/a", "/path/b", "/path/c"]

        chunks = self.processor._create_work_chunks(file_paths, chunk_size=1)

        # Each file should be its own chunk
        self.assertEqual(len(chunks), 3)
        self.assertEqual(len(chunks[0]), 1)


class TestParallelResult(unittest.TestCase):
    """Test ParallelResult dataclass."""

    def test_parallel_result_creation(self):
        """Test creating ParallelResult."""
        result = ParallelResult(
            file_path="/path/test",
            success=True,
            result={"name": "test"},
            processing_time_seconds=1.5,
            worker_id=2,
            retry_count=1,
        )

        self.assertEqual(result.file_path, "/path/test")
        self.assertTrue(result.success)
        self.assertEqual(result.processing_time_seconds, 1.5)
        self.assertEqual(result.worker_id, 2)
        self.assertEqual(result.retry_count, 1)

    def test_parallel_result_to_dict(self):
        """Test ParallelResult serialization."""
        result = ParallelResult(
            file_path="/path/test",
            success=True,
            result={"name": "test"},
            error=None,
            processing_time_seconds=1.0,
        )

        result_dict = result.to_dict()

        self.assertEqual(result_dict["file_path"], "/path/test")
        self.assertTrue(result_dict["success"])
        self.assertEqual(result_dict["result"], {"name": "test"})
        self.assertIsNone(result_dict["error"])


class TestConfigurationMethods(unittest.TestCase):
    """Test configuration and getter methods."""

    def test_get_config(self):
        """Test getting processor configuration."""
        processor = ParallelProcessor(max_workers=4, timeout_seconds=180)

        config = processor.get_config()

        self.assertEqual(config["max_workers"], 4)
        self.assertEqual(config["timeout_seconds"], 180)
        self.assertIn("effective_workers", config)
        self.assertIn("enable_eta_estimation", config)

    def test_get_eta_estimator(self):
        """Test getting ETA estimator instance."""
        processor = ParallelProcessor(enable_eta_estimation=True)
        estimator = processor.get_eta_estimator()

        self.assertIsNotNone(estimator)

    def test_get_eta_estimator_disabled(self):
        """Test getting ETA estimator when disabled."""
        processor = ParallelProcessor(enable_eta_estimation=False)
        estimator = processor.get_eta_estimator()

        self.assertIsNone(estimator)


if __name__ == "__main__":
    unittest.main()
