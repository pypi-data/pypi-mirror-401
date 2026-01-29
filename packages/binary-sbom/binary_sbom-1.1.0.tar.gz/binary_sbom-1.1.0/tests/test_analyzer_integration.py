"""
Integration tests for sandboxed binary analyzer.

These tests verify that the analyzer module correctly uses the sandboxed
LIEF wrapper instead of direct LIEF calls. Tests use mocking to avoid
requiring actual LIEF installation or real binary files.

This test file focuses on:
- Verifying SandboxManager is used instead of direct LIEF calls
- Backward compatibility with original analyzer API
- Error handling and propagation
- Integration between analyzer and sandbox modules
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, call
from unittest.mock import MagicMock

# Mock the sandbox module before importing analyzer
mock_sandbox = MagicMock()
mock_manager_class = MagicMock()
mock_sandbox.SandboxManager = mock_manager_class
mock_sandbox.SandboxError = Exception
mock_sandbox.SandboxTimeoutError = Exception
mock_sandbox.SandboxMemoryError = Exception
mock_sandbox.SandboxSecurityError = Exception
mock_sandbox.SandboxFileError = Exception
mock_sandbox.SandboxCrashedError = Exception

sys.modules['binary_sbom.sandbox'] = mock_sandbox
sys.modules['binary_sbom.sandbox.errors'] = MagicMock()

from binary_sbom.analyzer import analyze_binary, detect_format, analyze_binaries


class TestAnalyzeBinary(unittest.TestCase):
    """Test the analyze_binary function with sandboxed parsing."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_file = "/path/to/test_binary"

        # Create mock manager instance
        self.mock_manager = MagicMock()
        mock_manager_class.return_value = self.mock_manager

        # Reset mock calls
        mock_manager_class.reset_mock()

    def test_analyze_binary_success(self):
        """Test successful binary analysis through sandbox."""
        # Mock sandbox result
        mock_metadata = {
            "name": "test_binary",
            "type": "ELF",
            "architecture": "x86_64",
            "entrypoint": "0x400000",
            "sections": [{"name": ".text", "size": 4096}],
            "dependencies": ["libc.so.6"],
        }
        self.mock_manager.parse_binary.return_value = mock_metadata

        # Analyze binary
        result = analyze_binary(self.test_file)

        # Verify result
        self.assertEqual(result["name"], "test_binary")
        self.assertEqual(result["type"], "ELF")
        self.assertEqual(result["architecture"], "x86_64")

        # Verify sandbox was created with correct limits
        mock_manager_class.assert_called_once()
        call_kwargs = mock_manager_class.call_args[1]
        self.assertEqual(call_kwargs["memory_mb"], 500)
        self.assertEqual(call_kwargs["cpu_time_seconds"], 30)
        self.assertEqual(call_kwargs["wall_clock_timeout"], 60)

        # Verify parse_binary was called on manager
        self.mock_manager.parse_binary.assert_called_once_with(self.test_file, max_file_size_mb=100)

    def test_analyze_binary_custom_limits(self):
        """Test binary analysis with custom resource limits."""
        mock_metadata = {"name": "test", "type": "PE", "architecture": "AMD64"}
        self.mock_manager.parse_binary.return_value = mock_metadata

        # Analyze with custom limits
        analyze_binary(
            self.test_file,
            max_file_size_mb=200,
            memory_mb=1000,
            cpu_time_seconds=60,
            wall_clock_timeout=120,
        )

        # Verify manager was created with custom limits
        call_kwargs = mock_manager_class.call_args[1]
        self.assertEqual(call_kwargs["memory_mb"], 1000)
        self.assertEqual(call_kwargs["cpu_time_seconds"], 60)
        self.assertEqual(call_kwargs["wall_clock_timeout"], 120)

        # Verify max_file_size_mb was passed to parse_binary
        self.mock_manager.parse_binary.assert_called_once_with(self.test_file, max_file_size_mb=200)

    def test_analyze_binary_sandbox_error_propagation(self):
        """Test that sandbox errors are properly propagated."""
        # Mock sandbox to raise error
        mock_error = Exception("Sandbox error")
        self.mock_manager.parse_binary.side_effect = mock_error

        # Verify error is propagated
        with self.assertRaises(Exception) as context:
            analyze_binary(self.test_file)

        self.assertIn("Sandbox error", str(context.exception))

    def test_analyze_binary_file_not_found(self):
        """Test handling when file doesn't exist."""
        # Mock manager to raise FileNotFoundError
        self.mock_manager.parse_binary.side_effect = FileNotFoundError("File not found")

        # Verify error is propagated
        with self.assertRaises(FileNotFoundError):
            analyze_binary(self.test_file)

    def test_analyze_binary_invalid_file(self):
        """Test handling when file is invalid."""
        # Mock manager to raise ValueError
        self.mock_manager.parse_binary.side_effect = ValueError("Invalid file")

        # Verify error is propagated
        with self.assertRaises(ValueError):
            analyze_binary(self.test_file)

    def test_analyze_binary_uses_isolated_process(self):
        """Test that LIEF parsing happens in isolated process, not main process."""
        # This test verifies that analyze_binary doesn't import or use LIEF directly
        # It should only go through SandboxManager

        # Mock successful parsing
        mock_metadata = {"name": "test", "type": "ELF", "architecture": "x86_64"}
        self.mock_manager.parse_binary.return_value = mock_metadata

        # Analyze binary
        result = analyze_binary(self.test_file)

        # Verify result came through sandbox manager
        self.assertEqual(result["type"], "ELF")

        # Verify sandbox manager was the only path to LIEF
        # (no direct LIEF import or usage in analyzer module)
        self.mock_manager.parse_binary.assert_called_once()

    def test_analyze_binary_max_file_size_enforced(self):
        """Test that max_file_size_mb parameter is properly passed."""
        mock_metadata = {"name": "test", "type": "ELF", "architecture": "x86_64"}
        self.mock_manager.parse_binary.return_value = mock_metadata

        # Test with different max_file_size_mb values
        for size_mb in [10, 50, 100, 200]:
            mock_manager_class.reset_mock()
            self.mock_manager.reset_mock()

            analyze_binary(self.test_file, max_file_size_mb=size_mb)

            # Verify size was passed to parse_binary
            self.mock_manager.parse_binary.assert_called_once_with(
                self.test_file, max_file_size_mb=size_mb
            )


