"""
File discovery module for Binary SBOM Generator.

This module provides functionality for scanning directories and discovering binary files
for batch processing. It implements a multi-layered binary detection approach combining
extension filtering, magic number detection, and LIEF validation for accurate identification
of executable files.

The discovery module supports:
- Recursive directory traversal with depth control
- Symbolic link handling with circular reference detection
- File filtering by extension, size, and glob patterns
- Permission and accessibility handling with graceful degradation
- Cross-platform compatibility (Linux, macOS, Windows)

Example:
    >>> from binary_sbom.discovery import discover_binaries
    >>> result = discover_binaries('/path/to/binaries', recursive=True)
    >>> print(f"Found {len(result.binary_files)} binary files")
"""

import fnmatch
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Set

try:
    from lief import ELF, MachO, PE
except ImportError:
    ELF = None  # type: ignore[assignment]
    MachO = None  # type: ignore[assignment]
    PE = None  # type: ignore[assignment]

try:
    from binary_sbom.parallel_processor import ParallelProcessor
except ImportError:
    ParallelProcessor = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)


# Known binary file extensions (quick filter)
BINARY_EXTENSIONS = {
    # Executables
    '.exe', '.dll', '.so', '.dylib', '.bin',
    # Firmware
    '.elf', '.hex', '.rom', '.fw', '.bios',
    # Kernel/Boot
    '.vmlinuz', '.zimage', '.uimage', '.fit',
    # Object files and libraries
    '.o', '.a', '.lib', '.obj', '.sys', '.driver',
}

# Known text file extensions (quick exclusion)
TEXT_EXTENSIONS = {
    '.txt', '.md', '.rst', '.html', '.xml',
    '.py', '.js', '.ts', '.java', '.c', '.cpp', '.h', '.hpp',
    '.sh', '.bash', '.zsh', '.fish',
    '.yml', '.yaml', '.json', '.toml', '.ini', '.cfg',
    '.css', '.scss', '.less', '.sass',
}

# Default directories to exclude during scanning
DEFAULT_EXCLUDE_DIRS = {
    '.git', '.svn', '.hg',  # Version control
    '__pycache__', 'node_modules',  # Build artifacts
    'venv', '.venv', 'env',  # Virtual environments
}

# Magic number signatures for binary file detection
MAGIC_NUMBERS: Dict[bytes, str] = {
    # ELF (Linux/Unix)
    b'\x7fELF': 'ELF',
    # PE (Windows)
    b'MZ': 'PE',
    # MachO (macOS)
    b'\xfe\xed\xfa\xce': 'MachO',
    b'\xfe\xed\xfa\xcf': 'MachO',
    b'\xce\xfa\xed\xfe': 'MachO',
    b'\xcf\xfa\xed\xfe': 'MachO',
    # ZIP-based (JAR, APK, etc.)
    b'PK\x03\x04': 'ZIP',
    # GZIP
    b'\x1f\x8b': 'GZIP',
    # BZIP2
    b'BZh': 'BZIP2',
    # XZ/LZMA
    b'\xfd7zXZ\x00': 'XZ',
    # LZ4
    b'\x04\x22\x4d\x18': 'LZ4',
    # 7Z
    b'7z\xbc\xaf\x27\x1c': '7Z',
    # RAR
    b'Rar!\x1a\x07': 'RAR',
    # ISO 9660
    b'CD001': 'ISO',
}


@dataclass
class DiscoveryError:
    """
    Error encountered during file discovery.

    This dataclass represents an error that occurred while scanning a directory
    or validating a file during the discovery process.

    Attributes:
        file_path: Path to the file that caused the error
        error_type: Type of error ('permission', 'broken_symlink', 'corrupted', etc.)
        message: Human-readable error message
        exception: Optional exception object if available

    Example:
        >>> error = DiscoveryError(
        ...     file_path='/path/to/file.bin',
        ...     error_type='permission',
        ...     message='Permission denied'
        ... )
    """
    file_path: str
    error_type: str
    message: str
    exception: Optional[Exception] = None


