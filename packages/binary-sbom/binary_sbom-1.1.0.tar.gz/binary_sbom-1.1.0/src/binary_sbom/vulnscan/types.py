"""
Vulnerability scanning data types and models.

This module defines the core data structures for vulnerability scanning,
including vulnerability findings, CVE entries, severity scores, and API
responses from various vulnerability databases (OSV, NVD, GitHub).

All data structures use type hints and follow Python best practices
for dataclass definitions.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class Severity(Enum):
    """
    CVSS severity levels.

    Follows CVSS v3.1 specification for severity classification
    based on base score ranges.
    """

    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

    @classmethod
    def from_score(cls, score: float) -> "Severity":
        """
        Convert CVSS score to severity level.

        Args:
            score: CVSS base score (0.0 - 10.0)

        Returns:
            Severity enum value based on score ranges:
            - 0.0: NONE
            - 0.1 - 3.9: LOW
            - 4.0 - 6.9: MEDIUM
            - 7.0 - 8.9: HIGH
            - 9.0 - 10.0: CRITICAL

        Example:
            >>> Severity.from_score(9.8)
            <Severity.CRITICAL: 'CRITICAL'>
            >>> Severity.from_score(5.5)
            <Severity.MEDIUM: 'MEDIUM'>
        """
        if score == 0.0:
            return cls.NONE
        if score <= 3.9:
            return cls.LOW
        if score <= 6.9:
            return cls.MEDIUM
        if score <= 8.9:
            return cls.HIGH
        return cls.CRITICAL


class VulnerabilitySource(Enum):
    """
    Vulnerability database sources.

    Identifies which database provided the vulnerability information.
    """

    OSV = "OSV"  # Open Source Vulnerabilities
    NVD = "NVD"  # National Vulnerability Database
    GITHUB = "GITHUB"  # GitHub Security Advisories
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class PackageIdentifier:
    """
    Identifies a software package for vulnerability scanning.

    Attributes:
        ecosystem: Package ecosystem (e.g., "npm", "PyPI", "Maven", "Go")
        name: Package name (e.g., "lodash", "requests", "webpack")
        version: Package version (e.g., "4.17.15", "2.28.0")

    Example:
        >>> pkg = PackageIdentifier(ecosystem="npm", name="lodash", version="4.17.15")
        >>> pkg.ecosystem
        'npm'
    """

    ecosystem: str
    name: str
    version: str

    def __str__(self) -> str:
        """Return string representation."""
        return f"{self.ecosystem}/{self.name}@{self.version}"


@dataclass(frozen=True)
class CVSSScore:
    """
    CVSS (Common Vulnerability Scoring System) score information.

    Supports CVSS v2.0, v3.0, and v3.1 specifications.

    Attributes:
        version: CVSS version (e.g., "3.1")
        vector_string: Full CVSS vector string
        base_score: Base score (0.0 - 10.0)
        base_severity: Severity level (CRITICAL, HIGH, MEDIUM, LOW, NONE)
        impact_score: Impact sub-score (optional)
        exploitability_score: Exploitability sub-score (optional)

    Example:
        >>> cvss = CVSSScore(
        ...     version="3.1",
        ...     vector_string="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
        ...     base_score=9.8,
        ...     base_severity=Severity.CRITICAL
        ... )
        >>> cvss.base_score
        9.8
    """

    version: str
    vector_string: str
    base_score: float
    base_severity: Severity
    impact_score: Optional[float] = None
    exploitability_score: Optional[float] = None

    def __post_init__(self) -> None:
        """Validate CVSS score range."""
        if not 0.0 <= self.base_score <= 10.0:
            raise ValueError(f"CVSS base_score must be between 0.0 and 10.0, got {self.base_score}")


@dataclass(frozen=True)
class Reference:
    """
    Reference URL or link related to a vulnerability.

    Attributes:
        url: Reference URL
        type: Reference type (e.g., "ADVISORY", "FIX", "WEB")
        source: Source database (optional)

    Example:
        >>> ref = Reference(
        ...     url="https://nvd.nist.gov/vuln/detail/CVE-2021-23337",
        ...     type="ADVISORY"
        ... )
    """

    url: str
    type: str
    source: Optional[str] = None


@dataclass(frozen=True)
class AffectedVersion:
    """
    Version range affected by a vulnerability.

    Attributes:
        introduced: Version where vulnerability was introduced (optional)
        fixed: Version where vulnerability was fixed (optional)
        range_type: Range type (e.g., "SEMVER", "ECOSYSTEM", "GIT")
        range_string: Human-readable version range (optional)

    Example:
        >>> affected = AffectedVersion(
        ...     introduced="4.0.0",
        ...     fixed="4.17.21",
        ...     range_type="SEMVER"
        ... )
    """

    introduced: Optional[str] = None
    fixed: Optional[str] = None
    range_type: str = "SEMVER"
    range_string: Optional[str] = None

    def is_affected(self, version: str) -> bool:
        """
        Check if a version is affected by this vulnerability.

        This is a placeholder for version comparison logic.
        Full implementation will handle semver, ecosystem-specific,
        and git-based version matching.

        Args:
            version: Version string to check

        Returns:
            True if version is affected, False otherwise

        Note:
            Full implementation requires semantic version parsing
            and will be added in the version matching module.
        """
        # Placeholder - will be implemented with semver parsing
        return False


@dataclass
class Vulnerability:
    """
    Core vulnerability finding.

    Represents a security vulnerability identified from any source
    (OSV, NVD, GitHub). Provides a unified representation regardless
    of the original database.

    Attributes:
        id: Vulnerability ID (e.g., "CVE-2021-23337", "GHSA-4w2v-vmj7-klvd")
        source: Database that provided this vulnerability
        summary: One-line description of the vulnerability
        description: Full detailed description (optional)
        aliases: Related vulnerability IDs (CVE IDs, GHSA IDs, etc.)
        affected_versions: List of affected version ranges
        severity: CVSS score information (primary score if multiple exist)
        additional_scores: Additional CVSS scores from different sources/versions
        references: List of reference URLs
        published: Publication date (optional)
        modified: Last modification date (optional)
        cwe_ids: List of CWE identifiers (optional)
        raw_data: Raw data from source API (optional)

    Example:
        >>> vuln = Vulnerability(
        ...     id="CVE-2021-23337",
        ...     source=VulnerabilitySource.OSV,
        ...     summary="Prototype Pollution in lodash",
        ...     aliases=["GHSA-4w2v-vmj7-klvd"],
        ...     severity=CVSSScore(...)
        ... )
    """

    id: str
    source: VulnerabilitySource
    summary: str
    description: Optional[str] = None
    aliases: List[str] = field(default_factory=list)
    affected_versions: List[AffectedVersion] = field(default_factory=list)
    severity: Optional[CVSSScore] = None
    additional_scores: List[CVSSScore] = field(default_factory=list)
    references: List[Reference] = field(default_factory=list)
    published: Optional[datetime] = None
    modified: Optional[datetime] = None
    cwe_ids: List[str] = field(default_factory=list)
    raw_data: Optional[Dict[str, Any]] = None

    @property
    def cve_ids(self) -> List[str]:
        """
        Extract CVE IDs from id and aliases.

        Returns:
            List of CVE IDs (e.g., ["CVE-2021-23337"])

        Note:
            Checks both id field and aliases. ID is returned first if present.

        Example:
            >>> vuln = Vulnerability(
            ...     id="CVE-2021-23337",
            ...     source=VulnerabilitySource.OSV,
            ...     summary="Prototype Pollution",
            ...     aliases=["GHSA-4w2v-vmj7-klvd"]
            ... )
            >>> vuln.cve_ids
            ['CVE-2021-23337']
        """
        cves = []
        if self.id.startswith("CVE-"):
            cves.append(self.id)
        cves.extend([alias for alias in self.aliases if alias.startswith("CVE-")])
        return cves

    @property
    def ghsa_ids(self) -> List[str]:
        """
        Extract GHSA IDs from aliases and ID.

        Returns:
            List of GHSA IDs

        Example:
            >>> vuln = Vulnerability(
            ...     id="GHSA-4w2v-vmj7-klvd",
            ...     source=VulnerabilitySource.GITHUB,
            ...     summary="Prototype Pollution"
            ... )
            >>> vuln.ghsa_ids
            ['GHSA-4w2v-vmj7-klvd']
        """
        ids = []
        if self.id.startswith("GHSA-"):
            ids.append(self.id)
        ids.extend([alias for alias in self.aliases if alias.startswith("GHSA-")])
        return ids

    def get_highest_severity(self) -> Optional[Severity]:
        """
        Get the highest severity across all scores.

        Returns:
            Highest Severity level or None if no scores available

        Example:
            >>> vuln.get_highest_severity()
            <Severity.CRITICAL: 'CRITICAL'>
        """
        if not self.severity and not self.additional_scores:
            return None

        scores = [self.severity] + self.additional_scores if self.severity else self.additional_scores
        if not scores:
            return None

        # Sort by base score descending
        scores = [s for s in scores if s is not None]
        if not scores:
            return None

        scores.sort(key=lambda s: s.base_score, reverse=True)
        return scores[0].base_severity


@dataclass
class VulnerabilityMatch:
    """
    Result of matching a package against vulnerability databases.

    Represents a specific package version that was found to have
    vulnerabilities.

    Attributes:
        package: The package being scanned
        vulnerabilities: List of vulnerabilities found for this package
        total_count: Total number of vulnerabilities found
        critical_count: Number of CRITICAL severity vulnerabilities
        high_count: Number of HIGH severity vulnerabilities
        medium_count: Number of MEDIUM severity vulnerabilities
        low_count: Number of LOW severity vulnerabilities

    Example:
        >>> match = VulnerabilityMatch(
        ...     package=PackageIdentifier("npm", "lodash", "4.17.15"),
        ...     vulnerabilities=[vuln1, vuln2]
        ... )
        >>> match.total_count
        2
    """

    package: PackageIdentifier
    vulnerabilities: List[Vulnerability] = field(default_factory=list)
    total_count: int = 0
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0

    def __post_init__(self) -> None:
        """Calculate severity counts from vulnerabilities."""
        self.total_count = len(self.vulnerabilities)
        for vuln in self.vulnerabilities:
            severity = vuln.get_highest_severity()
            if severity == Severity.CRITICAL:
                self.critical_count += 1
            elif severity == Severity.HIGH:
                self.high_count += 1
            elif severity == Severity.MEDIUM:
                self.medium_count += 1
            elif severity == Severity.LOW:
                self.low_count += 1

    def add_vulnerability(self, vuln: Vulnerability) -> None:
        """
        Add a vulnerability and update counts.

        Args:
            vuln: Vulnerability to add

        Example:
            >>> match.add_vulnerability(new_vuln)
            >>> match.total_count
            3
        """
        self.vulnerabilities.append(vuln)
        self.total_count += 1
        severity = vuln.get_highest_severity()
        if severity == Severity.CRITICAL:
            self.critical_count += 1
        elif severity == Severity.HIGH:
            self.high_count += 1
        elif severity == Severity.MEDIUM:
            self.medium_count += 1
        elif severity == Severity.LOW:
            self.low_count += 1


@dataclass
class ScanResult:
    """
    Complete vulnerability scan result for multiple packages.

    Aggregates vulnerability matches for all scanned packages.

    Attributes:
        packages: List of package matches
        total_packages: Total number of packages scanned
        affected_packages: Number of packages with vulnerabilities
        total_vulnerabilities: Total number of vulnerability findings
        severity_summary: Count of vulnerabilities by severity
        scan_timestamp: When the scan was performed
        sources_queried: Which databases were queried
        errors: Any errors encountered during scanning (optional)

    Example:
        >>> result = ScanResult(
        ...     packages=[match1, match2],
        ...     scan_timestamp=datetime.now(),
        ...     sources_queried={VulnerabilitySource.OSV, VulnerabilitySource.NVD}
        ... )
        >>> result.total_vulnerabilities
        5
    """

    packages: List[VulnerabilityMatch] = field(default_factory=list)
    total_packages: int = 0
    affected_packages: int = 0
    total_vulnerabilities: int = 0
    severity_summary: Dict[str, int] = field(default_factory=dict)
    scan_timestamp: Optional[datetime] = None
    sources_queried: Set[VulnerabilitySource] = field(default_factory=set)
    errors: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Calculate summary statistics."""
        if self.scan_timestamp is None:
            self.scan_timestamp = datetime.utcnow()

        # Calculate summary statistics
        self.total_packages = len(self.packages)
        self.affected_packages = len([p for p in self.packages if p.total_count > 0])
        self.total_vulnerabilities = sum(p.total_count for p in self.packages)

        # Aggregate severity counts
        self.severity_summary = {
            "CRITICAL": sum(p.critical_count for p in self.packages),
            "HIGH": sum(p.high_count for p in self.packages),
            "MEDIUM": sum(p.medium_count for p in self.packages),
            "LOW": sum(p.low_count for p in self.packages),
        }

    def add_package_match(self, match: VulnerabilityMatch) -> None:
        """
        Add a package match result.

        Args:
            match: VulnerabilityMatch to add

        Example:
            >>> result.add_package_match(new_match)
        """
        self.packages.append(match)
        # Recalculate summary
        self.total_packages = len(self.packages)
        if match.total_count > 0:
            self.affected_packages += 1
        self.total_vulnerabilities += match.total_count

        # Update severity summary
        self.severity_summary["CRITICAL"] += match.critical_count
        self.severity_summary["HIGH"] += match.high_count
        self.severity_summary["MEDIUM"] += match.medium_count
        self.severity_summary["LOW"] += match.low_count

    @property
    def has_vulnerabilities(self) -> bool:
        """Check if any vulnerabilities were found."""
        return self.total_vulnerabilities > 0

    @property
    def critical_exists(self) -> bool:
        """Check if any CRITICAL vulnerabilities exist."""
        return self.severity_summary.get("CRITICAL", 0) > 0