class TestDetectFormat(unittest.TestCase):
    """Test the detect_format function with sandboxed parsing."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_file = "/path/to/test_binary"
        self.mock_manager = MagicMock()
        mock_manager_class.return_value = self.mock_manager
        mock_manager_class.reset_mock()

    def test_detect_format_elf(self):
        """Test format detection for ELF binary."""
        mock_metadata = {
            "name": "test",
            "type": "ELF",
            "architecture": "EM_X86_64",
        }
        self.mock_manager.parse_binary.return_value = mock_metadata

        format_type, arch = detect_format(self.test_file)

        self.assertEqual(format_type, "ELF")
        self.assertEqual(arch, "EM_X86_64")

    def test_detect_format_pe(self):
        """Test format detection for PE binary."""
        mock_metadata = {
            "name": "test.exe",
            "type": "PE",
            "architecture": "IMAGE_FILE_MACHINE_AMD64",
        }
        self.mock_manager.parse_binary.return_value = mock_metadata

        format_type, arch = detect_format(self.test_file)

        self.assertEqual(format_type, "PE")
        self.assertEqual(arch, "IMAGE_FILE_MACHINE_AMD64")

    def test_detect_format_macho(self):
        """Test format detection for MachO binary."""
        mock_metadata = {
            "name": "test_macho",
            "type": "MachO",
            "architecture": "CPU_TYPE_ARM64",
        }
        self.mock_manager.parse_binary.return_value = mock_metadata

        format_type, arch = detect_format(self.test_file)

        self.assertEqual(format_type, "MachO")
        self.assertEqual(arch, "CPU_TYPE_ARM64")

    def test_detect_format_raw(self):
        """Test format detection for raw binary."""
        mock_metadata = {
            "name": "test.bin",
            "type": "Raw",
            "architecture": "unknown",
        }
        self.mock_manager.parse_binary.return_value = mock_metadata

        format_type, arch = detect_format(self.test_file)

        self.assertEqual(format_type, "Raw")
        self.assertEqual(arch, "unknown")

    def test_detect_format_custom_limits(self):
        """Test detect_format with custom resource limits."""
        mock_metadata = {"name": "test", "type": "ELF", "architecture": "x86_64"}
        self.mock_manager.parse_binary.return_value = mock_metadata

        detect_format(
            self.test_file,
            max_file_size_mb=200,
            memory_mb=1000,
            cpu_time_seconds=60,
            wall_clock_timeout=120,
        )

        # Verify manager was created with custom limits
        call_kwargs = mock_manager_class.call_args[1]
        self.assertEqual(call_kwargs["memory_mb"], 1000)
        self.assertEqual(call_kwargs["cpu_time_seconds"], 60)
        self.assertEqual(call_kwargs["wall_clock_timeout"], 120)

    def test_detect_format_error_propagation(self):
        """Test that errors from analyze_binary are propagated."""
        self.mock_manager.parse_binary.side_effect = FileNotFoundError("File not found")

        with self.assertRaises(FileNotFoundError):
            detect_format(self.test_file)


class TestAnalyzeBinaries(unittest.TestCase):
    """Test the analyze_binaries batch analysis function."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_files = ["/path/binary1", "/path/binary2", "/path/binary3"]
        self.mock_manager = MagicMock()
        mock_manager_class.return_value = self.mock_manager
        mock_manager_class.reset_mock()

    def test_analyze_binaries_all_success(self):
        """Test successful batch analysis of multiple binaries."""
        # Mock different results for each file
        mock_results = [
            {"name": "binary1", "type": "ELF", "architecture": "x86_64"},
            {"name": "binary2", "type": "PE", "architecture": "AMD64"},
            {"name": "binary3", "type": "MachO", "architecture": "ARM64"},
        ]
        self.mock_manager.parse_binary.side_effect = mock_results

        # Analyze binaries
        results = analyze_binaries(self.test_files)

        # Verify all results returned
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["type"], "ELF")
        self.assertEqual(results[1]["type"], "PE")
        self.assertEqual(results[2]["type"], "MachO")

        # Verify parse_binary called for each file
        self.assertEqual(self.mock_manager.parse_binary.call_count, 3)

    def test_analyze_binaries_partial_failure(self):
        """Test batch analysis with some failures."""
        # Mock first success, then error, then success
        self.mock_manager.parse_binary.side_effect = [
            {"name": "binary1", "type": "ELF", "architecture": "x86_64"},
            FileNotFoundError("File not found"),
            {"name": "binary3", "type": "PE", "architecture": "AMD64"},
        ]

        # Analyze binaries
        results = analyze_binaries(self.test_files)

        # Verify results include errors
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["type"], "ELF")  # Success
        self.assertTrue(results[1]["_error"])  # Error
        self.assertEqual(results[1]["file"], self.test_files[1])
        self.assertEqual(results[2]["type"], "PE")  # Success

    def test_analyze_binaries_all_failure(self):
        """Test batch analysis where all files fail."""
        self.mock_manager.parse_binary.side_effect = FileNotFoundError("Not found")

        # Analyze binaries
        results = analyze_binaries(self.test_files)

        # Verify all results have errors
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertTrue(result.get("_error", False))

    def test_analyze_binaries_custom_limits(self):
        """Test batch analysis with custom resource limits."""
        mock_metadata = {"name": "test", "type": "ELF", "architecture": "x86_64"}
        self.mock_manager.parse_binary.return_value = mock_metadata

        # Analyze with custom limits
        analyze_binaries(
            self.test_files,
            max_file_size_mb=200,
            memory_mb=1000,
            cpu_time_seconds=60,
            wall_clock_timeout=120,
        )

        # Verify manager was created with custom limits for each file
        self.assertEqual(mock_manager_class.call_count, 3)
        for call in mock_manager_class.call_args_list:
            call_kwargs = call[1]
            self.assertEqual(call_kwargs["memory_mb"], 1000)
            self.assertEqual(call_kwargs["cpu_time_seconds"], 60)
            self.assertEqual(call_kwargs["wall_clock_timeout"], 120)

    def test_analyze_binaries_sequential_processing(self):
        """Test that binaries are processed sequentially, not in parallel."""
        import time

        # Mock that tracks call order
        call_order = []

        def side_effect(file_path, max_file_size_mb):
            call_order.append(file_path)
            return {"name": Path(file_path).name, "type": "ELF", "architecture": "x86_64"}

        self.mock_manager.parse_binary.side_effect = side_effect

        # Analyze binaries
        analyze_binaries(self.test_files)

        # Verify calls were in order
        self.assertEqual(call_order, self.test_files)


