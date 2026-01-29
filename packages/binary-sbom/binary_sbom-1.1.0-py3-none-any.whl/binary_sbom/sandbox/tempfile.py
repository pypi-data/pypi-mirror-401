"""
Temporary file isolation for sandboxed binary processing.

This module manages isolated temporary directories with restrictive
permissions (mode 700) to prevent path traversal and symlink attacks.
"""

import logging
import os
import shutil
import tempfile
from typing import Optional


logger = logging.getLogger(__name__)


class TempDirectory:
    """
    Manage isolated temporary directory for sandboxed processing.

    The temporary directory is created with mode 700 (owner-only access)
    and is automatically cleaned up after use.

    Example:
        >>> temp_dir = TempDirectory()
        >>> path = temp_dir.create()
        >>> isolated_file = temp_dir.copy_file('/input/binary', path)
        >>> # ... use isolated_file in sandbox ...
        >>> temp_dir.cleanup(path)
    """

    def __init__(self, prefix: str = "sandbox_binary_"):
        """
        Initialize TempDirectory manager.

        Args:
            prefix: Prefix for temporary directory name.
        """
        self.prefix = prefix

    def create(self) -> str:
        """
        Create isolated temporary directory.

        Returns:
            Path to temporary directory.

        Raises:
            SandboxFileError: If directory creation fails.
            SandboxSecurityError: If security validation fails.
        """
        try:
            # Create temporary directory
            temp_dir = tempfile.mkdtemp(prefix=self.prefix)

            # Set restrictive permissions (mode 700 - owner only)
            # Note: chmod must be called after creation for Python < 3.11 compatibility
            os.chmod(temp_dir, 0o700)

            # Validate it's not a symlink (security check)
            if os.path.islink(temp_dir):
                os.remove(temp_dir)
                from binary_sbom.sandbox.errors import SandboxSecurityError

                from binary_sbom.sandbox.security_logger import log_security_violation

                log_security_violation(
                    pid=None,
                    file_path=temp_dir,
                    violation_type="symlink",
                    details={"location": "temp_directory_creation"},
                )

                raise SandboxSecurityError(
                    "Temp directory is a symlink - possible security attack",
                    {"path": temp_dir},
                )

            return temp_dir

        except OSError as e:
            from binary_sbom.sandbox.errors import SandboxFileError

            raise SandboxFileError(f"Failed to create temporary directory: {e}") from e

    def copy_file(self, source_path: str, temp_dir: str) -> str:
        """
        Copy file to isolated temporary directory.

        Args:
            source_path: Path to source file.
            temp_dir: Path to temporary directory.

        Returns:
            Path to isolated file.

        Raises:
            SandboxFileError: If copy operation fails.
            SandboxSecurityError: If file validation fails.
        """
        try:
            # Validate source file exists
            if not os.path.isfile(source_path):
                from binary_sbom.sandbox.errors import SandboxFileError

                raise SandboxFileError(f"Source file not found: {source_path}")

            # Check for symlinks
            if os.path.islink(source_path):
                from binary_sbom.sandbox.errors import SandboxSecurityError

                from binary_sbom.sandbox.security_logger import log_security_violation

                log_security_violation(
                    pid=None,
                    file_path=source_path,
                    violation_type="symlink",
                    details={"location": "source_file"},
                )

                raise SandboxSecurityError(
                    "Source file is a symlink - not allowed in sandbox",
                    {"path": source_path},
                )

            # Generate safe filename
            filename = os.path.basename(source_path)

            # Path traversal check - ensure filename doesn't contain .. or path separators
            if ".." in filename or "/" in filename or "\\" in filename:
                from binary_sbom.sandbox.errors import SandboxSecurityError

                from binary_sbom.sandbox.security_logger import log_security_violation

                log_security_violation(
                    pid=None,
                    file_path=source_path,
                    violation_type="path_traversal",
                    details={"filename": filename, "detected_patterns": [".." if ".." in filename else None, "/" if "/" in filename else None, "\\" if "\\" in filename else None]},
                )

                raise SandboxSecurityError(
                    "Path traversal detected in filename",
                    {"filename": filename},
                )

            # Copy to isolated directory
            isolated_path = os.path.join(temp_dir, filename)
            shutil.copy2(source_path, isolated_path)

            # Set restrictive permissions (read-only for owner)
            os.chmod(isolated_path, 0o400)

            return isolated_path

        except (OSError, IOError) as e:
            from binary_sbom.sandbox.errors import SandboxFileError

            raise SandboxFileError(f"Failed to copy file to sandbox: {e}") from e

    def cleanup(self, temp_dir: str) -> None:
        """
        Remove temporary directory and all contents.

        Args:
            temp_dir: Path to temporary directory.
        """
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            # Best-effort cleanup - log error but don't raise
            # (don't mask original errors with cleanup errors)
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to cleanup temp directory {temp_dir}: {e}")
