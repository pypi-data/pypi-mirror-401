"""
Configuration management for vulnerability scanning.

This module provides configuration loading from multiple sources:
- Environment variables
- Configuration files (JSON format)
- Programmatic configuration

Configuration is loaded in the following order (later sources override earlier ones):
1. Default values
2. Configuration file (if found)
3. Environment variables
4. Programmatic arguments (highest priority)

Configuration file search locations (in order):
1. Path specified by VULNSCAN_CONFIG environment variable
2. .vulnscanrc in current directory
3. vulnscan.json in current directory
4. ~/.vulnscanrc
5. ~/.config/vulnscan/config.json

Example:
    >>> from binary_sbom.vulnscan.config import load_config
    >>> config = load_config()
    >>> config.nvd_api_key  # Loaded from env or config file
    'your-api-key'
"""

from __future__ import annotations

import json
import os
import stat
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# Configuration file search paths (in order)
CONFIG_SEARCH_PATHS = [
    ".vulnscanrc",
    "vulnscan.json",
    "~/.vulnscanrc",
    "~/.config/vulnscan/config.json",
]

# Sensitive configuration keys (should not be logged)
SENSITIVE_KEYS = {"nvd_api_key", "github_token"}


@dataclass
class VulnScanConfig:
    """
    Configuration for vulnerability scanning.

    Attributes:
        enabled: Whether vulnerability scanning is enabled
        nvd_api_key: Optional NVD API key (loaded from NVD_API_KEY env var)
        github_token: Optional GitHub personal access token (loaded from GITHUB_TOKEN env var)
        osv_timeout: OSV API timeout in seconds
        nvd_timeout: NVD API timeout in seconds
        github_timeout: GitHub API timeout in seconds
        cache_enabled: Whether to enable caching
        cache_ttl: Cache time-to-live in seconds
        max_retries: Maximum number of API request retries
        retry_delay: Delay between retries in seconds
        config_file: Path to configuration file (if loaded from file)

    Example:
        >>> config = VulnScanConfig(
        ...     enabled=True,
        ...     nvd_api_key=os.getenv("NVD_API_KEY"),
        ...     github_token=os.getenv("GITHUB_TOKEN")
        ... )
    """

    enabled: bool = True
    nvd_api_key: str | None = None
    github_token: str | None = None
    osv_timeout: int = 30
    nvd_timeout: int = 30
    github_timeout: int = 30
    cache_enabled: bool = True
    cache_ttl: int = 3600  # 1 hour
    max_retries: int = 3
    retry_delay: float = 1.0
    config_file: str | None = field(default=None, repr=False, compare=False)

    def __post_init__(self):
        """Validate and load credentials from environment."""
        # Load credentials from environment (environment overrides config file)
        nvd_key = os.getenv("NVD_API_KEY")
        if nvd_key:
            self.nvd_api_key = nvd_key

        github_token = os.getenv("GITHUB_TOKEN")
        if github_token:
            self.github_token = github_token

        # Validate configuration
        self._validate()

    def _validate(self) -> None:
        """
        Validate configuration values.

        Raises:
            ValueError: If configuration values are invalid
        """
        if self.osv_timeout <= 0:
            raise ValueError(f"osv_timeout must be positive, got {self.osv_timeout}")

        if self.nvd_timeout <= 0:
            raise ValueError(f"nvd_timeout must be positive, got {self.nvd_timeout}")

        if self.github_timeout <= 0:
            raise ValueError(f"github_timeout must be positive, got {self.github_timeout}")

        if self.cache_ttl <= 0:
            raise ValueError(f"cache_ttl must be positive, got {self.cache_ttl}")

        if self.max_retries < 0:
            raise ValueError(f"max_retries must be non-negative, got {self.max_retries}")

        if self.retry_delay < 0:
            raise ValueError(f"retry_delay must be non-negative, got {self.retry_delay}")

    def redacted(self) -> dict[str, Any]:
        """
        Return configuration dictionary with sensitive values redacted.

        Useful for logging and debugging without exposing credentials.

        Returns:
            Dictionary with sensitive values replaced by "***"

        Example:
            >>> config = VulnScanConfig(nvd_api_key="secret123")
            >>> safe_dict = config.redacted()
            >>> safe_dict["nvd_api_key"]
            '***'
        """
        result = {}
        for key, value in self.__dict__.items():
            if key in SENSITIVE_KEYS and value:
                result[key] = "***"
            else:
                result[key] = value
        return result

    def to_dict(self) -> dict[str, Any]:
        """
        Convert configuration to dictionary (with sensitive values redacted).

        Returns:
            Dictionary representation of configuration

        Example:
            >>> config = VulnScanConfig(enabled=True)
            >>> config_dict = config.to_dict()
            >>> config_dict["enabled"]
            True
        """
        return self.redacted()


