"""
Disk Image Parser Plugin for Binary SBOM Generator.

This plugin provides parsing capabilities for disk image files (.img) containing
filesystem metadata. It supports common disk image formats including FAT32, EXT4,
NTFS, and ISO9660 filesystem types.

The plugin extracts basic filesystem metadata including:
- Filesystem type (FAT32, EXT4, NTFS, ISO9660)
- Disk size and block information
- Basic volume information

Note: This plugin provides basic metadata extraction. For comprehensive filesystem
forensics capabilities, consider using tools like The Sleuth Kit (TSK) or pytsk3.
"""

from pathlib import Path
from typing import Dict, Any, List
import struct
import os

from binary_sbom.plugins.api import BinaryParserPlugin


class ImgParser(BinaryParserPlugin):
    """Parser for disk image files (.img) containing filesystem metadata.

    This plugin handles disk image files used in OS development, embedded systems,
    and system programming. It supports common filesystem formats including:
    - FAT32 (common in embedded systems and older Windows)
    - EXT4 (standard Linux filesystem)
    - NTFS (Windows NT filesystem)
    - ISO9660 (CD-ROM filesystem)

    The plugin extracts basic metadata from the disk image header and boot sector
    to identify filesystem type, size, and volume information. For comprehensive
    file extraction and deep forensics analysis, dedicated tools like The Sleuth
    Kit (TSK) should be used instead.

    Example:
        >>> from pathlib import Path
        >>> from binary_sbom.plugins.img_parser import ImgParser
        >>>
        >>> parser = ImgParser()
        >>> metadata = parser.parse(Path('/path/to/disk.img'))
        >>> print(metadata['packages'][0]['fileSystemType'])
        'FAT32'
    """

    # Filesystem magic numbers (matching file_detector.py)
    FAT32_MAGIC = b'FAT32   '
    EXT4_MAGIC = b'\x53\xEF'
    NTFS_MAGIC = b'NTFS    '
    ISO9660_MAGIC = b'\x01CD001'

    # Offsets for magic numbers in disk images
    FAT32_OFFSET = 0x36    # FAT32 identifier in boot sector
    EXT4_OFFSET = 0x400    # EXT4 superblock magic
    NTFS_OFFSET = 0x03     # NTFS identifier in boot sector
    ISO9660_OFFSET = 0x8000  # ISO9660 volume descriptor

    def get_name(self) -> str:
        """Return unique plugin name.

        Returns:
            "ImgParser" as the unique identifier for this plugin.
        """
        return "ImgParser"

    def get_supported_formats(self) -> List[str]:
        """Return list of supported file extensions.

        Returns:
            List containing '.img' extension.
        """
        return ['.img']

    def can_parse(self, file_path: Path) -> bool:
        """Check if this plugin can parse the given file.

        This method performs a fast check to determine if the file is a disk
        image by verifying:
        1. File extension is .img (fast check)
        2. File exists and is readable
        3. Magic bytes match known filesystem types (reliable check)

        Args:
            file_path: Path to the binary file to check.

        Returns:
            True if the file appears to be a disk image, False otherwise.
        """
        # Fast extension check first
        if file_path.suffix.lower() != '.img':
            return False

        # Verify file exists
        if not file_path.exists() or not file_path.is_file():
            return False

        # Reliable magic byte check - verify it's a valid disk image
        # by checking for known filesystem magic numbers
        try:
            with open(file_path, 'rb') as f:
                # Read enough bytes to check all filesystem types
                # Maximum offset is ISO9660 at 0x8000 + 6 bytes = 32774
                header = f.read(32774)

            if not header:
                return False

            # Check NTFS (offset 0x03, "NTFS    " string)
            if len(header) >= 11:
                ntfs_offset = self.NTFS_OFFSET
                if header[ntfs_offset:ntfs_offset+8] == self.NTFS_MAGIC:
                    return True

            # Check FAT32 (offset 0x36, "FAT32   " string)
            if len(header) >= 62:
                fat32_offset = self.FAT32_OFFSET
                if header[fat32_offset:fat32_offset+8] == self.FAT32_MAGIC:
                    return True

            # Check EXT4 (offset 0x400, 0xEF53 in little-endian)
            if len(header) >= 1026:
                ext4_offset = self.EXT4_OFFSET
                if header[ext4_offset:ext4_offset+2] == self.EXT4_MAGIC:
                    return True

            # Check ISO9660 (offset 0x8000, "\x01CD001")
            if len(header) >= 32774:
                iso9660_offset = self.ISO9660_OFFSET
                if header[iso9660_offset:iso9660_offset+6] == self.ISO9660_MAGIC:
                    return True

            # No known filesystem magic numbers found
            return False

        except (OSError, IOError):
            return False

    def parse(self, file_path: Path) -> Dict[str, Any]:
        """Parse disk image file and return metadata dictionary.

        This method extracts filesystem metadata from a disk image file, including:
        - Filesystem type (FAT32, EXT4, NTFS, ISO9660, or unknown)
        - Volume size and block information
        - Volume label/name if available
        - Format-specific annotations

        Args:
            file_path: Path to the disk image file to parse.

        Returns:
            Dictionary with 'packages', 'relationships', and 'annotations' keys.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If file format is invalid or corrupted.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Disk image file not found: {file_path}")

        try:
            # Get file size
            file_size = file_path.stat().st_size

            # Detect filesystem type by reading magic numbers
            filesystem_type = self._detect_filesystem_type(file_path)

            # Create disk image package
            disk_image_package = {
                'name': file_path.stem,
                'type': 'disk-image',
                'fileSystemType': filesystem_type,
                'size': file_size,
                'description': f'Disk image with {filesystem_type} filesystem',
                'spdx_id': 'SPDXRef-diskimage',
                'download_location': 'NOASSERTION',
            }

            # Add volume label if available
            volume_label = self._extract_volume_label(file_path, filesystem_type)
            if volume_label:
                disk_image_package['volumeLabel'] = volume_label

            packages = [disk_image_package]
            relationships = []
            annotations = []

            # Add parsing annotation with filesystem details
            annotation_text = (
                f'Parsed by {self.get_name()} v{self.version}. '
                f'Filesystem type: {filesystem_type}, '
                f'Size: {file_size} bytes ({file_size / (1024*1024):.2f} MB)'
            )

            # Add filesystem-specific notes
            if filesystem_type == 'unknown':
                annotation_text += '. Filesystem type could not be determined from magic numbers.'

            annotations.append({
                'spdx_id': 'SPDXRef-diskimage',
                'type': 'OTHER',
                'text': annotation_text
            })

            return {
                'packages': packages,
                'relationships': relationships,
                'annotations': annotations
            }

        except (OSError, IOError) as e:
            raise ValueError(f"Error reading disk image file: {e}")
        except Exception as e:
            raise ValueError(f"Failed to parse disk image: {e}")

    def _detect_filesystem_type(self, file_path: Path) -> str:
        """Detect filesystem type by checking magic numbers.

        Args:
            file_path: Path to the disk image file.

        Returns:
            Filesystem type string ('FAT32', 'EXT4', 'NTFS', 'ISO9660', or 'unknown').
        """
        try:
            with open(file_path, 'rb') as f:
                # Read enough bytes to check all filesystem types
                # Maximum offset is ISO9660 at 0x8000 + 6 bytes = 32774
                header = f.read(32774)

            if not header:
                return 'unknown'

            # Check NTFS (offset 0x03, "NTFS    " string)
            if len(header) >= 11:
                ntfs_offset = self.NTFS_OFFSET
                if header[ntfs_offset:ntfs_offset+8] == self.NTFS_MAGIC:
                    return 'NTFS'

            # Check FAT32 (offset 0x36, "FAT32   " string)
            if len(header) >= 62:
                fat32_offset = self.FAT32_OFFSET
                if header[fat32_offset:fat32_offset+8] == self.FAT32_MAGIC:
                    return 'FAT32'

            # Check EXT4 (offset 0x400, 0xEF53 in little-endian)
            if len(header) >= 1026:
                ext4_offset = self.EXT4_OFFSET
                if header[ext4_offset:ext4_offset+2] == self.EXT4_MAGIC:
                    return 'EXT4'

            # Check ISO9660 (offset 0x8000, "\x01CD001")
            if len(header) >= 32774:
                iso9660_offset = self.ISO9660_OFFSET
                if header[iso9660_offset:iso9660_offset+6] == self.ISO9660_MAGIC:
                    return 'ISO9660'

            return 'unknown'

        except (OSError, IOError):
            return 'unknown'

    def _extract_volume_label(self, file_path: Path, filesystem_type: str) -> str:
        """Extract volume label from disk image if available.

        This is a simplified implementation that extracts basic volume labels.
        A complete implementation would parse each filesystem's specific
        volume label location and format.

        Args:
            file_path: Path to the disk image file.
            filesystem_type: Detected filesystem type.

        Returns:
            Volume label string, or empty string if not available.
        """
        try:
            with open(file_path, 'rb') as f:
                if filesystem_type == 'FAT32':
                    # FAT32 volume label is at offset 0x2B (43) in boot sector
                    # 11 bytes, padded with spaces
                    f.seek(0x2B)
                    label_bytes = f.read(11)
                    try:
                        label = label_bytes.rstrip(b' \x00').decode('ascii', errors='replace')
                        return label if label else ''
                    except UnicodeDecodeError:
                        return ''

                elif filesystem_type == 'NTFS':
                    # NTFS volume label is more complex and requires parsing the
                    # Master File Table (MFT). For basic metadata, we skip this.
                    return ''

                elif filesystem_type == 'EXT4':
                    # EXT4 volume label requires parsing the superblock structure
                    # For basic metadata, we skip this.
                    return ''

                elif filesystem_type == 'ISO9660':
                    # ISO9660 volume label is at offset 0x8028 in volume descriptor
                    f.seek(0x8028)
                    label_bytes = f.read(32)
                    try:
                        label = label_bytes.rstrip(b' \x00').decode('ascii', errors='replace')
                        return label if label else ''
                    except UnicodeDecodeError:
                        return ''

                return ''

        except (OSError, IOError):
            return ''

    @property
    def version(self) -> str:
        """Plugin version string.

        Returns:
            "1.0.0" as the initial version of this plugin.
        """
        return "1.0.0"
