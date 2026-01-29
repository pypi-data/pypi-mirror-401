"""
SPDX and CycloneDX document validator with detailed error reporting.

This module provides validation functions for SBOM documents against official schemas.
Integrated with progress tracking callbacks for real-time feedback.
"""

import json
from json import JSONDecodeError
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

try:
    from spdx_tools.spdx.model import Document
    from spdx_tools.spdx.parser.error import SPDXParsingError
    from spdx_tools.spdx.parser.parse_anything import parse_file
    # spdx-tools 0.8.x uses validate_full_spdx_document
    try:
        from spdx_tools.spdx.validation.document_validator import validate_full_spdx_document
        _validate_func = validate_full_spdx_document
    except ImportError:
        # Older versions might use validate_document
        try:
            from spdx_tools.spdx.validation import validate_document
            _validate_func = validate_document
        except ImportError:
            _validate_func = None
            SPDX_TOOLS_AVAILABLE = False
    SPDX_TOOLS_AVAILABLE = True
except ImportError:
    SPDX_TOOLS_AVAILABLE = False
    _validate_func = None
    # Type fallback for TYPE_CHECKING to avoid NameError
    if TYPE_CHECKING:
        from spdx_tools.spdx.model import Document  # type: ignore
    else:
        # Runtime fallback - use object as base type
        Document = object  # type: ignore

try:
    import jsonschema
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False

from .progress_state import StageState


class ValidationError(Exception):
    """Custom exception for validation errors with detailed context."""

    def __init__(
        self,
        message: str,
        errors: Optional[List[str]] = None,
        file_path: Optional[str] = None,
    ):
        """
        Initialize validation error.

        Args:
            message: Human-readable error message
            errors: List of specific validation error messages
            file_path: Optional path to the file being validated
        """
        self.message = message
        self.errors = errors or []
        self.file_path = file_path
        super().__init__(self.message)


class ValidationResult:
    """Result of SBOM validation with detailed error information."""

    def __init__(
        self,
        is_valid: bool,
        errors: Optional[List[str]] = None,
        warnings: Optional[List[str]] = None,
        error_details: Optional[List[Dict[str, Any]]] = None,
        file_path: Optional[str] = None,
    ):
        """
        Initialize validation result.

        Args:
            is_valid: Whether the document passed validation
            errors: List of validation error messages (formatted for display)
            warnings: List of validation warning messages
            error_details: List of detailed error dictionaries with field paths
            file_path: Optional path to the validated file
        """
        self.is_valid = is_valid
        self.errors = errors or []
        self.warnings = warnings or []
        self.error_details = error_details or []
        self.file_path = file_path

    def __bool__(self) -> bool:
        """Allow truthy checking of validation result."""
        return self.is_valid

    def __repr__(self) -> str:
        """String representation of validation result."""
        if self.is_valid:
            return f"ValidationResult(valid=True, warnings={len(self.warnings)})"
        else:
            return f"ValidationResult(valid=False, errors={len(self.errors)}, warnings={len(self.warnings)})"

    def get_error_summary(self) -> str:
        """
        Get a formatted error summary with field locations.

        Returns:
            Formatted string with all errors and their locations
        """
        if self.is_valid:
            return "Validation passed successfully"

        lines = []
        if self.file_path:
            lines.append(f"File: {self.file_path}")
        lines.append(f"Validation failed with {len(self.errors)} error(s):")
        lines.append("")

        for i, error_detail in enumerate(self.error_details, 1):
            location = error_detail.get("location", "unknown")
            field = error_detail.get("field", "unknown")
            message = error_detail.get("message", "")
            severity = error_detail.get("severity", "error")

            lines.append(f"{i}. [{severity.upper()}] {field}")
            lines.append(f"   Location: {location}")
            lines.append(f"   Issue: {message}")
            lines.append("")

        return "\n".join(lines)


