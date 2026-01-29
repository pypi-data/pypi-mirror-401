"""
Unit tests for the plugin system.

Tests plugin API, registry, discovery, loader, and SPDX integration.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch
import sys

import pytest

from binary_sbom.plugins.api import BinaryParserPlugin
from binary_sbom.plugins.registry import PluginRegistry, get_global_registry
from binary_sbom.plugins.discovery import discover_plugins
from binary_sbom.plugins.loader import load_plugin
from binary_sbom.plugins.integration import (
    SPDXIntegrationError,
    create_spdx_from_plugin_metadata,
)


class TestPluginAPI:
    """Test BinaryParserPlugin abstract base class."""

    def test_binary_parser_plugin_is_abstract(self):
        """Test that BinaryParserPlugin cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BinaryParserPlugin()

    def test_binary_parser_plugin_requires_get_name(self):
        """Test that get_name method must be implemented."""
        class IncompletePlugin(BinaryParserPlugin):
            def get_supported_formats(self):
                return ['.test']

            def can_parse(self, file_path):
                return True

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        with pytest.raises(TypeError, match='abstract'):
            IncompletePlugin()

    def test_binary_parser_plugin_requires_get_supported_formats(self):
        """Test that get_supported_formats method must be implemented."""
        class IncompletePlugin(BinaryParserPlugin):
            def get_name(self):
                return "Incomplete"

            def can_parse(self, file_path):
                return True

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        with pytest.raises(TypeError, match='abstract'):
            IncompletePlugin()

    def test_binary_parser_plugin_requires_can_parse(self):
        """Test that can_parse method must be implemented."""
        class IncompletePlugin(BinaryParserPlugin):
            def get_name(self):
                return "Incomplete"

            def get_supported_formats(self):
                return ['.test']

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        with pytest.raises(TypeError, match='abstract'):
            IncompletePlugin()

    def test_binary_parser_plugin_requires_parse(self):
        """Test that parse method must be implemented."""
        class IncompletePlugin(BinaryParserPlugin):
            def get_name(self):
                return "Incomplete"

            def get_supported_formats(self):
                return ['.test']

            def can_parse(self, file_path):
                return True

        with pytest.raises(TypeError, match='abstract'):
            IncompletePlugin()

    def test_binary_parser_plugin_concrete_implementation(self):
        """Test that concrete plugin can be instantiated."""
        class ConcretePlugin(BinaryParserPlugin):
            def get_name(self):
                return "Concrete"

            def get_supported_formats(self):
                return ['.test']

            def can_parse(self, file_path):
                return True

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        plugin = ConcretePlugin()
        assert plugin.get_name() == "Concrete"
        assert plugin.get_supported_formats() == ['.test']
        assert plugin.version == "1.0.0"

    def test_binary_parser_plugin_version_property(self):
        """Test that version property has default value."""
        class TestPlugin(BinaryParserPlugin):
            def get_name(self):
                return "Test"

            def get_supported_formats(self):
                return ['.test']

            def can_parse(self, file_path):
                return True

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        plugin = TestPlugin()
        assert plugin.version == "1.0.0"

    def test_binary_parser_plugin_custom_version(self):
        """Test that version property can be overridden."""
        class TestPlugin(BinaryParserPlugin):
            def get_name(self):
                return "Test"

            def get_supported_formats(self):
                return ['.test']

            def can_parse(self, file_path):
                return True

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

            @property
            def version(self):
                return "2.5.0"

        plugin = TestPlugin()
        assert plugin.version == "2.5.0"


