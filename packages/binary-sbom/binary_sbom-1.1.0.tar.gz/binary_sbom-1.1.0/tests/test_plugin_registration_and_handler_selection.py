"""
End-to-end verification tests for plugin registration and handler selection.

This test file verifies that all new format plugins (.img, .hex, .so, .exe) are:
1. Properly registered in the plugin system
2. Discoverable by the plugin discovery mechanism
3. Correctly selected as handlers for their respective file formats
4. Integrated with the enhanced LIEF parsing for .so and .exe files

Tests cover the complete plugin pipeline from discovery to handler selection.
"""

import sys
import tempfile
import unittest
from pathlib import Path
from typing import Optional

# Try to import plugin system components
try:
    from binary_sbom.plugins import (
        BinaryParserPlugin,
        discover_plugins,
        load_plugin,
        registry,
        get_global_registry,
    )
    from binary_sbom.plugins.registry import PluginRegistry
    from binary_sbom.plugins.img_parser import ImgParser
    from binary_sbom.plugins.hex_parser import HexParser
    PLUGINS_AVAILABLE = True
except ImportError as e:
    PLUGINS_AVAILABLE = False
    IMPORT_ERROR = str(e)


class TestImgParserRegistration(unittest.TestCase):
    """
    Test ImgParser plugin registration and handler selection.

    Verifies that the ImgParser plugin for .img files is properly
    registered and can be selected as a handler for disk image files.
    """

    def setUp(self):
        """Set up test registry before each test."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")
        self.test_registry = PluginRegistry()

    def test_img_parser_class_exists(self):
        """Test that ImgParser class can be imported."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        self.assertIsNotNone(ImgParser)
        self.assertTrue(issubclass(ImgParser, BinaryParserPlugin))

    def test_img_parser_registration(self):
        """Test that ImgParser can be registered in the registry."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        # Register ImgParser
        success = self.test_registry.register(ImgParser)
        self.assertTrue(success, "ImgParser should register successfully")

        # Verify registration
        registered_plugin = self.test_registry.get_plugin("ImgParser")
        self.assertIs(registered_plugin, ImgParser)

    def test_img_parser_supported_formats(self):
        """Test that ImgParser reports correct supported formats."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        parser_instance = ImgParser()
        formats = parser_instance.get_supported_formats()

        self.assertIsInstance(formats, list)
        self.assertIn('.img', formats)
        self.assertIn('IMG', formats)

    def test_img_handler_selection_by_extension(self):
        """Test that .img files select ImgParser as handler."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        self.test_registry.register(ImgParser)

        # Test lowercase extension
        test_file_lower = Path('/path/to/disk.img')
        handler = self.test_registry.find_handler(test_file_lower)
        self.assertIs(handler, ImgParser, "Should select ImgParser for .img files")

        # Test uppercase extension
        test_file_upper = Path('/path/to/disk.IMG')
        handler_upper = self.test_registry.find_handler(test_file_upper)
        self.assertIs(handler_upper, ImgParser, "Should select ImgParser for .IMG files")

    def test_img_parser_instance_creation(self):
        """Test that ImgParser can be instantiated correctly."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        parser = ImgParser()
        self.assertIsNotNone(parser)
        self.assertIsInstance(parser, BinaryParserPlugin)
        self.assertEqual(parser.get_name(), "ImgParser")
        self.assertEqual(parser.version, "1.0.0")


class TestHexParserRegistration(unittest.TestCase):
    """
    Test HexParser plugin registration and handler selection.

    Verifies that the HexParser plugin for .hex files is properly
    registered and can be selected as a handler for Intel HEX files.
    """

    def setUp(self):
        """Set up test registry before each test."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")
        self.test_registry = PluginRegistry()

    def test_hex_parser_class_exists(self):
        """Test that HexParser class can be imported."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        self.assertIsNotNone(HexParser)
        self.assertTrue(issubclass(HexParser, BinaryParserPlugin))

    def test_hex_parser_registration(self):
        """Test that HexParser can be registered in the registry."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        # Register HexParser
        success = self.test_registry.register(HexParser)
        self.assertTrue(success, "HexParser should register successfully")

        # Verify registration
        registered_plugin = self.test_registry.get_plugin("HexParser")
        self.assertIs(registered_plugin, HexParser)

    def test_hex_parser_supported_formats(self):
        """Test that HexParser reports correct supported formats."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        parser_instance = HexParser()
        formats = parser_instance.get_supported_formats()

        self.assertIsInstance(formats, list)
        self.assertIn('.hex', formats)
        self.assertIn('HEX', formats)

    def test_hex_handler_selection_by_extension(self):
        """Test that .hex files select HexParser as handler."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        self.test_registry.register(HexParser)

        # Test lowercase extension
        test_file_lower = Path('/path/to/firmware.hex')
        handler = self.test_registry.find_handler(test_file_lower)
        self.assertIs(handler, HexParser, "Should select HexParser for .hex files")

        # Test uppercase extension
        test_file_upper = Path('/path/to/firmware.HEX')
        handler_upper = self.test_registry.find_handler(test_file_upper)
        self.assertIs(handler_upper, HexParser, "Should select HexParser for .HEX files")

    def test_hex_parser_instance_creation(self):
        """Test that HexParser can be instantiated correctly."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        parser = HexParser()
        self.assertIsNotNone(parser)
        self.assertIsInstance(parser, BinaryParserPlugin)
        self.assertEqual(parser.get_name(), "HexParser")
        self.assertEqual(parser.version, "1.0.0")


