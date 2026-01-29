"""
Unit tests for the binary analyzer module.

Tests format detection, metadata extraction, and error handling.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from binary_sbom.analyzer import (
    BinaryAnalysisError,
    _detect_format,
    _extract_metadata,
    analyze_binary,
    detect_format,
    extract_metadata,
)


class TestAnalyzeBinary:
    """Test binary analysis functionality."""

    @patch('binary_sbom.analyzer.lief')
    def test_analyze_binary_without_lief(self, mock_lief):
        """Test that missing LIEF raises ImportError."""
        with patch('binary_sbom.analyzer.lief', None):
            with pytest.raises(ImportError, match='LIEF library is required'):
                analyze_binary('test.bin')

    @patch('binary_sbom.analyzer.lief')
    def test_analyze_binary_file_not_found(self, mock_lief):
        """Test that non-existent file raises FileNotFoundError."""
        mock_lief.parse.return_value = MagicMock()
        with pytest.raises(FileNotFoundError, match='Binary file not found'):
            analyze_binary('/nonexistent/file.bin')

    @patch('binary_sbom.analyzer.lief')
    def test_analyze_binary_path_is_directory(self, mock_lief):
        """Test that directory path raises BinaryAnalysisError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_lief.parse.return_value = MagicMock()
            with pytest.raises(BinaryAnalysisError, match='Path is not a file'):
                analyze_binary(tmpdir)

    @patch('binary_sbom.analyzer.lief')
    def test_analyze_binary_permission_denied(self, mock_lief):
        """Test that unreadable file raises BinaryAnalysisError."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name

        try:
            # Make file unreadable
            os.chmod(temp_path, 0o000)
            mock_lief.parse.return_value = MagicMock()

            with pytest.raises(BinaryAnalysisError, match='Permission denied'):
                analyze_binary(temp_path)
        finally:
            # Restore permissions for cleanup
            os.chmod(temp_path, 0o644)
            os.unlink(temp_path)

    @patch('binary_sbom.analyzer.lief')
    def test_analyze_binary_empty_file(self, mock_lief):
        """Test that empty file raises BinaryAnalysisError."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name

        try:
            # Truncate to empty
            with open(temp_path, 'w') as f:
                f.write('')
            mock_lief.parse.return_value = MagicMock()

            with pytest.raises(BinaryAnalysisError, match='File is empty'):
                analyze_binary(temp_path)
        finally:
            os.unlink(temp_path)

    @patch('binary_sbom.analyzer.lief')
    def test_analyze_binary_file_too_large(self, mock_lief):
        """Test that file exceeding max size raises BinaryAnalysisError."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            # Write 1 MB of data
            f.write(b'x' * (1024 * 1024))
            temp_path = f.name

        try:
            mock_lief.parse.return_value = MagicMock()

            with pytest.raises(BinaryAnalysisError, match='File too large'):
                analyze_binary(temp_path, max_file_size_mb=0.5)
        finally:
            os.unlink(temp_path)

    @patch('binary_sbom.analyzer.lief')
    def test_analyze_binary_lief_parse_returns_none(self, mock_lief):
        """Test that LIEF returning None raises BinaryAnalysisError."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'some binary content')
            temp_path = f.name

        try:
            mock_lief.parse.return_value = None

            with pytest.raises(
                BinaryAnalysisError, match='Failed to parse binary file'
            ):
                analyze_binary(temp_path)
        finally:
            os.unlink(temp_path)

    @patch('binary_sbom.analyzer.lief')
    def test_analyze_binary_memory_error(self, mock_lief):
        """Test that MemoryError during parsing is handled."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'some binary content')
            temp_path = f.name

        try:
            mock_lief.parse.side_effect = MemoryError('Out of memory')

            with pytest.raises(BinaryAnalysisError, match='File too large to parse'):
                analyze_binary(temp_path)
        finally:
            os.unlink(temp_path)

    @patch('binary_sbom.analyzer.lief')
    def test_analyze_binary_io_error(self, mock_lief):
        """Test that IOError during parsing is handled."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'some binary content')
            temp_path = f.name

        try:
            mock_lief.parse.side_effect = IOError('Read failed')

            with pytest.raises(BinaryAnalysisError, match='Read error while parsing'):
                analyze_binary(temp_path)
        finally:
            os.unlink(temp_path)

    @patch('binary_sbom.analyzer.lief')
    def test_analyze_binary_corrupted_file(self, mock_lief):
        """Test that corrupted file error is detected."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'some binary content')
            temp_path = f.name

        try:
            mock_lief.parse.side_effect = Exception('File is corrupted')

            with pytest.raises(BinaryAnalysisError, match='Corrupted binary file'):
                analyze_binary(temp_path)
        finally:
            os.unlink(temp_path)

    @patch('binary_sbom.analyzer.lief')
    def test_analyze_binary_unsupported_format(self, mock_lief):
        """Test that unsupported format error is detected."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'some binary content')
            temp_path = f.name

        try:
            mock_lief.parse.side_effect = Exception('Format not supported')

            with pytest.raises(BinaryAnalysisError, match='Unsupported binary format'):
                analyze_binary(temp_path)
        finally:
            os.unlink(temp_path)

    @patch('binary_sbom.analyzer.lief')
    def test_analyze_binary_success(self, mock_lief):
        """Test successful binary analysis."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'some binary content')
            temp_path = f.name

        try:
            # Create mock binary object
            mock_binary = MagicMock()
            mock_binary.name = 'test_binary'
            mock_binary.entrypoint = 0x400000
            mock_binary.imported_libraries = ['libc.so.6', 'libm.so.6']

            # Create sections with properly configured attributes
            sections = []
            for name, size, vaddr in [('.text', 4096, 0x400000), ('.data', 1024, 0x401000)]:
                section = MagicMock()
                section.configure_mock(name=name, size=size, virtual_address=vaddr)
                sections.append(section)
            mock_binary.sections = sections

            # Mock ELF type
            mock_elf_class = MagicMock
            mock_lief.ELF.Binary = lambda x: isinstance(x, MagicMock)

            mock_lief.parse.return_value = mock_binary

            with patch('binary_sbom.analyzer._detect_format', return_value=('ELF', 'x86_64')):
                metadata = analyze_binary(temp_path)

                assert metadata['name'] == 'test_binary'
                assert metadata['type'] == 'ELF'
                assert metadata['architecture'] == 'x86_64'
                assert metadata['entrypoint'] == hex(0x400000)
                assert len(metadata['dependencies']) == 2
                assert len(metadata['sections']) == 2
        finally:
            os.unlink(temp_path)


class TestDetectFormat:
    """Test format detection functionality."""

    @patch('binary_sbom.analyzer.lief')
    def test_detect_format_without_lief(self, mock_lief):
        """Test that missing LIEF raises ImportError."""
        with patch('binary_sbom.analyzer.lief', None):
            with pytest.raises(ImportError, match='LIEF library is required'):
                detect_format('test.bin')

    @patch('binary_sbom.analyzer.lief')
    def test_detect_format_file_not_found(self, mock_lief):
        """Test that non-existent file raises FileNotFoundError."""
        mock_lief.parse.return_value = MagicMock()
        with pytest.raises(FileNotFoundError, match='Binary file not found'):
            detect_format('/nonexistent/file.bin')

    @patch('binary_sbom.analyzer.lief')
    def test_detect_format_empty_file(self, mock_lief):
        """Test that empty file raises BinaryAnalysisError."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name

        try:
            # Truncate to empty
            with open(temp_path, 'w') as f:
                f.write('')
            mock_lief.parse.return_value = MagicMock()

            with pytest.raises(BinaryAnalysisError, match='File is empty'):
                detect_format(temp_path)
        finally:
            os.unlink(temp_path)

    @patch('binary_sbom.analyzer.lief')
    def test_detect_format_elf_binary(self, mock_lief):
        """Test format detection for ELF binary."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'ELF binary content')
            temp_path = f.name

        try:
            mock_binary = MagicMock()
            mock_lief.parse.return_value = mock_binary
            mock_lief.ELF.Binary = lambda x: isinstance(x, MagicMock)
            mock_binary.header.machine_type = 'EM_X86_64'

            with patch('binary_sbom.analyzer._detect_format', return_value=('ELF', 'EM_X86_64')):
                format_type, arch = detect_format(temp_path)

                assert format_type == 'ELF'
                assert arch == 'EM_X86_64'
        finally:
            os.unlink(temp_path)

    @patch('binary_sbom.analyzer.lief')
    def test_detect_format_pe_binary(self, mock_lief):
        """Test format detection for PE binary."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'PE binary content')
            temp_path = f.name

        try:
            mock_binary = MagicMock()
            mock_lief.parse.return_value = mock_binary
            # Mock that it's not ELF
            mock_lief.ELF.Binary = lambda x: False
            mock_lief.PE.Binary = lambda x: isinstance(x, MagicMock)
            mock_binary.header.machine = 'IMAGE_FILE_MACHINE_AMD64'

            with patch('binary_sbom.analyzer._detect_format', return_value=('PE', 'AMD64')):
                format_type, arch = detect_format(temp_path)

                assert format_type == 'PE'
                assert arch == 'AMD64'
        finally:
            os.unlink(temp_path)

    @patch('binary_sbom.analyzer.lief')
    def test_detect_format_macho_binary(self, mock_lief):
        """Test format detection for MachO binary."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'MachO binary content')
            temp_path = f.name

        try:
            mock_binary = MagicMock()
            mock_lief.parse.return_value = mock_binary
            # Mock that it's not ELF or PE
            mock_lief.ELF.Binary = lambda x: False
            mock_lief.PE.Binary = lambda x: False
            mock_lief.MachO.Binary = lambda x: isinstance(x, MagicMock)
            mock_binary.header.cpu_type = 'CPU_TYPE_X86_64'

            with patch('binary_sbom.analyzer._detect_format', return_value=('MachO', 'CPU_TYPE_X86_64')):
                format_type, arch = detect_format(temp_path)

                assert format_type == 'MachO'
                assert arch == 'CPU_TYPE_X86_64'
        finally:
            os.unlink(temp_path)

    @patch('binary_sbom.analyzer.lief')
    def test_detect_format_raw_binary(self, mock_lief):
        """Test format detection for raw binary."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'raw binary content')
            temp_path = f.name

        try:
            mock_binary = MagicMock()
            mock_lief.parse.return_value = mock_binary
            # Mock that it's not ELF, PE, or MachO
            mock_lief.ELF.Binary = lambda x: False
            mock_lief.PE.Binary = lambda x: False
            mock_lief.MachO.Binary = lambda x: False

            with patch('binary_sbom.analyzer._detect_format', return_value=('Raw', 'unknown')):
                format_type, arch = detect_format(temp_path)

                assert format_type == 'Raw'
                assert arch == 'unknown'
        finally:
            os.unlink(temp_path)