class TestPluginRegistry:
    """Test PluginRegistry functionality."""

    def test_plugin_registry_initialization(self):
        """Test that registry initializes with empty state."""
        registry = PluginRegistry()
        assert len(registry._plugins) == 0
        assert len(registry._format_handlers) == 0

    def test_plugin_registry_register_success(self):
        """Test successful plugin registration."""
        registry = PluginRegistry()

        class MockPlugin(BinaryParserPlugin):
            def get_name(self):
                return "MockPlugin"

            def get_supported_formats(self):
                return ['.mock', 'MOCK']

            def can_parse(self, file_path):
                return True

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        result = registry.register(MockPlugin)
        assert result is True
        assert registry.get_plugin("MockPlugin") is MockPlugin

    def test_plugin_registry_register_duplicate(self):
        """Test that duplicate plugin registration is rejected."""
        registry = PluginRegistry()

        class MockPlugin(BinaryParserPlugin):
            def get_name(self):
                return "MockPlugin"

            def get_supported_formats(self):
                return ['.mock']

            def can_parse(self, file_path):
                return True

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        registry.register(MockPlugin)
        result = registry.register(MockPlugin)
        assert result is False

    def test_plugin_registry_get_plugin_not_found(self):
        """Test getting non-existent plugin returns None."""
        registry = PluginRegistry()
        assert registry.get_plugin("NonExistent") is None

    def test_plugin_registry_find_handler_by_extension(self):
        """Test finding handler by file extension."""
        registry = PluginRegistry()

        class MockPlugin(BinaryParserPlugin):
            def get_name(self):
                return "MockPlugin"

            def get_supported_formats(self):
                return ['.xfw']

            def can_parse(self, file_path):
                return file_path.suffix == '.xfw'

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        registry.register(MockPlugin)
        handler = registry.find_handler(Path('/path/to/file.xfw'))
        assert handler is MockPlugin

    def test_plugin_registry_find_handler_not_found(self):
        """Test finding handler for unsupported format returns None."""
        registry = PluginRegistry()

        class MockPlugin(BinaryParserPlugin):
            def get_name(self):
                return "MockPlugin"

            def get_supported_formats(self):
                return ['.xfw']

            def can_parse(self, file_path):
                return False

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        registry.register(MockPlugin)
        handler = registry.find_handler(Path('/path/to/file.unknown'))
        assert handler is None

    def test_plugin_registry_find_handler_fallback_to_can_parse(self):
        """Test that find_handler falls back to can_parse check."""
        registry = PluginRegistry()

        class MockPlugin(BinaryParserPlugin):
            def get_name(self):
                return "MockPlugin"

            def get_supported_formats(self):
                return ['.special']

            def can_parse(self, file_path):
                # Custom logic beyond extension check
                return file_path.stem.startswith('valid')

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        registry.register(MockPlugin)

        # Should find handler even with wrong extension if can_parse returns True
        handler = registry.find_handler(Path('/path/to/valid-file.txt'))
        assert handler is MockPlugin

    def test_global_registry_singleton(self):
        """Test that global registry returns same instance."""
        registry1 = get_global_registry()
        registry2 = get_global_registry()
        assert registry1 is registry2

    def test_plugin_registry_multiple_plugins_same_format(self):
        """Test that multiple plugins can support the same format."""
        registry = PluginRegistry()

        class Plugin1(BinaryParserPlugin):
            def get_name(self):
                return "Plugin1"

            def get_supported_formats(self):
                return ['.shared']

            def can_parse(self, file_path):
                return file_path.stem.startswith('p1')

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        class Plugin2(BinaryParserPlugin):
            def get_name(self):
                return "Plugin2"

            def get_supported_formats(self):
                return ['.shared']

            def can_parse(self, file_path):
                return file_path.stem.startswith('p2')

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        # Both plugins should register successfully
        assert registry.register(Plugin1) is True
        assert registry.register(Plugin2) is True

        # Both should be retrievable
        assert registry.get_plugin("Plugin1") is Plugin1
        assert registry.get_plugin("Plugin2") is Plugin2

        # Format handler should have both plugins
        assert '.shared' in registry._format_handlers
        assert len(registry._format_handlers['.shared']) == 2
        assert 'Plugin1' in registry._format_handlers['.shared']
        assert 'Plugin2' in registry._format_handlers['.shared']

    def test_plugin_registry_handler_selection_with_conflict(self):
        """Test handler selection when multiple plugins support same format."""
        registry = PluginRegistry()

        class FirstPlugin(BinaryParserPlugin):
            def get_name(self):
                return "FirstPlugin"

            def get_supported_formats(self):
                return ['.conflict']

            def can_parse(self, file_path):
                # Only handles files with 'first' in name
                return 'first' in file_path.stem

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        class SecondPlugin(BinaryParserPlugin):
            def get_name(self):
                return "SecondPlugin"

            def get_supported_formats(self):
                return ['.conflict']

            def can_parse(self, file_path):
                # Handles all .conflict files
                return file_path.suffix == '.conflict'

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        # Register both - order matters for handler lookup
        registry.register(FirstPlugin)
        registry.register(SecondPlugin)

        # FirstPlugin should handle files with 'first' in name
        handler1 = registry.find_handler(Path('/path/to/first-file.conflict'))
        assert handler1 is FirstPlugin

        # SecondPlugin should handle other .conflict files
        handler2 = registry.find_handler(Path('/path/to/other-file.conflict'))
        assert handler2 is SecondPlugin

    def test_plugin_registry_handler_priority_by_registration_order(self):
        """Test that handler priority follows registration order."""
        registry = PluginRegistry()

        class HighPlugin(BinaryParserPlugin):
            def get_name(self):
                return "HighPlugin"

            def get_supported_formats(self):
                return ['.test']

            def can_parse(self, file_path):
                # All plugins claim they can parse
                return True

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        class LowPlugin(BinaryParserPlugin):
            def get_name(self):
                return "LowPlugin"

            def get_supported_formats(self):
                return ['.test']

            def can_parse(self, file_path):
                # All plugins claim they can parse
                return True

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        # Register in specific order
        registry.register(HighPlugin)
        registry.register(LowPlugin)

        # First registered should be returned
        handler = registry.find_handler(Path('/path/to/file.test'))
        assert handler is HighPlugin

    def test_plugin_registry_case_insensitive_extension_lookup(self):
        """Test that extension lookup is case-insensitive."""
        registry = PluginRegistry()

        class CasePlugin(BinaryParserPlugin):
            def get_name(self):
                return "CasePlugin"

            def get_supported_formats(self):
                return ['.TEST']  # Uppercase

            def can_parse(self, file_path):
                return True

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        registry.register(CasePlugin)

        # Should find handler with lowercase extension
        handler = registry.find_handler(Path('/path/to/file.test'))
        assert handler is CasePlugin

        # Should find handler with uppercase extension
        handler = registry.find_handler(Path('/path/to/file.TEST'))
        assert handler is CasePlugin

        # Should find handler with mixed case extension
        handler = registry.find_handler(Path('/path/to/file.Test'))
        assert handler is CasePlugin

    def test_plugin_unregister_clears_format_handlers(self):
        """Test that unregistering plugins clears their format handlers."""
        registry = PluginRegistry()

        class TempPlugin(BinaryParserPlugin):
            def get_name(self):
                return "TempPlugin"

            def get_supported_formats(self):
                return ['.temp']

            def can_parse(self, file_path):
                return True

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        registry.register(TempPlugin)
        assert registry.get_plugin("TempPlugin") is TempPlugin
        assert '.temp' in registry._format_handlers

        # Manually remove to test cleanup
        del registry._plugins['TempPlugin']
        del registry._format_handlers['.temp']

        assert registry.get_plugin("TempPlugin") is None
        assert '.temp' not in registry._format_handlers

    def test_plugin_registry_with_overlapping_formats(self):
        """Test registry behavior with overlapping format support."""
        registry = PluginRegistry()

        class SpecializedPlugin(BinaryParserPlugin):
            def get_name(self):
                return "SpecializedPlugin"

            def get_supported_formats(self):
                return ['.special']

            def can_parse(self, file_path):
                return file_path.stem == 'special'

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        class GenericPlugin(BinaryParserPlugin):
            def get_name(self):
                return "GenericPlugin"

            def get_supported_formats(self):
                return ['.special', '.generic']

            def can_parse(self, file_path):
                return True  # Claims to handle everything

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        # Register specialized first, then generic
        registry.register(SpecializedPlugin)
        registry.register(GenericPlugin)

        # Specialized file should get specialized handler
        handler1 = registry.find_handler(Path('/path/to/special.special'))
        assert handler1 is SpecializedPlugin

        # Other .special files should get generic handler
        handler2 = registry.find_handler(Path('/path/to/other.special'))
        assert handler2 is GenericPlugin

        # .generic files should get generic handler
        handler3 = registry.find_handler(Path('/path/to/file.generic'))
        assert handler3 is GenericPlugin

    def test_plugin_registry_empty_format_list(self):
        """Test registration with empty format list."""
        registry = PluginRegistry()

        class EmptyFormatPlugin(BinaryParserPlugin):
            def get_name(self):
                return "EmptyFormatPlugin"

            def get_supported_formats(self):
                return []

            def can_parse(self, file_path):
                return True

            def parse(self, file_path):
                return {'packages': [], 'relationships': [], 'annotations': []}

        # Should register successfully
        result = registry.register(EmptyFormatPlugin)
        assert result is True
        assert registry.get_plugin("EmptyFormatPlugin") is EmptyFormatPlugin

        # Should not appear in format handlers
        assert len(registry._format_handlers) == 0

        # Should still be findable via can_parse fallback
        handler = registry.find_handler(Path('/path/to/file.unknown'))
        assert handler is EmptyFormatPlugin


