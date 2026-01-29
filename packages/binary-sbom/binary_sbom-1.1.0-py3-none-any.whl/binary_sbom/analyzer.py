"""
Binary analyzer module for extracting metadata from executable files.

This module provides functions for analyzing binary files (ELF, PE, MachO)
and extracting metadata such as format, architecture, sections, and dependencies.
All LIEF parsing operations are performed through a sandboxed environment
to protect against malicious binary exploits.

The sandbox provides:
- Process isolation to prevent parser exploits from affecting the main process
- Resource limits (memory, CPU, time) to prevent DoS attacks
- File system isolation to prevent path traversal via symlinks
- Automatic cleanup of temporary resources
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from binary_sbom.sandbox import SandboxManager, SandboxError
from binary_sbom.sandbox.config import SandboxConfig, load_config

logger = logging.getLogger(__name__)

# Flag to track if plugins have been loaded
_plugins_loaded = False


# Default resource limits for sandboxed binary processing
DEFAULT_MEMORY_MB = 500
DEFAULT_CPU_TIME_SECONDS = 30
DEFAULT_WALL_CLOCK_TIMEOUT = 60


def _load_plugins_once() -> None:
    """Load plugins from the plugin directory once.

    This function discovers and loads all plugins from ~/.binary-sbom/plugins/
    and registers them in the global registry. It uses a module-level flag
    to ensure plugins are only loaded once per Python session.

    Plugin loading happens lazily on the first call to analyze_binary(),
    ensuring that plugins are available when needed without impacting
    startup time for users who don't use plugins.

    Errors during plugin loading are logged but don't prevent the
    application from running - malformed plugins are skipped gracefully.

    Note:
        This function is internal to the analyzer module and is called
        automatically by analyze_binary(). Users don't need to call it.
    """
    global _plugins_loaded

    if _plugins_loaded:
        return

    try:
        # Import here to avoid circular dependencies
        from binary_sbom.plugins import discover_plugins, load_plugin, registry

        # Discover plugin files
        plugin_files = discover_plugins()

        if not plugin_files:
            logger.debug("No plugin files found in plugin directory")
            _plugins_loaded = True
            return

        # Load and register each plugin
        loaded_count = 0
        for plugin_path in plugin_files:
            try:
                plugin_class = load_plugin(plugin_path)
                if plugin_class:
                    # Register the plugin in the global registry
                    if registry.register(plugin_class):
                        plugin_instance = plugin_class()
                        logger.info(
                            f"Loaded and registered plugin: {plugin_instance.get_name()} "
                            f"from {plugin_path.name}"
                        )
                        loaded_count += 1
                    else:
                        plugin_instance = plugin_class()
                        logger.warning(
                            f"Plugin '{plugin_instance.get_name()}' already registered, "
                            f"skipping duplicate from {plugin_path.name}"
                        )
                else:
                    logger.debug(f"No valid plugin class found in {plugin_path.name}")
            except Exception as e:
                # Log but continue loading other plugins
                logger.error(f"Error loading plugin from {plugin_path.name}: {e}")

        logger.info(f"Plugin loading complete: {loaded_count} plugin(s) loaded")
        _plugins_loaded = True

    except ImportError as e:
        logger.warning(f"Plugin system not available: {e}")
        _plugins_loaded = True
    except Exception as e:
        logger.error(f"Unexpected error during plugin loading: {e}")
        _plugins_loaded = True


def analyze_binary(
    file_path: str,
    max_file_size_mb: int = 100,
    memory_mb: Optional[int] = None,
    cpu_time_seconds: Optional[int] = None,
    wall_clock_timeout: Optional[int] = None,
    sandbox_config: Optional[SandboxConfig] = None,
    config_file: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Analyze binary file and extract metadata using sandboxed LIEF parsing.

    This function is the primary entry point for binary analysis. It validates
    the input file, creates a sandboxed environment for LIEF parsing, and
    returns comprehensive metadata about the binary.

    Plugin Integration:
        This function first checks if a plugin can handle the file format.
        If a plugin is found, it uses the plugin to parse the file and returns
        plugin-specific metadata (including packages, relationships, annotations).
        If no plugin is available or the plugin fails, it falls back to the
        default sandboxed LIEF parser.

        Plugins are automatically discovered from ~/.binary-sbom/plugins/ on the
        first call and cached for subsequent calls.

    All LIEF operations are performed in an isolated subprocess with:
    - Memory limits to prevent OOM attacks
    - CPU time limits to prevent infinite loops
    - Wall-clock timeout to prevent hangs
    - Temporary file isolation to prevent path traversal

    Args:
        file_path: Path to the binary file to analyze.
        max_file_size_mb: Maximum file size in megabytes (default: 100).
        memory_mb: Maximum memory for sandbox in MB (default: from env or 500).
        cpu_time_seconds: Maximum CPU time for sandbox in seconds (default: from env or 30).
        wall_clock_timeout: Maximum wall-clock time in seconds (default: from env or 60).
        sandbox_config: Optional SandboxConfig object with all settings.
        config_file: Optional path to configuration file (YAML/TOML/JSON).

    Returns:
        Dictionary containing extracted binary metadata.

        When using default LIEF parser:
        - name (str): Binary filename
        - type (str): Binary format (ELF, PE, MachO, Raw)
        - architecture (str): Target architecture
        - entrypoint (Optional[str]): Entry point address in hex format
        - sections (List[Dict]): Section information with keys:
            - name (str): Section name
            - size (int): Section size in bytes
            - virtual_address (Optional[str]): Virtual address in hex
        - dependencies (List[str]): Imported library names
        - _parser (str): Set to 'lief' for default parser

        For ELF binaries (.so), additional fields:
        - exported_symbols (List[Dict]): Exported symbols with name, type, size, address, binding
        - imported_symbols (List[Dict]): Imported symbols with name and version
        - soname (Optional[str]): Shared object name from DT_SONAME
        - runpath (Optional[str]): DT_RUNPATH value for library search paths
        - rpath (Optional[str]): DT_RPATH value for library search paths
        - has_version_info (bool): Whether version information is present
        - is_stripped (bool): Whether the binary has been stripped

        For PE binaries (.exe), additional fields:
        - import_table (List[Dict]): Imported DLLs with their functions and ordinals
        - export_table (List[Dict]): Exported functions with ordinals and addresses
        - version_info (Optional[Dict]): Version resource with CompanyName, FileVersion, etc.
        - has_authenticode (bool): Whether Authenticode signature is present
        - resources (List[str]): Resource types found in the binary
        - authenticode_info (Optional[Dict]): Detailed signature information if present
        When using plugin parser:
        - packages (List[Dict]): Package metadata from plugin
        - relationships (List[Dict]): Package relationships
        - annotations (List[Dict]): Additional metadata
        - _parser (str): Set to 'plugin'
        - _parser_name (str): Name of the plugin used
        - _file_path (str): Path to the analyzed file

    Raises:
        ConfigValidationError: If configuration is invalid.
        FileNotFoundError: If the binary file doesn't exist.
        ValueError: If the file is invalid, empty, or too large.
        SandboxError: If sandboxed parsing fails.
        SandboxTimeoutError: If parsing exceeds time limits.
        SandboxMemoryError: If parsing exceeds memory limits.
        SandboxSecurityError: If security validation fails.
        SandboxFileError: If file operations fail in the sandbox.
        SandboxCrashedError: If the sandboxed process crashes.

    Example:
        >>> # Use defaults
        >>> metadata = analyze_binary('/bin/ls')
        >>> print(f"Format: {metadata['type']}")
        Format: ELF

        >>> # With custom limits
        >>> metadata = analyze_binary('/bin/ls', memory_mb=1000, cpu_time_seconds=60)

        >>> # With configuration file
        >>> metadata = analyze_binary('/bin/ls', config_file='sandbox_config.yaml')

        >>> # With SandboxConfig object
        >>> from binary_sbom.sandbox.config import SandboxConfig
        >>> config = SandboxConfig(memory_mb=1000)
        >>> metadata = analyze_binary('/bin/ls', sandbox_config=config)

        >>> # Plugin parsing (if plugin installed)
        >>> metadata = analyze_binary('firmware.xfw')
        >>> if metadata.get('_parser') == 'plugin':
        ...     print(f"Parsed with {metadata['_parser_name']}")
        ...     for pkg in metadata.get('packages', []):
        ...         print(f"Package: {pkg['name']}")

    Configuration Priority (highest to lowest):
        1. sandbox_config parameter
        2. config_file parameter
        3. Individual parameters (memory_mb, cpu_time_seconds, wall_clock_timeout)
        4. Environment variables
        5. Hardcoded defaults

    Notes:
        - This function uses process isolation via SandboxManager for LIEF parsing
        - Plugins are discovered from ~/.binary-sbom/plugins/ automatically
        - Plugins are loaded once on first call and cached
        - Plugin failures fall back to default LIEF parser gracefully
        - Resource limits are enforced by the OS kernel
        - All temporary files are automatically cleaned up
        - The API is backward compatible with the original non-sandboxed version
    """
    # Load plugins once (lazy initialization on first call)
    _load_plugins_once()

    # Convert file_path to Path object for plugin system
    file_path_obj = Path(file_path)

    # Check if a plugin can handle this file
    try:
        from binary_sbom.plugins import registry

        plugin_class = registry.find_handler(file_path_obj)
        if plugin_class is not None:
            plugin_instance = plugin_class()
            logger.info(
                f"Using plugin '{plugin_instance.get_name()}' for {file_path}"
            )

            # Use plugin to parse the file
            try:
                plugin_metadata = plugin_instance.parse(file_path_obj)

                # Add plugin metadata to result
                plugin_metadata['_parser'] = 'plugin'
                plugin_metadata['_parser_name'] = plugin_instance.get_name()
                plugin_metadata['_file_path'] = str(file_path)

                logger.info(
                    f"Successfully parsed {file_path} with plugin "
                    f"'{plugin_instance.get_name()}': "
                    f"{len(plugin_metadata.get('packages', []))} package(s)"
                )

                return plugin_metadata

            except Exception as e:
                # Log plugin error but fall back to default parser
                logger.warning(
                    f"Plugin '{plugin_instance.get_name()}' failed to parse {file_path}: {e}. "
                    f"Falling back to default parser."
                )
                # Continue to default parser below

    except ImportError:
        # Plugin system not available, use default parser
        logger.debug("Plugin system not available, using default parser")
    except Exception as e:
        # Unexpected error with plugin system, log and fall back
        logger.warning(f"Error checking for plugin handler: {e}. Using default parser.")

    # Load configuration with priority:
    # 1. sandbox_config > 2. config_file > 3. individual params > 4. environment > 5. defaults
    if sandbox_config is not None:
        config = sandbox_config
    elif config_file is not None:
        config = SandboxConfig.from_file(config_file)
        # Override with individual parameters if provided
        if memory_mb is not None or cpu_time_seconds is not None or wall_clock_timeout is not None:
            config_dict = config.to_full_dict()
            if memory_mb is not None:
                config_dict['memory_mb'] = memory_mb
            if cpu_time_seconds is not None:
                config_dict['cpu_time_seconds'] = cpu_time_seconds
            if wall_clock_timeout is not None:
                config_dict['wall_clock_timeout'] = wall_clock_timeout
            config = SandboxConfig.from_dict(config_dict)
    else:
        # Load from environment with parameter overrides
        config = load_config(
            use_environment=True,
            memory_mb=memory_mb,
            cpu_time_seconds=cpu_time_seconds,
            wall_clock_timeout=wall_clock_timeout,
        )

    # Create sandbox manager with configuration
    manager = SandboxManager(sandbox_config=config)

    logger.info(f"Analyzing binary file with default parser: {file_path}")

    # Parse binary in sandboxed environment
    # All LIEF operations happen in isolated subprocess
    try:
        metadata = manager.parse_binary(file_path, max_file_size_mb=max_file_size_mb)
        # Add parser identifier for consistency with plugin metadata
        metadata['_parser'] = 'lief'
        logger.info(
            f"Successfully analyzed {file_path}: "
            f"type={metadata['type']}, "
            f"arch={metadata['architecture']}"
        )
        return metadata

    except SandboxError as e:
        # Re-raise sandbox errors with additional context
        logger.error(f"Sandboxed parsing failed for {file_path}: {e}")
        raise