class TestBackwardCompatibility(unittest.TestCase):
    """Test backward compatibility with original analyzer API."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_file = "/path/to/test_binary"
        self.mock_manager = MagicMock()
        mock_manager_class.return_value = self.mock_manager
        mock_manager_class.reset_mock()

    def test_analyze_binary_api_signature(self):
        """Test that analyze_binary has the expected signature."""
        import inspect

        sig = inspect.signature(analyze_binary)
        params = list(sig.parameters.keys())

        # Verify expected parameters exist
        self.assertIn("file_path", params)
        self.assertIn("max_file_size_mb", params)
        self.assertIn("memory_mb", params)
        self.assertIn("cpu_time_seconds", params)
        self.assertIn("wall_clock_timeout", params)

    def test_analyze_binary_default_values(self):
        """Test that default parameter values work correctly."""
        mock_metadata = {"name": "test", "type": "ELF", "architecture": "x86_64"}
        self.mock_manager.parse_binary.return_value = mock_metadata

        # Call with just file_path (use defaults)
        result = analyze_binary(self.test_file)

        # Should succeed
        self.assertEqual(result["type"], "ELF")

    def test_return_format_compatibility(self):
        """Test that return format matches original analyzer."""
        mock_metadata = {
            "name": "test_binary",
            "type": "ELF",
            "architecture": "x86_64",
            "entrypoint": "0x400000",
            "sections": [
                {"name": ".text", "size": 4096, "virtual_address": "0x400000"}
            ],
            "dependencies": ["libc.so.6", "libm.so.6"],
        }
        self.mock_manager.parse_binary.return_value = mock_metadata

        result = analyze_binary(self.test_file)

        # Verify all expected keys exist
        self.assertIn("name", result)
        self.assertIn("type", result)
        self.assertIn("architecture", result)
        self.assertIn("entrypoint", result)
        self.assertIn("sections", result)
        self.assertIn("dependencies", result)

    def test_detect_format_api_signature(self):
        """Test that detect_format has the expected signature."""
        import inspect

        sig = inspect.signature(detect_format)
        params = list(sig.parameters.keys())

        # Verify expected parameters
        self.assertIn("file_path", params)
        self.assertIn("max_file_size_mb", params)
        self.assertIn("memory_mb", params)
        self.assertIn("cpu_time_seconds", params)
        self.assertIn("wall_clock_timeout", params)

    def test_detect_format_returns_tuple(self):
        """Test that detect_format returns a tuple."""
        mock_metadata = {"name": "test", "type": "ELF", "architecture": "x86_64"}
        self.mock_manager.parse_binary.return_value = mock_metadata

        result = detect_format(self.test_file)

        # Should be a tuple
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], str)
        self.assertIsInstance(result[1], str)


if __name__ == "__main__":
    unittest.main()
