"""
Unit tests for the SPDX and CycloneDX validator module.

Tests SBOM validation functionality including SPDX 2.3 and CycloneDX 1.5 validation,
error reporting, and progress tracking.
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch
from unittest.mock import patch as mock_patch

import pytest

import binary_sbom.validator
from binary_sbom.validator import (
    ValidationError,
    ValidationResult,
    _format_cyclonedx_validation_error,
    _format_error_message,
    _format_spdx_validation_message,
    _get_cyclonedx_schema,
    _parse_cyclonedx_file,
    _parse_spdx_file,
    validate_cyclonedx_json,
    validate_spdx_document,
    validate_spdx_document_strict,
)


class TestValidationError:
    """Test ValidationError exception."""

    def test_validation_error_is_exception(self):
        """Test that ValidationError is an Exception subclass."""
        assert issubclass(ValidationError, Exception)

    def test_validation_error_basic_init(self):
        """Test basic ValidationError initialization."""
        error = ValidationError("Test error")
        assert error.message == "Test error"
        assert error.errors == []
        assert error.file_path is None
        assert str(error) == "Test error"

    def test_validation_error_with_errors(self):
        """Test ValidationError with error list."""
        errors = ["Error 1", "Error 2"]
        error = ValidationError("Test error", errors=errors)
        assert error.errors == errors

    def test_validation_error_with_file_path(self):
        """Test ValidationError with file path."""
        error = ValidationError("Test error", file_path="/path/to/file.json")
        assert error.file_path == "/path/to/file.json"

    def test_validation_error_all_parameters(self):
        """Test ValidationError with all parameters."""
        errors = ["Error 1"]
        error = ValidationError("Test error", errors=errors, file_path="/path/to/file.json")
        assert error.message == "Test error"
        assert error.errors == errors
        assert error.file_path == "/path/to/file.json"

    def test_validation_error_can_be_raised(self):
        """Test that ValidationError can be raised and caught."""
        with pytest.raises(ValidationError, match="Test error"):
            raise ValidationError("Test error")


class TestValidationResult:
    """Test ValidationResult class."""

    def test_validation_result_valid(self):
        """Test ValidationResult for valid document."""
        result = ValidationResult(is_valid=True)
        assert result.is_valid is True
        assert result.errors == []
        assert result.warnings == []
        assert result.error_details == []
        assert result.file_path is None
        assert bool(result) is True

    def test_validation_result_invalid_with_errors(self):
        """Test ValidationResult for invalid document with errors."""
        errors = ["Error 1", "Error 2"]
        result = ValidationResult(is_valid=False, errors=errors)
        assert result.is_valid is False
        assert result.errors == errors
        assert bool(result) is False

    def test_validation_result_with_warnings(self):
        """Test ValidationResult with warnings."""
        warnings = ["Warning 1"]
        result = ValidationResult(is_valid=True, warnings=warnings)
        assert result.warnings == warnings

    def test_validation_result_with_error_details(self):
        """Test ValidationResult with error details."""
        error_details = [{"field": "name", "message": "Missing name"}]
        result = ValidationResult(is_valid=False, error_details=error_details)
        assert result.error_details == error_details

    def test_validation_result_with_file_path(self):
        """Test ValidationResult with file path."""
        result = ValidationResult(is_valid=True, file_path="/path/to/file.json")
        assert result.file_path == "/path/to/file.json"

    def test_validation_result_repr_valid(self):
        """Test ValidationResult repr for valid result."""
        result = ValidationResult(is_valid=True, warnings=["Warning 1"])
        repr_str = repr(result)
        assert "ValidationResult(valid=True" in repr_str
        assert "warnings=1" in repr_str

    def test_validation_result_repr_invalid(self):
        """Test ValidationResult repr for invalid result."""
        result = ValidationResult(is_valid=False, errors=["Error 1"], warnings=["Warning 1"])
        repr_str = repr(result)
        assert "ValidationResult(valid=False" in repr_str
        assert "errors=1" in repr_str
        assert "warnings=1" in repr_str

    def test_validation_result_get_error_summary_valid(self):
        """Test get_error_summary for valid result."""
        result = ValidationResult(is_valid=True)
        summary = result.get_error_summary()
        assert summary == "Validation passed successfully"

    def test_validation_result_get_error_summary_invalid(self):
        """Test get_error_summary for invalid result."""
        error_details = [
            {
                "field": "name",
                "location": "/path/to/file.json -> root",
                "message": "Missing required field",
                "severity": "error",
            }
        ]
        result = ValidationResult(
            is_valid=False,
            errors=["[name] Missing required field"],
            error_details=error_details,
            file_path="/path/to/file.json",
        )
        summary = result.get_error_summary()
        assert "File: /path/to/file.json" in summary
        assert "Validation failed with 1 error(s):" in summary
        assert "[ERROR] name" in summary
        assert "Location: /path/to/file.json -> root" in summary
        assert "Issue: Missing required field" in summary

    def test_validation_result_get_error_summary_multiple_errors(self):
        """Test get_error_summary with multiple errors."""
        error_details = [
            {
                "field": "name",
                "location": "root",
                "message": "Missing name",
                "severity": "error",
            },
            {
                "field": "version",
                "location": "root",
                "message": "Missing version",
                "severity": "error",
            },
        ]
        result = ValidationResult(
            is_valid=False,
            errors=["Error 1", "Error 2"],
            error_details=error_details,
        )
        summary = result.get_error_summary()
        assert "1. [ERROR] name" in summary
        assert "2. [ERROR] version" in summary


class TestValidateSpdxDocument:
    """Test SPDX document validation functionality."""

    @patch('binary_sbom.validator.SPDX_TOOLS_AVAILABLE', False)
    def test_validate_spdx_document_without_spdx_tools(self):
        """Test that missing spdx-tools raises RuntimeError."""
        with pytest.raises(RuntimeError, match='spdx-tools library is not installed'):
            validate_spdx_document(document_path="test.spdx.json")

    def test_validate_spdx_document_no_document(self):
        """Test that missing document_path and document raises ValueError."""
        with patch('binary_sbom.validator.SPDX_TOOLS_AVAILABLE', True):
            with pytest.raises(ValueError, match='Either document_path or document must be provided'):
                validate_spdx_document()

    def test_validate_spdx_document_both_document_and_path(self):
        """Test that providing both document_path and document raises ValueError."""
        with patch('binary_sbom.validator.SPDX_TOOLS_AVAILABLE', True):
            mock_doc = MagicMock()
            with pytest.raises(ValueError, match='Only one of document_path or document should be provided'):
                validate_spdx_document(document_path="test.spdx.json", document=mock_doc)

    @patch('binary_sbom.validator._parse_spdx_file')
    def test_validate_spdx_document_parsing_failure(self, mock_parse):
        """Test that parsing failure raises ValidationError."""
        with patch('binary_sbom.validator.SPDX_TOOLS_AVAILABLE', True):
            mock_parse.side_effect = Exception("Parsing failed")
            with pytest.raises(ValidationError, match='Failed to parse SPDX document'):
                validate_spdx_document(document_path="test.spdx.json")

    @patch('binary_sbom.validator._parse_spdx_file')
    def test_validate_spdx_document_valid(self, mock_parse):
        """Test successful validation of valid SPDX document."""
        mock_validate = MagicMock(return_value=[])
        with patch('binary_sbom.validator.SPDX_TOOLS_AVAILABLE', True):
            # Manually add validate_document to the module
            binary_sbom.validator.validate_document = mock_validate
            try:
                mock_doc = MagicMock()
                mock_parse.return_value = mock_doc

                result = validate_spdx_document(document_path="test.spdx.json")

                assert result.is_valid is True
                assert result.errors == []
                assert result.file_path == "test.spdx.json"
            finally:
                # Clean up
                delattr(binary_sbom.validator, 'validate_document')

    @patch('binary_sbom.validator._parse_spdx_file')
    def test_validate_spdx_document_invalid(self, mock_parse):
        """Test validation of invalid SPDX document with errors."""
        mock_error = MagicMock()
        mock_error.validation_context = "spdx_id: name"
        mock_error.__str__ = lambda self: "Field 'name' is required"
        mock_validate = MagicMock(return_value=[mock_error])

        with patch('binary_sbom.validator.SPDX_TOOLS_AVAILABLE', True):
            # Manually add validate_document to the module
            binary_sbom.validator.validate_document = mock_validate
            try:
                mock_doc = MagicMock()
                mock_parse.return_value = mock_doc

                result = validate_spdx_document(document_path="test.spdx.json")

                assert result.is_valid is False
                assert len(result.errors) > 0
                assert result.file_path == "test.spdx.json"
            finally:
                # Clean up
                delattr(binary_sbom.validator, 'validate_document')

    def test_validate_spdx_document_with_document_object(self):
        """Test validation with Document object instead of file path."""
        mock_validate = MagicMock(return_value=[])
        with patch('binary_sbom.validator.SPDX_TOOLS_AVAILABLE', True):
            # Manually add validate_document to the module
            binary_sbom.validator.validate_document = mock_validate
            try:
                mock_doc = MagicMock()

                result = validate_spdx_document(document=mock_doc)

                assert result.is_valid is True
                assert result.file_path is None
            finally:
                # Clean up
                delattr(binary_sbom.validator, 'validate_document')

    @patch('binary_sbom.validator._parse_spdx_file')
    def test_validate_spdx_document_with_progress_callback(self, mock_parse):
        """Test validation with progress callback."""
        mock_validate = MagicMock(return_value=[])
        with patch('binary_sbom.validator.SPDX_TOOLS_AVAILABLE', True):
            # Manually add validate_document to the module
            binary_sbom.validator.validate_document = mock_validate
            try:
                mock_doc = MagicMock()
                mock_parse.return_value = mock_doc

                progress_calls = []

                def progress_callback(**kwargs):
                    progress_calls.append(kwargs)

                result = validate_spdx_document(
                    document_path="test.spdx.json",
                    progress_callback=progress_callback
                )

                assert result.is_valid is True
                assert len(progress_calls) > 0

                # Check that progress was reported
                stages = [call['stage_id'] for call in progress_calls]
                assert 1 in stages  # Document parsing stage
                assert 2 in stages  # Schema validation stage
            finally:
                # Clean up
                delattr(binary_sbom.validator, 'validate_document')

    @patch('binary_sbom.validator._parse_spdx_file')
    def test_validate_spdx_document_schema_exception(self, mock_parse):
        """Test that schema validation exception is handled."""
        mock_validate = MagicMock(side_effect=Exception("Schema validation failed"))
        with patch('binary_sbom.validator.SPDX_TOOLS_AVAILABLE', True):
            # Manually add validate_document to the module
            binary_sbom.validator.validate_document = mock_validate
            try:
                mock_doc = MagicMock()
                mock_parse.return_value = mock_doc

                result = validate_spdx_document(document_path="test.spdx.json")

                assert result.is_valid is False
                assert len(result.errors) > 0
                assert "Schema validation exception" in result.errors[0]
            finally:
                # Clean up
                delattr(binary_sbom.validator, 'validate_document')


class TestValidateSpdxDocumentStrict:
    """Test strict SPDX validation that raises on errors."""

    @patch('binary_sbom.validator.SPDX_TOOLS_AVAILABLE', False)
    def test_validate_spdx_document_strict_without_spdx_tools(self):
        """Test that missing spdx-tools raises RuntimeError."""
        with pytest.raises(RuntimeError, match='spdx-tools library is not installed'):
            validate_spdx_document_strict(document_path="test.spdx.json")

    @patch('binary_sbom.validator.validate_spdx_document')
    def test_validate_spdx_document_strict_valid(self, mock_validate):
        """Test strict validation with valid document."""
        with patch('binary_sbom.validator.SPDX_TOOLS_AVAILABLE', True):
            mock_result = ValidationResult(is_valid=True)
            mock_validate.return_value = mock_result

            result = validate_spdx_document_strict(document_path="test.spdx.json")

            assert result is True

    @patch('binary_sbom.validator.validate_spdx_document')
    def test_validate_spdx_document_strict_invalid(self, mock_validate):
        """Test strict validation raises ValidationError on invalid document."""
        with patch('binary_sbom.validator.SPDX_TOOLS_AVAILABLE', True):
            mock_result = ValidationResult(
                is_valid=False,
                errors=["Error 1", "Error 2"]
            )
            mock_validate.return_value = mock_result

            with pytest.raises(ValidationError, match='SPDX validation failed with 2 error'):
                validate_spdx_document_strict(document_path="test.spdx.json")

    @patch('binary_sbom.validator.validate_spdx_document')
    def test_validate_spdx_document_strict_with_progress_callback(self, mock_validate):
        """Test strict validation with progress callback."""
        with patch('binary_sbom.validator.SPDX_TOOLS_AVAILABLE', True):
            mock_result = ValidationResult(is_valid=True)
            mock_validate.return_value = mock_result

            progress_mock = MagicMock()

            result = validate_spdx_document_strict(
                document_path="test.spdx.json",
                progress_callback=progress_mock
            )

            assert result is True
            mock_validate.assert_called_once()
            # Verify progress_callback was passed through
            call_kwargs = mock_validate.call_args[1]
            assert call_kwargs['progress_callback'] == progress_mock


class TestParseSpdxFile:
    """Test SPDX file parsing functionality."""

    @patch('binary_sbom.validator.SPDX_TOOLS_AVAILABLE', False)
    def test_parse_spdx_file_without_spdx_tools(self):
        """Test that missing spdx-tools raises RuntimeError in validate."""
        # This is tested through validate_spdx_document
        pass

    def test_parse_spdx_file_not_found(self):
        """Test that FileNotFoundError is raised for missing file."""
        with patch('binary_sbom.validator.SPDX_TOOLS_AVAILABLE', True):
            with pytest.raises(ValidationError, match='SPDX file not found'):
                _parse_spdx_file("/nonexistent/file.spdx.json")

    def test_parse_spdx_file_empty(self):
        """Test that ValidationError is raised for empty file."""
        with patch('binary_sbom.validator.SPDX_TOOLS_AVAILABLE', True):
            with tempfile.NamedTemporaryFile(delete=False) as f:
                temp_path = f.name

            try:
                with pytest.raises(ValidationError, match='SPDX file is empty'):
                    _parse_spdx_file(temp_path)
            finally:
                Path(temp_path).unlink()

    @patch('binary_sbom.validator.parse_file')
    def test_parse_spdx_file_spdx_parsing_error(self, mock_parse):
        """Test that SPDXParsingError is wrapped in ValidationError."""
        with patch('binary_sbom.validator.SPDX_TOOLS_AVAILABLE', True):
            from spdx_tools.spdx.parser.error import SPDXParsingError

            # Create a temporary file
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
                temp_path = f.name
                f.write('{}')

            try:
                mock_parse.side_effect = SPDXParsingError("Invalid SPDX format")

                with pytest.raises(ValidationError, match='SPDX parsing error'):
                    _parse_spdx_file(temp_path)
            finally:
                Path(temp_path).unlink()

    @patch('binary_sbom.validator.parse_file')
    def test_parse_spdx_file_json_decode_error(self, mock_parse):
        """Test that JSONDecodeError is wrapped in ValidationError."""
        with patch('binary_sbom.validator.SPDX_TOOLS_AVAILABLE', True):
            # Create a temporary file
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
                temp_path = f.name
                f.write('invalid json {')

            try:
                # Mock parse_file to raise JSONDecodeError
                from json import JSONDecodeError
                mock_parse.side_effect = JSONDecodeError("Invalid JSON", "<string>", 0)

                with pytest.raises(ValidationError, match='Invalid JSON in SPDX file'):
                    _parse_spdx_file(temp_path)
            finally:
                Path(temp_path).unlink()

    @patch('binary_sbom.validator.parse_file')
    def test_parse_spdx_file_success(self, mock_parse):
        """Test successful file parsing."""
        with patch('binary_sbom.validator.SPDX_TOOLS_AVAILABLE', True):
            # Create a temporary file
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
                temp_path = f.name
                f.write('{}')

            try:
                mock_doc = MagicMock()
                mock_parse.return_value = mock_doc

                result = _parse_spdx_file(temp_path)

                assert result == mock_doc
                mock_parse.assert_called_once()
            finally:
                Path(temp_path).unlink()


class TestFormatSpdxValidationMessage:
    """Test SPDX validation message formatting."""

    def test_format_spdx_validation_message_basic(self):
        """Test basic validation message formatting."""
        mock_message = MagicMock()
        mock_message.validation_context = None
        mock_message.__str__ = lambda self: "Test validation message"

        result = _format_spdx_validation_message(mock_message)

        assert result["field"] == "unknown"
        assert result["message"] == "Test validation message"
        assert result["severity"] == "error"
        assert result["location"] == "in-memory"

    def test_format_spdx_validation_message_with_context(self):
        """Test formatting with validation context."""
        mock_message = MagicMock()
        mock_message.validation_context = "spdx_id: name"
        mock_message.__str__ = lambda self: "Field 'name' is required"

        result = _format_spdx_validation_message(mock_message, "/path/to/file.json")

        assert result["field"] == "name"
        assert "spdx_id: name" in result["context"]
        assert "/path/to/file.json" in result["location"]

    def test_format_spdx_validation_message_with_file_path(self):
        """Test formatting with file path."""
        mock_message = MagicMock()
        mock_message.validation_context = None
        mock_message.__str__ = lambda self: "Test error"

        result = _format_spdx_validation_message(mock_message, "/test/file.spdx.json")

        assert result["location"] == "/test/file.spdx.json"

    def test_format_spdx_validation_message_context_without_colon(self):
        """Test context parsing when no colon present."""
        mock_message = MagicMock()
        mock_message.validation_context = "document_name"
        mock_message.__str__ = lambda self: "Test error"

        result = _format_spdx_validation_message(mock_message)

        assert result["field"] == "document_name"


class TestFormatErrorMessage:
    """Test error message formatting."""

    def test_format_error_message_basic(self):
        """Test basic error message formatting."""
        error_detail = {
            "field": "name",
            "message": "Field is required",
            "location": "root"
        }

        result = _format_error_message(error_detail)

        assert result == "[name] Field is required (at root)"

    def test_format_error_message_no_location(self):
        """Test formatting without location."""
        error_detail = {
            "field": "version",
            "message": "Must be a string",
        }

        result = _format_error_message(error_detail)

        assert result == "[version] Must be a string"

    def test_format_error_message_location_same_as_field(self):
        """Test formatting when location is same as field."""
        error_detail = {
            "field": "root",
            "message": "Invalid document",
            "location": "root"
        }

        result = _format_error_message(error_detail)

        assert result == "[root] Invalid document"


class TestValidateCyclonedxJson:
    """Test CycloneDX JSON validation functionality."""

    @patch('binary_sbom.validator.JSONSCHEMA_AVAILABLE', False)
    def test_validate_cyclonedx_json_without_jsonschema(self):
        """Test that missing jsonschema raises RuntimeError."""
        with pytest.raises(RuntimeError, match='jsonschema library is not installed'):
            validate_cyclonedx_json(document_path="test.cyclonedx.json")

    def test_validate_cyclonedx_json_no_document(self):
        """Test that missing document_path and document raises ValueError."""
        with patch('binary_sbom.validator.JSONSCHEMA_AVAILABLE', True):
            with pytest.raises(ValueError, match='Either document_path or document must be provided'):
                validate_cyclonedx_json()

    def test_validate_cyclonedx_json_both_document_and_path(self):
        """Test that providing both raises ValueError."""
        with patch('binary_sbom.validator.JSONSCHEMA_AVAILABLE', True):
            mock_doc = {}
            with pytest.raises(ValueError, match='Only one of document_path or document should be provided'):
                validate_cyclonedx_json(document_path="test.json", document=mock_doc)

    @patch('binary_sbom.validator._parse_cyclonedx_file')
    def test_validate_cyclonedx_json_parsing_failure(self, mock_parse):
        """Test that parsing failure raises ValidationError."""
        with patch('binary_sbom.validator.JSONSCHEMA_AVAILABLE', True):
            mock_parse.side_effect = Exception("Parsing failed")
            with pytest.raises(ValidationError, match='Failed to parse CycloneDX document'):
                validate_cyclonedx_json(document_path="test.json")

    @patch('jsonschema.Draft7Validator')
    @patch('binary_sbom.validator._get_cyclonedx_schema')
    @patch('binary_sbom.validator._parse_cyclonedx_file')
    def test_validate_cyclonedx_json_valid(self, mock_parse, mock_schema, mock_validator):
        """Test successful validation of valid CycloneDX document."""
        with patch('binary_sbom.validator.JSONSCHEMA_AVAILABLE', True):
            mock_doc = {
                "bomFormat": "CycloneDX",
                "specVersion": "1.5",
                "version": 1
            }
            mock_parse.return_value = mock_doc

            mock_schema_instance = MagicMock()
            mock_schema.return_value = {}
            mock_validator_instance = MagicMock()
            mock_validator_instance.iter_errors.return_value = []  # No errors
            mock_validator.return_value = mock_validator_instance

            result = validate_cyclonedx_json(document_path="test.json")

            assert result.is_valid is True
            assert result.errors == []

    @patch('jsonschema.Draft7Validator')
    @patch('binary_sbom.validator._get_cyclonedx_schema')
    @patch('binary_sbom.validator._parse_cyclonedx_file')
    def test_validate_cyclonedx_json_invalid(self, mock_parse, mock_schema, mock_validator):
        """Test validation of invalid CycloneDX document."""
        with patch('binary_sbom.validator.JSONSCHEMA_AVAILABLE', True):
            mock_doc = {
                "bomFormat": "Invalid",
            }
            mock_parse.return_value = mock_doc

            mock_schema.return_value = {}
            mock_validator_instance = MagicMock()
            mock_error = MagicMock()
            mock_error.path = ["bomFormat"]
            mock_error.message = "Must be 'CycloneDX'"
            mock_validator_instance.iter_errors.return_value = [mock_error]
            mock_validator.return_value = mock_validator_instance

            result = validate_cyclonedx_json(document_path="test.json")

            assert result.is_valid is False
            assert len(result.errors) > 0

    @patch('jsonschema.Draft7Validator')
    @patch('binary_sbom.validator._get_cyclonedx_schema')
    def test_validate_cyclonedx_json_with_document_object(self, mock_schema, mock_validator):
        """Test validation with document dict instead of file path."""
        with patch('binary_sbom.validator.JSONSCHEMA_AVAILABLE', True):
            mock_doc = {
                "bomFormat": "CycloneDX",
                "specVersion": "1.5",
                "version": 1
            }

            mock_schema.return_value = {}
            mock_validator_instance = MagicMock()
            mock_validator_instance.iter_errors.return_value = []
            mock_validator.return_value = mock_validator_instance

            result = validate_cyclonedx_json(document=mock_doc)

            assert result.is_valid is True
            assert result.file_path is None

    @patch('jsonschema.Draft7Validator')
    @patch('binary_sbom.validator._get_cyclonedx_schema')
    @patch('binary_sbom.validator._parse_cyclonedx_file')
    def test_validate_cyclonedx_json_with_progress_callback(self, mock_parse, mock_schema, mock_validator):
        """Test validation with progress callback."""
        with patch('binary_sbom.validator.JSONSCHEMA_AVAILABLE', True):
            mock_doc = {
                "bomFormat": "CycloneDX",
                "specVersion": "1.5",
                "version": 1
            }
            mock_parse.return_value = mock_doc

            mock_schema.return_value = {}
            mock_validator_instance = MagicMock()
            mock_validator_instance.iter_errors.return_value = []
            mock_validator.return_value = mock_validator_instance

            progress_calls = []

            def progress_callback(**kwargs):
                progress_calls.append(kwargs)

            result = validate_cyclonedx_json(
                document_path="test.json",
                progress_callback=progress_callback
            )

            assert result.is_valid is True
            assert len(progress_calls) > 0


class TestGetCyclonedxSchema:
    """Test CycloneDX schema retrieval."""

    @patch('binary_sbom.validator.JSONSCHEMA_AVAILABLE', False)
    def test_get_cyclonedx_schema_without_jsonschema(self):
        """Test that missing jsonschema raises RuntimeError."""
        with pytest.raises(RuntimeError, match='jsonschema library is not installed'):
            _get_cyclonedx_schema()

    def test_get_cyclonedx_schema_structure(self):
        """Test that schema has correct structure."""
        with patch('binary_sbom.validator.JSONSCHEMA_AVAILABLE', True):
            schema = _get_cyclonedx_schema()

            assert isinstance(schema, dict)
            assert "$schema" in schema
            assert "$id" in schema
            assert "title" in schema
            assert schema["type"] == "object"

            # Check required fields
            assert "required" in schema
            assert "bomFormat" in schema["required"]
            assert "specVersion" in schema["required"]
            assert "version" in schema["required"]

            # Check bomFormat property
            assert "bomFormat" in schema["properties"]
            assert schema["properties"]["bomFormat"]["type"] == "string"
            assert "CycloneDX" in schema["properties"]["bomFormat"]["enum"]


class TestFormatCyclonedxValidationError:
    """Test CycloneDX validation error formatting."""

    def test_format_cyclonedx_validation_error_basic(self):
        """Test basic error formatting."""
        mock_error = MagicMock()
        mock_error.path = ["name"]
        mock_error.message = "Field is required"
        mock_error.validator = "required"
        mock_error.validator_value = "name"

        result = _format_cyclonedx_validation_error(mock_error)

        assert result["field"] == "name"
        assert result["message"] == "Field is required"
        assert result["severity"] == "error"
        assert "name" in result["location"]

    def test_format_cyclonedx_validation_error_nested_path(self):
        """Test formatting with nested path."""
        mock_error = MagicMock()
        mock_error.path = ["metadata", "component", "name"]
        mock_error.message = "Invalid value"
        mock_error.validator = "pattern"
        mock_error.validator_value = "^[a-zA-Z]+$"

        result = _format_cyclonedx_validation_error(mock_error, "/test.json")

        assert result["field"] == "metadata -> component -> name"
        assert "/test.json" in result["location"]

    def test_format_cyclonedx_validation_error_no_path(self):
        """Test formatting with no path (root level error)."""
        mock_error = MagicMock()
        mock_error.path = []
        mock_error.message = "Missing required field"
        mock_error.validator = "required"
        mock_error.validator_value = None

        result = _format_cyclonedx_validation_error(mock_error)

        assert result["field"] == "root"
        assert result["location"] == "in-memory"


class TestParseCyclonedxFile:
    """Test CycloneDX file parsing functionality."""

    def test_parse_cyclonedx_file_not_found(self):
        """Test that FileNotFoundError is raised for missing file."""
        with patch('binary_sbom.validator.JSONSCHEMA_AVAILABLE', True):
            with pytest.raises(ValidationError, match='CycloneDX file not found'):
                _parse_cyclonedx_file("/nonexistent/file.json")

    def test_parse_cyclonedx_file_empty(self):
        """Test that ValidationError is raised for empty file."""
        with patch('binary_sbom.validator.JSONSCHEMA_AVAILABLE', True):
            with tempfile.NamedTemporaryFile(delete=False) as f:
                temp_path = f.name

            try:
                with pytest.raises(ValidationError, match='CycloneDX file is empty'):
                    _parse_cyclonedx_file(temp_path)
            finally:
                Path(temp_path).unlink()

    def test_parse_cyclonedx_file_invalid_json(self):
        """Test that invalid JSON raises ValidationError."""
        with patch('binary_sbom.validator.JSONSCHEMA_AVAILABLE', True):
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
                temp_path = f.name
                f.write('invalid json {')

            try:
                with pytest.raises(ValidationError, match='Invalid JSON'):
                    _parse_cyclonedx_file(temp_path)
            finally:
                Path(temp_path).unlink()

    def test_parse_cyclonedx_file_not_object(self):
        """Test that non-object JSON raises ValidationError."""
        with patch('binary_sbom.validator.JSONSCHEMA_AVAILABLE', True):
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
                temp_path = f.name
                f.write('["array", "values"]')

            try:
                with pytest.raises(ValidationError, match='must be a JSON object'):
                    _parse_cyclonedx_file(temp_path)
            finally:
                Path(temp_path).unlink()

    def test_parse_cyclonedx_file_missing_bom_format(self):
        """Test that missing bomFormat raises ValidationError."""
        with patch('binary_sbom.validator.JSONSCHEMA_AVAILABLE', True):
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
                temp_path = f.name
                f.write('{"specVersion": "1.5", "version": 1}')

            try:
                with pytest.raises(ValidationError, match="Missing required field 'bomFormat'"):
                    _parse_cyclonedx_file(temp_path)
            finally:
                Path(temp_path).unlink()

    def test_parse_cyclonedx_file_invalid_bom_format(self):
        """Test that invalid bomFormat raises ValidationError."""
        with patch('binary_sbom.validator.JSONSCHEMA_AVAILABLE', True):
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
                temp_path = f.name
                f.write('{"bomFormat": "InvalidFormat", "specVersion": "1.5", "version": 1}')

            try:
                with pytest.raises(ValidationError, match="Invalid bomFormat 'InvalidFormat'"):
                    _parse_cyclonedx_file(temp_path)
            finally:
                Path(temp_path).unlink()

    def test_parse_cyclonedx_file_success(self):
        """Test successful file parsing."""
        with patch('binary_sbom.validator.JSONSCHEMA_AVAILABLE', True):
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
                temp_path = f.name
                f.write('{"bomFormat": "CycloneDX", "specVersion": "1.5", "version": 1}')

            try:
                result = _parse_cyclonedx_file(temp_path)

                assert isinstance(result, dict)
                assert result["bomFormat"] == "CycloneDX"
                assert result["specVersion"] == "1.5"
                assert result["version"] == 1
            finally:
                Path(temp_path).unlink()
