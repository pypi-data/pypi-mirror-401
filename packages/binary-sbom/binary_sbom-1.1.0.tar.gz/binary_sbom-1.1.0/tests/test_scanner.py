"""
Unit tests for the scanner module.

Tests recursive directory traversal, pattern filtering, and binary file discovery.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.scanner import DirectoryScanner, scan_directory
from src.file_detector import FileType


def resolve_path(path):
    """Resolve a path to its absolute canonical form."""
    return str(Path(path).resolve())


class TestDirectoryScannerInitialization(unittest.TestCase):
    """Test DirectoryScanner class initialization and validation."""

    def setUp(self):
        """Create temporary directories for testing."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary directories."""
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def test_initialization_with_valid_directory(self):
        """Test scanner initialization with a valid directory."""
        scanner = DirectoryScanner(self.test_dir)
        self.assertEqual(str(scanner.root_dir), resolve_path(self.test_dir))
        self.assertIsNone(scanner.include_patterns)
        self.assertEqual(scanner.exclude_patterns, [])
        self.assertFalse(scanner.verbose)

    def test_initialization_with_include_patterns(self):
        """Test scanner initialization with include patterns."""
        scanner = DirectoryScanner(self.test_dir, include_patterns=['*.so', '*.exe'])
        self.assertEqual(scanner.include_patterns, ['*.so', '*.exe'])

    def test_initialization_with_exclude_patterns(self):
        """Test scanner initialization with exclude patterns."""
        scanner = DirectoryScanner(self.test_dir, exclude_patterns=['*.debug', '*.log'])
        self.assertEqual(scanner.exclude_patterns, ['*.debug', '*.log'])

    def test_initialization_with_verbose_mode(self):
        """Test scanner initialization with verbose mode enabled."""
        scanner = DirectoryScanner(self.test_dir, verbose=True)
        self.assertTrue(scanner.verbose)

    def test_initialization_with_nonexistent_directory(self):
        """Test that nonexistent directory raises ValueError."""
        nonexistent = os.path.join(self.test_dir, 'does_not_exist')
        with self.assertRaises(ValueError) as context:
            DirectoryScanner(nonexistent)
        self.assertIn('does not exist', str(context.exception))

    def test_initialization_with_file_instead_of_directory(self):
        """Test that file path instead of directory raises ValueError."""
        # Create a file
        file_path = os.path.join(self.test_dir, 'not_a_dir')
        with open(file_path, 'w') as f:
            f.write('test')

        # Try to create scanner with file path
        with self.assertRaises(ValueError) as context:
            DirectoryScanner(file_path)
        self.assertIn('not a directory', str(context.exception))

        # Clean up the file before tearDown
        os.remove(file_path)


