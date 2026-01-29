"""
SPDX document generator module for Binary SBOM Generator.

This module provides functionality to generate SPDX SBOM documents
from binary metadata, with progress tracking for large documents.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

from .progress import ProgressTracker, should_show_progress
from .config import load_config, get_min_file_size_mb


def create_spdx_document(
    metadata: Dict[str, Any],
    output_path: Optional[Path] = None,
    output_format: str = "json",
    progress_force: Optional[bool] = None,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Generate an SPDX document from binary metadata.

    This function creates an SPDX document with the following steps:
    1. Create SPDX header (document namespace, version, creation info)
    2. Add package information (binary details, dependencies)
    3. Add relationships (dependencies, describes)

    Progress bars are shown automatically for documents with many packages/relationships
    in TTY environments. Use progress_force=True to force enable or progress_force=False
    to force disable.

    Args:
        metadata: Binary metadata dictionary from analyze_binary().
        output_path: Optional path to save the SPDX document.
        output_format: SPDX document format (json, xml, tagvalue).
        progress_force: Override for progress indicators (True/False/None).
                       True forces enable, False forces disable, None uses auto-detection.
        config: Optional configuration dictionary. If not provided, loads default config.

    Returns:
        Dictionary containing the SPDX document structure.

    Raises:
        ValueError: If metadata is invalid or incomplete.
        IOError: If the document cannot be written to file.

    Example:
        >>> metadata = analyze_binary("firmware.bin")
        >>> doc = create_spdx_document(metadata)
        >>> doc['spdxVersion']
        'SPDX-2.3'

        >>> # Force disable progress indicators
        >>> doc = create_spdx_document(metadata, progress_force=False)
    """
    # Load config if not provided
    if config is None:
        config = load_config()

    # Validate metadata
    if not metadata:
        raise ValueError("Metadata cannot be empty")

    if 'file_path' not in metadata:
        raise ValueError("Metadata must contain 'file_path' field")

    try:
        # Determine document complexity for progress tracking
        # Use file size as a proxy for complexity
        file_size = metadata.get('file_size', 0)
        dependency_count = len(metadata.get('dependencies', []))
        section_count = len(metadata.get('sections', []))

        # Calculate complexity score: file_size + dependencies*1000 + sections*100
        complexity_score = file_size + (dependency_count * 1000) + (section_count * 100)

        # Create progress tracker based on complexity
        # Use a lower threshold (10MB equivalent) for SPDX generation since it can be slow
        min_complexity = 10 * 1024 * 1024  # 10MB equivalent

        tracker = None
        if should_show_progress(complexity_score, config, progress_force):
            tracker = ProgressTracker(
                file_size=complexity_score,
                min_size=min_complexity,
                config=config,
                force=progress_force
            )

        # Start SPDX document generation progress (3 main steps: header, packages, relationships)
        if tracker is not None and tracker.is_enabled():
            tracker.start_operation("Generating SPDX document...", total=3)

        # Step 1: Create SPDX header
        if tracker is not None and tracker.is_enabled():
            tracker.set_description("Generating SPDX document: Creating header...")
        document = _create_spdx_header(metadata)
        if tracker is not None and tracker.is_enabled():
            tracker.update_progress(1)  # Step 1 complete

        # Step 2: Add package information
        if tracker is not None and tracker.is_enabled():
            tracker.set_description("Generating SPDX document: Adding packages...")
        document['packages'] = _create_spdx_packages(metadata)
        if tracker is not None and tracker.is_enabled():
            tracker.update_progress(1)  # Step 2 complete

        # Step 3: Add relationships
        if tracker is not None and tracker.is_enabled():
            tracker.set_description("Generating SPDX document: Adding relationships...")
        document['relationships'] = _create_spdx_relationships(metadata)
        if tracker is not None and tracker.is_enabled():
            tracker.update_progress(1)  # Step 3 complete

        # Write to file if output path is provided
        if output_path:
            _write_spdx_document(document, output_path, output_format, tracker)

        return document

    except Exception as e:
        # Ensure progress bar is cleaned up on error
        if tracker is not None:
            tracker.finish_operation()
        raise