# ============================================================================
# OSV API Response Types
# ============================================================================


@dataclass(frozen=True)
class OSVSeverity:
    """
    OSV-specific severity information.

    Attributes:
        type: Severity type (e.g., "CVSS_V3")
        score: CVSS vector string
        calculations: Optional calculations object with baseScore and baseSeverity
    """

    type: str
    score: str
    calculations: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class OSVPackage:
    """
    OSV package identifier.

    Attributes:
        name: Package name
        ecosystem: Ecosystem name
    """

    name: str
    ecosystem: str


@dataclass(frozen=True)
class OSVEvent:
    """
    Version event in affected range.

    Attributes:
        introduced: Version where vulnerability introduced (optional)
        fixed: Version where vulnerability fixed (optional)
    """

    introduced: Optional[str] = None
    fixed: Optional[str] = None


@dataclass(frozen=True)
class OSVRange:
    """
    Version range from OSV.

    Attributes:
        type: Range type (SEMVER, ECOSYSTEM, GIT)
        events: List of version events
    """

    type: str
    events: List[OSVEvent] = field(default_factory=list)


@dataclass(frozen=True)
class OSVAffected:
    """
    OSV affected package information.

    Attributes:
        package: Package identifier
        ranges: List of version ranges
    """

    package: OSVPackage
    ranges: List[OSVRange] = field(default_factory=list)