@dataclass
class DiscoveryResult:
    """
    Result of directory scan for binary files.

    This dataclass encapsulates the results of a directory scanning operation,
    including discovered binary files, skipped files, and any errors encountered.

    Attributes:
        total_files: Total number of files scanned
        binary_files: List of paths to discovered binary files
        skipped_files: List of paths to skipped non-binary files
        errors: List of DiscoveryError objects for files that couldn't be processed

    Example:
        >>> result = discover_binaries('/path/to/binaries')
        >>> print(f"Found {result.success_count} binaries")
        >>> print(f"Skipped {result.skipped_count} files")
        >>> if result.errors:
        ...     print(f"Encountered {result.error_count} errors")
    """
    total_files: int = 0
    binary_files: List[str] = field(default_factory=list)
    skipped_files: List[str] = field(default_factory=list)
    errors: List[DiscoveryError] = field(default_factory=list)

    @property
    def success_count(self) -> int:
        """Number of successfully discovered binary files."""
        return len(self.binary_files)

    @property
    def skipped_count(self) -> int:
        """Number of skipped non-binary files."""
        return len(self.skipped_files)

    @property
    def error_count(self) -> int:
        """Number of errors encountered during discovery."""
        return len(self.errors)


def check_magic_number(file_path: str) -> Optional[str]:
    """
    Check file header for magic number signature.

    This function reads the first 32 bytes of a file and checks if the
    header matches known binary file signatures (magic numbers).

    Args:
        file_path: Path to the file to check

    Returns:
        File type string if magic number matches (e.g., 'ELF', 'PE', 'MachO'),
        or None if no match or file cannot be read

    Example:
        >>> file_type = check_magic_number('/bin/ls')
        >>> print(file_type)  # 'ELF'
        'ELF'
    """
    try:
        with open(file_path, 'rb') as f:
            header = f.read(32)

        for magic, file_type in MAGIC_NUMBERS.items():
            if header.startswith(magic):
                return file_type

        return None
    except (IOError, OSError) as e:
        logger.debug(f"Cannot read file header for {file_path}: {e}")
        return None


def validate_with_lief(file_path: str) -> bool:
    """
    Validate binary file using LIEF parsing.

    This function attempts to parse a file using LIEF to definitively
    confirm it's a valid binary file in a supported format.

    Args:
        file_path: Path to the file to validate

    Returns:
        True if LIEF successfully parses the file as a binary format,
        False otherwise

    Example:
        >>> is_valid = validate_with_lief('/bin/ls')
        >>> print(is_valid)
        True
    """
    if ELF is None:
        # LIEF is not installed, skip validation
        logger.warning("LIEF is not installed, skipping binary validation")
        return False

    try:
        import lief

        binary = lief.parse(file_path)
        if binary is None:
            return False

        # Check if it's a known binary format
        if isinstance(binary, (ELF.Binary, PE.Binary, MachO.Binary)):
            return True

        # LIEF can also parse some archive formats
        if hasattr(binary, 'is_archive') and binary.is_archive:
            return True

        return False
    except Exception as e:
        logger.debug(f"LIEF validation failed for {file_path}: {e}")
        return False


def is_binary_file(
    file_path: str,
    use_magic_numbers: bool = True,
    use_lief_validation: bool = True
) -> bool:
    """
    Check if file is a binary file using multi-layered detection.

    This function implements a three-layered detection approach:
    1. Quick extension filter (known binary/text extensions)
    2. Magic number detection (file header signatures)
    3. LIEF parsing validation (definitive confirmation)

    Args:
        file_path: Path to the file to check
        use_magic_numbers: Enable magic number detection (default: True)
        use_lief_validation: Enable LIEF validation (default: True)

    Returns:
        True if the file is determined to be a binary file, False otherwise

    Example:
        >>> is_binary = is_binary_file('/bin/ls')
        >>> print(is_binary)
        True
        >>> is_binary = is_binary_file('/etc/hosts')
        >>> print(is_binary)
        False
    """
    # Layer 1: Extension-based quick filter
    _, ext = os.path.splitext(file_path)
    ext_lower = ext.lower()

    # Known text extensions - skip immediately
    if ext_lower in TEXT_EXTENSIONS:
        return False

    # Known binary extensions - proceed to validation
    if ext_lower in BINARY_EXTENSIONS:
        if use_lief_validation:
            return validate_with_lief(file_path)
        return True

    # Layer 2: Magic number detection
    if use_magic_numbers:
        file_type = check_magic_number(file_path)
        if file_type:
            # Magic number matched - confirm with LIEF
            if use_lief_validation:
                return validate_with_lief(file_path)
            return True

    # Layer 3: LIEF validation for ambiguous files
    if use_lief_validation:
        return validate_with_lief(file_path)

    # No confirmation - treat as non-binary
    return False


