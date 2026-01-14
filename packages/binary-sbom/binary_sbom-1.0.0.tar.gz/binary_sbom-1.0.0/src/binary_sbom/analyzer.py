"""
Binary analyzer module for Binary SBOM Generator.

This module provides functionality to analyze binary files (ELF, PE, MachO, raw)
and extract metadata including name, type, architecture, entrypoint, sections,
and dependencies using the LIEF library.
"""

import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Tuple

if TYPE_CHECKING:
    import lief

try:
    import lief  # noqa: F811
except ImportError:
    lief = None  # type: ignore  # pragma: no cover


class BinaryAnalysisError(Exception):
    """Exception raised when binary analysis fails."""

    pass


def analyze_binary(file_path: str, max_file_size_mb: int = 100) -> Dict[str, Any]:
    """
    Analyze binary file and extract metadata.

    This function uses LIEF to parse the binary file, automatically detecting
    the format (ELF, PE, MachO, or raw). It extracts metadata including:
    - Binary name
    - Format type (ELF, PE, MachO, Raw)
    - Architecture
    - Entrypoint address
    - Section information
    - Imported libraries/dependencies

    Args:
        file_path: Path to the binary file to analyze.
        max_file_size_mb: Maximum file size in MB (default: 100).

    Returns:
        Dictionary containing extracted metadata with keys:
        - name (str): Binary name
        - type (str): Binary format type (ELF, PE, MachO, Raw)
        - architecture (str): Target architecture
        - entrypoint (Optional[str]): Entry point address in hex
        - sections (List[Dict[str, Any]]): List of section information
        - dependencies (List[str]): List of imported libraries

    Raises:
        ImportError: If LIEF library is not installed.
        FileNotFoundError: If the binary file does not exist.
        BinaryAnalysisError: If the binary file cannot be parsed or is invalid.

    Example:
        >>> metadata = analyze_binary('/bin/ls')
        >>> metadata['type']
        'ELF'
        >>> metadata['architecture']
        'x86_64'
        >>> len(metadata['dependencies']) > 0
        True
    """
    if lief is None:
        raise ImportError(
            "LIEF library is required for binary analysis. "
            "Install it with: pip install lief"
        )

    # Validate file exists
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Binary file not found: {file_path}")

    if not path.is_file():
        raise BinaryAnalysisError(f"Path is not a file: {file_path}")

    # Check file permissions
    if not os.access(file_path, os.R_OK):
        raise BinaryAnalysisError(
            f"Permission denied: Cannot read file {file_path}"
        )

    # Check file size
    try:
        file_size = path.stat().st_size
        max_size_bytes = max_file_size_mb * 1024 * 1024
        if file_size == 0:
            raise BinaryAnalysisError(f"File is empty: {file_path}")
        if file_size > max_size_bytes:
            raise BinaryAnalysisError(
                f"File too large: {file_path} ({file_size / 1024 / 1024:.2f} MB). "
                f"Maximum size is {max_file_size_mb} MB."
            )
    except OSError as e:
        raise BinaryAnalysisError(f"Cannot access file {file_path}: {e}")

    # Parse binary with LIEF (auto-detects format)
    try:
        binary = lief.parse(file_path)
    except MemoryError as e:
        raise BinaryAnalysisError(
            f"File too large to parse {file_path}: {e}"
        )
    except (IOError, OSError) as e:
        raise BinaryAnalysisError(
            f"Read error while parsing {file_path}: {e}. "
            "File may be corrupted or inaccessible."
        )
    except Exception as e:
        error_msg = str(e).lower()
        if 'corrupted' in error_msg or 'truncated' in error_msg or 'invalid' in error_msg:
            raise BinaryAnalysisError(
                f"Corrupted binary file {file_path}: {e}. "
                "File may be truncated or have invalid headers."
            )
        elif 'not supported' in error_msg or 'unknown format' in error_msg:
            raise BinaryAnalysisError(
                f"Unsupported binary format in {file_path}: {e}. "
                "Supported formats: ELF, PE, MachO, and raw binaries."
            )
        elif 'out of memory' in error_msg or 'memory' in error_msg:
            raise BinaryAnalysisError(
                f"File too large to parse {file_path}: {e}"
            )
        else:
            raise BinaryAnalysisError(f"Failed to parse binary file {file_path}: {e}")

    if binary is None:
        # LIEF returns None for unsupported or corrupted binaries
        raise BinaryAnalysisError(
            f"Failed to parse binary file: {file_path}. "
            "File may be corrupted, truncated, or in an unsupported format. "
            "Supported formats: ELF, PE, MachO, and raw binaries."
        )

    # Detect binary type and extract format-specific metadata
    try:
        metadata = _extract_metadata(binary, file_path)
    except Exception as e:
        raise BinaryAnalysisError(f"Failed to extract metadata from {file_path}: {e}")

    return metadata


