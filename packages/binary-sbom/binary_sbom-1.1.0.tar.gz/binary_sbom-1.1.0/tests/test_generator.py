"""
Unit tests for the SPDX generator module.

Tests SPDX document creation, package generation, and file writing in all formats.
"""

import os
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from binary_sbom.generator import (
    SPDXGenerationError,
    _create_package,
    _validate_metadata,
    create_document,
    create_package,
    create_spdx_document,
    write_spdx_file,
)


class TestCreateSpdxDocument:
    """Test SPDX document creation functionality."""

    @patch('binary_sbom.generator.Document', None)
    def test_create_spdx_document_without_spdx_tools(self):
        """Test that missing spdx-tools raises ImportError."""
        with pytest.raises(ImportError, match='spdx-tools library is required'):
            create_spdx_document({'name': 'test', 'type': 'ELF', 'architecture': 'x86_64'})

    def test_create_spdx_document_missing_name(self):
        """Test that missing name field raises ValueError."""
        metadata = {'type': 'ELF', 'architecture': 'x86_64'}
        with pytest.raises(ValueError, match='Missing required metadata fields'):
            create_spdx_document(metadata)

    def test_create_spdx_document_missing_type(self):
        """Test that missing type field raises ValueError."""
        metadata = {'name': 'test', 'architecture': 'x86_64'}
        with pytest.raises(ValueError, match='Missing required metadata fields'):
            create_spdx_document(metadata)

    def test_create_spdx_document_missing_architecture(self):
        """Test that missing architecture field raises ValueError."""
        metadata = {'name': 'test', 'type': 'ELF'}
        with pytest.raises(ValueError, match='Missing required metadata fields'):
            create_spdx_document(metadata)

    def test_create_spdx_document_empty_name(self):
        """Test that empty name field raises ValueError."""
        metadata = {'name': '', 'type': 'ELF', 'architecture': 'x86_64'}
        with pytest.raises(ValueError, match="Metadata field 'name' cannot be empty"):
            create_spdx_document(metadata)

    @patch('binary_sbom.generator._create_package')
    def test_create_spdx_document_package_creation_failure(self, mock_create_package):
        """Test that package creation failure is wrapped."""
        mock_create_package.side_effect = Exception('Package creation failed')
        metadata = {'name': 'test', 'type': 'ELF', 'architecture': 'x86_64'}
        with pytest.raises(SPDXGenerationError, match='Failed to create SPDX package'):
            create_spdx_document(metadata)

    @patch('binary_sbom.generator.CreationInfo')
    def test_create_spdx_document_creation_info_failure(self, mock_creation_info):
        """Test that creation info failure is wrapped."""
        mock_creation_info.side_effect = Exception('Creation info failed')
        with patch('binary_sbom.generator._create_package', return_value=MagicMock()):
            metadata = {'name': 'test', 'type': 'ELF', 'architecture': 'x86_64'}
            with pytest.raises(SPDXGenerationError, match='Failed to create creation info'):
                create_spdx_document(metadata)

    @patch('binary_sbom.generator.Document')
    @patch('binary_sbom.generator.CreationInfo')
    @patch('binary_sbom.generator._create_package')
    def test_create_spdx_document_success(self, mock_create_package, mock_creation_info, mock_document):
        """Test successful SPDX document creation."""
        mock_package = MagicMock()
        mock_create_package.return_value = mock_package
        mock_creation_info_instance = MagicMock()
        mock_creation_info.return_value = mock_creation_info_instance
        mock_doc_instance = MagicMock()
        mock_document.return_value = mock_doc_instance

        metadata = {
            'name': 'test-binary',
            'type': 'ELF',
            'architecture': 'x86_64',
            'entrypoint': '0x4000',
            'sections': [{'name': '.text', 'size': 1024}],
            'dependencies': ['libc.so.6']
        }

        doc = create_spdx_document(metadata)

        assert doc == mock_doc_instance
        mock_document.assert_called_once()
        # Check that creation_info is passed as keyword argument (spdx-tools 0.8+ API)
        call_kwargs = mock_document.call_args[1]
        assert call_kwargs['creation_info'] == mock_creation_info_instance
        assert call_kwargs['packages'] == [mock_package]

    def test_create_spdx_document_custom_namespace(self):
        """Test document creation with custom namespace."""
        with patch('binary_sbom.generator._create_package', return_value=MagicMock()):
            with patch('binary_sbom.generator.CreationInfo', return_value=MagicMock()) as mock_ci:
                with patch('binary_sbom.generator.Document', return_value=MagicMock()):
                    metadata = {'name': 'test', 'type': 'ELF', 'architecture': 'x86_64'}
                    create_spdx_document(metadata, namespace='https://custom.com/sbom')

                    # Check that CreationInfo was called with the correct namespace
                    mock_ci.assert_called_once()
                    call_kwargs = mock_ci.call_args[1]
                    # document_namespace should contain custom namespace
                    assert 'https://custom.com/sbom' in call_kwargs['document_namespace']

    def test_create_spdx_document_custom_creator(self):
        """Test document creation with custom creator."""
        with patch('binary_sbom.generator._create_package', return_value=MagicMock()):
            with patch('binary_sbom.generator.CreationInfo') as mock_ci:
                with patch('binary_sbom.generator.Document', return_value=MagicMock()):
                    metadata = {'name': 'test', 'type': 'ELF', 'architecture': 'x86_64'}
                    create_spdx_document(metadata, creator='Tool: custom-tool')

                    mock_ci.assert_called_once()
                    # creators is passed as keyword argument
                    call_kwargs = mock_ci.call_args[1]
                    creators_list = call_kwargs['creators']
                    assert len(creators_list) == 1
                    assert creators_list[0].name == 'custom-tool'


