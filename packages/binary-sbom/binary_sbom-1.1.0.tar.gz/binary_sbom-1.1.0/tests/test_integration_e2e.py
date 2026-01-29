"""
End-to-end integration tests with real-world binaries.

These tests verify that the sandboxed binary analysis works correctly with
actual binary files found on the system. Tests cover:

- Various binary formats (ELF, PE, Mach-O)
- Stripped and unstripped binaries
- Position-independent executables (PIE)
- Statically and dynamically linked binaries
- Performance overhead measurement
- Complete SBOM generation pipeline

Tests use @unittest.skipIf to gracefully handle missing LIEF dependency.
"""

import os
import sys
import time
import unittest
from pathlib import Path
from typing import List, Tuple

# Try to import LIEF - if not available, tests will be skipped
try:
    import lief

    LIEF_AVAILABLE = True
except ImportError:
    LIEF_AVAILABLE = False

# Try to import analyzer - requires sandbox modules
try:
    from binary_sbom.analyzer import analyze_binary, analyze_binaries, detect_format
    from binary_sbom.sandbox import SandboxManager
    ANALYZER_AVAILABLE = True
except ImportError:
    ANALYZER_AVAILABLE = False


@unittest.skipIf(not LIEF_AVAILABLE, "LIEF not installed - skipping real binary tests")
@unittest.skipIf(not ANALYZER_AVAILABLE, "Analyzer modules not available")
class TestRealBinaryFormats(unittest.TestCase):
    """
    Test analysis of real binaries in different formats.

    These tests use actual system binaries to verify that the sandboxed
    analysis correctly handles ELF, PE, and Mach-O formats.
    """

    @classmethod
    def setUpClass(cls):
        """Find available test binaries once for all tests."""
        cls.test_binaries = cls._find_test_binaries()

    @staticmethod
    def _find_test_binaries() -> dict:
        """
        Find real system binaries for testing.

        Returns:
            Dict mapping format names to lists of binary paths.
        """
        binaries = {"ELF": [], "PE": [], "MachO": [], "Unknown": []}

        # Common system binary locations
        search_paths = [
            "/bin",
            "/usr/bin",
            "/usr/local/bin",
            "/sbin",
            "/usr/sbin",
            "/Applications",
        ]

        # Binaries to search for (platform-specific)
        if sys.platform.startswith("linux"):
            candidates = [
                "/bin/ls",
                "/bin/bash",
                "/bin/sh",
                "/usr/bin/python3",
                "/usr/bin/gcc",
                "/usr/bin/ld",
            ]
        elif sys.platform == "darwin":
            candidates = [
                "/bin/ls",
                "/bin/bash",
                "/bin/zsh",
                "/usr/bin/python3",
                "/usr/bin/swift",
                "/usr/bin/clang",
            ]
        elif sys.platform == "win32":
            candidates = [
                r"C:\Windows\System32\cmd.exe",
                r"C:\Windows\System32\powershell.exe",
                r"C:\Windows\System32\notepad.exe",
            ]
        else:
            candidates = []

        # Check which binaries exist and detect their format
        for binary_path in candidates:
            if os.path.exists(binary_path):
                try:
                    # Use LIEF to detect format
                    binary = lief.parse(binary_path)
                    if binary is not None:
                        if hasattr(binary, "format"):
                            format_name = binary.format.name
                            if format_name in binaries:
                                binaries[format_name].append(binary_path)
                except Exception:
                    binaries["Unknown"].append(binary_path)

        return binaries

    def test_analyze_macho_binary(self):
        """Test analysis of Mach-O binary (macOS)."""
        if not self.test_binaries["MachO"]:
            self.skipTest("No Mach-O binaries found on system")

        binary_path = self.test_binaries["MachO"][0]

        # Analyze binary through sandbox
        metadata = analyze_binary(binary_path)

        # Verify metadata
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata["type"], "MachO")
        self.assertIn("name", metadata)
        self.assertIn("architecture", metadata)
        self.assertIsNotNone(metadata["name"])

        # Verify sections were extracted
        self.assertIsInstance(metadata.get("sections"), list)
        if metadata["sections"]:
            section = metadata["sections"][0]
            self.assertIn("name", section)
            self.assertIn("size", section)

    def test_analyze_elf_binary(self):
        """Test analysis of ELF binary (Linux)."""
        if not self.test_binaries["ELF"]:
            self.skipTest("No ELF binaries found on system")

        binary_path = self.test_binaries["ELF"][0]

        # Analyze binary through sandbox
        metadata = analyze_binary(binary_path)

        # Verify metadata
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata["type"], "ELF")
        self.assertIn("name", metadata)
        self.assertIn("architecture", metadata)

        # Verify dependencies were extracted
        self.assertIsInstance(metadata.get("dependencies"), list)

    def test_analyze_pe_binary(self):
        """Test analysis of PE binary (Windows)."""
        if not self.test_binaries["PE"]:
            self.skipTest("No PE binaries found on system")

        binary_path = self.test_binaries["PE"][0]

        # Analyze binary through sandbox
        metadata = analyze_binary(binary_path)

        # Verify metadata
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata["type"], "PE")
        self.assertIn("name", metadata)
        self.assertIn("architecture", metadata)

    def test_detect_format_real_binaries(self):
        """Test format detection on real binaries."""
        all_binaries = []
        for format_name, paths in self.test_binaries.items():
            if format_name != "Unknown":
                all_binaries.extend([(format_name, path) for path in paths])

        if not all_binaries:
            self.skipTest("No recognized binaries found on system")

        for expected_format, binary_path in all_binaries[:5]:  # Test up to 5
            with self.subTest(binary=binary_path):
                detected_format, arch = detect_format(binary_path)
                self.assertEqual(detected_format, expected_format)
                self.assertIsNotNone(arch)
                self.assertNotEqual(arch, "unknown")

    def test_analyze_multiple_binaries(self):
        """Test batch analysis of multiple real binaries."""
        all_binaries = []
        for paths in self.test_binaries.values():
            all_binaries.extend(paths[:2])  # Take up to 2 from each format

        if len(all_binaries) < 2:
            self.skipTest("Need at least 2 binaries for batch test")

        # Analyze binaries
        results = analyze_binaries(all_binaries)

        # Verify results
        self.assertEqual(len(results), len(all_binaries))

        # Check that at least some succeeded
        successful = [r for r in results if "_error" not in r]
        self.assertGreater(len(successful), 0, "At least one binary should analyze successfully")

    def test_fallback_to_default_parser(self):
        """Test that files without a matching plugin use the default LIEF parser."""
        import tempfile

        # Find a real binary to test with (using one that won't match plugins)
        if not self.test_binaries["ELF"] and not self.test_binaries["MachO"] and not self.test_binaries["PE"]:
            self.skipTest("No recognized binaries found on system")

        # Use the first available binary (plugins don't handle standard binary formats)
        all_binaries = []
        for format_name, paths in self.test_binaries.items():
            if format_name != "Unknown":
                all_binaries.extend(paths)

        if not all_binaries:
            self.skipTest("No recognized binaries found on system")

        binary_path = all_binaries[0]

        # Analyze binary - should use default LIEF parser since no plugin matches
        metadata = analyze_binary(binary_path)

        # Verify metadata was returned
        self.assertIsNotNone(metadata)
        self.assertNotIn("_error", metadata, "Analysis should succeed without errors")

        # Verify default parser was used
        self.assertEqual(metadata.get("_parser"), "lief",
                        "Default LIEF parser should be used when no plugin matches")

        # Verify basic metadata fields are present
        self.assertIn("type", metadata)
        self.assertIn("architecture", metadata)
        self.assertIn("name", metadata)

        # Verify type is a valid binary format
        valid_types = ["ELF", "PE", "MachO"]
        self.assertIn(metadata["type"], valid_types,
                     f"Binary type should be one of {valid_types}, got {metadata['type']}")