def validate_spdx_document(
    document_path: Optional[str] = None,
    document: Optional[Document] = None,
    progress_callback: Optional[Callable] = None,
) -> ValidationResult:
    """
    Validate an SPDX document against SPDX 2.3 specification.

    This function performs comprehensive validation including:
    1. Document parsing and structure validation (0-30%)
    2. Schema validation (30-60%)
    3. Field constraint validation (60-90%)
    4. Result compilation (90-100%)

    Args:
        document_path: Path to SPDX file (JSON, XML, YAML, or Tag-Value)
        document: SPDX Document object (alternative to document_path)
        progress_callback: Optional callback for progress updates
            Signature: (stage_id, state, progress, processed_items, total_items, result, error_message)

    Returns:
        ValidationResult with validation status and detailed error messages

    Raises:
        RuntimeError: If spdx-tools library is not installed
        ValueError: If neither document_path nor document is provided, or if both are provided
        ValidationError: If document parsing fails

    Example:
        >>> result = validate_spdx_document(document_path="sbom.spdx.json")
        >>> if result:
        ...     print("SBOM is valid!")
        ... else:
        ...     for error in result.errors:
        ...         print(f"Error: {error}")
    """
    # Check if spdx-tools is available
    if not SPDX_TOOLS_AVAILABLE:
        raise RuntimeError(
            "spdx-tools library is not installed. Install with: pip install spdx-tools"
        )

    # Validate arguments
    if document_path is None and document is None:
        raise ValueError("Either document_path or document must be provided")
    if document_path is not None and document is not None:
        raise ValueError("Only one of document_path or document should be provided")

    # ========================================
    # STAGE 1: Document Parsing (0-30%)
    # ========================================
    if progress_callback:
        progress_callback(
            stage_id=1,
            state=StageState.ACTIVE,
            progress=0,
        )

    try:
        if document_path:
            doc = _parse_spdx_file(document_path, progress_callback)
        else:
            doc = document
    except Exception as e:
        if progress_callback:
            progress_callback(
                stage_id=1,
                state=StageState.FAILED,
                error_message=f"Document parsing failed: {str(e)}",
            )
        raise ValidationError(
            f"Failed to parse SPDX document: {str(e)}",
            file_path=document_path,
        )

    if progress_callback:
        progress_callback(
            stage_id=1,
            state=StageState.COMPLETE,
            progress=30,
        )

    # ========================================
    # STAGE 2: Schema Validation (30-60%)
    # ========================================
    if progress_callback:
        progress_callback(
            stage_id=2,
            state=StageState.ACTIVE,
            progress=30,
        )

    try:
        validation_messages = _validate_func(doc)
    except Exception as e:
        if progress_callback:
            progress_callback(
                stage_id=2,
                state=StageState.FAILED,
                error_message=f"Schema validation failed: {str(e)}",
            )
        # Return validation result with the exception as an error
        return ValidationResult(
            is_valid=False,
            errors=[f"Schema validation exception: {str(e)}"],
            error_details=[{
                "field": "schema",
                "location": document_path or "in-memory",
                "message": str(e),
                "severity": "error",
            }],
            file_path=document_path,
        )

    if progress_callback:
        progress_callback(
            stage_id=2,
            state=StageState.COMPLETE,
            progress=60,
        )

    # ========================================
    # STAGE 3: Error Classification (60-90%)
    # ========================================
    if progress_callback:
        progress_callback(
            stage_id=3,
            state=StageState.ACTIVE,
            progress=60,
        )

    errors = []
    warnings = []
    error_details = []

    for validation_message in validation_messages:
        message = str(validation_message)

        # Extract detailed error information
        error_detail = _format_spdx_validation_message(
            validation_message,
            document_path,
        )
        error_details.append(error_detail)

        # Create formatted error message
        formatted_message = _format_error_message(error_detail)
        errors.append(formatted_message)

    if progress_callback:
        progress_callback(
            stage_id=3,
            state=StageState.COMPLETE,
            progress=90,
        )

    # ========================================
    # STAGE 4: Result Compilation (90-100%)
    # ========================================
    is_valid = len(errors) == 0

    result = ValidationResult(
        is_valid=is_valid,
        errors=errors,
        warnings=warnings,
        error_details=error_details,
        file_path=document_path,
    )

    if progress_callback:
        progress_callback(
            stage_id=4,
            state=StageState.COMPLETE,
            progress=100,
            result="Valid" if is_valid else f"Invalid with {len(errors)} error(s)",
        )

    return result


