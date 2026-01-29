"""
Plugin system for Binary SBOM Generator.

This package provides a flexible plugin architecture that enables users to extend
binary parsing capabilities without modifying core code. Plugins are discovered from
~/.binary-sbom/plugins/, loaded at runtime, and integrated with the SPDX generator.

The plugin system architecture uses:
- Abstract base classes (ABC) for plugin interface definition
- pathlib for cross-platform plugin discovery
- importlib.util for dynamic plugin loading
- Global registry for handler management

Example:
    >>> from binary_sbom.plugins import BinaryParserPlugin, discover_plugins, registry
    >>> from pathlib import Path
    >>>
    >>> # Discover and load plugins
    >>> plugin_files = discover_plugins()
    >>> for plugin_path in plugin_files:
    ...     plugin_class = load_plugin(plugin_path)
    ...     if plugin_class:
    ...         registry.register(plugin_class)
    >>>
    >>> # Use plugin for parsing
    >>> plugin = registry.find_handler(Path('/path/to/binary.xfw'))
    >>> if plugin:
    ...     metadata = plugin().parse(Path('/path/to/binary.xfw'))
    ...     print(metadata['packages'])

    >>> # Creating a custom plugin
    >>> from binary_sbom.plugins import BinaryParserPlugin
    >>> class MyCustomParser(BinaryParserPlugin):
    ...     def get_name(self) -> str:
    ...         return "MyCustomParser"
    ...     def get_supported_formats(self) -> list[str]:
    ...         return ['.custom']
    ...     def can_parse(self, file_path: Path) -> bool:
    ...         return file_path.suffix == '.custom'
    ...     def parse(self, file_path: Path) -> dict:
    ...         return {'packages': [], 'relationships': [], 'annotations': []}
"""

from binary_sbom.plugins.api import BinaryParserPlugin
from binary_sbom.plugins.discovery import discover_plugins
from binary_sbom.plugins.integration import create_spdx_from_plugin_metadata
from binary_sbom.plugins.loader import load_plugin
from binary_sbom.plugins.registry import PluginRegistry, get_global_registry

# Global registry instance for convenient access
registry = get_global_registry()

__all__ = [
    "BinaryParserPlugin",
    "discover_plugins",
    "load_plugin",
    "PluginRegistry",
    "registry",
    "create_spdx_from_plugin_metadata",
]

__version__ = "0.1.0"
