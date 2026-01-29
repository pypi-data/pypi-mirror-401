"""
Unit tests for the file_detector module.

Tests magic number detection and file type identification.
"""

import os
import tempfile
import unittest

from src.file_detector import (
    FileType,
    ELF_MAGIC,
    PE_MAGIC,
    MACHO_MAGICS,
    INTEL_HEX_MAGIC,
    FAT32_MAGIC,
    EXT4_MAGIC,
    NTFS_MAGIC,
    ISO9660_MAGIC,
    detect_file_type,
    is_binary_file,
    is_binary_extension,
    BINARY_EXTENSIONS,
    _detect_type_by_extension,
)


class TestMagicNumberDetection(unittest.TestCase):
    """Test magic number constants and detection."""

    def test_elf_magic_constant(self):
        """Test that ELF_MAGIC is correctly defined."""
        self.assertEqual(ELF_MAGIC, b'\x7fELF')

    def test_pe_magic_constant(self):
        """Test that PE_MAGIC is correctly defined."""
        self.assertEqual(PE_MAGIC, b'MZ')

    def test_macho_magic_constants(self):
        """Test that all MachO magic numbers are defined."""
        self.assertEqual(len(MACHO_MAGICS), 6)
        self.assertIn(b'\xfe\xed\xfa\xce', MACHO_MAGICS)  # 32-bit big endian
        self.assertIn(b'\xce\xfa\xed\xfe', MACHO_MAGICS)  # 32-bit little endian
        self.assertIn(b'\xfe\xed\xfa\xcf', MACHO_MAGICS)  # 64-bit big endian
        self.assertIn(b'\xcf\xfa\xed\xfe', MACHO_MAGICS)  # 64-bit little endian
        self.assertIn(b'\xca\xfe\xba\xbe', MACHO_MAGICS)  # Fat binary
        self.assertIn(b'\xca\xfe\xba\xbf', MACHO_MAGICS)  # Fat 64-bit binary

    def test_intel_hex_magic_constant(self):
        """Test that INTEL_HEX_MAGIC is correctly defined."""
        self.assertEqual(INTEL_HEX_MAGIC, b':')

    def test_img_magic_constants(self):
        """Test that IMG magic numbers are correctly defined."""
        self.assertEqual(FAT32_MAGIC, b'FAT32   ')
        self.assertEqual(EXT4_MAGIC, b'\x53\xEF')
        self.assertEqual(NTFS_MAGIC, b'NTFS    ')
        self.assertEqual(ISO9660_MAGIC, b'\x01CD001')