class TestCreatePackage:
    """Test SPDX package creation functionality."""

    @patch('binary_sbom.generator.Package', None)
    def test_create_package_without_spdx_tools(self):
        """Test that missing spdx-tools raises ImportError."""
        with pytest.raises(ImportError, match='spdx-tools library is required'):
            create_package({'name': 'test', 'type': 'ELF', 'architecture': 'x86_64'})

    def test_create_package_missing_required_fields(self):
        """Test that missing required fields raises ValueError."""
        metadata = {'name': 'test'}
        with pytest.raises(ValueError, match='Missing required metadata fields'):
            create_package(metadata)

    def test_create_package_invalid_dependencies_type(self):
        """Test that invalid dependencies type raises ValueError."""
        metadata = {
            'name': 'test',
            'type': 'ELF',
            'architecture': 'x86_64',
            'dependencies': 'not-a-list'
        }
        with pytest.raises(ValueError, match="Metadata field 'dependencies' must be a list"):
            create_package(metadata)

    def test_create_package_invalid_sections_type(self):
        """Test that invalid sections type raises ValueError."""
        metadata = {
            'name': 'test',
            'type': 'ELF',
            'architecture': 'x86_64',
            'sections': 'not-a-list'
        }
        with pytest.raises(ValueError, match="Metadata field 'sections' must be a list"):
            create_package(metadata)

    @patch('binary_sbom.generator._create_package')
    def test_create_package_creation_failure(self, mock_create_package):
        """Test that package creation failure is wrapped."""
        mock_create_package.side_effect = Exception('Creation failed')
        metadata = {'name': 'test', 'type': 'ELF', 'architecture': 'x86_64'}
        with pytest.raises(SPDXGenerationError, match='Failed to create SPDX package'):
            create_package(metadata)

    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    def test_create_package_success(self, mock_no_assertion, mock_package):
        """Test successful package creation."""
        mock_no_assertion.return_value = MagicMock()
        mock_package_instance = MagicMock()
        mock_package.return_value = mock_package_instance

        metadata = {
            'name': 'test-binary',
            'type': 'ELF',
            'architecture': 'x86_64',
            'entrypoint': '0x4000',
            'sections': [{'name': '.text', 'size': 1024}],
            'dependencies': ['libc.so.6']
        }

        package = create_package(metadata)

        assert package == mock_package_instance
        mock_package.assert_called_once()
        call_kwargs = mock_package.call_args[1]
        assert call_kwargs['name'] == 'test-binary'
        assert call_kwargs['spdx_id'] == 'SPDXRef-Package'
        assert 'ELF' in call_kwargs['description']
        assert 'x86_64' in call_kwargs['description']
        assert '0x4000' in call_kwargs['description']
        assert 'Sections: 1' in call_kwargs['description']
        assert call_kwargs['version'] == 'ELF-x86_64'

    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    def test_create_package_minimal_metadata(self, mock_no_assertion, mock_package):
        """Test package creation with minimal metadata."""
        mock_no_assertion.return_value = MagicMock()
        mock_package_instance = MagicMock()
        mock_package.return_value = mock_package_instance

        metadata = {
            'name': 'minimal',
            'type': 'Raw',
            'architecture': 'unknown'
        }

        package = create_package(metadata)

        assert package == mock_package_instance
        call_kwargs = mock_package.call_args[1]
        assert call_kwargs['name'] == 'minimal'
        assert call_kwargs['version'] == 'Raw-unknown'
        # Should not include entrypoint or sections in description
        assert 'Entrypoint' not in call_kwargs['description']
        assert 'Sections' not in call_kwargs['description']