class TestPatternMatching(unittest.TestCase):
    """Test include/exclude pattern matching functionality."""

    def setUp(self):
        """Create temporary directory with test files."""
        self.test_dir = tempfile.mkdtemp()
        self.scanner = DirectoryScanner(self.test_dir)

    def tearDown(self):
        """Clean up temporary files and directories."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_matches_include_patterns_with_none(self):
        """Test that None include patterns match all files."""
        test_file = Path(self.test_dir) / 'any_file.txt'
        self.assertTrue(self.scanner._matches_include_patterns(test_file))

    def test_matches_include_patterns_with_exact_match(self):
        """Test pattern matching with exact filename match."""
        self.scanner.include_patterns = ['*.so']
        self.assertTrue(
            self.scanner._matches_include_patterns(Path(self.test_dir) / 'test.so')
        )
        self.assertFalse(
            self.scanner._matches_include_patterns(Path(self.test_dir) / 'test.exe')
        )

    def test_matches_include_patterns_with_wildcards(self):
        """Test pattern matching with wildcards."""
        self.scanner.include_patterns = ['lib*.so']
        self.assertTrue(
            self.scanner._matches_include_patterns(Path(self.test_dir) / 'libc.so')
        )
        self.assertTrue(
            self.scanner._matches_include_patterns(Path(self.test_dir) / 'libtest.so')
        )
        self.assertFalse(
            self.scanner._matches_include_patterns(Path(self.test_dir) / 'test.so')
        )

    def test_matches_include_patterns_with_question_mark(self):
        """Test pattern matching with question mark wildcard."""
        self.scanner.include_patterns = ['lib?.so']
        self.assertTrue(
            self.scanner._matches_include_patterns(Path(self.test_dir) / 'libc.so')
        )
        self.assertTrue(
            self.scanner._matches_include_patterns(Path(self.test_dir) / 'libx.so')
        )
        self.assertFalse(
            self.scanner._matches_include_patterns(Path(self.test_dir) / 'libtest.so')
        )

    def test_matches_include_patterns_with_character_range(self):
        """Test pattern matching with character ranges."""
        self.scanner.include_patterns = ['lib[abc].so']
        self.assertTrue(
            self.scanner._matches_include_patterns(Path(self.test_dir) / 'liba.so')
        )
        self.assertTrue(
            self.scanner._matches_include_patterns(Path(self.test_dir) / 'libb.so')
        )
        self.assertFalse(
            self.scanner._matches_include_patterns(Path(self.test_dir) / 'libx.so')
        )

    def test_matches_include_patterns_with_path(self):
        """Test pattern matching against full path."""
        self.scanner.include_patterns = ['*/lib/*.so']
        sub_dir = Path(self.test_dir) / 'lib'
        sub_dir.mkdir()
        self.assertTrue(
            self.scanner._matches_include_patterns(sub_dir / 'test.so')
        )

    def test_matches_exclude_patterns_with_empty_list(self):
        """Test that empty exclude patterns match nothing."""
        test_file = Path(self.test_dir) / 'any_file.so'
        self.assertFalse(self.scanner._matches_exclude_patterns(test_file))

    def test_matches_exclude_patterns_with_match(self):
        """Test exclude pattern matching."""
        self.scanner.exclude_patterns = ['*.debug']
        self.assertTrue(
            self.scanner._matches_exclude_patterns(Path(self.test_dir) / 'test.debug')
        )
        self.assertFalse(
            self.scanner._matches_exclude_patterns(Path(self.test_dir) / 'test.so')
        )

    def test_should_process_file_with_no_patterns(self):
        """Test that all files are processed when no patterns specified."""
        test_file = Path(self.test_dir) / 'test.so'
        self.assertTrue(self.scanner._should_process_file(test_file))

    def test_should_process_file_with_include_only(self):
        """Test file processing with include pattern only."""
        self.scanner.include_patterns = ['*.so']
        self.assertTrue(
            self.scanner._should_process_file(Path(self.test_dir) / 'test.so')
        )
        self.assertFalse(
            self.scanner._should_process_file(Path(self.test_dir) / 'test.exe')
        )

    def test_should_process_file_with_exclude_only(self):
        """Test file processing with exclude pattern only."""
        self.scanner.exclude_patterns = ['*.debug']
        self.assertFalse(
            self.scanner._should_process_file(Path(self.test_dir) / 'test.debug')
        )
        self.assertTrue(
            self.scanner._should_process_file(Path(self.test_dir) / 'test.so')
        )

    def test_should_process_file_with_both_patterns(self):
        """Test file processing with both include and exclude patterns."""
        self.scanner.include_patterns = ['*.so']
        self.scanner.exclude_patterns = ['*.debug']

        # Matches include, not exclude -> should process
        self.assertTrue(
            self.scanner._should_process_file(Path(self.test_dir) / 'test.so')
        )

        # Matches include, also exclude -> should not process
        self.assertFalse(
            self.scanner._should_process_file(Path(self.test_dir) / 'test.debug')
        )

        # Doesn't match include -> should not process
        self.assertFalse(
            self.scanner._should_process_file(Path(self.test_dir) / 'test.exe')
        )


class TestBasicScanning(unittest.TestCase):
    """Test basic directory scanning functionality."""

    def setUp(self):
        """Create temporary directory with test files."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files and directories."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_scan_empty_directory(self):
        """Test scanning an empty directory."""
        scanner = DirectoryScanner(self.test_dir)
        results = scanner.scan()
        self.assertEqual(len(results), 0)
        self.assertIsInstance(results, list)

    def test_scan_directory_with_only_text_files(self):
        """Test scanning directory with only text files."""
        # Create text files
        for i in range(3):
            with open(os.path.join(self.test_dir, f'text{i}.txt'), 'w') as f:
                f.write('This is a text file\n')

        scanner = DirectoryScanner(self.test_dir)
        results = scanner.scan()
        self.assertEqual(len(results), 0)

    def test_scan_directory_with_binary_files(self):
        """Test scanning directory with binary files."""
        # Create ELF binary file
        elf_file = os.path.join(self.test_dir, 'test.so')
        with open(elf_file, 'wb') as f:
            f.write(b'\x7fELF')
            f.write(b'\x00' * 100)

        # Create PE binary file
        pe_file = os.path.join(self.test_dir, 'test.exe')
        with open(pe_file, 'wb') as f:
            f.write(b'MZ')
            f.write(b'\x00' * 100)

        scanner = DirectoryScanner(self.test_dir)
        results = scanner.scan()
        self.assertEqual(len(results), 2)
        self.assertIn(resolve_path(elf_file), results)
        self.assertIn(resolve_path(pe_file), results)

    def test_scan_returns_absolute_paths(self):
        """Test that scan returns absolute paths."""
        # Create binary file
        binary_file = os.path.join(self.test_dir, 'test.so')
        with open(binary_file, 'wb') as f:
            f.write(b'\x7fELF')
            f.write(b'\x00' * 100)

        scanner = DirectoryScanner(self.test_dir)
        results = scanner.scan()
        self.assertEqual(len(results), 1)
        # Result should be absolute path
        self.assertTrue(os.path.isabs(results[0]))


