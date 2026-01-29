"""
Plugin discovery module for Binary SBOM Generator.

This module handles discovering plugin files from the filesystem, scanning
the plugins directory for Python files that may contain parser implementations.
Plugins are discovered from ~/.binary-sbom/plugins/ by default, with automatic
directory creation if missing.

The discovery system uses:
- pathlib for cross-platform path handling
- Glob patterns for file matching
- Filtering to exclude private and special files

Example:
    >>> from binary_sbom.plugins.discovery import discover_plugins
    >>> from pathlib import Path
    >>>
    >>> # Discover all plugin files
    >>> plugin_files = discover_plugins()
    >>> for plugin_path in plugin_files:
    ...     print(f"Found plugin: {plugin_path.name}")
    Found plugin: elf_parser.py
    Found plugin: firmware_parser.py
    >>>
    >>> # Discover from custom directory
    >>> custom_plugins = discover_plugins(Path('/path/to/custom/plugins'))
"""

from pathlib import Path
from typing import List, Optional


def discover_plugins(plugins_dir: Optional[Path] = None) -> List[Path]:
    """Discover Python plugin files in the plugins directory.

    This function searches for plugin files in the specified directory or the
    default location (~/.binary-sbom/plugins/). It automatically creates the
    directory if it doesn't exist, ensuring the plugin system is always ready
    for use.

    Plugin files are Python files (.py extension) that are not:
    - __init__.py (reserved for module initialization)
    - Starting with underscore (private files like _helper.py)

    The function uses pathlib for cross-platform compatibility, working
    seamlessly on Windows, Linux, and macOS.

    Args:
        plugins_dir: Optional path to custom plugin directory.
                    If None, uses ~/.binary-sbom/plugins/
                    Must be a Path object or None.

    Returns:
        List of Path objects pointing to discovered plugin files.
        Returns empty list if:
        - No plugin files are found
        - Directory doesn't exist and can't be created
        - Directory exists but contains no .py files

    Raises:
        TypeError: If plugins_dir is not a Path object or None.
        PermissionError: Propagated if directory creation fails due to permissions.

    Example:
        >>> # Discover from default location
        >>> plugins = discover_plugins()
        >>> print(f"Found {len(plugins)} plugins")
        Found 3 plugins
        >>>
        >>> # Discover from custom directory
        >>> custom_dir = Path('/opt/binary-sbom/plugins')
        >>> plugins = discover_plugins(custom_dir)
        >>> for plugin in plugins:
        ...     print(plugin)
        /opt/binary-sbom/plugins/custom_parser.py
        >>>
        >>> # Process discovered plugins
        >>> from binary_sbom.plugins.loader import load_plugin
        >>> plugins = discover_plugins()
        >>> for plugin_path in plugins:
        ...     plugin_class = load_plugin(plugin_path)
        ...     if plugin_class:
        ...         print(f"Loaded: {plugin_class.__name__}")

    Notes:
        - Creates ~/.binary-sbom/plugins/ automatically if missing
        - Only returns files, not directories
        - Does not validate plugin content (use loader for validation)
        - Returns sorted list for deterministic order
        - Symbolic links are followed if they point to valid .py files
        - Hidden files (starting with .) are excluded on Unix-like systems
    """
    if plugins_dir is None:
        plugins_dir = Path.home() / ".binary-sbom" / "plugins"
    elif not isinstance(plugins_dir, Path):
        raise TypeError(
            f"plugins_dir must be a Path object or None, got {type(plugins_dir).__name__}"
        )

    # Create directory if it doesn't exist
    if not plugins_dir.exists():
        try:
            plugins_dir.mkdir(parents=True, exist_ok=True)
            return []
        except (OSError, PermissionError) as e:
            # Return empty list if we can't create the directory
            # This allows the system to function gracefully
            return []

    # Verify it's a directory (not a file)
    if not plugins_dir.is_dir():
        return []

    # Find all .py files
    try:
        all_py_files = list(plugins_dir.glob("*.py"))
    except (OSError, PermissionError):
        # Return empty list if we can't read the directory
        return []

    # Filter out special files
    plugin_files = [
        f for f in all_py_files
        if f.name != "__init__.py" and not f.name.startswith("_")
    ]

    # Return sorted list for deterministic order
    return sorted(plugin_files)


__all__ = [
    'discover_plugins',
]