class TestExtractMetadata:
    """Test metadata extraction functionality."""

    @patch('binary_sbom.analyzer._detect_format')
    def test_extract_metadata_basic(self, mock_detect_format):
        """Test basic metadata extraction."""
        mock_detect_format.return_value = ('ELF', 'x86_64')

        mock_binary = MagicMock()
        mock_binary.name = 'test_binary'
        mock_binary.entrypoint = 0x400000

        metadata = extract_metadata(mock_binary, 'test.bin')

        assert metadata['name'] == 'test_binary'
        assert metadata['type'] == 'ELF'
        assert metadata['architecture'] == 'x86_64'
        assert metadata['entrypoint'] == hex(0x400000)
        assert isinstance(metadata['sections'], list)
        assert isinstance(metadata['dependencies'], list)

    @patch('binary_sbom.analyzer._detect_format')
    def test_extract_metadata_with_dependencies(self, mock_detect_format):
        """Test metadata extraction with dependencies."""
        mock_detect_format.return_value = ('ELF', 'x86_64')

        mock_binary = MagicMock()
        mock_binary.name = 'test'
        mock_binary.imported_libraries = ['libc.so.6', 'libm.so.6', 'libpthread.so.0']

        metadata = extract_metadata(mock_binary, 'test.bin')

        assert len(metadata['dependencies']) == 3
        assert 'libc.so.6' in metadata['dependencies']
        assert 'libm.so.6' in metadata['dependencies']
        assert 'libpthread.so.0' in metadata['dependencies']

    @patch('binary_sbom.analyzer._detect_format')
    def test_extract_metadata_with_sections(self, mock_detect_format):
        """Test metadata extraction with sections."""
        mock_detect_format.return_value = ('PE', 'AMD64')

        mock_binary = MagicMock()
        mock_binary.name = 'test.exe'

        # Create sections with properly configured attributes
        sections = []
        for name, size, vaddr in [('.text', 4096, 0x1000), ('.data', 2048, 0x2000), ('.rdata', 1024, 0x3000)]:
            section = MagicMock()
            section.configure_mock(name=name, size=size, virtual_address=vaddr)
            sections.append(section)
        mock_binary.sections = sections

        metadata = extract_metadata(mock_binary, 'test.exe')

        assert len(metadata['sections']) == 3
        assert metadata['sections'][0]['name'] == '.text'
        assert metadata['sections'][0]['size'] == 4096
        assert metadata['sections'][0]['virtual_address'] == hex(0x1000)
        assert metadata['sections'][1]['name'] == '.data'
        assert metadata['sections'][1]['size'] == 2048

    @patch('binary_sbom.analyzer._detect_format')
    def test_extract_metadata_without_name(self, mock_detect_format):
        """Test metadata extraction falls back to file path when binary has no name."""
        mock_detect_format.return_value = ('Raw', 'unknown')

        mock_binary = MagicMock(spec=[])  # No 'name' attribute

        metadata = extract_metadata(mock_binary, '/path/to/binary.bin')

        assert metadata['name'] == '/path/to/binary.bin'

    @patch('binary_sbom.analyzer._detect_format')
    def test_extract_metadata_without_entrypoint(self, mock_detect_format):
        """Test metadata extraction when binary has no entrypoint."""
        mock_detect_format.return_value = ('Raw', 'unknown')

        mock_binary = MagicMock()
        mock_binary.name = 'raw_binary'
        mock_binary.entrypoint = 0

        metadata = extract_metadata(mock_binary, 'raw.bin')

        assert metadata['entrypoint'] is None

    @patch('binary_sbom.analyzer._detect_format')
    def test_extract_metadata_filters_empty_dependencies(self, mock_detect_format):
        """Test that empty strings are filtered from dependencies."""
        mock_detect_format.return_value = ('ELF', 'x86_64')

        mock_binary = MagicMock()
        mock_binary.name = 'test'
        mock_binary.imported_libraries = ['libc.so.6', '', 'libm.so.6', '', '']

        metadata = extract_metadata(mock_binary, 'test.bin')

        assert len(metadata['dependencies']) == 2
        assert 'libc.so.6' in metadata['dependencies']
        assert 'libm.so.6' in metadata['dependencies']
        assert '' not in metadata['dependencies']

    @patch('binary_sbom.analyzer._detect_format')
    def test_extract_metadata_sections_without_virtual_address(self, mock_detect_format):
        """Test metadata extraction when sections lack virtual_address."""
        mock_detect_format.return_value = ('Raw', 'unknown')

        mock_binary = MagicMock()
        mock_binary.name = 'raw'

        # Create section with properly configured attributes (no virtual_address)
        section = MagicMock()
        section.configure_mock(name='.text', size=4096)
        # Remove virtual_address attribute
        del section.virtual_address
        mock_binary.sections = [section]

        metadata = extract_metadata(mock_binary, 'raw.bin')

        assert len(metadata['sections']) == 1
        assert metadata['sections'][0]['name'] == '.text'
        assert 'virtual_address' not in metadata['sections'][0]

    @patch('binary_sbom.analyzer._detect_format')
    def test_extract_metadata_exception_handling(self, mock_detect_format):
        """Test that exceptions during extraction are wrapped."""
        mock_detect_format.side_effect = Exception('Detection failed')

        mock_binary = MagicMock()
        mock_binary.name = 'test'

        with pytest.raises(BinaryAnalysisError, match='Failed to extract metadata'):
            extract_metadata(mock_binary, 'test.bin')


