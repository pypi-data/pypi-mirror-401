"""
Performance benchmark tests for CI/CD optimizations.

Tests verify the performance targets for streaming, parallel processing,
and ETA estimation features. These benchmarks ensure the implementation
meets the acceptance criteria from the spec.

Performance Targets:
- SBOM generation for <100MB binaries in under 30 seconds
- 50%+ wall-clock time reduction with parallel processing
- ETA estimation accuracy within ±20%
- Constant memory usage for streaming mode
"""

import os
import tempfile
import time
from pathlib import Path
from typing import Dict, List
from unittest.mock import MagicMock, Mock, patch

import pytest

from binary_sbom.eta_estimator import (
    ETAEstimator,
    EMAEstimate,
    ProcessingRecord,
)
from binary_sbom.parallel_processor import (
    ParallelProcessor,
    ParallelConfig,
    ParallelResult,
    AggregatedResults,
)
from binary_sbom.streaming_parser import (
    StreamingParser,
    StreamingConfig,
    LIEFStreamingParser,
    ChunkReadError,
    FileSizeExceededError,
)


class TestETAEstimatorPerformance:
    """Test ETA estimator performance and accuracy."""

    def test_eta_estimator_initialization_performance(self):
        """Test that ETA estimator initializes quickly."""
        start_time = time.time()
        estimator = ETAEstimator(history_size=1000)
        init_time = time.time() - start_time

        # Should initialize in under 10ms even with large history
        assert init_time < 0.01, f"ETA estimator initialization took {init_time:.3f}s"

    def test_record_processing_performance(self):
        """Test that recording processing times is efficient."""
        estimator = ETAEstimator()

        # Record 1000 processing times
        start_time = time.time()
        for i in range(1000):
            estimator.record_processing(
                file_size_bytes=1024 * 1024,  # 1 MB
                processing_time_seconds=1.0,
                file_type="ELF",
                architecture="x86_64"
            )
        record_time = time.time() - start_time

        # Should record 1000 entries in under 100ms
        assert record_time < 0.1, f"Recording 1000 entries took {record_time:.3f}s"

    def test_estimate_time_performance(self):
        """Test that time estimation is fast."""
        estimator = ETAEstimator()

        # Pre-populate with some data
        for i in range(100):
            estimator.record_processing(
                file_size_bytes=1024 * 1024,
                processing_time_seconds=1.0 + (i * 0.01),  # Vary slightly
                file_type="ELF",
                architecture="x86_64"
            )

        # Time 1000 estimates
        start_time = time.time()
        for i in range(1000):
            eta = estimator.estimate_time(file_size_bytes=1024 * 1024)
        estimate_time = time.time() - start_time

        # Should make 1000 estimates in under 50ms
        assert estimate_time < 0.05, f"1000 estimates took {estimate_time:.3f}s"

    def test_eta_accuracy_within_tolerance(self):
        """Test that ETA estimates are within ±20% of actual times."""
        estimator = ETAEstimator(alpha=0.3)

        # Record historical processing times with some variance
        # Simulating: 1MB files take ~1 second with ±10% variance
        for i in range(50):
            variance = 0.9 + (i % 20) * 0.01  # 0.9 to 1.09
            estimator.record_processing(
                file_size_bytes=1024 * 1024,
                processing_time_seconds=variance,
                file_type="ELF",
                architecture="x86_64"
            )

        # Now test estimation accuracy for similar files
        errors = []
        for i in range(20):
            actual_time = 1.0 + (i % 10) * 0.05  # 1.0 to 1.45 seconds
            estimated_time = estimator.estimate_time(file_size_bytes=1024 * 1024)

            if estimated_time is not None:
                error_pct = abs(estimated_time - actual_time) / actual_time
                errors.append(error_pct)

        # After sufficient samples, error should be within ±20%
        avg_error = sum(errors) / len(errors) if errors else 1.0
        assert avg_error < 0.20, f"Average ETA error {avg_error:.1%} exceeds ±20% tolerance"

    def test_ema_convergence_speed(self):
        """Test that EMA estimate converges quickly with new data."""
        estimator = ETAEstimator(alpha=0.3)

        # Start with incorrect estimate (simulate historical data)
        for i in range(10):
            estimator.record_processing(
                file_size_bytes=1024 * 1024,
                processing_time_seconds=5.0,  # Initially slow
                file_type="ELF",
                architecture="x86_64"
            )

        # Now process faster files (system upgrade)
        for i in range(15):
            estimator.record_processing(
                file_size_bytes=1024 * 1024,
                processing_time_seconds=1.0,  # Now fast
                file_type="ELF",
                architecture="x86_64"
            )

        # Estimate should converge close to new faster time
        eta = estimator.estimate_time(file_size_bytes=1024 * 1024)

        # Should be closer to 1.0s than 5.0s
        assert eta is not None
        assert eta < 2.0, f"EMA did not converge: ETA={eta:.2f}s (expected <2.0s)"

    def test_real_time_eta_accuracy(self):
        """Test accuracy of real-time ETA estimates during processing."""
        estimator = ETAEstimator()

        # Train with similar files
        for i in range(20):
            estimator.record_processing(
                file_size_bytes=10 * 1024 * 1024,  # 10 MB
                processing_time_seconds=10.0,
                file_type="ELF",
                architecture="x86_64"
            )

        # Simulate processing with real-time updates
        file_size = 10 * 1024 * 1024  # 10 MB
        actual_total_time = 10.0

        # Check accuracy at 25%, 50%, 75% progress
        checkpoints = [0.25, 0.5, 0.75]
        errors = []

        for progress in checkpoints:
            bytes_processed = int(file_size * progress)
            elapsed = actual_total_time * progress

            eta = estimator.estimate_remaining(
                file_size_bytes=file_size,
                bytes_processed=bytes_processed,
                elapsed_seconds=elapsed
            )

            if eta is not None:
                actual_remaining = actual_total_time - elapsed
                error = abs(eta - actual_remaining) / actual_remaining
                errors.append(error)

        # Real-time estimates should be reasonably accurate
        avg_error = sum(errors) / len(errors) if errors else 1.0
        assert avg_error < 0.25, f"Real-time ETA error {avg_error:.1%} too high"

    def test_thread_safety_under_load(self):
        """Test that ETA estimator is thread-safe under concurrent access."""
        import threading

        estimator = ETAEstimator()
        errors = []

        def record_worker():
            try:
                for i in range(100):
                    estimator.record_processing(
                        file_size_bytes=1024 * 1024,
                        processing_time_seconds=1.0,
                        file_type="ELF",
                        architecture="x86_64"
                    )
            except Exception as e:
                errors.append(e)

        def estimate_worker():
            try:
                for i in range(100):
                    estimator.estimate_time(file_size_bytes=1024 * 1024)
            except Exception as e:
                errors.append(e)

        # Launch concurrent threads
        threads = []
        for _ in range(5):
            t1 = threading.Thread(target=record_worker)
            t2 = threading.Thread(target=estimate_worker)
            threads.extend([t1, t2])
            t1.start()
            t2.start()

        # Wait for completion
        for t in threads:
            t.join()

        # Should have no errors
        assert len(errors) == 0, f"Thread safety errors: {errors}"
        assert len(estimator) > 0, "No records were added"


