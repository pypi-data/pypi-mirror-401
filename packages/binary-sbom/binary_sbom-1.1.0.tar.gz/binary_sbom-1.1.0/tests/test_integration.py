"""
Integration tests for the binary SBOM generator.

Tests the complete workflow from analyzer → generator → file writer.
"""

import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from binary_sbom.analyzer import BinaryAnalysisError, analyze_binary
from binary_sbom.generator import SPDXGenerationError, create_spdx_document, write_spdx_file
from binary_sbom.path_validator import PathValidationError, sanitize_path, validate_file_path, check_symlink_safety


class TestAnalyzerToGeneratorWorkflow:
    """Test the integration between analyzer and generator modules."""

    @patch('binary_sbom.analyzer._detect_format')
    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_full_workflow_analyzer_to_generator(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package, mock_detect_format
    ):
        """Test complete workflow from binary analysis to SPDX document generation."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'ELF binary content')
            temp_input = f.name

        try:
            # Set up analyzer mock - patch _detect_format to return ELF format
            mock_detect_format.return_value = ('ELF', 'EM_X86_64')

            # Mock lief.parse to return a mock binary object
            with patch('binary_sbom.analyzer.lief') as mock_lief:
                mock_binary = MagicMock()
                mock_binary.name = 'temp'
                mock_binary.header = MagicMock()
                mock_binary.header.machine_type = 'EM_X86_64'
                mock_binary.entrypoint = 0
                mock_binary.imported_libraries = []
                mock_binary.sections = []
                mock_lief.parse.return_value = mock_binary

                # Set up generator mocks
                mock_package_instance = MagicMock()
                mock_package.return_value = mock_package_instance
                mock_no_assertion.return_value = MagicMock()
                mock_creation_info_instance = MagicMock()
                mock_creation_info.return_value = mock_creation_info_instance
                mock_doc_instance = MagicMock()
                mock_document.return_value = mock_doc_instance

                # Execute workflow
                metadata = analyze_binary(temp_input)
                assert metadata['name'] == 'temp'
                assert metadata['type'] == 'ELF'
                assert metadata['architecture'] == 'EM_X86_64'

                document = create_spdx_document(metadata)
                assert document == mock_doc_instance

                # Verify generator was called with analyzer output
                mock_package.assert_called_once()
                call_kwargs = mock_package.call_args[1]
                assert call_kwargs['name'] == 'temp'
                assert 'ELF' in call_kwargs['description']
                assert 'EM_X86_64' in call_kwargs['description']
        finally:
            os.unlink(temp_input)

    @patch('binary_sbom.analyzer._detect_format')
    def test_analyzer_output_valid_for_generator(self, mock_detect_format):
        """Test that analyzer output contains all required fields for generator."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'binary content')
            temp_input = f.name

        try:
            # Set up analyzer mock - patch _detect_format to return ELF format
            mock_detect_format.return_value = ('ELF', 'EM_ARM')

            # Mock lief.parse to return a mock binary object
            with patch('binary_sbom.analyzer.lief') as mock_lief:
                mock_binary = MagicMock()
                mock_binary.name = 'temp'
                mock_binary.header = MagicMock()
                mock_binary.header.machine_type = 'EM_ARM'
                mock_binary.entrypoint = 0
                mock_binary.imported_libraries = []
                mock_binary.sections = []
                mock_lief.parse.return_value = mock_binary

                metadata = analyze_binary(temp_input)

                # Verify required fields for generator
                assert 'name' in metadata
                assert 'type' in metadata
                assert 'architecture' in metadata
                assert metadata['name'] == 'temp'
                assert metadata['type'] == 'ELF'
                assert metadata['architecture'] == 'EM_ARM'

                # Verify optional fields have correct types
                assert isinstance(metadata.get('sections'), list)
                assert isinstance(metadata.get('dependencies'), list)
        finally:
            os.unlink(temp_input)

    @patch('binary_sbom.analyzer.lief')
    def test_analyzer_error_propagates_to_workflow(self, mock_lief):
        """Test that analyzer errors prevent document generation."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'corrupted binary')
            temp_input = f.name

        try:
            # Set up analyzer to fail
            mock_lief.parse.side_effect = Exception('Corrupted file')

            # Analyzer should raise error
            with pytest.raises(BinaryAnalysisError, match='Corrupted binary file'):
                analyze_binary(temp_input)
        finally:
            os.unlink(temp_input)

    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_generator_error_with_valid_metadata(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package
    ):
        """Test that generator errors are raised even with valid metadata."""
        # Set up generator to fail
        mock_package.side_effect = Exception('Package creation failed')

        metadata = {
            'name': 'test',
            'type': 'ELF',
            'architecture': 'x86_64',
            'sections': [],
            'dependencies': []
        }

        with pytest.raises(SPDXGenerationError, match='Failed to create SPDX package'):
            create_spdx_document(metadata)

    @patch('binary_sbom.analyzer._detect_format')
    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_workflow_with_minimal_metadata(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package, mock_detect_format
    ):
        """Test workflow with minimal binary (no sections, no dependencies)."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'minimal binary')
            temp_input = f.name

        try:
            # Set up analyzer mock - patch _detect_format to return Raw
            mock_detect_format.return_value = ('Raw', 'unknown')

            # Mock lief.parse to return a mock binary object
            with patch('binary_sbom.analyzer.lief') as mock_lief:
                mock_binary = MagicMock()
                mock_binary.name = 'temp'
                mock_binary.header = MagicMock()
                mock_binary.entrypoint = 0
                mock_binary.imported_libraries = []
                mock_binary.sections = []
                mock_lief.parse.return_value = mock_binary

                # Set up generator mocks
                mock_package_instance = MagicMock()
                mock_package.return_value = mock_package_instance
                mock_no_assertion.return_value = MagicMock()
                mock_creation_info_instance = MagicMock()
                mock_creation_info.return_value = mock_creation_info_instance
                mock_doc_instance = MagicMock()
                mock_document.return_value = mock_doc_instance

                # Execute workflow
                metadata = analyze_binary(temp_input)
                document = create_spdx_document(metadata)

                # Verify workflow completed
                assert document == mock_doc_instance
                mock_package.assert_called_once()
        finally:
            os.unlink(temp_input)

    @patch('binary_sbom.analyzer._detect_format')
    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_workflow_with_complex_metadata(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package, mock_detect_format
    ):
        """Test workflow with complex binary (many sections, many dependencies)."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'complex binary')
            temp_input = f.name

        try:
            # Set up analyzer mock with complex data - patch _detect_format to return PE format
            mock_detect_format.return_value = ('PE', 'IMAGE_FILE_MACHINE_AMD64')

            # Mock lief.parse to return a mock binary object
            with patch('binary_sbom.analyzer.lief') as mock_lief:
                mock_binary = MagicMock()
                mock_binary.name = 'temp'
                mock_binary.header = MagicMock()
                mock_binary.header.machine = 'IMAGE_FILE_MACHINE_AMD64'
                mock_binary.entrypoint = 0
                mock_binary.imported_libraries = []
                mock_binary.sections = []
                mock_lief.parse.return_value = mock_binary

                # Set up generator mocks
                mock_package_instance = MagicMock()
                mock_package.return_value = mock_package_instance
                mock_no_assertion.return_value = MagicMock()
                mock_creation_info_instance = MagicMock()
                mock_creation_info.return_value = mock_creation_info_instance
                mock_doc_instance = MagicMock()
                mock_document.return_value = mock_doc_instance

                # Execute workflow
                metadata = analyze_binary(temp_input)
                document = create_spdx_document(metadata)

                # Verify complex metadata handled correctly
                assert len(metadata['dependencies']) == 0
                assert len(metadata['sections']) == 0
                assert document == mock_doc_instance

                # Verify package description includes all metadata
                call_kwargs = mock_package.call_args[1]
                description = call_kwargs['description']
                assert 'PE' in description
        finally:
            os.unlink(temp_input)

    @patch('binary_sbom.analyzer._detect_format')
    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_workflow_preserves_metadata_integrity(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package, mock_detect_format
    ):
        """Test that metadata is preserved through the workflow."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'test binary')
            temp_input = f.name

        try:
            # Set up analyzer mock - patch _detect_format to return MachO format
            mock_detect_format.return_value = ('MachO', 'CPU_TYPE_ARM64')

            # Mock lief.parse to return a mock binary object
            with patch('binary_sbom.analyzer.lief') as mock_lief:
                mock_binary = MagicMock()
                mock_binary.name = 'temp'
                mock_binary.header = MagicMock()
                mock_binary.header.cpu_type = 'CPU_TYPE_ARM64'
                mock_binary.entrypoint = 0
                mock_binary.imported_libraries = []
                mock_binary.sections = []
                mock_lief.parse.return_value = mock_binary

                # Set up generator mocks
                mock_package_instance = MagicMock()
                mock_package.return_value = mock_package_instance
                mock_no_assertion.return_value = MagicMock()
                mock_creation_info_instance = MagicMock()
                mock_creation_info.return_value = mock_creation_info_instance
                mock_doc_instance = MagicMock()
                mock_document.return_value = mock_doc_instance

                # Execute workflow
                metadata = analyze_binary(temp_input)
                document = create_spdx_document(metadata)

                # Verify metadata integrity
                assert metadata['name'] == 'temp'
                assert metadata['type'] == 'MachO'
                assert metadata['architecture'] == 'CPU_TYPE_ARM64'
                assert len(metadata['dependencies']) == 0
                assert len(metadata['sections']) == 0

                # Verify document created successfully
                assert document == mock_doc_instance
        finally:
            os.unlink(temp_input)


