"""
Configuration module for Binary SBOM Generator.

This module handles loading and managing configuration settings from YAML files
and environment variables, with sensible defaults for all options.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import yaml  # noqa: F401
except ImportError:
    yaml = None  # type: ignore[assignment]  # pragma: no cover


DEFAULT_CONFIG: Dict[str, Any] = {
    'output_format': 'json',
    'log_level': 'INFO',
    'temp_dir': None,
    'max_file_size_mb': 100,
}


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from YAML file or use defaults.

    This function searches for configuration files in the following order:
    1. Path provided via config_path parameter
    2. Environment variable BINARY_SBOM_CONFIG
    3. Current directory (.binary-sbom.yml)
    4. Home directory (~/.binary-sbom.yml)

    If no configuration file is found, returns DEFAULT_CONFIG.
    User configuration values override DEFAULT_CONFIG values.

    Args:
        config_path: Optional path to configuration file.

    Returns:
        Dictionary containing merged configuration (user config + defaults).

    Raises:
        ValueError: If configuration file exists but contains invalid YAML.

    Example:
        >>> config = load_config()
        >>> config['output_format']
        'json'
        >>> config = load_config('/path/to/config.yml')
    """
    if config_path is None:
        config_path = _find_config_file()

    if config_path and Path(config_path).exists():
        if yaml is None:
            raise ImportError(
                "PyYAML is required to load configuration files. "
                "Install it with: pip install pyyaml"
            )

        try:
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in configuration file {config_path}: {e}")

        # Merge user config with defaults (user config takes precedence)
        return {**DEFAULT_CONFIG, **user_config}

    return DEFAULT_CONFIG.copy()


def _find_config_file() -> Optional[str]:
    """
    Search for config file in standard locations.

    Searches in the following order:
    1. Environment variable BINARY_SBOM_CONFIG
    2. Current directory (.binary-sbom.yml)
    3. Home directory (~/.binary-sbom.yml)

    Returns:
        Path to configuration file if found, None otherwise.

    Example:
        >>> path = _find_config_file()
        >>> if path:
        ...     print(f"Found config at: {path}")
    """
    # Check environment variable
    env_path = os.getenv('BINARY_SBOM_CONFIG')
    if env_path:
        return env_path

    # Check current directory
    if Path('.binary-sbom.yml').exists():
        return '.binary-sbom.yml'

    # Check home directory
    home_config = Path.home() / '.binary-sbom.yml'
    if home_config.exists():
        return str(home_config)

    return None


__all__ = [
    'DEFAULT_CONFIG',
    'load_config',
    '_find_config_file',
]
