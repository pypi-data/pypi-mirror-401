"""
Tests for configuration management system.

Tests configuration loading from multiple sources:
- Default values
- Config files (JSON, YAML)
- Environment variables
- CLI arguments
"""

import json
import os
import tempfile
from pathlib import Path

import pytest

# Import configuration modules
from src.binary_sbom.config import (
    Config,
    ProgressConfig,
    create_default_config_file,
    load_config,
    load_config_file,
    load_env_config,
    save_config_file,
)


class TestProgressConfig:
    """Tests for ProgressConfig dataclass."""

    def test_default_values(self):
        """Test default configuration values."""
        config = ProgressConfig()

        assert config.refresh_per_second == 10
        assert config.show_file_metric is True
        assert config.show_elapsed_metric is True
        assert config.show_speed_metric is True
        assert config.show_eta_metric is True
        assert config.dashboard_mode == "full"
        assert config.force_text_mode is False
        assert config.enable_colors is True
        assert config.enable_unicode is True

    def test_custom_values(self):
        """Test custom configuration values."""
        config = ProgressConfig(
            refresh_per_second=5,
            show_file_metric=False,
            show_elapsed_metric=True,
            show_speed_metric=False,
            show_eta_metric=True,
            dashboard_mode="compact",
            force_text_mode=True,
            enable_colors=False,
            enable_unicode=False,
        )

        assert config.refresh_per_second == 5
        assert config.show_file_metric is False
        assert config.show_elapsed_metric is True
        assert config.show_speed_metric is False
        assert config.show_eta_metric is True
        assert config.dashboard_mode == "compact"
        assert config.force_text_mode is True
        assert config.enable_colors is False
        assert config.enable_unicode is False

    def test_validation_refresh_rate_too_low(self):
        """Test validation rejects refresh rate below 1."""
        with pytest.raises(ValueError, match="refresh_per_second must be 1-60"):
            ProgressConfig(refresh_per_second=0)

    def test_validation_refresh_rate_too_high(self):
        """Test validation rejects refresh rate above 60."""
        with pytest.raises(ValueError, match="refresh_per_second must be 1-60"):
            ProgressConfig(refresh_per_second=61)

    def test_validation_invalid_dashboard_mode(self):
        """Test validation rejects invalid dashboard mode."""
        with pytest.raises(ValueError, match="dashboard_mode must be one of"):
            ProgressConfig(dashboard_mode="invalid")

    def test_enabled_metrics_property(self):
        """Test enabled_metrics property returns correct list."""
        config = ProgressConfig(
            show_file_metric=True,
            show_elapsed_metric=False,
            show_speed_metric=True,
            show_eta_metric=False,
        )

        assert config.enabled_metrics == ["file", "speed"]

    def test_to_dict(self):
        """Test conversion to dictionary."""
        config = ProgressConfig(refresh_per_second=15)

        config_dict = config.to_dict()

        assert config_dict["refresh_per_second"] == 15
        assert config_dict["show_file_metric"] is True
        assert "dashboard_mode" in config_dict

    def test_from_dict(self):
        """Test creation from dictionary."""
        config_dict = {
            "refresh_per_second": 20,
            "dashboard_mode": "minimal",
            "show_speed_metric": False,
        }

        config = ProgressConfig.from_dict(config_dict)

        assert config.refresh_per_second == 20
        assert config.dashboard_mode == "minimal"
        assert config.show_speed_metric is False
        # Defaults should be used for missing values
        assert config.show_file_metric is True


class TestConfig:
    """Tests for main Config dataclass."""

    def test_default_values(self):
        """Test default configuration values."""
        config = Config()

        assert config.max_file_size_mb == 100
        assert config.output_format == "json"
        assert isinstance(config.progress, ProgressConfig)

    def test_custom_values(self):
        """Test custom configuration values."""
        progress_config = ProgressConfig(refresh_per_second=5)
        config = Config(
            progress=progress_config,
            max_file_size_mb=200,
            output_format="xml",
        )

        assert config.progress.refresh_per_second == 5
        assert config.max_file_size_mb == 200
        assert config.output_format == "xml"

    def test_validation_max_file_size_invalid(self):
        """Test validation rejects invalid max file size."""
        with pytest.raises(ValueError, match="max_file_size_mb must be > 0"):
            Config(max_file_size_mb=0)

    def test_validation_invalid_output_format(self):
        """Test validation rejects invalid output format."""
        with pytest.raises(ValueError, match="output_format must be 'json' or 'xml'"):
            Config(output_format="invalid")

    def test_to_dict(self):
        """Test conversion to dictionary."""
        config = Config(max_file_size_mb=150)

        config_dict = config.to_dict()

        assert config_dict["max_file_size_mb"] == 150
        assert "progress" in config_dict