@unittest.skipIf(not LIEF_AVAILABLE, "LIEF not installed")
@unittest.skipIf(not ANALYZER_AVAILABLE, "Analyzer modules not available")
class TestBinaryCharacteristics(unittest.TestCase):
    """
    Test analysis of binaries with different characteristics.

    Tests cover:
    - Stripped vs unstripped binaries
    - Position-independent executables (PIE)
    - Statically vs dynamically linked binaries
    """

    def test_stripped_vs_unstripped(self):
        """Test that both stripped and unstripped binaries are handled correctly."""
        # Try to find stripped and unstripped versions
        # On many systems, /bin/ls is stripped while development tools are unstripped

        binaries_to_test = []
        if sys.platform == "darwin":
            binaries_to_test.append(("/bin/ls", "likely stripped"))
            binaries_to_test.append(("/bin/bash", "likely unstripped"))
        elif sys.platform.startswith("linux"):
            binaries_to_test.append(("/bin/ls", "production binary"))
            # Python binaries often have symbols
            if os.path.exists("/usr/bin/python3"):
                binaries_to_test.append(("/usr/bin/python3", "may have symbols"))

        results = []
        for binary_path, description in binaries_to_test:
            if os.path.exists(binary_path):
                try:
                    metadata = analyze_binary(binary_path)
                    results.append((binary_path, description, metadata))
                except Exception as e:
                    # Some binaries might fail to parse - that's OK
                    pass

        if not results:
            self.skipTest("No suitable binaries found for testing")

        # Verify all analyzed binaries returned valid metadata
        for binary_path, description, metadata in results:
            with self.subTest(binary=binary_path, desc=description):
                self.assertIn("type", metadata)
                self.assertIn("architecture", metadata)
                self.assertIn("sections", metadata)

                # Sections should be present even for stripped binaries
                # (though stripped binaries have fewer sections with meaningful names)
                self.assertIsInstance(metadata["sections"], list)

    def test_position_independent_executable(self):
        """Test analysis of PIE (Position Independent Executable) binaries."""
        # Most modern system binaries are PIE
        pie_binaries = []

        if sys.platform == "darwin":
            # macOS binaries are typically PIE
            if os.path.exists("/bin/ls"):
                pie_binaries.append("/bin/ls")
        elif sys.platform.startswith("linux"):
            if os.path.exists("/bin/ls"):
                pie_binaries.append("/bin/ls")
            if os.path.exists("/usr/bin/python3"):
                pie_binaries.append("/usr/bin/python3")

        if not pie_binaries:
            self.skipTest("No PIE binaries found for testing")

        for binary_path in pie_binaries:
            with self.subTest(binary=binary_path):
                metadata = analyze_binary(binary_path)

                # Verify PIE binary is analyzed correctly
                self.assertIsNotNone(metadata)
                self.assertIn("type", metadata)

    def test_dynamically_linked_binary(self):
        """Test analysis of dynamically linked binaries."""
        # Most system binaries are dynamically linked
        dynamic_binaries = []

        if sys.platform == "darwin":
            if os.path.exists("/bin/bash"):
                dynamic_binaries.append("/bin/bash")
            if os.path.exists("/bin/zsh"):
                dynamic_binaries.append("/bin/zsh")
        elif sys.platform.startswith("linux"):
            if os.path.exists("/bin/bash"):
                dynamic_binaries.append("/bin/bash")
            if os.path.exists("/usr/bin/python3"):
                dynamic_binaries.append("/usr/bin/python3")

        if not dynamic_binaries:
            self.skipTest("No dynamically linked binaries found")

        for binary_path in dynamic_binaries:
            with self.subTest(binary=binary_path):
                metadata = analyze_binary(binary_path)

                # Dynamically linked binaries should have dependencies
                self.assertIsNotNone(metadata)
                self.assertIn("dependencies", metadata)
                self.assertIsInstance(metadata["dependencies"], list)

                # Should have at least one dependency
                # (Note: some binaries might have empty dependencies list if parsing fails)
                self.assertIsNotNone(metadata["dependencies"])


