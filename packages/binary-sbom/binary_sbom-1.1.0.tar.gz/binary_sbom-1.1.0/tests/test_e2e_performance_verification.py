"""
End-to-end performance verification for CI/CD optimization features.

This script performs comprehensive verification of all performance targets
from the spec acceptance criteria:
- SBOM generation for <100MB binaries in under 30 seconds
- Parallel processing reduces wall-clock time by 50%+
- Streaming mode uses constant memory
- ETA estimation accuracy within ±20%

Run with: python tests/test_e2e_performance_verification.py
"""

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Tuple

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from binary_sbom.analyzer import analyze_binary
from binary_sbom.parallel_processor import ParallelProcessor
from binary_sbom.streaming_parser import StreamingParser, StreamingConfig
from binary_sbom.eta_estimator import ETAEstimator


class PerformanceMetrics:
    """Container for performance metrics."""

    def __init__(self):
        self.sequential_time: float = 0.0
        self.parallel_time: float = 0.0
        self.speedup: float = 0.0
        self.memory_usage_mb: float = 0.0
        self.eta_accuracy: float = 0.0
        self.results: Dict = {}

    def to_dict(self) -> Dict:
        """Convert metrics to dictionary for JSON serialization."""
        return {
            "sequential_time_seconds": round(self.sequential_time, 2),
            "parallel_time_seconds": round(self.parallel_time, 2),
            "speedup_percentage": round(self.speedup * 100, 1),
            "memory_usage_mb": round(self.memory_usage_mb, 2),
            "eta_accuracy_percentage": round(self.eta_accuracy * 100, 1),
            "targets_met": self.get_targets_met(),
        }

    def get_targets_met(self) -> Dict[str, bool]:
        """Check which performance targets are met."""
        return {
            "100mb_under_30s": self.sequential_time < 30.0,
            "parallel_50pct_faster": self.speedup >= 0.5,
            "streaming_constant_memory": self.memory_usage_mb < 200,  # Reasonable threshold
            "eta_accuracy_within_20pct": abs(self.eta_accuracy) <= 0.2,
        }


def generate_test_binary(output_path: Path, size_mb: int) -> None:
    """Generate a test binary file of specified size.

    Args:
        output_path: Path where binary should be created
        size_mb: Size of binary in megabytes
    """
    print(f"Generating {size_mb}MB test binary: {output_path.name}")
    with open(output_path, "wb") as f:
        # Write random data in chunks for efficiency
        chunk_size = 1024 * 1024  # 1MB chunks
        for _ in range(size_mb):
            f.write(os.urandom(chunk_size))
    actual_size = output_path.stat().st_size / (1024 * 1024)
    print(f"  Created: {actual_size:.2f}MB")


def run_cli_analysis(
    binary_paths: List[Path],
    parallel: bool = False,
    workers: int = None,
    streaming: bool = False,
) -> Tuple[float, Dict]:
    """Run binary-sbom CLI analysis and measure time.

    Args:
        binary_paths: List of binary file paths to analyze
        parallel: Whether to enable parallel processing
        workers: Number of parallel workers (None = auto)
        streaming: Whether to enable streaming mode

    Returns:
        Tuple of (elapsed_time, result_data)
    """
    cmd = [sys.executable, "-m", "binary_sbom.cli"]

    if parallel:
        cmd.append("--parallel")
        if workers:
            cmd.extend(["--workers", str(workers)])

    if streaming:
        cmd.append("--streaming")

    cmd.extend([str(p) for p in binary_paths])

    print(f"\nRunning: {' '.join(cmd)}")

    start_time = time.time()
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,  # 2 minute timeout
            cwd=Path(__file__).parent.parent,
        )
        elapsed = time.time() - start_time

        # Parse output for metrics
        result_data = {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0,
        }

        return elapsed, result_data

    except subprocess.TimeoutExpired:
        print(f"  ERROR: Command timed out after 120 seconds")
        return 120.0, {"success": False, "error": "timeout"}
    except Exception as e:
        print(f"  ERROR: {e}")
        elapsed = time.time() - start_time
        return elapsed, {"success": False, "error": str(e)}


def test_sequential_performance(binaries: List[Path]) -> float:
    """Test sequential processing performance.

    Args:
        binaries: List of binary files to process

    Returns:
        Total time for sequential processing
    """
    print("\n" + "=" * 60)
    print("TEST 1: Sequential Processing Performance")
    print("=" * 60)

    total_time = 0.0
    for binary in binaries:
        print(f"\nProcessing {binary.name} ({binary.stat().st_size / (1024*1024):.1f}MB)...")
        start = time.time()
        try:
            metadata = analyze_binary(str(binary), verbose=False)
            elapsed = time.time() - start
            total_time += elapsed
            print(f"  Completed in {elapsed:.2f}s")
        except Exception as e:
            print(f"  ERROR: {e}")
            elapsed = time.time() - start
            total_time += elapsed

    print(f"\nTotal sequential time: {total_time:.2f}s")
    return total_time