class TestDetectFileType(unittest.TestCase):
    """Test the detect_file_type function."""

    def setUp(self):
        """Create temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary test files."""
        for filename in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, filename))
        os.rmdir(self.test_dir)

    def test_detect_elf_file(self):
        """Test detection of ELF files by magic number."""
        elf_file = os.path.join(self.test_dir, 'test.elf')
        with open(elf_file, 'wb') as f:
            f.write(b'\x7fELF')  # ELF magic number
            f.write(b'\x00' * 100)  # Some padding

        file_type = detect_file_type(elf_file)
        self.assertEqual(file_type, FileType.ELF)

    def test_detect_pe_file(self):
        """Test detection of PE files by magic number."""
        pe_file = os.path.join(self.test_dir, 'test.exe')
        with open(pe_file, 'wb') as f:
            f.write(b'MZ')  # PE magic number
            f.write(b'\x00' * 100)  # Some padding

        file_type = detect_file_type(pe_file)
        self.assertEqual(file_type, FileType.PE)

    def test_detect_macho_file_32_le(self):
        """Test detection of MachO 32-bit little endian files."""
        macho_file = os.path.join(self.test_dir, 'test.macho')
        with open(macho_file, 'wb') as f:
            f.write(b'\xce\xfa\xed\xfe')  # MachO 32-bit little endian
            f.write(b'\x00' * 100)

        file_type = detect_file_type(macho_file)
        self.assertEqual(file_type, FileType.MACHO)

    def test_detect_macho_file_64_le(self):
        """Test detection of MachO 64-bit little endian files."""
        macho_file = os.path.join(self.test_dir, 'test.macho64')
        with open(macho_file, 'wb') as f:
            f.write(b'\xcf\xfa\xed\xfe')  # MachO 64-bit little endian
            f.write(b'\x00' * 100)

        file_type = detect_file_type(macho_file)
        self.assertEqual(file_type, FileType.MACHO)

    def test_detect_macho_fat_binary(self):
        """Test detection of MachO fat binary files."""
        macho_file = os.path.join(self.test_dir, 'test.fat')
        with open(macho_file, 'wb') as f:
            f.write(b'\xca\xfe\xba\xbe')  # MachO fat binary
            f.write(b'\x00' * 100)

        file_type = detect_file_type(macho_file)
        self.assertEqual(file_type, FileType.MACHO)

    def test_detect_unknown_file(self):
        """Test detection of unknown file types."""
        unknown_file = os.path.join(self.test_dir, 'test.txt')
        with open(unknown_file, 'wb') as f:
            f.write(b'This is a text file')

        file_type = detect_file_type(unknown_file)
        self.assertEqual(file_type, FileType.UNKNOWN)

    def test_detect_nonexistent_file(self):
        """Test detection of non-existent file."""
        file_type = detect_file_type('/nonexistent/file')
        self.assertEqual(file_type, FileType.UNKNOWN)

    def test_detect_empty_file(self):
        """Test detection of empty file."""
        empty_file = os.path.join(self.test_dir, 'empty')
        with open(empty_file, 'wb') as f:
            pass  # Create empty file

        file_type = detect_file_type(empty_file)
        self.assertEqual(file_type, FileType.UNKNOWN)

    def test_detect_intel_hex_file(self):
        """Test detection of Intel HEX files by magic number."""
        hex_file = os.path.join(self.test_dir, 'test.hex')
        with open(hex_file, 'wb') as f:
            f.write(b':')  # Intel HEX magic number
            f.write(b'10001000214C01')  # Sample Intel HEX data

        file_type = detect_file_type(hex_file)
        self.assertEqual(file_type, FileType.HEX)

    def test_detect_ntfs_img_file(self):
        """Test detection of NTFS disk images by magic number."""
        img_file = os.path.join(self.test_dir, 'test.img')
        with open(img_file, 'wb') as f:
            f.write(b'\x00' * 3)  # Padding to offset 0x03
            f.write(b'NTFS    ')  # NTFS magic number at offset 3
            f.write(b'\x00' * 100)  # Padding

        file_type = detect_file_type(img_file)
        self.assertEqual(file_type, FileType.IMG)

    def test_detect_fat32_img_file(self):
        """Test detection of FAT32 disk images by magic number."""
        img_file = os.path.join(self.test_dir, 'fat32.img')
        with open(img_file, 'wb') as f:
            f.write(b'\x00' * 0x36)  # Padding to offset 0x36
            f.write(b'FAT32   ')  # FAT32 magic number at offset 54
            f.write(b'\x00' * 100)  # Padding

        file_type = detect_file_type(img_file)
        self.assertEqual(file_type, FileType.IMG)

    def test_detect_ext4_img_file(self):
        """Test detection of EXT4 disk images by magic number."""
        img_file = os.path.join(self.test_dir, 'ext4.img')
        with open(img_file, 'wb') as f:
            f.write(b'\x00' * 0x400)  # Padding to offset 0x400
            f.write(b'\x53\xEF')  # EXT4 magic number at offset 1024
            f.write(b'\x00' * 100)  # Padding

        file_type = detect_file_type(img_file)
        self.assertEqual(file_type, FileType.IMG)

    def test_detect_iso9660_img_file(self):
        """Test detection of ISO9660 disk images by magic number."""
        img_file = os.path.join(self.test_dir, 'cdrom.img')
        with open(img_file, 'wb') as f:
            f.write(b'\x00' * 0x8000)  # Padding to offset 0x8000
            f.write(b'\x01CD001')  # ISO9660 magic number at offset 32768
            f.write(b'\x00' * 100)  # Padding

        file_type = detect_file_type(img_file)
        self.assertEqual(file_type, FileType.IMG)

    def test_detect_img_fat32(self):
        """Test detection of FAT32 disk images by magic number."""
        img_file = os.path.join(self.test_dir, 'fat32.img')
        with open(img_file, 'wb') as f:
            f.write(b'\x00' * 0x36)  # Padding to offset 0x36
            f.write(b'FAT32   ')  # FAT32 magic number at offset 54
            f.write(b'\x00' * 100)  # Padding

        file_type = detect_file_type(img_file)
        self.assertEqual(file_type, FileType.IMG)


