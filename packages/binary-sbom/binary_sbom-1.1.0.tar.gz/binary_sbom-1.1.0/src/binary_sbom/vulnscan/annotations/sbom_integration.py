"""
SBOM integration for vulnerability annotations.

This module provides high-level utilities for integrating vulnerability
scanning results into SPDX SBOM documents. It handles the complete workflow
of scanning packages, deduplicating results, and creating annotations.

Implementation for Phase 7, Subtask 7.2.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from binary_sbom.vulnscan.aggregation.deduplicator import Deduplicator
from binary_sbom.vulnscan.annotations.annotation import (
    SPDXAnnotation,
    VulnerabilityAnnotationBuilder,
)
from binary_sbom.vulnscan.scanners.scanner import VulnScanner
from binary_sbom.vulnscan.types import (
    PackageIdentifier,
    ScanResult,
    Severity,
    VulnerabilityMatch,
    VulnerabilitySource,
)

logger = logging.getLogger(__name__)


class SBOMAnnotator:
    """
    High-level interface for adding vulnerability annotations to SBOMs.

    This class provides a simple API for scanning packages and creating
    SPDX annotations that can be added to SBOM documents during generation.

    The workflow is:
    1. Scan packages for vulnerabilities
    2. Deduplicate results from multiple sources
    3. Generate SPDX annotations
    4. Add annotations to package entries

    Example:
        >>> annotator = SBOMAnnotator()
        >>> packages = [
        ...     PackageIdentifier("npm", "lodash", "4.17.15"),
        ...     PackageIdentifier("PyPI", "requests", "2.28.0")
        ... ]
        >>> scan_result = annotator.scan_packages(packages)
        >>> annotations = annotator.create_package_annotations(scan_result)
        >>> for pkg, annotation in zip(packages, annotations):
        ...     spdx_id = f"SPDXRef-{pkg.ecosystem}-{pkg.name}-{pkg.version}"
        ...     # Add annotation to SPDX package entry
    """

    def __init__(
        self,
        scanner: Optional[VulnScanner] = None,
        deduplicator: Optional[Deduplicator] = None,
        annotation_builder: Optional[VulnerabilityAnnotationBuilder] = None,
    ):
        """
        Initialize the SBOM annotator.

        Args:
            scanner: VulnScanner instance for querying vulnerability databases.
                If None, creates a default scanner with OSV enabled.
            deduplicator: Deduplicator instance for merging duplicate vulnerabilities.
                If None, creates a default Deduplicator.
            annotation_builder: VulnerabilityAnnotationBuilder for creating annotations.
                If None, creates a default builder.

        Example:
            >>> annotator = SBOMAnnotator()
            >>> # Or with custom components
            >>> from binary_sbom.vulnscan.scanners.scanner import VulnScanner
            >>> scanner = VulnScanner(sources={VulnerabilitySource.OSV})
            >>> annotator = SBOMAnnotator(scanner=scanner)
        """
        self.scanner = scanner or VulnScanner()
        self.deduplicator = deduplicator or Deduplicator()
        self.annotation_builder = annotation_builder or VulnerabilityAnnotationBuilder()

        logger.debug(
            f"Initialized SBOMAnnotator with scanner sources: {self.scanner.sources}"
        )

    def scan_packages(
        self,
        packages: List[PackageIdentifier],
        deduplicate: bool = True,
    ) -> ScanResult:
        """
        Scan multiple packages for vulnerabilities.

        Queries all enabled vulnerability databases for the specified packages,
        aggregates results, and optionally deduplicates findings.

        Args:
            packages: List of PackageIdentifier objects to scan.
            deduplicate: Whether to deduplicate vulnerabilities across sources.
                Defaults to True.

        Returns:
            ScanResult containing VulnerabilityMatch objects for each package.
            Packages with no vulnerabilities will have empty vulnerability lists.

        Raises:
            APIError: If vulnerability database queries fail.
            ValueError: If packages list is empty.

        Example:
            >>> packages = [
            ...     PackageIdentifier("npm", "lodash", "4.17.15"),
            ...     PackageIdentifier("PyPI", "requests", "2.28.0")
            ... ]
            >>> result = annotator.scan_packages(packages)
            >>> result.total_vulnerabilities
            3
            >>> result.affected_packages
            1
        """
        if not packages:
            raise ValueError("Packages list cannot be empty")

        logger.info(f"Scanning {len(packages)} packages for vulnerabilities")

        # Scan all packages
        matches: List[VulnerabilityMatch] = []
        for pkg in packages:
            try:
                logger.debug(f"Scanning package: {pkg}")
                match = self.scanner.scan_package(pkg)
                matches.append(match)
            except Exception as e:
                logger.error(f"Failed to scan package {pkg}: {e}")
                # Create empty match for failed scans
                matches.append(
                    VulnerabilityMatch(package=pkg, vulnerabilities=[])
                )

        # Create scan result
        result = ScanResult(
            packages=matches,
            scan_timestamp=datetime.now(),
            sources_queried=self.scanner.sources,
        )

        # Deduplicate if requested
        if deduplicate:
            logger.debug("Deduplicating vulnerability results")
            result = self.deduplicate_scan_result(result)

        logger.info(
            f"Scan complete: {result.total_vulnerabilities} vulnerabilities "
            f"in {result.affected_packages} packages"
        )

        return result

    def deduplicate_scan_result(self, result: ScanResult) -> ScanResult:
        """
        Deduplicate vulnerabilities in a scan result.

        Merges duplicate vulnerabilities from multiple sources for each package.

        Args:
            result: ScanResult with potential duplicates.

        Returns:
            New ScanResult with deduplicated vulnerabilities.

        Example:
            >>> result = scanner.scan_packages(packages, deduplicate=False)
            >>> deduplicated = annotator.deduplicate_scan_result(result)
        """
        deduplicated_matches: List[VulnerabilityMatch] = []

        for match in result.packages:
            if match.vulnerabilities:
                deduplicated_vulns = self.deduplicator.merge_vulnerabilities(
                    match.vulnerabilities
                )
                deduplicated_matches.append(
                    VulnerabilityMatch(
                        package=match.package,
                        vulnerabilities=deduplicated_vulns,
                    )
                )
            else:
                # No vulnerabilities to deduplicate
                deduplicated_matches.append(match)

        return ScanResult(
            packages=deduplicated_matches,
            scan_timestamp=result.scan_timestamp,
            sources_queried=result.sources_queried,
        )

    def create_package_annotations(
        self,
        scan_result: ScanResult,
        include_cvss: bool = False,
        include_references: bool = False,
    ) -> List[Optional[SPDXAnnotation]]:
        """
        Create SPDX annotations for each package in a scan result.

        Creates package-level annotations that can be added to SPDX package entries.

        Args:
            scan_result: ScanResult from scan_packages().
            include_cvss: Include detailed CVSS score information in annotations.
            include_references: Include reference URLs in annotations.

        Returns:
            List of SPDXAnnotation objects, one per package. Packages with no
            vulnerabilities will have None instead of an annotation.

        Example:
            >>> result = annotator.scan_packages(packages)
            >>> annotations = annotator.create_package_annotations(result)
            >>> for pkg, annotation in zip(packages, annotations):
            ...     if annotation:
            ...         print(f"{pkg}: {annotation.total_vulnerabilities} vulnerabilities")
        """
        annotations: List[Optional[SPDXAnnotation]] = []

        for match in scan_result.packages:
            if match.vulnerabilities:
                annotation = self.annotation_builder.build_from_match(
                    match,
                    spdx_id=None,  # Will be set by caller
                    include_cvss=include_cvss,
                    include_references=include_references,
                )
                annotations.append(annotation)
            else:
                # No vulnerabilities for this package
                annotations.append(None)

        return annotations

    def create_document_annotation(
        self,
        scan_result: ScanResult,
        include_package_details: bool = False,
    ) -> Optional[SPDXAnnotation]:
        """
        Create a document-level SPDX annotation for a scan result.

        Creates a summary annotation for the entire SBOM document that aggregates
        vulnerability findings across all packages.

        Args:
            scan_result: ScanResult from scan_packages().
            include_package_details: Include per-package breakdown in comment.

        Returns:
            SPDXAnnotation for document-level metadata, or None if no vulnerabilities found.

        Example:
            >>> result = annotator.scan_packages(packages)
            >>> doc_annotation = annotator.create_document_annotation(result)
            >>> if doc_annotation:
            ...     print(f"Total: {doc_annotation.total_vulnerabilities} vulnerabilities")
        """
        return self.annotation_builder.build_from_scan_result(
            scan_result,
            include_package_details=include_package_details,
        )

    def annotate_spdx_package(
        self,
        spdx_package: Dict[str, Any],
        match: VulnerabilityMatch,
        include_cvss: bool = False,
        include_references: bool = False,
    ) -> Dict[str, Any]:
        """
        Add vulnerability annotation to an SPDX package dictionary.

        Modifies an existing SPDX package entry to include vulnerability annotations.

        Args:
            spdx_package: SPDX package dictionary (must have 'SPDXID' key).
            match: VulnerabilityMatch for the package.
            include_cvss: Include detailed CVSS score information.
            include_references: Include reference URLs.

        Returns:
            Modified SPDX package dictionary with annotations added.

        Raises:
            ValueError: If spdx_package doesn't have 'SPDXID' key.

        Example:
            >>> spdx_pkg = {
            ...     "SPDXID": "SPDXRef-package-npm-lodash-4.17.15",
            ...     "name": "lodash",
            ...     "versionInfo": "4.17.15"
            ... }
            >>> match = VulnerabilityMatch(...)
            >>> annotated_pkg = annotator.annotate_spdx_package(spdx_pkg, match)
        """
        if "SPDXID" not in spdx_package:
            raise ValueError("SPDX package must have 'SPDXID' key")

        # Only add annotation if vulnerabilities were found
        if match.vulnerabilities:
            spdx_id = spdx_package["SPDXID"]

            # Create annotation
            annotation = self.annotation_builder.build_from_match(
                match,
                spdx_id=spdx_id,
                include_cvss=include_cvss,
                include_references=include_references,
            )

            # Add to package
            if "annotations" not in spdx_package:
                spdx_package["annotations"] = []

            spdx_package["annotations"].append(annotation.to_spdx_dict())

            logger.debug(f"Added vulnerability annotation to {spdx_id}")

        return spdx_package

    def annotate_spdx_document(
        self,
        spdx_document: Dict[str, Any],
        scan_result: ScanResult,
        include_package_details: bool = False,
    ) -> Dict[str, Any]:
        """
        Add vulnerability annotations to an SPDX document.

        Adds document-level summary annotation and package-level annotations.

        Args:
            spdx_document: SPDX document dictionary (must have 'spdxVersion' key).
            scan_result: ScanResult from scan_packages().
            include_package_details: Include per-package breakdown in document annotation.

        Returns:
            Modified SPDX document with annotations added.

        Raises:
            ValueError: If spdx_document doesn't have required keys.

        Example:
            >>> spdx_doc = {
            ...     "spdxVersion": "SPDX-2.3",
            ...     "packages": [...]
            ... }
            >>> result = annotator.scan_packages(packages)
            >>> annotated_doc = annotator.annotate_spdx_document(spdx_doc, result)
        """
        if "spdxVersion" not in spdx_document:
            raise ValueError("SPDX document must have 'spdxVersion' key")

        # Add document-level annotation if vulnerabilities found
        doc_annotation = self.create_document_annotation(
            scan_result,
            include_package_details=include_package_details,
        )

        if doc_annotation:
            if "annotations" not in spdx_document:
                spdx_document["annotations"] = []

            spdx_document["annotations"].append(doc_annotation.to_spdx_dict())
            logger.info("Added document-level vulnerability annotation")

        # Add package-level annotations
        if "packages" in spdx_document:
            for i, pkg in enumerate(spdx_document["packages"]):
                if i < len(scan_result.packages):
                    match = scan_result.packages[i]
                    if match.vulnerabilities:
                        spdx_document["packages"][i] = self.annotate_spdx_package(
                            pkg,
                            match,
                            include_cvss=False,
                            include_references=False,
                        )

        return spdx_document

    def extract_vulnerability_metadata(
        self,
        scan_result: ScanResult,
    ) -> Dict[str, Any]:
        """
        Extract aggregate vulnerability statistics for SBOM metadata.

        Creates a dictionary of vulnerability statistics that can be included
        in SBOM document metadata (e.g., creationInfo, document comment, or
        custom properties).

        Args:
            scan_result: ScanResult from scan_packages().

        Returns:
            Dictionary with aggregate vulnerability statistics:
            - totalVulnerabilities: Total number of vulnerabilities found
            - affectedPackages: Number of packages with vulnerabilities
            - totalPackages: Total number of packages scanned
            - severitySummary: Severity level counts (CRITICAL, HIGH, MEDIUM, LOW)
            - highestSeverity: Highest severity level found
            - sourcesQueried: List of vulnerability sources queried
            - scanTimestamp: ISO 8601 timestamp of the scan
            - vulnerabilityIds: Deduplicated list of all vulnerability IDs
            - hasCriticalVulnerabilities: Boolean indicating if critical vulns exist

        Example:
            >>> result = annotator.scan_packages(packages)
            >>> metadata = annotator.extract_vulnerability_metadata(result)
            >>> metadata["totalVulnerabilities"]
            15
            >>> metadata["severitySummary"]
            {'CRITICAL': 3, 'HIGH': 7, 'MEDIUM': 4, 'LOW': 1}
        """
        # Extract all vulnerability IDs for deduplication
        all_vuln_ids = []
        for match in scan_result.packages:
            all_vuln_ids.extend(
                self.annotation_builder._extract_vulnerability_ids(match.vulnerabilities)
            )
        unique_vuln_ids = sorted(list(set(all_vuln_ids)))

        # Determine highest severity across all vulnerabilities
        all_vulnerabilities = []
        for match in scan_result.packages:
            all_vulnerabilities.extend(match.vulnerabilities)
        highest_severity = self.annotation_builder._get_highest_severity(all_vulnerabilities)

        # Build metadata dictionary
        metadata = {
            "totalVulnerabilities": scan_result.total_vulnerabilities,
            "affectedPackages": scan_result.affected_packages,
            "totalPackages": scan_result.total_packages,
            "severitySummary": scan_result.severity_summary.copy(),
            "highestSeverity": highest_severity.value if highest_severity else None,
            "sourcesQueried": [source.value for source in scan_result.sources_queried],
            "scanTimestamp": scan_result.scan_timestamp.isoformat() + "Z" if scan_result.scan_timestamp else None,
            "vulnerabilityIds": unique_vuln_ids,
            "hasCriticalVulnerabilities": scan_result.severity_summary.get("CRITICAL", 0) > 0,
        }

        logger.debug(
            f"Extracted vulnerability metadata: {metadata['totalVulnerabilities']} total, "
            f"{metadata['affectedPackages']} affected packages, "
            f"highest severity: {metadata['highestSeverity']}"
        )

        return metadata


def scan_and_annotate(
    packages: List[PackageIdentifier],
    spdx_document: Optional[Dict[str, Any]] = None,
    sources: Optional[Set[VulnerabilitySource]] = None,
    deduplicate: bool = True,
    include_cvss: bool = False,
    include_references: bool = False,
    include_package_details: bool = False,
) -> ScanResult:
    """
    Convenience function to scan packages and optionally annotate an SPDX document.

    This is a high-level helper that combines scanning and annotation in one call.

    Args:
        packages: List of PackageIdentifier objects to scan.
        spdx_document: Optional SPDX document dict to annotate. If provided,
            annotations will be added directly to the document.
        sources: Set of VulnerabilitySource to query. If None, uses default sources.
        deduplicate: Whether to deduplicate results.
        include_cvss: Include CVSS scores in package annotations.
        include_references: Include references in package annotations.
        include_package_details: Include per-package breakdown in document annotation.

    Returns:
        ScanResult with vulnerability findings.

    Example:
        >>> packages = [
        ...     PackageIdentifier("npm", "lodash", "4.17.15"),
        ...     PackageIdentifier("PyPI", "requests", "2.28.0")
        ... ]
        >>> result = scan_and_annotate(packages)
        >>> print(f"Found {result.total_vulnerabilities} vulnerabilities")
        >>>
        >>> # Or with existing SPDX document
        >>> spdx_doc = {"spdxVersion": "SPDX-2.3", "packages": [...]}
        >>> result = scan_and_annotate(packages, spdx_document=spdx_doc)
        >>> # spdx_doc now has annotations
    """
    # Create annotator with specified sources
    scanner = VulnScanner(sources=sources) if sources else None
    annotator = SBOMAnnotator(scanner=scanner)

    # Scan packages
    result = annotator.scan_packages(packages, deduplicate=deduplicate)

    # Annotate document if provided
    if spdx_document is not None:
        annotator.annotate_spdx_document(
            spdx_document,
            result,
            include_package_details=include_package_details,
        )

    return result