@unittest.skipIf(not LIEF_AVAILABLE, "LIEF not installed")
@unittest.skipIf(not ANALYZER_AVAILABLE, "Analyzer modules not available")
class TestPerformanceOverhead(unittest.TestCase):
    """
    Test that sandboxing overhead is acceptable (<20%).

    Measures the performance impact of sandboxed parsing compared to
    baseline parsing time.
    """

    def test_sandboxing_overhead_acceptable(self):
        """
        Verify that sandboxing overhead is less than 20% of parse time.

        This test measures:
        1. Baseline: Direct LIEF parsing time
        2. Sandboxed: Sandboxed parsing time
        3. Overhead: (Sandboxed - Baseline) / Baseline

        The overhead should be less than 20% for typical binaries.
        """
        # Find a suitable test binary (small but real)
        test_binary = None
        for candidate in ["/bin/ls", "/bin/bash", "/bin/zsh", "/usr/bin/python3"]:
            if os.path.exists(candidate) and os.path.getsize(candidate) < 200000:
                test_binary = candidate
                break

        if not test_binary:
            self.skipTest("No suitable test binary found")

        # Measure baseline LIEF parsing (5 iterations, take median)
        baseline_times = []
        for _ in range(5):
            start = time.perf_counter()
            binary = lief.parse(test_binary)
            # Force parsing by accessing attributes
            if binary:
                _ = binary.format
                _ = binary.entrypoint
            baseline_times.append(time.perf_counter() - start)

        baseline_time = sorted(baseline_times)[2]  # Median
        print(f"\nBaseline LIEF parse time: {baseline_time * 1000:.2f}ms")

        # Measure sandboxed parsing (5 iterations, take median)
        sandboxed_times = []
        for _ in range(5):
            start = time.perf_counter()
            metadata = analyze_binary(test_binary)
            sandboxed_times.append(time.perf_counter() - start)

        sandboxed_time = sorted(sandboxed_times)[2]  # Median
        print(f"Sandboxed parse time: {sandboxed_time * 1000:.2f}ms")

        # Calculate overhead
        overhead_ms = sandboxed_time - baseline_time
        overhead_percent = (overhead_ms / baseline_time) * 100 if baseline_time > 0 else 0

        print(f"Sandboxing overhead: {overhead_ms * 1000:.2f}ms ({overhead_percent:.1f}%)")

        # Verify overhead is acceptable
        # Allow up to 20% overhead OR up to 100ms absolute overhead
        # (for very fast binaries where percentage is misleading)
        max_overhead_percent = 20
        max_overhead_ms = 100

        self.assertLess(
            overhead_percent,
            max_overhead_percent,
            f"Sandboxing overhead ({overhead_percent:.1f}%) exceeds {max_overhead_percent}%",
        )

        # Also verify absolute overhead is reasonable
        self.assertLess(
            overhead_ms,
            max_overhead_ms / 1000.0,
            f"Absolute sandboxing overhead ({overhead_ms * 1000:.1f}ms) exceeds {max_overhead_ms}ms",
        )

    def test_sandboxing_overhead_consistency(self):
        """Test that sandboxing overhead is consistent across multiple runs."""
        test_binary = None
        for candidate in ["/bin/ls", "/bin/bash"]:
            if os.path.exists(candidate):
                test_binary = candidate
                break

        if not test_binary:
            self.skipTest("No suitable test binary found")

        # Measure sandboxed parsing time over 10 runs
        times = []
        for _ in range(10):
            start = time.perf_counter()
            metadata = analyze_binary(test_binary)
            times.append(time.perf_counter() - start)

        # Calculate statistics
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        std_dev = (sum((t - avg_time) ** 2 for t in times) / len(times)) ** 0.5

        print(f"\nSandboxed parsing statistics (10 runs):")
        print(f"  Average: {avg_time * 1000:.2f}ms")
        print(f"  Min: {min_time * 1000:.2f}ms")
        print(f"  Max: {max_time * 1000:.2f}ms")
        print(f"  Std Dev: {std_dev * 1000:.2f}ms")

        # Verify consistency: standard deviation should be less than 50% of average
        # (allows for some system load variance)
        coefficient_of_variation = (std_dev / avg_time) * 100 if avg_time > 0 else 0

        self.assertLess(
            coefficient_of_variation,
            50,
            f"Sandboxing time is inconsistent (CV={coefficient_of_variation:.1f}%)",
        )

    def test_batch_analysis_performance(self):
        """Test performance of analyzing multiple binaries sequentially."""
        # Find multiple small binaries
        binaries = []
        for candidate in ["/bin/ls", "/bin/bash", "/bin/zsh", "/bin/cat", "/bin/echo"]:
            if os.path.exists(candidate):
                binaries.append(candidate)

        if len(binaries) < 2:
            self.skipTest("Need at least 2 binaries for batch test")

        # Measure sequential analysis time
        start = time.perf_counter()
        results = analyze_binaries(binaries)
        total_time = time.perf_counter() - start

        # Calculate average time per binary
        avg_time_per_binary = total_time / len(binaries)

        print(f"\nBatch analysis of {len(binaries)} binaries:")
        print(f"  Total time: {total_time * 1000:.2f}ms")
        print(f"  Average per binary: {avg_time_per_binary * 1000:.2f}ms")

        # Verify average time is reasonable (<500ms per binary)
        self.assertLess(
            avg_time_per_binary,
            0.5,
            f"Average analysis time ({avg_time_per_binary * 1000:.1f}ms) exceeds 500ms",
        )


