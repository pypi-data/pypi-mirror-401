"""
Configuration management for sandbox resource limits and behavior.

This module provides a centralized configuration system that supports:
1. Configuration files (YAML, TOML, JSON)
2. Environment variables
3. Programmatic configuration
4. Validation with helpful error messages

Priority order (highest to lowest):
1. Programmatic parameters (e.g., SandboxManager(memory_mb=1000))
2. Configuration file
3. Environment variables
4. Default values

Example:
    >>> # Load from file
    >>> config = SandboxConfig.from_file('/path/to/config.yaml')
    >>>
    >>> # Use with manager
    >>> manager = SandboxManager(config=config.to_dict())
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

logger = logging.getLogger(__name__)

# Default configuration values
DEFAULT_CONFIG = {
    "memory_mb": 500,
    "cpu_time_seconds": 30,
    "wall_clock_timeout": 60,
    "max_file_size_mb": 100,
    "enable_security_logging": True,
    "cleanup_on_error": True,
}

# Environment variable mappings
ENV_VAR_MAPPING = {
    "memory_mb": "SANDBOX_MAX_MEMORY_MB",
    "cpu_time_seconds": "SANDBOX_MAX_CPU_TIME",
    "wall_clock_timeout": "SANDBOX_WALL_CLOCK_TIMEOUT",
    "max_file_size_mb": "SANDBOX_MAX_FILE_SIZE_MB",
    "enable_security_logging": "SANDBOX_ENABLE_SECURITY_LOGGING",
    "cleanup_on_error": "SANDBOX_CLEANUP_ON_ERROR",
}


class ConfigValidationError(Exception):
    """Raised when configuration validation fails."""

    pass


class SandboxConfig:
    """
    Sandbox configuration with validation.

    This class handles loading, validating, and managing sandbox configuration
    from multiple sources (files, environment variables, programmatic).

    Example:
        >>> # Load with defaults
        >>> config = SandboxConfig()
        >>>
        >>> # Load from environment
        >>> config = SandboxConfig.from_environment()
        >>>
        >>> # Load from file
        >>> config = SandboxConfig.from_file('sandbox_config.yaml')
        >>>
        >>> # Use with manager
        >>> manager = SandboxManager(config=config.to_dict())
    """

    def __init__(
        self,
        memory_mb: Optional[int] = None,
        cpu_time_seconds: Optional[int] = None,
        wall_clock_timeout: Optional[int] = None,
        max_file_size_mb: Optional[int] = None,
        enable_security_logging: Optional[bool] = None,
        cleanup_on_error: Optional[bool] = None,
    ):
        """
        Initialize sandbox configuration.

        Args:
            memory_mb: Maximum memory in megabytes (default: 500).
            cpu_time_seconds: Maximum CPU time in seconds (default: 30).
            wall_clock_timeout: Wall-clock timeout in seconds (default: 60).
            max_file_size_mb: Maximum file size in MB (default: 100).
            enable_security_logging: Enable security event logging (default: True).
            cleanup_on_error: Cleanup temp files on errors (default: True).
        """
        self.memory_mb = memory_mb if memory_mb is not None else DEFAULT_CONFIG["memory_mb"]
        self.cpu_time_seconds = (
            cpu_time_seconds if cpu_time_seconds is not None else DEFAULT_CONFIG["cpu_time_seconds"]
        )
        self.wall_clock_timeout = (
            wall_clock_timeout
            if wall_clock_timeout is not None
            else DEFAULT_CONFIG["wall_clock_timeout"]
        )
        self.max_file_size_mb = (
            max_file_size_mb
            if max_file_size_mb is not None
            else DEFAULT_CONFIG["max_file_size_mb"]
        )
        self.enable_security_logging = (
            enable_security_logging
            if enable_security_logging is not None
            else DEFAULT_CONFIG["enable_security_logging"]
        )
        self.cleanup_on_error = (
            cleanup_on_error
            if cleanup_on_error is not None
            else DEFAULT_CONFIG["cleanup_on_error"]
        )

        # Validate configuration
        self._validate()

    def _validate(self) -> None:
        """
        Validate configuration values.

        Raises:
            ConfigValidationError: If any configuration value is invalid.
        """
        errors = []

        # Validate memory_mb
        if not isinstance(self.memory_mb, (int, float)) or self.memory_mb <= 0:
            errors.append(
                f"memory_mb must be a positive number, got: {self.memory_mb} ({type(self.memory_mb).__name__})"
            )

        # Validate cpu_time_seconds
        if not isinstance(self.cpu_time_seconds, (int, float)) or self.cpu_time_seconds <= 0:
            errors.append(
                f"cpu_time_seconds must be a positive number, got: {self.cpu_time_seconds} ({type(self.cpu_time_seconds).__name__})"
            )

        # Validate wall_clock_timeout
        if not isinstance(self.wall_clock_timeout, (int, float)) or self.wall_clock_timeout <= 0:
            errors.append(
                f"wall_clock_timeout must be a positive number, got: {self.wall_clock_timeout} ({type(self.wall_clock_timeout).__name__})"
            )

        # Validate max_file_size_mb
        if not isinstance(self.max_file_size_mb, (int, float)) or self.max_file_size_mb <= 0:
            errors.append(
                f"max_file_size_mb must be a positive number, got: {self.max_file_size_mb} ({type(self.max_file_size_mb).__name__})"
            )

        # Validate enable_security_logging
        if not isinstance(self.enable_security_logging, bool):
            errors.append(
                f"enable_security_logging must be a boolean, got: {self.enable_security_logging} ({type(self.enable_security_logging).__name__})"
            )

        # Validate cleanup_on_error
        if not isinstance(self.cleanup_on_error, bool):
            errors.append(
                f"cleanup_on_error must be a boolean, got: {self.cleanup_on_error} ({type(self.cleanup_on_error).__name__})"
            )

        # Validate logical relationships
        if self.wall_clock_timeout < self.cpu_time_seconds:
            logger.warning(
                f"wall_clock_timeout ({self.wall_clock_timeout}s) is less than "
                f"cpu_time_seconds ({self.cpu_time_seconds}s). This may cause premature timeouts."
            )

        # Raise error if validation failed
        if errors:
            raise ConfigValidationError(
                f"Configuration validation failed:\n" + "\n".join(f"  - {error}" for error in errors)
            )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.

        Returns:
            Dictionary with configuration values (only resource limits).
        """
        return {
            "memory_mb": self.memory_mb,
            "cpu_time_seconds": self.cpu_time_seconds,
            "wall_clock_timeout": self.wall_clock_timeout,
        }

    def to_full_dict(self) -> Dict[str, Any]:
        """
        Convert full configuration to dictionary.

        Returns:
            Dictionary with all configuration values including behavioral settings.
        """
        return {
            "memory_mb": self.memory_mb,
            "cpu_time_seconds": self.cpu_time_seconds,
            "wall_clock_timeout": self.wall_clock_timeout,
            "max_file_size_mb": self.max_file_size_mb,
            "enable_security_logging": self.enable_security_logging,
            "cleanup_on_error": self.cleanup_on_error,
        }

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> "SandboxConfig":
        """
        Create SandboxConfig from dictionary.

        Args:
            config: Dictionary with configuration values.

        Returns:
            SandboxConfig instance.

        Raises:
            ConfigValidationError: If configuration is invalid.
        """
        return cls(
            memory_mb=config.get("memory_mb"),
            cpu_time_seconds=config.get("cpu_time_seconds"),
            wall_clock_timeout=config.get("wall_clock_timeout"),
            max_file_size_mb=config.get("max_file_size_mb"),
            enable_security_logging=config.get("enable_security_logging"),
            cleanup_on_error=config.get("cleanup_on_error"),
        )

    @classmethod
    def from_environment(cls) -> "SandboxConfig":
        """
        Load configuration from environment variables.

        Environment variables:
        - SANDBOX_MAX_MEMORY_MB: Memory limit in MB
        - SANDBOX_MAX_CPU_TIME: CPU time limit in seconds
        - SANDBOX_WALL_CLOCK_TIMEOUT: Wall-clock timeout in seconds
        - SANDBOX_MAX_FILE_SIZE_MB: Maximum file size in MB
        - SANDBOX_ENABLE_SECURITY_LOGGING: Enable security logging (true/false)
        - SANDBOX_CLEANUP_ON_ERROR: Cleanup on error (true/false)

        Returns:
            SandboxConfig instance with values from environment variables.
        """
        def parse_bool(env_var: str, default: bool) -> bool:
            """Parse boolean from environment variable."""
            value = os.getenv(env_var)
            if value is None:
                return default
            return value.lower() in ("true", "1", "yes", "on")

        config = cls(
            memory_mb=int(os.getenv("SANDBOX_MAX_MEMORY_MB", DEFAULT_CONFIG["memory_mb"])),
            cpu_time_seconds=int(
                os.getenv("SANDBOX_MAX_CPU_TIME", DEFAULT_CONFIG["cpu_time_seconds"])
            ),
            wall_clock_timeout=int(
                os.getenv("SANDBOX_WALL_CLOCK_TIMEOUT", DEFAULT_CONFIG["wall_clock_timeout"])
            ),
            max_file_size_mb=int(
                os.getenv("SANDBOX_MAX_FILE_SIZE_MB", DEFAULT_CONFIG["max_file_size_mb"])
            ),
            enable_security_logging=parse_bool(
                "SANDBOX_ENABLE_SECURITY_LOGGING", DEFAULT_CONFIG["enable_security_logging"]
            ),
            cleanup_on_error=parse_bool(
                "SANDBOX_CLEANUP_ON_ERROR", DEFAULT_CONFIG["cleanup_on_error"]
            ),
        )

        logger.debug(f"Loaded configuration from environment variables: {config.to_full_dict()}")
        return config

    @classmethod
    def from_file(cls, file_path: Union[str, Path]) -> "SandboxConfig":
        """
        Load configuration from file (YAML, TOML, or JSON).

        Supported file formats:
        - YAML (.yaml, .yml): Requires PyYAML
        - TOML (.toml): Requires tomli or tomllib (Python 3.11+)
        - JSON (.json): Built-in support

        Configuration file format (example):
        ```yaml
        # sandbox_config.yaml
        memory_mb: 500
        cpu_time_seconds: 30
        wall_clock_timeout: 60
        max_file_size_mb: 100
        enable_security_logging: true
        cleanup_on_error: true
        ```

        Args:
            file_path: Path to configuration file.

        Returns:
            SandboxConfig instance.

        Raises:
            FileNotFoundError: If configuration file doesn't exist.
            ConfigValidationError: If file format is unsupported or config is invalid.
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")

        # Determine file format from extension
        suffix = path.suffix.lower()

        try:
            if suffix in (".yaml", ".yml"):
                config_dict = cls._load_yaml(path)
            elif suffix == ".toml":
                config_dict = cls._load_toml(path)
            elif suffix == ".json":
                config_dict = cls._load_json(path)
            else:
                raise ConfigValidationError(
                    f"Unsupported configuration file format: {suffix}. "
                    f"Supported formats: .yaml, .yml, .toml, .json"
                )

            config = cls.from_dict(config_dict)
            logger.info(f"Loaded configuration from file: {file_path}")
            return config

        except Exception as e:
            if isinstance(e, (FileNotFoundError, ConfigValidationError)):
                raise
            raise ConfigValidationError(f"Failed to load configuration from {file_path}: {e}") from e

    @staticmethod
    def _load_yaml(path: Path) -> Dict[str, Any]:
        """Load YAML configuration file."""
        try:
            import yaml

            with open(path, "r") as f:
                return yaml.safe_load(f) or {}
        except ImportError:
            raise ConfigValidationError(
                "PyYAML is required to load .yaml files. "
                "Install it with: pip install pyyaml"
            )

    @staticmethod
    def _load_toml(path: Path) -> Dict[str, Any]:
        """Load TOML configuration file."""
        # Try tomllib first (Python 3.11+)
        try:
            import tomllib

            with open(path, "rb") as f:
                return tomllib.load(f)
        except ImportError:
            pass

        # Fall back to tomli (Python 3.8-3.10)
        try:
            import tomli

            with open(path, "rb") as f:
                return tomli.load(f)
        except ImportError:
            raise ConfigValidationError(
                "tomllib (Python 3.11+) or tomli is required to load .toml files. "
                "Install it with: pip install tomli"
            )

    @staticmethod
    def _load_json(path: Path) -> Dict[str, Any]:
        """Load JSON configuration file."""
        with open(path, "r") as f:
            return json.load(f)

    def save_to_file(self, file_path: Union[str, Path]) -> None:
        """
        Save configuration to file.

        The file format is determined by the file extension:
        - .yaml, .yml: YAML format (requires PyYAML)
        - .toml: TOML format (requires tomli/tomllib)
        - .json: JSON format (built-in)

        Args:
            file_path: Path to save configuration file.

        Raises:
            ConfigValidationError: If file format is unsupported or dependencies missing.
        """
        path = Path(file_path)
        suffix = path.suffix.lower()
        config_dict = self.to_full_dict()

        try:
            if suffix in (".yaml", ".yml"):
                self._save_yaml(path, config_dict)
            elif suffix == ".toml":
                self._save_toml(path, config_dict)
            elif suffix == ".json":
                self._save_json(path, config_dict)
            else:
                raise ConfigValidationError(
                    f"Unsupported configuration file format: {suffix}. "
                    f"Supported formats: .yaml, .yml, .toml, .json"
                )

            logger.info(f"Saved configuration to file: {file_path}")

        except Exception as e:
            if isinstance(e, ConfigValidationError):
                raise
            raise ConfigValidationError(f"Failed to save configuration to {file_path}: {e}") from e

    @staticmethod
    def _save_yaml(path: Path, config_dict: Dict[str, Any]) -> None:
        """Save configuration as YAML."""
        try:
            import yaml

            with open(path, "w") as f:
                yaml.safe_dump(config_dict, f, default_flow_style=False, sort_keys=False)
        except ImportError:
            raise ConfigValidationError(
                "PyYAML is required to save .yaml files. "
                "Install it with: pip install pyyaml"
            )

    @staticmethod
    def _save_toml(path: Path, config_dict: Dict[str, Any]) -> None:
        """Save configuration as TOML."""
        try:
            import tomli_w

            with open(path, "wb") as f:
                tomli_w.dump(config_dict, f)
        except ImportError:
            # Try tomli_w for writing (even with tomllib for reading)
            raise ConfigValidationError(
                "tomli_w is required to save .toml files. "
                "Install it with: pip install tomli_w"
            )

    @staticmethod
    def _save_json(path: Path, config_dict: Dict[str, Any]) -> None:
        """Save configuration as JSON."""
        with open(path, "w") as f:
            json.dump(config_dict, f, indent=2)

    def __repr__(self) -> str:
        """String representation of configuration."""
        return (
            f"SandboxConfig(memory_mb={self.memory_mb}, "
            f"cpu_time_seconds={self.cpu_time_seconds}, "
            f"wall_clock_timeout={self.wall_clock_timeout}, "
            f"max_file_size_mb={self.max_file_size_mb})"
        )


def load_config(
    file_path: Optional[Union[str, Path]] = None,
    use_environment: bool = True,
    **kwargs,
) -> SandboxConfig:
    """
    Load sandbox configuration with configurable priority.

    Priority order (highest to lowest):
    1. Keyword arguments (e.g., memory_mb=1000)
    2. Configuration file (if file_path is provided)
    3. Environment variables (if use_environment is True)
    4. Default values

    Args:
        file_path: Optional path to configuration file.
        use_environment: Whether to load from environment variables (default: True).
        **kwargs: Override configuration values programmatically.

    Returns:
        SandboxConfig instance.

    Example:
        >>> # Load from file with overrides
        >>> config = load_config(
        ...     file_path='sandbox_config.yaml',
        ...     memory_mb=1000  # Override file value
        ... )
        >>>
        >>> # Load from environment with overrides
        >>> config = load_config(memory_mb=1000)
    """
    # Start with defaults or file
    if file_path:
        config = SandboxConfig.from_file(file_path)
    elif use_environment:
        config = SandboxConfig.from_environment()
    else:
        config = SandboxConfig()

    # Apply keyword argument overrides (highest priority)
    if kwargs:
        # Create new config with overrides
        config_dict = config.to_full_dict()
        config_dict.update(kwargs)
        config = SandboxConfig.from_dict(config_dict)

    return config