def _extract_metadata(binary: Any, file_path: str) -> Dict[str, Any]:
    """
    Extract metadata from parsed LIEF binary object.

    This helper function determines the binary format (ELF, PE, MachO, or raw)
    and extracts format-specific metadata including architecture, entrypoint,
    sections, and dependencies.

    Args:
        binary: Parsed LIEF binary object.
        file_path: Original file path for fallback naming.

    Returns:
        Dictionary containing extracted metadata.
    """
    # Determine binary type and architecture
    binary_type, architecture = _detect_format(binary)

    # Build base metadata
    metadata: Dict[str, Any] = {
        'name': binary.name if hasattr(binary, 'name') else file_path,
        'type': binary_type,
        'architecture': architecture,
        'entrypoint': None,
        'sections': [],
        'dependencies': [],
    }

    # Extract entrypoint if available
    if hasattr(binary, 'entrypoint') and binary.entrypoint != 0:
        try:
            metadata['entrypoint'] = hex(binary.entrypoint)
        except (TypeError, ValueError):
            metadata['entrypoint'] = None

    # Extract imported libraries (dependencies)
    if hasattr(binary, 'imported_libraries'):
        try:
            for library in binary.imported_libraries:
                if library:  # Filter out empty strings
                    metadata['dependencies'].append(library)
        except (AttributeError, TypeError):
            pass

    # Extract section information
    if hasattr(binary, 'sections'):
        try:
            for section in binary.sections:
                section_info: Dict[str, Any] = {
                    'name': section.name if hasattr(section, 'name') else 'unknown',
                    'size': section.size if hasattr(section, 'size') else 0,
                }

                # Add virtual address if available
                if hasattr(section, 'virtual_address'):
                    try:
                        section_info['virtual_address'] = hex(section.virtual_address)
                    except (TypeError, ValueError):
                        section_info['virtual_address'] = None

                metadata['sections'].append(section_info)
        except (AttributeError, TypeError):
            pass

    return metadata


def extract_metadata(binary: Any, file_path: str) -> Dict[str, Any]:
    """
    Extract metadata from parsed LIEF binary object.

    This is the public interface for metadata extraction. It determines the
    binary format (ELF, PE, MachO, or raw) and extracts format-specific
    metadata including name, type, architecture, entrypoint, sections,
    and dependencies.

    Args:
        binary: Parsed LIEF binary object.
        file_path: Original file path for fallback naming.

    Returns:
        Dictionary containing extracted metadata with keys:
        - name (str): Binary name
        - type (str): Binary format type (ELF, PE, MachO, Raw)
        - architecture (str): Target architecture
        - entrypoint (Optional[str]): Entry point address in hex
        - sections (List[Dict[str, Any]]): List of section information
        - dependencies (List[str]): List of imported libraries

    Raises:
        BinaryAnalysisError: If metadata extraction fails.

    Example:
        >>> binary = lief.parse('/bin/ls')
        >>> metadata = extract_metadata(binary, '/bin/ls')
        >>> metadata['type']
        'ELF'
        >>> metadata['architecture']
        'x86_64'
        >>> len(metadata['dependencies']) > 0
        True
    """
    try:
        return _extract_metadata(binary, file_path)
    except Exception as e:
        raise BinaryAnalysisError(f"Failed to extract metadata: {e}")


