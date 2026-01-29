"""
SBOM annotation integration for vulnerability findings.

This package provides utilities for converting vulnerability scan results
into SPDX annotations for inclusion in SBOM documents.

Implementation for Phase 7: SBOM Annotation Integration.
"""

from binary_sbom.vulnscan.annotations.annotation import (
    SPDXAnnotation,
    SPDXAnnotationType,
    VulnerabilityAnnotationBuilder,
)
from binary_sbom.vulnscan.annotations.sbom_integration import (
    SBOMAnnotator,
    scan_and_annotate,
)

__all__ = [
    "SPDXAnnotation",
    "SPDXAnnotationType",
    "VulnerabilityAnnotationBuilder",
    "SBOMAnnotator",
    "scan_and_annotate",
]