class TestRecursiveTraversal(unittest.TestCase):
    """Test recursive directory traversal."""

    def setUp(self):
        """Create nested directory structure."""
        self.test_dir = tempfile.mkdtemp()
        # Create nested directories
        self.level1 = os.path.join(self.test_dir, 'level1')
        self.level2 = os.path.join(self.level1, 'level2')
        self.level3 = os.path.join(self.level2, 'level3')
        for dir_path in [self.level1, self.level2, self.level3]:
            os.mkdir(dir_path)

    def tearDown(self):
        """Clean up temporary directories."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_scan_finds_files_in_nested_directories(self):
        """Test that scan finds files in deeply nested directories."""
        # Create binary files at different levels
        binary_files = []
        for level, dir_path in [
            (0, self.test_dir),
            (1, self.level1),
            (2, self.level2),
            (3, self.level3)
        ]:
            file_path = os.path.join(dir_path, f'binary{level}.so')
            with open(file_path, 'wb') as f:
                f.write(b'\x7fELF')
                f.write(b'\x00' * 100)
            binary_files.append(file_path)

        scanner = DirectoryScanner(self.test_dir)
        results = scanner.scan()

        # Should find all 4 binary files
        self.assertEqual(len(results), 4)
        for binary_file in binary_files:
            self.assertIn(resolve_path(binary_file), results)

    def test_scan_mixed_nested_structure(self):
        """Test scanning directory with mixed files and nesting."""
        # Create binary files in various directories
        binary_in_root = os.path.join(self.test_dir, 'root.so')
        with open(binary_in_root, 'wb') as f:
            f.write(b'\x7fELF')
            f.write(b'\x00' * 100)

        binary_in_nested = os.path.join(self.level3, 'nested.so')
        with open(binary_in_nested, 'wb') as f:
            f.write(b'\x7fELF')
            f.write(b'\x00' * 100)

        # Create text files
        for i in range(2):
            text_file = os.path.join(self.level1, f'text{i}.txt')
            with open(text_file, 'w') as f:
                f.write('text content')

        scanner = DirectoryScanner(self.test_dir)
        results = scanner.scan()

        # Should find only the 2 binary files
        self.assertEqual(len(results), 2)
        self.assertIn(resolve_path(binary_in_root), results)
        self.assertIn(resolve_path(binary_in_nested), results)


class TestIncludeFiltering(unittest.TestCase):
    """Test include pattern filtering during scanning."""

    def setUp(self):
        """Create temporary directory with various file types."""
        self.test_dir = tempfile.mkdtemp()

        # Create different binary file types
        self.elf_file = os.path.join(self.test_dir, 'test.so')
        with open(self.elf_file, 'wb') as f:
            f.write(b'\x7fELF')
            f.write(b'\x00' * 100)

        self.pe_file = os.path.join(self.test_dir, 'test.exe')
        with open(self.pe_file, 'wb') as f:
            f.write(b'MZ')
            f.write(b'\x00' * 100)

        self.macho_file = os.path.join(self.test_dir, 'test.dylib')
        with open(self.macho_file, 'wb') as f:
            f.write(b'\xce\xfa\xed\xfe')
            f.write(b'\x00' * 100)

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_include_pattern_filters_by_extension(self):
        """Test that include pattern filters by file extension."""
        scanner = DirectoryScanner(self.test_dir, include_patterns=['*.so'])
        results = scanner.scan()

        # Should only find .so file
        self.assertEqual(len(results), 1)
        self.assertIn(resolve_path(self.elf_file), results)
        self.assertNotIn(resolve_path(self.pe_file), results)
        self.assertNotIn(resolve_path(self.macho_file), results)

    def test_include_pattern_with_multiple_patterns(self):
        """Test include pattern with multiple patterns."""
        scanner = DirectoryScanner(
            self.test_dir,
            include_patterns=['*.so', '*.exe']
        )
        results = scanner.scan()

        # Should find .so and .exe files
        self.assertEqual(len(results), 2)
        self.assertIn(resolve_path(self.elf_file), results)
        self.assertIn(resolve_path(self.pe_file), results)
        self.assertNotIn(resolve_path(self.macho_file), results)

    def test_include_pattern_with_wildcards(self):
        """Test include pattern with wildcard matching."""
        scanner = DirectoryScanner(self.test_dir, include_patterns=['test.*'])
        results = scanner.scan()

        # Should find all files matching pattern
        self.assertEqual(len(results), 3)

    def test_include_none_includes_all(self):
        """Test that None include pattern includes all files."""
        scanner = DirectoryScanner(self.test_dir, include_patterns=None)
        results = scanner.scan()

        # Should find all binary files
        self.assertEqual(len(results), 3)


class TestExcludeFiltering(unittest.TestCase):
    """Test exclude pattern filtering during scanning."""

    def setUp(self):
        """Create temporary directory with binary files."""
        self.test_dir = tempfile.mkdtemp()

        # Create binary files
        self.so_file = os.path.join(self.test_dir, 'lib.so')
        with open(self.so_file, 'wb') as f:
            f.write(b'\x7fELF')
            f.write(b'\x00' * 100)

        self.debug_file = os.path.join(self.test_dir, 'lib.debug')
        with open(self.debug_file, 'wb') as f:
            f.write(b'\x7fELF')
            f.write(b'\x00' * 100)

        self.exe_file = os.path.join(self.test_dir, 'app.exe')
        with open(self.exe_file, 'wb') as f:
            f.write(b'MZ')
            f.write(b'\x00' * 100)

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_exclude_pattern_filters_files(self):
        """Test that exclude pattern filters out files."""
        scanner = DirectoryScanner(self.test_dir, exclude_patterns=['*.debug'])
        results = scanner.scan()

        # Should exclude .debug file
        self.assertEqual(len(results), 2)
        self.assertIn(resolve_path(self.so_file), results)
        self.assertNotIn(resolve_path(self.debug_file), results)
        self.assertIn(resolve_path(self.exe_file), results)

    def test_exclude_pattern_with_multiple_patterns(self):
        """Test exclude pattern with multiple patterns."""
        scanner = DirectoryScanner(
            self.test_dir,
            exclude_patterns=['*.debug', '*.exe']
        )
        results = scanner.scan()

        # Should exclude .debug and .exe files
        self.assertEqual(len(results), 1)
        self.assertIn(resolve_path(self.so_file), results)
        self.assertNotIn(resolve_path(self.debug_file), results)
        self.assertNotIn(resolve_path(self.exe_file), results)

    def test_exclude_empty_list_excludes_none(self):
        """Test that empty exclude list excludes nothing."""
        scanner = DirectoryScanner(self.test_dir, exclude_patterns=[])
        results = scanner.scan()

        # Should find all files
        self.assertEqual(len(results), 3)


class TestCombinedFiltering(unittest.TestCase):
    """Test combined include and exclude filtering."""

    def setUp(self):
        """Create temporary directory with various files."""
        self.test_dir = tempfile.mkdtemp()

        # Create binary files
        self.lib_so = os.path.join(self.test_dir, 'lib.so')
        with open(self.lib_so, 'wb') as f:
            f.write(b'\x7fELF')
            f.write(b'\x00' * 100)

        self.lib_debug = os.path.join(self.test_dir, 'lib.debug')
        with open(self.lib_debug, 'wb') as f:
            f.write(b'\x7fELF')
            f.write(b'\x00' * 100)

        self.app_exe = os.path.join(self.test_dir, 'app.exe')
        with open(self.app_exe, 'wb') as f:
            f.write(b'MZ')
            f.write(b'\x00' * 100)

        self.test_dll = os.path.join(self.test_dir, 'test.dll')
        with open(self.test_dll, 'wb') as f:
            f.write(b'MZ')
            f.write(b'\x00' * 100)

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_include_and_exclude_combined(self):
        """Test that include and exclude patterns work together."""
        scanner = DirectoryScanner(
            self.test_dir,
            include_patterns=['*.so', '*.exe', '*.dll'],
            exclude_patterns=['*.debug']
        )
        results = scanner.scan()

        # Should include .so, .exe, .dll but exclude .debug
        self.assertEqual(len(results), 3)
        self.assertIn(resolve_path(self.lib_so), results)
        self.assertNotIn(resolve_path(self.lib_debug), results)
        self.assertIn(resolve_path(self.app_exe), results)
        self.assertIn(resolve_path(self.test_dll), results)

    def test_include_only_some_then_exclude(self):
        """Test include pattern with exclude of subset."""
        scanner = DirectoryScanner(
            self.test_dir,
            include_patterns=['*.*'],
            exclude_patterns=['*.debug']
        )
        results = scanner.scan()

        # Should include all with extensions except .debug
        self.assertEqual(len(results), 3)


class TestScanDirectoryFunction(unittest.TestCase):
    """Test the convenience scan_directory function."""

    def setUp(self):
        """Create temporary directory with test files."""
        self.test_dir = tempfile.mkdtemp()

        # Create binary file
        self.binary_file = os.path.join(self.test_dir, 'test.so')
        with open(self.binary_file, 'wb') as f:
            f.write(b'\x7fELF')
            f.write(b'\x00' * 100)

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_scan_directory_returns_list(self):
        """Test that scan_directory returns a list."""
        results = scan_directory(self.test_dir)
        self.assertIsInstance(results, list)

    def test_scan_directory_finds_binaries(self):
        """Test that scan_directory finds binary files."""
        results = scan_directory(self.test_dir)
        self.assertEqual(len(results), 1)
        self.assertIn(resolve_path(self.binary_file), results)

    def test_scan_directory_with_patterns(self):
        """Test scan_directory with include/exclude patterns."""
        # Create additional files
        exe_file = os.path.join(self.test_dir, 'test.exe')
        with open(exe_file, 'wb') as f:
            f.write(b'MZ')
            f.write(b'\x00' * 100)

        results = scan_directory(self.test_dir, include_patterns=['*.so'])
        self.assertEqual(len(results), 1)
        self.assertIn(resolve_path(self.binary_file), results)

    def test_scan_directory_with_invalid_directory(self):
        """Test that scan_directory raises ValueError for invalid directory."""
        with self.assertRaises(ValueError):
            scan_directory('/nonexistent/directory')


class TestVerboseMode(unittest.TestCase):
    """Test verbose mode output."""

    def setUp(self):
        """Create temporary directory with test files."""
        self.test_dir = tempfile.mkdtemp()

        # Create binary file
        self.binary_file = os.path.join(self.test_dir, 'test.so')
        with open(self.binary_file, 'wb') as f:
            f.write(b'\x7fELF')
            f.write(b'\x00' * 100)

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch('builtins.print')
    def test_verbose_mode_shows_output(self, mock_print):
        """Test that verbose mode produces output."""
        scanner = DirectoryScanner(self.test_dir, verbose=True)
        results = scanner.scan()

        # Should have called print with verbose messages
        self.assertTrue(len(mock_print.call_args_list) > 0)

        # Check that verbose prefix is present
        verbose_calls = [
            call for call in mock_print.call_args_list
            if '[VERBOSE]' in str(call)
        ]
        self.assertTrue(len(verbose_calls) > 0)

    @patch('builtins.print')
    def test_non_verbose_mode_silent(self, mock_print):
        """Test that non-verbose mode is silent."""
        scanner = DirectoryScanner(self.test_dir, verbose=False)
        results = scanner.scan()

        # Should not have called print
        self.assertEqual(len(mock_print.call_args_list), 0)


class TestFixtureScanning(unittest.TestCase):
    """Test scanner using actual fixture files."""

    @classmethod
    def setUpClass(cls):
        """Get the path to the fixtures directory."""
        cls.fixtures_dir = os.path.join(
            os.path.dirname(__file__), 'fixtures'
        )

    def test_scan_binaries_directory(self):
        """Test scanning the binaries fixture directory."""
        binaries_dir = os.path.join(self.fixtures_dir, 'binaries')
        if not os.path.exists(binaries_dir):
            self.skipTest('Binaries fixtures directory not found')

        scanner = DirectoryScanner(binaries_dir)
        results = scanner.scan()

        # Should find multiple binary files
        self.assertGreater(len(results), 0)

        # All results should be valid paths
        for result in results:
            self.assertTrue(os.path.exists(result))
            self.assertTrue(os.path.isfile(result))

    def test_scan_text_directory_finds_no_binaries(self):
        """Test scanning the text fixture directory finds no binaries."""
        text_dir = os.path.join(self.fixtures_dir, 'text')
        if not os.path.exists(text_dir):
            self.skipTest('Text fixtures directory not found')

        scanner = DirectoryScanner(text_dir)
        results = scanner.scan()

        # Should find no binary files
        self.assertEqual(len(results), 0)

    def test_scan_config_directory_finds_no_binaries(self):
        """Test scanning the config fixture directory finds no binaries."""
        config_dir = os.path.join(self.fixtures_dir, 'config')
        if not os.path.exists(config_dir):
            self.skipTest('Config fixtures directory not found')

        scanner = DirectoryScanner(config_dir)
        results = scanner.scan()

        # Should find no binary files
        self.assertEqual(len(results), 0)

    def test_scan_mixed_directory_filters_correctly(self):
        """Test scanning mixed directory correctly filters binary vs non-binary."""
        mixed_dir = os.path.join(self.fixtures_dir, 'mixed')
        if not os.path.exists(mixed_dir):
            self.skipTest('Mixed fixtures directory not found')

        scanner = DirectoryScanner(mixed_dir)
        results = scanner.scan()

        # Should find some binaries (binary.elf and app.exe)
        self.assertGreater(len(results), 0)

        # Verify binary files are found
        binary_elf = os.path.join(mixed_dir, 'binary.elf')
        app_exe = os.path.join(mixed_dir, 'app.exe')

        if os.path.exists(binary_elf):
            self.assertIn(binary_elf, results)
        if os.path.exists(app_exe):
            self.assertIn(app_exe, results)

        # Text/config files should not be in results
        readme_txt = os.path.join(mixed_dir, 'readme.txt')
        config_json = os.path.join(mixed_dir, 'config.json')

        self.assertNotIn(readme_txt, results)
        self.assertNotIn(config_json, results)

    def test_scan_with_include_pattern_on_fixtures(self):
        """Test include pattern filtering on fixture files."""
        binaries_dir = os.path.join(self.fixtures_dir, 'binaries')
        if not os.path.exists(binaries_dir):
            self.skipTest('Binaries fixtures directory not found')

        scanner = DirectoryScanner(binaries_dir, include_patterns=['*.so'])
        results = scanner.scan()

        # Should only find .so files
        for result in results:
            self.assertTrue(result.endswith('.so'))

    def test_scan_with_exclude_pattern_on_fixtures(self):
        """Test exclude pattern filtering on fixture files."""
        binaries_dir = os.path.join(self.fixtures_dir, 'binaries')
        if not os.path.exists(binaries_dir):
            self.skipTest('Binaries fixtures directory not found')

        scanner = DirectoryScanner(binaries_dir, exclude_patterns=['*.exe', '*.dll'])
        results = scanner.scan()

        # Should not find .exe or .dll files
        for result in results:
            self.assertFalse(result.endswith('.exe'))
            self.assertFalse(result.endswith('.dll'))

    def test_scan_deeply_nested_fixtures(self):
        """Test scanning finds files in deeply nested fixture directories."""
        binaries_dir = os.path.join(self.fixtures_dir, 'binaries')
        if not os.path.exists(binaries_dir):
            self.skipTest('Binaries fixtures directory not found')

        scanner = DirectoryScanner(binaries_dir)
        results = scanner.scan()

        # Check for deeply nested binary file
        deep_binary = os.path.join(
            binaries_dir, 'deep', 'level1', 'level2', 'level3', 'deep_binary.so'
        )

        if os.path.exists(deep_binary):
            self.assertIn(deep_binary, results)


class TestSymlinkHandling(unittest.TestCase):
    """Test symbolic link handling functionality."""

    def setUp(self):
        """Create temporary directory with test files and symlinks."""
        self.test_dir = tempfile.mkdtemp()
        self.fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')

        # Create actual binary and text files
        self.binary_file = os.path.join(self.test_dir, 'actual_binary.so')
        with open(self.binary_file, 'wb') as f:
            f.write(b'\x7f\x45\x4c\x46')  # ELF magic
            f.write(b'\x00' * 100)

        self.text_file = os.path.join(self.test_dir, 'actual_text.txt')
        with open(self.text_file, 'w') as f:
            f.write('This is a text file')

        # Create symlinks
        self.symlink_to_binary = os.path.join(self.test_dir, 'link_to_binary.so')
        self.symlink_to_text = os.path.join(self.test_dir, 'link_to_text.txt')
        self.broken_symlink = os.path.join(self.test_dir, 'broken_link')

        try:
            os.symlink(self.binary_file, self.symlink_to_binary)
            os.symlink(self.text_file, self.symlink_to_text)
            os.symlink('/nonexistent/path', self.broken_symlink)
        except OSError:
            # Skip tests if symlinks are not supported
            self.symlinks_supported = False
        else:
            self.symlinks_supported = True

    def tearDown(self):
        """Clean up temporary files and directories."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_initialization_with_follow_symlinks_false(self):
        """Test scanner initialization with follow_symlinks=False (default)."""
        scanner = DirectoryScanner(self.test_dir, follow_symlinks=False)
        self.assertFalse(scanner.follow_symlinks)

    def test_initialization_with_follow_symlinks_true(self):
        """Test scanner initialization with follow_symlinks=True."""
        scanner = DirectoryScanner(self.test_dir, follow_symlinks=True)
        self.assertTrue(scanner.follow_symlinks)

    def test_scan_skips_symlinks_by_default(self):
        """Test that scan skips symlinks when follow_symlinks=False (default)."""
        if not self.symlinks_supported:
            self.skipTest('Symbolic links not supported on this system')

        scanner = DirectoryScanner(self.test_dir, follow_symlinks=False)
        results = scanner.scan()

        # Should find the actual binary file
        self.assertIn(resolve_path(self.binary_file), results)

        # Should NOT find the symlink (even though it points to a binary)
        self.assertNotIn(self.symlink_to_binary, results)

    def test_scan_follows_symlinks_when_enabled(self):
        """Test that scan follows symlinks when follow_symlinks=True."""
        if not self.symlinks_supported:
            self.skipTest('Symbolic links not supported on this system')

        scanner = DirectoryScanner(self.test_dir, follow_symlinks=True)
        results = scanner.scan()

        # Should find the actual binary file
        self.assertIn(resolve_path(self.binary_file), results)

        # Should also find the symlink (it resolves to the binary)
        # The resolved path should be in results
        resolved_link = str(Path(self.symlink_to_binary).resolve())
        self.assertIn(resolved_link, results)

    def test_scan_skips_broken_symlinks(self):
        """Test that broken symlinks are skipped even with follow_symlinks=True."""
        if not self.symlinks_supported:
            self.skipTest('Symbolic links not supported on this system')

        scanner = DirectoryScanner(self.test_dir, follow_symlinks=True)
        results = scanner.scan()

        # Broken symlink should not be in results
        self.assertNotIn(self.broken_symlink, results)

    def test_scan_with_symlink_fixtures(self):
        """Test scanning with actual symlink fixtures."""
        symlinks_dir = os.path.join(self.fixtures_dir, 'symlinks')
        if not os.path.exists(symlinks_dir):
            self.skipTest('Symlinks fixtures directory not found')

        # Test without following symlinks (default)
        scanner = DirectoryScanner(symlinks_dir, follow_symlinks=False)
        results = scanner.scan()

        # Should find 0 binary files (symlinks are skipped)
        # Note: The symlinks point to binaries but are not followed
        self.assertEqual(len(results), 0)

        # Test with following symlinks
        scanner = DirectoryScanner(symlinks_dir, follow_symlinks=True)
        results = scanner.scan()

        # Should find binary files through symlinks
        # link_to_lib.so points to ../binaries/lib/libtest.so (binary)
        # link_to_app points to ../binaries/bin/testapp (binary)
        # link_to_readme.txt points to ../text/readme.txt (text, not binary)
        # broken_link points to nonexistent (skipped)
        # So we should find 2 binaries
        self.assertGreater(len(results), 0)

    def test_scan_directory_function_with_follow_symlinks(self):
        """Test scan_directory convenience function with follow_symlinks parameter."""
        if not self.symlinks_supported:
            self.skipTest('Symbolic links not supported on this system')

        # Test with follow_symlinks=False
        results = scan_directory(self.test_dir, follow_symlinks=False)
        self.assertIn(resolve_path(self.binary_file), results)
        self.assertNotIn(self.symlink_to_binary, results)

        # Test with follow_symlinks=True
        results = scan_directory(self.test_dir, follow_symlinks=True)
        self.assertIn(resolve_path(self.binary_file), results)
        resolved_link = str(Path(self.symlink_to_binary).resolve())
        self.assertIn(resolved_link, results)

    def test_verbose_mode_shows_symlink_skips(self):
        """Test that verbose mode shows when symlinks are skipped."""
        if not self.symlinks_supported:
            self.skipTest('Symbolic links not supported on this system')

        from io import StringIO

        scanner = DirectoryScanner(self.test_dir, follow_symlinks=False, verbose=True)
        captured_output = StringIO()

        with patch('sys.stdout', captured_output):
            results = scanner.scan()

        output = captured_output.getvalue()
        # Should show that symlinks were skipped
        self.assertIn('symlink', output.lower())


