"""
End-to-end tests for the binary SBOM generator CLI.

Tests the complete workflow from binary file input to SPDX output using the actual CLI.
"""

import os
import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from binary_sbom.cli import cli


class TestBasicSBOMGeneration:
    """Test basic SBOM generation workflow."""

    @patch('binary_sbom.analyzer._detect_format')
    @patch('binary_sbom.cli.analyze_binary')
    @patch('binary_sbom.cli.write_spdx_file')
    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_e2e_basic_sbom_generation(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package, mock_write, mock_analyze, mock_detect_format
    ):
        """Test complete workflow: binary file → SPDX document."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files within the temporary directory
            temp_input = os.path.join(temp_dir, 'test_input.bin')
            with open(temp_input, 'wb') as f:
                f.write(b'ELF binary content for testing')

            temp_output = os.path.join(temp_dir, 'test_output.json')

            # Set up analyzer mock
            mock_detect_format.return_value = ('ELF', 'EM_X86_64')
            mock_analyze.return_value = {
                'name': 'test_input',
                'type': 'ELF',
                'architecture': 'EM_X86_64',
                'entrypoint': None,
                'sections': [],
                'dependencies': []
            }

            # Set up generator mocks
            mock_package_instance = MagicMock()
            mock_package.return_value = mock_package_instance
            mock_no_assertion.return_value = MagicMock()
            mock_creation_info_instance = MagicMock()
            mock_creation_info.return_value = mock_creation_info_instance
            mock_doc_instance = MagicMock()
            mock_document.return_value = mock_doc_instance

            # Execute CLI command
            result = runner.invoke(cli, [
                '--input', temp_input,
                '--output', temp_output,
                '--format', 'json',
                '--allow-dir', temp_dir
            ])

            # Verify CLI execution
            assert result.exit_code == 0, f"CLI failed: {result.output}"

            # Verify the workflow completed
            mock_package.assert_called_once()
            mock_document.assert_called_once()
            mock_write.assert_called_once()

            # Verify output file path is shown
            assert temp_output in result.output

    @patch('binary_sbom.analyzer._detect_format')
    @patch('binary_sbom.cli.analyze_binary')
    @patch('binary_sbom.cli.write_spdx_file')
    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_e2e_minimal_binary_workflow(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package, mock_write, mock_analyze, mock_detect_format
    ):
        """Test workflow with minimal binary (no sections, no dependencies)."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files within the temporary directory
            temp_input = os.path.join(temp_dir, 'test_input.bin')
            with open(temp_input, 'wb') as f:
                f.write(b'minimal binary')

            temp_output = os.path.join(temp_dir, 'test_output.json')

            # Set up analyzer mock - Raw format for minimal binary
            mock_detect_format.return_value = ('Raw', 'unknown')
            mock_analyze.return_value = {
                'name': 'temp',
                'type': 'Raw',
                'architecture': 'unknown',
                'entrypoint': None,
                'sections': [],
                'dependencies': []
            }

            # Set up generator mocks
            mock_package.return_value = MagicMock()
            mock_no_assertion.return_value = MagicMock()
            mock_creation_info.return_value = MagicMock()
            mock_document.return_value = MagicMock()

            # Execute CLI command
            result = runner.invoke(cli, [
                '--input', temp_input,
                '--output', temp_output,
                '--allow-dir', temp_dir
            ])

            # Verify workflow completed successfully
            assert result.exit_code == 0