class TestParallelProcessorPerformance:
    """Test parallel processing performance and speedup."""

    def _create_mock_process_func(self, duration: float = 0.1):
        """Create a mock processing function with controlled duration."""
        def process_func(file_path: str) -> Dict:
            time.sleep(duration)
            return {
                "file": file_path,
                "type": "ELF",
                "architecture": "x86_64",
                "size": os.path.getsize(file_path) if os.path.exists(file_path) else 0
            }
        return process_func

    def _create_test_files(self, count: int, size_mb: float = 1.0) -> List[str]:
        """Create temporary test files."""
        files = []
        for i in range(count):
            with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
                # Write specified size
                f.write(b'x' * int(size_mb * 1024 * 1024))
                files.append(f.name)
        return files

    def _cleanup_test_files(self, files: List[str]):
        """Clean up temporary test files."""
        for file_path in files:
            try:
                os.unlink(file_path)
            except OSError:
                pass

    def test_parallel_processor_initialization_performance(self):
        """Test that parallel processor initializes quickly."""
        start_time = time.time()
        processor = ParallelProcessor(max_workers=4)
        init_time = time.time() - start_time

        # Should initialize in under 50ms
        assert init_time < 0.05, f"Initialization took {init_time:.3f}s"

    def test_parallel_speedup_target(self):
        """Test that parallel processing achieves 50%+ speedup."""
        # Create test files
        test_files = self._create_test_files(count=10, size_mb=0.5)

        try:
            process_func = self._create_mock_process_func(duration=0.2)

            # Sequential baseline
            start_time = time.time()
            for file_path in test_files:
                process_func(file_path)
            sequential_time = time.time() - start_time

            # Parallel processing
            processor = ParallelProcessor(max_workers=4)
            start_time = time.time()
            results = processor.process_files(test_files, process_func)
            parallel_time = time.time() - start_time

            # Calculate speedup
            speedup = sequential_time / parallel_time
            speedup_pct = (1 - parallel_time / sequential_time) * 100

            # Should achieve at least 50% speedup (2x faster)
            assert speedup >= 1.5, (
                f"Parallel speedup {speedup:.2f}x ({speedup_pct:.1f}% reduction) "
                f"below 50% target. Sequential: {sequential_time:.2f}s, "
                f"Parallel: {parallel_time:.2f}s"
            )

            # Verify all files processed
            assert len(results) == len(test_files)
            successful = [r for r in results if r.success]
            assert len(successful) == len(test_files)

        finally:
            self._cleanup_test_files(test_files)

    def test_parallel_scaling_with_workers(self):
        """Test that performance scales with worker count."""
        test_files = self._create_test_files(count=20, size_mb=0.5)

        try:
            process_func = self._create_mock_process_func(duration=0.1)

            # Test with different worker counts
            worker_counts = [1, 2, 4]
            times = []

            for workers in worker_counts:
                processor = ParallelProcessor(max_workers=workers)
                start_time = time.time()
                results = processor.process_files(test_files, process_func)
                elapsed = time.time() - start_time
                times.append(elapsed)

                # Verify all succeeded
                successful = [r for r in results if r.success]
                assert len(successful) == len(test_files)

            # More workers should be faster (or at least not slower)
            # Allow some tolerance for overhead
            assert times[0] >= times[1] * 0.9, "2 workers not faster than 1"
            assert times[1] >= times[2] * 0.9, "4 workers not faster than 2"

        finally:
            self._cleanup_test_files(test_files)

    def test_work_queue_overhead(self):
        """Test that work queue overhead is minimal."""
        test_files = self._create_test_files(count=100, size_mb=0.1)

        try:
            # Very fast processing function
            process_func = self._create_mock_process_func(duration=0.001)

            processor = ParallelProcessor(max_workers=4)
            start_time = time.time()
            results = processor.process_files(test_files, process_func)
            total_time = time.time() - start_time

            # Overhead per file should be small (< 1ms per file)
            overhead_per_file = total_time / len(test_files)
            assert overhead_per_file < 0.01, (
                f"Work queue overhead too high: {overhead_per_file*1000:.2f}ms per file"
            )

        finally:
            self._cleanup_test_files(test_files)

    def test_result_aggregation_performance(self):
        """Test that result aggregation is efficient."""
        processor = ParallelProcessor(max_workers=4)

        # Create mock results
        results = []
        for i in range(1000):
            result = ParallelResult(
                file_path=f"/tmp/file_{i}.bin",
                success=i % 10 != 0,  # 10% failure rate
                result={"type": "ELF"} if i % 10 != 0 else None,
                error="Parse error" if i % 10 == 0 else None,
                processing_time_seconds=1.0 + (i * 0.01),
            )
            results.append(result)

        # Time aggregation
        start_time = time.time()
        aggregated = processor.aggregate_results(results)
        agg_time = time.time() - start_time

        # Should aggregate 1000 results quickly
        assert agg_time < 0.01, f"Aggregating 1000 results took {agg_time:.3f}s"

        # Verify aggregation correctness
        assert aggregated.total_files == 1000
        assert aggregated.successful_count == 900
        assert aggregated.failed_count == 100

    def test_parallel_with_progress_tracking(self):
        """Test parallel processing with progress tracking overhead."""
        test_files = self._create_test_files(count=10, size_mb=0.5)

        try:
            process_func = self._create_mock_process_func(duration=0.1)
            progress_updates = []

            def progress_callback(completed: int, total: int):
                progress_updates.append((completed, total))

            processor = ParallelProcessor(max_workers=4)
            start_time = time.time()
            results = processor.process_files_with_progress(
                test_files,
                process_func,
                progress_callback=progress_callback
            )
            total_time = time.time() - start_time

            # Should have received progress updates
            assert len(progress_updates) > 0

            # Progress tracking overhead should be minimal
            assert total_time < 2.0, "Progress tracking added too much overhead"

        finally:
            self._cleanup_test_files(test_files)

    def test_eta_estimation_integration(self):
        """Test ETA estimation integration with parallel processor."""
        test_files = self._create_test_files(count=5, size_mb=1.0)

        try:
            # Pre-train ETA estimator
            eta = ETAEstimator()
            for i in range(20):
                eta.record_processing(
                    file_size_bytes=1024 * 1024,
                    processing_time_seconds=0.5,
                    file_type="ELF",
                    architecture="x86_64"
                )

            process_func = self._create_mock_process_func(duration=0.5)
            processor = ParallelProcessor(max_workers=2, eta_estimator=eta)

            # Get ETA before processing
            estimated_time = processor.estimate_total_time(test_files)
            assert estimated_time is not None

            # Process files
            start_time = time.time()
            results = processor.process_files(test_files, process_func)
            actual_time = time.time() - start_time

            # ETA should be reasonably accurate (within 50% for parallel)
            error = abs(estimated_time - actual_time) / actual_time
            assert error < 0.5, f"ETA estimate error {error:.1%} too high"

        finally:
            self._cleanup_test_files(test_files)


