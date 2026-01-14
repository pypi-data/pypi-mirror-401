"""
SPDX document generator module for Binary SBOM Generator.

This module provides functionality to generate SPDX 2.3 compliant documents
from binary metadata, supporting multiple output formats (JSON, XML, YAML, Tag-Value).
"""

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from spdx_tools.spdx.model import (
        Actor,
        ActorType,
        CreationInfo,
        Document,
        Package,
        SpdxNoAssertion,
    )

try:
    from spdx_tools.spdx.model import (  # noqa: F811
        Actor,
        ActorType,
        CreationInfo,
        Document,
        Package,
        SpdxNoAssertion,
    )
except ImportError:
    # Set dummy values for runtime when spdx-tools is not installed
    # These will never be used because we check for None in functions
    Actor = None  # type: ignore
    ActorType = None  # type: ignore
    CreationInfo = None  # type: ignore
    Document = None  # type: ignore
    Package = None  # type: ignore
    SpdxNoAssertion = None  # type: ignore


class SPDXGenerationError(Exception):
    """Exception raised when SPDX document generation fails."""

    pass


def create_spdx_document(
    metadata: Dict[str, Any],
    namespace: str = "https://example.com/sbom",
    creator: str = "Tool: binary-sbom-generator"
) -> Document:
    """
    Create SPDX 2.3 document from binary metadata.

    This function creates an SPDX Document object with the extracted binary
    metadata, including package information, dependencies, and section details.
    The document follows SPDX 2.3 specification and includes all required fields.

    Args:
        metadata: Dictionary containing binary metadata with keys:
            - name (str): Binary name
            - type (str): Binary format type (ELF, PE, MachO, Raw)
            - architecture (str): Target architecture
            - entrypoint (Optional[str]): Entry point address in hex
            - sections (List[Dict[str, Any]]): List of section information
            - dependencies (List[str]): List of imported libraries
        namespace: Namespace URI for the SPDX document
            (default: "https://example.com/sbom").
        creator: Creator string in format "Tool: tool-name"
            (default: "Tool: binary-sbom-generator").

    Returns:
        SPDX Document object containing:
        - Document-level metadata (name, namespace, creation info)
        - Package with binary information
        - Dependencies as external references or packages

    Raises:
        ImportError: If spdx-tools library is not installed.
        SPDXGenerationError: If document creation fails or required metadata is missing.
        ValueError: If metadata is invalid or missing required fields.

    Example:
        >>> metadata = {
        ...     'name': 'my-binary',
        ...     'type': 'ELF',
        ...     'architecture': 'x86_64',
        ...     'entrypoint': '0x4000',
        ...     'sections': [{'name': '.text', 'size': 1024}],
        ...     'dependencies': ['libc.so.6']
        ... }
        >>> doc = create_spdx_document(metadata)
        >>> doc.name
        'my-binary-SBOM'
        >>> len(doc.packages)
        1
    """
    if Document is None:
        raise ImportError(
            "spdx-tools library is required for SPDX generation. "
            "Install it with: pip install spdx-tools"
        )

    # Validate required metadata fields
    _validate_metadata(metadata)

    # Create package from binary metadata
    try:
        package = _create_package(metadata)
    except Exception as e:
        raise SPDXGenerationError(f"Failed to create SPDX package: {e}")

    # Parse creator string to create Actor (spdx-tools 0.8+ API)
    # Creator string format: "Tool: name" or "Person: name" or "Organization: name"
    try:
        if ActorType is None:
            raise ImportError("ActorType not available")
        if ":" in creator:
            actor_type_str, actor_name = creator.split(":", 1)
            actor_type_str = actor_type_str.strip().lower()
            if actor_type_str == "tool":
                actor_type = ActorType.TOOL
            elif actor_type_str == "person":
                actor_type = ActorType.PERSON
            elif actor_type_str == "organization":
                actor_type = ActorType.ORGANIZATION
            else:
                actor_type = ActorType.TOOL
        else:
            actor_type = ActorType.TOOL
            actor_name = creator

        creator_actor = Actor(actor_type=actor_type, name=actor_name.strip())
    except Exception as e:
        raise SPDXGenerationError(f"Failed to create creator actor: {e}")

    # Create document name and namespace
    document_name = f"{metadata['name']}-SBOM"
    if namespace.endswith('/'):
        document_namespace = f"{namespace}{metadata['name']}"
    else:
        document_namespace = f"{namespace}/{metadata['name']}"

    # Create creation info (spdx-tools 0.8+ API)
    try:
        creation_info = CreationInfo(
            spdx_version="SPDX-2.3",
            spdx_id="SPDXRef-DOCUMENT",
            name=document_name,
            document_namespace=document_namespace,
            creators=[creator_actor],
            created=datetime.now(),
        )
    except Exception as e:
        raise SPDXGenerationError(f"Failed to create creation info: {e}")

    # Create SPDX document (spdx-tools 0.8+ API)
    try:
        document = Document(
            creation_info=creation_info,
            packages=[package] if package else [],
            relationships=[],
        )
    except Exception as e:
        raise SPDXGenerationError(f"Failed to create SPDX document: {e}")

    return document