@dataclass
class OSVVuln:
    """
    Raw OSV vulnerability response.

    Direct mapping from OSV API response format.

    Attributes:
        id: Vulnerability ID
        summary: Summary (optional)
        details: Detailed description
        aliases: Related IDs
        modified: Last modified timestamp
        published: Published timestamp
        affected: Affected package versions
        severity: Severity information
        references: Reference links
    """

    id: str
    details: str
    modified: str
    published: str
    affected: List[OSVAffected] = field(default_factory=list)
    severity: List[OSVSeverity] = field(default_factory=list)
    references: List[Reference] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    summary: Optional[str] = None


@dataclass
class OSVQueryResponse:
    """
    OSV query API response.

    Attributes:
        vulns: List of vulnerabilities found
    """

    vulns: List[OSVVuln] = field(default_factory=list)


# ============================================================================
# NVD API Response Types
# ============================================================================


@dataclass(frozen=True)
class NVDCVSSData:
    """
    NVD CVSS data from metrics.

    Attributes:
        version: CVSS version
        vector_string: CVSS vector
        base_score: Base score
        base_severity: Severity level
    """

    version: str
    vector_string: str
    base_score: float
    base_severity: str


@dataclass(frozen=True)
class NVDMetric:
    """
    NVD metric object.

    Attributes:
        cvss_data: CVSS score data
        exploitability_score: Exploitability score (optional)
        impact_score: Impact score (optional)
    """

    cvss_data: NVDCVSSData
    exploitability_score: Optional[float] = None
    impact_score: Optional[float] = None


