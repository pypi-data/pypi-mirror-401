"""
Test detailed error reporting structure.

This test verifies the error reporting data structures and formatting
without requiring full spdx-tools integration.
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# Import directly from the module
import binary_sbom.validator as validator


def test_validation_result_structure():
    """Test ValidationResult has the correct structure."""
    result = validator.ValidationResult(
        is_valid=False,
        errors=["Test error"],
        warnings=["Test warning"],
        error_details=[
            {
                "field": "test_field",
                "location": "test_location",
                "message": "Test error message",
                "severity": "error",
            }
        ],
        file_path="/path/to/file.json",
    )

    # Check basic properties
    assert result.is_valid == False
    assert len(result.errors) == 1
    assert len(result.warnings) == 1
    assert result.file_path == "/path/to/file.json"

    # Check error_details structure
    assert len(result.error_details) == 1
    error_detail = result.error_details[0]
    assert "field" in error_detail
    assert "location" in error_detail
    assert "message" in error_detail
    assert "severity" in error_detail

    print("✓ ValidationResult structure is correct")


def test_validation_error_structure():
    """Test ValidationError has the correct structure."""
    error = validator.ValidationError(
        message="Test error",
        errors=["Error 1", "Error 2"],
        file_path="/path/to/file.json",
    )

    assert error.message == "Test error"
    assert len(error.errors) == 2
    assert error.file_path == "/path/to/file.json"
    assert str(error) == "Test error"

    print("✓ ValidationError structure is correct")


def test_error_summary_format():
    """Test error summary formatting."""
    result = validator.ValidationResult(
        is_valid=False,
        errors=["Error 1", "Error 2"],
        error_details=[
            {
                "field": "packages[0].SPDXID",
                "location": "/path/to/file.json -> packages[0]",
                "message": "Missing required field",
                "severity": "error",
            },
            {
                "field": "packages[1].name",
                "location": "/path/to/file.json -> packages[1]",
                "message": "Invalid name format",
                "severity": "error",
            },
        ],
        file_path="/path/to/file.json",
    )

    summary = result.get_error_summary()

    # Check that summary contains expected information
    assert "Validation failed" in summary
    assert "2 error" in summary
    assert "/path/to/file.json" in summary
    assert "packages[0].SPDXID" in summary
    assert "packages[1].name" in summary
    assert "Missing required field" in summary
    assert "Invalid name format" in summary

    print("\n✓ Error summary format includes field paths and locations")
    print("\n=== Sample Error Summary ===")
    print(summary)
    print("============================\n")


def test_spdx_error_formatting():
    """Test SPDX validation message formatting."""
    # Create a mock validation message object
    class MockValidationMessage:
        def __init__(self, message, context=None):
            self.message = message
            self.validation_context = context

        def __str__(self):
            return self.message

    mock_msg = MockValidationMessage(
        "Field must not be empty",
        "SPDXRef-Package: downloadLocation"
    )

    error_detail = validator._format_spdx_validation_message(
        mock_msg,
        "/path/to/file.json"
    )

    # Verify error detail structure
    assert "field" in error_detail
    assert "location" in error_detail
    assert "message" in error_detail
    assert "severity" in error_detail

    # Check that field path was extracted correctly
    assert "downloadLocation" in error_detail["field"]
    assert "/path/to/file.json" in error_detail["location"]

    print("✓ SPDX error formatting extracts field paths correctly")
    print(f"  Field: {error_detail['field']}")
    print(f"  Location: {error_detail['location']}")
    print(f"  Message: {error_detail['message']}")


def test_cyclonedx_error_formatting():
    """Test CycloneDX validation error formatting."""
    # Create a mock jsonschema error
    class MockPath:
        def __init__(self, path):
            self.path = path

        def __iter__(self):
            return iter(self.path)

    class MockValidationError:
        def __init__(self, message, path, validator_type):
            self.message = message
            self.path = path
            self.validator = validator_type
            self.validator_value = "required"

    mock_error = MockValidationError(
        "'bomFormat' is a required property",
        ["bomFormat"],
        "required"
    )

    error_detail = validator._format_cyclonedx_validation_error(
        mock_error,
        "/path/to/file.json"
    )

    # Verify error detail structure
    assert "field" in error_detail
    assert "location" in error_detail
    assert "message" in error_detail
    assert "severity" in error_detail

    # Check that field path was extracted correctly
    assert error_detail["field"] == "bomFormat"
    assert "/path/to/file.json" in error_detail["location"]
    assert "bomFormat" in error_detail["location"]

    print("✓ CycloneDX error formatting extracts field paths correctly")
    print(f"  Field: {error_detail['field']}")
    print(f"  Location: {error_detail['location']}")
    print(f"  Message: {error_detail['message']}")


def test_valid_result_summary():
    """Test summary for valid result."""
    result = validator.ValidationResult(is_valid=True)

    summary = result.get_error_summary()

    assert "passed successfully" in summary
    assert "failed" not in summary

    print("✓ Valid result summary is correct")
    print(f"  Summary: {summary}")


if __name__ == "__main__":
    print("Testing error reporting structures...\n")

    test_validation_result_structure()
    test_validation_error_structure()
    test_error_summary_format()
    test_spdx_error_formatting()
    test_cyclonedx_error_formatting()
    test_valid_result_summary()

    print("\n" + "=" * 60)
    print("ALL STRUCTURE TESTS PASSED")
    print("=" * 60)
    print("\nThe error reporting code has been enhanced with:")
    print("  ✓ Field path extraction (e.g., 'packages[0].SPDXID')")
    print("  ✓ File location tracking")
    print("  ✓ Detailed error information structure")
    print("  ✓ Formatted error summaries")
    print("  ✓ Severity classification")