def create_package(metadata: Dict[str, Any]) -> Package:
    """
    Create SPDX Package from binary metadata.

    This function creates an SPDX Package object from extracted binary metadata,
    mapping the metadata fields to SPDX package properties. The package includes
    information about the binary type, architecture, entrypoint, sections, and
    a description that summarizes the binary characteristics.

    Args:
        metadata: Dictionary containing binary metadata with keys:
            - name (str): Binary name
            - type (str): Binary format type (ELF, PE, MachO, Raw)
            - architecture (str): Target architecture
            - entrypoint (Optional[str]): Entry point address in hex
            - sections (Optional[List[Dict[str, Any]]]): List of section information
            - dependencies (Optional[List[str]]): List of imported libraries

    Returns:
        SPDX Package object containing:
        - Package name (from metadata name)
        - SPDX identifier (SPDXRef-Package)
        - Download location (NOASSERTION for binaries)
        - Description with binary type, architecture, and other details
        - Version string combining type and architecture
        - License information (NOASSERTION for binaries)

    Raises:
        ValueError: If metadata is invalid or missing required fields.
        SPDXGenerationError: If package creation fails.
        ImportError: If spdx-tools library is not installed.

    Example:
        >>> metadata = {
        ...     'name': 'my-binary',
        ...     'type': 'ELF',
        ...     'architecture': 'x86_64',
        ...     'entrypoint': '0x4000',
        ...     'sections': [{'name': '.text', 'size': 1024}]
        ... }
        >>> package = create_package(metadata)
        >>> package.name
        'my-binary'
        >>> package.spdx_id
        'SPDXRef-Package'
    """
    if Package is None:
        raise ImportError(
            "spdx-tools library is required for SPDX generation. "
            "Install it with: pip install spdx-tools"
        )

    # Validate metadata
    _validate_metadata(metadata)

    # Create and return package
    try:
        return _create_package(metadata)
    except Exception as e:
        raise SPDXGenerationError(f"Failed to create SPDX package: {e}")


def create_document(
    metadata: Dict[str, Any],
    namespace: str = "https://example.com/sbom",
    creator: str = "Tool: binary-sbom-generator"
) -> Document:
    """
    Create SPDX 2.3 document from binary metadata.

    This is a convenience function that creates an SPDX Document from binary
    metadata. It is an alias for create_spdx_document() with a simpler name.
    The document includes package information, dependencies, and follows
    SPDX 2.3 specification with all required fields.

    Args:
        metadata: Dictionary containing binary metadata with keys:
            - name (str): Binary name
            - type (str): Binary format type (ELF, PE, MachO, Raw)
            - architecture (str): Target architecture
            - entrypoint (Optional[str]): Entry point address in hex
            - sections (List[Dict[str, Any]]): List of section information
            - dependencies (List[str]): List of imported libraries
        namespace: Namespace URI for the SPDX document
            (default: "https://example.com/sbom").
        creator: Creator string in format "Tool: tool-name"
            (default: "Tool: binary-sbom-generator").

    Returns:
        SPDX Document object containing:
        - Document-level metadata (name, namespace, creation info)
        - Package with binary information
        - Dependencies as external references or packages

    Raises:
        ImportError: If spdx-tools library is not installed.
        SPDXGenerationError: If document creation fails or required metadata is missing.
        ValueError: If metadata is invalid or missing required fields.

    Example:
        >>> metadata = {
        ...     'name': 'my-binary',
        ...     'type': 'ELF',
        ...     'architecture': 'x86_64',
        ...     'entrypoint': '0x4000',
        ...     'sections': [{'name': '.text', 'size': 1024}],
        ...     'dependencies': ['libc.so.6']
        ... }
        >>> doc = create_document(metadata)
        >>> doc.name
        'my-binary-SBOM'
        >>> len(doc.packages)
        1
    """
    return create_spdx_document(metadata, namespace, creator)


def _validate_metadata(metadata: Dict[str, Any]) -> None:
    """
    Validate that required metadata fields are present.

    Args:
        metadata: Dictionary containing binary metadata.

    Raises:
        ValueError: If required fields are missing or invalid.
    """
    required_fields = ['name', 'type', 'architecture']
    missing_fields = [field for field in required_fields if field not in metadata]

    if missing_fields:
        raise ValueError(
            f"Missing required metadata fields: {', '.join(missing_fields)}. "
            f"Required fields: {', '.join(required_fields)}"
        )

    if not metadata['name']:
        raise ValueError("Metadata field 'name' cannot be empty")

    # Validate optional fields have correct types if present
    if 'dependencies' in metadata and not isinstance(metadata['dependencies'], list):
        raise ValueError("Metadata field 'dependencies' must be a list")

    if 'sections' in metadata and not isinstance(metadata['sections'], list):
        raise ValueError("Metadata field 'sections' must be a list")