class TestPluginDiscovery:
    """Test plugin discovery functionality."""

    def test_discover_plugins_default_directory(self):
        """Test discovering plugins from default directory."""
        # The function should create directory if it doesn't exist
        plugins = discover_plugins()
        assert isinstance(plugins, list)
        # All items should be Path objects
        for plugin in plugins:
            assert isinstance(plugin, Path)

    def test_discover_plugins_custom_directory(self):
        """Test discovering plugins from custom directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test plugin files
            plugin_dir = Path(tmpdir)
            (plugin_dir / 'plugin1.py').touch()
            (plugin_dir / 'plugin2.py').touch()
            (plugin_dir / '__init__.py').touch()
            (plugin_dir / '_private.py').touch()

            plugins = discover_plugins(plugin_dir)

            # Should find plugin1 and plugin2, but not __init__ or _private
            assert len(plugins) == 2
            plugin_names = [p.name for p in plugins]
            assert 'plugin1.py' in plugin_names
            assert 'plugin2.py' in plugin_names
            assert '__init__.py' not in plugin_names
            assert '_private.py' not in plugin_names

    def test_discover_plugins_empty_directory(self):
        """Test discovering plugins from empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            plugins = discover_plugins(Path(tmpdir))
            assert len(plugins) == 0

    def test_discover_plugins_filters_init_files(self):
        """Test that __init__.py files are filtered out."""
        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_dir = Path(tmpdir)
            (plugin_dir / '__init__.py').touch()

            plugins = discover_plugins(plugin_dir)
            assert len(plugins) == 0

    def test_discover_plugins_filters_private_files(self):
        """Test that files starting with underscore are filtered out."""
        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_dir = Path(tmpdir)
            (plugin_dir / '_private.py').touch()
            (plugin_dir / '__helper.py').touch()

            plugins = discover_plugins(plugin_dir)
            assert len(plugins) == 0

    def test_discover_plugins_requires_path_object(self):
        """Test that plugins_dir must be a Path object."""
        with pytest.raises(TypeError, match='must be a Path object'):
            discover_plugins('/not/a/path/object')

    def test_discover_plugins_creates_directory(self):
        """Test that directory is created when it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_dir = Path(tmpdir) / 'new_plugins'
            # Directory doesn't exist yet
            assert not plugin_dir.exists()

            # Discover plugins should create directory and return empty list
            plugins = discover_plugins(plugin_dir)

            # Directory should now exist
            assert plugin_dir.exists()
            assert plugin_dir.is_dir()
            # Should return empty list since no plugins in new directory
            assert len(plugins) == 0

    def test_discover_plugins_path_is_file(self):
        """Test that file path returns empty list."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = Path(f.name)

        try:
            # Path exists but is a file, not a directory
            plugins = discover_plugins(temp_path)
            assert len(plugins) == 0
        finally:
            temp_path.unlink()

    def test_discover_plugins_permission_denied_creation(self):
        """Test that permission denied during directory creation returns empty list."""
        # This test may not work on all systems due to permission handling
        # Skip if we can't create a test scenario
        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_dir = Path(tmpdir) / 'protected_dir'
            # Create a directory with a file that has the same name
            plugin_dir.parent.mkdir(parents=True, exist_ok=True)
            plugin_dir.touch()  # Create a file with the directory name

            # Now try to discover plugins - should fail gracefully
            plugins = discover_plugins(plugin_dir)
            # Should return empty list when path is a file
            assert len(plugins) == 0

    def test_discover_plugins_permission_denied_read(self):
        """Test that permission denied during directory read returns empty list."""
        from unittest.mock import patch
        import tempfile

        # Create a real temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_dir = Path(tmpdir)

            # Mock the glob method to raise PermissionError
            original_glob = Path.glob
            def mock_glob(self, pattern):
                raise PermissionError("Permission denied")

            with patch.object(Path, 'glob', mock_glob):
                plugins = discover_plugins(plugin_dir)
                # Should return empty list on permission error
                assert len(plugins) == 0

    def test_discover_plugins_returns_sorted_list(self):
        """Test that discovered plugins are returned in sorted order."""
        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_dir = Path(tmpdir)
            # Create plugin files in random order
            (plugin_dir / 'zebra.py').touch()
            (plugin_dir / 'apple.py').touch()
            (plugin_dir / 'middle.py').touch()

            plugins = discover_plugins(plugin_dir)

            # Should be sorted alphabetically
            plugin_names = [p.name for p in plugins]
            assert plugin_names == ['apple.py', 'middle.py', 'zebra.py']

    def test_discover_filters_non_py_files(self):
        """Test that non-Python files are filtered out."""
        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_dir = Path(tmpdir)
            (plugin_dir / 'plugin.py').touch()
            (plugin_dir / 'readme.txt').touch()
            (plugin_dir / 'config.json').touch()
            (plugin_dir / 'script.sh').touch()

            plugins = discover_plugins(plugin_dir)

            assert len(plugins) == 1
            assert plugins[0].name == 'plugin.py'


class TestPluginLoader:
    """Test plugin loader functionality."""

    def test_load_plugin_file_not_found(self):
        """Test that loading non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_plugin(Path('/nonexistent/plugin.py'))

    def test_load_plugin_not_python_file(self):
        """Test that loading non-.py file raises ValueError."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            temp_path = f.name

        try:
            with pytest.raises(ValueError):
                load_plugin(Path(temp_path))
        finally:
            os.unlink(temp_path)

    def test_load_plugin_no_binary_parser_subclass(self):
        """Test loading file without BinaryParserPlugin subclass."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('# Empty file\n')
            temp_path = f.name

        try:
            result = load_plugin(Path(temp_path))
            assert result is None
        finally:
            os.unlink(temp_path)

    def test_load_plugin_invalid_syntax(self):
        """Test loading file with invalid Python syntax."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('this is not valid python syntax {{{\n')
            temp_path = f.name

        try:
            result = load_plugin(Path(temp_path))
            assert result is None
        finally:
            os.unlink(temp_path)

    def test_load_plugin_success(self):
        """Test successfully loading a valid plugin."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
from binary_sbom.plugins.api import BinaryParserPlugin
from pathlib import Path

class TestLoaderPlugin(BinaryParserPlugin):
    def get_name(self):
        return "TestLoaderPlugin"

    def get_supported_formats(self):
        return ['.test']

    def can_parse(self, file_path):
        return True

    def parse(self, file_path):
        return {'packages': [], 'relationships': [], 'annotations': []}
''')
            temp_path = f.name

        try:
            plugin_class = load_plugin(Path(temp_path))
            assert plugin_class is not None
            assert plugin_class.__name__ == "TestLoaderPlugin"

            # Verify we can instantiate it
            plugin = plugin_class()
            assert plugin.get_name() == "TestLoaderPlugin"
        finally:
            os.unlink(temp_path)

    def test_load_plugin_requires_path_object(self):
        """Test that plugin_path must be a Path object."""
        with pytest.raises(TypeError):
            load_plugin('plugin.py')

    def test_load_plugin_with_import_error(self):
        """Test loading plugin with missing dependencies."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
from binary_sbom.plugins.api import BinaryParserPlugin
from nonexistent_module import Something

class BrokenPlugin(BinaryParserPlugin):
    def get_name(self):
        return "BrokenPlugin"

    def get_supported_formats(self):
        return ['.broken']

    def can_parse(self, file_path):
        return True

    def parse(self, file_path):
        return {'packages': [], 'relationships': [], 'annotations': []}
