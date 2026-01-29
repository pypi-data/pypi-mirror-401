"""
SPDX integration module for plugin metadata transformation.

This module provides functionality to transform plugin-provided metadata
into SPDX 2.3 compliant documents. It bridges the plugin system with the
SPDX generator, converting plugin output to standard SPDX format.

The integration handles:
- Package metadata mapping to SPDX Package objects
- Relationship mapping to SPDX Relationship objects
- Annotation mapping to SPDX Annotation objects
- Document creation with proper namespace and creation info
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List

if TYPE_CHECKING:
    from spdx_tools.spdx.model import (
        Actor,
        ActorType,
        Annotation,
        AnnotationType,
        CreationInfo,
        Document,
        Package,
        Relationship,
        RelationshipType,
        SpdxNoAssertion,
    )

try:
    from spdx_tools.spdx.model import (  # noqa: F811
        Actor,
        ActorType,
        Annotation,
        AnnotationType,
        CreationInfo,
        Document,
        Package,
        Relationship,
        RelationshipType,
        SpdxNoAssertion,
    )
except ImportError:
    # Set dummy values for runtime when spdx-tools is not installed
    Actor = None  # type: ignore
    ActorType = None  # type: ignore
    Annotation = None  # type: ignore
    AnnotationType = None  # type: ignore
    CreationInfo = None  # type: ignore
    Document = None  # type: ignore
    Package = None  # type: ignore
    Relationship = None  # type: ignore
    RelationshipType = None  # type: ignore
    SpdxNoAssertion = None  # type: ignore


class SPDXIntegrationError(Exception):
    """Exception raised when SPDX integration fails."""

    pass


def create_spdx_from_plugin_metadata(
    metadata: Dict[str, Any],
    file_path: Path,
    namespace: str = "https://example.com/sbom",
    creator: str = "Tool: binary-sbom-plugin"
) -> Document:
    """Create SPDX document from plugin-provided metadata.

    This function transforms metadata returned by a plugin's parse() method
    into a valid SPDX 2.3 Document. The metadata must follow the plugin API
    format with packages, relationships, and annotations lists.

    The function handles:
    - Converting plugin package data to SPDX Package objects
    - Mapping relationship definitions to SPDX Relationship objects
    - Creating document-level annotations including plugin name
    - Generating unique document namespace based on file path and mtime
    - Creating proper creation info with timestamp

    Args:
        metadata: Dictionary returned by plugin.parse() with keys:
            - packages (List[Dict[str, Any]]): List of package data
            - relationships (List[Dict[str, Any]]): List of relationships
            - annotations (List[Dict[str, Any]]): List of annotations
            - plugin_name (str, optional): Name of the plugin that generated metadata
        file_path: Path to the original binary file being analyzed.
            Used for document naming and namespace generation.
        namespace: Base namespace URI for the SPDX document
            (default: "https://example.com/sbom").
        creator: Creator string in format "Tool: tool-name"
            (default: "Tool: binary-sbom-plugin").

    Returns:
        SPDX Document object containing:
        - Document-level metadata (name, namespace, creation info)
        - Packages extracted from plugin metadata
        - Relationships between packages
        - Annotations including plugin attribution

    Raises:
        ImportError: If spdx-tools library is not installed.
        SPDXIntegrationError: If document creation fails or metadata is invalid.
        ValueError: If metadata is missing required keys or has invalid structure.

    Example:
        >>> from pathlib import Path
        >>> from binary_sbom.plugins.integration import create_spdx_from_plugin_metadata
        >>>
        >>> metadata = {
        ...     'packages': [{
        ...         'name': 'firmware-base',
        ...         'version': '1.0.0',
        ...         'spdx_id': 'SPDXRef-firmware-base',
        ...         'download_location': 'NOASSERTION'
        ...     }],
        ...     'relationships': [{
        ...         'source': 'SPDXRef-firmware-base',
        ...         'type': 'DEPENDS_ON',
        ...         'target': 'SPDXRef-libcrypto'
        ...     }],
        ...     'annotations': [],
        ...     'plugin_name': 'ExampleFirmwareParser'
        ... }
        >>> doc = create_spdx_from_plugin_metadata(metadata, Path('firmware.bin'))
        >>> doc.name
        'firmware.bin-SBOM'
        >>> len(doc.packages)
        1
    """
    if Document is None:
        raise ImportError(
            "spdx-tools library is required for SPDX integration. "
            "Install it with: pip install spdx-tools"
        )

    # Validate required metadata keys
    _validate_metadata(metadata)

    # Create SPDX packages from plugin metadata
    try:
        packages = _create_packages(metadata.get('packages', []))
    except Exception as e:
        raise SPDXIntegrationError(f"Failed to create SPDX packages: {e}")

    # Create SPDX relationships from plugin metadata
    try:
        relationships = _create_relationships(metadata.get('relationships', []))
    except Exception as e:
        raise SPDXIntegrationError(f"Failed to create SPDX relationships: {e}")

    # Create SPDX annotations from plugin metadata
    try:
        annotations = _create_annotations(
            metadata.get('annotations', []),
            plugin_name=metadata.get('plugin_name')
        )
    except Exception as e:
        raise SPDXIntegrationError(f"Failed to create SPDX annotations: {e}")

    # Parse creator string to create Actor (spdx-tools 0.8+ API)
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
        raise SPDXIntegrationError(f"Failed to create creator actor: {e}")

    # Create document name and namespace
    document_name = f"{file_path.name}-SBOM"

    # Generate unique namespace using file path and modification time
    try:
        file_mtime = file_path.stat().st_mtime if file_path.exists() else datetime.now(timezone.utc).timestamp()
    except OSError:
        file_mtime = datetime.now(timezone.utc).timestamp()

    if namespace.endswith('/'):
        document_namespace = f"{namespace}{file_path.name}-{file_mtime}"
    else:
        document_namespace = f"{namespace}/{file_path.name}-{file_mtime}"

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
        raise SPDXIntegrationError(f"Failed to create creation info: {e}")

    # Create SPDX document (spdx-tools 0.8+ API)
    try:
        document = Document(
            creation_info=creation_info,
            packages=packages,
            relationships=relationships,
            annotations=annotations,
        )
    except Exception as e:
        raise SPDXIntegrationError(f"Failed to create SPDX document: {e}")

    return document


def _validate_metadata(metadata: Dict[str, Any]) -> None:
    """Validate that required metadata keys are present.

    Args:
        metadata: Dictionary containing plugin metadata.

    Raises:
        ValueError: If required keys are missing or metadata is invalid.
    """
    required_keys = ['packages', 'relationships', 'annotations']
    missing_keys = [key for key in required_keys if key not in metadata]

    if missing_keys:
        raise ValueError(
            f"Missing required metadata keys: {', '.join(missing_keys)}. "
            f"Required keys: {', '.join(required_keys)}"
        )

    # Validate that packages, relationships, and annotations are lists
    if not isinstance(metadata.get('packages'), list):
        raise ValueError("Metadata key 'packages' must be a list")

    if not isinstance(metadata.get('relationships'), list):
        raise ValueError("Metadata key 'relationships' must be a list")

    if not isinstance(metadata.get('annotations'), list):
        raise ValueError("Metadata key 'annotations' must be a list")


def _create_packages(packages_data: List[Dict[str, Any]]) -> List[Package]:
    """Create SPDX Package objects from plugin package data.

    Args:
        packages_data: List of package dictionaries from plugin metadata.

    Returns:
        List of SPDX Package objects.

    Raises:
        SPDXIntegrationError: If package creation fails.
    """
    if Package is None:
        raise SPDXIntegrationError("spdx-tools library is not available")

    packages = []

    for pkg_data in packages_data:
        try:
            # Extract required fields with defaults
            name = pkg_data.get('name', 'unknown')
            spdx_id = pkg_data.get('spdx_id', f"SPDXRef-{name}")
            download_location = pkg_data.get('download_location', SpdxNoAssertion())

            # Build description from available fields
            description_parts = []
            if pkg_data.get('version'):
                description_parts.append(f"Version: {pkg_data['version']}")
            if pkg_data.get('type'):
                description_parts.append(f"Type: {pkg_data['type']}")
            if pkg_data.get('supplier'):
                description_parts.append(f"Supplier: {pkg_data['supplier']}")

            description = " | ".join(description_parts) if description_parts else None

            # Create package with available fields
            package = Package(
                name=name,
                spdx_id=spdx_id,
                download_location=download_location,
                files_analyzed=False,
                verification_code=None,
                license_concluded=pkg_data.get('license', SpdxNoAssertion()),
                license_declared=pkg_data.get('license', SpdxNoAssertion()),
                copyright_text=pkg_data.get('copyright_text', SpdxNoAssertion()),
                description=description,
                version=pkg_data.get('version'),
                homepage=pkg_data.get('homepage'),
                supplier=pkg_data.get('supplier'),
            )

            packages.append(package)
        except Exception as e:
            raise SPDXIntegrationError(f"Failed to create package '{pkg_data.get('name', 'unknown')}': {e}")

    return packages


def _create_relationships(relationships_data: List[Dict[str, Any]]) -> List[Relationship]:
    """Create SPDX Relationship objects from plugin relationship data.

    Args:
        relationships_data: List of relationship dictionaries from plugin metadata.

    Returns:
        List of SPDX Relationship objects.

    Raises:
        SPDXIntegrationError: If relationship creation fails.
    """
    if Relationship is None or RelationshipType is None:
        raise SPDXIntegrationError("spdx-tools library is not available")

    relationships = []

    for rel_data in relationships_data:
        try:
            # Get relationship type
            rel_type_str = rel_data.get('type', 'DEPENDS_ON').upper().replace(' ', '_')

            # Map string to RelationshipType enum
            try:
                relationship_type = RelationshipType[rel_type_str]
            except KeyError:
                # Fallback to DEPENDS_ON for unknown types
                relationship_type = RelationshipType.DEPENDS_ON

            relationship = Relationship(
                spdx_element_id=rel_data['source'],
                relationship_type=relationship_type,
                related_spdx_element_id=rel_data['target']
            )

            relationships.append(relationship)
        except Exception as e:
            raise SPDXIntegrationError(
                f"Failed to create relationship '{rel_data.get('source', 'unknown')}': {e}"
            )

    return relationships


def _create_annotations(
    annotations_data: List[Dict[str, Any]],
    plugin_name: str = None
) -> List[Annotation]:
    """Create SPDX Annotation objects from plugin annotation data.

    Args:
        annotations_data: List of annotation dictionaries from plugin metadata.
        plugin_name: Optional plugin name to add as document-level annotation.

    Returns:
        List of SPDX Annotation objects.

    Raises:
        SPDXIntegrationError: If annotation creation fails.
    """
    if Annotation is None or AnnotationType is None:
        raise SPDXIntegrationError("spdx-tools library is not available")

    annotations = []

    # Add plugin name as document-level annotation if provided
    if plugin_name:
        try:
            plugin_annotation = Annotation(
                spdx_id="SPDXRef-DOCUMENT",
                annotation_type=AnnotationType.OTHER,
                annotator=Actor(actor_type=ActorType.TOOL, name="binary-sbom-plugin"),
                annotation_comment=f"Generated by plugin: {plugin_name}",
                annotation_date=datetime.now(timezone.utc)
            )
            annotations.append(plugin_annotation)
        except Exception:
            # Silently skip if plugin annotation creation fails
            pass

    # Process plugin-provided annotations
    for ann_data in annotations_data:
        try:
            # Get annotation type
            ann_type_str = ann_data.get('type', 'OTHER').upper()
            try:
                annotation_type = AnnotationType[ann_type_str]
            except KeyError:
                annotation_type = AnnotationType.OTHER

            # Parse annotator string (default to TOOL if not specified)
            annotator_str = ann_data.get('annotator', 'Tool: plugin')
            if ":" in annotator_str:
                actor_type_str, actor_name = annotator_str.split(":", 1)
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
                actor_name = annotator_str

            annotator = Actor(actor_type=actor_type, name=actor_name.strip())

            # Get annotation date from data or use current time
            ann_date_str = ann_data.get('date')
            if ann_date_str:
                # Parse ISO format date string
                from datetime import datetime as dt
                try:
                    ann_date = dt.fromisoformat(ann_date_str.replace('Z', '+00:00'))
                except (ValueError, AttributeError):
                    ann_date = datetime.now(timezone.utc)
            else:
                ann_date = datetime.now(timezone.utc)

            annotation = Annotation(
                spdx_id=ann_data.get('spdx_id', 'SPDXRef-DOCUMENT'),
                annotation_type=annotation_type,
                annotator=annotator,
                annotation_comment=ann_data['text'],
                annotation_date=ann_date
            )

            annotations.append(annotation)
        except Exception as e:
            # Log error but continue with other annotations
            # Don't fail entire document for annotation errors
            continue

    return annotations


__all__ = [
    'create_spdx_from_plugin_metadata',
    'SPDXIntegrationError',
]
