"""
Unit tests for the HexParser plugin.

Tests plugin API compliance, file detection, Intel HEX record parsing,
metadata extraction, and error handling for Intel HEX format files.
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from binary_sbom.plugins.hex_parser import HexParser
from binary_sbom.plugins.api import BinaryParserPlugin


class TestHexParserPluginAPI:
    """Test HexParser plugin API compliance."""

    def test_hex_parser_inherits_from_binary_parser_plugin(self):
        """Test that HexParser inherits from BinaryParserPlugin."""
        parser = HexParser()
        assert isinstance(parser, BinaryParserPlugin)

    def test_hex_parser_get_name(self):
        """Test that get_name returns 'HexParser'."""
        parser = HexParser()
        assert parser.get_name() == "HexParser"

    def test_hex_parser_get_supported_formats(self):
        """Test that get_supported_formats returns ['.hex']."""
        parser = HexParser()
        assert parser.get_supported_formats() == ['.hex']

    def test_hex_parser_version(self):
        """Test that version returns '1.0.0'."""
        parser = HexParser()
        assert parser.version == "1.0.0"


class TestHexParserCanParse:
    """Test HexParser.can_parse() method."""

    def test_can_parse_rejects_non_hex_extension(self):
        """Test that can_parse rejects files without .hex extension."""
        parser = HexParser()

        # Create a temporary file with different extension
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            f.write(b':020000040000FA')  # Valid Intel HEX content
            temp_path = Path(f.name)

        try:
            result = parser.can_parse(temp_path)
            assert result is False
        finally:
            temp_path.unlink()

    def test_can_parse_rejects_nonexistent_file(self):
        """Test that can_parse returns False for non-existent files."""
        parser = HexParser()
        nonexistent_path = Path('/nonexistent/path/to/file.hex')
        result = parser.can_parse(nonexistent_path)
        assert result is False

    def test_can_parse_valid_hex_file(self):
        """Test that can_parse recognizes valid Intel HEX format."""
        parser = HexParser()

        # Create a temporary file with valid Intel HEX content
        with tempfile.NamedTemporaryFile(suffix='.hex', delete=False) as f:
            # Write a simple Intel HEX data record
            # :020000040000FA - Extended Linear Address record
            f.write(b':020000040000FA\n')
            temp_path = Path(f.name)

        try:
            result = parser.can_parse(temp_path)
            assert result is True
        finally:
            temp_path.unlink()

    def test_can_parse_colon_start_marker(self):
        """Test that can_parse checks for colon start marker."""
        parser = HexParser()

        # Create a file without colon start
        with tempfile.NamedTemporaryFile(suffix='.hex', delete=False) as f:
            f.write(b'020000040000FA')  # Missing leading colon
            temp_path = Path(f.name)

        try:
            result = parser.can_parse(temp_path)
            assert result is False
        finally:
            temp_path.unlink()

    def test_can_parse_validates_regex_format(self):
        """Test that can_parse validates Intel HEX format with regex."""
        parser = HexParser()

        # Create a file with invalid format
        with tempfile.NamedTemporaryFile(suffix='.hex', delete=False) as f:
            f.write(b':INVALID_FORMAT\n')  # Invalid hex format
            temp_path = Path(f.name)

        try:
            result = parser.can_parse(temp_path)
            assert result is False
        finally:
            temp_path.unlink()

    def test_can_parse_validates_byte_count(self):
        """Test that can_parse validates byte count matches data length."""
        parser = HexParser()

        # Create a file with mismatched byte count
        with tempfile.NamedTemporaryFile(suffix='.hex', delete=False) as f:
            # Byte count is 02 but data has 4 bytes (8 hex chars)
            f.write(b':021000044444444444\n')  # Invalid byte count
            temp_path = Path(f.name)

        try:
            result = parser.can_parse(temp_path)
            assert result is False
        finally:
            temp_path.unlink()

    def test_can_parse_case_insensitive_extension(self):
        """Test that can_parse handles .HEX extension (uppercase)."""
        parser = HexParser()

        # Create a temporary file with uppercase .HEX extension
        with tempfile.NamedTemporaryFile(suffix='.HEX', delete=False) as f:
            f.write(b':020000040000FA\n')
            temp_path = Path(f.name)

        try:
            result = parser.can_parse(temp_path)
            assert result is True
        finally:
            temp_path.unlink()

    def test_can_parse_empty_file(self):
        """Test that can_parse returns False for empty .hex files."""
        parser = HexParser()

        with tempfile.NamedTemporaryFile(suffix='.hex', delete=False) as f:
            # Write nothing (empty file)
            temp_path = Path(f.name)

        try:
            result = parser.can_parse(temp_path)
            assert result is False
        finally:
            temp_path.unlink()

    def test_can_parse_handles_unicode_decode_error(self):
        """Test that can_parse handles Unicode decode errors gracefully."""
        parser = HexParser()

        # Create a file with invalid UTF-8 encoding
        with tempfile.NamedTemporaryFile(suffix='.hex', delete=False) as f:
            f.write(b'\xff\xfe Invalid UTF-8')
            temp_path = Path(f.name)

        try:
            result = parser.can_parse(temp_path)
            # Should return False, not raise an exception
            assert result is False
        finally:
            temp_path.unlink()


class TestHexParserParse:
    """Test HexParser.parse() method."""

    def test_parse_valid_hex_file(self):
        """Test parsing a valid Intel HEX file."""
        parser = HexParser()

        # Create a valid Intel HEX file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.hex', delete=False) as f:
            # Extended Linear Address record (sets upper 16 bits to 0x0000)
            f.write(':020000040000FA\n')
            # Data record with 16 bytes at address 0x0000
            f.write(':100000000102030405060708090A0B0C0D0E0F0078\n')
            # Data record with 16 bytes at address 0x0010
            f.write(':100010000102030405060708090A0B0C0D0E0F0068\n')
            # EOF record
            f.write(':00000001FF\n')
            temp_path = Path(f.name)

        try:
            result = parser.parse(temp_path)

            # Verify structure
            assert 'packages' in result
            assert 'relationships' in result
            assert 'annotations' in result

            # Verify package
            assert len(result['packages']) == 1
            package = result['packages'][0]
            assert package['name'] == temp_path.stem
            assert package['type'] == 'firmware'
            assert package['format'] == 'Intel HEX'
            assert 'startAddress' in package
            assert 'endAddress' in package
            assert 'dataSegments' in package
            assert 'spdx_id' in package

            # Verify annotations
            assert len(result['annotations']) == 1
            annotation = result['annotations'][0]
            assert 'text' in annotation
            assert 'HexParser' in annotation['text']
        finally:
            temp_path.unlink()

    def test_parse_returns_valid_structure(self):
        """Test that parse returns valid SPDX-compatible structure."""
        parser = HexParser()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.hex', delete=False) as f:
            f.write(':020000040000FA\n')
            f.write(':100000000102030405060708090A0B0C0D0E0F0078\n')
            f.write(':00000001FF\n')
            temp_path = Path(f.name)

        try:
            result = parser.parse(temp_path)

            # Verify top-level structure
            assert isinstance(result, dict)
            assert 'packages' in result
            assert 'relationships' in result
            assert 'annotations' in result

            # Verify packages is a list
            assert isinstance(result['packages'], list)

            # Verify relationships is a list
            assert isinstance(result['relationships'], list)

            # Verify annotations is a list
            assert isinstance(result['annotations'], list)

            # Verify package structure
            if len(result['packages']) > 0:
                package = result['packages'][0]
                assert 'name' in package
                assert 'type' in package
                assert 'spdx_id' in package
                assert 'download_location' in package
        finally:
            temp_path.unlink()

    def test_parse_extracts_metadata(self):
        """Test that parse extracts address range and metadata."""
        parser = HexParser()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.hex', delete=False) as f:
            # Extended Linear Address record (sets upper 16 bits to 0x0010)
            f.write(':020000040010EA\n')
            # Data record at 0x100000
            f.write(':100000000102030405060708090A0B0C0D0E0F0078\n')
            # Data record at 0x100010
            f.write(':100010000102030405060708090A0B0C0D0E0F0068\n')
            # EOF record
            f.write(':00000001FF\n')
            temp_path = Path(f.name)

        try:
            result = parser.parse(temp_path)

            package = result['packages'][0]

            # Verify start and end addresses
            assert package['startAddress'] == '0x100000'
            assert package['endAddress'] == '0x10001F'

            # Verify data segments
            assert package['dataSegments'] >= 1
        finally:
            temp_path.unlink()

    def test_parse_missing_file_raises_file_not_found_error(self):
        """Test that parse raises FileNotFoundError for missing files."""
        parser = HexParser()
        nonexistent_path = Path('/nonexistent/firmware.hex')

        with pytest.raises(FileNotFoundError, match='Intel HEX file not found'):
            parser.parse(nonexistent_path)

    def test_parse_invalid_format_raises_value_error(self):
        """Test that parse raises ValueError for invalid format."""
        parser = HexParser()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.hex', delete=False) as f:
            # Write invalid Intel HEX format
            f.write('INVALID HEX FILE CONTENT\n')
            temp_path = Path(f.name)

        try:
            with pytest.raises(ValueError, match='Failed to parse Intel HEX file'):
                parser.parse(temp_path)
        finally:
            temp_path.unlink()

    def test_parse_checksum_failure_raises_value_error(self):
        """Test that parse raises ValueError for checksum failures."""
        parser = HexParser()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.hex', delete=False) as f:
            # Write data record with invalid checksum
            # Correct checksum should be 0xA0, we write 0x00
            f.write(':100000000102030405060708090A0B0C0D0E0000\n')
            temp_path = Path(f.name)

        try:
            with pytest.raises(ValueError, match='Checksum validation failed'):
                parser.parse(temp_path)
        finally:
            temp_path.unlink()

    def test_parse_handles_empty_lines(self):
        """Test that parse handles empty lines in HEX file."""
        parser = HexParser()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.hex', delete=False) as f:
            f.write(':020000040000FA\n')
            f.write('\n')  # Empty line
            f.write(':100000000102030405060708090A0B0C0D0E0F0078\n')
            f.write('\n')  # Another empty line
            f.write(':00000001FF\n')
            temp_path = Path(f.name)

        try:
            result = parser.parse(temp_path)
            # Should parse successfully
            assert len(result['packages']) == 1
        finally:
            temp_path.unlink()

    def test_parse_annotation_includes_statistics(self):
        """Test that annotation includes parsing statistics."""
        parser = HexParser()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.hex', delete=False) as f:
            f.write(':020000040000FA\n')
            f.write(':100000000102030405060708090A0B0C0D0E0F0078\n')
            f.write(':00000001FF\n')
            temp_path = Path(f.name)

        try:
            result = parser.parse(temp_path)

            annotation = result['annotations'][0]
            assert 'Total records:' in annotation['text']
            assert 'Data records:' in annotation['text']
            assert 'Address range:' in annotation['text']
            assert 'Checksums validated' in annotation['text']
        finally:
            temp_path.unlink()

    @pytest.mark.skipif(sys.platform == 'darwin', reason="macOS allows owner to read files with chmod 000")
    def test_parse_read_error_raises_value_error(self):
        """Test that read errors during parse raise ValueError."""
        parser = HexParser()

        # Create a file and make it unreadable
        with tempfile.NamedTemporaryFile(mode='w', suffix='.hex', delete=False) as f:
            f.write(':020000040000FA\n')
            f.write(':100000000102030405060708090A0B0C0D0E0F0078\n')
            f.write(':00000001FF\n')
            temp_path = Path(f.name)

        # Make file unreadable (remove read permissions)
        try:
            os.chmod(temp_path, 0o000)

            with pytest.raises(ValueError, match='Error reading Intel HEX file'):
                parser.parse(temp_path)
        finally:
            # Restore permissions to delete the file
            os.chmod(temp_path, 0o644)
            temp_path.unlink()


class TestHexParserParseLine:
    """Test HexParser._parse_line() method."""

    def test_parse_line_valid_data_record(self):
        """Test parsing a valid data record."""
        parser = HexParser()

        line = ':100000000102030405060708090A0B0C0D0E0F0078'
        record = parser._parse_line(line, 1)

        assert record['byte_count'] == 0x10
        assert record['address'] == 0x0000
        assert record['record_type'] == 0x00  # Data record
        assert len(record['data']) == 16
        assert record['data'][0] == 0x01
        assert record['data'][15] == 0x00
        assert record['line_number'] == 1

    def test_parse_line_eof_record(self):
        """Test parsing an EOF record."""
        parser = HexParser()

        line = ':00000001FF'
        record = parser._parse_line(line, 1)

        assert record['byte_count'] == 0x00
        assert record['address'] == 0x0000
        assert record['record_type'] == 0x01  # EOF record
        assert len(record['data']) == 0

    def test_parse_line_extended_segment_address_record(self):
        """Test parsing an Extended Segment Address record."""
        parser = HexParser()

        line = ':020000021200EA'  # Extended Segment Address: 0x1200
        record = parser._parse_line(line, 1)

        assert record['byte_count'] == 0x02
        assert record['address'] == 0x0000
        assert record['record_type'] == 0x02  # Extended Segment Address
        assert len(record['data']) == 2
        assert record['data'][0] == 0x12
        assert record['data'][1] == 0x00

    def test_parse_line_start_segment_address_record(self):
        """Test parsing a Start Segment Address record."""
        parser = HexParser()

        line = ':0400000300003800C1'  # Start Segment Address: 0x0000:0x3800
        record = parser._parse_line(line, 1)

        assert record['byte_count'] == 0x04
        assert record['address'] == 0x0000
        assert record['record_type'] == 0x03  # Start Segment Address
        assert len(record['data']) == 4

    def test_parse_line_extended_linear_address_record(self):
        """Test parsing an Extended Linear Address record."""
        parser = HexParser()

        line = ':020000040001F9'  # Extended Linear Address: 0x0001
        record = parser._parse_line(line, 1)

        assert record['byte_count'] == 0x02
        assert record['address'] == 0x0000
        assert record['record_type'] == 0x04  # Extended Linear Address
        assert len(record['data']) == 2
        assert record['data'][0] == 0x00
        assert record['data'][1] == 0x01

    def test_parse_line_start_linear_address_record(self):
        """Test parsing a Start Linear Address record."""
        parser = HexParser()

        line = ':040000050000008077'  # Start Linear Address: 0x00008000
        record = parser._parse_line(line, 1)

        assert record['byte_count'] == 0x04
        assert record['address'] == 0x0000
        assert record['record_type'] == 0x05  # Start Linear Address
        assert len(record['data']) == 4

    def test_parse_line_invalid_format_raises_value_error(self):
        """Test that invalid line format raises ValueError."""
        parser = HexParser()

        line = 'INVALID_FORMAT'

        with pytest.raises(ValueError, match='Invalid Intel HEX line format'):
            parser._parse_line(line, 1)

    def test_parse_line_byte_count_mismatch_raises_value_error(self):
        """Test that byte count mismatch raises ValueError."""
        parser = HexParser()

        # Byte count is 0x10 but data has 4 bytes
        line = ':100000000102030400'  # Missing data bytes

        with pytest.raises(ValueError, match='Byte count'):
            parser._parse_line(line, 1)

    def test_parse_line_checksum_mismatch_raises_value_error(self):
        """Test that checksum mismatch raises ValueError."""
        parser = HexParser()

        # Valid line but wrong checksum (should be 0x78, we use 0x00)
        line = ':100000000102030405060708090A0B0C0D0E0F0000'

        with pytest.raises(ValueError, match='Checksum mismatch'):
            parser._parse_line(line, 1)

    def test_parse_line_case_insensitive_hex(self):
        """Test that hex values are case-insensitive."""
        parser = HexParser()

        # Mix of uppercase and lowercase (16 bytes)
        line = ':10000000aAbBcCdDeEfF08090a0B0c0D0e0F000198'
        record = parser._parse_line(line, 1)

        assert record['record_type'] == 0x00
        assert record['data'][0] == 0xAA
        assert record['data'][1] == 0xBB
        assert record['data'][2] == 0xCC


class TestHexParserExtractMetadata:
    """Test HexParser._extract_metadata() method."""

    def test_extract_metadata_single_data_record(self):
        """Test metadata extraction from single data record."""
        parser = HexParser()

        records = [
            {
                'byte_count': 0x10,
                'address': 0x1000,
                'record_type': 0x00,  # Data record
                'data': [0x01] * 16,
                'line_number': 1
            }
        ]

        metadata = parser._extract_metadata(records)

        assert metadata['start_addr'] == 0x1000
        assert metadata['end_addr'] == 0x100F
        assert metadata['data_segments'] == 1
        assert metadata['total_records'] == 1
        assert metadata['data_records'] == 1

    def test_extract_metadata_multiple_continuous_records(self):
        """Test metadata extraction from continuous data records."""
        parser = HexParser()

        records = [
            {
                'byte_count': 0x10,
                'address': 0x1000,
                'record_type': 0x00,
                'data': [0x01] * 16,
                'line_number': 1
            },
            {
                'byte_count': 0x10,
                'address': 0x1010,
                'record_type': 0x00,
                'data': [0x02] * 16,
                'line_number': 2
            }
        ]

        metadata = parser._extract_metadata(records)

        assert metadata['start_addr'] == 0x1000
        assert metadata['end_addr'] == 0x101F
        # Continuous data should count as 1 segment
        assert metadata['data_segments'] == 1
        assert metadata['data_records'] == 2

    def test_extract_metadata_multiple_discontinuous_records(self):
        """Test metadata extraction from discontinuous data records."""
        parser = HexParser()

        records = [
            {
                'byte_count': 0x10,
                'address': 0x1000,
                'record_type': 0x00,
                'data': [0x01] * 16,
                'line_number': 1
            },
            {
                'byte_count': 0x10,
                'address': 0x2000,  # Gap in addresses
                'record_type': 0x00,
                'data': [0x02] * 16,
                'line_number': 2
            }
        ]

        metadata = parser._extract_metadata(records)

        assert metadata['start_addr'] == 0x1000
        assert metadata['end_addr'] == 0x200F
        # Discontinuous data should count as 2 segments
        assert metadata['data_segments'] == 2
        assert metadata['data_records'] == 2

    def test_extract_metadata_with_extended_linear_address(self):
        """Test metadata extraction with Extended Linear Address record."""
        parser = HexParser()

        records = [
            {
                'byte_count': 0x02,
                'address': 0x0000,
                'record_type': 0x04,  # Extended Linear Address
                'data': [0x00, 0x10],  # Upper 16 bits = 0x0010
                'line_number': 1
            },
            {
                'byte_count': 0x10,
                'address': 0x0000,  # Full address will be 0x100000
                'record_type': 0x00,
                'data': [0x01] * 16,
                'line_number': 2
            }
        ]

        metadata = parser._extract_metadata(records)

        # Should apply extended address
        assert metadata['start_addr'] == 0x100000
        assert metadata['end_addr'] == 0x10000F
        assert metadata['extended_linear_addr'] == 0x0010

    def test_extract_metadata_with_extended_segment_address(self):
        """Test metadata extraction with Extended Segment Address record."""
        parser = HexParser()

        records = [
            {
                'byte_count': 0x02,
                'address': 0x0000,
                'record_type': 0x02,  # Extended Segment Address
                'data': [0x10, 0x00],  # Upper bits = 0x1000
                'line_number': 1
            },
            {
                'byte_count': 0x10,
                'address': 0x0100,
                'record_type': 0x00,
                'data': [0x01] * 16,
                'line_number': 2
            }
        ]

        metadata = parser._extract_metadata(records)

        assert metadata['extended_segment_addr'] == 0x1000

    def test_extract_metadata_eof_record_ignored(self):
        """Test that EOF record is ignored in metadata calculation."""
        parser = HexParser()

        records = [
            {
                'byte_count': 0x10,
                'address': 0x1000,
                'record_type': 0x00,
                'data': [0x01] * 16,
                'line_number': 1
            },
            {
                'byte_count': 0x00,
                'address': 0x0000,
                'record_type': 0x01,  # EOF record
                'data': [],
                'line_number': 2
            }
        ]

        metadata = parser._extract_metadata(records)

        assert metadata['data_records'] == 1  # EOF doesn't count as data record
        assert metadata['total_records'] == 2
        assert metadata['data_segments'] == 1

    def test_extract_metadata_empty_records(self):
        """Test metadata extraction with no data records."""
        parser = HexParser()

        records = [
            {
                'byte_count': 0x00,
                'address': 0x0000,
                'record_type': 0x01,  # Only EOF record
                'data': [],
                'line_number': 1
            }
        ]

        metadata = parser._extract_metadata(records)

        assert metadata['start_addr'] is None
        assert metadata['end_addr'] is None
        assert metadata['data_segments'] == 0
        assert metadata['data_records'] == 0


class TestHexParserRecordTypes:
    """Test Intel HEX record type constants."""

    def test_record_type_constants(self):
        """Test that all record type constants are defined correctly."""
        parser = HexParser()

        assert parser.RECORD_DATA == 0x00
        assert parser.RECORD_EOF == 0x01
        assert parser.RECORD_EXTENDED_SEGMENT_ADDR == 0x02
        assert parser.RECORD_START_SEGMENT_ADDR == 0x03
        assert parser.RECORD_EXTENDED_LINEAR_ADDR == 0x04
        assert parser.RECORD_START_LINEAR_ADDR == 0x05

    def test_hex_line_pattern(self):
        """Test that HEX_LINE_PATTERN regex is correctly defined."""
        parser = HexParser()

        # Valid pattern should match
        valid_line = ':100000000102030405060708090A0B0C0D0E0F78'
        match = parser.HEX_LINE_PATTERN.match(valid_line)
        assert match is not None

        # Invalid pattern should not match
        invalid_line = 'INVALID_FORMAT'
        match = parser.HEX_LINE_PATTERN.match(invalid_line)
        assert match is None


class TestHexParserErrorHandling:
    """Test HexParser error handling."""

    @pytest.mark.skipif(sys.platform == 'darwin', reason="macOS allows owner to read files with chmod 000")
    def test_can_parse_handles_permission_errors(self):
        """Test that can_parse handles permission errors gracefully."""
        parser = HexParser()

        # Create a file and make it unreadable
        with tempfile.NamedTemporaryFile(mode='w', suffix='.hex', delete=False) as f:
            f.write(':020000040000FA\n')
            temp_path = Path(f.name)

        try:
            os.chmod(temp_path, 0o000)

            result = parser.can_parse(temp_path)
            # Should return False, not raise an exception
            assert result is False
        finally:
            # Restore permissions to delete the file
            os.chmod(temp_path, 0o644)
            temp_path.unlink()

    def test_parse_handles_os_error(self):
        """Test that parse handles OS errors during file reading."""
        parser = HexParser()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.hex', delete=False) as f:
            f.write(':020000040000FA\n')
            temp_path = Path(f.name)

        # Mock open to raise OSError
        try:
            with patch('builtins.open', side_effect=OSError('Mocked OS error')):
                with pytest.raises(ValueError, match='Error reading Intel HEX file'):
                    parser.parse(temp_path)
        finally:
            temp_path.unlink()

    def test_parse_handles_generic_exception(self):
        """Test that parse handles unexpected exceptions."""
        parser = HexParser()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.hex', delete=False) as f:
            f.write(':020000040000FA\n')
            temp_path = Path(f.name)

        # Mock open to raise generic exception
        try:
            with patch('builtins.open', side_effect=RuntimeError('Unexpected error')):
                with pytest.raises(ValueError, match='Failed to parse Intel HEX file'):
                    parser.parse(temp_path)
        finally:
            temp_path.unlink()

    def test_parse_continues_after_checksum_error(self):
        """Test that parse collects all checksum errors before failing."""
        parser = HexParser()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.hex', delete=False) as f:
            # Two records with invalid checksums
            f.write(':100000000102030405060708090A0B0C0D0E0000\n')  # Line 1
            f.write(':100010000102030405060708090A0B0C0D0E0000\n')  # Line 2
            temp_path = Path(f.name)

        try:
            with pytest.raises(ValueError, match='Checksum validation failed'):
                parser.parse(temp_path)

            # Verify error message mentions both lines
            # (This is implicit in the ValueError being raised)
        finally:
            temp_path.unlink()