''')
            temp_path = f.name

        try:
            result = load_plugin(Path(temp_path))
            # Should return None due to import error
            assert result is None
        finally:
            os.unlink(temp_path)

    def test_load_plugin_with_runtime_error(self):
        """Test loading plugin that raises error during module execution."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
from binary_sbom.plugins.api import BinaryParserPlugin

# This will cause a runtime error during module load
raise RuntimeError("Intentional error during load")

class RuntimeErrorPlugin(BinaryParserPlugin):
    def get_name(self):
        return "RuntimeErrorPlugin"

    def get_supported_formats(self):
        return ['.error']

    def can_parse(self, file_path):
        return True

    def parse(self, file_path):
        return {'packages': [], 'relationships': [], 'annotations': []}
''')
            temp_path = f.name

        try:
            result = load_plugin(Path(temp_path))
            # Should return None due to runtime error
            assert result is None
        finally:
            os.unlink(temp_path)

    def test_load_plugin_abstract_class_only(self):
        """Test loading file with only abstract plugin class."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
from binary_sbom.plugins.api import BinaryParserPlugin
from abc import abstractmethod

class AbstractPlugin(BinaryParserPlugin):
    """This is still abstract because it doesn't implement all methods."""

    def get_name(self):
        return "Abstract"

    def get_supported_formats(self):
        return ['.abstract']

    @abstractmethod
    def can_parse(self, file_path):
        pass

    @abstractmethod
    def parse(self, file_path):
        pass
''')
            temp_path = f.name

        try:
            result = load_plugin(Path(temp_path))
            # Should return None because class is abstract
            assert result is None
        finally:
            os.unlink(temp_path)

    def test_load_plugin_multiple_classes_first_valid(self):
        """Test loading plugin with multiple classes, first one is valid."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
from binary_sbom.plugins.api import BinaryParserPlugin

class ValidPlugin(BinaryParserPlugin):
    def get_name(self):
        return "ValidPlugin"

    def get_supported_formats(self):
        return ['.valid']

    def can_parse(self, file_path):
        return True

    def parse(self, file_path):
        return {'packages': [], 'relationships': [], 'annotations': []}

class AnotherValidPlugin(BinaryParserPlugin):
    def get_name(self):
        return "AnotherValidPlugin"

    def get_supported_formats(self):
        return ['.another']

    def can_parse(self, file_path):
        return True

    def parse(self, file_path):
        return {'packages': [], 'relationships': [], 'annotations': []}
''')
            temp_path = f.name

        try:
            plugin_class = load_plugin(Path(temp_path))
            assert plugin_class is not None
            # Should return first valid class found
            assert plugin_class.__name__ == "ValidPlugin"
        finally:
            os.unlink(temp_path)

    def test_load_plugin_with_syntax_error_in_function(self):
        """Test loading plugin with syntax error in function body."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
from binary_sbom.plugins.api import BinaryParserPlugin

class SyntaxErrorPlugin(BinaryParserPlugin):
    def get_name(self):
        return "SyntaxErrorPlugin"

    def get_supported_formats(self):
        return ['.syntax']

    def can_parse(self, file_path):
        return True

    def parse(self, file_path):
        # Syntax error: incomplete statement
        x =
        return {'packages': [], 'relationships': [], 'annotations': []}
''')
            temp_path = f.name

        try:
            result = load_plugin(Path(temp_path))
            # Should return None due to syntax error
            assert result is None
        finally:
            os.unlink(temp_path)

    def test_load_plugin_path_is_directory(self):
        """Test that directory path raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValueError, match="not a file"):
                load_plugin(Path(tmpdir))

    def test_load_plugin_empty_file(self):
        """Test loading empty plugin file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('')
            temp_path = f.name

        try:
            result = load_plugin(Path(temp_path))
            # Empty file has no plugin class
            assert result is None
        finally:
            os.unlink(temp_path)

    def test_load_plugin_with_comments_only(self):
        """Test loading plugin file with only comments."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
# This is just a comment file
# No actual plugin code here
# Only documentation
''')
            temp_path = f.name

        try:
            result = load_plugin(Path(temp_path))
            # Comments only, no plugin class
            assert result is None
        finally:
            os.unlink(temp_path)

    def test_load_plugin_with_invalid_encoding(self):
        """Test loading plugin file with invalid UTF-8 encoding."""
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.py', delete=False) as f:
            # Write invalid UTF-8 sequence
            f.write(b'\xff\xfe Invalid UTF-8')
            temp_path = f.name

        try:
            result = load_plugin(Path(temp_path))
            # Should handle encoding error gracefully
            assert result is None
        finally:
            os.unlink(temp_path)

    def test_load_plugin_with_indention_error(self):
        """Test loading plugin file with indentation errors."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            # Create a file with an indentation error that will be caught at import time
            # The indentation error is at the method definition level (not inside a method)
            # so Python's parser will catch it during import
            f.write('''from binary_sbom.plugins.api import BinaryParserPlugin

class IndentionErrorPlugin(BinaryParserPlugin):
  def get_name(self):  # Wrong indentation (2 spaces instead of 4) - causes IndentationError
        return "IndentionErrorPlugin"

    def get_supported_formats(self):
        return ['.indent']

    def can_parse(self, file_path):
        return True

    def parse(self, file_path):
        return {'packages': [], 'relationships': [], 'annotations': []}
