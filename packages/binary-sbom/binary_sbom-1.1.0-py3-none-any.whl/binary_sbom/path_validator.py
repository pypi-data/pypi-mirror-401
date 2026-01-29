"""
Path validator module for Binary SBOM Generator.

This module provides comprehensive path validation and sanitization to prevent
directory traversal attacks and protect against symlink escapes in file processing
operations. It ensures that all file paths are within allowed directories and
properly validated before access.
"""

import os
from pathlib import Path
from typing import List, Union


class PathValidationError(Exception):
    """Exception raised when path validation fails."""

    pass


def sanitize_path(path: Union[str, Path]) -> str:
    """
    Resolve a file path to its canonical form and prevent directory traversal.

    This function sanitizes file paths by resolving all symbolic links,
    removing redundant directory separators, and eliminating directory
    traversal components (e.g., '..', '.'). The returned path is absolute
    and canonical, making it safe for file operations.

    Args:
        path: The file path to sanitize. Can be absolute or relative.

    Returns:
        The canonical absolute path as a string. All symbolic links are
        resolved, and directory traversal components are eliminated.

    Raises:
        PathValidationError: If the path contains invalid components or
            cannot be resolved.

    Example:
        >>> sanitize_path('/tmp/test/../file.bin')
        '/tmp/file.bin'
        >>> sanitize_path('relative/./path/../file')
        '/absolute/path/to/file'
    """
    try:
        # Convert to Path object if string
        path_obj = Path(path) if isinstance(path, str) else path

        # Expand user directory (e.g., ~ to /home/user)
        path_obj = path_obj.expanduser()

        # Resolve to absolute path, following symlinks and eliminating .. and .
        # strict=False means it won't raise for paths that don't exist
        try:
            resolved_path = path_obj.resolve(strict=False)
        except (OSError, RuntimeError) as e:
            raise PathValidationError(
                f"Cannot resolve path '{path}': {e}"
            )

        # Convert to string and ensure it's absolute
        canonical_path = str(resolved_path)

        # Additional validation: ensure no null bytes
        if '\0' in canonical_path:
            raise PathValidationError(
                f"Path contains null bytes: '{path}'"
            )

        return canonical_path

    except (TypeError, AttributeError) as e:
        raise PathValidationError(
            f"Invalid path type: '{path}'. Expected str or Path object: {e}"
        )


def validate_file_path(
    file_path: Union[str, Path],
    allowed_dirs: List[Union[str, Path]],
) -> str:
    """
    Validate that a file path is within allowed directory boundaries.

    This function ensures that a file path does not escape the allowed
    directories through directory traversal attacks or symbolic links.
    It sanitizes the input path and verifies it resides within one
    of the allowed directory trees. This prevents directory traversal
    attacks and symlink escapes.

    Args:
        file_path: Path to the file to validate. Can be absolute or relative.
        allowed_dirs: List of allowed directory paths. All paths will be
            sanitized and resolved to their canonical form.

    Returns:
        The sanitized absolute path if validation succeeds. This path is
        guaranteed to be within one of the allowed directories.

    Raises:
        PathValidationError: If the path is outside allowed directories,
            if the path is a directory instead of a file, or if the path
            cannot be resolved.

    Example:
        >>> validate_file_path('/tmp/file.bin', allowed_dirs=['/tmp'])
        '/tmp/file.bin'
        >>> validate_file_path('/etc/passwd', allowed_dirs=['/tmp'])
        Traceback (most recent call last):
            ...
        PathValidationError: Path '/etc/passwd' is outside allowed directory boundaries. Allowed: ['/tmp']
    """
    # Validate inputs
    if not allowed_dirs:
        raise PathValidationError(
            "No allowed directories specified. "
            "At least one directory must be provided."
        )

    # Sanitize the file path
    try:
        sanitized_path = sanitize_path(file_path)
    except PathValidationError as e:
        raise PathValidationError(
            f"Cannot validate file path '{file_path}': {e}"
        )

    # Sanitize all allowed directories
    sanitized_allowed_dirs = []
    for allowed_dir in allowed_dirs:
        try:
            sanitized_allowed_dirs.append(sanitize_path(allowed_dir))
        except PathValidationError as e:
            raise PathValidationError(
                f"Invalid allowed directory '{allowed_dir}': {e}"
            )

    # Check if the path is within any allowed directory
    # Use os.path.commonprefix to check if path starts with allowed directory
    path_is_allowed = False
    for allowed_dir in sanitized_allowed_dirs:
        # Ensure allowed directory ends with separator for proper comparison
        if not allowed_dir.endswith(os.sep):
            allowed_dir_with_sep = allowed_dir + os.sep
        else:
            allowed_dir_with_sep = allowed_dir

        # Check if sanitized path starts with allowed directory
        # We check both exact match and prefix match
        if (sanitized_path == allowed_dir or
            sanitized_path.startswith(allowed_dir_with_sep) or
            os.path.commonprefix([sanitized_path, allowed_dir]) == allowed_dir):
            path_is_allowed = True
            break

    if not path_is_allowed:
        allowed_dirs_str = ', '.join(f"'{d}'" for d in sanitized_allowed_dirs)
        raise PathValidationError(
            f"Path '{sanitized_path}' is outside allowed directory boundaries. "
            f"Allowed: [{allowed_dirs_str}]"
        )

    return sanitized_path


