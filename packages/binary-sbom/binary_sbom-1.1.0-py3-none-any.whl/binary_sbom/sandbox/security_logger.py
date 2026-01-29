"""
Security event logging for sandboxed binary processing.

This module provides utilities for logging security-relevant events during
sandboxed binary processing while ensuring sensitive data is sanitized.

All security events are logged at appropriate levels (INFO, WARNING, ERROR)
with sanitized file paths and contextual information to aid security monitoring
and forensics without exposing sensitive system information.
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional


logger = logging.getLogger(__name__)


def sanitize_path(file_path: str, max_length: int = 100) -> str:
    """
    Sanitize file path for safe logging.

    This function removes sensitive information from file paths while preserving
    enough context for debugging and security monitoring. It:
    - Shows only the filename and parent directory
    - Truncates long paths to prevent log injection
    - Removes absolute paths to hide system structure
    - Preserves relative paths if they're safe

    Args:
        file_path: Original file path.
        max_length: Maximum length for sanitized path (default: 100).

    Returns:
        Sanitized path safe for logging.

    Examples:
        >>> sanitize_path('/home/user/projects/binary_sbom/target/binary')
        '.../binary_sbom/target/binary'
        >>> sanitize_path('/very/long/path/that/exceeds/maximum/length/binary')
        '.../binary'
    """
    # Handle empty or None paths
    if not file_path:
        return "<sanitized_path>"

    try:
        path = Path(file_path)

        # Get filename (always safe to log)
        filename = path.name

        # Handle case where filename is empty
        if not filename:
            return "<sanitized_path>"

        # Get parent directory name for context
        parent = path.parent.name if path.parent.name else ""

        # Combine parent and filename
        if parent:
            sanitized = f".../{parent}/{filename}"
        else:
            sanitized = f".../{filename}"

        # Truncate if necessary
        if len(sanitized) > max_length:
            # Keep just the filename if it's too long
            sanitized = f".../{filename}"[:max_length]

        return sanitized

    except (OSError, ValueError) as e:
        # If path parsing fails, return a safe placeholder
        logger.debug(f"Failed to sanitize path {file_path}: {e}")
        return "<sanitized_path>"


def log_sandbox_spawn(
    pid: int,
    file_path: str,
    resource_limits: Dict[str, int],
    file_size_bytes: Optional[int] = None,
) -> None:
    """
    Log sandbox process spawn event.

    Args:
        pid: Process ID of spawned sandbox.
        file_path: Path to binary being processed (will be sanitized).
        resource_limits: Dictionary of resource limits applied.
        file_size_bytes: Optional file size in bytes.
    """
    sanitized_path = sanitize_path(file_path)

    log_data = {
        "event": "sandbox_spawn",
        "pid": pid,
        "file": sanitized_path,
        "limits": {
            "memory_mb": resource_limits.get("memory_mb", "unknown"),
            "cpu_time_seconds": resource_limits.get("cpu_time_seconds", "unknown"),
            "wall_clock_timeout": resource_limits.get("wall_clock_timeout", "unknown"),
        },
    }

    if file_size_bytes is not None:
        file_size_mb = file_size_bytes / (1024 * 1024)
        log_data["file_size_mb"] = round(file_size_mb, 2)

    logger.info(f"Security: Sandbox spawned - {log_data}")


def log_sandbox_completed(
    pid: int,
    file_path: str,
    resource_usage: Optional[Dict[str, float]] = None,
) -> None:
    """
    Log sandbox process successful completion.

    Args:
        pid: Process ID of completed sandbox.
        file_path: Path to processed binary (will be sanitized).
        resource_usage: Optional resource usage statistics.
    """
    sanitized_path = sanitize_path(file_path)

    log_data = {
        "event": "sandbox_completed",
        "pid": pid,
        "file": sanitized_path,
    }

    if resource_usage:
        log_data["usage"] = {
            "memory_mb": round(resource_usage.get("memory_mb", 0), 2),
            "cpu_time_seconds": round(resource_usage.get("cpu_time_seconds", 0), 2),
        }

    logger.info(f"Security: Sandbox completed successfully - {log_data}")


def log_sandbox_timeout(
    pid: int,
    file_path: str,
    timeout_type: str,
    timeout_value: int,
    elapsed_seconds: Optional[float] = None,
) -> None:
    """
    Log sandbox timeout event.

    Args:
        pid: Process ID of timed-out sandbox.
        file_path: Path to binary being processed (will be sanitized).
        timeout_type: Type of timeout ("wall_clock" or "cpu_time").
        timeout_value: Timeout limit in seconds.
        elapsed_seconds: Optional elapsed time before timeout.
    """
    sanitized_path = sanitize_path(file_path)

    log_data = {
        "event": "sandbox_timeout",
        "pid": pid,
        "file": sanitized_path,
        "timeout_type": timeout_type,
        "timeout_limit_seconds": timeout_value,
    }

    if elapsed_seconds is not None:
        log_data["elapsed_seconds"] = round(elapsed_seconds, 2)

    logger.warning(f"Security: Sandbox timeout - {log_data}")


def log_sandbox_memory_limit(
    pid: int,
    file_path: str,
    memory_limit_mb: int,
    attempted_allocation_mb: Optional[float] = None,
) -> None:
    """
    Log sandbox memory limit violation.

    Args:
        pid: Process ID of sandbox that exceeded memory limit.
        file_path: Path to binary being processed (will be sanitized).
        memory_limit_mb: Memory limit in megabytes.
        attempted_allocation_mb: Optional attempted allocation size.
    """
    sanitized_path = sanitize_path(file_path)

    log_data = {
        "event": "sandbox_memory_limit",
        "pid": pid,
        "file": sanitized_path,
        "memory_limit_mb": memory_limit_mb,
    }

    if attempted_allocation_mb is not None:
        log_data["attempted_allocation_mb"] = round(attempted_allocation_mb, 2)

    logger.warning(f"Security: Memory limit exceeded - {log_data}")


def log_sandbox_terminated(
    pid: int,
    file_path: str,
    termination_type: str,
    exit_code: Optional[int] = None,
    reason: Optional[str] = None,
) -> None:
    """
    Log sandbox process termination event.

    Args:
        pid: Process ID of terminated sandbox.
        file_path: Path to binary being processed (will be sanitized).
        termination_type: Type of termination ("normal", "forced", "crashed").
        exit_code: Optional process exit code.
        reason: Optional reason for termination.
    """
    sanitized_path = sanitize_path(file_path)

    log_data = {
        "event": "sandbox_terminated",
        "pid": pid,
        "file": sanitized_path,
        "termination_type": termination_type,
    }

    if exit_code is not None:
        log_data["exit_code"] = exit_code

    if reason:
        log_data["reason"] = reason

    if termination_type == "forced":
        logger.warning(f"Security: Sandbox forcibly terminated - {log_data}")
    elif termination_type == "crashed":
        logger.error(f"Security: Sandbox crashed - {log_data}")
    else:
        logger.info(f"Security: Sandbox terminated - {log_data}")


def log_security_violation(
    pid: int,
    file_path: str,
    violation_type: str,
    details: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Log security violation event.

    Args:
        pid: Process ID (or None if not spawned yet).
        file_path: Path to binary (will be sanitized).
        violation_type: Type of violation ("symlink", "path_traversal", etc.).
        details: Optional additional details about the violation.
    """
    sanitized_path = sanitize_path(file_path)

    log_data = {
        "event": "security_violation",
        "violation_type": violation_type,
        "file": sanitized_path,
    }

    if pid is not None:
        log_data["pid"] = pid

    if details:
        # Sanitize details dict
        sanitized_details = {}
        for key, value in details.items():
            if key.lower() in ["path", "file", "filename", "directory"]:
                sanitized_details[key] = sanitize_path(str(value))
            elif isinstance(value, str):
                # Truncate long strings to prevent log injection
                sanitized_details[key] = value[:200]
            else:
                sanitized_details[key] = value
        log_data["details"] = sanitized_details

    logger.error(f"Security: Violation detected - {log_data}")