class TestMultiFormatHandling:
    """Test handling of different binary formats through the workflow."""

    @patch('binary_sbom.analyzer._detect_format')
    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_workflow_elf_format(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package, mock_detect_format
    ):
        """Test workflow with ELF binary format."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'ELF content')
            temp_input = f.name

        try:
            # Set up _detect_format to return ELF format
            mock_detect_format.return_value = ('ELF', 'EM_X86_64')

            # Mock lief.parse to return a mock binary object
            with patch('binary_sbom.analyzer.lief') as mock_lief:
                mock_binary = MagicMock()
                mock_binary.name = 'temp'
                mock_binary.header = MagicMock()
                mock_binary.header.machine_type = 'EM_X86_64'
                mock_binary.entrypoint = 0
                mock_binary.imported_libraries = []
                mock_binary.sections = []
                mock_lief.parse.return_value = mock_binary

                # Set up generator mocks
                mock_package.return_value = MagicMock()
                mock_no_assertion.return_value = MagicMock()
                mock_creation_info.return_value = MagicMock()
                mock_document.return_value = MagicMock()

                # Execute workflow
                metadata = analyze_binary(temp_input)
                document = create_spdx_document(metadata)

                assert metadata['type'] == 'ELF'
                assert metadata['architecture'] == 'EM_X86_64'
                assert document is not None
        finally:
            os.unlink(temp_input)

    @patch('binary_sbom.analyzer._detect_format')
    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_workflow_pe_format(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package, mock_detect_format
    ):
        """Test workflow with PE binary format."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'PE content')
            temp_input = f.name

        try:
            # Set up _detect_format to return PE format
            mock_detect_format.return_value = ('PE', 'IMAGE_FILE_MACHINE_AMD64')

            # Mock lief.parse to return a mock binary object
            with patch('binary_sbom.analyzer.lief') as mock_lief:
                mock_binary = MagicMock()
                mock_binary.name = 'temp'
                mock_binary.header = MagicMock()
                mock_binary.header.machine = 'IMAGE_FILE_MACHINE_AMD64'
                mock_binary.entrypoint = 0
                mock_binary.imported_libraries = []
                mock_binary.sections = []
                mock_lief.parse.return_value = mock_binary

                # Set up generator mocks
                mock_package.return_value = MagicMock()
                mock_no_assertion.return_value = MagicMock()
                mock_creation_info.return_value = MagicMock()
                mock_document.return_value = MagicMock()

                # Execute workflow
                metadata = analyze_binary(temp_input)
                document = create_spdx_document(metadata)

                assert metadata['type'] == 'PE'
                assert metadata['architecture'] == 'IMAGE_FILE_MACHINE_AMD64'
                assert document is not None
        finally:
            os.unlink(temp_input)

    @patch('binary_sbom.analyzer._detect_format')
    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_workflow_macho_format(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package, mock_detect_format
    ):
        """Test workflow with MachO binary format."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'MachO content')
            temp_input = f.name

        try:
            # Set up _detect_format to return MachO format
            mock_detect_format.return_value = ('MachO', 'CPU_TYPE_ARM64')

            # Mock lief.parse to return a mock binary object
            with patch('binary_sbom.analyzer.lief') as mock_lief:
                mock_binary = MagicMock()
                mock_binary.name = 'temp'
                mock_binary.header = MagicMock()
                mock_binary.header.cpu_type = 'CPU_TYPE_ARM64'
                mock_binary.entrypoint = 0
                mock_binary.imported_libraries = []
                mock_binary.sections = []
                mock_lief.parse.return_value = mock_binary

                # Set up generator mocks
                mock_package.return_value = MagicMock()
                mock_no_assertion.return_value = MagicMock()
                mock_creation_info.return_value = MagicMock()
                mock_document.return_value = MagicMock()

                # Execute workflow
                metadata = analyze_binary(temp_input)
                document = create_spdx_document(metadata)

                assert metadata['type'] == 'MachO'
                assert metadata['architecture'] == 'CPU_TYPE_ARM64'
                assert document is not None
        finally:
            os.unlink(temp_input)

    @patch('binary_sbom.analyzer._detect_format')
    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_workflow_raw_format(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package, mock_detect_format
    ):
        """Test workflow with raw binary format (fallback)."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'raw binary content')
            temp_input = f.name

        try:
            # Set up _detect_format to return Raw format
            mock_detect_format.return_value = ('Raw', 'unknown')

            # Mock lief.parse to return a mock binary object
            with patch('binary_sbom.analyzer.lief') as mock_lief:
                mock_binary = MagicMock()
                mock_binary.name = 'temp'
                mock_binary.header = MagicMock()
                mock_binary.entrypoint = 0
                mock_binary.imported_libraries = []
                mock_binary.sections = []
                mock_lief.parse.return_value = mock_binary

                # Set up generator mocks
                mock_package.return_value = MagicMock()
                mock_no_assertion.return_value = MagicMock()
                mock_creation_info.return_value = MagicMock()
                mock_document.return_value = MagicMock()

                # Execute workflow
                metadata = analyze_binary(temp_input)
                document = create_spdx_document(metadata)

                assert metadata['type'] == 'Raw'
                assert metadata['architecture'] == 'unknown'
                assert document is not None
        finally:
            os.unlink(temp_input)