class TestDetectFormatInternal:
    """Test internal _detect_format function."""

    @patch('binary_sbom.analyzer.lief')
    def test_detect_format_internal_elf(self, mock_lief):
        """Test _detect_format for ELF binary."""
        # Create mock class that isinstance will recognize
        class MockELFBinary:
            pass

        mock_binary = MockELFBinary()
        mock_binary.header = MagicMock()
        mock_binary.header.machine_type = 'EM_AARCH64'
        mock_lief.ELF.Binary = MockELFBinary

        format_type, arch = _detect_format(mock_binary)

        assert format_type == 'ELF'
        assert arch == 'EM_AARCH64'

    @patch('binary_sbom.analyzer.lief')
    def test_detect_format_internal_pe(self, mock_lief):
        """Test _detect_format for PE binary."""
        # Create mock class that isinstance will recognize
        class MockPEBinary:
            pass

        mock_binary = MockPEBinary()
        mock_binary.header = MagicMock()
        mock_binary.header.machine = 'IMAGE_FILE_MACHINE_I386'
        mock_lief.ELF.Binary = lambda x: False
        mock_lief.PE.Binary = MockPEBinary

        format_type, arch = _detect_format(mock_binary)

        assert format_type == 'PE'
        assert arch == 'IMAGE_FILE_MACHINE_I386'

    @patch('binary_sbom.analyzer.lief')
    def test_detect_format_internal_macho(self, mock_lief):
        """Test _detect_format for MachO binary."""
        # Create mock class that isinstance will recognize
        class MockMachOBinary:
            pass

        mock_binary = MockMachOBinary()
        mock_binary.header = MagicMock()
        mock_binary.header.cpu_type = 'CPU_TYPE_ARM64'
        mock_lief.ELF.Binary = lambda x: False
        mock_lief.PE.Binary = lambda x: False
        mock_lief.MachO.Binary = MockMachOBinary

        format_type, arch = _detect_format(mock_binary)

        assert format_type == 'MachO'
        assert arch == 'CPU_TYPE_ARM64'

    @patch('binary_sbom.analyzer.lief')
    def test_detect_format_internal_raw(self, mock_lief):
        """Test _detect_format for raw binary."""
        mock_binary = MagicMock()
        # Not ELF, PE, or MachO
        mock_lief.ELF.Binary = lambda x: False
        mock_lief.PE.Binary = lambda x: False
        mock_lief.MachO.Binary = lambda x: False

        format_type, arch = _detect_format(mock_binary)

        assert format_type == 'Raw'
        assert arch == 'unknown'

    @patch('binary_sbom.analyzer.lief')
    def test_detect_format_internal_attribute_error_handling(self, mock_lief):
        """Test _detect_format handles missing attributes gracefully."""
        mock_binary = MagicMock(spec=[])  # No attributes

        # Should fall back to Raw without raising
        format_type, arch = _detect_format(mock_binary)

        assert format_type == 'Raw'
        assert arch == 'unknown'


class TestBinaryAnalysisError:
    """Test BinaryAnalysisError exception."""

    def test_binary_analysis_error_is_exception(self):
        """Test that BinaryAnalysisError is an Exception subclass."""
        assert issubclass(BinaryAnalysisError, Exception)

    def test_binary_analysis_error_can_be_raised(self):
        """Test that BinaryAnalysisError can be raised and caught."""
        with pytest.raises(BinaryAnalysisError):
            raise BinaryAnalysisError("Test error")

    def test_binary_analysis_error_message(self):
        """Test that BinaryAnalysisError preserves error message."""
        error_msg = "Test binary analysis error"
        with pytest.raises(BinaryAnalysisError, match=error_msg):
            raise BinaryAnalysisError(error_msg)