def _create_spdx_header(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create SPDX document header information.

    Args:
        metadata: Binary metadata dictionary.

    Returns:
        Dictionary containing SPDX header fields.

    Example:
        >>> header = _create_spdx_header(metadata)
        >>> header['spdxVersion']
        'SPDX-2.3'
    """
    # Generate unique document namespace ID
    namespace_id = str(uuid.uuid4())
    file_path = metadata.get('file_path', 'unknown')
    file_name = Path(file_path).name

    # Create SPDX document header
    header = {
        'spdxVersion': 'SPDX-2.3',
        'dataLicense': 'CC0-1.0',
        'SPDXID': 'SPDXRef-DOCUMENT',
        'name': f'{file_name}-SBOM',
        'documentNamespace': f'https://spdx.org/spdxdocs/{namespace_id}',
        'creationInfo': {
            'created': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'creators': [
                'Tool: binary-sbom-0.1.0'
            ]
        },
        'documentDescribes': ['SPDXRef-Package']
    }

    return header


def _create_spdx_packages(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Create SPDX package information from binary metadata.

    Args:
        metadata: Binary metadata dictionary.

    Returns:
        List of SPDX package dictionaries.

    Example:
        >>> packages = _create_spdx_packages(metadata)
        >>> len(packages)
        1
    """
    file_path = metadata.get('file_path', 'unknown')
    file_size = metadata.get('file_size', 0)
    file_name = Path(file_path).name
    format_name = metadata.get('format', 'Unknown')
    architecture = metadata.get('architecture', 'Unknown')

    # Create primary package for the binary
    package = {
        'SPDXID': 'SPDXRef-Package',
        'name': file_name,
        'downloadLocation': file_path,
        'filesAnalyzed': False,
        'packageVerificationCode': {
            'packageVerificationCodeValue': str(uuid.uuid4())[:32]
        },
        'size': file_size,
        'externalRefs': [
            {
                'referenceCategory': 'PACKAGE-MANAGER',
                'referenceType': 'purl',
                'referenceLocator': f'pkg:generic/{file_name}'
            }
        ],
        'properties': [
            {
                'name': 'binaryFormat',
                'value': format_name
            },
            {
                'name': 'architecture',
                'value': architecture
            }
        ]
    }

    # Add dependencies as separate packages if present
    packages = [package]
    dependencies = metadata.get('dependencies', [])

    for idx, dep in enumerate(dependencies, start=1):
        dep_package = {
            'SPDXID': f'SPDXRef-Package-{idx}',
            'name': dep,
            'downloadLocation': 'NOASSERTION',
            'filesAnalyzed': False,
            'externalRefs': [
                {
                    'referenceCategory': 'PACKAGE-MANAGER',
                    'referenceType': 'purl',
                    'referenceLocator': f'pkg:generic/{dep}'
                }
            ]
        }
        packages.append(dep_package)

    return packages


def _create_spdx_relationships(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Create SPDX relationships from binary metadata.

    Args:
        metadata: Binary metadata dictionary.

    Returns:
        List of SPDX relationship dictionaries.

    Example:
        >>> relationships = _create_spdx_relationships(metadata)
        >>> len(relationships) > 0
        True
    """
    relationships = []
    dependencies = metadata.get('dependencies', [])

    # Add relationship: DOCUMENT describes PACKAGE
    relationships.append({
        'spdxElementId': 'SPDXRef-DOCUMENT',
        'relationshipType': 'DESCRIBES',
        'relatedSpdxElement': 'SPDXRef-Package'
    })

    # Add relationships for dependencies
    for idx, dep in enumerate(dependencies, start=1):
        relationships.append({
            'spdxElementId': 'SPDXRef-Package',
            'relationshipType': 'DEPENDS_ON',
            'relatedSpdxElement': f'SPDXRef-Package-{idx}'
        })

    return relationships


def _write_spdx_document(
    document: Dict[str, Any],
    output_path: Path,
    output_format: str,
    tracker: Optional[ProgressTracker] = None
) -> None:
    """
    Write SPDX document to file.

    For documents >1MB in size, shows a progress bar during writing.

    Args:
        document: SPDX document dictionary.
        output_path: Path to write the document.
        output_format: SPDX document format (json, xml, tagvalue).
        tracker: Optional ProgressTracker for showing write progress.

    Raises:
        IOError: If the document cannot be written.

    Example:
        >>> tracker = ProgressTracker(file_size=150*1024*1024)
        >>> _write_spdx_document(doc, Path("sbom.json"), "json", tracker)
    """
    try:
        import json

        # Serialize document to get size
        content = json.dumps(document, indent=2)
        content_size = len(content.encode('utf-8'))

        # Minimum size for showing write progress: 1MB
        min_write_size = 1024 * 1024

        # Start write progress if content is large
        if tracker is not None and tracker.is_enabled() and content_size >= min_write_size:
            tracker.start_operation(
                f"Writing SBOM: {output_path.name}",
                total=content_size,
                unit="B",
                unit_scale=True
            )

        # Write document to file
        with open(output_path, 'w', encoding='utf-8') as f:
            if tracker is not None and tracker.is_enabled() and content_size >= min_write_size:
                # Write in chunks to show progress
                chunk_size = 1024 * 1024  # 1MB chunks
                bytes_written = 0

                for i in range(0, len(content), chunk_size):
                    chunk = content[i:i+chunk_size]
                    f.write(chunk)
                    bytes_written += len(chunk.encode('utf-8'))
                    tracker.update_progress(len(chunk.encode('utf-8')))
            else:
                # Write without progress
                f.write(content)

        # Finish write progress
        if tracker is not None and tracker.is_enabled():
            tracker.finish_operation()

    except Exception as e:
        # Ensure progress bar is cleaned up on error
        if tracker is not None:
            tracker.finish_operation()
        raise IOError(f"Error writing SPDX document to {output_path}: {e}")


__all__ = [
    'create_spdx_document',
    '_create_spdx_header',
    '_create_spdx_packages',
    '_create_spdx_relationships',
    '_write_spdx_document',
]
