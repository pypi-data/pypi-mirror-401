"""
Worker process for sandboxed binary parsing.

This module provides the worker process entry point that executes LIEF
parsing in an isolated process with resource limits applied.
"""

import logging
from typing import Any, Dict

from multiprocessing import Queue

from binary_sbom.sandbox.limits import ResourceLimits

logger = logging.getLogger(__name__)


def worker_main(
    file_path: str,
    result_queue: Queue,
    error_queue: Queue,
    config: Dict[str, int],
) -> None:
    """
    Worker process entry point for sandboxed binary parsing.

    This function runs in a separate process with resource limits applied.
    It parses the binary file using LIEF and returns the metadata via IPC.

    Resource limits are applied BEFORE parsing begins, ensuring the LIEF
    library operates within the constrained environment. If parsing exceeds
    limits, the kernel terminates this process.

    Args:
        file_path: Path to isolated binary file.
        result_queue: Queue for sending successful results.
        error_queue: Queue for sending error information.
        config: Resource limit configuration with keys:
            - memory_mb: Maximum memory in megabytes
            - cpu_time_seconds: Maximum CPU time in seconds
            - wall_clock_timeout: Wall-clock timeout in seconds

    The worker sends results via result_queue:
        - On success: Dict with parsed metadata
        - On error: Dict with "_error" key set to True

    Example:
        Result format (success):
        {
            "name": "binary",
            "type": "ELF",
            "architecture": "x86_64",
            "entrypoint": "0x400000",
            "sections": [...],
            "dependencies": [...]
        }

        Result format (error):
        {
            "_error": True,
            "_error_type": "MemoryError",
            "_error_message": "Out of memory"
        }
    """
    try:
        # Step 1: Apply resource limits to this process
        # This MUST be done before any LIEF operations
        limits = ResourceLimits.from_dict(config)
        limits.apply()

        logger.info(
            f"Worker started with limits: memory={limits.memory_mb}MB, "
            f"cpu_time={limits.cpu_time_seconds}s"
        )

        # Step 2: Parse binary using LIEF
        # This is the potentially dangerous operation that we're sandboxing
        metadata = parse_binary_with_lief(file_path)

        # Step 3: Get resource usage statistics
        usage = limits.get_current_usage()
        logger.info(
            f"Worker completed. Resource usage: "
            f"memory={usage['memory_mb']}MB, "
            f"cpu_time={usage['cpu_time_seconds']}s"
        )

        # Step 4: Send result back via IPC
        # Include resource usage for security logging
        metadata["_resource_usage"] = usage
        result_queue.put(metadata)

    except MemoryError as e:
        # Memory limit exceeded
        logger.error(f"Memory limit exceeded: {e}")
        error_queue.put(("MemoryError", str(e)))

    except Exception as e:
        # Other errors (parsing errors, file errors, etc.)
        error_type = type(e).__name__
        error_msg = str(e)
        logger.error(f"Worker error: {error_type}: {error_msg}")
        error_queue.put((error_type, error_msg))

    finally:
        # Ensure queues are closed
        try:
            result_queue.close()
        except Exception:
            pass
        try:
            error_queue.close()
        except Exception:
            pass