def _format_spdx_validation_message(
    validation_message: Any,
    file_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Format SPDX validation message into detailed error structure.

    Args:
        validation_message: SPDX validation message object
        file_path: Optional path to the validated file

    Returns:
        Dictionary with detailed error information including field path and location
    """
    # Extract message and context
    message = str(validation_message)

    # Extract context information
    context_parts = []
    field_path = "unknown"

    if hasattr(validation_message, 'validation_context'):
        context = validation_message.validation_context
        if context:
            context_str = str(context)
            # Parse context to extract field path
            # SPDX tools typically use format like "spdx_id: field_name"
            if ':' in context_str:
                parts = context_str.split(':', 1)
                field_path = parts[1].strip() if len(parts) > 1 else parts[0]
            else:
                field_path = context_str
            context_parts.append(context_str)

    # Build location string
    location = file_path or "in-memory"
    if context_parts:
        location = f"{location} -> {' -> '.join(context_parts)}"

    # Determine severity
    severity = "error"

    return {
        "field": field_path,
        "location": location,
        "message": message,
        "severity": severity,
        "context": context_parts,
    }


def _format_error_message(error_detail: Dict[str, Any]) -> str:
    """
    Format error detail into human-readable error message.

    Args:
        error_detail: Dictionary with detailed error information

    Returns:
        Formatted error message string
    """
    field = error_detail.get("field", "unknown")
    message = error_detail.get("message", "")
    location = error_detail.get("location", "")

    if location and location != field:
        return f"[{field}] {message} (at {location})"
    else:
        return f"[{field}] {message}"


def _parse_spdx_file(
    file_path: str,
    progress_callback: Optional[Callable] = None,
) -> Document:
    """
    Parse SPDX file and return Document object.

    Args:
        file_path: Path to SPDX file
        progress_callback: Optional progress callback

    Returns:
        SPDX Document object

    Raises:
        FileNotFoundError: If file does not exist
        SPDXParsingError: If file parsing fails
        ValidationError: If file is not valid SPDX
    """
    path = Path(file_path)

    # Check file exists
    if not path.exists():
        raise ValidationError(
            f"SPDX file not found: {file_path}",
            file_path=file_path,
        )

    # Check file is not empty
    if path.stat().st_size == 0:
        raise ValidationError(
            f"SPDX file is empty: {file_path}",
            file_path=file_path,
        )

    try:
        # Parse using spdx-tools (auto-detects format)
        doc = parse_file(str(path))
        return doc
    except SPDXParsingError as e:
        # Re-raise SPDX parsing errors with context
        raise ValidationError(
            f"SPDX parsing error: {str(e)}",
            file_path=file_path,
        )
    except JSONDecodeError as e:
        raise ValidationError(
            f"Invalid JSON in SPDX file: {str(e)}",
            file_path=file_path,
        )
    except Exception as e:
        # Wrap other exceptions
        raise ValidationError(
            f"Failed to parse SPDX file: {str(e)}",
            file_path=file_path,
        )


def validate_spdx_document_strict(
    document_path: Optional[str] = None,
    document: Optional[Document] = None,
    progress_callback: Optional[Callable] = None,
) -> bool:
    """
    Strict validation that raises exception on invalid documents.

    This is a convenience wrapper around validate_spdx_document() that
    raises ValidationError instead of returning ValidationResult.

    Args:
        document_path: Path to SPDX file
        document: SPDX Document object
        progress_callback: Optional progress callback

    Returns:
        True if document is valid

    Raises:
        ValidationError: If document is invalid
        RuntimeError: If spdx-tools library is not installed
        ValueError: If arguments are invalid

    Example:
        >>> try:
        ...     validate_spdx_document_strict(document_path="sbom.spdx.json")
        ...     print("SBOM is valid!")
        ... except ValidationError as e:
        ...     print(f"Validation failed: {e}")
    """
    result = validate_spdx_document(
        document_path=document_path,
        document=document,
        progress_callback=progress_callback,
    )

    if not result.is_valid:
        error_message = f"SPDX validation failed with {len(result.errors)} error(s)"
        if result.errors:
            error_message += ":\n" + "\n".join(f"  - {err}" for err in result.errors)
        raise ValidationError(error_message, errors=result.errors)

    return True


def _get_cyclonedx_schema() -> Dict[str, Any]:
    """
    Get the CycloneDX 1.5 JSON schema.

    Returns:
        CycloneDX 1.5 JSON schema as a dictionary

    Raises:
        RuntimeError: If jsonschema library is not installed
    """
    if not JSONSCHEMA_AVAILABLE:
        raise RuntimeError(
            "jsonschema library is not installed. Install with: pip install jsonschema"
        )

    # CycloneDX 1.5 JSON schema
    # This is a simplified schema for basic validation
    # For production use, download the full schema from:
    # https://cyclonedx.org/schema/bom-1.5.schema.json
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://cyclonedx.org/schema/bom-1.5.schema.json",
        "title": "CycloneDX Software Bill-of-Materials Specification",
        "type": "object",
        "required": ["bomFormat", "specVersion", "version"],
        "properties": {
            "bomFormat": {
                "type": "string",
                "enum": ["CycloneDX"],
                "description": "The format of the BOM"
            },
            "specVersion": {
                "type": "string",
                "pattern": "^1\\.5$",
                "description": "The CycloneDX specification version"
            },
            "version": {
                "type": "integer",
                "minimum": 1,
                "description": "The BOM version"
            },
            "metadata": {
                "type": "object",
                "properties": {
                    "timestamp": {
                        "type": "string",
                        "format": "date-time"
                    },
                    "tools": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "vendor": {"type": "string"},
                                "name": {"type": "string"},
                                "version": {"type": "string"}
                            }
                        }
                    },
                    "component": {
                        "type": "object",
                        "required": ["type", "name", "bom-ref"],
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["application", "library", "framework", "container", "platform", "operating-system", "device", "firmware", "file"]
                            },
                            "name": {"type": "string"},
                            "version": {"type": "string"},
                            "bom-ref": {"type": "string"},
                            "purl": {"type": "string"},
                            "licenses": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "license": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "components": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["type", "name", "bom-ref"],
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": ["application", "library", "framework", "container", "platform", "operating-system", "device", "firmware", "file"]
                        },
                        "name": {"type": "string"},
                        "version": {"type": "string"},
                        "bom-ref": {"type": "string"},
                        "purl": {"type": "string"},
                        "licenses": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "license": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    return schema


def validate_cyclonedx_json(
    document_path: Optional[str] = None,
    document: Optional[Dict[str, Any]] = None,
    progress_callback: Optional[Callable] = None,
) -> ValidationResult:
    """
    Validate a CycloneDX JSON document against CycloneDX 1.5 specification.

    This function performs comprehensive validation including:
    1. Document parsing and structure validation (0-30%)
    2. Schema validation (30-70%)
    3. Field constraint validation (70-90%)
    4. Result compilation (90-100%)

    Args:
        document_path: Path to CycloneDX JSON file
        document: CycloneDX document as dictionary (alternative to document_path)
        progress_callback: Optional callback for progress updates
            Signature: (stage_id, state, progress, processed_items, total_items, result, error_message)

    Returns:
        ValidationResult with validation status and detailed error messages

    Raises:
        RuntimeError: If jsonschema library is not installed
        ValueError: If neither document_path nor document is provided, or if both are provided
        ValidationError: If document parsing fails

    Example:
        >>> result = validate_cyclonedx_json(document_path="sbom.cyclonedx.json")
        >>> if result:
        ...     print("SBOM is valid!")
        ... else:
        ...     for error in result.errors:
        ...         print(f"Error: {error}")
    """
    # Check if jsonschema is available
    if not JSONSCHEMA_AVAILABLE:
        raise RuntimeError(
            "jsonschema library is not installed. Install with: pip install jsonschema"
        )

    # Validate arguments
    if document_path is None and document is None:
        raise ValueError("Either document_path or document must be provided")
    if document_path is not None and document is not None:
        raise ValueError("Only one of document_path or document should be provided")

    # ========================================
    # STAGE 1: Document Parsing (0-30%)
    # ========================================
    if progress_callback:
        progress_callback(
            stage_id=1,
            state=StageState.ACTIVE,
            progress=0,
        )

    try:
        if document_path:
            doc = _parse_cyclonedx_file(document_path, progress_callback)
        else:
            doc = document
    except Exception as e:
        if progress_callback:
            progress_callback(
                stage_id=1,
                state=StageState.FAILED,
                error_message=f"Document parsing failed: {str(e)}",
            )
        raise ValidationError(
            f"Failed to parse CycloneDX document: {str(e)}",
            file_path=document_path,
        )

    if progress_callback:
        progress_callback(
            stage_id=1,
            state=StageState.COMPLETE,
            progress=30,
        )

    # ========================================
    # STAGE 2: Schema Validation (30-70%)
    # ========================================
    if progress_callback:
        progress_callback(
            stage_id=2,
            state=StageState.ACTIVE,
            progress=30,
        )

    try:
        schema = _get_cyclonedx_schema()
        validator = jsonschema.Draft7Validator(schema)
        errors = list(validator.iter_errors(doc))
    except Exception as e:
        if progress_callback:
            progress_callback(
                stage_id=2,
                state=StageState.FAILED,
                error_message=f"Schema validation failed: {str(e)}",
            )
        # Return validation result with the exception as an error
        return ValidationResult(
            is_valid=False,
            errors=[f"Schema validation exception: {str(e)}"],
            error_details=[{
                "field": "schema",
                "location": document_path or "in-memory",
                "message": str(e),
                "severity": "error",
            }],
            file_path=document_path,
        )

    if progress_callback:
        progress_callback(
            stage_id=2,
            state=StageState.COMPLETE,
            progress=70,
        )

    # ========================================
    # STAGE 3: Error Classification (70-90%)
    # ========================================
    if progress_callback:
        progress_callback(
            stage_id=3,
            state=StageState.ACTIVE,
            progress=70,
        )

    formatted_errors = []
    warnings = []
    error_details = []

    for error in errors:
        # Build detailed error information
        error_detail = _format_cyclonedx_validation_error(
            error,
            document_path,
        )
        error_details.append(error_detail)

        # Build error path
        path = " -> ".join(str(p) for p in error.path) if error.path else "root"
        formatted_message = f"[{path}] {error.message}"
        formatted_errors.append(formatted_message)

    if progress_callback:
        progress_callback(
            stage_id=3,
            state=StageState.COMPLETE,
            progress=90,
        )

    # ========================================
    # STAGE 4: Result Compilation (90-100%)
    # ========================================
    is_valid = len(formatted_errors) == 0

    result = ValidationResult(
        is_valid=is_valid,
        errors=formatted_errors,
        warnings=warnings,
        error_details=error_details,
        file_path=document_path,
    )

    if progress_callback:
        progress_callback(
            stage_id=4,
            state=StageState.COMPLETE,
            progress=100,
            result="Valid" if is_valid else f"Invalid with {len(formatted_errors)} error(s)",
        )

    return result


def _format_cyclonedx_validation_error(
    error: Any,
    file_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Format CycloneDX validation error into detailed error structure.

    Args:
        error: jsonschema validation error object
        file_path: Optional path to the validated file

    Returns:
        Dictionary with detailed error information including field path and location
    """
    # Build field path from jsonschema error path
    path_parts = list(error.path) if error.path else []
    field_path = " -> ".join(str(p) for p in path_parts) if path_parts else "root"

    # Build location string
    location = file_path or "in-memory"
    if path_parts:
        location = f"{location} -> {field_path}"

    # Get error message
    message = error.message

    # Determine severity based on validator type
    severity = "error"

    return {
        "field": field_path,
        "location": location,
        "message": message,
        "severity": severity,
        "context": {
            "validator": error.validator,
            "validator_value": str(error.validator_value) if error.validator_value else None,
        },
    }


def _parse_cyclonedx_file(
    file_path: str,
    progress_callback: Optional[Callable] = None,
) -> Dict[str, Any]:
    """
    Parse CycloneDX JSON file and return dictionary.

    Args:
        file_path: Path to CycloneDX JSON file
        progress_callback: Optional progress callback

    Returns:
        CycloneDX document as dictionary

    Raises:
        FileNotFoundError: If file does not exist
        ValidationError: If file is not valid JSON or CycloneDX
    """
    path = Path(file_path)

    # Check file exists
    if not path.exists():
        raise ValidationError(
            f"CycloneDX file not found: {file_path}",
            file_path=file_path,
        )

    # Check file is not empty
    if path.stat().st_size == 0:
        raise ValidationError(
            f"CycloneDX file is empty: {file_path}",
            file_path=file_path,
        )

    try:
        with open(path, 'r', encoding='utf-8') as f:
            doc = json.load(f)
    except JSONDecodeError as e:
        raise ValidationError(
            f"Invalid JSON in CycloneDX file: {str(e)}",
            file_path=file_path,
        )
    except Exception as e:
        raise ValidationError(
            f"Failed to parse CycloneDX file: {str(e)}",
            file_path=file_path,
        )

    # Verify it's a CycloneDX document
    if not isinstance(doc, dict):
        raise ValidationError(
            "CycloneDX document must be a JSON object",
            file_path=file_path,
        )

    if "bomFormat" not in doc:
        raise ValidationError(
            "Missing required field 'bomFormat' in CycloneDX document",
            file_path=file_path,
        )

    if doc["bomFormat"] != "CycloneDX":
        raise ValidationError(
            f"Invalid bomFormat '{doc['bomFormat']}', expected 'CycloneDX'",
            file_path=file_path,
        )

    return doc