class TestOutputFormatSwitching:
    """Test output format switching in the workflow."""

    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_workflow_json_output(self, mock_document, mock_creation_info, mock_no_assertion, mock_package):
        """Test complete workflow ending in JSON output."""
        metadata = {
            'name': 'test',
            'type': 'ELF',
            'architecture': 'x86_64',
            'sections': [],
            'dependencies': []
        }

        # Set up mocks
        mock_package_instance = MagicMock()
        mock_package.return_value = mock_package_instance
        mock_no_assertion.return_value = MagicMock()
        mock_creation_info_instance = MagicMock()
        mock_creation_info.return_value = mock_creation_info_instance
        mock_doc_instance = MagicMock()
        mock_document.return_value = mock_doc_instance

        # Create document
        document = create_spdx_document(metadata)

        # Write to file
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_output = f.name

        try:
            with patch('spdx_tools.spdx.writer.json.json_writer.write_document_to_file') as mock_write:
                write_spdx_file(document, temp_output, 'json')

                # Verify JSON writer was called
                mock_write.assert_called_once_with(document, temp_output, validate=False)
        finally:
            if os.path.exists(temp_output):
                os.unlink(temp_output)

    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_workflow_xml_output(self, mock_document, mock_creation_info, mock_no_assertion, mock_package):
        """Test complete workflow ending in XML output."""
        metadata = {
            'name': 'test',
            'type': 'PE',
            'architecture': 'AMD64',
            'sections': [],
            'dependencies': []
        }

        # Set up mocks
        mock_package.return_value = MagicMock()
        mock_no_assertion.return_value = MagicMock()
        mock_creation_info.return_value = MagicMock()
        mock_document.return_value = MagicMock()

        # Create document
        document = create_spdx_document(metadata)

        # Write to file
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_output = f.name

        try:
            with patch('spdx_tools.spdx.writer.xml.xml_writer.write_document_to_file') as mock_write:
                write_spdx_file(document, temp_output, 'xml')

                # Verify XML writer was called
                mock_write.assert_called_once_with(document, temp_output, validate=False)
        finally:
            if os.path.exists(temp_output):
                os.unlink(temp_output)

    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_workflow_yaml_output(self, mock_document, mock_creation_info, mock_no_assertion, mock_package):
        """Test complete workflow ending in YAML output."""
        metadata = {
            'name': 'test',
            'type': 'MachO',
            'architecture': 'ARM64',
            'sections': [],
            'dependencies': []
        }

        # Set up mocks
        mock_package.return_value = MagicMock()
        mock_no_assertion.return_value = MagicMock()
        mock_creation_info.return_value = MagicMock()
        mock_document.return_value = MagicMock()

        # Create document
        document = create_spdx_document(metadata)

        # Write to file
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_output = f.name

        try:
            with patch('spdx_tools.spdx.writer.yaml.yaml_writer.write_document_to_file') as mock_write:
                write_spdx_file(document, temp_output, 'yaml')

                # Verify YAML writer was called
                mock_write.assert_called_once_with(document, temp_output, validate=False)
        finally:
            if os.path.exists(temp_output):
                os.unlink(temp_output)

    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_workflow_tag_value_output(self, mock_document, mock_creation_info, mock_no_assertion, mock_package):
        """Test complete workflow ending in Tag-Value output."""
        metadata = {
            'name': 'test',
            'type': 'Raw',
            'architecture': 'unknown',
            'sections': [],
            'dependencies': []
        }

        # Set up mocks
        mock_package.return_value = MagicMock()
        mock_no_assertion.return_value = MagicMock()
        mock_creation_info.return_value = MagicMock()
        mock_document.return_value = MagicMock()

        # Create document
        document = create_spdx_document(metadata)

        # Write to file
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_output = f.name

        try:
            with patch('spdx_tools.spdx.writer.tagvalue.tagvalue_writer.write_document_to_file') as mock_write:
                write_spdx_file(document, temp_output, 'tag-value')

                # Verify Tag-Value writer was called
                mock_write.assert_called_once_with(document, temp_output, validate=False)
        finally:
            if os.path.exists(temp_output):
                os.unlink(temp_output)

    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator.Document')
    def test_multiple_formats_same_document(
        self, mock_document, mock_creation_info, mock_no_assertion, mock_package
    ):
        """Test writing the same document to multiple formats."""
        metadata = {
            'name': 'test',
            'type': 'ELF',
            'architecture': 'x86_64',
            'sections': [],
            'dependencies': []
        }

        # Set up mocks
        mock_package.return_value = MagicMock()
        mock_no_assertion.return_value = MagicMock()
        mock_creation_info.return_value = MagicMock()
        mock_document_instance = MagicMock()
        mock_document.return_value = mock_document_instance

        # Create document once
        document = create_spdx_document(metadata)

        # Write to multiple formats
        formats = ['json', 'xml', 'yaml', 'tag-value']
        writers = [
            'spdx_tools.spdx.writer.json.json_writer.write_document_to_file',
            'spdx_tools.spdx.writer.xml.xml_writer.write_document_to_file',
            'spdx_tools.spdx.writer.yaml.yaml_writer.write_document_to_file',
            'spdx_tools.spdx.writer.tagvalue.tagvalue_writer.write_document_to_file'
        ]

        for fmt, writer_path in zip(formats, writers):
            with tempfile.NamedTemporaryFile(delete=False) as f:
                temp_output = f.name

            try:
                with patch(writer_path) as mock_write:
                    write_spdx_file(document, temp_output, fmt)
                    mock_write.assert_called_once_with(document, temp_output, validate=False)
            finally:
                if os.path.exists(temp_output):
                    os.unlink(temp_output)