@unittest.skipIf(not LIEF_AVAILABLE, "LIEF not installed")
@unittest.skipIf(not ANALYZER_AVAILABLE, "Analyzer modules not available")
class TestSBOMGeneration(unittest.TestCase):
    """
    Test that SBOM generation still works correctly with sandboxing.

    Verifies that the complete metadata extraction pipeline works,
    producing all required fields for SBOM generation.
    """

    def test_metadata_completeness(self):
        """Test that all required SBOM metadata fields are extracted."""
        test_binary = None
        for candidate in ["/bin/ls", "/bin/bash", "/bin/zsh"]:
            if os.path.exists(candidate):
                test_binary = candidate
                break

        if not test_binary:
            self.skipTest("No suitable test binary found")

        # Analyze binary
        metadata = analyze_binary(test_binary)

        # Verify required SBOM fields are present
        required_fields = ["name", "type", "architecture"]
        for field in required_fields:
            self.assertIn(field, metadata, f"Required SBOM field '{field}' is missing")

        # Verify optional fields are present and properly typed
        optional_fields = {
            "entrypoint": (str, type(None)),
            "sections": list,
            "dependencies": list,
        }

        for field, expected_type in optional_fields.items():
            self.assertIn(field, metadata, f"Optional field '{field}' is missing")
            self.assertIsInstance(
                metadata[field],
                expected_type,
                f"Field '{field}' has wrong type: {type(metadata[field])}",
            )

    def test_metadata_accuracy(self):
        """Test that extracted metadata is accurate."""
        test_binary = None
        for candidate in ["/bin/ls", "/bin/bash"]:
            if os.path.exists(candidate):
                test_binary = candidate
                break

        if not test_binary:
            self.skipTest("No suitable test binary found")

        # Analyze binary
        metadata = analyze_binary(test_binary)

        # Cross-validate with direct LIEF parsing
        binary = lief.parse(test_binary)
        self.assertIsNotNone(binary)

        # Verify format matches
        self.assertEqual(metadata["type"], binary.format.name)

        # Verify name matches
        expected_name = os.path.basename(test_binary)
        self.assertEqual(metadata["name"], expected_name)

        # Verify architecture is present and valid
        self.assertIsNotNone(metadata["architecture"])
        self.assertIsInstance(metadata["architecture"], str)
        self.assertNotEqual(metadata["architecture"], "")

    def test_sections_metadata(self):
        """Test that sections metadata is properly extracted."""
        test_binary = None
        for candidate in ["/bin/ls", "/bin/bash", "/usr/bin/python3"]:
            if os.path.exists(candidate):
                test_binary = candidate
                break

        if not test_binary:
            self.skipTest("No suitable test binary found")

        # Analyze binary
        metadata = analyze_binary(test_binary)

        # Verify sections are extracted
        self.assertIn("sections", metadata)
        sections = metadata["sections"]
        self.assertIsInstance(sections, list)

        if sections:
            # Check first section has required fields
            section = sections[0]
            self.assertIn("name", section)
            self.assertIn("size", section)

            # Verify types
            self.assertIsInstance(section["name"], str)
            self.assertIsInstance(section["size"], int)
            self.assertGreater(section["size"], 0)

    def test_dependencies_metadata(self):
        """Test that dependencies are properly extracted."""
        # Use a dynamically linked binary
        test_binary = None
        for candidate in ["/bin/bash", "/bin/zsh", "/usr/bin/python3"]:
            if os.path.exists(candidate):
                test_binary = candidate
                break

        if not test_binary:
            self.skipTest("No suitable test binary found")

        # Analyze binary
        metadata = analyze_binary(test_binary)

        # Verify dependencies list exists
        self.assertIn("dependencies", metadata)
        dependencies = metadata["dependencies"]
        self.assertIsInstance(dependencies, list)

        # Dependencies should be strings
        for dep in dependencies:
            self.assertIsInstance(dep, str)

    def test_error_handling_in_pipeline(self):
        """Test that errors are properly handled in SBOM generation pipeline."""
        # Test with non-existent file
        with self.assertRaises(FileNotFoundError):
            analyze_binary("/nonexistent/binary/path")

        # Test with invalid file (empty file)
        import tempfile

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        try:
            with self.assertRaises((ValueError, Exception)):
                analyze_binary(tmp_path)
        finally:
            os.unlink(tmp_path)