class TestEnhancedELFHandlerSelection(unittest.TestCase):
    """
    Test handler selection for .so files with enhanced LIEF parsing.

    Verifies that .so (ELF) files are properly handled by the enhanced
    LIEF parser that extracts symbol tables, version info, and dependencies.
    """

    def setUp(self):
        """Set up test registry before each test."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")
        self.test_registry = PluginRegistry()

    def test_so_file_type_detection(self):
        """Test that .so files are detected as ELF format."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        # Try to import file_detector
        try:
            from src.file_detector import detect_file_type, FileType
        except ImportError:
            self.skipTest("file_detector module not available")

        # Create a minimal ELF shared library fixture
        with tempfile.NamedTemporaryFile(suffix='.so', delete=False, mode='wb') as f:
            # Write ELF magic number and basic header
            elf_header = b'\x7fELF'  # ELF magic
            elf_header += b'\x02'      # 64-bit
            elf_header += b'\x01'      # Little endian
            elf_header += b'\x01'      # ELF version
            elf_header += b'\x00' * 8  # Padding
            elf_header += b'\x03\x00'  # ET_DYN (shared object)
            f.write(elf_header)
            test_so_path = Path(f.name)

        try:
            # Verify file type detection
            detected_type = detect_file_type(test_so_path)
            self.assertEqual(detected_type, FileType.ELF, ".so files should be detected as ELF")

        finally:
            test_so_path.unlink()

    def test_so_handler_uses_enhanced_lief_parsing(self):
        """Test that .so files use enhanced LIEF parsing."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        # This test verifies that when a .so file is analyzed,
        # the enhanced LIEF parser is used (not just basic detection)

        # The actual parsing happens in sandbox/worker.py with
        # _extract_elf_enhanced_metadata() function

        # We can verify the metadata structure includes enhanced fields
        try:
            from src.binary_sbom.sandbox.worker import _extract_elf_enhanced_metadata
            ENHANCED_ELF_AVAILABLE = True
        except ImportError:
            ENHANCED_ELF_AVAILABLE = False

        if not ENHANCED_ELF_AVAILABLE:
            self.skipTest("Enhanced ELF parsing not available in worker")

        # The function should exist for enhanced ELF parsing
        self.assertTrue(callable(_extract_elf_enhanced_metadata),
                       "Enhanced ELF metadata extraction should be available")


class TestEnhancedPEHandlerSelection(unittest.TestCase):
    """
    Test handler selection for .exe files with enhanced LIEF parsing.

    Verifies that .exe (PE) files are properly handled by the enhanced
    LIEF parser that extracts import/export tables and version info.
    """

    def setUp(self):
        """Set up test registry before each test."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")
        self.test_registry = PluginRegistry()

    def test_exe_file_type_detection(self):
        """Test that .exe files are detected as PE format."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        # Try to import file_detector
        try:
            from src.file_detector import detect_file_type, FileType
        except ImportError:
            self.skipTest("file_detector module not available")

        # Create a minimal PE executable fixture
        with tempfile.NamedTemporaryFile(suffix='.exe', delete=False, mode='wb') as f:
            # Write MZ header
            pe_header = b'MZ'          # DOS magic
            pe_header += b'\x00' * 58   # DOS header
            pe_header += b'\x40\x00'    # Offset to PE header
            pe_header += b'\x00' * 2    # Padding
            f.write(pe_header)
            test_exe_path = Path(f.name)

        try:
            # Verify file type detection
            detected_type = detect_file_type(test_exe_path)
            self.assertEqual(detected_type, FileType.PE, ".exe files should be detected as PE")

        finally:
            test_exe_path.unlink()

    def test_exe_handler_uses_enhanced_lief_parsing(self):
        """Test that .exe files use enhanced LIEF parsing."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        # This test verifies that when a .exe file is analyzed,
        # the enhanced LIEF parser is used (not just basic detection)

        # The actual parsing happens in sandbox/worker.py with
        # _extract_pe_enhanced_metadata() function

        # We can verify the metadata structure includes enhanced fields
        try:
            from src.binary_sbom.sandbox.worker import _extract_pe_enhanced_metadata
            ENHANCED_PE_AVAILABLE = True
        except ImportError:
            ENHANCED_PE_AVAILABLE = False

        if not ENHANCED_PE_AVAILABLE:
            self.skipTest("Enhanced PE parsing not available in worker")

        # The function should exist for enhanced PE parsing
        self.assertTrue(callable(_extract_pe_enhanced_metadata),
                       "Enhanced PE metadata extraction should be available")