class TestFormatSpecification:
    """Test output format specification in E2E workflow."""

    @patch('binary_sbom.analyzer._detect_format')
    @patch('binary_sbom.cli.analyze_binary')
    @patch('binary_sbom.cli.write_spdx_file')
    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_e2e_json_output(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package, mock_write, mock_analyze, mock_detect_format
    ):
        """Test complete workflow ending in JSON output."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files within the temporary directory
            temp_input = os.path.join(temp_dir, 'test_input.bin')
            with open(temp_input, 'wb') as f:
                f.write(b'binary for json')

            temp_output = os.path.join(temp_dir, 'test_output.json')

            # Set up mocks
            mock_detect_format.return_value = ('ELF', 'EM_X86_64')
            mock_analyze.return_value = {
                'name': 'temp',
                'type': 'ELF',
                'architecture': 'EM_X86_64',
                'entrypoint': None,
                'sections': [],
                'dependencies': []
            }

            mock_package.return_value = MagicMock()
            mock_no_assertion.return_value = MagicMock()
            mock_creation_info.return_value = MagicMock()
            mock_document.return_value = MagicMock()

            # Execute CLI command with JSON format
            result = runner.invoke(cli, [
                '--input', temp_input,
                '--output', temp_output,
                '--format', 'json',
                '--allow-dir', temp_dir
            ])

            assert result.exit_code == 0
            # Verify write was called
            mock_write.assert_called_once()

    @patch('binary_sbom.analyzer._detect_format')
    @patch('binary_sbom.cli.analyze_binary')
    @patch('binary_sbom.cli.write_spdx_file')
    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_e2e_xml_output(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package, mock_write, mock_analyze, mock_detect_format
    ):
        """Test complete workflow ending in XML output."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files within the temporary directory
            temp_input = os.path.join(temp_dir, 'test_input.bin')
            with open(temp_input, 'wb') as f:
                f.write(b'binary for xml')

            temp_output = os.path.join(temp_dir, 'test_output.xml')

            # Set up mocks
            mock_detect_format.return_value = ('PE', 'IMAGE_FILE_MACHINE_AMD64')
            mock_analyze.return_value = {
                'name': 'temp',
                'type': 'PE',
                'architecture': 'IMAGE_FILE_MACHINE_AMD64',
                'entrypoint': None,
                'sections': [],
                'dependencies': []
            }

            mock_package.return_value = MagicMock()
            mock_no_assertion.return_value = MagicMock()
            mock_creation_info.return_value = MagicMock()
            mock_document.return_value = MagicMock()

            # Execute CLI command with XML format
            result = runner.invoke(cli, [
                '--input', temp_input,
                '--output', temp_output,
                '--format', 'xml',
                '--allow-dir', temp_dir
            ])

            assert result.exit_code == 0
            # Verify write was called
            mock_write.assert_called_once()

    @patch('binary_sbom.analyzer._detect_format')
    @patch('binary_sbom.cli.analyze_binary')
    @patch('binary_sbom.cli.write_spdx_file')
    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_e2e_yaml_output(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package, mock_write, mock_analyze, mock_detect_format
    ):
        """Test complete workflow ending in YAML output."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files within the temporary directory
            temp_input = os.path.join(temp_dir, 'test_input.bin')
            with open(temp_input, 'wb') as f:
                f.write(b'binary for yaml')

            temp_output = os.path.join(temp_dir, 'test_output.yaml')

            # Set up mocks
            mock_detect_format.return_value = ('MachO', 'CPU_TYPE_ARM64')
            mock_analyze.return_value = {
                'name': 'temp',
                'type': 'MachO',
                'architecture': 'CPU_TYPE_ARM64',
                'entrypoint': None,
                'sections': [],
                'dependencies': []
            }

            mock_package.return_value = MagicMock()
            mock_no_assertion.return_value = MagicMock()
            mock_creation_info.return_value = MagicMock()
            mock_document.return_value = MagicMock()

            # Execute CLI command with YAML format
            result = runner.invoke(cli, [
                '--input', temp_input,
                '--output', temp_output,
                '--format', 'yaml',
                '--allow-dir', temp_dir
            ])

            assert result.exit_code == 0
            # Verify write was called
            mock_write.assert_called_once()

    @patch('binary_sbom.analyzer._detect_format')
    @patch('binary_sbom.cli.analyze_binary')
    @patch('binary_sbom.cli.write_spdx_file')
    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_e2e_tag_value_output(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package, mock_write, mock_analyze, mock_detect_format
    ):
        """Test complete workflow ending in Tag-Value output."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files within the temporary directory
            temp_input = os.path.join(temp_dir, 'test_input.bin')
            with open(temp_input, 'wb') as f:
                f.write(b'binary for tag-value')

            temp_output = os.path.join(temp_dir, 'test_output.spdx')

            # Set up mocks
            mock_detect_format.return_value = ('Raw', 'unknown')
            mock_analyze.return_value = {
                'name': 'temp',
                'type': 'Raw',
                'architecture': 'unknown',
                'entrypoint': None,
                'sections': [],
                'dependencies': []
            }

            mock_package.return_value = MagicMock()
            mock_no_assertion.return_value = MagicMock()
            mock_creation_info.return_value = MagicMock()
            mock_document.return_value = MagicMock()

            # Execute CLI command with Tag-Value format
            result = runner.invoke(cli, [
                '--input', temp_input,
                '--output', temp_output,
                '--format', 'tag-value',
                '--allow-dir', temp_dir
            ])

            assert result.exit_code == 0
            # Verify write was called
            mock_write.assert_called_once()