@dataclass(frozen=True)
class NVDReference:
    """
    NVD reference URL.

    Attributes:
        url: Reference URL
        source: Reference source
        tags: Reference tags (optional)
    """

    url: str
    source: str
    tags: Optional[List[str]] = None


@dataclass(frozen=True)
class NVDWeakness:
    """
    NVD CWE weakness.

    Attributes:
        description: Weakness description with CWE ID
    """

    description: List[Dict[str, str]]


@dataclass
class NVDCVE:
    """
    NVD CVE entry.

    Attributes:
        id: CVE ID
        published: Published timestamp
        last_modified: Last modified timestamp
        descriptions: Vulnerability descriptions
        metrics: CVSS metrics
        weaknesses: CWE weaknesses
        references: Reference URLs
    """

    id: str
    published: str
    last_modified: str
    descriptions: List[Dict[str, str]]
    metrics: Dict[str, List[NVDMetric]] = field(default_factory=dict)
    weaknesses: List[NVDWeakness] = field(default_factory=list)
    references: List[NVDReference] = field(default_factory=list)


@dataclass
class NVDResponse:
    """
    NVD API response.

    Attributes:
        results_per_page: Pagination info
        start_index: Pagination info
        total_results: Total results
        vulnerabilities: List of CVE entries
    """

    results_per_page: int
    start_index: int
    total_results: int
    vulnerabilities: List[Dict[str, NVDCVE]] = field(default_factory=list)