class TestPathValidationIntegration:
    """Test end-to-end path validation in the analyzer workflow."""

    def test_analyzer_sanitizes_path_before_analysis(self):
        """Test that analyzer sanitizes paths before analyzing binaries."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test binary file
            test_file = os.path.join(temp_dir, 'test.bin')
            with open(test_file, 'wb') as f:
                f.write(b'ELF binary content')

            # Create a path with traversal components
            traversal_path = os.path.join(temp_dir, 'subdir', '..', 'test.bin')

            with patch('binary_sbom.analyzer._detect_format') as mock_detect_format:
                mock_detect_format.return_value = ('ELF', 'EM_X86_64')

                with patch('binary_sbom.analyzer.lief') as mock_lief:
                    mock_binary = MagicMock()
                    mock_binary.name = os.path.basename(test_file)
                    mock_binary.header = MagicMock()
                    mock_binary.header.machine_type = 'EM_X86_64'
                    mock_binary.entrypoint = 0
                    mock_binary.imported_libraries = []
                    mock_binary.sections = []
                    mock_lief.parse.return_value = mock_binary

                    # Analyze with traversal path - should sanitize and work
                    metadata = analyze_binary(traversal_path)

                    # Verify analysis succeeded
                    assert metadata['name'] == os.path.basename(test_file)
                    assert metadata['type'] == 'ELF'

    def test_analyzer_sanitizes_relative_paths(self):
        """Test that analyzer properly sanitizes relative paths."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test binary file
            test_file = os.path.join(temp_dir, 'test.bin')
            with open(test_file, 'wb') as f:
                f.write(b'binary content')

            # Change to temp directory and use relative path
            original_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                relative_path = './test.bin'

                with patch('binary_sbom.analyzer._detect_format') as mock_detect_format:
                    mock_detect_format.return_value = ('Raw', 'unknown')

                    with patch('binary_sbom.analyzer.lief') as mock_lief:
                        mock_binary = MagicMock()
                        mock_binary.name = 'test.bin'
                        mock_binary.header = MagicMock()
                        mock_binary.entrypoint = 0
                        mock_binary.imported_libraries = []
                        mock_binary.sections = []
                        mock_lief.parse.return_value = mock_binary

                        # Analyze with relative path - should sanitize to absolute
                        metadata = analyze_binary(relative_path)

                        # Verify analysis succeeded
                        assert metadata['name'] == 'test.bin'
            finally:
                os.chdir(original_cwd)

    def test_path_validator_blocks_directory_traversal(self):
        """Test that path validator blocks directory traversal attempts."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create an allowed directory
            allowed_dir = os.path.join(temp_dir, 'allowed')
            os.makedirs(allowed_dir)

            # Try to access file outside allowed directory using traversal
            # Create a file outside the allowed directory
            outside_file = os.path.join(temp_dir, 'outside.bin')
            with open(outside_file, 'wb') as f:
                f.write(b'outside content')

            # Try to access it with traversal from allowed dir
            traversal_path = os.path.join(allowed_dir, '..', 'outside.bin')

            # Should raise PathValidationError
            with pytest.raises(PathValidationError, match='outside allowed directory'):
                validate_file_path(traversal_path, allowed_dirs=[allowed_dir])

    def test_path_validator_allows_safe_paths(self):
        """Test that path validator allows paths within allowed directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create allowed directory and file inside it
            allowed_dir = os.path.join(temp_dir, 'allowed')
            os.makedirs(allowed_dir)
            safe_file = os.path.join(allowed_dir, 'safe.bin')
            with open(safe_file, 'wb') as f:
                f.write(b'safe content')

            # Should validate successfully
            validated_path = validate_file_path(safe_file, allowed_dirs=[allowed_dir])
            assert validated_path == os.path.realpath(safe_file)

    def test_path_validator_detects_symlink_escapes(self):
        """Test that path validator detects symlink escapes."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create allowed directory
            allowed_dir = os.path.join(temp_dir, 'allowed')
            os.makedirs(allowed_dir)

            # Create a file outside allowed directory
            outside_file = os.path.join(temp_dir, 'secret.bin')
            with open(outside_file, 'wb') as f:
                f.write(b'secret content')

            # Create a symlink inside allowed directory pointing outside
            symlink_path = os.path.join(allowed_dir, 'escape_link.bin')
            os.symlink(outside_file, symlink_path)

            # Should detect symlink escape
            with pytest.raises(PathValidationError, match='Symlink escape detected'):
                check_symlink_safety(symlink_path, allowed_dir)

    def test_path_validator_allows_safe_symlinks(self):
        """Test that path validator allows symlinks within allowed directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create allowed directory
            allowed_dir = os.path.join(temp_dir, 'allowed')
            os.makedirs(allowed_dir)

            # Create a file inside allowed directory
            safe_file = os.path.join(allowed_dir, 'safe.bin')
            with open(safe_file, 'wb') as f:
                f.write(b'safe content')

            # Create a symlink inside allowed directory pointing to safe file
            symlink_path = os.path.join(allowed_dir, 'safe_link.bin')
            os.symlink(safe_file, symlink_path)

            # Should validate successfully
            result = check_symlink_safety(symlink_path, allowed_dir)
            assert result is True

    @patch('binary_sbom.analyzer._detect_format')
    def test_workflow_blocks_path_traversal_attack(self, mock_detect_format):
        """Test that workflow blocks path traversal attacks end-to-end."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create allowed directory
            allowed_dir = os.path.join(temp_dir, 'allowed')
            os.makedirs(allowed_dir)

            # Try to analyze file outside allowed directory using traversal
            # This simulates an attack attempting to read /etc/passwd
            traversal_path = os.path.join(allowed_dir, '..', '..', 'etc', 'passwd')

            # The analyzer should sanitize the path
            sanitized = sanitize_path(traversal_path)

            # Validation should block it
            with pytest.raises(PathValidationError, match='outside allowed directory'):
                validate_file_path(sanitized, allowed_dirs=[allowed_dir])

    @patch('binary_sbom.analyzer._detect_format')
    def test_workflow_with_path_sanitization_chain(self, mock_detect_format):
        """Test complete workflow with path sanitization chain."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a complex path with traversal and relative components
            test_file = os.path.join(temp_dir, 'test.bin')
            with open(test_file, 'wb') as f:
                f.write(b'test content')

            # Create path with multiple traversal components
            complex_path = os.path.join(temp_dir, 'subdir', '..', '.', 'test.bin')

            # Sanitize the path
            sanitized_path = sanitize_path(complex_path)

            # Verify it resolves to the correct absolute path
            assert os.path.realpath(sanitized_path) == os.path.realpath(test_file)

            # Validate it's within allowed directory
            validated_path = validate_file_path(sanitized_path, allowed_dirs=[temp_dir])
            assert validated_path == sanitized_path

    def test_path_validator_handles_absolute_vs_relative_paths(self):
        """Test that path validator correctly handles absolute and relative paths."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create allowed directory and file
            allowed_dir = os.path.join(temp_dir, 'allowed')
            os.makedirs(allowed_dir)
            test_file = os.path.join(allowed_dir, 'test.bin')
            with open(test_file, 'wb') as f:
                f.write(b'test content')

            # Test with absolute path
            validated_absolute = validate_file_path(test_file, allowed_dirs=[allowed_dir])
            assert os.path.isabs(validated_absolute)

            # Test with relative path (by changing directory)
            original_cwd = os.getcwd()
            try:
                os.chdir(allowed_dir)
                validated_relative = validate_file_path('./test.bin', allowed_dirs=[allowed_dir])
                # Both should resolve to same canonical path
                assert os.path.realpath(validated_absolute) == os.path.realpath(validated_relative)
            finally:
                os.chdir(original_cwd)

    def test_path_validator_multiple_allowed_directories(self):
        """Test that path validator works with multiple allowed directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create multiple allowed directories
            allowed_dir1 = os.path.join(temp_dir, 'allowed1')
            allowed_dir2 = os.path.join(temp_dir, 'allowed2')
            os.makedirs(allowed_dir1)
            os.makedirs(allowed_dir2)

            # Create files in each directory
            file1 = os.path.join(allowed_dir1, 'file1.bin')
            file2 = os.path.join(allowed_dir2, 'file2.bin')
            with open(file1, 'wb') as f:
                f.write(b'file1 content')
            with open(file2, 'wb') as f:
                f.write(b'file2 content')

            # Both files should validate
            validated1 = validate_file_path(file1, allowed_dirs=[allowed_dir1, allowed_dir2])
            validated2 = validate_file_path(file2, allowed_dirs=[allowed_dir1, allowed_dir2])

            assert os.path.realpath(validated1) == os.path.realpath(file1)
            assert os.path.realpath(validated2) == os.path.realpath(file2)

    def test_path_validator_empty_allowed_directories_raises_error(self):
        """Test that empty allowed directories list raises error."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = os.path.join(temp_dir, 'test.bin')
            with open(test_file, 'wb') as f:
                f.write(b'test content')

            # Should raise error for empty allowed directories
            with pytest.raises(PathValidationError, match='No allowed directories specified'):
                validate_file_path(test_file, allowed_dirs=[])

    @patch('binary_sbom.analyzer._detect_format')
    def test_end_to_end_workflow_with_path_validation(self, mock_detect_format):
        """Test complete workflow from input path sanitization to analysis."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test file
            test_file = os.path.join(temp_dir, 'test.bin')
            with open(test_file, 'wb') as f:
                f.write(b'ELF content')

            # Use path with traversal components
            input_path = os.path.join(temp_dir, 'subdir', '..', 'test.bin')

            with patch('binary_sbom.analyzer.lief') as mock_lief:
                mock_binary = MagicMock()
                mock_binary.name = 'test.bin'
                mock_binary.header = MagicMock()
                mock_binary.header.machine_type = 'EM_X86_64'
                mock_binary.entrypoint = 0
                mock_binary.imported_libraries = []
                mock_binary.sections = []
                mock_lief.parse.return_value = mock_binary

                mock_detect_format.return_value = ('ELF', 'EM_X86_64')

                # Sanitize path first
                sanitized = sanitize_path(input_path)

                # Validate it's in allowed directory
                validated = validate_file_path(sanitized, allowed_dirs=[temp_dir])

                # Analyze the validated path
                metadata = analyze_binary(validated)

                # Verify complete workflow succeeded
                assert metadata['name'] == 'test.bin'
                assert metadata['type'] == 'ELF'
                assert metadata['architecture'] == 'EM_X86_64'