class TestVerboseMode:
    """Test verbose mode in E2E workflow."""

    @patch('binary_sbom.analyzer._detect_format')
    @patch('binary_sbom.cli.analyze_binary')
    @patch('binary_sbom.cli.write_spdx_file')
    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_e2e_verbose_mode_shows_progress(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package, mock_write, mock_analyze, mock_detect_format
    ):
        """Test that verbose mode displays detailed progress messages."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files within the temporary directory
            temp_input = os.path.join(temp_dir, 'test_input.bin')
            with open(temp_input, 'wb') as f:
                f.write(b'verbose mode test')

            temp_output = os.path.join(temp_dir, 'test_output.json')

            # Set up mocks
            mock_detect_format.return_value = ('ELF', 'EM_X86_64')
            mock_analyze.return_value = {
                'name': 'temp',
                'type': 'ELF',
                'architecture': 'EM_X86_64',
                'entrypoint': None,
                'sections': [],
                'dependencies': []
            }

            mock_package.return_value = MagicMock()
            mock_no_assertion.return_value = MagicMock()
            mock_creation_info.return_value = MagicMock()
            mock_document.return_value = MagicMock()

            # Execute CLI command with verbose flag
            result = runner.invoke(cli, [
                '--input', temp_input,
                '--output', temp_output,
                '--verbose',
                '--allow-dir', temp_dir
            ])

            # Verify success
            assert result.exit_code == 0

            # Verify verbose progress messages
            assert 'Analyzing binary file' in result.output
            assert 'Binary Type:' in result.output or 'Architecture:' in result.output
            assert 'Creating SPDX document' in result.output
            assert 'Writing SBOM' in result.output

    @patch('binary_sbom.analyzer._detect_format')
    @patch('binary_sbom.cli.analyze_binary')
    @patch('binary_sbom.cli.write_spdx_file')
    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_e2e_non_verbose_mode_minimal_output(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package, mock_write, mock_analyze, mock_detect_format
    ):
        """Test that non-verbose mode shows minimal output."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files within the temporary directory
            temp_input = os.path.join(temp_dir, 'test_input.bin')
            with open(temp_input, 'wb') as f:
                f.write(b'non-verbose test')

            temp_output = os.path.join(temp_dir, 'test_output.json')

            # Set up mocks
            mock_detect_format.return_value = ('ELF', 'EM_X86_64')
            mock_analyze.return_value = {
                'name': 'temp',
                'type': 'ELF',
                'architecture': 'EM_X86_64',
                'entrypoint': None,
                'sections': [],
                'dependencies': []
            }

            mock_package.return_value = MagicMock()
            mock_no_assertion.return_value = MagicMock()
            mock_creation_info.return_value = MagicMock()
            mock_document.return_value = MagicMock()

            # Execute CLI command without verbose flag
            result = runner.invoke(cli, [
                '--input', temp_input,
                '--output', temp_output,
                '--allow-dir', temp_dir
            ])

            # Verify success
            assert result.exit_code == 0

            # Verify minimal output (no verbose messages)
            assert 'Analyzing binary file' not in result.output
            assert 'Creating SPDX document' not in result.output
            assert 'Writing SBOM' not in result.output

            # Should only show output file path
            assert temp_output in result.output