class TestExtensionBasedDetection(unittest.TestCase):
    """Test extension-based detection as fallback method."""

    def setUp(self):
        """Create temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary test files."""
        for filename in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, filename))
        os.rmdir(self.test_dir)

    def test_fallback_to_extension_for_pe(self):
        """Test extension-based detection for PE files without magic numbers."""
        # Create a .exe file without PE magic number
        pe_file = os.path.join(self.test_dir, 'test.exe')
        with open(pe_file, 'wb') as f:
            f.write(b'Not a PE file')  # No MZ magic number

        # Should still detect as PE based on extension
        file_type = detect_file_type(pe_file)
        self.assertEqual(file_type, FileType.PE)

    def test_fallback_to_extension_for_elf(self):
        """Test extension-based detection for ELF files without magic numbers."""
        # Create a .so file without ELF magic number
        elf_file = os.path.join(self.test_dir, 'test.so')
        with open(elf_file, 'wb') as f:
            f.write(b'Not an ELF file')  # No ELF magic number

        # Should still detect as ELF based on extension
        file_type = detect_file_type(elf_file)
        self.assertEqual(file_type, FileType.ELF)

    def test_fallback_to_extension_for_macho(self):
        """Test extension-based detection for MachO files without magic numbers."""
        # Create a .dylib file without MachO magic number
        macho_file = os.path.join(self.test_dir, 'test.dylib')
        with open(macho_file, 'wb') as f:
            f.write(b'Not a MachO file')  # No MachO magic number

        # Should still detect as MachO based on extension
        file_type = detect_file_type(macho_file)
        self.assertEqual(file_type, FileType.MACHO)

    def test_magic_number_takes_precedence(self):
        """Test that magic number detection takes precedence over extension."""
        # Create a .txt file with ELF magic number
        elf_file = os.path.join(self.test_dir, 'not_really.txt')
        with open(elf_file, 'wb') as f:
            f.write(b'\x7fELF')  # ELF magic number

        # Should detect as ELF based on magic number, not extension
        file_type = detect_file_type(elf_file)
        self.assertEqual(file_type, FileType.ELF)

    def test_unknown_extension_returns_unknown(self):
        """Test that unknown extensions return UNKNOWN."""
        # Create a file with unknown extension
        unknown_file = os.path.join(self.test_dir, 'test.unknown_ext')
        with open(unknown_file, 'wb') as f:
            f.write(b'Some content')

        file_type = detect_file_type(unknown_file)
        self.assertEqual(file_type, FileType.UNKNOWN)


class TestIsBinaryFile(unittest.TestCase):
    """Test the is_binary_file function."""

    def setUp(self):
        """Create temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary test files."""
        for filename in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, filename))
        os.rmdir(self.test_dir)

    def test_binary_file_with_null_bytes(self):
        """Test detection of binary files with null bytes."""
        binary_file = os.path.join(self.test_dir, 'binary.bin')
        with open(binary_file, 'wb') as f:
            f.write(b'\x00\x01\x02\x03\x00')

        self.assertTrue(is_binary_file(binary_file))

    def test_text_file(self):
        """Test that text files are not detected as binary."""
        text_file = os.path.join(self.test_dir, 'text.txt')
        with open(text_file, 'w') as f:
            f.write('This is a plain text file\n')

        self.assertFalse(is_binary_file(text_file))

    def test_mixed_content_file(self):
        """Test detection of files with mixed content."""
        mixed_file = os.path.join(self.test_dir, 'mixed.dat')
        with open(mixed_file, 'wb') as f:
            f.write(b'Text content')
            f.write(b'\x00\x01\x02')  # Binary content

        self.assertTrue(is_binary_file(mixed_file))


class TestIsBinaryExtension(unittest.TestCase):
    """Test the is_binary_extension function."""

    def test_windows_extensions(self):
        """Test detection of Windows binary extensions."""
        self.assertTrue(is_binary_extension('test.exe'))
        self.assertTrue(is_binary_extension('test.dll'))
        self.assertTrue(is_binary_extension('test.sys'))

    def test_unix_extensions(self):
        """Test detection of Unix binary extensions."""
        self.assertTrue(is_binary_extension('test.elf'))
        self.assertTrue(is_binary_extension('test.so'))
        self.assertTrue(is_binary_extension('test.a'))
        self.assertTrue(is_binary_extension('test.o'))

    def test_macos_extensions(self):
        """Test detection of macOS binary extensions."""
        self.assertTrue(is_binary_extension('test.dylib'))
        self.assertTrue(is_binary_extension('test.bundle'))

    def test_text_extensions(self):
        """Test that text file extensions are not detected as binary."""
        self.assertFalse(is_binary_extension('test.txt'))
        self.assertFalse(is_binary_extension('test.md'))
        self.assertFalse(is_binary_extension('test.py'))
        self.assertFalse(is_binary_extension('test.json'))

    def test_case_insensitive(self):
        """Test that extension detection is case-insensitive."""
        self.assertTrue(is_binary_extension('TEST.EXE'))
        self.assertTrue(is_binary_extension('Test.Dll'))

    def test_no_extension(self):
        """Test files without extension."""
        self.assertFalse(is_binary_extension('Makefile'))
        self.assertFalse(is_binary_extension('README'))