def is_broken_symlink(file_path: str) -> bool:
    """
    Check if symlink points to non-existent target.

    Args:
        file_path: Path to check

    Returns:
        True if the path is a broken symlink, False otherwise

    Example:
        >>> is_broken = is_broken_symlink('/path/to/broken_link')
        >>> print(is_broken)
        True
    """
    if not os.path.islink(file_path):
        return False

    return not os.path.exists(file_path)


# Global variable to store validation options for parallel processing
_validation_options = {
    'use_magic_numbers': True,
    'use_lief_validation': True,
}


def _validate_file_for_binary(file_path: str) -> Dict[str, Any]:
    """
    Validate a single file as binary (worker function for parallel processing).

    This function is designed to be called by the ParallelProcessor to validate
    files in parallel. It performs all the same checks as the sequential version
    but returns a dictionary result.

    Note: This function reads validation options from the global _validation_options
    dict to avoid pickling issues with closures.

    Args:
        file_path: Path to the file to validate

    Returns:
        Dictionary with validation results:
        {
            'file_path': str,
            'is_binary': bool,
            'is_archive': bool,
            'error': Optional[str],
            'is_broken_symlink': bool,
            'has_permission': bool
        }
    """
    use_magic_numbers = _validation_options.get('use_magic_numbers', True)
    use_lief_validation = _validation_options.get('use_lief_validation', True)

    result = {
        'file_path': file_path,
        'is_binary': False,
        'is_archive': False,
        'error': None,
        'is_broken_symlink': False,
        'has_permission': True,
    }

    # Check permissions
    if not os.access(file_path, os.R_OK):
        result['has_permission'] = False
        result['error'] = 'Permission denied'
        return result

    # Check for broken symlinks
    if is_broken_symlink(file_path):
        result['is_broken_symlink'] = True
        result['error'] = 'Broken symlink'
        return result

    # Check if file is binary
    try:
        if is_binary_file(file_path, use_magic_numbers=use_magic_numbers, use_lief_validation=use_lief_validation):
            result['is_binary'] = True

            # Check if it's an archive file
            file_type = check_magic_number(file_path)
            if file_type in ('ZIP', 'GZIP', 'BZIP2', 'XZ', 'LZ4', '7Z', 'RAR', 'ISO'):
                result['is_archive'] = True

    except Exception as e:
        result['error'] = f'Error processing file: {e}'

    return result


def resolve_symlink(
    file_path: str,
    scope: str = 'any',
    root_dir: Optional[str] = None
) -> Optional[str]:
    """
    Resolve symlink according to scope policy.

    Args:
        file_path: Path to potential symlink
        scope: Symlink resolution scope - 'any', 'directory', or 'none'
            - 'any': Follow all symlinks (default)
            - 'directory': Follow only if target is within root_dir
            - 'none': Don't follow symlinks
        root_dir: Root directory path (required for 'directory' scope)

    Returns:
        Resolved target path if symlink should be followed, None otherwise

    Example:
        >>> # Follow all symlinks
        >>> resolved = resolve_symlink('/path/to/link', scope='any')
        >>> # Follow only within directory
        >>> resolved = resolve_symlink('/path/to/link', scope='directory', root_dir='/path')
    """
    if scope == 'none':
        return None

    if not os.path.islink(file_path):
        return file_path

    try:
        resolved = os.path.realpath(file_path)

        if scope == 'directory' and root_dir:
            # Check if resolved path is within root_dir
            try:
                resolved_path = Path(resolved).resolve()
                root_path = Path(root_dir).resolve()
                # Check if resolved is relative to root
                try:
                    resolved_path.relative_to(root_path)
                    return resolved
                except ValueError:
                    # Not within root directory
                    logger.debug(f"Symlink target outside directory: {file_path} -> {resolved}")
                    return None
            except (OSError, ValueError):
                return None

        return resolved

    except (OSError, ValueError) as e:
        logger.warning(f"Cannot resolve symlink {file_path}: {e}")
        return None


