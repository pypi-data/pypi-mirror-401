"""
Binary SBOM Generator

A CLI tool for analyzing binary files and generating SPDX SBOM documents.
Supports ELF, PE, MachO, and raw binary formats with output in multiple formats.

The tool includes a plugin system that enables users to extend binary parsing
capabilities without modifying core code. Plugins are discovered from
~/.binary-sbom/plugins/, loaded at runtime, and integrated with the SPDX generator.

Example:
    >>> from binary_sbom import BinaryParserPlugin, discover_plugins, load_plugin, registry
    >>> from pathlib import Path
    >>>
    >>> # Discover and load plugins
    >>> plugin_files = discover_plugins()
    >>> for plugin_path in plugin_files:
    ...     plugin_class = load_plugin(plugin_path)
    ...     if plugin_class:
    ...         registry.register(plugin_class)
    >>>
    >>> # Find and use a plugin for parsing
    >>> plugin = registry.find_handler(Path('/path/to/binary.xfw'))
    >>> if plugin:
    ...     metadata = plugin().parse(Path('/path/to/binary.xfw'))
    ...     print(metadata['packages'])

    >>> # Creating a custom plugin
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

from binary_sbom.plugins import (
    BinaryParserPlugin,
    discover_plugins,
    load_plugin,
    registry,
)

__version__ = "0.1.0"
__author__ = "Binary SBOM Generator Contributors"
__license__ = "MIT"

__all__ = [
    "__version__",
    "BinaryParserPlugin",
    "discover_plugins",
    "load_plugin",
    "registry",
]