class TestBinaryExtensionsSet(unittest.TestCase):
    """Test the BINARY_EXTENSIONS constant."""

    def test_binary_extensions_defined(self):
        """Test that BINARY_EXTENSIONS contains expected extensions."""
        self.assertIn('.exe', BINARY_EXTENSIONS)
        self.assertIn('.dll', BINARY_EXTENSIONS)
        self.assertIn('.elf', BINARY_EXTENSIONS)
        self.assertIn('.so', BINARY_EXTENSIONS)
        self.assertIn('.dylib', BINARY_EXTENSIONS)
        self.assertIn('.bin', BINARY_EXTENSIONS)


class TestFixtureFileDetection(unittest.TestCase):
    """Test file detection using actual test fixture files."""

    @classmethod
    def setUpClass(cls):
        """Get the path to the fixtures directory."""
        import os
        cls.fixtures_dir = os.path.join(
            os.path.dirname(__file__), 'fixtures'
        )

    def test_detect_elf_fixtures(self):
        """Test detection of ELF files in fixtures."""
        elf_files = [
            'binaries/lib/libtest.so',
            'binaries/lib/libc.so.6',
            'binaries/bin/testapp',
            'binaries/bin/ls',
            'binaries/usr/lib/libnested.so',
            'binaries/deep/level1/level2/level3/deep_binary.so',
            'binaries/no_ext_binary',
            'mixed/binary.elf',
        ]

        for file_path in elf_files:
            full_path = os.path.join(self.fixtures_dir, file_path)
            if os.path.exists(full_path):
                file_type = detect_file_type(full_path)
                self.assertEqual(
                    file_type,
                    FileType.ELF,
                    f"Failed to detect ELF file: {file_path}"
                )
                # Also verify it's detected as binary
                self.assertTrue(
                    is_binary_file(full_path),
                    f"ELF file not detected as binary: {file_path}"
                )

    def test_detect_pe_fixtures(self):
        """Test detection of PE files in fixtures."""
        pe_files = [
            'binaries/program.exe',
            'binaries/library.dll',
            'mixed/app.exe',
        ]

        for file_path in pe_files:
            full_path = os.path.join(self.fixtures_dir, file_path)
            if os.path.exists(full_path):
                file_type = detect_file_type(full_path)
                self.assertEqual(
                    file_type,
                    FileType.PE,
                    f"Failed to detect PE file: {file_path}"
                )
                # Also verify it's detected as binary
                self.assertTrue(
                    is_binary_file(full_path),
                    f"PE file not detected as binary: {file_path}"
                )

    def test_detect_macho_fixtures(self):
        """Test detection of MachO files in fixtures."""
        macho_files = [
            'binaries/app.dylib',
            'binaries/libfoo.dylib',
            'binaries/macho.bin',
        ]

        for file_path in macho_files:
            full_path = os.path.join(self.fixtures_dir, file_path)
            if os.path.exists(full_path):
                file_type = detect_file_type(full_path)
                self.assertEqual(
                    file_type,
                    FileType.MACHO,
                    f"Failed to detect MachO file: {file_path}"
                )
                # Also verify it's detected as binary
                self.assertTrue(
                    is_binary_file(full_path),
                    f"MachO file not detected as binary: {file_path}"
                )

    def test_skip_text_fixtures(self):
        """Test that text files are not detected as binary."""
        text_files = [
            'text/readme.txt',
            'text/notes.md',
            'text/document.txt',
            'text/no_ext_text',
            'mixed/readme.txt',
        ]

        for file_path in text_files:
            full_path = os.path.join(self.fixtures_dir, file_path)
            if os.path.exists(full_path):
                self.assertFalse(
                    is_binary_file(full_path),
                    f"Text file incorrectly detected as binary: {file_path}"
                )
                # Should also have unknown file type
                file_type = detect_file_type(full_path)
                self.assertEqual(
                    file_type,
                    FileType.UNKNOWN,
                    f"Text file has known file type: {file_path}"
                )

    def test_skip_config_fixtures(self):
        """Test that config files are not detected as binary."""
        config_files = [
            'config/app.conf',
            'config/config.json',
            'config/settings.yaml',
            'config/data.xml',
            'mixed/config.json',
        ]

        for file_path in config_files:
            full_path = os.path.join(self.fixtures_dir, file_path)
            if os.path.exists(full_path):
                self.assertFalse(
                    is_binary_file(full_path),
                    f"Config file incorrectly detected as binary: {file_path}"
                )
                file_type = detect_file_type(full_path)
                self.assertEqual(
                    file_type,
                    FileType.UNKNOWN,
                    f"Config file has known file type: {file_path}"
                )

    def test_fake_binary_files(self):
        """Test detection of fake binary files (text with binary extensions)."""
        # These files have binary extensions but contain text content
        fake_files = [
            'binaries/fake_binary.elf',  # Text file with .elf extension
            'binaries/fake_exe.exe',     # Text file with .exe extension
        ]

        for file_path in fake_files:
            full_path = os.path.join(self.fixtures_dir, file_path)
            if os.path.exists(full_path):
                # Should not be detected as binary (no magic number)
                self.assertFalse(
                    is_binary_file(full_path),
                    f"Fake binary file detected as binary: {file_path}"
                )
                # Should still detect file type by extension
                file_type = detect_file_type(full_path)
                self.assertNotEqual(
                    file_type,
                    FileType.UNKNOWN,
                    f"Fake binary file should be detected by extension: {file_path}"
                )

    def test_extension_based_detection_for_fixtures(self):
        """Test extension-based detection for files without magic numbers."""
        # Test files with binary extensions but text content
        fake_elf = os.path.join(self.fixtures_dir, 'binaries/fake_binary.elf')
        fake_exe = os.path.join(self.fixtures_dir, 'binaries/fake_exe.exe')

        if os.path.exists(fake_elf):
            file_type = detect_file_type(fake_elf)
            self.assertEqual(
                file_type,
                FileType.ELF,
                "Should detect ELF by extension despite text content"
            )

        if os.path.exists(fake_exe):
            file_type = detect_file_type(fake_exe)
            self.assertEqual(
                file_type,
                FileType.PE,
                "Should detect PE by extension despite text content"
            )

    def test_files_without_extensions(self):
        """Test detection of files without extensions."""
        no_ext_binary = os.path.join(self.fixtures_dir, 'binaries/no_ext_binary')
        no_ext_text = os.path.join(self.fixtures_dir, 'text/no_ext_text')

        if os.path.exists(no_ext_binary):
            # Binary file with magic number but no extension
            file_type = detect_file_type(no_ext_binary)
            self.assertEqual(
                file_type,
                FileType.ELF,
                "Should detect binary by magic number without extension"
            )
            self.assertTrue(
                is_binary_file(no_ext_binary),
                "Binary file without extension should be detected as binary"
            )

        if os.path.exists(no_ext_text):
            # Text file without extension
            self.assertFalse(
                is_binary_file(no_ext_text),
                "Text file without extension should not be detected as binary"
            )
            file_type = detect_file_type(no_ext_text)
            self.assertEqual(
                file_type,
                FileType.UNKNOWN,
                "Text file without extension should be UNKNOWN"
            )

    def test_deep_nested_files(self):
        """Test detection of files in deeply nested directories."""
        deep_binary = os.path.join(
            self.fixtures_dir,
            'binaries/deep/level1/level2/level3/deep_binary.so'
        )
        deep_text = os.path.join(
            self.fixtures_dir,
            'binaries/deep/level1/level2/level3/readme.txt'
        )

        if os.path.exists(deep_binary):
            file_type = detect_file_type(deep_binary)
            self.assertEqual(
                file_type,
                FileType.ELF,
                "Should detect binary in deeply nested directory"
            )
            self.assertTrue(is_binary_file(deep_binary))

        if os.path.exists(deep_text):
            self.assertFalse(
                is_binary_file(deep_text),
                "Should not detect text in deeply nested directory as binary"
            )


if __name__ == '__main__':
    unittest.main()