def _create_package(metadata: Dict[str, Any]) -> Package:
    """
    Create SPDX Package from binary metadata.

    Args:
        metadata: Dictionary containing binary metadata.

    Returns:
        SPDX Package object with binary information.

    Raises:
        SPDXGenerationError: If package creation fails.
    """
    # Build package description
    description_parts = [
        f"Binary Type: {metadata.get('type', 'Unknown')}",
        f"Architecture: {metadata.get('architecture', 'Unknown')}",
    ]

    if metadata.get('entrypoint'):
        description_parts.append(f"Entrypoint: {metadata['entrypoint']}")

    if metadata.get('sections'):
        section_count = len(metadata['sections'])
        description_parts.append(f"Sections: {section_count}")

    description = " | ".join(description_parts)

    # Create package
    try:
        package = Package(
            name=metadata['name'],
            spdx_id="SPDXRef-Package",
            download_location=SpdxNoAssertion(),
            files_analyzed=False,
            verification_code=None,
            license_concluded=SpdxNoAssertion(),
            license_declared=SpdxNoAssertion(),
            copyright_text=SpdxNoAssertion(),
            description=description,
            version=f"{metadata.get('type', 'Unknown')}-{metadata.get('architecture', 'Unknown')}",
        )
    except Exception as e:
        raise SPDXGenerationError(f"Failed to create package: {e}")

    return package


def write_spdx_file(
    document: Document,
    output_path: str,
    output_format: str = "json"
) -> None:
    """
    Write SPDX document to file in the specified format.

    This function writes an SPDX Document object to a file in the specified
    format. Supported formats include JSON, XML, YAML, and Tag-Value. The
    function validates the format string and handles errors during file writing.

    Args:
        document: SPDX Document object to write.
        output_path: Path where the SPDX document will be written.
        output_format: Output format for the SPDX document. Supported values:
            - "json": SPDX JSON format (default)
            - "xml": SPDX XML format
            - "yaml": SPDX YAML format
            - "tag-value": SPDX Tag-Value format

    Raises:
        ImportError: If spdx-tools library is not installed.
        SPDXGenerationError: If document writing fails or format is unsupported.
        ValueError: If output_format is invalid.
        IOError: If file cannot be written (permissions, disk space, etc.).

    Example:
        >>> from binary_sbom.generator import create_spdx_document, write_spdx_file
        >>> metadata = {
        ...     'name': 'my-binary',
        ...     'type': 'ELF',
        ...     'architecture': 'x86_64',
        ...     'sections': [],
        ...     'dependencies': []
        ... }
        >>> doc = create_spdx_document(metadata)
        >>> write_spdx_file(doc, 'output.spdx.json', 'json')
        >>> write_spdx_file(doc, 'output.spdx.xml', 'xml')
        >>> write_spdx_file(doc, 'output.spdx.yaml', 'yaml')
        >>> write_spdx_file(doc, 'output.spdx', 'tag-value')
    """
    if Document is None:
        raise ImportError(
            "spdx-tools library is required for SPDX generation. "
            "Install it with: pip install spdx-tools"
        )

    # Validate output format
    supported_formats = ["json", "xml", "yaml", "tag-value"]
    normalized_format = output_format.lower().replace("_", "-")

    if normalized_format not in supported_formats:
        raise ValueError(
            f"Unsupported output format: '{output_format}'. "
            f"Supported formats: {', '.join(supported_formats)}"
        )

    # Import the appropriate writer based on format (spdx-tools >= 0.8.0 API)
    write_file: Any  # Different writers have different signatures
    try:
        if normalized_format == "json":
            from spdx_tools.spdx.writer.json import json_writer
            write_file = json_writer.write_document_to_file
        elif normalized_format == "xml":
            from spdx_tools.spdx.writer.xml import xml_writer
            write_file = xml_writer.write_document_to_file
        elif normalized_format == "yaml":
            from spdx_tools.spdx.writer.yaml import yaml_writer
            write_file = yaml_writer.write_document_to_file
        elif normalized_format == "tag-value":
            from spdx_tools.spdx.writer.tagvalue import tagvalue_writer
            write_file = tagvalue_writer.write_document_to_file
        else:
            # This should not happen due to validation above
            raise SPDXGenerationError(f"Unsupported format: {normalized_format}")
    except ImportError as e:
        raise SPDXGenerationError(
            f"Failed to import SPDX writer for format '{normalized_format}': {e}"
        )

    # Write the document to file
    try:
        write_file(document, output_path, validate=False)
    except IOError as e:
        raise IOError(
            f"Failed to write SPDX document to '{output_path}': {e}"
        )
    except Exception as e:
        raise SPDXGenerationError(
            f"Failed to write SPDX document in {normalized_format} format: {e}"
        )


__all__ = [
    'create_spdx_document',
    'create_document',
    'create_package',
    'write_spdx_file',
    'SPDXGenerationError',
]