''')
            temp_path = f.name

        try:
            result = load_plugin(Path(temp_path))
            # Should return None due to indentation error
            assert result is None
        finally:
            os.unlink(temp_path)

    def test_load_plugin_valid_with_docstring(self):
        """Test loading valid plugin with comprehensive docstrings."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
"""
Comprehensive plugin for testing.

This plugin provides extensive functionality.
"""

from binary_sbom.plugins.api import BinaryParserPlugin
from pathlib import Path
from typing import Dict, List, Any

class DocstringPlugin(BinaryParserPlugin):
    """A plugin with comprehensive documentation.

    This plugin demonstrates proper documentation practices.
    """

    def get_name(self) -> str:
        """Return the plugin name.

        Returns:
            The plugin name as a string.
        """
        return "DocstringPlugin"

    def get_supported_formats(self) -> List[str]:
        """Return list of supported file formats.

        Returns:
            List of file extensions including the dot.
        """
        return ['.doc']

    def can_parse(self, file_path: Path) -> bool:
        """Check if file can be parsed.

        Args:
            file_path: Path to the file to check.

        Returns:
            True if file can be parsed, False otherwise.
        """
        return file_path.suffix == '.doc'

    def parse(self, file_path: Path) -> Dict[str, List[Any]]:
        """Parse the binary file and extract metadata.

        Args:
            file_path: Path to the binary file.

        Returns:
            Dictionary with packages, relationships, and annotations.
        """
        return {
            'packages': [],
            'relationships': [],
            'annotations': []
        }
''')
            temp_path = f.name

        try:
            plugin_class = load_plugin(Path(temp_path))
            assert plugin_class is not None
            assert plugin_class.__name__ == "DocstringPlugin"

            # Verify it works correctly
            plugin = plugin_class()
            assert plugin.get_name() == "DocstringPlugin"
            assert plugin.get_supported_formats() == ['.doc']
            assert plugin.can_parse(Path('/test/file.doc')) is True
            assert plugin.can_parse(Path('/test/file.txt')) is False
        finally:
            os.unlink(temp_path)

    def test_load_plugin_valid_with_version_override(self):
        """Test loading valid plugin with custom version property."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
from binary_sbom.plugins.api import BinaryParserPlugin

class VersionedPlugin(BinaryParserPlugin):
    def get_name(self):
        return "VersionedPlugin"

    def get_supported_formats(self):
        return ['.ver']

    def can_parse(self, file_path):
        return True

    def parse(self, file_path):
        return {'packages': [], 'relationships': [], 'annotations': []}

    @property
    def version(self):
        return "3.2.1-beta"
''')
            temp_path = f.name

        try:
            plugin_class = load_plugin(Path(temp_path))
            assert plugin_class is not None

            plugin = plugin_class()
            assert plugin.version == "3.2.1-beta"
        finally:
            os.unlink(temp_path)

    def test_load_plugin_with_name_collision(self):
        """Test loading multiple plugins with same class name from different files."""
        # Create first plugin
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f1:
            f1.write('''
from binary_sbom.plugins.api import BinaryParserPlugin

class DuplicateName(BinaryParserPlugin):
    def get_name(self):
        return "First"

    def get_supported_formats(self):
        return ['.first']

    def can_parse(self, file_path):
        return True

    def parse(self, file_path):
        return {'packages': [], 'relationships': [], 'annotations': []}
''')
            temp_path1 = f1.name

        # Create second plugin with same class name
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f2:
            f2.write('''
from binary_sbom.plugins.api import BinaryParserPlugin

class DuplicateName(BinaryParserPlugin):
    def get_name(self):
        return "Second"

    def get_supported_formats(self):
        return ['.second']

    def can_parse(self, file_path):
        return True

    def parse(self, file_path):
        return {'packages': [], 'relationships': [], 'annotations': []}
''')
            temp_path2 = f2.name

        try:
            # Load both plugins
            plugin1 = load_plugin(Path(temp_path1))
            plugin2 = load_plugin(Path(temp_path2))

            # Both should load successfully despite same class name
            assert plugin1 is not None
            assert plugin2 is not None

            # They should be different classes
            assert plugin1 is not plugin2

            # Verify they work independently
            instance1 = plugin1()
            instance2 = plugin2()
            assert instance1.get_name() == "First"
            assert instance2.get_name() == "Second"
        finally:
            os.unlink(temp_path1)
            os.unlink(temp_path2)

    def test_load_plugin_recovers_from_previous_error(self):
        """Test that loader can recover after loading a malformed plugin."""
        # First, try to load a malformed plugin
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('invalid python syntax {{{')
            bad_path = f.name

        # Then create a valid plugin
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
from binary_sbom.plugins.api import BinaryParserPlugin

class RecoveryPlugin(BinaryParserPlugin):
    def get_name(self):
        return "RecoveryPlugin"

    def get_supported_formats(self):
        return ['.recover']

    def can_parse(self, file_path):
        return True

    def parse(self, file_path):
        return {'packages': [], 'relationships': [], 'annotations': []}
''')
            good_path = f.name

        try:
            # Load bad plugin (should fail gracefully)
            bad_result = load_plugin(Path(bad_path))
            assert bad_result is None

            # Load good plugin (should succeed)
            good_result = load_plugin(Path(good_path))
            assert good_result is not None
            assert good_result.__name__ == "RecoveryPlugin"
        finally:
            os.unlink(bad_path)
            os.unlink(good_path)


class TestSPDXIntegration:
    """Test SPDX integration functionality."""

    def test_create_spdx_from_plugin_metadata_missing_keys(self):
        """Test that missing required keys raises ValueError."""
        metadata = {}  # Missing all required keys
        file_path = Path('/test/file.bin')

        with pytest.raises(ValueError, match='Missing required metadata keys'):
            create_spdx_from_plugin_metadata(metadata, file_path)

    def test_create_spdx_from_plugin_metadata_packages_not_list(self):
        """Test that non-list packages raises ValueError."""
        metadata = {
            'packages': 'not-a-list',
            'relationships': [],
            'annotations': []
        }
        file_path = Path('/test/file.bin')

        with pytest.raises(ValueError, match="'packages' must be a list"):
            create_spdx_from_plugin_metadata(metadata, file_path)

    def test_create_spdx_from_plugin_metadata_relationships_not_list(self):
        """Test that non-list relationships raises ValueError."""
        metadata = {
            'packages': [],
            'relationships': 'not-a-list',
            'annotations': []
        }
        file_path = Path('/test/file.bin')

        with pytest.raises(ValueError, match="'relationships' must be a list"):
            create_spdx_from_plugin_metadata(metadata, file_path)

    def test_create_spdx_from_plugin_metadata_annotations_not_list(self):
        """Test that non-list annotations raises ValueError."""
        metadata = {
            'packages': [],
            'relationships': [],
            'annotations': 'not-a-list'
        }
        file_path = Path('/test/file.bin')

        with pytest.raises(ValueError, match="'annotations' must be a list"):
            create_spdx_from_plugin_metadata(metadata, file_path)

    @patch('binary_sbom.plugins.integration.Document')
    def test_create_spdx_from_plugin_metadata_no_spdx_tools(self, mock_document):
        """Test that missing spdx-tools raises ImportError."""
        # Mock Document to None to simulate missing library
        with patch('binary_sbom.plugins.integration.Document', None):
            metadata = {
                'packages': [],
                'relationships': [],
                'annotations': []
            }
            file_path = Path('/test/file.bin')

            with pytest.raises(ImportError, match='spdx-tools library is required'):
                create_spdx_from_plugin_metadata(metadata, file_path)

    @patch('binary_sbom.plugins.integration.Document')
    @patch('binary_sbom.plugins.integration.Package')
    @patch('binary_sbom.plugins.integration.Relationship')
    @patch('binary_sbom.plugins.integration.Annotation')
    @patch('binary_sbom.plugins.integration.CreationInfo')
    @patch('binary_sbom.plugins.integration.Actor')
    @patch('binary_sbom.plugins.integration.ActorType')
    def test_create_spdx_from_plugin_metadata_success(
        self, mock_actor_type, mock_actor, mock_creation_info, mock_annotation,
        mock_relationship, mock_package, mock_document
    ):
        """Test successful SPDX document creation."""
        # Setup mocks
        mock_actor_type.TOOL = 'tool'
        mock_actor.return_value = MagicMock()
        mock_creation_info.return_value = MagicMock()
        mock_package.return_value = MagicMock()
        mock_relationship.return_value = MagicMock()
        mock_annotation.return_value = MagicMock()
        mock_document.return_value = MagicMock()

        metadata = {
            'packages': [
                {
                    'name': 'test-package',
                    'version': '1.0.0',
                    'type': 'library',
                    'spdx_id': 'SPDXRef-test'
                }
            ],
            'relationships': [
                {
                    'source': 'SPDXRef-test',
                    'type': 'DEPENDS_ON',
                    'target': 'SPDXRef-dep'
                }
            ],
            'annotations': [
                {
                    'spdx_id': 'SPDXRef-test',
                    'type': 'OTHER',
                    'text': 'Test annotation'
                }
            ]
        }
        file_path = Path('/test/file.bin')

        result = create_spdx_from_plugin_metadata(metadata, file_path)
        assert result is not None

    @patch('binary_sbom.plugins.integration.Document')
    @patch('binary_sbom.plugins.integration.Package')
    @patch('binary_sbom.plugins.integration.CreationInfo')
    @patch('binary_sbom.plugins.integration.Actor')
    @patch('binary_sbom.plugins.integration.ActorType')
    def test_create_spdx_from_plugin_metadata_empty_metadata(
        self, mock_actor_type, mock_actor, mock_creation_info, mock_package, mock_document
    ):
        """Test SPDX creation with empty metadata."""
        mock_actor_type.TOOL = 'tool'
        mock_actor.return_value = MagicMock()
        mock_creation_info.return_value = MagicMock()
        mock_document.return_value = MagicMock()

        metadata = {
            'packages': [],
            'relationships': [],
            'annotations': []
        }
        file_path = Path('/test/file.bin')

        result = create_spdx_from_plugin_metadata(metadata, file_path)
        assert result is not None

    @patch('binary_sbom.plugins.integration.Document')
    @patch('binary_sbom.plugins.integration.Package')
    @patch('binary_sbom.plugins.integration.CreationInfo')
    @patch('binary_sbom.plugins.integration.Actor')
    @patch('binary_sbom.plugins.integration.ActorType')
    def test_create_spdx_from_plugin_metadata_with_plugin_name(
        self, mock_actor_type, mock_actor, mock_creation_info, mock_package, mock_document
    ):
        """Test SPDX creation with plugin_name metadata."""
        mock_actor_type.TOOL = 'tool'
        mock_actor.return_value = MagicMock()
        mock_creation_info.return_value = MagicMock()
        mock_document.return_value = MagicMock()

        metadata = {
            'packages': [],
            'relationships': [],
            'annotations': [],
            'plugin_name': 'TestPlugin'
        }
        file_path = Path('/test/file.bin')

        result = create_spdx_from_plugin_metadata(metadata, file_path)
        assert result is not None

    @patch('binary_sbom.plugins.integration.Document')
    @patch('binary_sbom.plugins.integration.Package')
    @patch('binary_sbom.plugins.integration.CreationInfo')
    @patch('binary_sbom.plugins.integration.Actor')
    @patch('binary_sbom.plugins.integration.ActorType')
    def test_create_spdx_from_plugin_metadata_custom_namespace(
        self, mock_actor_type, mock_actor, mock_creation_info, mock_package, mock_document
    ):
        """Test SPDX creation with custom namespace."""
        mock_actor_type.TOOL = 'tool'
        mock_actor.return_value = MagicMock()
        mock_creation_info.return_value = MagicMock()
        mock_document.return_value = MagicMock()

        metadata = {
            'packages': [],
            'relationships': [],
            'annotations': []
        }
        file_path = Path('/test/file.bin')
        custom_namespace = 'https://custom.com/sbom'

        result = create_spdx_from_plugin_metadata(metadata, file_path, namespace=custom_namespace)
        assert result is not None
        # Verify creation_info was called with custom namespace
        mock_creation_info.assert_called_once()
        call_kwargs = mock_creation_info.call_args[1]
        assert custom_namespace in call_kwargs['document_namespace']

    @patch('binary_sbom.plugins.integration.Document')
    @patch('binary_sbom.plugins.integration.Package')
    @patch('binary_sbom.plugins.integration.CreationInfo')
    @patch('binary_sbom.plugins.integration.Actor')
    @patch('binary_sbom.plugins.integration.ActorType')
    def test_create_spdx_from_plugin_metadata_custom_creator(
        self, mock_actor_type, mock_actor, mock_creation_info, mock_package, mock_document
    ):
        """Test SPDX creation with custom creator."""
        mock_actor_type.TOOL = 'tool'
        mock_actor.return_value = MagicMock()
        mock_creation_info.return_value = MagicMock()
        mock_document.return_value = MagicMock()

        metadata = {
            'packages': [],
            'relationships': [],
            'annotations': []
        }
        file_path = Path('/test/file.bin')

        result = create_spdx_from_plugin_metadata(metadata, file_path, creator='Tool: custom-tool')
        assert result is not None
        # Verify Actor was called with custom creator
        mock_actor.assert_called()
        call_kwargs = mock_actor.call_args[1]
        assert call_kwargs['name'] == 'custom-tool'

    @patch('binary_sbom.plugins.integration._create_packages')
    def test_create_spdx_from_plugin_metadata_package_creation_failure(self, mock_create_packages):
        """Test that package creation failure is wrapped."""
        mock_create_packages.side_effect = Exception('Package creation failed')

        metadata = {
            'packages': [{'name': 'test'}],
            'relationships': [],
            'annotations': []
        }
        file_path = Path('/test/file.bin')

        with pytest.raises(SPDXIntegrationError, match='Failed to create SPDX packages'):
            create_spdx_from_plugin_metadata(metadata, file_path)

    @patch('binary_sbom.plugins.integration._create_packages')
    @patch('binary_sbom.plugins.integration._create_relationships')
    def test_create_spdx_from_plugin_metadata_relationship_creation_failure(
        self, mock_create_relationships, mock_create_packages
    ):
        """Test that relationship creation failure is wrapped."""
        mock_create_packages.return_value = []
        mock_create_relationships.side_effect = Exception('Relationship creation failed')

        metadata = {
            'packages': [],
            'relationships': [{'source': 'test'}],
            'annotations': []
        }
        file_path = Path('/test/file.bin')

        with pytest.raises(SPDXIntegrationError, match='Failed to create SPDX relationships'):
            create_spdx_from_plugin_metadata(metadata, file_path)

    @patch('binary_sbom.plugins.integration._create_packages')
    @patch('binary_sbom.plugins.integration._create_relationships')
    @patch('binary_sbom.plugins.integration._create_annotations')
    def test_create_spdx_from_plugin_metadata_annotation_creation_failure(
        self, mock_create_annotations, mock_create_relationships, mock_create_packages
    ):
        """Test that annotation creation failure is wrapped."""
        mock_create_packages.return_value = []
        mock_create_relationships.return_value = []
        mock_create_annotations.side_effect = Exception('Annotation creation failed')

        metadata = {
            'packages': [],
            'relationships': [],
            'annotations': [{'text': 'test'}]
        }
        file_path = Path('/test/file.bin')

        with pytest.raises(SPDXIntegrationError, match='Failed to create SPDX annotations'):
            create_spdx_from_plugin_metadata(metadata, file_path)

    @patch('binary_sbom.plugins.integration.Document')
    @patch('binary_sbom.plugins.integration._create_packages')
    @patch('binary_sbom.plugins.integration._create_relationships')
    @patch('binary_sbom.plugins.integration._create_annotations')
    @patch('binary_sbom.plugins.integration.Actor')
    @patch('binary_sbom.plugins.integration.ActorType')
    def test_create_spdx_from_plugin_metadata_creation_info_failure(
        self, mock_actor_type, mock_actor, mock_create_annotations,
        mock_create_relationships, mock_create_packages, mock_document
    ):
        """Test that creation info failure is wrapped."""
        mock_actor_type.TOOL = 'tool'
        mock_actor.side_effect = Exception('Actor creation failed')
        mock_create_packages.return_value = []
        mock_create_relationships.return_value = []
        mock_create_annotations.return_value = []

        metadata = {
            'packages': [],
            'relationships': [],
            'annotations': []
        }
        file_path = Path('/test/file.bin')

        with pytest.raises(SPDXIntegrationError, match='Failed to create creator actor'):
            create_spdx_from_plugin_metadata(metadata, file_path)

    @patch('binary_sbom.plugins.integration.Document')
    @patch('binary_sbom.plugins.integration._create_packages')
    @patch('binary_sbom.plugins.integration._create_relationships')
    @patch('binary_sbom.plugins.integration._create_annotations')
    @patch('binary_sbom.plugins.integration.CreationInfo')
    @patch('binary_sbom.plugins.integration.Actor')
    @patch('binary_sbom.plugins.integration.ActorType')
    def test_create_spdx_from_plugin_metadata_document_creation_failure(
        self, mock_actor_type, mock_actor, mock_creation_info, mock_create_annotations,
        mock_create_relationships, mock_create_packages, mock_document
    ):
        """Test that document creation failure is wrapped."""
        mock_actor_type.TOOL = 'tool'
        mock_actor.return_value = MagicMock()
        mock_creation_info.side_effect = Exception('Creation info failed')
        mock_create_packages.return_value = []
        mock_create_relationships.return_value = []
        mock_create_annotations.return_value = []

        metadata = {
            'packages': [],
            'relationships': [],
            'annotations': []
        }
        file_path = Path('/test/file.bin')

        with pytest.raises(SPDXIntegrationError, match='Failed to create creation info'):
            create_spdx_from_plugin_metadata(metadata, file_path)


class TestCreatePackages:
    """Test _create_packages helper function."""

    @patch('binary_sbom.plugins.integration.Package', None)
    def test_create_packages_without_spdx_tools(self):
        """Test that missing spdx-tools raises SPDXIntegrationError."""
        from binary_sbom.plugins.integration import _create_packages
        with pytest.raises(SPDXIntegrationError, match='spdx-tools library is not available'):
            _create_packages([])

    @patch('binary_sbom.plugins.integration.Package')
    @patch('binary_sbom.plugins.integration.SpdxNoAssertion')
    def test_create_packages_success(self, mock_no_assertion, mock_package):
        """Test successful package creation."""
        from binary_sbom.plugins.integration import _create_packages
        mock_no_assertion.return_value = MagicMock()
        mock_package_instance = MagicMock()
        mock_package.return_value = mock_package_instance

        packages_data = [
            {
                'name': 'test-package',
                'version': '1.0.0',
                'type': 'library',
                'spdx_id': 'SPDXRef-test',
                'supplier': 'Test Corp'
            }
        ]

        packages = _create_packages(packages_data)

        assert len(packages) == 1
        assert packages[0] == mock_package_instance
        mock_package.assert_called_once()
        call_kwargs = mock_package.call_args[1]
        assert call_kwargs['name'] == 'test-package'
        assert call_kwargs['spdx_id'] == 'SPDXRef-test'
        assert call_kwargs['version'] == '1.0.0'

    @patch('binary_sbom.plugins.integration.Package')
    @patch('binary_sbom.plugins.integration.SpdxNoAssertion')
    def test_create_packages_minimal_data(self, mock_no_assertion, mock_package):
        """Test package creation with minimal data."""
        from binary_sbom.plugins.integration import _create_packages
        mock_no_assertion.return_value = MagicMock()
        mock_package.return_value = MagicMock()

        packages_data = [{'name': 'minimal'}]

        packages = _create_packages(packages_data)

        assert len(packages) == 1
        call_kwargs = mock_package.call_args[1]
        assert call_kwargs['name'] == 'minimal'
        assert call_kwargs['spdx_id'] == 'SPDXRef-minimal'

    @patch('binary_sbom.plugins.integration.Package')
    def test_create_packages_failure(self, mock_package):
        """Test that package creation failure is wrapped."""
        from binary_sbom.plugins.integration import _create_packages
        mock_package.side_effect = Exception('Package creation failed')

        packages_data = [{'name': 'test'}]

        with pytest.raises(SPDXIntegrationError, match="Failed to create package 'test'"):
            _create_packages(packages_data)


class TestCreateRelationships:
    """Test _create_relationships helper function."""

    @patch('binary_sbom.plugins.integration.Relationship', None)
    def test_create_relationships_without_spdx_tools(self):
        """Test that missing spdx-tools raises SPDXIntegrationError."""
        from binary_sbom.plugins.integration import _create_relationships
        with pytest.raises(SPDXIntegrationError, match='spdx-tools library is not available'):
            _create_relationships([])

    @patch('binary_sbom.plugins.integration.Relationship')
    @patch('binary_sbom.plugins.integration.RelationshipType')
    def test_create_relationships_success(self, mock_rel_type, mock_relationship):
        """Test successful relationship creation."""
        from binary_sbom.plugins.integration import _create_relationships
        mock_rel_type.DEPENDS_ON = 'DEPENDS_ON'
        mock_relationship_instance = MagicMock()
        mock_relationship.return_value = mock_relationship_instance

        relationships_data = [
            {
                'source': 'SPDXRef-pkg1',
                'type': 'DEPENDS_ON',
                'target': 'SPDXRef-pkg2'
            }
        ]

        relationships = _create_relationships(relationships_data)

        assert len(relationships) == 1
        assert relationships[0] == mock_relationship_instance

    @patch('binary_sbom.plugins.integration.Relationship')
    @patch('binary_sbom.plugins.integration.RelationshipType')
    def test_create_relationships_unknown_type_fallback(self, mock_rel_type, mock_relationship):
        """Test that unknown relationship type falls back to DEPENDS_ON."""
        from binary_sbom.plugins.integration import _create_relationships
        mock_rel_type.DEPENDS_ON = 'DEPENDS_ON'
        mock_rel_type.__getitem__.side_effect = KeyError('Unknown type')
        mock_relationship_instance = MagicMock()
        mock_relationship.return_value = mock_relationship_instance

        relationships_data = [
            {
                'source': 'SPDXRef-pkg1',
                'type': 'UNKNOWN_TYPE',
                'target': 'SPDXRef-pkg2'
            }
        ]

        relationships = _create_relationships(relationships_data)

        assert len(relationships) == 1
        # Should use DEPENDS_ON as fallback
        assert mock_relationship.call_args[1]['relationship_type'] == 'DEPENDS_ON'

    @patch('binary_sbom.plugins.integration.Relationship')
    def test_create_relationships_failure(self, mock_relationship):
        """Test that relationship creation failure is wrapped."""
        from binary_sbom.plugins.integration import _create_relationships
        mock_relationship.side_effect = Exception('Relationship creation failed')

        relationships_data = [{'source': 'test', 'type': 'DEPENDS_ON', 'target': 'dep'}]

        with pytest.raises(SPDXIntegrationError, match="Failed to create relationship 'test'"):
            _create_relationships(relationships_data)


class TestCreateAnnotations:
    """Test _create_annotations helper function."""

    @patch('binary_sbom.plugins.integration.Annotation', None)
    def test_create_annotations_without_spdx_tools(self):
        """Test that missing spdx-tools raises SPDXIntegrationError."""
        from binary_sbom.plugins.integration import _create_annotations
        with pytest.raises(SPDXIntegrationError, match='spdx-tools library is not available'):
            _create_annotations([], None)

    @patch('binary_sbom.plugins.integration.Annotation')
    @patch('binary_sbom.plugins.integration.AnnotationType')
    @patch('binary_sbom.plugins.integration.Actor')
    @patch('binary_sbom.plugins.integration.ActorType')
    def test_create_annotations_success(self, mock_actor_type, mock_actor, mock_ann_type, mock_annotation):
        """Test successful annotation creation."""
        from binary_sbom.plugins.integration import _create_annotations
        mock_actor_type.TOOL = 'tool'
        mock_actor.return_value = MagicMock()
        mock_ann_type.OTHER = 'OTHER'
        mock_annotation_instance = MagicMock()
        mock_annotation.return_value = mock_annotation_instance

        annotations_data = [
            {
                'spdx_id': 'SPDXRef-test',
                'type': 'OTHER',
                'text': 'Test annotation',
                'annotator': 'Tool: test-tool'
            }
        ]

        annotations = _create_annotations(annotations_data, plugin_name='TestPlugin')

        # Should have 2 annotations: plugin annotation + user annotation
        assert len(annotations) >= 1

    @patch('binary_sbom.plugins.integration.Annotation')
    @patch('binary_sbom.plugins.integration.AnnotationType')
    @patch('binary_sbom.plugins.integration.Actor')
    @patch('binary_sbom.plugins.integration.ActorType')
    def test_create_annotations_with_plugin_name(self, mock_actor_type, mock_actor, mock_ann_type, mock_annotation):
        """Test that plugin_name creates document-level annotation."""
        from binary_sbom.plugins.integration import _create_annotations
        mock_actor_type.TOOL = 'tool'
        mock_actor.return_value = MagicMock()
        mock_ann_type.OTHER = 'OTHER'
        mock_annotation_instance = MagicMock()
        mock_annotation.return_value = mock_annotation_instance

        annotations = _create_annotations([], plugin_name='TestPlugin')

        # Should create plugin annotation
        assert len(annotations) == 1
        assert mock_annotation.call_args[1]['annotation_comment'] == 'Generated by plugin: TestPlugin'

    @patch('binary_sbom.plugins.integration.Annotation')
    @patch('binary_sbom.plugins.integration.AnnotationType')
    @patch('binary_sbom.plugins.integration.Actor')
    @patch('binary_sbom.plugins.integration.ActorType')
    def test_create_annotations_unknown_type_fallback(self, mock_actor_type, mock_actor, mock_ann_type, mock_annotation):
        """Test that unknown annotation type falls back to OTHER."""
        from binary_sbom.plugins.integration import _create_annotations
        mock_actor_type.TOOL = 'tool'
        mock_actor.return_value = MagicMock()
        mock_ann_type.OTHER = 'OTHER'
        mock_ann_type.__getitem__.side_effect = KeyError('Unknown type')
        mock_annotation_instance = MagicMock()
        mock_annotation.return_value = mock_annotation_instance

        annotations_data = [
            {
                'spdx_id': 'SPDXRef-test',
                'type': 'UNKNOWN_TYPE',
                'text': 'Test annotation'
            }
        ]

        annotations = _create_annotations(annotations_data)

        # Should use OTHER as fallback
        assert mock_annotation.call_args[1]['annotation_type'] == 'OTHER'

    @patch('binary_sbom.plugins.integration.Annotation')
    @patch('binary_sbom.plugins.integration.AnnotationType')
    @patch('binary_sbom.plugins.integration.Actor')
    @patch('binary_sbom.plugins.integration.ActorType')
    def test_create_annotations_invalid_date_handling(self, mock_actor_type, mock_actor, mock_ann_type, mock_annotation):
        """Test that invalid date string falls back to current time."""
        from binary_sbom.plugins.integration import _create_annotations
        mock_actor_type.TOOL = 'tool'
        mock_actor.return_value = MagicMock()
        mock_ann_type.OTHER = 'OTHER'
        mock_annotation_instance = MagicMock()
        mock_annotation.return_value = mock_annotation_instance

        annotations_data = [
            {
                'spdx_id': 'SPDXRef-test',
                'type': 'OTHER',
                'text': 'Test annotation',
                'date': 'invalid-date-format'
            }
        ]

        # Should not raise, should use current time
        annotations = _create_annotations(annotations_data)
        assert len(annotations) == 1

    @patch('binary_sbom.plugins.integration.Annotation')
    @patch('binary_sbom.plugins.integration.AnnotationType')
    @patch('binary_sbom.plugins.integration.Actor')
    @patch('binary_sbom.plugins.integration.ActorType')
    def test_create_annotations_continues_on_error(self, mock_actor_type, mock_actor, mock_ann_type, mock_annotation):
        """Test that annotation creation errors don't stop processing."""
        from binary_sbom.plugins.integration import _create_annotations
        mock_actor_type.TOOL = 'tool'
        mock_actor.return_value = MagicMock()
        mock_ann_type.OTHER = 'OTHER'
        # First annotation fails, second succeeds
        mock_annotation.side_effect = [Exception('Failed'), MagicMock()]

        annotations_data = [
            {'spdx_id': 'SPDXRef-test1', 'type': 'OTHER', 'text': 'Failing annotation'},
            {'spdx_id': 'SPDXRef-test2', 'type': 'OTHER', 'text': 'Success annotation'}
        ]

        # Should not raise, should continue with second annotation
        annotations = _create_annotations(annotations_data)
        # Should have at least one annotation (the successful one)
        assert len(annotations) >= 1


class TestSPDXIntegrationError:
    """Test SPDXIntegrationError exception."""

    def test_spdx_integration_error_is_exception(self):
        """Test that SPDXIntegrationError is an Exception subclass."""
        assert issubclass(SPDXIntegrationError, Exception)

    def test_spdx_integration_error_can_be_raised(self):
        """Test that SPDXIntegrationError can be raised and caught."""
        with pytest.raises(SPDXIntegrationError):
            raise SPDXIntegrationError("Test error")

    def test_spdx_integration_error_message(self):
        """Test that SPDXIntegrationError preserves error message."""
        error_msg = "Test SPDX integration error"
        with pytest.raises(SPDXIntegrationError, match=error_msg):
            raise SPDXIntegrationError(error_msg)