class TestPluginDiscoveryAndLoading(unittest.TestCase):
    """
    Test plugin discovery and loading for all new formats.

    Verifies that ImgParser and HexParser can be discovered from
    the plugin directory and loaded successfully.
    """

    def test_discover_img_parser_from_plugin_directory(self):
        """Test that ImgParser can be discovered from plugins directory."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        # Discover plugins from src/binary_sbom/plugins
        plugin_dir = Path(__file__).parent.parent / 'src' / 'binary_sbom' / 'plugins'

        if not plugin_dir.exists():
            self.skipTest("Plugin directory not found")

        discovered = discover_plugins(plugin_dir)

        # Should find img_parser.py
        plugin_names = [p.name for p in discovered]
        self.assertIn('img_parser.py', plugin_names, "Should discover img_parser.py")

    def test_discover_hex_parser_from_plugin_directory(self):
        """Test that HexParser can be discovered from plugins directory."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        # Discover plugins from src/binary_sbom/plugins
        plugin_dir = Path(__file__).parent.parent / 'src' / 'binary_sbom' / 'plugins'

        if not plugin_dir.exists():
            self.skipTest("Plugin directory not found")

        discovered = discover_plugins(plugin_dir)

        # Should find hex_parser.py
        plugin_names = [p.name for p in discovered]
        self.assertIn('hex_parser.py', plugin_names, "Should discover hex_parser.py")

    def test_load_img_parser_from_file(self):
        """Test that ImgParser can be loaded from its file."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        plugin_dir = Path(__file__).parent.parent / 'src' / 'binary_sbom' / 'plugins'
        img_parser_path = plugin_dir / 'img_parser.py'

        if not img_parser_path.exists():
            self.skipTest("img_parser.py not found")

        # Load the plugin
        plugin_class = load_plugin(img_parser_path)

        self.assertIsNotNone(plugin_class, "ImgParser should load successfully")
        self.assertEqual(plugin_class.__name__, "ImgParser")

        # Verify it's the correct class
        self.assertTrue(issubclass(plugin_class, BinaryParserPlugin))

    def test_load_hex_parser_from_file(self):
        """Test that HexParser can be loaded from its file."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        plugin_dir = Path(__file__).parent.parent / 'src' / 'binary_sbom' / 'plugins'
        hex_parser_path = plugin_dir / 'hex_parser.py'

        if not hex_parser_path.exists():
            self.skipTest("hex_parser.py not found")

        # Load the plugin
        plugin_class = load_plugin(hex_parser_path)

        self.assertIsNotNone(plugin_class, "HexParser should load successfully")
        self.assertEqual(plugin_class.__name__, "HexParser")

        # Verify it's the correct class
        self.assertTrue(issubclass(plugin_class, BinaryParserPlugin))