# ============================================================================
# GitHub Advisory Response Types
# ============================================================================


@dataclass(frozen=True)
class GitHubIdentifiers:
    """
    GitHub advisory identifiers.

    Attributes:
        type: Identifier type (GHSA, CVE)
        value: Identifier value
    """

    type: str
    value: str


@dataclass(frozen=True)
class GitHubCVSS:
    """
    GitHub CVSS score.

    Attributes:
        vector_string: CVSS vector
        score: Base score
    """

    vector_string: str
    score: float


@dataclass(frozen=True)
class GitHubPackage:
    """
    GitHub package identifier.

    Attributes:
        ecosystem: Package ecosystem
        name: Package name
    """

    ecosystem: str
    name: str


@dataclass(frozen=True)
class GitHubVulnerability:
    """
    GitHub vulnerability package info.

    Attributes:
        package: Package identifier
        severity: Severity level
        vulnerable_version_range: Affected version range
        first_patched_version: Fixed version (optional)
    """

    package: GitHubPackage
    severity: str
    vulnerable_version_range: str
    first_patched_version: Optional[Dict[str, str]] = None


@dataclass
class GitHubAdvisory:
    """
    GitHub security advisory.

    Attributes:
        ghsa_id: GHSA ID
        summary: Summary
        description: Full description
        severity: Severity level
        identifiers: List of identifiers (GHSA, CVE)
        published_at: Publication timestamp
        updated_at: Update timestamp
        cvss: CVSS score (optional)
        vulnerabilities: List of affected packages
        references: Reference URLs
    """

    ghsa_id: str
    summary: str
    description: str
    severity: str
    identifiers: List[GitHubIdentifiers]
    published_at: str
    updated_at: str
    vulnerabilities: List[GitHubVulnerability] = field(default_factory=list)
    references: List[Dict[str, str]] = field(default_factory=list)
    cvss: Optional[GitHubCVSS] = None