class TestCreateDocument:
    """Test create_document alias functionality."""

    @patch('binary_sbom.generator.create_spdx_document')
    def test_create_document_is_alias(self, mock_create_spdx):
        """Test that create_document calls create_spdx_document."""
        mock_create_spdx.return_value = MagicMock()
        metadata = {'name': 'test', 'type': 'ELF', 'architecture': 'x86_64'}
        namespace = 'https://test.com/sbom'
        creator = 'Tool: test-tool'

        create_document(metadata, namespace, creator)

        mock_create_spdx.assert_called_once_with(metadata, namespace, creator)


class TestValidateMetadata:
    """Test metadata validation functionality."""

    def test_validate_metadata_all_required_fields_present(self):
        """Test validation with all required fields."""
        metadata = {
            'name': 'test',
            'type': 'ELF',
            'architecture': 'x86_64'
        }
        # Should not raise
        _validate_metadata(metadata)

    def test_validate_metadata_missing_name(self):
        """Test validation fails when name is missing."""
        metadata = {'type': 'ELF', 'architecture': 'x86_64'}
        with pytest.raises(ValueError, match='Missing required metadata fields.*name'):
            _validate_metadata(metadata)

    def test_validate_metadata_missing_type(self):
        """Test validation fails when type is missing."""
        metadata = {'name': 'test', 'architecture': 'x86_64'}
        with pytest.raises(ValueError, match='Missing required metadata fields.*type'):
            _validate_metadata(metadata)

    def test_validate_metadata_missing_architecture(self):
        """Test validation fails when architecture is missing."""
        metadata = {'name': 'test', 'type': 'ELF'}
        with pytest.raises(ValueError, match='Missing required metadata fields.*architecture'):
            _validate_metadata(metadata)

    def test_validate_metadata_missing_multiple_fields(self):
        """Test validation fails when multiple fields are missing."""
        metadata = {'name': 'test'}
        with pytest.raises(ValueError, match='Missing required metadata fields.*type.*architecture'):
            _validate_metadata(metadata)

    def test_validate_metadata_empty_name(self):
        """Test validation fails when name is empty."""
        metadata = {'name': '', 'type': 'ELF', 'architecture': 'x86_64'}
        with pytest.raises(ValueError, match="Metadata field 'name' cannot be empty"):
            _validate_metadata(metadata)

    def test_validate_metadata_invalid_dependencies_type(self):
        """Test validation fails when dependencies is not a list."""
        metadata = {
            'name': 'test',
            'type': 'ELF',
            'architecture': 'x86_64',
            'dependencies': 'invalid'
        }
        with pytest.raises(ValueError, match="Metadata field 'dependencies' must be a list"):
            _validate_metadata(metadata)

    def test_validate_metadata_invalid_sections_type(self):
        """Test validation fails when sections is not a list."""
        metadata = {
            'name': 'test',
            'type': 'ELF',
            'architecture': 'x86_64',
            'sections': 'invalid'
        }
        with pytest.raises(ValueError, match="Metadata field 'sections' must be a list"):
            _validate_metadata(metadata)

    def test_validate_metadata_valid_optional_fields(self):
        """Test validation passes with valid optional fields."""
        metadata = {
            'name': 'test',
            'type': 'ELF',
            'architecture': 'x86_64',
            'dependencies': ['libc.so.6'],
            'sections': [{'name': '.text'}]
        }
        # Should not raise
        _validate_metadata(metadata)