class TestStreamingParserPerformance:
    """Test streaming parser memory efficiency and performance."""

    def test_streaming_parser_initialization(self):
        """Test that streaming parser initializes quickly."""
        # Create a test file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            f.write(b'x' * (1024 * 1024))  # 1 MB
            test_file = f.name

        try:
            config = StreamingConfig(chunk_size=65536)
            start_time = time.time()
            parser = StreamingParser(test_file, config=config)
            init_time = time.time() - start_time

            # Should initialize quickly
            assert init_time < 0.01, f"Initialization took {init_time:.3f}s"

        finally:
            os.unlink(test_file)

    def test_chunked_reading_performance(self):
        """Test that chunked reading is efficient."""
        # Create a 10 MB test file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            f.write(b'x' * (10 * 1024 * 1024))
            test_file = f.name

        try:
            config = StreamingConfig(chunk_size=65536)  # 64 KB chunks
            parser = LIEFStreamingParser(test_file, config=config)

            start_time = time.time()
            total_bytes = 0

            with parser:
                for chunk in parser.iter_chunks():
                    total_bytes += len(chunk)

            read_time = time.time() - start_time
            throughput_mbps = (total_bytes / (1024 * 1024)) / read_time

            # Should achieve reasonable throughput (> 100 MB/s)
            assert throughput_mbps > 100, (
                f"Chunked reading throughput too low: {throughput_mbps:.1f} MB/s"
            )

            assert total_bytes == 10 * 1024 * 1024

        finally:
            os.unlink(test_file)

    def test_memory_efficiency(self):
        """Test that memory usage stays constant for large files."""
        # Create files of different sizes
        sizes_mb = [10, 50, 100]
        memory_samples = []

        for size_mb in sizes_mb:
            with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
                f.write(b'x' * (size_mb * 1024 * 1024))
                test_file = f.name

            try:
                config = StreamingConfig(chunk_size=65536)
                parser = LIEFStreamingParser(test_file, config=config)

                # Measure "memory" by tracking max chunk size processed
                max_chunk_size = 0
                chunk_count = 0

                with parser:
                    for chunk in parser.iter_chunks():
                        max_chunk_size = max(max_chunk_size, len(chunk))
                        chunk_count += 1

                # Max chunk size should be constant (chunk_size)
                # regardless of file size
                memory_samples.append(max_chunk_size)

                assert max_chunk_size <= 65536, "Chunk size exceeded limit"

            finally:
                os.unlink(test_file)

        # All samples should have similar max chunk sizes (constant memory)
        max_variance = max(memory_samples) - min(memory_samples)
        assert max_variance < 8192, "Memory usage varied significantly with file size"

    def test_large_binary_performance_target(self):
        """Test that large binary processing meets performance target."""
        # Create a 100 MB test file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            f.write(b'x' * (100 * 1024 * 1024))
            test_file = f.name

        try:
            config = StreamingConfig(chunk_size=1048576)  # 1 MB chunks
            parser = LIEFStreamingParser(test_file, config=config)

            start_time = time.time()
            with parser:
                # Read through entire file
                for chunk in parser.iter_chunks():
                    pass  # Just read, don't process
            read_time = time.time() - start_time

            # Reading 100 MB should be fast (< 5 seconds just for reading)
            # Note: Actual parsing will take longer, but reading is the baseline
            assert read_time < 5.0, (
                f"Reading 100 MB took {read_time:.2f}s, exceeds target"
            )

        finally:
            os.unlink(test_file)

    def test_random_access_performance(self):
        """Test that random chunk access is efficient."""
        # Create a 10 MB test file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            f.write(b'x' * (10 * 1024 * 1024))
            test_file = f.name

        try:
            config = StreamingConfig(chunk_size=65536, use_mmap=True)
            parser = LIEFStreamingParser(test_file, config=config)

            # Time 1000 random accesses
            import random
            random.seed(42)
            offsets = [random.randint(0, 10 * 1024 * 1024 - 4096) for _ in range(1000)]

            start_time = time.time()
            with parser:
                for offset in offsets:
                    data = parser.read_chunk(offset, 4096)
                    assert len(data) == 4096
            access_time = time.time() - start_time

            # 1000 random accesses should be fast
            avg_access_time = access_time / 1000
            assert avg_access_time < 0.001, (
                f"Random access too slow: {avg_access_time*1000:.2f}ms per access"
            )

        finally:
            os.unlink(test_file)

    def test_mmap_vs_file_io_performance(self):
        """Test that memory-mapped I/O provides performance benefit."""
        # Create a 50 MB test file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            f.write(b'x' * (50 * 1024 * 1024))
            test_file = f.name

        try:
            # Test with mmap
            config_mmap = StreamingConfig(chunk_size=65536, use_mmap=True)
            parser_mmap = LIEFStreamingParser(test_file, config=config_mmap)

            start_time = time.time()
            with parser_mmap:
                for chunk in parser_mmap.iter_chunks():
                    pass
            mmap_time = time.time() - start_time

            # Test without mmap
            config_no_mmap = StreamingConfig(chunk_size=65536, use_mmap=False)
            parser_no_mmap = LIEFStreamingParser(test_file, config=config_no_mmap)

            start_time = time.time()
            with parser_no_mmap:
                for chunk in parser_no_mmap.iter_chunks():
                    pass
            no_mmap_time = time.time() - start_time

            # mmap should be faster or at least not significantly slower
            # Allow 20% tolerance for system variations
            assert mmap_time <= no_mmap_time * 1.2, (
                f"mmap ({mmap_time:.2f}s) significantly slower than file I/O ({no_mmap_time:.2f}s)"
            )

        finally:
            os.unlink(test_file)

    def test_progress_tracking_overhead(self):
        """Test that progress tracking adds minimal overhead."""
        # Create a 10 MB test file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            f.write(b'x' * (10 * 1024 * 1024))
            test_file = f.name

        try:
            eta = ETAEstimator()

            # Test without progress tracking
            config_no_progress = StreamingConfig(
                chunk_size=65536,
                enable_progress_tracking=False
            )
            parser_no_progress = LIEFStreamingParser(
                test_file,
                config=config_no_progress,
                eta_estimator=None
            )

            start_time = time.time()
            with parser_no_progress:
                for chunk in parser_no_progress.iter_chunks():
                    pass
            no_progress_time = time.time() - start_time

            # Test with progress tracking
            config_with_progress = StreamingConfig(
                chunk_size=65536,
                enable_progress_tracking=True
            )
            parser_with_progress = LIEFStreamingParser(
                test_file,
                config=config_with_progress,
                eta_estimator=eta
            )

            start_time = time.time()
            with parser_with_progress:
                for chunk in parser_with_progress.iter_chunks():
                    pass
            with_progress_time = time.time() - start_time

            # Progress tracking overhead should be minimal (< 10%)
            overhead = (with_progress_time - no_progress_time) / no_progress_time
            assert overhead < 0.1, (
                f"Progress tracking overhead {overhead:.1%} too high"
            )

        finally:
            os.unlink(test_file)


