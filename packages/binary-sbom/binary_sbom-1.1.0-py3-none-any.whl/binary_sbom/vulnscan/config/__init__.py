"""
Configuration management for vulnerability scanning.

This package provides configuration loading and management for:
- API keys and credentials
- Rate limit settings
- Cache configuration
- Scanner preferences

Configuration is loaded from multiple sources:
- Environment variables (highest priority)
- Configuration files (JSON format)
- Programmatic configuration

Supported configuration file locations:
- VULNSCAN_CONFIG environment variable
- .vulnscanrc in current directory
- vulnscan.json in current directory
- ~/.vulnscanrc
- ~/.config/vulnscan/config.json

Example:
    >>> from binary_sbom.vulnscan.config import VulnScanConfig, load_config
    >>> config = load_config()
    >>> scanner = VulnScanner(config=config)
"""

from binary_sbom.vulnscan.config.settings import (
    VulnScanConfig,
    check_config_permissions,
    find_config_file,
    load_config,
    load_config_from_file,
)

__all__ = [
    "VulnScanConfig",
    "load_config",
    "find_config_file",
    "load_config_from_file",
    "check_config_permissions",
]