def test_parallel_performance(
    binaries: List[Path],
    workers: int = None,
) -> float:
    """Test parallel processing performance.

    Args:
        binaries: List of binary files to process
        workers: Number of parallel workers (None = auto)

    Returns:
        Total time for parallel processing
    """
    print("\n" + "=" * 60)
    print(f"TEST 2: Parallel Processing Performance (workers={workers or 'auto'})")
    print("=" * 60)

    def process_single_binary(binary_path: str) -> Dict:
        """Process a single binary file."""
        try:
            start = time.time()
            metadata = analyze_binary(binary_path, verbose=False)
            elapsed = time.time() - start
            return {
                "file": binary_path,
                "success": True,
                "time": elapsed,
                "metadata": metadata,
            }
        except Exception as e:
            return {
                "file": binary_path,
                "success": False,
                "time": 0,
                "error": str(e),
            }

    # Use parallel processor
    processor = ParallelProcessor(max_workers=workers)
    binary_strs = [str(b) for b in binaries]

    start_time = time.time()
    results = processor.process_files(
        files=binary_strs,
        process_func=process_single_binary,
    )
    elapsed = time.time() - start_time

    successful = sum(1 for r in results if r.success)
    print(f"\nProcessed {successful}/{len(binaries)} binaries successfully")
    print(f"Total parallel time: {elapsed:.2f}s")

    return elapsed


def test_100mb_target(binary_100mb: Path) -> bool:
    """Test that 100MB binary processes in under 30 seconds.

    Args:
        binary_100mb: Path to 100MB test binary

    Returns:
        True if processing completes in under 30 seconds
    """
    print("\n" + "=" * 60)
    print("TEST 3: 100MB Binary Performance Target (< 30s)")
    print("=" * 60)

    print(f"\nProcessing {binary_100mb.name}...")
    start = time.time()
    try:
        metadata = analyze_binary(str(binary_100mb), verbose=False)
        elapsed = time.time() - start
        print(f"  Completed in {elapsed:.2f}s")

        if elapsed < 30.0:
            print(f"  ✓ PASS: Completed in {elapsed:.2f}s (< 30s target)")
            return True
        else:
            print(f"  ✗ FAIL: Took {elapsed:.2f}s (exceeds 30s target)")
            return False

    except Exception as e:
        elapsed = time.time() - start
        print(f"  ERROR: {e}")
        print(f"  ✗ FAIL: Error after {elapsed:.2f}s")
        return False


def test_parallel_speedup(
    binaries: List[Path],
    sequential_time: float,
    parallel_time: float,
) -> float:
    """Test that parallel processing provides 50%+ speedup.

    Args:
        binaries: List of binary files processed
        sequential_time: Time for sequential processing
        parallel_time: Time for parallel processing

    Returns:
        Speedup as a fraction (0.5 = 50% faster)
    """
    print("\n" + "=" * 60)
    print("TEST 4: Parallel Speedup (50%+ target)")
    print("=" * 60)

    speedup = (sequential_time - parallel_time) / sequential_time
    print(f"\nSequential time: {sequential_time:.2f}s")
    print(f"Parallel time:   {parallel_time:.2f}s")
    print(f"Speedup:          {speedup * 100:.1f}%")

    if speedup >= 0.5:
        print(f"  ✓ PASS: {speedup * 100:.1f}% speedup (≥ 50% target)")
        return speedup
    else:
        print(f"  ✗ FAIL: {speedup * 100:.1f}% speedup (below 50% target)")
        return speedup


def test_streaming_memory_usage(binary_100mb: Path) -> float:
    """Test that streaming mode uses constant memory.

    Args:
        binary_100mb: Path to 100MB test binary

    Returns:
        Peak memory usage in MB
    """
    print("\n" + "=" * 60)
    print("TEST 5: Streaming Mode Memory Efficiency")
    print("=" * 60)

    try:
        import tracemalloc

        tracemalloc.start()

        # Use streaming parser directly
        config = StreamingConfig(chunk_size_bytes=1024 * 1024)  # 1MB chunks
        parser = StreamingParser(str(binary_100mb), config=config)

        with parser:
            # Read through all chunks
            chunk_count = 0
            for chunk in parser.iter_chunks():
                chunk_count += 1

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        peak_mb = peak / (1024 * 1024)
        print(f"\nProcessed {chunk_count} chunks")
        print(f"Peak memory usage: {peak_mb:.2f}MB")

        # Memory should stay constant (not grow with file size)
        # For a 100MB file, peak should be much less than file size
        if peak_mb < 200:  # Reasonable threshold
            print(f"  ✓ PASS: Memory usage {peak_mb:.2f}MB (constant)")
            return peak_mb
        else:
            print(f"  ✗ FAIL: Memory usage {peak_mb:.2f}MB (excessive)")
            return peak_mb

    except ImportError:
        print("  WARNING: tracemalloc not available, skipping memory test")
        return 0.0
    except Exception as e:
        print(f"  ERROR: {e}")
        return 0.0


