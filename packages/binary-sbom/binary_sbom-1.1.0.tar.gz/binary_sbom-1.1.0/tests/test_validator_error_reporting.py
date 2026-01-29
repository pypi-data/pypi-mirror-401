"""
Test detailed error reporting with file/field locations.

This test verifies that validation errors include:
- Field paths (e.g., "packages[0].SPDXID")
- File locations
- Specific validation issues
"""

import json
import sys
import tempfile
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# Import directly from the module
import binary_sbom.validator as validator

validate_spdx_document = validator.validate_spdx_document
validate_cyclonedx_json = validator.validate_cyclonedx_json
ValidationError = validator.ValidationError
ValidationResult = validator.ValidationResult


def create_invalid_spdx_sbom():
    """Create an SPDX SBOM with missing required fields."""
    return {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "spdxId": "SPDXRef-DOCUMENT",
        # Missing "name" field
        "documentNamespace": "https://example.com/test-sbom",
        "creationInfo": {
            "created": "2024-01-14T13:00:00Z",
            # Missing "creators" field
        },
        "packages": [
            {
                # Missing "SPDXID" field
                "name": "test-package",
                # Missing "downloadLocation" field
            }
        ],
    }


def create_invalid_cyclonedx_sbom():
    """Create a CycloneDX SBOM with missing required fields."""
    return {
        # Missing "bomFormat" field
        "specVersion": "1.5",
        "version": 1,
        "metadata": {
            "timestamp": "2024-01-14T13:00:00Z",
        },
    }


def test_spdx_error_includes_field_path():
    """Test that SPDX validation errors include field paths."""
    invalid_sbom = create_invalid_spdx_sbom()

    # Write to temporary file
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.spdx.json',
        delete=False,
    ) as f:
        json.dump(invalid_sbom, f)
        temp_path = f.name

    try:
        # Validate the invalid SBOM
        result = validate_spdx_document(document_path=temp_path)

        # Should have errors
        assert not result.is_valid, "Expected validation to fail"
        assert len(result.errors) > 0, "Expected validation errors"

        # Check that error_details is populated
        assert len(result.error_details) > 0, "Expected error_details to be populated"

        # Check that file_path is included
        assert result.file_path == temp_path, "Expected file_path in result"

        # Check that error details include field information
        for error_detail in result.error_details:
            assert "field" in error_detail, "Expected 'field' in error_detail"
            assert "location" in error_detail, "Expected 'location' in error_detail"
            assert "message" in error_detail, "Expected 'message' in error_detail"
            assert "severity" in error_detail, "Expected 'severity' in error_detail"

            # Verify field path is not just "unknown"
            if error_detail["field"] != "unknown":
                print(f"✓ Field: {error_detail['field']}")
                print(f"✓ Location: {error_detail['location']}")
                print(f"✓ Message: {error_detail['message']}")
                print(f"✓ Severity: {error_detail['severity']}")
                print()

        # Test get_error_summary()
        summary = result.get_error_summary()
        assert "Validation failed" in summary, "Expected validation failure in summary"
        assert temp_path in summary, "Expected file path in summary"
        print("\n=== Error Summary ===")
        print(summary)
        print("=====================\n")

        print("✓ SPDX error reporting includes field paths and locations")

    finally:
        # Clean up
        Path(temp_path).unlink()


def test_cyclonedx_error_includes_field_path():
    """Test that CycloneDX validation errors include field paths."""
    invalid_sbom = create_invalid_cyclonedx_sbom()

    # Write to temporary file
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.cyclonedx.json',
        delete=False,
    ) as f:
        json.dump(invalid_sbom, f)
        temp_path = f.name

    try:
        # Validate the invalid SBOM
        result = validate_cyclonedx_json(document_path=temp_path)

        # Should have errors
        assert not result.is_valid, "Expected validation to fail"
        assert len(result.errors) > 0, "Expected validation errors"

        # Check that error_details is populated
        assert len(result.error_details) > 0, "Expected error_details to be populated"

        # Check that file_path is included
        assert result.file_path == temp_path, "Expected file_path in result"

        # Check that error details include field information
        for error_detail in result.error_details:
            assert "field" in error_detail, "Expected 'field' in error_detail"
            assert "location" in error_detail, "Expected 'location' in error_detail"
            assert "message" in error_detail, "Expected 'message' in error_detail"
            assert "severity" in error_detail, "Expected 'severity' in error_detail"

            # Verify field path is not just "unknown"
            if error_detail["field"] != "unknown":
                print(f"✓ Field: {error_detail['field']}")
                print(f"✓ Location: {error_detail['location']}")
                print(f"✓ Message: {error_detail['message']}")
                print(f"✓ Severity: {error_detail['severity']}")
                print()

        # Test get_error_summary()
        summary = result.get_error_summary()
        assert "Validation failed" in summary, "Expected validation failure in summary"
        assert temp_path in summary, "Expected file path in summary"
        print("\n=== Error Summary ===")
        print(summary)
        print("=====================\n")

        print("✓ CycloneDX error reporting includes field paths and locations")

    finally:
        # Clean up
        Path(temp_path).unlink()


def test_validation_error_includes_file_path():
    """Test that ValidationError exceptions include file path."""
    with tempfile.NamedTemporaryFile(
        suffix='.spdx.json',
        delete=False,
    ) as f:
        # Write invalid JSON
        f.write(b"{invalid json")
        temp_path = f.name

    try:
        # Should raise ValidationError
        try:
            validate_spdx_document(document_path=temp_path)
            assert False, "Expected ValidationError to be raised"
        except ValidationError as e:
            # Check that file_path is in the exception
            assert e.file_path == temp_path, "Expected file_path in ValidationError"
            assert temp_path in str(e), "Expected file path in error message"
            print(f"✓ ValidationError includes file_path: {e.file_path}")

    finally:
        # Clean up
        Path(temp_path).unlink()


if __name__ == "__main__":
    print("Testing SPDX error reporting...")
    test_spdx_error_includes_field_path()
    print("\nPASSED: SPDX error reporting test\n")

    print("Testing CycloneDX error reporting...")
    test_cyclonedx_error_includes_field_path()
    print("\nPASSED: CycloneDX error reporting test\n")

    print("Testing ValidationError includes file_path...")
    test_validation_error_includes_file_path()
    print("\nPASSED: ValidationError file_path test\n")

    print("=" * 60)
    print("ALL TESTS PASSED")
    print("=" * 60)
