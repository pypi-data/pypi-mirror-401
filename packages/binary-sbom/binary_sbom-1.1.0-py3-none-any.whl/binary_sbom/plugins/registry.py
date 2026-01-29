"""
Plugin registry module for Binary SBOM Generator.

This module provides a centralized registry for managing loaded parser plugins,
tracking them by name and supported file formats, and enabling efficient
handler lookup for file parsing operations.
"""

import logging
import threading
from pathlib import Path
from typing import Dict, List, Optional, Type

from binary_sbom.plugins.api import BinaryParserPlugin


logger = logging.getLogger(__name__)


class PluginRegistry:
    """Registry for managing loaded parser plugins.

    The registry maintains a collection of loaded plugins, indexed by plugin name
    and supported file formats. This enables efficient lookup of appropriate
    parsers for specific file types.

    Attributes:
        _plugins: Dictionary mapping plugin names to plugin classes.
        _format_handlers: Dictionary mapping file extensions to lists of plugin names.

    Example:
        >>> registry = PluginRegistry()
        >>> registry.register(MyCustomParser)
        True
        >>> plugin = registry.get_plugin("MyCustomParser")
        >>> handler = registry.find_handler(Path("/path/to/file.xfw"))
    """

    def __init__(self) -> None:
        """Initialize an empty plugin registry.

        Creates empty dictionaries for tracking plugins by name and by
        supported file formats.
        """
        self._plugins: Dict[str, Type[BinaryParserPlugin]] = {}
        self._format_handlers: Dict[str, List[str]] = {}

    def register(self, plugin_class: Type[BinaryParserPlugin]) -> bool:
        """Register a plugin class in the registry.

        Checks for naming conflicts before registering. If a plugin with the same
        name is already registered, the registration is rejected.

        Args:
            plugin_class: The plugin class to register.

        Returns:
            True if the plugin was registered successfully, False if a plugin
            with the same name already exists.

        Example:
            >>> registry = PluginRegistry()
            >>> registry.register(MyCustomParser)
            True
            >>> registry.register(MyCustomParser)  # Duplicate
            False
        """
        # Instantiate plugin to get its metadata
        plugin_instance = plugin_class()
        plugin_name = plugin_instance.get_name()

        # Check for name conflict
        if plugin_name in self._plugins:
            return False

        # Register the plugin
        self._plugins[plugin_name] = plugin_class

        # Register format handlers
        for fmt in plugin_instance.get_supported_formats():
            if fmt not in self._format_handlers:
                self._format_handlers[fmt] = []
            self._format_handlers[fmt].append(plugin_name)

        return True

    def get_plugin(self, name: str) -> Optional[Type[BinaryParserPlugin]]:
        """Get a plugin class by name.

        Args:
            name: The name of the plugin to retrieve.

        Returns:
            The plugin class if found, None otherwise.

        Example:
            >>> registry = PluginRegistry()
            >>> registry.register(MyCustomParser)
            True
            >>> plugin = registry.get_plugin("MyCustomParser")
            >>> plugin is MyCustomParser
            True
        """
        return self._plugins.get(name)

    def find_handler(self, file_path: Path) -> Optional[Type[BinaryParserPlugin]]:
        """Find an appropriate plugin handler for the given file.

        This method performs a two-step lookup:
        1. First checks if any plugins are registered for the file's extension
        2. Falls back to checking all plugins' can_parse methods

        Args:
            file_path: Path to the file to find a handler for.

        Returns:
            The plugin class that can handle the file, or None if no suitable
            plugin is found.

        Example:
            >>> registry = PluginRegistry()
            >>> registry.register(XFWParser)
            True
            >>> handler = registry.find_handler(Path("/path/to/file.xfw"))
            >>> handler is XFWParser
            True
        """
        # Check by extension first for efficiency
        ext = file_path.suffix.lower()
        if ext in self._format_handlers:
            for plugin_name in self._format_handlers[ext]:
                plugin = self._plugins[plugin_name]
                if plugin().can_parse(file_path):
                    return plugin

        # Fall back to checking all plugins
        for plugin_class in self._plugins.values():
            if plugin_class().can_parse(file_path):
                return plugin_class

        return None


# Global registry instance
_global_registry: Optional[PluginRegistry] = None
_global_registry_lock = threading.Lock()


def get_global_registry() -> PluginRegistry:
    """
    Get the global plugin registry instance.

    This function returns a singleton PluginRegistry instance that can be
    shared across the application for plugin management.

    Returns:
        The global PluginRegistry instance.
    """
    global _global_registry

    with _global_registry_lock:
        if _global_registry is None:
            _global_registry = PluginRegistry()
            logger.debug("Created global plugin registry instance")

        return _global_registry


__all__ = [
    'PluginRegistry',
    'get_global_registry',
]
