"""
Unit tests for the ImgParser plugin.

Tests plugin API compliance, file detection, filesystem type detection,
metadata extraction, and error handling for disk image files.
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from binary_sbom.plugins.img_parser import ImgParser
from binary_sbom.plugins.api import BinaryParserPlugin


class TestImgParserPluginAPI:
    """Test ImgParser plugin API compliance."""

    def test_img_parser_inherits_from_binary_parser_plugin(self):
        """Test that ImgParser inherits from BinaryParserPlugin."""
        parser = ImgParser()
        assert isinstance(parser, BinaryParserPlugin)

    def test_img_parser_get_name(self):
        """Test that get_name returns 'ImgParser'."""
        parser = ImgParser()
        assert parser.get_name() == "ImgParser"

    def test_img_parser_get_supported_formats(self):
        """Test that get_supported_formats returns ['.img']."""
        parser = ImgParser()
        assert parser.get_supported_formats() == ['.img']

    def test_img_parser_version(self):
        """Test that version returns '1.0.0'."""
        parser = ImgParser()
        assert parser.version == "1.0.0"


class TestImgParserCanParse:
    """Test ImgParser.can_parse() method."""

    def test_can_parse_rejects_non_img_extension(self):
        """Test that can_parse rejects files without .img extension."""
        parser = ImgParser()

        # Create a temporary file with different extension
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            f.write(b'test content')
            temp_path = Path(f.name)

        try:
            result = parser.can_parse(temp_path)
            assert result is False
        finally:
            temp_path.unlink()

    def test_can_parse_rejects_nonexistent_file(self):
        """Test that can_parse returns False for non-existent files."""
        parser = ImgParser()
        nonexistent_path = Path('/nonexistent/path/to/file.img')
        result = parser.can_parse(nonexistent_path)
        assert result is False

    def test_can_parse_fat32_magic_number(self):
        """Test that can_parse recognizes FAT32 disk images."""
        parser = ImgParser()

        # Create a temporary file with FAT32 magic number at offset 0x36
        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            # Write enough data to include FAT32 offset
            data = b'\x00' * 0x36
            data += b'FAT32   '  # FAT32 magic number
            data += b'\x00' * 100  # Padding
            f.write(data)
            temp_path = Path(f.name)

        try:
            result = parser.can_parse(temp_path)
            assert result is True
        finally:
            temp_path.unlink()

    def test_can_parse_ntfs_magic_number(self):
        """Test that can_parse recognizes NTFS disk images."""
        parser = ImgParser()

        # Create a temporary file with NTFS magic number at offset 0x03
        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            # Write NTFS magic at offset 0x03
            data = b'\x00\x00\x00NTFS    '  # NTFS magic at offset 3
            data += b'\x00' * 100  # Padding
            f.write(data)
            temp_path = Path(f.name)

        try:
            result = parser.can_parse(temp_path)
            assert result is True
        finally:
            temp_path.unlink()

    def test_can_parse_ext4_magic_number(self):
        """Test that can_parse recognizes EXT4 disk images."""
        parser = ImgParser()

        # Create a temporary file with EXT4 magic number at offset 0x400
        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            # Write data up to EXT4 offset
            data = b'\x00' * 0x400
            data += b'\x53\xEF'  # EXT4 magic number (little-endian 0xEF53)
            data += b'\x00' * 100  # Padding
            f.write(data)
            temp_path = Path(f.name)

        try:
            result = parser.can_parse(temp_path)
            assert result is True
        finally:
            temp_path.unlink()

    def test_can_parse_iso9660_magic_number(self):
        """Test that can_parse recognizes ISO9660 disk images."""
        parser = ImgParser()

        # Create a temporary file with ISO9660 magic number at offset 0x8000
        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            # Write data up to ISO9660 offset
            data = b'\x00' * 0x8000
            data += b'\x01CD001'  # ISO9660 magic number
            data += b'\x00' * 100  # Padding
            f.write(data)
            temp_path = Path(f.name)

        try:
            result = parser.can_parse(temp_path)
            assert result is True
        finally:
            temp_path.unlink()

    def test_can_parse_rejects_img_without_valid_magic(self):
        """Test that can_parse rejects .img files without valid magic numbers."""
        parser = ImgParser()

        # Create a temporary .img file without valid magic numbers
        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            f.write(b'This is not a valid disk image')
            temp_path = Path(f.name)

        try:
            result = parser.can_parse(temp_path)
            assert result is False
        finally:
            temp_path.unlink()

    def test_can_parse_case_insensitive_extension(self):
        """Test that can_parse handles .IMG extension (uppercase)."""
        parser = ImgParser()

        # Create a temporary file with uppercase .IMG extension
        with tempfile.NamedTemporaryFile(suffix='.IMG', delete=False) as f:
            # Write FAT32 magic number
            data = b'\x00' * 0x36
            data += b'FAT32   '
            data += b'\x00' * 100
            f.write(data)
            temp_path = Path(f.name)

        try:
            result = parser.can_parse(temp_path)
            assert result is True
        finally:
            temp_path.unlink()

    def test_can_parse_empty_file(self):
        """Test that can_parse returns False for empty .img files."""
        parser = ImgParser()

        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            # Write nothing (empty file)
            temp_path = Path(f.name)

        try:
            result = parser.can_parse(temp_path)
            assert result is False
        finally:
            temp_path.unlink()


class TestImgParserParse:
    """Test ImgParser.parse() method."""

    def test_parse_fat32_image(self):
        """Test parsing a FAT32 disk image."""
        parser = ImgParser()

        # Create a FAT32 disk image
        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            # Write FAT32 boot sector structure
            data = b'\x00' * 0x36
            data += b'FAT32   '  # FAT32 magic at offset 0x36
            data += b'\x00' * 100
            # Add a volume label at offset 0x2B (we need to go back)
            data_list = list(data)
            # Insert volume label "TESTVOL" at position 0x2B
            label = b'TESTVOL'
            # Ensure we have enough space
            while len(data_list) < 0x2B + len(label):
                data_list.append(0)
            for i, byte in enumerate(label):
                data_list[0x2B + i] = byte
            f.write(bytes(data_list))
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
            assert package['type'] == 'disk-image'
            assert package['fileSystemType'] == 'FAT32'
            assert 'size' in package
            assert 'spdx_id' in package

            # Verify annotations
            assert len(result['annotations']) == 1
            annotation = result['annotations'][0]
            assert 'text' in annotation
            assert 'FAT32' in annotation['text']
        finally:
            temp_path.unlink()

    def test_parse_ntfs_image(self):
        """Test parsing an NTFS disk image."""
        parser = ImgParser()

        # Create an NTFS disk image
        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            # Write NTFS boot sector structure
            data = b'\x00\x00\x00NTFS    '  # NTFS magic at offset 0x03
            data += b'\x00' * 200
            f.write(data)
            temp_path = Path(f.name)

        try:
            result = parser.parse(temp_path)

            # Verify filesystem type
            assert result['packages'][0]['fileSystemType'] == 'NTFS'
            assert 'NTFS' in result['annotations'][0]['text']
        finally:
            temp_path.unlink()

    def test_parse_ext4_image(self):
        """Test parsing an EXT4 disk image."""
        parser = ImgParser()

        # Create an EXT4 disk image
        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            # Write EXT4 superblock structure
            data = b'\x00' * 0x400
            data += b'\x53\xEF'  # EXT4 magic at offset 0x400
            data += b'\x00' * 200
            f.write(data)
            temp_path = Path(f.name)

        try:
            result = parser.parse(temp_path)

            # Verify filesystem type
            assert result['packages'][0]['fileSystemType'] == 'EXT4'
            assert 'EXT4' in result['annotations'][0]['text']
        finally:
            temp_path.unlink()

    def test_parse_iso9660_image(self):
        """Test parsing an ISO9660 disk image."""
        parser = ImgParser()

        # Create an ISO9660 disk image
        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            # Write ISO9660 volume descriptor
            data = b'\x00' * 0x8000
            data += b'\x01CD001'  # ISO9660 magic at offset 0x8000
            # Add volume label at offset 0x8028
            data += b'\x00' * (0x8028 - 0x8000 - 6)  # Padding to volume label
            data += b'ISOCD'  # Volume label
            data += b'\x00' * 100
            f.write(data)
            temp_path = Path(f.name)

        try:
            result = parser.parse(temp_path)

            # Verify filesystem type
            assert result['packages'][0]['fileSystemType'] == 'ISO9660'
            assert 'ISO9660' in result['annotations'][0]['text']
        finally:
            temp_path.unlink()

    def test_parse_unknown_filesystem(self):
        """Test parsing a disk image with unknown filesystem type."""
        parser = ImgParser()

        # Create a disk image without valid magic numbers
        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            # Write invalid data
            f.write(b'INVALID DISK IMAGE DATA' + b'\x00' * 32774)
            temp_path = Path(f.name)

        try:
            result = parser.parse(temp_path)

            # Verify filesystem is marked as unknown
            assert result['packages'][0]['fileSystemType'] == 'unknown'
            assert 'unknown' in result['annotations'][0]['text'].lower()
        finally:
            temp_path.unlink()

    def test_parse_returns_valid_structure(self):
        """Test that parse returns valid SPDX-compatible structure."""
        parser = ImgParser()

        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            data = b'\x00' * 0x36
            data += b'FAT32   '
            data += b'\x00' * 100
            f.write(data)
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

    def test_parse_includes_file_size(self):
        """Test that parse includes file size in metadata."""
        parser = ImgParser()

        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            data = b'\x00' * 0x36
            data += b'FAT32   '
            data += b'\x00' * 1000
            f.write(data)
            temp_path = Path(f.name)

        try:
            result = parser.parse(temp_path)

            # Verify size is included
            package = result['packages'][0]
            assert 'size' in package
            assert package['size'] > 0
            assert package['size'] == temp_path.stat().st_size
        finally:
            temp_path.unlink()

    def test_parse_missing_file_raises_file_not_found_error(self):
        """Test that parse raises FileNotFoundError for missing files."""
        parser = ImgParser()
        nonexistent_path = Path('/nonexistent/disk.img')

        with pytest.raises(FileNotFoundError, match='Disk image file not found'):
            parser.parse(nonexistent_path)

    def test_parse_annotation_includes_size_mb(self):
        """Test that annotation includes size in MB."""
        parser = ImgParser()

        # Create a 1MB file
        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            data = b'\x00' * 0x36
            data += b'FAT32   '
            data += b'\x00' * (1024 * 1024 - 0x36 - 8)
            f.write(data)
            temp_path = Path(f.name)

        try:
            result = parser.parse(temp_path)

            # Verify annotation includes size in MB
            annotation = result['annotations'][0]
            assert 'MB' in annotation['text']
            assert 'Size:' in annotation['text']
        finally:
            temp_path.unlink()


class TestImgParserFilesystemDetection:
    """Test ImgParser._detect_filesystem_type() method."""

    def test_detect_filesystem_type_fat32(self):
        """Test filesystem type detection for FAT32."""
        parser = ImgParser()

        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            data = b'\x00' * 0x36
            data += b'FAT32   '
            data += b'\x00' * 200
            f.write(data)
            temp_path = Path(f.name)

        try:
            filesystem_type = parser._detect_filesystem_type(temp_path)
            assert filesystem_type == 'FAT32'
        finally:
            temp_path.unlink()

    def test_detect_filesystem_type_ntfs(self):
        """Test filesystem type detection for NTFS."""
        parser = ImgParser()

        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            data = b'\x00\x00\x00NTFS    '
            data += b'\x00' * 200
            f.write(data)
            temp_path = Path(f.name)

        try:
            filesystem_type = parser._detect_filesystem_type(temp_path)
            assert filesystem_type == 'NTFS'
        finally:
            temp_path.unlink()

    def test_detect_filesystem_type_ext4(self):
        """Test filesystem type detection for EXT4."""
        parser = ImgParser()

        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            data = b'\x00' * 0x400
            data += b'\x53\xEF'
            data += b'\x00' * 200
            f.write(data)
            temp_path = Path(f.name)

        try:
            filesystem_type = parser._detect_filesystem_type(temp_path)
            assert filesystem_type == 'EXT4'
        finally:
            temp_path.unlink()

    def test_detect_filesystem_type_iso9660(self):
        """Test filesystem type detection for ISO9660."""
        parser = ImgParser()

        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            data = b'\x00' * 0x8000
            data += b'\x01CD001'
            data += b'\x00' * 200
            f.write(data)
            temp_path = Path(f.name)

        try:
            filesystem_type = parser._detect_filesystem_type(temp_path)
            assert filesystem_type == 'ISO9660'
        finally:
            temp_path.unlink()

    def test_detect_filesystem_type_unknown(self):
        """Test filesystem type detection for unknown filesystems."""
        parser = ImgParser()

        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            f.write(b'UNKNOWN FILESYSTEM DATA' + b'\x00' * 32774)
            temp_path = Path(f.name)

        try:
            filesystem_type = parser._detect_filesystem_type(temp_path)
            assert filesystem_type == 'unknown'
        finally:
            temp_path.unlink()


class TestImgParserVolumeLabel:
    """Test ImgParser._extract_volume_label() method."""

    def test_extract_volume_label_fat32(self):
        """Test volume label extraction for FAT32."""
        parser = ImgParser()

        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            # Create FAT32 boot sector with volume label at offset 0x2B
            data = b'\x00' * 0x2B
            data += b'MYVOLUME'  # Volume label (8 bytes)
            data += b'   '  # Padding to 11 bytes total
            data += b'\x00' * 0x36
            data += b'FAT32   '
            data += b'\x00' * 100
            f.write(data)
            temp_path = Path(f.name)

        try:
            label = parser._extract_volume_label(temp_path, 'FAT32')
            assert label == 'MYVOLUME'
        finally:
            temp_path.unlink()

    def test_extract_volume_label_fat32_padded(self):
        """Test volume label extraction with space padding."""
        parser = ImgParser()

        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            data = b'\x00' * 0x2B
            data += b'TEST     '  # Volume label with spaces
            data += b'\x00' * 0x36
            data += b'FAT32   '
            data += b'\x00' * 100
            f.write(data)
            temp_path = Path(f.name)

        try:
            label = parser._extract_volume_label(temp_path, 'FAT32')
            # Should strip trailing spaces
            assert label == 'TEST'
        finally:
            temp_path.unlink()

    def test_extract_volume_label_iso9660(self):
        """Test volume label extraction for ISO9660."""
        parser = ImgParser()

        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            data = b'\x00' * 0x8000
            data += b'\x01CD001'
            # Volume label is at offset 0x8028 (0x8000 + 6 + 0x22)
            padding_needed = 0x8028 - 0x8000 - 6
            data += b'\x00' * padding_needed
            data += b'MYISOCD'  # Volume label
            data += b'\x00' * 100
            f.write(data)
            temp_path = Path(f.name)

        try:
            label = parser._extract_volume_label(temp_path, 'ISO9660')
            assert label == 'MYISOCD'
        finally:
            temp_path.unlink()

    def test_extract_volume_label_unknown_filesystem(self):
        """Test volume label extraction for unknown filesystem returns empty string."""
        parser = ImgParser()

        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            f.write(b'\x00' * 1000)
            temp_path = Path(f.name)

        try:
            label = parser._extract_volume_label(temp_path, 'unknown')
            assert label == ''
        finally:
            temp_path.unlink()

    def test_extract_volume_label_ntfs_returns_empty(self):
        """Test that NTFS volume label extraction returns empty (not implemented)."""
        parser = ImgParser()

        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            data = b'\x00\x00\x00NTFS    '
            data += b'\x00' * 200
            f.write(data)
            temp_path = Path(f.name)

        try:
            label = parser._extract_volume_label(temp_path, 'NTFS')
            # NTFS label extraction is not implemented
            assert label == ''
        finally:
            temp_path.unlink()

    def test_extract_volume_label_ext4_returns_empty(self):
        """Test that EXT4 volume label extraction returns empty (not implemented)."""
        parser = ImgParser()

        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            data = b'\x00' * 0x400
            data += b'\x53\xEF'
            data += b'\x00' * 200
            f.write(data)
            temp_path = Path(f.name)

        try:
            label = parser._extract_volume_label(temp_path, 'EXT4')
            # EXT4 label extraction is not implemented
            assert label == ''
        finally:
            temp_path.unlink()


class TestImgParserErrorHandling:
    """Test ImgParser error handling."""

    @pytest.mark.skipif(sys.platform == 'darwin', reason="macOS allows owner to read files with chmod 000")
    def test_parse_read_error_raises_value_error(self):
        """Test that read errors during parse raise ValueError."""
        parser = ImgParser()

        # Create a file and make it unreadable
        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            data = b'\x00' * 0x36
            data += b'FAT32   '
            data += b'\x00' * 100
            f.write(data)
            temp_path = Path(f.name)

        # Make file unreadable (remove read permissions)
        try:
            import stat
            os.chmod(temp_path, 0o000)

            with pytest.raises(ValueError, match='Error reading disk image file'):
                parser.parse(temp_path)
        finally:
            # Restore permissions to delete the file
            os.chmod(temp_path, 0o644)
            temp_path.unlink()

    @pytest.mark.skipif(sys.platform == 'darwin', reason="macOS allows owner to read files with chmod 000")
    def test_can_parse_handles_permission_errors(self):
        """Test that can_parse handles permission errors gracefully."""
        import stat

        parser = ImgParser()

        # Create a file and make it unreadable
        with tempfile.NamedTemporaryFile(suffix='.img', delete=False) as f:
            data = b'\x00' * 0x36
            data += b'FAT32   '
            data += b'\x00' * 100
            f.write(data)
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