class TestErrorHandling:
    """Test error handling in E2E workflow."""

    def test_e2e_non_existent_file_error(self):
        """Test that non-existent input file produces clear error."""
        runner = CliRunner()

        result = runner.invoke(cli, [
            '--input', '/nonexistent/path/to/file.bin',
            '--output', 'test.json'
        ])

        # Should fail
        assert result.exit_code != 0

        # Should show clear error message
        assert 'does not exist' in result.output or 'Error' in result.output

    def test_e2e_missing_input_argument(self):
        """Test that missing --input argument produces helpful error."""
        runner = CliRunner()

        result = runner.invoke(cli, ['--output', 'test.json'])

        # Should fail
        assert result.exit_code != 0

        # Should show helpful message
        assert 'Missing option' in result.output or '--input' in result.output

    def test_e2e_missing_output_argument(self):
        """Test that missing --output argument produces helpful error."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_input = os.path.join(temp_dir, 'test_input.bin')
            with open(temp_input, 'wb') as f:
                f.write(b'test input')

            result = runner.invoke(cli, [
                '--input', temp_input,
                '--allow-dir', temp_dir
            ])

            # Should fail
            assert result.exit_code != 0

            # Should show helpful message
            assert 'Missing option' in result.output or '--output' in result.output

    def test_e2e_invalid_format_choice(self):
        """Test that invalid format choice produces helpful error."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_input = os.path.join(temp_dir, 'test_input.bin')
            with open(temp_input, 'wb') as f:
                f.write(b'test input')

            temp_output = os.path.join(temp_dir, 'test.out')

            result = runner.invoke(cli, [
                '--input', temp_input,
                '--output', temp_output,
                '--format', 'invalid-format',
                '--allow-dir', temp_dir
            ])

            # Should fail
            assert result.exit_code != 0

            # Should show valid choices
            assert 'Invalid value' in result.output or 'json' in result.output


class TestHelpDisplay:
    """Test help display functionality."""

    def test_e2e_help_displays_usage_information(self):
        """Test that --help displays comprehensive usage information."""
        runner = CliRunner()

        result = runner.invoke(cli, ['--help'])

        # Should succeed
        assert result.exit_code == 0

        # Should show usage information
        assert 'Usage:' in result.output or 'binary-sbom' in result.output

        # Should document all options
        assert '--input' in result.output or '-i' in result.output
        assert '--output' in result.output or '-o' in result.output
        assert '--format' in result.output or '-f' in result.output
        assert '--verbose' in result.output or '-v' in result.output

        # Should show description
        assert 'SBOM' in result.output or 'binary' in result.output

    def test_e2e_help_shows_examples(self):
        """Test that help includes usage examples."""
        runner = CliRunner()

        result = runner.invoke(cli, ['--help'])

        # Should show examples or help text
        assert 'Generate' in result.output or 'binary' in result.output