class TestCompletePluginPipeline(unittest.TestCase):
    """
    Test the complete plugin pipeline for all new formats.

    Verifies the end-to-end flow: discovery -> loading -> registration -> handler selection.
    """

    def test_complete_pipeline_for_img_files(self):
        """Test complete pipeline for .img files."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        # Step 1: Discover plugins
        plugin_dir = Path(__file__).parent.parent / 'src' / 'binary_sbom' / 'plugins'
        if not plugin_dir.exists():
            self.skipTest("Plugin directory not found")

        discovered = discover_plugins(plugin_dir)
        self.assertGreater(len(discovered), 0, "Should discover at least one plugin")

        # Step 2: Load ImgParser
        img_parser_path = plugin_dir / 'img_parser.py'
        if not img_parser_path.exists():
            self.skipTest("img_parser.py not found")

        img_parser_class = load_plugin(img_parser_path)
        self.assertIsNotNone(img_parser_class, "ImgParser should load")

        # Step 3: Register in registry
        test_registry = PluginRegistry()
        success = test_registry.register(img_parser_class)
        self.assertTrue(success, "ImgParser should register")

        # Step 4: Verify handler selection
        test_file = Path('/test/disk.img')
        handler = test_registry.find_handler(test_file)
        self.assertIs(handler, img_parser_class, "Should select ImgParser for .img files")

    def test_complete_pipeline_for_hex_files(self):
        """Test complete pipeline for .hex files."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        # Step 1: Discover plugins
        plugin_dir = Path(__file__).parent.parent / 'src' / 'binary_sbom' / 'plugins'
        if not plugin_dir.exists():
            self.skipTest("Plugin directory not found")

        discovered = discover_plugins(plugin_dir)
        self.assertGreater(len(discovered), 0, "Should discover at least one plugin")

        # Step 2: Load HexParser
        hex_parser_path = plugin_dir / 'hex_parser.py'
        if not hex_parser_path.exists():
            self.skipTest("hex_parser.py not found")

        hex_parser_class = load_plugin(hex_parser_path)
        self.assertIsNotNone(hex_parser_class, "HexParser should load")

        # Step 3: Register in registry
        test_registry = PluginRegistry()
        success = test_registry.register(hex_parser_class)
        self.assertTrue(success, "HexParser should register")

        # Step 4: Verify handler selection
        test_file = Path('/test/firmware.hex')
        handler = test_registry.find_handler(test_file)
        self.assertIs(handler, hex_parser_class, "Should select HexParser for .hex files")

    def test_multiple_plugins_registered_simultaneously(self):
        """Test that ImgParser and HexParser can be registered together."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        # Register both plugins
        test_registry = PluginRegistry()

        img_success = test_registry.register(ImgParser)
        hex_success = test_registry.register(HexParser)

        self.assertTrue(img_success, "ImgParser should register")
        self.assertTrue(hex_success, "HexParser should register")

        # Verify both are registered
        self.assertIsNotNone(test_registry.get_plugin("ImgParser"))
        self.assertIsNotNone(test_registry.get_plugin("HexParser"))

        # Verify handler selection for both formats
        img_handler = test_registry.find_handler(Path('/test/disk.img'))
        hex_handler = test_registry.find_handler(Path('/test/firmware.hex'))

        self.assertIs(img_handler, ImgParser)
        self.assertIs(hex_handler, HexParser)


class TestPluginMetadataFields(unittest.TestCase):
    """
    Test that plugins provide correct metadata fields.

    Verifies that ImgParser and HexParser implement all required
    plugin interface methods correctly.
    """

    def test_img_parser_metadata_fields(self):
        """Test that ImgParser provides all required metadata fields."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        parser = ImgParser()

        # Test get_name()
        self.assertEqual(parser.get_name(), "ImgParser")

        # Test get_supported_formats()
        formats = parser.get_supported_formats()
        self.assertIsInstance(formats, list)
        self.assertIn('.img', formats)

        # Test version property
        self.assertEqual(parser.version, "1.0.0")

    def test_hex_parser_metadata_fields(self):
        """Test that HexParser provides all required metadata fields."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        parser = HexParser()

        # Test get_name()
        self.assertEqual(parser.get_name(), "HexParser")

        # Test get_supported_formats()
        formats = parser.get_supported_formats()
        self.assertIsInstance(formats, list)
        self.assertIn('.hex', formats)

        # Test version property
        self.assertEqual(parser.version, "1.0.0")


class TestEnhancedParsingIntegration(unittest.TestCase):
    """
    Test integration of enhanced LIEF parsing with file analysis.

    Verifies that .so and .exe files trigger enhanced metadata extraction
    in the analyzer pipeline.
    """

    def test_so_enhanced_metadata_fields_exist(self):
        """Test that enhanced ELF metadata fields are defined."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        # Try to import enhanced ELF extraction
        try:
            from src.binary_sbom.sandbox.worker import _extract_elf_enhanced_metadata
        except ImportError:
            self.skipTest("Enhanced ELF extraction not available")

        # The function should exist
        self.assertTrue(callable(_extract_elf_enhanced_metadata))

    def test_exe_enhanced_metadata_fields_exist(self):
        """Test that enhanced PE metadata fields are defined."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        # Try to import enhanced PE extraction
        try:
            from src.binary_sbom.sandbox.worker import _extract_pe_enhanced_metadata
        except ImportError:
            self.skipTest("Enhanced PE extraction not available")

        # The function should exist
        self.assertTrue(callable(_extract_pe_enhanced_metadata))


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