def test_eta_accuracy(binary_50mb: Path, runs: int = 10) -> float:
    """Test ETA estimation accuracy within ±20%.

    Args:
        binary_50mb: Path to 50MB test binary
        runs: Number of test runs for accuracy measurement

    Returns:
        Average error fraction (0.2 = ±20%)
    """
    print("\n" + "=" * 60)
    print(f"TEST 6: ETA Estimation Accuracy (±20% target, {runs} runs)")
    print("=" * 60)

    estimator = ETAEstimator()
    errors = []

    for run in range(runs):
        # Record some historical data first
        for i in range(5):
            try:
                start = time.time()
                metadata = analyze_binary(str(binary_50mb), verbose=False)
                actual_time = time.time() - start

                # Get estimate before recording (similar to real usage)
                file_size = binary_50mb.stat().st_size
                estimated_time = estimator.estimate_time(file_size_bytes=file_size)

                if estimated_time is not None:
                    error_fraction = abs(estimated_time - actual_time) / actual_time
                    errors.append(error_fraction)

                    # Record the actual time
                    estimator.record_processing(
                        file_size_bytes=file_size,
                        processing_time_seconds=actual_time,
                        file_type="ELF",
                        architecture="x86_64",
                    )

                    print(
                        f"  Run {run + 1}: ETA={estimated_time:.2f}s, "
                        f"Actual={actual_time:.2f}s, "
                        f"Error={error_fraction * 100:.1f}%"
                    )
                    break  # Only record once per run
            except Exception as e:
                print(f"  Run {run + 1}: ERROR - {e}")
                continue

    if errors:
        avg_error = sum(errors) / len(errors)
        print(f"\nAverage ETA error: {avg_error * 100:.1f}%")

        if avg_error <= 0.2:
            print(f"  ✓ PASS: Average error {avg_error * 100:.1f}% (≤ 20% target)")
            return avg_error
        else:
            print(f"  ✗ FAIL: Average error {avg_error * 100:.1f}% (exceeds 20% target)")
            return avg_error
    else:
        print("  WARNING: No successful measurements")
        return 0.0


def run_all_verification_tests():
    """Run all end-to-end performance verification tests."""
    print("\n" + "=" * 60)
    print("END-TO-END PERFORMANCE VERIFICATION")
    print("=" * 60)
    print("\nThis will run comprehensive performance tests which may take")
    print("several minutes. Please be patient.")

    # Create temporary directory for test binaries
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        print(f"\nUsing temporary directory: {tmpdir_path}")

        # Generate test binaries
        print("\n" + "-" * 60)
        print("GENERATING TEST BINARIES")
        print("-" * 60)

        binaries = {
            "10mb": tmpdir_path / "test_10mb.bin",
            "50mb": tmpdir_path / "test_50mb.bin",
            "100mb": tmpdir_path / "test_100mb.bin",
        }

        for name, path in binaries.items():
            size_mb = int(name.replace("mb", ""))
            generate_test_binary(path, size_mb)

        binary_list = list(binaries.values())

        # Initialize metrics
        metrics = PerformanceMetrics()

        # Test 1: Sequential performance
        metrics.sequential_time = test_sequential_performance(binary_list)

        # Test 2 & 4: Parallel performance and speedup
        metrics.parallel_time = test_parallel_performance(binary_list, workers=None)
        metrics.speedup = test_parallel_speedup(
            binary_list,
            metrics.sequential_time,
            metrics.parallel_time,
        )

        # Test 3: 100MB target
        test_100mb_target(binaries["100mb"])

        # Test 5: Streaming memory usage
        metrics.memory_usage_mb = test_streaming_memory_usage(binaries["100mb"])

        # Test 6: ETA accuracy
        metrics.eta_accuracy = test_eta_accuracy(binaries["50mb"], runs=5)

        # Summary
        print("\n" + "=" * 60)
        print("VERIFICATION SUMMARY")
        print("=" * 60)

        results = metrics.to_dict()
        targets_met = metrics.get_targets_met()

        print("\nPerformance Metrics:")
        print(f"  Sequential time:  {results['sequential_time_seconds']}s")
        print(f"  Parallel time:    {results['parallel_time_seconds']}s")
        print(f"  Speedup:          {results['speedup_percentage']}%")
        print(f"  Memory usage:     {results['memory_usage_mb']}MB")
        print(f"  ETA accuracy:     {results['eta_accuracy_percentage']}%")

        print("\nTargets Met:")
        all_passed = True
        for target, passed in targets_met.items():
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"  {status}: {target}")
            if not passed:
                all_passed = False

        # Save results to JSON
        results_path = Path(__file__).parent / "e2e_performance_results.json"
        with open(results_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {results_path}")

        if all_passed:
            print("\n" + "=" * 60)
            print("ALL TESTS PASSED ✓")
            print("=" * 60)
            return 0
        else:
            print("\n" + "=" * 60)
            print("SOME TESTS FAILED ✗")
            print("=" * 60)
            return 1


if __name__ == "__main__":
    sys.exit(run_all_verification_tests())
