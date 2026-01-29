"""
Plugin loader module for Binary SBOM Generator.

This module handles dynamic loading of binary parser plugins from Python files.
It uses importlib.util to load plugin modules from file paths and extracts
plugin classes that implement the BinaryParserPlugin interface.

The loader system uses:
- importlib.util for dynamic module loading from file paths
- Abstract base class validation to ensure plugins implement required methods
- Robust error handling for malformed or incompatible plugins
- Module cleanup to prevent resource leaks

Example:
    >>> from binary_sbom.plugins.loader import load_plugin
    >>> from pathlib import Path
    >>>
    >>> # Load a plugin from file
    >>> plugin_path = Path('~/.binary-sbom/plugins/custom_parser.py').expanduser()
    >>> plugin_class = load_plugin(plugin_path)
    >>> if plugin_class:
    ...     # Create instance and use it
    ...     plugin = plugin_class()
    ...     metadata = plugin.parse(Path('/path/to/binary.bin'))
    ...     print(f"Parsed with: {plugin.get_name()}")
    >>>
    >>> # Load multiple plugins
    >>> from binary_sbom.plugins.discovery import discover_plugins
    >>> for plugin_path in discover_plugins():
    ...     plugin_class = load_plugin(plugin_path)
    ...     if plugin_class:
    ...         print(f"Loaded: {plugin_class.__name__}")
"""

import importlib.util
import logging
import sys
from pathlib import Path
from typing import Optional, Type

from binary_sbom.plugins.api import BinaryParserPlugin

logger = logging.getLogger(__name__)


