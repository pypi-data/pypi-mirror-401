"""
Plugin API definition for Binary SBOM Generator.

This module defines the abstract base class that all binary parser plugins
must implement. The plugin interface establishes a contract for custom binary
parsers, specifying required methods and return types.

The plugin system provides:
- Extensible architecture for adding custom binary format parsers
- Standardized interface for parser discovery and loading
- Type-safe contract for parser implementations
- Consistent metadata output format across all parsers

Plugin Lifecycle:
1. Discovery: Plugins are discovered from entry points or directories
2. Registration: Each plugin registers its supported formats
3. Selection: The plugin manager selects the appropriate plugin for a file
4. Execution: The plugin's parse() method is called to extract metadata

Required Methods:
- get_name(): Return a unique identifier for the plugin
- get_supported_formats(): Declare supported file extensions and magic bytes
- can_parse(): Determine if a specific file can be parsed by this plugin
- parse(): Extract and return package metadata in standardized format
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pathlib import Path


class BinaryParserPlugin(ABC):
    """Abstract base class for binary parser plugins.

    All plugins must inherit from this class and implement the required methods.
    The plugin system uses these methods to discover, load, and execute parsers
    for custom binary formats.

    This class establishes a contract that all parser plugins must follow to
    ensure consistent behavior and interoperability with the plugin manager.
    Each plugin is responsible for parsing a specific binary format or family
    of related formats.

    Plugin Naming Convention:
        - Use descriptive names that indicate the format (e.g., "ELFParser", "MXFirmwareParser")
        - Avoid generic names (e.g., "Parser", "BinaryParser")
        - Use PascalCase with no spaces or special characters

    Plugin Best Practices:
        - Implement can_parse() to efficiently reject unsupported files
        - Return complete and accurate metadata in parse()
        - Handle errors gracefully and raise appropriate exceptions
        - Document any format-specific quirks or limitations
        - Include version information for compatibility tracking

    Example:
        >>> from pathlib import Path
        >>> from binary_sbom.plugins.api import BinaryParserPlugin
        >>>
        >>> class MyFirmwareParser(BinaryParserPlugin):
        ...     '''Custom parser for MyFirmware format.'''
        ...
        ...     def get_name(self) -> str:
        ...         return "MyFirmwareParser"
        ...
        ...     def get_supported_formats(self) -> list[str]:
        ...         return ['.mfw', 'MYFW']
        ...
        ...     def can_parse(self, file_path: Path) -> bool:
        ...         # Check extension first (fast)
        ...         if file_path.suffix != '.mfw':
        ...             return False
        ...         # Verify magic bytes (more reliable)
        ...         with open(file_path, 'rb') as f:
        ...             header = f.read(4)
        ...             return header == b'MYFW'
        ...
        ...     def parse(self, file_path: Path) -> dict:
        ...         # Extract metadata from firmware file
        ...         return {
        ...             'packages': [{
        ...                 'name': 'my-firmware',
        ...                 'version': '1.0.0',
        ...                 'type': 'firmware'
        ...             }],
        ...             'relationships': [],
        ...             'annotations': []
        ...         }
        ...
        ...     @property
        ...     def version(self) -> str:
        ...         return "1.2.0"

    Notes:
        - All abstract methods must be implemented by concrete subclasses
        - The parse() method may be called on large files, so implement efficiently
        - Plugin instances may be reused for multiple files
        - Thread safety is the plugin's responsibility if needed
    """

    @abstractmethod
    def get_name(self) -> str:
        """Return unique plugin name.

        This method returns a unique identifier for the plugin. The name is used
        for plugin registration, logging, and user-facing messages. It should be
        descriptive and indicate the binary format(s) the plugin handles.

        The plugin name should:
        - Be unique across all registered plugins
        - Use PascalCase (e.g., "ELFParser", "MXFirmwareParser")
        - Indicate the supported format or family of formats
        - Not contain spaces, underscores, or special characters
        - Remain stable across plugin versions for compatibility

        Returns:
            Unique identifier for this plugin. Examples:
            - "ELFParser" for ELF format binaries
            - "PEParser" for Windows PE format
            - "MXFirmwareParser" for custom MX firmware format
            - "IntelMEParser" for Intel Management Engine firmware

        Raises:
            NotImplementedError: If not implemented by subclass.

        Example:
            >>> plugin = MyCustomParser()
            >>> name = plugin.get_name()
            >>> print(f"Loading plugin: {name}")
            Loading plugin: MyCustomParser

        Notes:
            - This method is called once during plugin registration
            - The name is used as a key in plugin manager's registry
            - Changing a plugin's name may break existing integrations
        """
        pass

    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """Return list of supported file extensions and/or magic bytes.

        This method declares which file formats the plugin can handle. The
        plugin manager uses this information for plugin selection and to
        provide informative error messages when no plugin supports a file.

        Format identifiers can be:
        - File extensions (with leading dot): ['.elf', '.exe', '.bin']
        - Magic bytes (hex strings): ['0x7FELF', 'MZ']
        - Format family names: ['firmware', 'archive']

        Using both extensions and magic bytes is recommended for reliability:
        - Extensions are fast but can be spoofed
        - Magic bytes are reliable but require file I/O
        - The plugin manager checks extensions first, then magic bytes

        Returns:
            List of supported format identifiers. Examples:
            - ['.elf'] for ELF binaries (extension only)
            - ['.exe', 'MZ'] for PE binaries (extension + magic)
            - ['.mfw', 'MYFW', '0x4D595647'] for custom firmware
            - ['.bin'] for generic binary files

        Raises:
            NotImplementedError: If not implemented by subclass.

        Example:
            >>> plugin = ELFParser()
            >>> formats = plugin.get_supported_formats()
            >>> print(f"Supported formats: {', '.join(formats)}")
            Supported formats: .elf

            >>> # Multiple format indicators
            >>> plugin = PEParser()
            >>> formats = plugin.get_supported_formats()
            >>> print(formats)
            ['.exe', '.dll', '.sys', 'MZ']

        Notes:
            - Extensions must include the leading dot (e.g., '.elf', not 'elf')
            - Magic bytes can be in hex (0x...) or string format
            - The plugin manager may use this for initial filtering
            - Actual file compatibility is determined by can_parse()
            - Return at least one format identifier
            - Order doesn't matter; all formats are considered equally
        """
        pass

    @abstractmethod
    def can_parse(self, file_path: Path) -> bool:
        """Check if this plugin can parse the given file.

        This method performs a detailed check to determine if the plugin can
        handle the specified file. It should be fast and efficient to avoid
        unnecessary parsing attempts on incompatible files.

        The method should:
        - Check file extension if applicable (fast check)
        - Verify magic bytes/file signature (reliable check)
        - Validate basic file structure if needed
        - Return quickly on negative results
        - Handle file I/O errors gracefully

        This method is called before parse() to avoid attempting to parse
        incompatible files. It may be called multiple times during plugin
        selection, so efficiency is important.

        Args:
            file_path: Path to the binary file to check. Can be absolute or
                relative path. The file should exist and be readable.

        Returns:
            True if this plugin can parse the file, False otherwise.
            Return False for:
            - Missing or inaccessible files
            - Files with wrong extensions
            - Files with mismatched magic bytes
            - Files with invalid structure for this format
            - Any condition that would cause parse() to fail

        Raises:
            NotImplementedError: If not implemented by subclass.
            OSError: If file access fails (optional, can return False instead).

        Example:
            >>> from pathlib import Path
            >>> plugin = ELFParser()
            >>>
            >>> # Check ELF file
            >>> plugin.can_parse(Path('/bin/ls'))
            True
            >>>
            >>> # Check non-ELF file
            >>> plugin.can_parse(Path('/etc/passwd'))
            False
            >>>
            >>> # Implementation example
            >>> def can_parse(self, file_path: Path) -> bool:
            ...     # Fast extension check
            ...     if file_path.suffix not in ['.elf', '.so', '']:
            ...         return False
            ...     # Reliable magic byte check
            ...     try:
            ...         with open(file_path, 'rb') as f:
            ...             header = f.read(4)
            ...             return header.startswith(b'\\x7fELF')
            ...     except OSError:
            ...         return False

        Notes:
            - This method should not raise exceptions for normal parsing failures
            - Return False instead of raising for incompatible files
            - File I/O errors can be handled by returning False or raising
            - This method may be called before or after file existence checks
            - The plugin manager calls this for each candidate plugin
            - Performance matters; avoid expensive operations here
            - Parse-time validation should still happen in parse() method
        """
        pass

    @abstractmethod
    def parse(self, file_path: Path) -> Dict[str, Any]:
        """Parse binary file and return metadata dictionary.

        This is the main method that extracts package and component information
        from a binary file. It should perform a thorough analysis of the file
        and return comprehensive metadata in the standardized format.

        The method should:
        - Validate the file format before parsing
        - Extract all identifiable packages, components, and dependencies
        - Map relationships between components (depends_on, contains, etc.)
        - Add annotations for format-specific findings or limitations
        - Handle errors gracefully with informative messages
        - Work efficiently with large files (stream when possible)

        The returned metadata follows SPDX-style structure for compatibility
        with SBOM (Software Bill of Materials) tools and standards.

        Args:
            file_path: Path to the binary file to parse. Can be absolute or
                relative path. The file must exist and be readable.

        Returns:
            Dictionary containing extracted metadata with the following structure:

            ::

                {
                    'packages': [
                        {
                            'name': str,              # Package/component name
                            'version': str,           # Version if available
                            'type': str,              # Type (library, firmware, etc.)
                            'license': str,           # License if available
                            'supplier': str,          # Vendor/author if available
                            'download_location': str, # Source URL if available
                            'homepage': str,          # Project URL if available
                            ...                       # Additional fields allowed
                        },
                        ...
                    ],
                    'relationships': [
                        {
                            'source': str,    # SPDX ID of source component
                            'type': str,      # Relationship type (depends_on, contains, etc.)
                            'target': str     # SPDX ID of target component
                        },
                        ...
                    ],
                    'annotations': [
                        {
                            'spdx_id': str,   # Related component SPDX ID or 'DOCUMENT'
                            'type': str,      # Annotation type (review, other)
                            'text': str       # Free-form annotation text
                        },
                        ...
                    ]
                }

            All keys are required, but lists may be empty if no data is available.
            Additional fields may be added to package dictionaries as needed.

        Raises:
            NotImplementedError: If not implemented by subclass.
            FileNotFoundError: If file_path doesn't exist or is inaccessible.
            ValueError: If file format is invalid or corrupted.
            ParseError: If parsing fails due to format-specific issues.
            MemoryError: If file is too large to process (optional).

        Example:
            >>> from pathlib import Path
            >>> plugin = MyFirmwareParser()
            >>> metadata = plugin.parse(Path('/path/to/firmware.mfw'))
            >>>
            >>> # Print extracted packages
            >>> for pkg in metadata['packages']:
            ...     print(f"{pkg['name']} {pkg.get('version', 'unknown')}")
            libcrypto 3.0.5
            libssl 3.0.5
            firmware-base 2.1.0
            >>>
            >>> # Print relationships
            >>> for rel in metadata['relationships']:
            ...     print(f"{rel['source']} -> {rel['type']} -> {rel['target']}")
            firmware-base -> contains -> libcrypto
            firmware-base -> contains -> libssl
            libssl -> depends_on -> libcrypto

        Notes:
            - File validation should happen before heavy processing
            - Return empty lists for missing data, not None
            - Use descriptive names for packages and components
            - Include version information whenever available
            - Document any parsing limitations in annotations
            - Consider performance for large binary files
            - Thread safety is the plugin's responsibility
            - The same plugin instance may be reused for multiple files
            - Parse results should be deterministic (same file = same output)
        """
        pass

    @property
    def version(self) -> str:
        """Plugin version string.

        This property returns the version of the plugin implementation. Version
        information is useful for:
        - Compatibility checking with plugin manager
        - Debugging and logging
        - Feature detection across plugin versions
        - Dependency resolution between plugins

        Versions should follow Semantic Versioning (semver):
        - MAJOR.MINOR.PATCH format (e.g., "1.2.3")
        - Increment MAJOR for breaking changes
        - Increment MINOR for backward-compatible features
        - Increment PATCH for backward-compatible bug fixes

        Returns:
            Version identifier string. Examples:
            - "1.0.0" for initial release
            - "2.1.3" for version 2, patch 3
            - "0.5.0-beta" for pre-release versions

        Example:
            >>> plugin = MyFirmwareParser()
            >>> print(f"Using {plugin.get_name()} v{plugin.version}")
            Using MyFirmwareParser v1.2.0

            >>> # Check version compatibility
            >>> from packaging import version
            >>> if version.parse(plugin.version) >= version.parse("2.0.0"):
            ...     use_new_api(plugin)
            ... else:
            ...     use_legacy_api(plugin)

        Notes:
            - Default implementation returns "1.0.0"
            - Override this property to provide custom version
            - Version should be updated with each release
            - Consider using __version__ module variable for single source of truth
            - Pre-release identifiers are allowed (e.g., "1.0.0-alpha")
            - Build metadata is allowed (e.g., "1.0.0+build.123")
        """
        return "1.0.0"