def scan_directory(
    root_dir: str,
    recursive: bool = True,
    max_depth: Optional[int] = None,
    follow_symlinks: bool = True,
    exclude_dirs: Optional[Set[str]] = None,
    include_hidden: bool = True
) -> Iterator[str]:
    """
    Scan directory and yield file paths.

    This function performs directory traversal with support for recursion control,
    symlink handling, and directory filtering.

    Args:
        root_dir: Root directory to scan
        recursive: Enable recursive directory traversal (default: True)
        max_depth: Maximum recursion depth (None = unlimited)
        follow_symlinks: Follow symbolic links (default: True)
        exclude_dirs: Set of directory names to exclude (default: DEFAULT_EXCLUDE_DIRS)
        include_hidden: Include hidden files and directories (default: True)

    Yields:
        Paths to files discovered in the directory

    Example:
        >>> for file_path in scan_directory('/path/to/binaries'):
        ...     print(file_path)
    """
    if exclude_dirs is None:
        exclude_dirs = DEFAULT_EXCLUDE_DIRS

    root_path = Path(root_dir)

    if not root_path.exists():
        raise FileNotFoundError(f"Directory does not exist: {root_dir}")

    if not root_path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {root_dir}")

    def _scan_with_depth(current_dir: Path, current_depth: int) -> Iterator[str]:
        """Helper function for depth-limited scanning."""
        if max_depth is not None and current_depth > max_depth:
            return

        try:
            with os.scandir(str(current_dir)) as entries:
                dirs_to_scan = []

                for entry in entries:
                    # Skip hidden directories if configured
                    if not include_hidden and entry.name.startswith('.') and entry.is_dir():
                        continue

                    # Skip excluded directories
                    if entry.is_dir() and entry.name in exclude_dirs:
                        continue

                    if entry.is_file(follow_symlinks=False):
                        # Skip hidden files if configured
                        if not include_hidden and entry.name.startswith('.'):
                            continue

                        yield entry.path

                    elif entry.is_dir() and recursive:
                        dirs_to_scan.append(entry.name)

                # Recursively scan subdirectories
                for dir_name in dirs_to_scan:
                    dir_path = current_dir / dir_name
                    yield from _scan_with_depth(dir_path, current_depth + 1)

        except (PermissionError, OSError) as e:
            logger.warning(f"Cannot access directory {current_dir}: {e}")

    if recursive and max_depth is None:
        # Use os.walk for unlimited depth (faster)
        for root, dirs, files in os.walk(root_dir, followlinks=follow_symlinks):
            # Modify dirs in-place to prevent descent into excluded dirs
            if exclude_dirs:
                dirs[:] = [d for d in dirs if d not in exclude_dirs and (include_hidden or not d.startswith('.'))]

            for name in files:
                if not include_hidden and name.startswith('.'):
                    continue

                yield os.path.join(root, name)
    else:
        # Use depth-limited scanning
        yield from _scan_with_depth(root_path, 0)