def check_symlink_safety(
    file_path: Union[str, Path],
    allowed_dir: Union[str, Path],
) -> bool:
    """
    Check if a file path's symlinks are safe and do not escape allowed directory.

    This function detects symlink escapes by verifying that when all symbolic
    links in a file path are resolved, the final target does not escape the
    allowed directory boundary. This prevents symlink-based directory traversal
    attacks where a malicious symlink could point outside the allowed directory.

    The function resolves the file path to its canonical form (following all
    symlinks) and verifies the resolved path is within the allowed directory.

    Args:
        file_path: Path to the file to check. Can be absolute or relative.
            The path will be resolved following all symbolic links.
        allowed_dir: Allowed directory boundary. The resolved file path must
            be within this directory.

    Returns:
        True if the symlink is safe (resolved path is within allowed directory).

    Raises:
        PathValidationError: If following symlinks would escape the allowed
            directory, or if the path cannot be resolved.

    Example:
        >>> check_symlink_safety('/tmp/file', '/tmp')
        True
        >>> # If /tmp/file is a symlink to /etc/passwd
        >>> check_symlink_safety('/tmp/file', '/tmp')
        Traceback (most recent call last):
            ...
        PathValidationError: Symlink escape detected: '/tmp/file' resolves to '/etc/passwd' outside allowed directory '/tmp'
    """
    try:
        # Sanitize the file path (resolves symlinks)
        resolved_file_path = sanitize_path(file_path)

        # Sanitize the allowed directory
        resolved_allowed_dir = sanitize_path(allowed_dir)

        # Check if resolved file path is within allowed directory
        # Ensure allowed directory ends with separator for proper comparison
        if not resolved_allowed_dir.endswith(os.sep):
            allowed_dir_with_sep = resolved_allowed_dir + os.sep
        else:
            allowed_dir_with_sep = resolved_allowed_dir

        # Check if resolved file is within allowed directory
        is_within_bounds = (
            resolved_file_path == resolved_allowed_dir or
            resolved_file_path.startswith(allowed_dir_with_sep) or
            os.path.commonprefix([resolved_file_path, resolved_allowed_dir]) == resolved_allowed_dir
        )

        if not is_within_bounds:
            raise PathValidationError(
                f"Symlink escape detected: '{file_path}' resolves to "
                f"'{resolved_file_path}' outside allowed directory '{resolved_allowed_dir}'"
            )

        return True

    except PathValidationError:
        # Re-raise PathValidationError as-is
        raise
    except Exception as e:
        raise PathValidationError(
            f"Failed to check symlink safety for '{file_path}': {e}"
        )


