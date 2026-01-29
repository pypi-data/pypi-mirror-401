"""
End-to-end integration tests for plugin system.

These tests verify that the complete plugin pipeline works correctly:
- Plugin discovery from filesystem
- Plugin loading and initialization
- Binary parsing with plugins
- SPDX document generation from plugin metadata
- Integration with existing analyzer infrastructure

Tests use real plugin files and temporary test plugins to verify
the complete workflow from discovery to SPDX generation.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Dict, Any

# Try to import plugin system components
try:
    from binary_sbom.plugins import (
        BinaryParserPlugin,
        discover_plugins,
        load_plugin,
        registry,
        create_spdx_from_plugin_metadata,
    )
    from binary_sbom.plugins.registry import PluginRegistry
    PLUGINS_AVAILABLE = True
except ImportError:
    PLUGINS_AVAILABLE = False

# Try to import spdx-tools for SPDX integration tests
try:
    from spdx_tools.spdx.model import Document
    SPDX_TOOLS_AVAILABLE = True
except ImportError:
    SPDX_TOOLS_AVAILABLE = False


class TestPluginDiscoveryE2E(unittest.TestCase):
    """
    End-to-end tests for plugin discovery.

    Verifies that plugins can be discovered from real directories,
    including handling of edge cases like missing directories and
    permission issues.
    """

    def test_discover_plugins_from_example_directory(self):
        """Test discovering plugins from the plugins directory."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        # Discover from the example plugins directory
        plugin_dir = Path(__file__).parent.parent / "plugins"
        if not plugin_dir.exists():
            self.skipTest("Example plugins directory not found")

        plugin_files = discover_plugins(plugin_dir)

        # Verify discovery results
        self.assertIsInstance(plugin_files, list)
        self.assertGreater(len(plugin_files), 0, "Should discover at least one plugin")

        # All returned items should be Path objects pointing to .py files
        for plugin_path in plugin_files:
            self.assertIsInstance(plugin_path, Path)
            self.assertEqual(plugin_path.suffix, ".py")
            self.assertTrue(plugin_path.exists())

    def test_discover_plugins_creates_missing_directory(self):
        """Test that missing plugin directory is created automatically."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        with tempfile.TemporaryDirectory() as tmpdir:
            missing_dir = Path(tmpdir) / "nonexistent" / "plugins"

            # Directory shouldn't exist initially
            self.assertFalse(missing_dir.exists())

            # Discover should create it
            plugin_files = discover_plugins(missing_dir)

            # Directory should now exist
            self.assertTrue(missing_dir.exists())
            self.assertIsInstance(plugin_files, list)

    def test_discover_plugins_filters_private_files(self):
        """Test that private files are filtered out during discovery."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_dir = Path(tmpdir)

            # Create mix of public and private files
            (plugin_dir / "public_plugin.py").touch()
            (plugin_dir / "_private_helper.py").touch()
            (plugin_dir / "__init__.py").touch()
            (plugin_dir / "another_public.py").touch()

            plugin_files = discover_plugins(plugin_dir)

            # Should only discover public plugins
            plugin_names = [p.name for p in plugin_files]
            self.assertIn("public_plugin.py", plugin_names)
            self.assertIn("another_public.py", plugin_names)
            self.assertNotIn("_private_helper.py", plugin_names)
            self.assertNotIn("__init__.py", plugin_names)


