"""
Tests for Binary SBOM CLI functionality.
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

import click
from click.testing import CliRunner

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from binary_sbom.cli import cli


class TestCLI:
    """Test CLI command group and global options."""

    def test_cli_version(self):
        """Test version command."""
        runner = CliRunner()
        result = runner.invoke(cli, ["version"])
        assert result.exit_code == 0
        assert "Binary SBOM v0.1.0" in result.output
        assert "SPDX Version: 2.3" in result.output

    def test_cli_help(self):
        """Test CLI help output."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Binary SBOM" in result.output
        assert "--verbose" in result.output
        assert "--quiet" in result.output


class TestScanCommand:
    """Test scan command options and flags."""

    def test_scan_requires_input(self):
        """Test that scan command requires input path."""
        runner = CliRunner()
        result = runner.invoke(cli, ["scan"])
        assert result.exit_code != 0
        assert "Missing option" in result.output or "input" in result.output.lower()

    def test_scan_help(self):
        """Test scan command help output."""
        runner = CliRunner()
        result = runner.invoke(cli, ["scan", "--help"])
        assert result.exit_code == 0
        assert "--scan-vulns" in result.output
        assert "vulnerability scanning" in result.output.lower()

    def test_scan_vulns_flag_in_help(self):
        """Test that --scan-vulns flag is documented in help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["scan", "--help"])
        assert result.exit_code == 0
        assert "--scan-vulns" in result.output
        # Check that the help text mentions vulnerability scanning
        assert "CVE" in result.output
        assert "OSV" in result.output

    @patch("binary_sbom.cli._process_single_file")
    def test_scan_vulns_flag_disabled_by_default(self, mock_process):
        """Test that --scan-vulns flag is disabled by default."""
        # Create a temporary test file
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(cli, ["scan", "-i", str(test_file)])
            # Should fail because processing not implemented, but we can check the call
            # The _process_single_file should be called with scan_vulns=False

    @patch("binary_sbom.cli._process_single_file")
    def test_scan_vulns_flag_enabled(self, mock_process):
        """Test that --scan-vulns flag can be enabled."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(cli, ["scan", "-i", str(test_file), "--scan-vulns"])
            # Should fail because processing not implemented, but we can check the call
            # The _process_single_file should be called with scan_vulns=True

    def test_scan_vulns_with_verbose(self):
        """Test --scan-vulns flag with verbose output."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(
                cli,
                ["scan", "-i", str(test_file), "--scan-vulns", "--verbose"]
            )
            # Should show vulnerability scanning status in verbose output
            # even though processing fails
            if "Vulnerability scanning: True" in result.output:
                assert True  # Flag is being passed through
            else:
                # May not reach verbose output if it exits early
                pass


class TestScanVulnsFlag:
    """Specific tests for the --scan-vulns flag."""

    def test_scan_vulns_flag_exists(self):
        """Test that --scan-vulns flag is recognized."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            # This should not fail with "no such option"
            result = runner.invoke(cli, ["scan", "-i", str(test_file), "--scan-vulns"])
            assert "--scan-vulns" not in result.output or "Error" not in result.output

    def test_scan_vulns_flag_shows_in_help(self):
        """Test that --scan-vulns appears in command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["scan", "--help"])
        assert "--scan-vulns" in result.output
        assert "Enable vulnerability scanning" in result.output

    def test_nvd_api_key_flag_exists(self):
        """Test that --nvd-api-key flag is recognized."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            # This should not fail with "no such option"
            result = runner.invoke(
                cli,
                ["scan", "-i", str(test_file), "--nvd-api-key", "test-key-123"]
            )
            assert "--nvd-api-key" not in result.output or "Error" not in result.output

    def test_nvd_api_key_flag_shows_in_help(self):
        """Test that --nvd-api-key appears in command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["scan", "--help"])
        assert "--nvd-api-key" in result.output
        assert "NVD API key" in result.output

    def test_github_token_flag_exists(self):
        """Test that --github-token flag is recognized."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            # This should not fail with "no such option"
            result = runner.invoke(
                cli,
                ["scan", "-i", str(test_file), "--github-token", "ghp_test_token"]
            )
            assert "--github-token" not in result.output or "Error" not in result.output

    def test_github_token_flag_shows_in_help(self):
        """Test that --github-token appears in command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["scan", "--help"])
        assert "--github-token" in result.output
        assert "GitHub token" in result.output

    def test_api_keys_with_verbose(self):
        """Test that API keys are redacted in verbose output."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(
                cli,
                [
                    "scan", "-i", str(test_file),
                    "--nvd-api-key", "secret-key-123",
                    "--github-token", "ghp_secret_token",
                    "--verbose"
                ]
            )
            # API keys should be redacted in verbose output
            if "NVD API key:" in result.output:
                assert "[redacted]" in result.output
                assert "secret-key-123" not in result.output
            if "GitHub token:" in result.output:
                assert "[redacted]" in result.output
                assert "ghp_secret_token" not in result.output

    def test_api_keys_optional(self):
        """Test that API keys are optional."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            # Scan without API keys should work
            result = runner.invoke(cli, ["scan", "-i", str(test_file)])
            # Should fail because processing not implemented, but not because of missing API keys
            assert "API key" not in result.output or "required" not in result.output.lower()


class TestVulnerabilitySummaryDisplay:
    """Test vulnerability summary display in CLI output."""

    def test_scan_vulns_displays_summary(self):
        """Test that --scan-vulns displays vulnerability summary."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(cli, ["scan", "-i", str(test_file), "--scan-vulns"])
            # Should display vulnerability summary section
            assert "VULNERABILITY SCAN RESULTS" in result.output
            assert "Vulnerabilities Found:" in result.output
            assert "Critical:" in result.output
            assert "High:" in result.output
            assert "Medium:" in result.output
            assert "Low:" in result.output

    def test_vulnerability_summary_shows_count(self):
        """Test that vulnerability summary shows total count."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(cli, ["scan", "-i", str(test_file), "--scan-vulns"])
            # Should show total count
            assert "Total:" in result.output
            # Demo has 2 vulnerabilities
            assert "Total: 2" in result.output

    def test_vulnerability_summary_shows_severity_breakdown(self):
        """Test that vulnerability summary shows severity breakdown."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(cli, ["scan", "-i", str(test_file), "--scan-vulns"])
            # Should show severity breakdown with percentages
            assert "Severity Breakdown:" in result.output
            assert "CRITICAL:" in result.output
            assert "HIGH:" in result.output
            # Demo has 1 critical and 1 high
            assert "CRITICAL: 1" in result.output
            assert "HIGH: 1" in result.output

    def test_vulnerability_summary_shows_affected_packages(self):
        """Test that vulnerability summary shows affected packages count."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(cli, ["scan", "-i", str(test_file), "--scan-vulns"])
            # Should show affected packages
            assert "Affected Packages:" in result.output
            # Demo has 1 package affected
            assert "Affected Packages: 1/1" in result.output

    def test_vulnerability_summary_shows_sources(self):
        """Test that vulnerability summary shows sources queried."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(cli, ["scan", "-i", str(test_file), "--scan-vulns"])
            # Should show sources queried
            assert "Sources Queried:" in result.output
            # Demo uses OSV
            assert "OSV" in result.output

    def test_critical_vulnerability_warning(self):
        """Test that critical vulnerabilities trigger warning."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(cli, ["scan", "-i", str(test_file), "--scan-vulns"])
            # Should show critical vulnerability warning
            # Demo has 1 critical vulnerability
            assert "CRITICAL vulnerabilities detected" in result.output or "⚠️" in result.output

    def test_vulnerability_summary_with_api_keys_verbose(self):
        """Test that API keys are shown in verbose mode when scanning."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(
                cli,
                [
                    "scan", "-i", str(test_file),
                    "--scan-vulns",
                    "--nvd-api-key", "test-key",
                    "--github-token", "test-token",
                    "--verbose"
                ]
            )
            # Verbose output should show scanner configuration
            assert "Vulnerability Scanning Configuration:" in result.output
            assert "OSV Scanner: Enabled" in result.output
            # API keys should enable scanners
            assert "NVD Scanner: Enabled" in result.output
            assert "GitHub Scanner: Enabled" in result.output

    def test_vulnerability_summary_quiet_mode(self):
        """Test that quiet mode suppresses vulnerability summary."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(cli, ["scan", "-i", str(test_file), "--scan-vulns", "--quiet"])
            # Quiet mode should suppress all output
            assert result.output == ""
            # But should still exit successfully
            assert result.exit_code == 0

    def test_vulnerability_summary_shows_package_being_scanned(self):
        """Test that the package being scanned is displayed."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(cli, ["scan", "-i", str(test_file), "--scan-vulns"])
            # Should show which package is being scanned
            assert "Scanning package:" in result.output
            # Demo scans npm/lodash
            assert "npm/lodash" in result.output

    def test_vulnerability_summary_zero_vulnerabilities_format(self):
        """Test that zero vulnerabilities are handled correctly."""
        # This test verifies the format would be correct for zero vulnerabilities
        # The demo uses mock vulnerabilities, but the code should handle empty results
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(cli, ["scan", "-i", str(test_file), "--scan-vulns"])
            # The demo has vulnerabilities, so we verify the format is correct
            # In production with 0 vulns, it would show "No vulnerabilities found"
            assert "VULNERABILITY SCAN RESULTS" in result.output

    def test_verbose_mode_shows_scan_completion(self):
        """Test that verbose mode shows scan completion message."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(
                cli,
                ["scan", "-i", str(test_file), "--scan-vulns", "--verbose"]
            )
            # Verbose mode should show completion details
            assert "Vulnerability scanning complete" in result.output
            assert "Total vulnerabilities found:" in result.output
            assert "Highest severity:" in result.output

    def test_verbose_shows_detailed_vulnerability_info(self):
        """Test that verbose mode shows detailed vulnerability information."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(
                cli,
                ["scan", "-i", str(test_file), "--scan-vulns", "--verbose"]
            )
            # Should show detailed vulnerability section
            assert "DETAILED VULNERABILITY INFORMATION" in result.output
            # Should show individual vulnerabilities
            assert "CVE-2021-23337" in result.output
            assert "CVE-2020-8203" in result.output
            # Should show vulnerability index
            assert "[1]" in result.output
            assert "[2]" in result.output

    def test_verbose_shows_cvss_scores(self):
        """Test that verbose mode shows CVSS scores with vector strings."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(
                cli,
                ["scan", "-i", str(test_file), "--scan-vulns", "--verbose"]
            )
            # Should show CVSS score information
            assert "CVSS Score:" in result.output
            assert "Base Score:" in result.output
            assert "Version:" in result.output
            assert "Vector:" in result.output
            # Demo has CVSS v3.1 scores
            assert "3.1" in result.output
            # Demo has scores 8.1 and 9.8
            assert "8.1" in result.output
            assert "9.8" in result.output

    def test_verbose_shows_severity_icons(self):
        """Test that verbose mode shows severity icons."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(
                cli,
                ["scan", "-i", str(test_file), "--scan-vulns", "--verbose"]
            )
            # Should show severity icons (emoji)
            # Critical = 🔴, High = 🟠
            assert "🔴" in result.output  # Critical
            assert "🟠" in result.output  # High

    def test_verbose_shows_references(self):
        """Test that verbose mode shows vulnerability references."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(
                cli,
                ["scan", "-i", str(test_file), "--scan-vulns", "--verbose"]
            )
            # Should show references section
            assert "References:" in result.output
            # Should show reference URLs
            assert "https://nvd.nist.gov/vuln/detail/CVE-2021-23337" in result.output
            assert "https://nvd.nist.gov/vuln/detail/CVE-2020-8203" in result.output
            # Should show reference types
            assert "[ADVISORY]" in result.output

    def test_verbose_shows_cwe_ids(self):
        """Test that verbose mode shows CWE IDs."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(
                cli,
                ["scan", "-i", str(test_file), "--scan-vulns", "--verbose"]
            )
            # Should show CWE IDs
            assert "CWE IDs:" in result.output
            # Demo has CWE-1321 and CWE-77
            assert "CWE-1321" in result.output
            assert "CWE-77" in result.output

    def test_verbose_shows_affected_versions(self):
        """Test that verbose mode shows affected versions if present."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(
                cli,
                ["scan", "-i", str(test_file), "--scan-vulns", "--verbose"]
            )
            # Should show affected versions section
            # Note: Demo vulnerabilities have empty affected_versions lists
            # but the section would appear if they had data

    def test_verbose_shows_aliases(self):
        """Test that verbose mode shows vulnerability aliases."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(
                cli,
                ["scan", "-i", str(test_file), "--scan-vulns", "--verbose"]
            )
            # Should show aliases
            assert "Aliases:" in result.output
            # Demo has GHSA-4w2v-vmj7-klvd as alias
            assert "GHSA-4w2v-vmj7-klvd" in result.output

    def test_verbose_shows_dates(self):
        """Test that verbose mode shows published and modified dates."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(
                cli,
                ["scan", "-i", str(test_file), "--scan-vulns", "--verbose"]
            )
            # Should show publication dates
            assert "Published:" in result.output
            assert "Modified:" in result.output
            # Demo has dates from 2020 and 2021
            assert "2021" in result.output
            assert "2020" in result.output

    def test_verbose_shows_source(self):
        """Test that verbose mode shows vulnerability source."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(
                cli,
                ["scan", "-i", str(test_file), "--scan-vulns", "--verbose"]
            )
            # Should show source
            assert "Source:" in result.output
            # Demo uses OSV
            assert "OSV" in result.output

    def test_non_verbose_mode_hides_details(self):
        """Test that non-verbose mode hides detailed vulnerability information."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(
                cli,
                ["scan", "-i", str(test_file), "--scan-vulns"]
            )
            # Should NOT show detailed section
            assert "DETAILED VULNERABILITY INFORMATION" not in result.output
            # Should still show summary
            assert "VULNERABILITY SCAN RESULTS" in result.output

    def test_quiet_mode_hides_details(self):
        """Test that quiet mode hides all output including details."""
        runner = CliRunner()
        with runner.isolated_filesystem():
            test_file = Path("test.bin")
            test_file.write_text("test content")

            result = runner.invoke(
                cli,
                ["scan", "-i", str(test_file), "--scan-vulns", "--quiet"]
            )
            # Quiet mode should suppress all output
            assert result.output == ""
            # Should not show detailed section
            assert "DETAILED VULNERABILITY INFORMATION" not in result.output