def parse_binary_with_lief(file_path: str) -> Dict[str, Any]:
    """
    Parse binary file using LIEF library and extract metadata.

    This function executes LIEF parsing inside the sandboxed worker process.
    It supports ELF, PE, MachO, and raw binary formats and extracts metadata
    including sections, dependencies, entrypoint, and architecture information.

    Args:
        file_path: Path to binary file to parse.

    Returns:
        Dictionary containing parsed binary metadata with keys:
        - name (str): Binary name
        - type (str): Binary format (ELF, PE, MachO, Raw)
        - architecture (str): Target architecture
        - entrypoint (Optional[str]): Entry point address in hex format
        - sections (List[Dict]): Section information with name, size, virtual_address
        - dependencies (List[str]): Imported libraries

    Raises:
        RuntimeError: If LIEF library is not available.
        Exception: If binary parsing fails (corrupted, unsupported format, etc.).
        MemoryError: If file is too large to parse.
        OSError: If file cannot be read.

    Example:
        >>> metadata = parse_binary_with_lief('/bin/ls')
        >>> print(metadata['type'])
        'ELF'
        >>> print(metadata['architecture'])
        'x86_64'
    """
    try:
        import lief
    except ImportError as e:
        raise RuntimeError(
            "LIEF library is not available. Install it with: pip install lief"
        ) from e

    # Parse binary using LIEF
    try:
        binary = lief.parse(file_path)
    except MemoryError as e:
        # Memory error during parsing
        raise MemoryError(f"File too large to parse {file_path}: {e}") from e
    except (IOError, OSError) as e:
        # File read errors
        raise OSError(f"Read error while parsing {file_path}: {e}") from e
    except Exception as e:
        # Other LIEF parsing errors
        error_msg = str(e).lower()
        if 'corrupted' in error_msg or 'truncated' in error_msg:
            raise Exception(f"Corrupted binary file {file_path}: {e}") from e
        elif 'not supported' in error_msg or 'unknown format' in error_msg:
            raise Exception(f"Unsupported binary format in {file_path}: {e}") from e
        elif 'out of memory' in error_msg or 'memory' in error_msg:
            raise MemoryError(f"File too large to parse {file_path}: {e}") from e
        else:
            raise Exception(f"Failed to parse binary file {file_path}: {e}") from e

    # Check if parsing succeeded
    if binary is None:
        raise Exception(f"Failed to parse binary file {file_path}: Unknown format or corrupted file")

    # Extract metadata
    metadata = _extract_metadata(binary, file_path)

    return metadata


def _extract_metadata(binary: Any, file_path: str) -> Dict[str, Any]:
    """
    Extract metadata from parsed LIEF binary object.

    For ELF files (.so), this extracts enhanced metadata including:
    - Exported and imported symbols
    - SONAME and version information
    - DT_RUNPATH/DT_RPATH for library search paths
    - Dynamic dependencies with version information

    Args:
        binary: Parsed LIEF binary object.
        file_path: Original file path (for error messages).

    Returns:
        Dictionary with extracted metadata.

    Raises:
        Exception: If metadata extraction fails.
    """
    from pathlib import Path

    metadata = {
        "name": Path(file_path).name,
        "type": "Unknown",
        "architecture": "unknown",
        "entrypoint": None,
        "sections": [],
        "dependencies": [],
    }

    try:
        # Detect format and architecture
        metadata["type"], metadata["architecture"] = _detect_format(binary)

        # Extract entrypoint (if present and non-zero)
        if hasattr(binary, 'entrypoint') and binary.entrypoint != 0:
            try:
                metadata["entrypoint"] = hex(binary.entrypoint)
            except (AttributeError, ValueError):
                # Some binary types may not have entrypoint or it may not be convertible
                pass

        # Extract dependencies (imported libraries)
        if hasattr(binary, 'imported_libraries'):
            try:
                for library in binary.imported_libraries:
                    if library:
                        metadata["dependencies"].append(library)
            except (AttributeError, TypeError) as e:
                logger.warning(f"Failed to extract imported libraries: {e}")

        # Extract sections
        if hasattr(binary, 'sections'):
            try:
                for section in binary.sections:
                    try:
                        section_info = {
                            'name': section.name,
                            'size': section.size,
                            'virtual_address': hex(section.virtual_address) if hasattr(section, 'virtual_address') else None,
                        }
                        metadata["sections"].append(section_info)
                    except (AttributeError, ValueError) as e:
                        # Skip problematic sections but continue processing
                        logger.warning(f"Failed to extract section info: {e}")
                        continue
            except (AttributeError, TypeError) as e:
                logger.warning(f"Failed to extract sections: {e}")

        # Enhanced ELF metadata extraction for .so files
        if metadata["type"] == "ELF":
            _extract_elf_enhanced_metadata(binary, metadata)

        # Enhanced PE metadata extraction for .exe files
        elif metadata["type"] == "PE":
            _extract_pe_enhanced_metadata(binary, metadata)

    except Exception as e:
        raise Exception(f"Failed to extract metadata from binary: {e}") from e

    return metadata