def find_config_file(custom_path: str | None = None) -> Path | None:
    """
    Search for configuration file in standard locations.

    Search order:
    1. Custom path (if provided)
    2. VULNSCAN_CONFIG environment variable
    3. .vulnscanrc in current directory
    4. vulnscan.json in current directory
    5. ~/.vulnscanrc
    6. ~/.config/vulnscan/config.json

    Args:
        custom_path: Optional custom configuration file path

    Returns:
        Path to configuration file, or None if not found

    Example:
        >>> config_path = find_config_file()
        >>> if config_path:
        ...     print(f"Using config: {config_path}")
    """
    # Check custom path first
    if custom_path:
        path = Path(custom_path)
        if path.exists() and path.is_file():
            return path
        return None

    # Check VULNSCAN_CONFIG environment variable
    env_path = os.getenv("VULNSCAN_CONFIG")
    if env_path:
        path = Path(env_path).expanduser()
        if path.exists() and path.is_file():
            return path

    # Search standard locations
    for config_path in CONFIG_SEARCH_PATHS:
        path = Path(config_path).expanduser()
        if path.exists() and path.is_file():
            return path

    return None


def check_config_permissions(config_path: Path) -> None:
    """
    Check that configuration file has secure permissions.

    Configuration files containing API keys should have restrictive
    permissions (user read/write only, i.e., 0600 or more restrictive).

    Args:
        config_path: Path to configuration file

    Raises:
        PermissionError: If configuration file has insecure permissions

    Example:
        >>> config_path = Path("~/.vulnscanrc").expanduser()
        >>> try:
        ...     check_config_permissions(config_path)
        ... except PermissionError as e:
        ...     print(f"Warning: {e}")
    """
    if not config_path.exists():
        return

    stat_info = config_path.stat()
    mode = stat_info.st_mode

    # Check if group or others have read/write permissions
    if mode & (stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH):
        # Only check files that might contain sensitive data
        # (files in home directory or explicitly named config files)
        config_str = str(config_path)
        if ("vulnscan" in config_str.lower() or
            config_path.home() in config_path.parents or
            config_path == config_path.home()):
            raise PermissionError(
                f"Configuration file {config_path} has insecure permissions. "
                f"Please restrict permissions to user-only (chmod 600)."
            )


def load_config_from_file(config_path: Path) -> dict[str, Any]:
    """
    Load configuration from JSON file.

    Args:
        config_path: Path to configuration file

    Returns:
        Configuration dictionary

    Raises:
        ValueError: If configuration file is invalid
        PermissionError: If configuration file has insecure permissions
        json.JSONDecodeError: If configuration file is not valid JSON

    Example:
        >>> config_path = Path("~/.vulnscanrc").expanduser()
        >>> config_dict = load_config_from_file(config_path)
        >>> config_dict["enabled"]
        True
    """
    # Check file permissions
    check_config_permissions(config_path)

    # Load and parse JSON
    try:
        with open(config_path, "r") as f:
            config_data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in configuration file {config_path}: {e}")

    # Validate that it's a dictionary
    if not isinstance(config_data, dict):
        raise ValueError(
            f"Configuration file {config_path} must contain a JSON object, "
            f"got {type(config_data).__name__}"
        )

    return config_data


def load_config(
    config_dict: dict[str, Any] | None = None,
    config_file: str | None = None,
) -> VulnScanConfig:
    """
    Load vulnerability scanning configuration from multiple sources.

    Configuration is loaded in the following order (later sources override earlier ones):
    1. Default values
    2. Configuration file (if found)
    3. Provided config_dict (if any)

    Environment variables always take precedence over all sources.

    Args:
        config_dict: Optional configuration dictionary (overrides config file)
        config_file: Optional path to configuration file

    Returns:
        VulnScanConfig object

    Raises:
        ValueError: If configuration values are invalid
        PermissionError: If configuration file has insecure permissions

    Example:
        >>> # Load from default locations
        >>> config = load_config()

        >>> # Load from custom file
        >>> config = load_config(config_file="/path/to/config.json")

        >>> # Load with programmatic overrides
        >>> config = load_config(config_dict={"enabled": False})
    """
    # Start with empty configuration
    final_config: dict[str, Any] = {}

    # Load from configuration file (if found)
    if config_file:
        # Use specified config file
        config_path = Path(config_file).expanduser()
        if config_path.exists():
            file_config = load_config_from_file(config_path)
            final_config.update(file_config)
            final_config["config_file"] = str(config_path)
    else:
        # Search for config file in standard locations
        config_path = find_config_file()
        if config_path:
            file_config = load_config_from_file(config_path)
            final_config.update(file_config)
            final_config["config_file"] = str(config_path)

    # Apply programmatic overrides (highest priority after env vars)
    if config_dict:
        final_config.update(config_dict)

    # Create configuration object (environment variables are applied in __post_init__)
    return VulnScanConfig(**final_config)