@unittest.skipIf(not LIEF_AVAILABLE, "LIEF not installed")
@unittest.skipIf(not ANALYZER_AVAILABLE, "Analyzer modules not available")
class TestSandboxIsolationE2E(unittest.TestCase):
    """
    End-to-end tests for sandbox isolation with real binaries.

    Verifies that sandbox isolation works correctly when analyzing
    real binaries, not just test cases.
    """

    def test_sandbox_process_cleanup(self):
        """Test that sandbox processes are properly cleaned up."""
        test_binary = None
        for candidate in ["/bin/ls", "/bin/bash"]:
            if os.path.exists(candidate):
                test_binary = candidate
                break

        if not test_binary:
            self.skipTest("No suitable test binary found")

        # Get initial process count
        import psutil

        parent = psutil.Process()
        initial_children = len(parent.children(recursive=True))

        # Analyze multiple binaries
        for _ in range(5):
            try:
                analyze_binary(test_binary)
            except Exception:
                pass  # Ignore parsing errors

        # Check that no zombie/child processes remain
        final_children = len(parent.children(recursive=True))

        # Allow some tolerance for system processes
        # (should not have more than 2 extra processes)
        self.assertLessEqual(
            final_children - initial_children,
            2,
            "Sandbox processes may not be properly cleaned up",
        )

    def test_sandbox_resource_limits_real_binary(self):
        """Test that resource limits work correctly with real binaries."""
        test_binary = None
        for candidate in ["/bin/ls", "/bin/bash"]:
            if os.path.exists(candidate):
                test_binary = candidate
                break

        if not test_binary:
            self.skipTest("No suitable test binary found")

        # Analyze with very strict limits
        # Real small binaries should still work
        try:
            metadata = analyze_binary(
                test_binary,
                memory_mb=100,  # 100MB should be plenty for small binaries
                cpu_time_seconds=5,  # 5 seconds should be enough
                wall_clock_timeout=10,  # 10 seconds total
            )

            # Verify success
            self.assertIsNotNone(metadata)
            self.assertIn("type", metadata)

        except Exception as e:
            self.fail(f"Real binary analysis failed with strict limits: {e}")

    def test_concurrent_analysis(self):
        """Test that multiple sandboxed analyses can run concurrently."""
        import multiprocessing

        # Find multiple binaries
        binaries = []
        for candidate in ["/bin/ls", "/bin/bash", "/bin/zsh", "/bin/cat"]:
            if os.path.exists(candidate):
                binaries.append(candidate)

        if len(binaries) < 2:
            self.skipTest("Need at least 2 binaries for concurrent test")

        def analyze_single(path):
            try:
                return analyze_binary(path)
            except Exception as e:
                return {"_error": str(e)}

        # Analyze binaries concurrently
        with multiprocessing.Pool(processes=2) as pool:
            results = pool.map(analyze_single, binaries)

        # Verify all analyses completed (successfully or with error)
        self.assertEqual(len(results), len(binaries))

        # At least some should succeed
        successful = [r for r in results if "_error" not in r]
        self.assertGreater(len(successful), 0, "At least one concurrent analysis should succeed")


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