def _detect_format(binary: Any) -> tuple[str, str]:
    """
    Detect binary format and architecture from LIEF binary object.

    Args:
        binary: Parsed LIEF binary object.

    Returns:
        Tuple of (format, architecture) where:
        - format: One of 'ELF', 'PE', 'MachO', 'Raw'
        - architecture: String representation of architecture

    Raises:
        Exception: If format detection fails.
    """
    try:
        import lief

        # Check format using isinstance
        if isinstance(binary, lief.ELF.Binary):
            architecture = str(binary.header.machine_type)
            return "ELF", architecture
        elif isinstance(binary, lief.PE.Binary):
            architecture = str(binary.header.machine)
            return "PE", architecture
        elif isinstance(binary, lief.MachO.Binary):
            architecture = str(binary.header.cpu_type)
            return "MachO", architecture
        else:
            # Unknown format - treat as raw binary
            return "Raw", "unknown"
    except Exception as e:
        raise Exception(f"Failed to detect binary format: {e}") from e


def _extract_elf_enhanced_metadata(binary: Any, metadata: Dict[str, Any]) -> None:
    """
    Extract enhanced ELF-specific metadata for .so files.

    This function extracts:
    - Exported symbols (functions and global variables)
    - Imported symbols (external dependencies)
    - SONAME (shared object name)
    - Version information from .gnu.version sections
    - DT_RUNPATH and DT_RPATH for library search paths
    - Dynamic dependency details

    Args:
        binary: Parsed LIEF ELF binary object.
        metadata: Dictionary to populate with enhanced metadata (modified in-place).

    Notes:
        - Adds the following keys to metadata:
            - exported_symbols (List[Dict]): Exported symbols with name, type, size, address
            - imported_symbols (List[Dict]): Imported symbols with name and version
            - soname (Optional[str]): Shared object name from DT_SONAME
            - runpath (Optional[str]): DT_RUNPATH value for library search paths
            - rpath (Optional[str]): DT_RPATH value for library search paths
            - has_version_info (bool): Whether version information is present
            - is_stripped (bool): Whether the binary has been stripped
        - Handles stripped binaries gracefully by noting missing symbol information
        - Symbol extraction failures are logged but don't stop parsing
    """
    try:
        # Initialize ELF-specific metadata fields
        metadata["exported_symbols"] = []
        metadata["imported_symbols"] = []
        metadata["soname"] = None
        metadata["runpath"] = None
        metadata["rpath"] = None
        metadata["has_version_info"] = False
        metadata["is_stripped"] = True

        # Extract exported symbols (from dynamic symbol table)
        if hasattr(binary, 'dynamic_symbols'):
            try:
                for symbol in binary.dynamic_symbols:
                    try:
                        # Only process exported symbols (functions and objects)
                        if symbol.shndx != 0:  # Not undefined
                            symbol_info = {
                                'name': symbol.name if symbol.name else '',
                                'type': str(symbol.type) if hasattr(symbol, 'type') else 'unknown',
                                'size': symbol.size if hasattr(symbol, 'size') else 0,
                                'address': hex(symbol.value) if hasattr(symbol, 'value') and symbol.value != 0 else None,
                                'binding': str(symbol.binding) if hasattr(symbol, 'binding') else 'unknown',
                            }
                            # Only add non-empty symbols
                            if symbol_info['name']:
                                metadata["exported_symbols"].append(symbol_info)
                    except (AttributeError, ValueError) as e:
                        logger.debug(f"Failed to process exported symbol: {e}")
                        continue

                # Determine if binary is stripped based on symbol presence
                metadata["is_stripped"] = len(metadata["exported_symbols"]) == 0

            except (AttributeError, TypeError) as e:
                logger.warning(f"Failed to extract exported symbols: {e}")

        # Extract imported symbols (undefined symbols from dynamic table)
        if hasattr(binary, 'dynamic_symbols'):
            try:
                for symbol in binary.dynamic_symbols:
                    try:
                        # Only process imported symbols (undefined symbols)
                        if symbol.shndx == 0 and symbol.name:  # Undefined
                            symbol_info = {
                                'name': symbol.name,
                                'version': symbol.symbol_version if hasattr(symbol, 'symbol_version') else None,
                            }
                            metadata["imported_symbols"].append(symbol_info)
                    except (AttributeError, ValueError) as e:
                        logger.debug(f"Failed to process imported symbol: {e}")
                        continue
            except (AttributeError, TypeError) as e:
                logger.warning(f"Failed to extract imported symbols: {e}")

        # Extract SONAME from DT_SONAME entry
        if hasattr(binary, 'has_dt_soname') and binary.has_dt_soname:
            try:
                metadata["soname"] = binary.soname
            except (AttributeError, ValueError) as e:
                logger.debug(f"Failed to extract SONAME: {e}")

        # Extract DT_RUNPATH for library search paths
        if hasattr(binary, 'has_dt_runpath') and binary.has_dt_runpath:
            try:
                metadata["runpath"] = binary.runpath
            except (AttributeError, ValueError) as e:
                logger.debug(f"Failed to extract DT_RUNPATH: {e}")

        # Extract DT_RPATH for library search paths (deprecated but still used)
        if hasattr(binary, 'has_dt_rpath') and binary.has_dt_rpath:
            try:
                metadata["rpath"] = binary.rpath
            except (AttributeError, ValueError) as e:
                logger.debug(f"Failed to extract DT_RPATH: {e}")

        # Check for version information (.gnu.version section)
        if hasattr(binary, 'has_gnu_version') and binary.has_gnu_version:
            try:
                metadata["has_version_info"] = True
                # Optionally extract version definitions and requirements
                if hasattr(binary, 'gnu_version_definitions'):
                    version_defs = []
                    for version_def in binary.gnu_version_definitions:
                        try:
                            version_defs.append({
                                'name': version_def.name if hasattr(version_def, 'name') else '',
                                'version': version_def.version if hasattr(version_def, 'version') else 0,
                            })
                        except (AttributeError, ValueError):
                            continue
                    if version_defs:
                        metadata["version_definitions"] = version_defs

                if hasattr(binary, 'gnu_version_requirements'):
                    version_reqs = []
                    for version_req in binary.gnu_version_requirements:
                        try:
                            version_reqs.append({
                                'name': version_req.name if hasattr(version_req, 'name') else '',
                                'version': version_req.version if hasattr(version_req, 'version') else 0,
                            })
                        except (AttributeError, ValueError):
                            continue
                    if version_reqs:
                        metadata["version_requirements"] = version_reqs

            except (AttributeError, TypeError) as e:
                logger.debug(f"Failed to extract version information: {e}")

        # Add annotation about stripped binaries
        if metadata["is_stripped"]:
            logger.info(f"ELF binary appears to be stripped (no exported symbols found)")

    except Exception as e:
        # Log error but don't fail the entire parsing
        logger.warning(f"Failed to extract enhanced ELF metadata: {e}")
        # Ensure all required keys exist even on error
        metadata.setdefault("exported_symbols", [])
        metadata.setdefault("imported_symbols", [])
        metadata.setdefault("soname", None)
        metadata.setdefault("runpath", None)
        metadata.setdefault("rpath", None)
        metadata.setdefault("has_version_info", False)
        metadata.setdefault("is_stripped", True)