class TestConfigFileLoading:
    """Tests for configuration file loading."""

    def test_load_json_config_file(self):
        """Test loading configuration from JSON file."""
        config_data = {
            "progress": {
                "refresh_per_second": 15,
                "dashboard_mode": "compact",
            },
            "max_file_size_mb": 200,
            "output_format": "xml",
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(config_data, f)
            config_path = Path(f.name)

        try:
            result = load_config_file(config_path)

            assert result["refresh_per_second"] == 15
            assert result["dashboard_mode"] == "compact"
            assert result["max_file_size_mb"] == 200
            assert result["output_format"] == "xml"
        finally:
            config_path.unlink()

    def test_load_yaml_config_file(self):
        """Test loading configuration from YAML file."""
        try:
            import yaml
        except ImportError:
            pytest.skip("PyYAML not installed")

        config_content = """
progress:
  refresh_per_second: 20
  dashboard_mode: minimal
  show_speed_metric: false
max_file_size_mb: 300
output_format: json
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as f:
            f.write(config_content)
            config_path = Path(f.name)

        try:
            result = load_config_file(config_path)

            assert result["refresh_per_second"] == 20
            assert result["dashboard_mode"] == "minimal"
            assert result["show_speed_metric"] is False
            assert result["max_file_size_mb"] == 300
            assert result["output_format"] == "json"
        finally:
            config_path.unlink()

    def test_load_nonexistent_file(self):
        """Test loading nonexistent file returns empty dict."""
        result = load_config_file(Path("/nonexistent/config.json"))
        assert result == {}

    def test_load_invalid_json(self):
        """Test loading invalid JSON file returns empty dict with warning."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            f.write("{ invalid json }")
            config_path = Path(f.name)

        try:
            result = load_config_file(config_path)
            # Should return empty dict and log warning
            assert result == {}
        finally:
            config_path.unlink()

    def test_save_json_config_file(self):
        """Test saving configuration to JSON file."""
        config = Config(
            max_file_size_mb=250,
            output_format="xml",
        )

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            config_path = Path(f.name)

        try:
            save_config_file(config, config_path)

            # Verify file was saved correctly
            with open(config_path, "r") as f:
                saved_data = json.load(f)

            assert saved_data["max_file_size_mb"] == 250
            assert saved_data["output_format"] == "xml"
            assert "progress" in saved_data
        finally:
            config_path.unlink()

    def test_save_yaml_config_file(self):
        """Test saving configuration to YAML file."""
        try:
            import yaml
        except ImportError:
            pytest.skip("PyYAML not installed")

        config = Config(
            max_file_size_mb=250,
            output_format="xml",
        )

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as f:
            config_path = Path(f.name)

        try:
            save_config_file(config, config_path)

            # Verify file was saved correctly
            with open(config_path, "r") as f:
                saved_data = yaml.safe_load(f)

            assert saved_data["max_file_size_mb"] == 250
            assert saved_data["output_format"] == "xml"
            assert "progress" in saved_data
        finally:
            config_path.unlink()

    def test_save_unsupported_format(self):
        """Test saving to unsupported format raises error."""
        config = Config()

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            config_path = Path(f.name)

        try:
            with pytest.raises(ValueError, match="Unsupported config file format"):
                save_config_file(config, config_path)
        finally:
            config_path.unlink()


class TestEnvironmentVariableLoading:
    """Tests for environment variable configuration loading."""

    def test_load_refresh_rate_from_env(self, monkeypatch):
        """Test loading refresh rate from environment variable."""
        monkeypatch.setenv("BINARY_SBOM_REFRESH_PER_SECOND", "15")

        result = load_env_config()

        assert result["refresh_per_second"] == 15

    def test_load_dashboard_mode_from_env(self, monkeypatch):
        """Test loading dashboard mode from environment variable."""
        monkeypatch.setenv("BINARY_SBOM_DASHBOARD_MODE", "compact")

        result = load_env_config()

        assert result["dashboard_mode"] == "compact"

    def test_load_show_metrics_from_env(self, monkeypatch):
        """Test loading show metrics flags from environment variables."""
        monkeypatch.setenv("BINARY_SBOM_SHOW_FILE_METRIC", "true")
        monkeypatch.setenv("BINARY_SBOM_SHOW_SPEED_METRIC", "false")

        result = load_env_config()

        assert result["show_file_metric"] is True
        assert result["show_speed_metric"] is False

    def test_load_force_text_mode_from_env(self, monkeypatch):
        """Test loading force text mode from environment variable."""
        monkeypatch.setenv("BINARY_SBOM_FORCE_TEXT_MODE", "true")

        result = load_env_config()

        assert result["force_text_mode"] is True

    def test_load_max_file_size_from_env(self, monkeypatch):
        """Test loading max file size from environment variable."""
        monkeypatch.setenv("BINARY_SBOM_MAX_FILE_SIZE_MB", "500")

        result = load_env_config()

        assert result["max_file_size_mb"] == 500

    def test_invalid_env_value_ignored(self, monkeypatch):
        """Test that invalid environment variable values are ignored."""
        monkeypatch.setenv("BINARY_SBOM_REFRESH_PER_SECOND", "invalid")

        result = load_env_config()

        assert "refresh_per_second" not in result


class TestConfigPriority:
    """Tests for configuration priority: CLI > config file > env > defaults."""

    def test_cli_overrides_config_file(self):
        """Test that CLI arguments override config file values."""
        config_data = {
            "progress": {
                "refresh_per_second": 10,
                "dashboard_mode": "full",
            },
            "max_file_size_mb": 100,
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(config_data, f)
            config_path = Path(f.name)

        try:
            cli_args = {
                "refresh_per_second": 20,
            }

            config = load_config(config_path=config_path, cli_args=cli_args)

            # CLI value should override config file
            assert config.progress.refresh_per_second == 20
            # Config file value should be used for non-CLI values
            assert config.progress.dashboard_mode == "full"
            assert config.max_file_size_mb == 100
        finally:
            config_path.unlink()

    def test_config_file_overrides_env(self, monkeypatch):
        """Test that config file overrides environment variables."""
        monkeypatch.setenv("BINARY_SBOM_REFRESH_PER_SECOND", "15")
        monkeypatch.setenv("BINARY_SBOM_MAX_FILE_SIZE_MB", "200")

        config_data = {
            "progress": {
                "refresh_per_second": 10,
            },
            "max_file_size_mb": 100,
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(config_data, f)
            config_path = Path(f.name)

        try:
            config = load_config(config_path=config_path)

            # Config file should override env
            assert config.progress.refresh_per_second == 10
            assert config.max_file_size_mb == 100
        finally:
            config_path.unlink()

    def test_env_overrides_defaults(self, monkeypatch):
        """Test that environment variables override defaults."""
        monkeypatch.setenv("BINARY_SBOM_REFRESH_PER_SECOND", "25")
        monkeypatch.setenv("BINARY_SBOM_DASHBOARD_MODE", "minimal")

        config = load_config()

        assert config.progress.refresh_per_second == 25
        assert config.progress.dashboard_mode == "minimal"

    def test_full_priority_chain(self, monkeypatch):
        """Test full priority chain: CLI > config file > env > defaults."""
        # Set environment variable
        monkeypatch.setenv("BINARY_SBOM_REFRESH_PER_SECOND", "15")
        monkeypatch.setenv("BINARY_SBOM_MAX_FILE_SIZE_MB", "300")

        # Create config file
        config_data = {
            "progress": {
                "refresh_per_second": 10,
                "dashboard_mode": "compact",
            },
            "max_file_size_mb": 200,
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(config_data, f)
            config_path = Path(f.name)

        try:
            # Set CLI args
            cli_args = {
                "refresh_per_second": 30,
                "dashboard_mode": "minimal",
            }

            config = load_config(config_path=config_path, cli_args=cli_args)

            # CLI should override everything
            assert config.progress.refresh_per_second == 30
            assert config.progress.dashboard_mode == "minimal"

            # Config file should override env
            assert config.max_file_size_mb == 200
        finally:
            config_path.unlink()


class TestCreateDefaultConfigFile:
    """Tests for creating default configuration file."""

    def test_create_default_yaml_config(self):
        """Test creating default YAML config file."""
        try:
            import yaml
        except ImportError:
            pytest.skip("PyYAML not installed")

        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / ".binary_sbom_config.yaml"

            result_path = create_default_config_file(config_path)

            assert result_path == config_path
            assert config_path.exists()

            # Load and verify content
            with open(config_path, "r") as f:
                config_data = yaml.safe_load(f)

            assert "progress" in config_data
            assert config_data["progress"]["refresh_per_second"] == 10

    def test_create_default_json_config(self):
        """Test creating default JSON config file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / ".binary_sbom_config.json"

            result_path = create_default_config_file(config_path)

            assert result_path == config_path
            assert config_path.exists()

            # Load and verify content
            with open(config_path, "r") as f:
                config_data = json.load(f)

            assert "progress" in config_data
            assert config_data["progress"]["refresh_per_second"] == 10


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