def detect_format(
    file_path: str,
    max_file_size_mb: int = 100,
    memory_mb: Optional[int] = None,
    cpu_time_seconds: Optional[int] = None,
    wall_clock_timeout: Optional[int] = None,
    sandbox_config: Optional[SandboxConfig] = None,
    config_file: Optional[str] = None,
) -> Tuple[str, str]:
    """
    Detect binary format type and architecture from file.

    This is a convenience function for format detection when you don't need
    the full metadata. It's more efficient than analyze_binary() when you
    only need to know the binary format and architecture.

    Like analyze_binary(), this function uses sandboxed parsing for security.

    Args:
        file_path: Path to the binary file to analyze.
        max_file_size_mb: Maximum file size in megabytes (default: 100).
        memory_mb: Maximum memory for sandbox in MB (default: from env or 500).
        cpu_time_seconds: Maximum CPU time for sandbox in seconds (default: from env or 30).
        wall_clock_timeout: Maximum wall-clock time in seconds (default: from env or 60).
        sandbox_config: Optional SandboxConfig object with all settings.
        config_file: Optional path to configuration file (YAML/TOML/JSON).

    Returns:
        Tuple of (format_type, architecture):
        - format_type (str): One of 'ELF', 'PE', 'MachO', 'Raw'
        - architecture (str): Architecture string (e.g., 'x86_64', 'ARM64')

    Raises:
        ConfigValidationError: If configuration is invalid.
        FileNotFoundError: If the binary file doesn't exist.
        ValueError: If the file is invalid, empty, or too large.
        SandboxError: If sandboxed parsing fails.
        SandboxTimeoutError: If parsing exceeds time limits.
        SandboxMemoryError: If parsing exceeds memory limits.

    Example:
        >>> format_type, arch = detect_format('/bin/ls')
        >>> print(f"This is a {format_type} binary for {arch}")
        This is a ELF binary for x86_64

        >>> # With configuration file
        >>> format_type, arch = detect_format('/bin/ls', config_file='config.yaml')

    Notes:
        - This function parses the entire binary in the sandbox
        - Returns only format and architecture, discarding other metadata
        - Use analyze_binary() if you need sections, dependencies, etc.
        - See analyze_binary() for configuration priority documentation
    """
    # Use analyze_binary to get full metadata, then extract format info
    metadata = analyze_binary(
        file_path=file_path,
        max_file_size_mb=max_file_size_mb,
        memory_mb=memory_mb,
        cpu_time_seconds=cpu_time_seconds,
        wall_clock_timeout=wall_clock_timeout,
        sandbox_config=sandbox_config,
        config_file=config_file,
    )

    format_type = metadata.get("type", "Unknown")
    architecture = metadata.get("architecture", "unknown")

    logger.debug(f"Detected format for {file_path}: {format_type} ({architecture})")
    return format_type, architecture