def _extract_pe_enhanced_metadata(binary: Any, metadata: Dict[str, Any]) -> None:
    """
    Extract enhanced PE-specific metadata for .exe files.

    This function extracts:
    - Import table (all imported DLLs and functions)
    - Export table (exported functions with ordinals)
    - Version resource (CompanyName, FileVersion, ProductVersion, Copyright)
    - Authenticode signature information
    - Resource types (icons, manifests, version info)

    Args:
        binary: Parsed LIEF PE binary object.
        metadata: Dictionary to populate with enhanced metadata (modified in-place).

    Notes:
        - Adds the following keys to metadata:
            - import_table (List[Dict]): Imported DLLs with their functions
            - export_table (List[Dict]): Exported functions with ordinals and addresses
            - version_info (Optional[Dict]): Version resource information
            - has_authenticode (bool): Whether Authenticode signature is present
            - resources (List[Dict]): Resource types found in the binary
        - Handles missing imports/exports gracefully
        - Version info extraction failures are logged but don't stop parsing
    """
    try:
        # Initialize PE-specific metadata fields
        metadata["import_table"] = []
        metadata["export_table"] = []
        metadata["version_info"] = None
        metadata["has_authenticode"] = False
        metadata["resources"] = []

        # Extract import table
        if hasattr(binary, 'imports'):
            try:
                for import_entry in binary.imports:
                    try:
                        dll_info = {
                            'name': import_entry.name if hasattr(import_entry, 'name') else '',
                            'functions': []
                        }

                        # Extract functions imported from this DLL
                        if hasattr(import_entry, 'entries'):
                            for entry in import_entry.entries:
                                try:
                                    func_info = {
                                        'name': entry.name if hasattr(entry, 'name') and entry.name else '',
                                        'ordinal': entry.ordinal if hasattr(entry, 'ordinal') else None,
                                        'iat_address': hex(entry.iat_address) if hasattr(entry, 'iat_address') and entry.iat_address != 0 else None,
                                        'is_ordinal': entry.is_ordinal if hasattr(entry, 'is_ordinal') else False,
                                    }
                                    dll_info['functions'].append(func_info)
                                except (AttributeError, ValueError) as e:
                                    logger.debug(f"Failed to process imported function: {e}")
                                    continue

                        # Only add DLLs that have at least one function or have a name
                        if dll_info['name'] or dll_info['functions']:
                            metadata["import_table"].append(dll_info)

                    except (AttributeError, TypeError) as e:
                        logger.debug(f"Failed to process import entry: {e}")
                        continue

            except (AttributeError, TypeError) as e:
                logger.warning(f"Failed to extract import table: {e}")

        # Extract export table
        if hasattr(binary, 'exports'):
            try:
                if binary.exports:
                    for export_entry in binary.exports:
                        try:
                            func_info = {
                                'name': export_entry.name if hasattr(export_entry, 'name') and export_entry.name else '',
                                'ordinal': export_entry.ordinal if hasattr(export_entry, 'ordinal') else None,
                                'address': hex(export_entry.address) if hasattr(export_entry, 'address') and export_entry.address != 0 else None,
                                'forwarded': export_entry.is_forwarded if hasattr(export_entry, 'is_forwarded') else False,
                            }
                            # Only add non-empty exports
                            if func_info['name'] or func_info['ordinal'] is not None:
                                metadata["export_table"].append(func_info)
                        except (AttributeError, ValueError) as e:
                            logger.debug(f"Failed to process export entry: {e}")
                            continue

            except (AttributeError, TypeError) as e:
                logger.warning(f"Failed to extract export table: {e}")

        # Extract version information from resources
        if hasattr(binary, 'resources_manager'):
            try:
                resources_manager = binary.resources_manager

                # Try to get version info
                if hasattr(resources_manager, 'version'):
                    version = resources_manager.version
                    if version:
                        version_info = {}

                        # Extract string file info if available
                        if hasattr(version, 'string_file_info'):
                            try:
                                for lang_info in version.string_file_info.lang_items:
                                    try:
                                        if hasattr(lang_info, 'items'):
                                            for item in lang_info.items:
                                                try:
                                                    key = item.key if hasattr(item, 'key') else ''
                                                    value = item.value if hasattr(item, 'value') else ''
                                                    if key and value:
                                                        version_info[key] = value
                                                except (AttributeError, ValueError):
                                                    continue
                                    except (AttributeError, TypeError):
                                        continue
                            except (AttributeError, TypeError) as e:
                                logger.debug(f"Failed to extract string file info: {e}")

                        # Extract fixed file info if available
                        if hasattr(version, 'fixed_file_info'):
                            try:
                                fixed_info = version.fixed_file_info
                                if fixed_info:
                                    version_info['file_version'] = str(fixed_info.file_version) if hasattr(fixed_info, 'file_version') else ''
                                    version_info['product_version'] = str(fixed_info.product_version) if hasattr(fixed_info, 'product_version') else ''
                                    version_info['file_flags'] = str(fixed_info.file_flags) if hasattr(fixed_info, 'file_flags') else ''
                                    version_info['file_os'] = str(fixed_info.file_os) if hasattr(fixed_info, 'file_os') else ''
                            except (AttributeError, TypeError) as e:
                                logger.debug(f"Failed to extract fixed file info: {e}")

                        if version_info:
                            metadata["version_info"] = version_info

            except (AttributeError, TypeError) as e:
                logger.debug(f"Failed to extract version information: {e}")

        # Check for Authenticode signature
        if hasattr(binary, 'signatures'):
            try:
                metadata["has_authenticode"] = len(binary.signatures) > 0

                # Optionally extract signature information
                if metadata["has_authenticode"]:
                    try:
                        sig_info = {
                            'count': len(binary.signatures),
                            'has_signer': False,
                            'has_counter_signer': False,
                        }

                        for sig in binary.signatures:
                            try:
                                if hasattr(sig, 'signers'):
                                    sig_info['has_signer'] = len(sig.signers) > 0
                                if hasattr(sig, 'countersignatures'):
                                    sig_info['has_counter_signer'] = len(sig.countersignatures) > 0
                            except (AttributeError, TypeError):
                                continue

                        metadata["authenticode_info"] = sig_info
                    except (AttributeError, TypeError) as e:
                        logger.debug(f"Failed to extract authenticode details: {e}")

            except (AttributeError, TypeError) as e:
                logger.debug(f"Failed to check authenticode signature: {e}")

        # Extract resource types
        if hasattr(binary, 'resources'):
            try:
                resource_types = set()
                for resource in binary.resources:
                    try:
                        if hasattr(resource, 'type'):
                            resource_type = str(resource.type)
                            resource_types.add(resource_type)
                    except (AttributeError, ValueError):
                        continue

                metadata["resources"] = sorted(list(resource_types))

            except (AttributeError, TypeError) as e:
                logger.warning(f"Failed to extract resource types: {e}")

        # Log summary
        import_count = len(metadata["import_table"])
        export_count = len(metadata["export_table"])
        logger.info(
            f"PE metadata extracted: {import_count} imported DLLs, "
            f"{export_count} exported functions, "
            f"version_info={'present' if metadata['version_info'] else 'none'}, "
            f"authenticode={'yes' if metadata['has_authenticode'] else 'no'}"
        )

    except Exception as e:
        # Log error but don't fail the entire parsing
        logger.warning(f"Failed to extract enhanced PE metadata: {e}")
        # Ensure all required keys exist even on error
        metadata.setdefault("import_table", [])
        metadata.setdefault("export_table", [])
        metadata.setdefault("version_info", None)
        metadata.setdefault("has_authenticode", False)
        metadata.setdefault("resources", [])
