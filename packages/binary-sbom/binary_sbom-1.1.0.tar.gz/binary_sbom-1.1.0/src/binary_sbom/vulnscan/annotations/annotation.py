"""
SPDX annotation structures for vulnerability findings.

This module defines data structures for representing vulnerability
information as SPDX annotations, following the SPDX 2.3 specification.

Implementation for Phase 7, Subtask 7.1.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set

from binary_sbom.vulnscan.types import (
    Reference,
    ScanResult,
    Severity,
    Vulnerability,
    VulnerabilityMatch,
    VulnerabilitySource,
)

logger = logging.getLogger(__name__)


class SPDXAnnotationType(str, Enum):
    """
    SPDX annotation types.

    Follows the SPDX 2.3 specification for annotationType field.
    """

    REVIEW = "REVIEW"
    """Package was reviewed for vulnerabilities."""

    OTHER = "OTHER"
    """Other type of annotation."""


@dataclass(frozen=True)
class SPDXAnnotation:
    """
    SPDX annotation for vulnerability findings.

    Represents vulnerability scan results as a SPDX annotation following
    the SPDX 2.3 specification. Annotations include CVE IDs, severity
    scores, and source links for discovered vulnerabilities.

    Attributes:
        annotator: Tool or person that created the annotation (e.g., "vulnerability-scanner")
        annotation_date: When the annotation was created (ISO 8601 format)
        annotation_type: Type of annotation (REVIEW for vulnerability scans)
        comment: Human-readable vulnerability summary with counts and severity breakdown
        spdx_id: SPDX ID of the package being annotated (optional, for package-level annotations)
        vulnerability_ids: List of vulnerability IDs found (CVE IDs, GHSA IDs, etc.)
        severity_summary: Severity level counts (CRITICAL, HIGH, MEDIUM, LOW)
        source_links: List of URLs to vulnerability databases/advisories
        highest_severity: The highest severity level found
        total_vulnerabilities: Total number of vulnerabilities found
        affected_versions: List of affected version ranges (optional)
        cvss_scores: List of CVSS scores (optional, for detailed annotation)
        references: Additional reference URLs and metadata (optional)
        scan_metadata: Metadata about the vulnerability scan (optional)

    Example:
        >>> annotation = SPDXAnnotation(
        ...     annotator="vulnerability-scanner",
        ...     annotation_date="2026-01-13T12:00:00Z",
        ...     annotation_type=SPDXAnnotationType.REVIEW,
        ...     comment="Found 5 vulnerabilities in package npm/lodash@4.17.15: CRITICAL: 2, HIGH: 2, LOW: 1",
        ...     spdx_id="SPDXRef-package-npm-lodash-4.17.15",
        ...     vulnerability_ids=["CVE-2021-23337", "GHSA-4w2v-vmj7-klvd"],
        ...     severity_summary={"CRITICAL": 2, "HIGH": 2, "MEDIUM": 0, "LOW": 1},
        ...     source_links=["https://nvd.nist.gov/vuln/detail/CVE-2021-23337"],
        ...     highest_severity=Severity.CRITICAL,
        ...     total_vulnerabilities=5
        ... )
        >>> annotation.annotator
        'vulnerability-scanner'
    """

    annotator: str
    annotation_date: str
    annotation_type: SPDXAnnotationType
    comment: str
    vulnerability_ids: List[str] = field(default_factory=list)
    severity_summary: Dict[str, int] = field(default_factory=dict)
    source_links: List[str] = field(default_factory=list)
    highest_severity: Optional[Severity] = None
    total_vulnerabilities: int = 0
    spdx_id: Optional[str] = None
    affected_versions: List[str] = field(default_factory=list)
    cvss_scores: List[Dict[str, Any]] = field(default_factory=list)
    references: List[Dict[str, str]] = field(default_factory=list)
    scan_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_spdx_dict(self) -> Dict[str, Any]:
        """
        Convert annotation to SPDX JSON format.

        Returns a dictionary following the SPDX 2.3 specification
        for the annotation field.

        Returns:
            Dictionary with SPDX annotation fields:
            - annotator: Tool identifier
            - annotationDate: ISO 8601 timestamp
            - annotationType: SPDX annotation type
            - comment: Human-readable description
            - spdxId: Package ID (if provided)

        Example:
            >>> annotation = SPDXAnnotation(...)
            >>> spdx_dict = annotation.to_spdx_dict()
            >>> spdx_dict["annotationType"]
            'REVIEW'
        """
        spdx_dict = {
            "annotator": self.annotator,
            "annotationDate": self.annotation_date,
            "annotationType": self.annotation_type.value,
            "comment": self.comment,
        }

        if self.spdx_id:
            spdx_dict["spdxId"] = self.spdx_id

        return spdx_dict

    def to_extended_dict(self) -> Dict[str, Any]:
        """
        Convert annotation to extended format with full vulnerability details.

        Returns a dictionary with both SPDX fields and extended vulnerability
        information for tools that support richer annotation data.

        Returns:
            Dictionary with SPDX fields plus:
            - vulnerabilityIds: List of CVE/GHSA IDs
            - severitySummary: Severity level counts
            - sourceLinks: URLs to vulnerability databases
            - highestSeverity: Highest severity found
            - totalVulnerabilities: Total count
            - affectedVersions: Version ranges (if available)
            - cvssScores: CVSS score details (if available)
            - references: Reference URLs with metadata (if available)
            - scanMetadata: Scan metadata (if available)

        Example:
            >>> annotation = SPDXAnnotation(...)
            >>> ext_dict = annotation.to_extended_dict()
            >>> "vulnerabilityIds" in ext_dict
            True
        """
        ext_dict = self.to_spdx_dict()

        # Add extended fields
        ext_dict.update({
            "vulnerabilityIds": self.vulnerability_ids,
            "severitySummary": self.severity_summary,
            "sourceLinks": self.source_links,
            "highestSeverity": self.highest_severity.value if self.highest_severity else None,
            "totalVulnerabilities": self.total_vulnerabilities,
        })

        if self.affected_versions:
            ext_dict["affectedVersions"] = self.affected_versions

        if self.cvss_scores:
            ext_dict["cvssScores"] = self.cvss_scores

        if self.references:
            ext_dict["references"] = self.references

        if self.scan_metadata:
            ext_dict["scanMetadata"] = self.scan_metadata

        return ext_dict


class VulnerabilityAnnotationBuilder:
    """
    Builds SPDX annotations from vulnerability scan results.

    Converts VulnerabilityMatch and ScanResult objects into SPDX annotations
    suitable for inclusion in SBOM documents.

    Example:
        >>> builder = VulnerabilityAnnotationBuilder()
        >>> match = VulnerabilityMatch(...)
        >>> annotation = builder.build_from_match(match, "SPDXRef-package-npm-lodash-4.17.15")
        >>> annotation.annotation_type
        <SPDXAnnotationType.REVIEW: 'REVIEW'>
    """

    DEFAULT_ANNOTATOR = "vulnerability-scanner"

    def __init__(self, annotator: Optional[str] = None):
        """
        Initialize the annotation builder.

        Args:
            annotator: Tool identifier (defaults to "vulnerability-scanner")

        Example:
            >>> builder = VulnerabilityAnnotationBuilder(annotator="my-scanner")
        """
        self.annotator = annotator or self.DEFAULT_ANNOTATOR

    def build_from_match(
        self,
        match: VulnerabilityMatch,
        spdx_id: Optional[str] = None,
        annotation_type: SPDXAnnotationType = SPDXAnnotationType.REVIEW,
        include_cvss: bool = False,
        include_references: bool = True,
    ) -> SPDXAnnotation:
        """
        Build SPDX annotation from a single package's vulnerability match.

        Args:
            match: VulnerabilityMatch for a package
            spdx_id: SPDX ID of the package (optional)
            annotation_type: Type of annotation (default: REVIEW)
            include_cvss: Include detailed CVSS scores (default: False)
            include_references: Include reference URLs (default: True)

        Returns:
            SPDXAnnotation with vulnerability information

        Example:
            >>> match = VulnerabilityMatch(
            ...     package=PackageIdentifier("npm", "lodash", "4.17.15"),
            ...     vulnerabilities=[vuln1, vuln2]
            ... )
            >>> annotation = builder.build_from_match(match, "SPDXRef-package-npm-lodash-4.17.15")
            >>> annotation.total_vulnerabilities
            2
        """
        if not match.vulnerabilities:
            logger.debug(f"No vulnerabilities found for {match.package}, creating empty annotation")

        # Extract vulnerability IDs
        vuln_ids = self._extract_vulnerability_ids(match.vulnerabilities)

        # Extract source links
        source_links = self._extract_source_links(match.vulnerabilities)

        # Determine highest severity
        highest_severity = self._get_highest_severity(match.vulnerabilities)

        # Build severity summary
        severity_summary = {
            "CRITICAL": match.critical_count,
            "HIGH": match.high_count,
            "MEDIUM": match.medium_count,
            "LOW": match.low_count,
        }

        # Build comment
        comment = self._build_comment(match, severity_summary)

        # Extract affected versions (optional)
        affected_versions = self._extract_affected_versions(match.vulnerabilities)

        # Extract CVSS scores (optional)
        cvss_scores = []
        if include_cvss:
            cvss_scores = self._extract_cvss_scores(match.vulnerabilities)

        # Extract references (optional)
        references = []
        if include_references:
            references = self._extract_references(match.vulnerabilities)

        # Build scan metadata
        scan_metadata = {
            "package": str(match.package),
            "ecosystem": match.package.ecosystem,
            "packageName": match.package.name,
            "version": match.package.version,
            "scanTimestamp": datetime.utcnow().isoformat() + "Z",
        }

        return SPDXAnnotation(
            annotator=self.annotator,
            annotation_date=datetime.utcnow().isoformat() + "Z",
            annotation_type=annotation_type,
            comment=comment,
            spdx_id=spdx_id,
            vulnerability_ids=vuln_ids,
            severity_summary=severity_summary,
            source_links=source_links,
            highest_severity=highest_severity,
            total_vulnerabilities=match.total_count,
            affected_versions=affected_versions,
            cvss_scores=cvss_scores,
            references=references,
            scan_metadata=scan_metadata,
        )

    def build_from_scan_result(
        self,
        scan_result: ScanResult,
        annotation_type: SPDXAnnotationType = SPDXAnnotationType.OTHER,
        include_package_details: bool = False,
    ) -> SPDXAnnotation:
        """
        Build SPDX annotation from a complete scan result.

        Creates a document-level annotation summarizing vulnerabilities
        across all scanned packages.

        Args:
            scan_result: ScanResult with multiple package matches
            annotation_type: Type of annotation (default: OTHER for document-level)
            include_package_details: Include per-package breakdown in comment (default: False)

        Returns:
            SPDXAnnotation with aggregate vulnerability information

        Example:
            >>> result = ScanResult(packages=[match1, match2, match3])
            >>> annotation = builder.build_from_scan_result(result)
            >>> annotation.total_vulnerabilities
            15
        """
        if not scan_result.has_vulnerabilities:
            logger.debug("No vulnerabilities found in scan result, creating empty annotation")

        # Extract all vulnerability IDs
        all_vuln_ids = []
        for match in scan_result.packages:
            all_vuln_ids.extend(self._extract_vulnerability_ids(match.vulnerabilities))

        # Deduplicate vulnerability IDs
        unique_vuln_ids = sorted(list(set(all_vuln_ids)))

        # Extract all source links
        all_source_links = []
        for match in scan_result.packages:
            all_source_links.extend(self._extract_source_links(match.vulnerabilities))

        # Deduplicate source links
        unique_source_links = sorted(list(set(all_source_links)))

        # Determine highest severity across all packages
        all_vulnerabilities = []
        for match in scan_result.packages:
            all_vulnerabilities.extend(match.vulnerabilities)
        highest_severity = self._get_highest_severity(all_vulnerabilities)

        # Build comment
        comment = self._build_scan_result_comment(scan_result, include_package_details)

        # Build scan metadata
        scan_metadata = {
            "totalPackages": scan_result.total_packages,
            "affectedPackages": scan_result.affected_packages,
            "sourcesQueried": [source.value for source in scan_result.sources_queried],
            "scanTimestamp": scan_result.scan_timestamp.isoformat() + "Z" if scan_result.scan_timestamp else None,
        }

        return SPDXAnnotation(
            annotator=self.annotator,
            annotation_date=datetime.utcnow().isoformat() + "Z",
            annotation_type=annotation_type,
            comment=comment,
            vulnerability_ids=unique_vuln_ids,
            severity_summary=scan_result.severity_summary,
            source_links=unique_source_links,
            highest_severity=highest_severity,
            total_vulnerabilities=scan_result.total_vulnerabilities,
            scan_metadata=scan_metadata,
        )

    def _extract_vulnerability_ids(self, vulnerabilities: List[Vulnerability]) -> List[str]:
        """
        Extract all vulnerability IDs from a list of vulnerabilities.

        Combines the primary ID and all aliases.

        Args:
            vulnerabilities: List of Vulnerability objects

        Returns:
            List of unique vulnerability IDs (CVE, GHSA, etc.)
        """
        ids = set()
        for vuln in vulnerabilities:
            ids.add(vuln.id)
            ids.update(vuln.aliases)
        return sorted(list(ids))

    def _extract_source_links(self, vulnerabilities: List[Vulnerability]) -> List[str]:
        """
        Extract source links from vulnerability references.

        Filters references to include only authoritative sources
        (advisory databases, issue trackers, etc.).

        Args:
            vulnerabilities: List of Vulnerability objects

        Returns:
            List of unique URLs
        """
        links = set()
        for vuln in vulnerabilities:
            for ref in vuln.references:
                # Prioritize advisory and fix references
                if ref.type in ("ADVISORY", "FIX", "WEB"):
                    links.add(ref.url)
        return sorted(list(links))

    def _get_highest_severity(self, vulnerabilities: List[Vulnerability]) -> Optional[Severity]:
        """
        Determine the highest severity across all vulnerabilities.

        Args:
            vulnerabilities: List of Vulnerability objects

        Returns:
            Highest Severity level or None if no vulnerabilities
        """
        if not vulnerabilities:
            return None

        severities = []
        for vuln in vulnerabilities:
            severity = vuln.get_highest_severity()
            if severity:
                severities.append(severity)

        if not severities:
            return None

        # Return highest severity (CRITICAL > HIGH > MEDIUM > LOW)
        severity_order = {
            Severity.CRITICAL: 4,
            Severity.HIGH: 3,
            Severity.MEDIUM: 2,
            Severity.LOW: 1,
            Severity.NONE: 0,
        }

        return max(severities, key=lambda s: severity_order.get(s, 0))

    def _extract_affected_versions(self, vulnerabilities: List[Vulnerability]) -> List[str]:
        """
        Extract affected version ranges from vulnerabilities.

        Args:
            vulnerabilities: List of Vulnerability objects

        Returns:
            List of version range strings
        """
        versions = []
        for vuln in vulnerabilities:
            for affected in vuln.affected_versions:
                # Build version range string
                if affected.introduced and affected.fixed:
                    range_str = f"{affected.introduced} - {affected.fixed} ({affected.range_type})"
                elif affected.introduced:
                    range_str = f">= {affected.introduced} ({affected.range_type})"
                elif affected.fixed:
                    range_str = f"< {affected.fixed} ({affected.range_type})"
                elif affected.range_string:
                    range_str = f"{affected.range_string} ({affected.range_type})"
                else:
                    continue

                versions.append(range_str)

        return versions

    def _extract_cvss_scores(self, vulnerabilities: List[Vulnerability]) -> List[Dict[str, Any]]:
        """
        Extract CVSS scores from vulnerabilities.

        Args:
            vulnerabilities: List of Vulnerability objects

        Returns:
            List of CVSS score dictionaries
        """
        scores = []
        for vuln in vulnerabilities:
            if vuln.severity:
                scores.append({
                    "vulnerabilityId": vuln.id,
                    "version": vuln.severity.version,
                    "vectorString": vuln.severity.vector_string,
                    "baseScore": vuln.severity.base_score,
                    "baseSeverity": vuln.severity.base_severity.value,
                })

            # Include additional scores
            for score in vuln.additional_scores:
                scores.append({
                    "vulnerabilityId": vuln.id,
                    "version": score.version,
                    "vectorString": score.vector_string,
                    "baseScore": score.base_score,
                    "baseSeverity": score.base_severity.value,
                })

        return scores

    def _extract_references(self, vulnerabilities: List[Vulnerability]) -> List[Dict[str, str]]:
        """
        Extract reference URLs with metadata from vulnerabilities.

        Args:
            vulnerabilities: List of Vulnerability objects

        Returns:
            List of reference dictionaries with URL, type, and source
        """
        refs = []
        for vuln in vulnerabilities:
            for ref in vuln.references:
                refs.append({
                    "url": ref.url,
                    "type": ref.type,
                    "source": ref.source or "UNKNOWN",
                })
        return refs

    def _build_comment(
        self,
        match: VulnerabilityMatch,
        severity_summary: Dict[str, int]
    ) -> str:
        """
        Build human-readable comment for package annotation.

        Args:
            match: VulnerabilityMatch for a package
            severity_summary: Severity level counts

        Returns:
            Human-readable comment string
        """
        if match.total_count == 0:
            return f"No vulnerabilities found in {match.package}"

        # Build severity breakdown
        severity_parts = []
        for severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
            count = severity_summary.get(severity, 0)
            if count > 0:
                severity_parts.append(f"{severity}: {count}")

        severity_breakdown = ", ".join(severity_parts) if severity_parts else "None"

        return (
            f"Found {match.total_count} "
            f"vulnerabilit{'y' if match.total_count == 1 else 'ies'} "
            f"in {match.package}: "
            f"{severity_breakdown}"
        )

    def _build_scan_result_comment(
        self,
        scan_result: ScanResult,
        include_package_details: bool
    ) -> str:
        """
        Build human-readable comment for document-level annotation.

        Args:
            scan_result: ScanResult with multiple packages
            include_package_details: Include per-package breakdown

        Returns:
            Human-readable comment string
        """
        if scan_result.total_vulnerabilities == 0:
            return f"No vulnerabilities found in {scan_result.total_packages} scanned packages"

        # Build severity breakdown
        severity_parts = []
        for severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
            count = scan_result.severity_summary.get(severity, 0)
            if count > 0:
                severity_parts.append(f"{severity}: {count}")

        severity_breakdown = ", ".join(severity_parts) if severity_parts else "None"

        comment = (
            f"Vulnerability scan completed: "
            f"{scan_result.total_vulnerabilities} "
            f"vulnerabilit{'y' if scan_result.total_vulnerabilities == 1 else 'ies'} "
            f"found in {scan_result.affected_packages}/{scan_result.total_packages} "
            f"package{'s' if scan_result.total_packages > 1 else ''}. "
            f"Severity: {severity_breakdown}."
        )

        if include_package_details:
            package_details = []
            for match in scan_result.packages:
                if match.total_count > 0:
                    package_details.append(f"  - {match.package}: {match.total_count} vulnerabilities")

            if package_details:
                comment += "\nAffected packages:\n" + "\n".join(package_details)

        return comment