class TestCreatePackageInternal:
    """Test internal _create_package function."""

    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    def test_create_package_internal_description_building(self, mock_no_assertion, mock_package):
        """Test description building from metadata."""
        mock_no_assertion.return_value = MagicMock()
        mock_package.return_value = MagicMock()

        metadata = {
            'name': 'test',
            'type': 'ELF',
            'architecture': 'x86_64',
            'entrypoint': '0x4000',
            'sections': [{'name': '.text'}, {'name': '.data'}]
        }

        _create_package(metadata)

        call_kwargs = mock_package.call_args[1]
        description = call_kwargs['description']
        assert 'Binary Type: ELF' in description
        assert 'Architecture: x86_64' in description
        assert 'Entrypoint: 0x4000' in description
        assert 'Sections: 2' in description
        assert ' | ' in description  # Check separator

    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    def test_create_package_internal_without_entrypoint(self, mock_no_assertion, mock_package):
        """Test package creation without entrypoint."""
        mock_no_assertion.return_value = MagicMock()
        mock_package.return_value = MagicMock()

        metadata = {
            'name': 'test',
            'type': 'Raw',
            'architecture': 'unknown',
            'sections': []
        }

        _create_package(metadata)

        call_kwargs = mock_package.call_args[1]
        description = call_kwargs['description']
        assert 'Entrypoint' not in description

    @patch('binary_sbom.generator.Package')
    @patch('binary_sbom.generator.SpdxNoAssertion')
    def test_create_package_internal_without_sections(self, mock_no_assertion, mock_package):
        """Test package creation without sections."""
        mock_no_assertion.return_value = MagicMock()
        mock_package.return_value = MagicMock()

        metadata = {
            'name': 'test',
            'type': 'PE',
            'architecture': 'AMD64',
            'entrypoint': '0x1000'
        }

        _create_package(metadata)

        call_kwargs = mock_package.call_args[1]
        description = call_kwargs['description']
        assert 'Sections' not in description

    @patch('binary_sbom.generator.Package')
    def test_create_package_internal_failure(self, mock_package):
        """Test that package creation failure is raised."""
        mock_package.side_effect = Exception('Package creation failed')

        metadata = {
            'name': 'test',
            'type': 'ELF',
            'architecture': 'x86_64'
        }

        with pytest.raises(SPDXGenerationError, match='Failed to create package'):
            _create_package(metadata)