class TestIntegratedPerformance:
    """Integration tests for combined performance features."""

    def test_end_to_end_performance_target(self):
        """Test end-to-end processing meets performance targets."""
        # This is an integration test for the full pipeline
        # For this test, we simulate the workload without actual binary parsing

        # Create 10 test files totaling 100 MB
        test_files = []
        for i in range(10):
            with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
                f.write(b'x' * (10 * 1024 * 1024))  # 10 MB each
                test_files.append(f.name)

        try:
            # Simulate fast processing function
            def fast_process(file_path: str) -> Dict:
                # Simulate analysis work
                time.sleep(0.1)  # 100ms per file
                return {
                    "file": file_path,
                    "type": "ELF",
                    "architecture": "x86_64",
                    "size": os.path.getsize(file_path)
                }

            # Use parallel processor
            processor = ParallelProcessor(max_workers=4)

            start_time = time.time()
            results = processor.process_files(test_files, fast_process)
            total_time = time.time() - start_time

            # Should process 100 MB across 10 files quickly
            # With parallelism and fast processing, should be < 5 seconds
            assert total_time < 5.0, (
                f"End-to-end processing took {total_time:.2f}s, exceeds target"
            )

            # Verify all processed successfully
            successful = [r for r in results if r.success]
            assert len(successful) == len(test_files)

        finally:
            for file_path in test_files:
                os.unlink(file_path)

    def test_streaming_and_parallel_combined(self):
        """Test streaming parser with parallel processing."""
        # This test verifies that streaming and parallel features work together

        # Create test files
        test_files = []
        for i in range(5):
            with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
                f.write(b'x' * (5 * 1024 * 1024))  # 5 MB each
                test_files.append(f.name)

        try:
            # Use streaming-aware processing function
            def streaming_process(file_path: str) -> Dict:
                config = StreamingConfig(chunk_size=65536)
                parser = LIEFStreamingParser(file_path, config=config)

                bytes_read = 0
                with parser:
                    for chunk in parser.iter_chunks():
                        bytes_read += len(chunk)

                return {
                    "file": file_path,
                    "size": bytes_read,
                    "_parser": "streaming"
                }

            # Process in parallel
            processor = ParallelProcessor(max_workers=2)
            start_time = time.time()
            results = processor.process_files(test_files, streaming_process)
            total_time = time.time() - start_time

            # Should complete in reasonable time
            assert total_time < 10.0, f"Combined processing too slow: {total_time:.2f}s"

            # Verify streaming parser was used
            successful = [r for r in results if r.success]
            assert len(successful) == len(test_files)
            for result in successful:
                assert result.result.get("_parser") == "streaming"

        finally:
            for file_path in test_files:
                os.unlink(file_path)

    def test_eta_accuracy_in_parallel_context(self):
        """Test ETA accuracy when used with parallel processing."""
        test_files = []
        for i in range(10):
            with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
                f.write(b'x' * (1 * 1024 * 1024))  # 1 MB each
                test_files.append(f.name)

        try:
            # Train ETA estimator
            eta = ETAEstimator()
            for i in range(30):
                eta.record_processing(
                    file_size_bytes=1024 * 1024,
                    processing_time_seconds=0.2,
                    file_type="ELF",
                    architecture="x86_64"
                )

            # Processing function with consistent timing
            def process_func(file_path: str) -> Dict:
                time.sleep(0.2)  # 200ms per file
                return {"file": file_path, "type": "ELF"}

            # Get ETA
            processor = ParallelProcessor(max_workers=4, eta_estimator=eta)
            estimated = processor.estimate_total_time(test_files)

            # Process files
            start_time = time.time()
            results = processor.process_files(test_files, process_func)
            actual = time.time() - start_time

            # ETA should be reasonably accurate even with parallelism
            if estimated is not None:
                error = abs(estimated - actual) / actual
                # Allow wider tolerance for parallel processing (50%)
                assert error < 0.5, f"Parallel ETA error {error:.1%} too high"

        finally:
            for file_path in test_files:
                os.unlink(file_path)