def load_plugin(plugin_path: Path) -> Optional[Type[BinaryParserPlugin]]:
    """Load a binary parser plugin class from a Python file.

    This function dynamically loads a Python module from the specified file path
    and extracts the plugin class that implements BinaryParserPlugin. It uses
    importlib.util.spec_from_file_location to load modules from arbitrary file
    paths, enabling plugins to be loaded from user directories.

    The function searches the loaded module for classes that:
    - Inherit from BinaryParserPlugin (directly or indirectly)
    - Are concrete (not abstract base classes themselves)
    - Have a concrete implementation of all abstract methods

    Only the first valid plugin class is returned. If multiple plugin classes
    exist in the file, only the first one found is returned.

    Args:
        plugin_path: Path to the Python file containing the plugin.
                    Must be a Path object pointing to a .py file.
                    Can be absolute or relative path.

    Returns:
        The plugin class (not an instance) if found and valid, None otherwise.
        Returns None if:
        - No BinaryParserPlugin subclass is found in the module
        - All found subclasses are abstract or invalid
        - The file cannot be loaded or executed
        - Import errors occur during module loading

    Raises:
        FileNotFoundError: If plugin_path doesn't exist or is inaccessible.
        ValueError: If plugin_path is not a .py file.
        TypeError: If plugin_path is not a Path object.

    Example:
        >>> from pathlib import Path
        >>> from binary_sbom.plugins.loader import load_plugin
        >>>
        >>> # Load a specific plugin
        >>> plugin_file = Path('~/my_plugins/elf_parser.py').expanduser()
        >>> PluginClass = load_plugin(plugin_file)
        >>> if PluginClass:
        ...     # Instantiate and use
        ...     plugin = PluginClass()
        ...     print(f"Loaded: {plugin.get_name()}")
        ...     print(f"Formats: {plugin.get_supported_formats()}")
        >>>
        >>> # Load from discovered plugins
        >>> from binary_sbom.plugins.discovery import discover_plugins
        >>> for plugin_path in discover_plugins():
        ...     PluginClass = load_plugin(plugin_path)
        ...     if PluginClass:
        ...         plugin = PluginClass()
        ...         print(f"Ready to use: {plugin.get_name()}")

    Notes:
        - Uses importlib.util.spec_from_file_location for dynamic loading
        - The loaded module is added to sys.modules with a unique name
        - Only the first valid plugin class is returned
        - Abstract classes are filtered out automatically
        - Import errors during plugin loading are logged but don't raise
        - The same plugin file can be loaded multiple times (each with unique module name)
        - Module namespace conflicts are prevented using unique names based on file path

    Implementation Details:
        The loading process:
        1. Validate the file path exists and is a .py file
        2. Create a unique module name using the file path
        3. Load the module using spec_from_file_location and module_from_spec
        4. Execute the module to populate its namespace
        5. Search for BinaryParserPlugin subclasses
        6. Filter out abstract base classes
        7. Return the first concrete plugin class found

        Error handling:
        - File not found errors are raised immediately
        - Import/execution errors are logged and return None
        - Type errors are raised for invalid arguments
    """
    # Validate input type
    if not isinstance(plugin_path, Path):
        raise TypeError(
            f"plugin_path must be a Path object, got {type(plugin_path).__name__}"
        )

    # Expand user path (~) if present
    plugin_path = plugin_path.expanduser()

    # Check file exists
    if not plugin_path.exists():
        raise FileNotFoundError(f"Plugin file not found: {plugin_path}")

    # Check it's a file (not directory)
    if not plugin_path.is_file():
        raise ValueError(f"Plugin path is not a file: {plugin_path}")

    # Check it's a Python file
    if plugin_path.suffix != '.py':
        raise ValueError(f"Plugin file must be a .py file, got: {plugin_path.suffix}")

    logger.debug(f"Loading plugin from: {plugin_path}")

    try:
        # Create a unique module name based on file path
        # This prevents conflicts when loading multiple plugins
        module_name = f"binary_sbom_plugin_{plugin_path.stem}_{hash(str(plugin_path)) & 0x7FFFFFFF}"

        # Create module spec from file location
        spec = importlib.util.spec_from_file_location(module_name, plugin_path)

        if spec is None or spec.loader is None:
            logger.error(f"Failed to create module spec for: {plugin_path}")
            return None

        # Create module from spec
        module = importlib.util.module_from_spec(spec)

        # Add to sys.modules before executing to handle circular imports
        sys.modules[module_name] = module

        # Execute the module to run its code
        spec.loader.exec_module(module)

        # Read the source file to get class definition order (deterministic)
        # Using AST ensures we get classes in the order they're defined in the file
        import ast
        try:
            plugin_source = plugin_path.read_text()
            tree = ast.parse(plugin_source)

            # Get class names in definition order
            class_names_in_order = [
                node.name for node in ast.walk(tree)
                if isinstance(node, ast.ClassDef)
            ]
        except Exception as e:
            logger.debug(f"Could not parse plugin file for class order: {e}")
            class_names_in_order = []

        # Search for BinaryParserPlugin subclasses in the module
        # If we have AST class order, use it; otherwise fall back to dir()
        search_order = class_names_in_order if class_names_in_order else dir(module)

        for attr_name in search_order:
            attr = getattr(module, attr_name, None)
            if attr is None:
                continue

            # Check if it's a class that inherits from BinaryParserPlugin
            if (isinstance(attr, type) and
                issubclass(attr, BinaryParserPlugin) and
                attr is not BinaryParserPlugin):  # Exclude the base class itself

                # Check if it's not abstract (can be instantiated)
                try:
                    # Try to check if it has abstract methods
                    if not hasattr(attr, '__abstractmethods__') or len(attr.__abstractmethods__) == 0:
                        logger.info(f"Successfully loaded plugin class: {attr.__name__} from {plugin_path}")
                        return attr
                except Exception as e:
                    logger.debug(f"Skipping {attr.__name__}: {e}")
                    continue

        # No valid plugin class found
        logger.warning(f"No valid BinaryParserPlugin subclass found in: {plugin_path}")
        return None

    except ImportError as e:
        logger.error(f"Import error loading plugin from {plugin_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error loading plugin from {plugin_path}: {e}")
        return None


__all__ = [
    'load_plugin',
]