def analyze_binaries(
    file_paths: List[str],
    max_file_size_mb: int = 100,
    memory_mb: Optional[int] = None,
    cpu_time_seconds: Optional[int] = None,
    wall_clock_timeout: Optional[int] = None,
    sandbox_config: Optional[SandboxConfig] = None,
    config_file: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Analyze multiple binary files in sequence.

    This is a convenience function for batch analysis of multiple binaries.
    Each binary is analyzed in a separate sandboxed process for isolation.

    Args:
        file_paths: List of paths to binary files to analyze.
        max_file_size_mb: Maximum file size in megabytes (default: 100).
        memory_mb: Maximum memory for sandbox in MB (default: from env or 500).
        cpu_time_seconds: Maximum CPU time for sandbox in seconds (default: from env or 30).
        wall_clock_timeout: Maximum wall-clock time in seconds (default: from env or 60).
        sandbox_config: Optional SandboxConfig object with all settings.
        config_file: Optional path to configuration file (YAML/TOML/JSON).

    Returns:
        List of metadata dictionaries, one per binary file.
        Failed analyses are represented as dicts with an '_error' key.

    Example:
        >>> files = ['/bin/ls', '/bin/bash', '/usr/bin/python3']
        >>> results = analyze_binaries(files)
        >>> for metadata in results:
        ...     if '_error' not in metadata:
        ...         print(f"{metadata['name']}: {metadata['type']}")

        >>> # With configuration file
        >>> results = analyze_binaries(files, config_file='config.yaml')

    Notes:
        - Files are analyzed sequentially, not in parallel
        - Each file gets a fresh sandboxed process
        - Errors for individual files don't stop analysis of remaining files
        - See analyze_binary() for configuration priority documentation
    """
    results = []

    for file_path in file_paths:
        try:
            metadata = analyze_binary(
                file_path=file_path,
                max_file_size_mb=max_file_size_mb,
                memory_mb=memory_mb,
                cpu_time_seconds=cpu_time_seconds,
                wall_clock_timeout=wall_clock_timeout,
                sandbox_config=sandbox_config,
                config_file=config_file,
            )
            results.append(metadata)
        except Exception as e:
            # Log error but continue with other files
            logger.error(f"Failed to analyze {file_path}: {e}")
            results.append({"_error": True, "file": file_path, "message": str(e)})

    return results