class TestMultipleBinaryFormats:
    """Test E2E workflow with different binary formats."""

    @patch('binary_sbom.analyzer._detect_format')
    @patch('binary_sbom.cli.analyze_binary')
    @patch('binary_sbom.cli.write_spdx_file')
    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_e2e_elf_binary_workflow(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package, mock_write, mock_analyze, mock_detect_format
    ):
        """Test complete workflow with ELF binary format."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files within the temporary directory
            temp_input = os.path.join(temp_dir, 'test_input.elf')
            with open(temp_input, 'wb') as f:
                f.write(b'ELF binary')

            temp_output = os.path.join(temp_dir, 'test_output.json')

            # Set up ELF binary mock
            mock_detect_format.return_value = ('ELF', 'EM_X86_64')
            mock_analyze.return_value = {
                'name': 'temp',
                'type': 'ELF',
                'architecture': 'EM_X86_64',
                'entrypoint': None,
                'sections': [],
                'dependencies': []
            }

            mock_package.return_value = MagicMock()
            mock_no_assertion.return_value = MagicMock()
            mock_creation_info.return_value = MagicMock()
            mock_document.return_value = MagicMock()

            # Execute CLI
            result = runner.invoke(cli, [
                '--input', temp_input,
                '--output', temp_output,
                '--verbose',
                '--allow-dir', temp_dir
            ])

            assert result.exit_code == 0
            assert 'ELF' in result.output

    @patch('binary_sbom.analyzer._detect_format')
    @patch('binary_sbom.cli.analyze_binary')
    @patch('binary_sbom.cli.write_spdx_file')
    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_e2e_pe_binary_workflow(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package, mock_write, mock_analyze, mock_detect_format
    ):
        """Test complete workflow with PE binary format."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files within the temporary directory
            temp_input = os.path.join(temp_dir, 'test_input.exe')
            with open(temp_input, 'wb') as f:
                f.write(b'PE binary')

            temp_output = os.path.join(temp_dir, 'test_output.json')

            # Set up PE binary mock
            mock_detect_format.return_value = ('PE', 'IMAGE_FILE_MACHINE_AMD64')
            mock_analyze.return_value = {
                'name': 'temp',
                'type': 'PE',
                'architecture': 'IMAGE_FILE_MACHINE_AMD64',
                'entrypoint': None,
                'sections': [],
                'dependencies': []
            }

            mock_package.return_value = MagicMock()
            mock_no_assertion.return_value = MagicMock()
            mock_creation_info.return_value = MagicMock()
            mock_document.return_value = MagicMock()

            # Execute CLI
            result = runner.invoke(cli, [
                '--input', temp_input,
                '--output', temp_output,
                '--verbose',
                '--allow-dir', temp_dir
            ])

            assert result.exit_code == 0
            assert 'PE' in result.output

    @patch('binary_sbom.analyzer._detect_format')
    @patch('binary_sbom.cli.analyze_binary')
    @patch('binary_sbom.cli.write_spdx_file')
    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_e2e_macho_binary_workflow(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package, mock_write, mock_analyze, mock_detect_format
    ):
        """Test complete workflow with MachO binary format."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files within the temporary directory
            temp_input = os.path.join(temp_dir, 'test_input.dylib')
            with open(temp_input, 'wb') as f:
                f.write(b'MachO binary')

            temp_output = os.path.join(temp_dir, 'test_output.json')

            # Set up MachO binary mock
            mock_detect_format.return_value = ('MachO', 'CPU_TYPE_ARM64')
            mock_analyze.return_value = {
                'name': 'temp',
                'type': 'MachO',
                'architecture': 'CPU_TYPE_ARM64',
                'entrypoint': None,
                'sections': [],
                'dependencies': []
            }

            mock_package.return_value = MagicMock()
            mock_no_assertion.return_value = MagicMock()
            mock_creation_info.return_value = MagicMock()
            mock_document.return_value = MagicMock()

            # Execute CLI
            result = runner.invoke(cli, [
                '--input', temp_input,
                '--output', temp_output,
                '--verbose',
                '--allow-dir', temp_dir
            ])

            assert result.exit_code == 0
            assert 'MachO' in result.output

    @patch('binary_sbom.analyzer._detect_format')
    @patch('binary_sbom.cli.analyze_binary')
    @patch('binary_sbom.cli.write_spdx_file')
    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_e2e_raw_binary_workflow(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package, mock_write, mock_analyze, mock_detect_format
    ):
        """Test complete workflow with raw binary format (fallback)."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files within the temporary directory
            temp_input = os.path.join(temp_dir, 'test_input.bin')
            with open(temp_input, 'wb') as f:
                f.write(b'raw binary content')

            temp_output = os.path.join(temp_dir, 'test_output.json')

            # Set up raw binary mock
            mock_detect_format.return_value = ('Raw', 'unknown')
            mock_analyze.return_value = {
                'name': 'temp',
                'type': 'Raw',
                'architecture': 'unknown',
                'entrypoint': None,
                'sections': [],
                'dependencies': []
            }

            mock_package.return_value = MagicMock()
            mock_no_assertion.return_value = MagicMock()
            mock_creation_info.return_value = MagicMock()
            mock_document.return_value = MagicMock()

            # Execute CLI
            result = runner.invoke(cli, [
                '--input', temp_input,
                '--output', temp_output,
                '--verbose',
                '--allow-dir', temp_dir
            ])

            assert result.exit_code == 0
            assert 'Raw' in result.output