def log_unusual_error(
    pid: Optional[int],
    file_path: str,
    error_type: str,
    error_message: str,
) -> None:
    """
    Log unusual error condition during sandbox processing.

    Args:
        pid: Process ID (or None if not spawned yet).
        file_path: Path to binary (will be sanitized).
        error_type: Type of error.
        error_message: Error message (will be truncated if too long).
    """
    sanitized_path = sanitize_path(file_path)

    # Truncate error message to prevent log injection
    safe_message = error_message[:500] if error_message else ""

    log_data = {
        "event": "sandbox_error",
        "error_type": error_type,
        "file": sanitized_path,
        "message": safe_message,
    }

    if pid is not None:
        log_data["pid"] = pid

    logger.error(f"Security: Unusual error - {log_data}")


def get_sanitized_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize binary metadata for safe logging.

    This function removes potentially sensitive information from parsed
    binary metadata before logging, such as:
    - Full section contents
    - Long dependency lists
    - Specific addresses

    Args:
        metadata: Raw metadata dictionary from LIEF parsing.

    Returns:
        Sanitized metadata safe for logging.
    """
    sanitized = {
        "name": sanitize_path(metadata.get("name", "unknown")),
        "type": metadata.get("type", "unknown"),
        "architecture": metadata.get("architecture", "unknown"),
        "has_entrypoint": metadata.get("entrypoint") is not None,
        "num_sections": len(metadata.get("sections", [])),
        "num_dependencies": len(metadata.get("dependencies", [])),
    }

    return sanitized