class TestPluginLoadingE2E(unittest.TestCase):
    """
    End-to-end tests for plugin loading.

    Verifies that discovered plugins can be loaded, instantiated,
    and registered correctly.
    """

    def test_load_and_instantiate_example_plugin(self):
        """Test loading and instantiating the example firmware parser."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        # Find example plugin
        plugin_dir = Path(__file__).parent.parent / "plugins"
        example_plugin = plugin_dir / "example_firmware_parser.py"

        if not example_plugin.exists():
            self.skipTest("Example plugin not found")

        # Load the plugin
        plugin_class = load_plugin(example_plugin)
        self.assertIsNotNone(plugin_class, "Plugin should load successfully")

        # Verify it's a class
        self.assertIsInstance(plugin_class, type)

        # Instantiate the plugin
        plugin_instance = plugin_class()
        self.assertIsNotNone(plugin_instance, "Plugin should instantiate")

        # Verify plugin interface
        self.assertIsInstance(plugin_instance, BinaryParserPlugin)
        self.assertTrue(hasattr(plugin_instance, "get_name"))
        self.assertTrue(hasattr(plugin_instance, "get_supported_formats"))
        self.assertTrue(hasattr(plugin_instance, "can_parse"))
        self.assertTrue(hasattr(plugin_instance, "parse"))

    def test_register_and_retrieve_plugin(self):
        """Test registering plugin and retrieving from registry."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        # Create a fresh registry
        test_registry = PluginRegistry()

        # Create a test plugin class
        class TestE2EPlugin(BinaryParserPlugin):
            def get_name(self):
                return "TestE2EPlugin"

            def get_supported_formats(self):
                return ['.e2e']

            def can_parse(self, file_path):
                return file_path.suffix == '.e2e'

            def parse(self, file_path):
                return {
                    'packages': [],
                    'relationships': [],
                    'annotations': []
                }

        # Register the plugin
        success = test_registry.register(TestE2EPlugin)
        self.assertTrue(success, "Plugin should register successfully")

        # Retrieve by name
        retrieved = test_registry.get_plugin("TestE2EPlugin")
        self.assertIs(retrieved, TestE2EPlugin)

        # Find handler for supported format
        handler = test_registry.find_handler(Path('/test/file.e2e'))
        self.assertIs(handler, TestE2EPlugin)

    def test_load_multiple_plugins(self):
        """Test loading and registering multiple plugins."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_dir = Path(tmpdir)

            # Create multiple test plugins
            plugins_created = []
            for i in range(3):
                plugin_code = f'''
from binary_sbom.plugins import BinaryParserPlugin

class Plugin{i}(BinaryParserPlugin):
    def get_name(self):
        return "Plugin{i}"

    def get_supported_formats(self):
        return ['.p{i}']

    def can_parse(self, file_path):
        return file_path.suffix == '.p{i}'

    def parse(self, file_path):
        return {{'packages': [], 'relationships': [], 'annotations': []}}
'''
                plugin_file = plugin_dir / f"plugin_{i}.py"
                plugin_file.write_text(plugin_code)
                plugins_created.append(plugin_file)

            # Load all plugins
            test_registry = PluginRegistry()
            loaded_count = 0

            for plugin_path in plugins_created:
                plugin_class = load_plugin(plugin_path)
                if plugin_class:
                    test_registry.register(plugin_class)
                    loaded_count += 1

            # All plugins should load successfully
            self.assertEqual(loaded_count, 3, "All plugins should load")

            # Verify all are registered
            for i in range(3):
                plugin = test_registry.get_plugin(f"Plugin{i}")
                self.assertIsNotNone(plugin, f"Plugin{i} should be registered")


class TestPluginParsingE2E(unittest.TestCase):
    """
    End-to-end tests for plugin-based binary parsing.

    Verifies that plugins can successfully parse binary files
    and return valid metadata.
    """

    def test_example_plugin_creates_valid_metadata(self):
        """Test that example plugin returns valid metadata structure."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        # Load example plugin
        plugin_dir = Path(__file__).parent.parent / "plugins"
        example_plugin = plugin_dir / "example_firmware_parser.py"

        if not example_plugin.exists():
            self.skipTest("Example plugin not found")

        plugin_class = load_plugin(example_plugin)
        if not plugin_class:
            self.skipTest("Example plugin failed to load")

        plugin = plugin_class()

        # Create a test XFW file
        with tempfile.NamedTemporaryFile(suffix='.xfw', delete=False, mode='wb') as f:
            # Write a valid XFW header
            import struct
            magic = b'XFW'
            version = 1
            name = b'testfirm\x00\x00\x00'
            flags = 0x01020304
            header = struct.pack('<3sB8sI', magic, version, name, flags)
            f.write(header)
            test_file = Path(f.name)

        try:
            # Verify plugin can parse the file
            self.assertTrue(plugin.can_parse(test_file))

            # Parse the file
            metadata = plugin.parse(test_file)

            # Verify metadata structure
            self.assertIsInstance(metadata, dict)
            self.assertIn('packages', metadata)
            self.assertIn('relationships', metadata)
            self.assertIn('annotations', metadata)

            # Verify types
            self.assertIsInstance(metadata['packages'], list)
            self.assertIsInstance(metadata['relationships'], list)
            self.assertIsInstance(metadata['annotations'], list)

            # At least the firmware package should be present
            self.assertGreater(len(metadata['packages']), 0)

            # Verify first package has required fields
            first_package = metadata['packages'][0]
            self.assertIn('name', first_package)
            self.assertIn('spdx_id', first_package)

        finally:
            test_file.unlink()

    def test_plugin_rejects_incompatible_files(self):
        """Test that plugin correctly rejects non-matching files."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        # Create a test plugin
        class TestPlugin(BinaryParserPlugin):
            def get_name(self):
                return "TestPlugin"

            def get_supported_formats(self):
                return ['.test']

            def can_parse(self, file_path):
                return file_path.suffix == '.test'

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        plugin = TestPlugin()

        # Create test files with different extensions
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir)

            matching_file = test_dir / "file.test"
            non_matching_file = test_dir / "file.other"

            matching_file.touch()
            non_matching_file.touch()

            # Plugin should accept .test file
            self.assertTrue(plugin.can_parse(matching_file))

            # Plugin should reject .other file
            self.assertFalse(plugin.can_parse(non_matching_file))


@unittest.skipIf(not SPDX_TOOLS_AVAILABLE, "spdx-tools not installed")
class TestSPDXIntegrationE2E(unittest.TestCase):
    """
    End-to-end tests for SPDX document generation from plugin metadata.

    Verifies that metadata produced by plugins can be converted into
    valid SPDX documents.
    """

    def test_create_spdx_from_plugin_metadata(self):
        """Test complete SPDX document creation from plugin metadata."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        # Create sample plugin metadata
        metadata = {
            'packages': [
                {
                    'name': 'test-firmware',
                    'version': '1.0.0',
                    'type': 'firmware',
                    'spdx_id': 'SPDXRef-firmware',
                    'download_location': 'NOASSERTION',
                }
            ],
            'relationships': [
                {
                    'source': 'SPDXRef-firmware',
                    'type': 'CONTAINS',
                    'target': 'SPDXRef-component'
                }
            ],
            'annotations': [
                {
                    'spdx_id': 'SPDXRef-firmware',
                    'type': 'OTHER',
                    'text': 'Test annotation'
                }
            ]
        }

        file_path = Path('/test/firmware.bin')

        # Create SPDX document
        try:
            spdx_doc = create_spdx_from_plugin_metadata(metadata, file_path)
            self.assertIsNotNone(spdx_doc)

            # Verify it's a valid SPDX Document
            self.assertIsInstance(spdx_doc, Document)

            # Verify document has expected properties
            self.assertIsNotNone(spdx_doc.creation_info)
            self.assertIsNotNone(spdx_doc.creation_info.spdx_id)
            self.assertEqual(spdx_doc.creation_info.spdx_id, "SPDXRef-DOCUMENT")

        except ImportError:
            self.skipTest("spdx-tools library not available")

    def test_spdx_generation_with_plugin_name_annotation(self):
        """Test that plugin name is added as document annotation."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        metadata = {
            'packages': [],
            'relationships': [],
            'annotations': [],
            'plugin_name': 'TestPlugin'
        }

        file_path = Path('/test/file.bin')

        try:
            spdx_doc = create_spdx_from_plugin_metadata(metadata, file_path)
            self.assertIsNotNone(spdx_doc)

            # Verify plugin annotation exists
            # (The annotation should mention the plugin name)
            has_plugin_annotation = any(
                'TestPlugin' in str(ann.annotation_comment)
                for ann in spdx_doc.annotations
            )
            self.assertTrue(has_plugin_annotation, "Plugin name should be in annotations")

        except ImportError:
            self.skipTest("spdx-tools library not available")


class TestCompletePipelineE2E(unittest.TestCase):
    """
    End-to-end tests for the complete plugin pipeline.

    Tests the full workflow: discovery -> loading -> parsing -> SPDX.
    """

    def test_full_pipeline_with_test_plugin(self):
        """Test complete pipeline from discovery to SPDX generation."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        # Step 1: Create a test plugin directory
        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_dir = Path(tmpdir)

            # Create a test plugin
            plugin_code = '''
from binary_sbom.plugins import BinaryParserPlugin

class PipelineTestPlugin(BinaryParserPlugin):
    def get_name(self):
        return "PipelineTestPlugin"

    def get_supported_formats(self):
        return ['.ptest']

    def can_parse(self, file_path):
        return file_path.suffix == '.ptest'

    def parse(self, file_path):
        return {
            'packages': [
                {
                    'name': 'test-package',
                    'version': '1.0',
                    'type': 'library',
                    'spdx_id': 'SPDXRef-test'
                }
            ],
            'relationships': [],
            'annotations': [
                {
                    'spdx_id': 'SPDXRef-test',
                    'type': 'OTHER',
                    'text': 'Parsed by PipelineTestPlugin'
                }
            ]
        }

    @property
    def version(self):
        return "1.0.0"
'''

            plugin_file = plugin_dir / "pipeline_test.py"
            plugin_file.write_text(plugin_code)

            # Step 2: Discover plugins
            discovered = discover_plugins(plugin_dir)
            self.assertEqual(len(discovered), 1)
            self.assertEqual(discovered[0].name, "pipeline_test.py")

            # Step 3: Load plugin
            plugin_class = load_plugin(discovered[0])
            self.assertIsNotNone(plugin_class)

            # Step 4: Register plugin
            test_registry = PluginRegistry()
            success = test_registry.register(plugin_class)
            self.assertTrue(success)

            # Step 5: Find handler
            test_file = Path(tmpdir) / "test.ptest"
            test_file.touch()

            handler = test_registry.find_handler(test_file)
            self.assertIsNotNone(handler)
            self.assertEqual(handler().get_name(), "PipelineTestPlugin")

            # Step 6: Parse file
            plugin_instance = handler()
            metadata = plugin_instance.parse(test_file)

            self.assertIn('packages', metadata)
            self.assertEqual(len(metadata['packages']), 1)
            self.assertEqual(metadata['packages'][0]['name'], 'test-package')

            # Step 7: Generate SPDX (if available)
            if SPDX_TOOLS_AVAILABLE:
                try:
                    spdx_doc = create_spdx_from_plugin_metadata(metadata, test_file)
                    self.assertIsNotNone(spdx_doc)
                    self.assertIsInstance(spdx_doc, Document)
                except ImportError:
                    pass  # SPDX tools not available

    def test_multiple_plugins_format_selection(self):
        """Test that correct plugin is selected for different formats."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_dir = Path(tmpdir)

            # Create two plugins for different formats
            plugin1_code = '''
from binary_sbom.plugins import BinaryParserPlugin

class Format1Plugin(BinaryParserPlugin):
    def get_name(self):
        return "Format1Plugin"

    def get_supported_formats(self):
        return ['.fmt1']

    def can_parse(self, file_path):
        return file_path.suffix == '.fmt1'

    def parse(self, file_path):
        return {'packages': [], 'relationships': [], 'annotations': []}
'''

            plugin2_code = '''
from binary_sbom.plugins import BinaryParserPlugin

class Format2Plugin(BinaryParserPlugin):
    def get_name(self):
        return "Format2Plugin"

    def get_supported_formats(self):
        return ['.fmt2']

    def can_parse(self, file_path):
        return file_path.suffix == '.fmt2'

    def parse(self, file_path):
        return {'packages': [], 'relationships': [], 'annotations': []}
'''

            (plugin_dir / "fmt1.py").write_text(plugin1_code)
            (plugin_dir / "fmt2.py").write_text(plugin2_code)

            # Load both plugins
            test_registry = PluginRegistry()

            for plugin_file in discover_plugins(plugin_dir):
                plugin_class = load_plugin(plugin_file)
                if plugin_class:
                    test_registry.register(plugin_class)

            # Verify correct handler is selected for each format
            fmt1_handler = test_registry.find_handler(Path('/test/file.fmt1'))
            fmt2_handler = test_registry.find_handler(Path('/test/file.fmt2'))

            self.assertIsNotNone(fmt1_handler)
            self.assertIsNotNone(fmt2_handler)

            # Handlers should be different
            self.assertNotEqual(fmt1_handler, fmt2_handler)

            # Verify correct handler for each format
            self.assertEqual(fmt1_handler().get_name(), "Format1Plugin")
            self.assertEqual(fmt2_handler().get_name(), "Format2Plugin")


class TestErrorHandlingE2E(unittest.TestCase):
    """
    End-to-end tests for error handling in the plugin pipeline.

    Verifies that errors are handled gracefully at each stage:
    - Discovery failures
    - Loading failures
    - Parsing failures
    - SPDX generation failures
    """

    def test_plugin_loading_failure_graceful(self):
        """Test that plugin loading failures are handled gracefully."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_dir = Path(tmpdir)

            # Create a plugin with syntax error
            bad_plugin = plugin_dir / "bad_plugin.py"
            bad_plugin.write_text("this is not valid python syntax {{{")

            # Discover should find it
            discovered = discover_plugins(plugin_dir)
            self.assertEqual(len(discovered), 1)

            # Load should fail gracefully
            plugin_class = load_plugin(discovered[0])
            self.assertIsNone(plugin_class, "Bad plugin should return None")

    def test_parse_nonexistent_file(self):
        """Test that parsing nonexistent file raises appropriate error."""
        if not PLUGINS_AVAILABLE:
            self.skipTest("Plugin system not available")

        # Create test plugin
        class TestPlugin(BinaryParserPlugin):
            def get_name(self):
                return "TestPlugin"

            def get_supported_formats(self):
                return ['.test']

            def can_parse(self, file_path):
                return file_path.suffix == '.test'

            def parse(self, file_path):
                if not file_path.exists():
                    raise FileNotFoundError(f"File not found: {file_path}")
                return {'packages': [], 'relationships': [], 'annotations': []}

        plugin = TestPlugin()

        # Should raise FileNotFoundError for non-existent file
        with self.assertRaises(FileNotFoundError):
            plugin.parse(Path('/nonexistent/file.test'))

    def test_invalid_metadata_structure(self):
        """Test SPDX generation with invalid metadata."""
        if not PLUGINS_AVAILABLE or not SPDX_TOOLS_AVAILABLE:
            self.skipTest("Plugin system or spdx-tools not available")

        # Missing required keys
        invalid_metadata = {}

        file_path = Path('/test/file.bin')

        # Should raise ValueError for invalid metadata
        with self.assertRaises(ValueError):
            create_spdx_from_plugin_metadata(invalid_metadata, file_path)


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