class TestProgressIndicator(unittest.TestCase):
    """Test progress indicator during directory scanning."""

    def setUp(self):
        """Create temporary directories with files for testing."""
        self.test_dir = tempfile.mkdtemp()
        self.fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')

        # Create multiple test files to trigger progress updates
        for i in range(10):
            # Create text files (will be skipped but still counted)
            with open(os.path.join(self.test_dir, f'file{i}.txt'), 'w') as f:
                f.write('test content')

    def tearDown(self):
        """Clean up temporary directories."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_progress_indicator_disabled_with_zero_interval(self):
        """Test that progress indicator can be disabled with progress_interval=0."""
        from io import StringIO

        scanner = DirectoryScanner(self.test_dir)
        captured_stderr = StringIO()

        with patch('sys.stderr', captured_stderr):
            results = scanner.scan(progress_interval=0)

        stderr_output = captured_stderr.getvalue()
        # Should not show any progress messages
        self.assertNotIn('Scanning...', stderr_output)

    def test_progress_indicator_disabled_in_verbose_mode(self):
        """Test that progress indicator is disabled in verbose mode."""
        from io import StringIO

        scanner = DirectoryScanner(self.test_dir, verbose=True)
        captured_stderr = StringIO()

        with patch('sys.stderr', captured_stderr):
            results = scanner.scan(progress_interval=5)

        stderr_output = captured_stderr.getvalue()
        # Should not show progress indicator in stderr in verbose mode
        # (verbose mode shows detailed output in stdout instead)
        self.assertNotIn('Scanning...', stderr_output)

    def test_progress_indicator_shows_initial_message(self):
        """Test that progress indicator shows initial message."""
        from io import StringIO

        scanner = DirectoryScanner(self.test_dir)
        captured_stderr = StringIO()

        with patch('sys.stderr', captured_stderr):
            results = scanner.scan(progress_interval=5)

        stderr_output = captured_stderr.getvalue()
        # Should show initial progress message
        self.assertIn('Scanning...', stderr_output)
        self.assertIn('files processed', stderr_output)

    def test_progress_indicator_updates_during_scan(self):
        """Test that progress indicator updates during scanning."""
        from io import StringIO

        # Create more files to trigger multiple progress updates
        for i in range(10, 25):
            with open(os.path.join(self.test_dir, f'file{i}.txt'), 'w') as f:
                f.write('test content')

        scanner = DirectoryScanner(self.test_dir)
        captured_stderr = StringIO()

        # Use small interval to trigger multiple updates
        with patch('sys.stderr', captured_stderr):
            results = scanner.scan(progress_interval=10)

        stderr_output = captured_stderr.getvalue()
        # Should show progress messages
        self.assertIn('Scanning...', stderr_output)
        # Should have carriage return for in-place updates
        self.assertIn('\r', stderr_output)

    def test_progress_indicator_shows_final_count(self):
        """Test that progress indicator shows final file count."""
        from io import StringIO

        scanner = DirectoryScanner(self.test_dir)
        captured_stderr = StringIO()

        with patch('sys.stderr', captured_stderr):
            results = scanner.scan(progress_interval=5)

        stderr_output = captured_stderr.getvalue()
        # Should show final count (should be 10 files from setUp)
        self.assertIn('Scanning...', stderr_output)
        # The final message should include the total count
        # The last line should end with a newline, not \r
        lines = stderr_output.strip().split('\r')
        final_line = lines[-1].strip()
        self.assertIn('files processed', final_line)

    def test_progress_indicator_with_scan_directory_function(self):
        """Test progress indicator through scan_directory convenience function."""
        from io import StringIO

        captured_stderr = StringIO()

        with patch('sys.stderr', captured_stderr):
            results = scan_directory(self.test_dir, progress_interval=5)

        stderr_output = captured_stderr.getvalue()
        # Should show progress messages
        self.assertIn('Scanning...', stderr_output)
        self.assertIn('files processed', stderr_output)

    def test_progress_indicator_default_interval(self):
        """Test that default progress_interval is 100."""
        scanner = DirectoryScanner(self.test_dir)

        # Test that we can call scan() without specifying progress_interval
        # and it should work without errors
        from io import StringIO

        captured_stderr = StringIO()
        with patch('sys.stderr', captured_stderr):
            results = scanner.scan()  # Uses default progress_interval=100

        # With only 10-25 files, default interval of 100 won't trigger updates
        # but should still show initial and final messages
        stderr_output = captured_stderr.getvalue()
        self.assertIn('Scanning...', stderr_output)

    def test_progress_indicator_on_fixtures_directory(self):
        """Test progress indicator on actual fixtures directory."""
        if not os.path.exists(self.fixtures_dir):
            self.skipTest('Fixtures directory not found')

        from io import StringIO

        binaries_dir = os.path.join(self.fixtures_dir, 'binaries')
        if not os.path.exists(binaries_dir):
            self.skipTest('Binaries fixtures directory not found')

        captured_stderr = StringIO()

        with patch('sys.stderr', captured_stderr):
            results = scan_directory(binaries_dir, progress_interval=10)

        stderr_output = captured_stderr.getvalue()
        # Should show progress messages
        self.assertIn('Scanning...', stderr_output)
        self.assertIn('files processed', stderr_output)


if __name__ == '__main__':
    unittest.main()