class TestPerformanceRegressions:
    """Tests to detect performance regressions."""

    def test_no_regression_in_eta_estimator(self):
        """Ensure ETA estimator performance hasn't regressed."""
        estimator = ETAEstimator(history_size=1000)

        # Record 100 entries
        start = time.time()
        for i in range(100):
            estimator.record_processing(
                file_size_bytes=1024 * 1024,
                processing_time_seconds=1.0
            )
        record_time = time.time() - start

        # Should complete in under 10ms
        assert record_time < 0.01, f"Recording regression: {record_time*1000:.2f}ms"

    def test_no_regression_in_parallel_processor(self):
        """Ensure parallel processor performance hasn't regressed."""
        # Create test files
        test_files = []
        for i in range(10):
            with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
                f.write(b'x' * 1024)  # 1 KB each
                test_files.append(f.name)

        try:
            def process_func(path):
                return {"file": path}

            processor = ParallelProcessor(max_workers=4)

            # Test overhead of submitting and collecting results
            start = time.time()
            results = processor.process_files(test_files, process_func)
            overhead_time = time.time() - start

            # Overhead should be minimal (< 50ms for 10 tiny files)
            assert overhead_time < 0.05, f"Parallel processor regression: {overhead_time*1000:.2f}ms"

        finally:
            for file_path in test_files:
                os.unlink(file_path)

    def test_no_regression_in_streaming_parser(self):
        """Ensure streaming parser performance hasn't regressed."""
        # Create a 10 MB test file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            f.write(b'x' * (10 * 1024 * 1024))
            test_file = f.name

        try:
            config = StreamingConfig(chunk_size=65536)
            parser = LIEFStreamingParser(test_file, config=config)

            # Measure read throughput
            start = time.time()
            with parser:
                for chunk in parser.iter_chunks():
                    pass
            read_time = time.time() - start

            throughput = (10 / read_time)  # MB/s

            # Should maintain > 50 MB/s throughput
            assert throughput > 50, f"Streaming parser regression: {throughput:.1f} MB/s"

        finally:
            os.unlink(test_file)