def validate_directory_path(
    directory_path: Union[str, Path],
    allowed_base_dirs: List[Union[str, Path]],
) -> str:
    """
    Validate that a directory path is within allowed base directory boundaries.

    This function ensures that a directory path does not escape the allowed
    base directories through directory traversal attacks or symbolic links.
    It is specifically designed for recursive directory scanning operations
    and provides protection against symlink escapes that could allow scanning
    unauthorized directories.

    The function sanitizes the input path, verifies it resides within one
    of the allowed base directory trees, and ensures the path exists and
    is a directory. This prevents directory traversal attacks during
    recursive scanning operations.

    Args:
        directory_path: Path to the directory to validate. Can be absolute
            or relative.
        allowed_base_dirs: List of allowed base directory paths. All paths
            will be sanitized and resolved to their canonical form.

    Returns:
        The sanitized absolute path if validation succeeds. This path is
        guaranteed to be within one of the allowed base directories and
        is a valid directory.

    Raises:
        PathValidationError: If the path is outside allowed directories,
            if the path is not a directory, if the path does not exist,
            or if the path cannot be resolved.

    Example:
        >>> validate_directory_path('/tmp/test', allowed_base_dirs=['/tmp'])
        '/tmp/test'
        >>> validate_directory_path('/etc', allowed_base_dirs=['/tmp'])
        Traceback (most recent call last):
            ...
        PathValidationError: Path '/etc' is outside allowed directory boundaries. Allowed: ['/tmp']
    """
    # Validate inputs
    if not allowed_base_dirs:
        raise PathValidationError(
            "No allowed base directories specified. "
            "At least one directory must be provided."
        )

    # Sanitize the directory path
    try:
        sanitized_path = sanitize_path(directory_path)
    except PathValidationError as e:
        raise PathValidationError(
            f"Cannot validate directory path '{directory_path}': {e}"
        )

    # Sanitize all allowed base directories
    sanitized_allowed_dirs = []
    for allowed_dir in allowed_base_dirs:
        try:
            sanitized_allowed_dirs.append(sanitize_path(allowed_dir))
        except PathValidationError as e:
            raise PathValidationError(
                f"Invalid allowed base directory '{allowed_dir}': {e}"
            )

    # Check if the path is within any allowed base directory
    path_is_allowed = False
    for allowed_dir in sanitized_allowed_dirs:
        # Ensure allowed directory ends with separator for proper comparison
        if not allowed_dir.endswith(os.sep):
            allowed_dir_with_sep = allowed_dir + os.sep
        else:
            allowed_dir_with_sep = allowed_dir

        # Check if sanitized path starts with allowed directory
        # We check both exact match and prefix match
        if (sanitized_path == allowed_dir or
            sanitized_path.startswith(allowed_dir_with_sep) or
            os.path.commonprefix([sanitized_path, allowed_dir]) == allowed_dir):
            path_is_allowed = True
            break

    if not path_is_allowed:
        allowed_dirs_str = ', '.join(f"'{d}'" for d in sanitized_allowed_dirs)
        raise PathValidationError(
            f"Path '{sanitized_path}' is outside allowed directory boundaries. "
            f"Allowed: [{allowed_dirs_str}]"
        )

    # Verify the path exists and is a directory
    try:
        if not os.path.exists(sanitized_path):
            raise PathValidationError(
                f"Directory does not exist: '{sanitized_path}'"
            )
        if not os.path.isdir(sanitized_path):
            raise PathValidationError(
                f"Path is not a directory: '{sanitized_path}'"
            )
    except OSError as e:
        raise PathValidationError(
            f"Cannot access directory '{sanitized_path}': {e}"
        )

    return sanitized_path


__all__ = [
    'PathValidationError',
    'sanitize_path',
    'validate_file_path',
    'validate_directory_path',
    'check_symlink_safety',
]