def discover_binaries(
    root_dir: str,
    *,
    # Traversal options
    recursive: bool = True,
    max_depth: Optional[int] = None,
    follow_symlinks: bool = True,
    symlink_scope: str = 'any',

    # Filtering options
    include_extensions: Optional[Set[str]] = None,
    exclude_extensions: Optional[Set[str]] = None,
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
    exclude_dirs: Optional[Set[str]] = None,
    include_hidden: bool = True,

    # Size filters
    min_size_bytes: int = 0,
    max_size_bytes: Optional[int] = None,

    # Detection options
    use_magic_numbers: bool = True,
    use_lief_validation: bool = True,
    include_archives: bool = False,

    # Parallel processing options
    parallel: bool = False,
    max_workers: Optional[int] = None,

    # Performance options
    verbose: bool = False
) -> DiscoveryResult:
    """
    Discover binary files in directory.

    This function scans a directory tree and identifies binary files using a
    multi-layered detection approach. It supports extensive filtering options
    and handles errors gracefully without stopping the entire scan.

    Args:
        root_dir: Root directory to scan
        recursive: Enable recursive directory traversal (default: True)
        max_depth: Maximum recursion depth (None = unlimited)
        follow_symlinks: Follow symbolic links (default: True)
        symlink_scope: 'any', 'directory', or 'none' - controls which symlinks to follow
        include_extensions: Only include files with these extensions (e.g., {'.elf', '.so'})
        exclude_extensions: Exclude files with these extensions
        include_patterns: Glob patterns to include (e.g., ['lib*.so'])
        exclude_patterns: Glob patterns to exclude (e.g., ['*test*'])
        exclude_dirs: Directory names to exclude (default: DEFAULT_EXCLUDE_DIRS)
        include_hidden: Include hidden files/directories (default: True)
        min_size_bytes: Minimum file size in bytes (default: 0)
        max_size_bytes: Maximum file size in bytes (None = unlimited)
        use_magic_numbers: Use magic number detection (default: True)
        use_lief_validation: Use LIEF parsing validation (default: True)
        include_archives: Include archive files (.zip, .tar, etc.) (default: False)
        parallel: Enable parallel processing for file validation (default: False)
        max_workers: Maximum number of parallel workers (None = auto-detect)
        verbose: Enable verbose logging (default: False)

    Returns:
        DiscoveryResult containing discovered binary files, skipped files, and errors

    Raises:
        FileNotFoundError: If root_dir does not exist
        NotADirectoryError: If root_dir is not a directory

    Example:
        >>> # Basic usage
        >>> result = discover_binaries('/path/to/binaries')
        >>> print(f"Found {len(result.binary_files)} binaries")
        >>> # With filtering
        >>> result = discover_binaries(
        ...     '/path/to/binaries',
        ...     include_extensions={'.so', '.elf'},
        ...     min_size_bytes=1024
        ... )
        >>> # With parallel processing
        >>> result = discover_binaries(
        ...     '/path/to/binaries',
        ...     parallel=True,
        ...     max_workers=4
        ... )
    """
    result = DiscoveryResult()

    # Validate root directory
    if not os.path.exists(root_dir):
        raise FileNotFoundError(f"Directory does not exist: {root_dir}")

    if not os.path.isdir(root_dir):
        raise NotADirectoryError(f"Path is not a directory: {root_dir}")

    # Check if parallel processing is requested and available
    use_parallel = parallel and ParallelProcessor is not None
    if parallel and ParallelProcessor is None:
        logger.warning("Parallel processing requested but ParallelProcessor is not available. Using sequential processing.")

    if verbose:
        mode = "parallel" if use_parallel else "sequential"
        logger.info(f"Scanning directory: {root_dir} (mode: {mode})")

    # Collect all file paths and apply quick filters
    candidate_files = []
    try:
        for file_path in scan_directory(
            root_dir,
            recursive=recursive,
            max_depth=max_depth,
            follow_symlinks=follow_symlinks,
            exclude_dirs=exclude_dirs,
            include_hidden=include_hidden
        ):
            result.total_files += 1

            try:
                # Check file permissions
                if not os.access(file_path, os.R_OK):
                    result.errors.append(DiscoveryError(
                        file_path=file_path,
                        error_type='permission',
                        message='Permission denied'
                    ))
                    if verbose:
                        logger.warning(f"Permission denied: {file_path}")
                    continue

                # Check for broken symlinks
                if is_broken_symlink(file_path):
                    result.errors.append(DiscoveryError(
                        file_path=file_path,
                        error_type='broken_symlink',
                        message='Broken symlink'
                    ))
                    if verbose:
                        logger.warning(f"Broken symlink: {file_path}")
                    continue

                # Apply symlink scope filtering
                if follow_symlinks and symlink_scope != 'none':
                    resolved = resolve_symlink(file_path, scope=symlink_scope, root_dir=root_dir)
                    if resolved is None:
                        # Symlink should not be followed
                        result.skipped_files.append(file_path)
                        continue

                # Apply extension filters
                _, ext = os.path.splitext(file_path)
                ext_lower = ext.lower()

                if include_extensions and ext_lower not in include_extensions:
                    result.skipped_files.append(file_path)
                    continue

                if exclude_extensions and ext_lower in exclude_extensions:
                    result.skipped_files.append(file_path)
                    continue

                # Apply pattern filters
                rel_path = os.path.relpath(file_path, root_dir)

                if exclude_patterns:
                    if any(fnmatch.fnmatch(rel_path, pat) for pat in exclude_patterns):
                        result.skipped_files.append(file_path)
                        continue

                if include_patterns:
                    if not any(fnmatch.fnmatch(rel_path, pat) for pat in include_patterns):
                        result.skipped_files.append(file_path)
                        continue

                # Apply size filters
                try:
                    file_size = os.path.getsize(file_path)

                    if file_size < min_size_bytes:
                        result.skipped_files.append(file_path)
                        continue

                    if max_size_bytes is not None and file_size > max_size_bytes:
                        result.errors.append(DiscoveryError(
                            file_path=file_path,
                            error_type='size_limit',
                            message=f'File too large ({file_size} bytes)'
                        ))
                        if verbose:
                            logger.warning(f"File too large: {file_path}")
                        continue

                except (OSError, IOError) as e:
                    result.errors.append(DiscoveryError(
                        file_path=file_path,
                        error_type='size_check',
                        message=f'Cannot get file size: {e}',
                        exception=e
                    ))
                    continue

                # File passed all quick filters, add to candidates for binary validation
                candidate_files.append(file_path)

            except Exception as e:
                result.errors.append(DiscoveryError(
                    file_path=file_path,
                    error_type='processing',
                    message=f'Error processing file: {e}',
                    exception=e
                ))
                logger.warning(f"Error processing {file_path}: {e}")
                continue

    except Exception as e:
        logger.error(f"Error scanning directory {root_dir}: {e}")
        raise

    # Perform binary validation
    if use_parallel and len(candidate_files) > 1:
        # Parallel processing
        if verbose:
            logger.info(f"Validating {len(candidate_files)} candidate files in parallel...")

        try:
            # Set global validation options for worker processes
            global _validation_options
            _validation_options = {
                'use_magic_numbers': use_magic_numbers,
                'use_lief_validation': use_lief_validation,
            }

            # Create parallel processor
            processor = ParallelProcessor(max_workers=max_workers)

            # Process files in parallel using module-level function
            parallel_results = processor.process_files(candidate_files, _validate_file_for_binary)

            # Process results
            for pr in parallel_results:
                if pr.success and pr.result:
                    validation_result = pr.result
                    if validation_result.get('is_binary'):
                        # Check if it's an archive file (skip unless explicitly included)
                        if validation_result.get('is_archive') and not include_archives:
                            result.skipped_files.append(validation_result['file_path'])
                            if verbose:
                                logger.debug(f"Skipping archive: {validation_result['file_path']}")
                        else:
                            result.binary_files.append(validation_result['file_path'])
                            if verbose:
                                logger.info(f"Found binary: {validation_result['file_path']}")
                    else:
                        result.skipped_files.append(validation_result['file_path'])
                        if verbose:
                            logger.debug(f"Skipped non-binary: {validation_result['file_path']}")

                    # Check for errors from validation
                    if validation_result.get('error'):
                        error_type = 'permission' if not validation_result.get('has_permission') else (
                            'broken_symlink' if validation_result.get('is_broken_symlink') else 'validation'
                        )
                        result.errors.append(DiscoveryError(
                            file_path=validation_result['file_path'],
                            error_type=error_type,
                            message=validation_result['error']
                        ))
                else:
                    # Parallel processing failed for this file
                    result.errors.append(DiscoveryError(
                        file_path=pr.file_path,
                        error_type='parallel_processing',
                        message=pr.error or 'Unknown parallel processing error'
                    ))

        except Exception as e:
            logger.error(f"Parallel processing error: {e}")
            # Fall back to sequential processing on error
            if verbose:
                logger.info("Falling back to sequential processing due to error")
            use_parallel = False

    # Sequential processing (either by choice or fallback)
    if not use_parallel:
        if verbose and len(candidate_files) > 0:
            logger.info(f"Validating {len(candidate_files)} candidate files sequentially...")

        for file_path in candidate_files:
            try:
                # Check if file is binary
                if is_binary_file(
                    file_path,
                    use_magic_numbers=use_magic_numbers,
                    use_lief_validation=use_lief_validation
                ):
                    # Check if it's an archive file (skip unless explicitly included)
                    file_type = check_magic_number(file_path)
                    if file_type in ('ZIP', 'GZIP', 'BZIP2', 'XZ', 'LZ4', '7Z', 'RAR', 'ISO'):
                        if not include_archives:
                            result.skipped_files.append(file_path)
                            if verbose:
                                logger.debug(f"Skipping archive: {file_path}")
                            continue

                    result.binary_files.append(file_path)
                    if verbose:
                        logger.info(f"Found binary: {file_path}")
                else:
                    result.skipped_files.append(file_path)
                    if verbose:
                        logger.debug(f"Skipped non-binary: {file_path}")

            except Exception as e:
                result.errors.append(DiscoveryError(
                    file_path=file_path,
                    error_type='processing',
                    message=f'Error processing file: {e}',
                    exception=e
                ))
                logger.warning(f"Error processing {file_path}: {e}")
                continue

    if verbose:
        logger.info(
            f"Scan complete: {result.success_count} binaries found, "
            f"{result.skipped_count} files skipped, {result.error_count} errors"
        )

    return result


__all__ = [
    'BINARY_EXTENSIONS',
    'TEXT_EXTENSIONS',
    'DEFAULT_EXCLUDE_DIRS',
    'MAGIC_NUMBERS',
    'DiscoveryError',
    'DiscoveryResult',
    'check_magic_number',
    'validate_with_lief',
    'is_binary_file',
    'is_broken_symlink',
    'resolve_symlink',
    'scan_directory',
    'discover_binaries',
]