class TestWriteSpdxFile:
    """Test SPDX file writing functionality."""

    @patch('binary_sbom.generator.Document', None)
    def test_write_spdx_file_without_spdx_tools(self):
        """Test that missing spdx-tools raises ImportError."""
        with pytest.raises(ImportError, match='spdx-tools library is required'):
            write_spdx_file(MagicMock(), 'output.json', 'json')

    def test_write_spdx_file_unsupported_format(self):
        """Test that unsupported format raises ValueError."""
        with patch('binary_sbom.generator.Document', return_value=MagicMock()):
            document = MagicMock()
            with pytest.raises(ValueError, match='Unsupported output format.*invalid'):
                write_spdx_file(document, 'output.spdx', 'invalid')

    def test_write_spdx_file_format_normalization_json(self):
        """Test format normalization for JSON (case-insensitive)."""
        with patch('binary_sbom.generator.Document', return_value=MagicMock()):
            with patch('spdx_tools.spdx.writer.json.json_writer.write_document_to_file') as mock_write:
                document = MagicMock()
                write_spdx_file(document, 'output.JSON', 'JSON')
                mock_write.assert_called_once()

    def test_write_spdx_file_format_normalization_underscore(self):
        """Test format normalization with underscore."""
        with patch('binary_sbom.generator.Document', return_value=MagicMock()):
            with patch('spdx_tools.spdx.writer.tagvalue.tagvalue_writer.write_document_to_file') as mock_write:
                document = MagicMock()
                write_spdx_file(document, 'output.json', 'tag_value')
                mock_write.assert_called_once()

    def test_write_spdx_file_json_format(self):
        """Test writing SPDX document in JSON format."""
        with patch('binary_sbom.generator.Document', return_value=MagicMock()):
            with patch('spdx_tools.spdx.writer.json.json_writer.write_document_to_file') as mock_write:
                document = MagicMock()
                write_spdx_file(document, 'output.spdx.json', 'json')
                mock_write.assert_called_once_with(document, 'output.spdx.json', validate=False)

    def test_write_spdx_file_xml_format(self):
        """Test writing SPDX document in XML format."""
        with patch('binary_sbom.generator.Document', return_value=MagicMock()):
            with patch('spdx_tools.spdx.writer.xml.xml_writer.write_document_to_file') as mock_write:
                document = MagicMock()
                write_spdx_file(document, 'output.spdx.xml', 'xml')
                mock_write.assert_called_once_with(document, 'output.spdx.xml', validate=False)

    def test_write_spdx_file_yaml_format(self):
        """Test writing SPDX document in YAML format."""
        with patch('binary_sbom.generator.Document', return_value=MagicMock()):
            with patch('spdx_tools.spdx.writer.yaml.yaml_writer.write_document_to_file') as mock_write:
                document = MagicMock()
                write_spdx_file(document, 'output.spdx.yaml', 'yaml')
                mock_write.assert_called_once_with(document, 'output.spdx.yaml', validate=False)

    def test_write_spdx_file_tag_value_format(self):
        """Test writing SPDX document in Tag-Value format."""
        with patch('binary_sbom.generator.Document', return_value=MagicMock()):
            with patch('spdx_tools.spdx.writer.tagvalue.tagvalue_writer.write_document_to_file') as mock_write:
                document = MagicMock()
                write_spdx_file(document, 'output.spdx', 'tag-value')
                mock_write.assert_called_once_with(document, 'output.spdx', validate=False)

    def test_write_spdx_file_import_error(self):
        """Test that import error during writer import is handled."""
        with patch('binary_sbom.generator.Document', return_value=MagicMock()):
            # Patch the import itself to raise ImportError
            with patch('builtins.__import__', side_effect=ImportError('Writer not found')):
                document = MagicMock()
                with pytest.raises(SPDXGenerationError, match='Failed to import SPDX writer'):
                    write_spdx_file(document, 'output.json', 'json')

    def test_write_spdx_file_io_error(self):
        """Test that IOError during write is propagated."""
        with patch('binary_sbom.generator.Document', return_value=MagicMock()):
            with patch('spdx_tools.spdx.writer.json.json_writer.write_document_to_file', side_effect=IOError('Permission denied')):
                document = MagicMock()
                with pytest.raises(IOError, match='Failed to write SPDX document'):
                    write_spdx_file(document, '/root/output.json', 'json')

    def test_write_spdx_file_generic_error(self):
        """Test that generic errors during write are wrapped."""
        with patch('binary_sbom.generator.Document', return_value=MagicMock()):
            with patch('spdx_tools.spdx.writer.json.json_writer.write_document_to_file', side_effect=Exception('Write failed')):
                document = MagicMock()
                with pytest.raises(SPDXGenerationError, match='Failed to write SPDX document in json format'):
                    write_spdx_file(document, 'output.json', 'json')

    def test_write_spdx_file_creates_output_file(self):
        """Test that write_spdx_file actually creates output file."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name

        try:
            # Create a minimal mock document
            with patch('binary_sbom.generator.Document', return_value=MagicMock()):
                with patch('spdx_tools.spdx.writer.json.json_writer.write_document_to_file') as mock_write:
                    document = MagicMock()
                    write_spdx_file(document, temp_path, 'json')

                    # Verify write_file was called with correct path
                    mock_write.assert_called_once()
                    args = mock_write.call_args[0]
                    assert args[1] == temp_path
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestSPDXGenerationError:
    """Test SPDXGenerationError exception."""

    def test_spdx_generation_error_is_exception(self):
        """Test that SPDXGenerationError is an Exception subclass."""
        assert issubclass(SPDXGenerationError, Exception)

    def test_spdx_generation_error_can_be_raised(self):
        """Test that SPDXGenerationError can be raised and caught."""
        with pytest.raises(SPDXGenerationError):
            raise SPDXGenerationError("Test error")

    def test_spdx_generation_error_message(self):
        """Test that SPDXGenerationError preserves error message."""
        error_msg = "Test SPDX generation error"
        with pytest.raises(SPDXGenerationError, match=error_msg):
            raise SPDXGenerationError(error_msg)