def detect_format(file_path: str, max_file_size_mb: int = 100) -> Tuple[str, str]:
    """
    Detect binary format type and architecture from file.

    This is a convenience function that parses a binary file and returns
    its format type and architecture. It uses LIEF to auto-detect the format.

    Args:
        file_path: Path to the binary file to analyze.
        max_file_size_mb: Maximum file size in MB (default: 100).

    Returns:
        Tuple of (format_type, architecture) where:
        - format_type: One of 'ELF', 'PE', 'MachO', or 'Raw'
        - architecture: String representation of architecture

    Raises:
        ImportError: If LIEF library is not installed.
        FileNotFoundError: If the binary file does not exist.
        BinaryAnalysisError: If the binary file cannot be parsed or is invalid.

    Example:
        >>> detect_format('/bin/ls')
        ('ELF', 'x86_64')
        >>> detect_format('/usr/bin/ls')
        ('ELF', 'x86_64')
    """
    if lief is None:
        raise ImportError(
            "LIEF library is required for format detection. "
            "Install it with: pip install lief"
        )

    # Validate file exists
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Binary file not found: {file_path}")

    if not path.is_file():
        raise BinaryAnalysisError(f"Path is not a file: {file_path}")

    # Check file permissions
    if not os.access(file_path, os.R_OK):
        raise BinaryAnalysisError(
            f"Permission denied: Cannot read file {file_path}"
        )

    # Check file size
    try:
        file_size = path.stat().st_size
        max_size_bytes = max_file_size_mb * 1024 * 1024
        if file_size == 0:
            raise BinaryAnalysisError(f"File is empty: {file_path}")
        if file_size > max_size_bytes:
            raise BinaryAnalysisError(
                f"File too large: {file_path} ({file_size / 1024 / 1024:.2f} MB). "
                f"Maximum size is {max_file_size_mb} MB."
            )
    except OSError as e:
        raise BinaryAnalysisError(f"Cannot access file {file_path}: {e}")

    # Parse binary with LIEF (auto-detects format)
    try:
        binary = lief.parse(file_path)
    except MemoryError as e:
        raise BinaryAnalysisError(
            f"File too large to parse {file_path}: {e}"
        )
    except (IOError, OSError) as e:
        raise BinaryAnalysisError(
            f"Read error while parsing {file_path}: {e}. "
            "File may be corrupted or inaccessible."
        )
    except Exception as e:
        error_msg = str(e).lower()
        if 'corrupted' in error_msg or 'truncated' in error_msg or 'invalid' in error_msg:
            raise BinaryAnalysisError(
                f"Corrupted binary file {file_path}: {e}. "
                "File may be truncated or have invalid headers."
            )
        elif 'not supported' in error_msg or 'unknown format' in error_msg:
            raise BinaryAnalysisError(
                f"Unsupported binary format in {file_path}: {e}. "
                "Supported formats: ELF, PE, MachO, and raw binaries."
            )
        elif 'out of memory' in error_msg or 'memory' in error_msg:
            raise BinaryAnalysisError(
                f"File too large to parse {file_path}: {e}"
            )
        else:
            raise BinaryAnalysisError(f"Failed to parse binary file {file_path}: {e}")

    if binary is None:
        # LIEF returns None for unsupported or corrupted binaries
        raise BinaryAnalysisError(
            f"Failed to parse binary file: {file_path}. "
            "File may be corrupted, truncated, or in an unsupported format. "
            "Supported formats: ELF, PE, MachO, and raw binaries."
        )

    # Use internal format detection
    return _detect_format(binary)


def _detect_format(binary: Any) -> Tuple[str, str]:
    """
    Detect binary format type and architecture from LIEF binary object.

    Uses isinstance checks to determine the binary format (ELF, PE, MachO)
    and extracts format-specific architecture information.

    This is an internal function that operates on already-parsed LIEF objects.
    For format detection from a file path, use the public detect_format() function.

    Args:
        binary: Parsed LIEF binary object.

    Returns:
        Tuple of (format_type, architecture) where:
        - format_type: One of 'ELF', 'PE', 'MachO', or 'Raw'
        - architecture: String representation of architecture

    Example:
        >>> binary = lief.parse('/bin/ls')
        >>> _detect_format(binary)
        ('ELF', 'x86_64')
    """
    # If lief is not available (None), return raw binary
    if lief is None:
        return "Raw", "unknown"

    # Check for ELF format
    try:
        if isinstance(binary, lief.ELF.Binary):
            architecture = str(binary.header.machine_type)
            return "ELF", architecture
    except (AttributeError, TypeError):
        pass

    # Check for PE format
    try:
        if isinstance(binary, lief.PE.Binary):
            architecture = str(binary.header.machine)
            return "PE", architecture
    except (AttributeError, TypeError):
        pass

    # Check for MachO format
    try:
        if isinstance(binary, lief.MachO.Binary):
            architecture = str(binary.header.cpu_type)
            return "MachO", architecture
    except (AttributeError, TypeError):
        pass

    # Fallback to raw binary
    return "Raw", "unknown"


__all__ = [
    'analyze_binary',
    'extract_metadata',
    'detect_format',
    'BinaryAnalysisError',
]
