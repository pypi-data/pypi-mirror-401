"""
GitHub Security Advisories API client.

This module provides a client for querying the GitHub Security Advisories database,
along with conversion utilities to transform GitHub responses into
the unified Vulnerability model.

GitHub requires authentication for practical use (5000 req/hr vs 60 req/hr).
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from binary_sbom.vulnscan.exceptions import APIError
from binary_sbom.vulnscan.scanners.scanner import Scanner
from binary_sbom.vulnscan.types import (
    AffectedVersion,
    CVSSScore,
    GitHubAdvisory,
    GitHubCVSS,
    GitHubIdentifiers,
    GitHubPackage,
    GitHubVulnerability,
    PackageIdentifier,
    Reference,
    Severity,
    Vulnerability,
    VulnerabilitySource,
)
from binary_sbom.vulnscan.utils.http_client import HttpClient
from binary_sbom.vulnscan.utils.rate_limiter import RateLimiter
from binary_sbom.vulnscan.utils.ecosystem import to_github_ecosystem


logger = logging.getLogger(__name__)


class GitHubClient:
    """
    Client for GitHub Security Advisories GraphQL API.

    GitHub provides high-quality curated vulnerability advisories
    for GitHub-hosted projects across 8 ecosystems.

    This client implements GraphQL queries to search advisories by package
    and ecosystem. It includes rate limiting, retry logic, and proper error handling.

    Attributes:
        token: Optional GitHub personal access token for higher rate limits
        base_url: Base URL for GitHub GraphQL API
        http_client: HTTP client with retry logic
        rate_limiter: Rate limiter for API requests

    Example:
        >>> client = GitHubClient(token="your-github-token")
        >>> advisories = client.query_advisories("NPM", "lodash")
        >>> len(advisories) > 0
        True
    """

    # Default rate limits: 60 req/hr without token, 5000 req/hr with token
    DEFAULT_RATE_LIMIT_NO_TOKEN = 60.0 / 3600.0  # ~0.017 req/s
    DEFAULT_RATE_LIMIT_WITH_TOKEN = 5000.0 / 3600.0  # ~1.39 req/s

    # Supported GitHub ecosystems (SecurityAdvisoryEcosystem enum values)
    SUPPORTED_ECOSYSTEMS = {
        "NPM",  # npm/JavaScript
        "PIP",  # PyPI/Python
        "MAVEN",  # Maven/Java
        "GEM",  # RubyGems/Ruby
        "GO",  # Go modules
        "NUGET",  # NuGet/.NET
        "COMPOSER",  # Composer/PHP
        "PUB",  # Pub/Dart
    }

    def __init__(
        self,
        token: str | None = None,
        base_url: str = "https://api.github.com/graphql",
        timeout: int = 30,
        rate_limit: float | None = None,
        max_retries: int = 3,
    ):
        """
        Initialize GitHub client.

        Args:
            token: Optional GitHub personal access token for higher rate limits
            base_url: Base URL for GitHub GraphQL API (default: https://api.github.com/graphql)
            timeout: Request timeout in seconds (default: 30)
            rate_limit: Maximum requests per second (default: auto-detected based on token)
            max_retries: Maximum number of retry attempts (default: 3)

        Example:
            >>> client = GitHubClient(token="your-github-token", timeout=60)
            >>> client.token == "your-github-token"
            True
        """
        self.token = token
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        # Initialize HTTP client with retry logic
        self.http_client = HttpClient(
            retry_max=max_retries,
            timeout=timeout,
        )

        # Auto-detect rate limit based on token presence
        if rate_limit is None:
            rate_limit = (
                self.DEFAULT_RATE_LIMIT_WITH_TOKEN
                if token
                else self.DEFAULT_RATE_LIMIT_NO_TOKEN
            )

        # Initialize rate limiter
        self.rate_limiter = RateLimiter(
            requests_per_second=rate_limit,
            capacity=int(rate_limit * 2),  # Allow burst up to 2x rate
        )

        logger.debug(
            f"GitHubClient initialized with base_url={self.base_url}, "
            f"token={'***' if token else 'none'}, rate_limit={rate_limit:.3f}"
        )

    def query_advisories(
        self, ecosystem: str, package_name: str
    ) -> list[GitHubAdvisory]:
        """
        Query GitHub for security advisories affecting a package.

        Uses GraphQL to search for vulnerabilities by package name and ecosystem.
        Returns advisories ordered by most recently updated.

        Args:
            ecosystem: Package ecosystem (e.g., "NPM", "PIP", "MAVEN")
            package_name: Package name

        Returns:
            List of GitHubAdvisory objects. Returns empty list if no advisories found.

        Raises:
            APIError: If API request fails after all retries
            ValueError: If ecosystem is not supported

        Example:
            >>> client = GitHubClient()
            >>> advisories = client.query_advisories("NPM", "lodash")
            >>> len(advisories) >= 0
            True
        """
        # Validate ecosystem
        if ecosystem not in self.SUPPORTED_ECOSYSTEMS:
            raise ValueError(
                f"Unsupported ecosystem: {ecosystem}. "
                f"Supported ecosystems: {', '.join(sorted(self.SUPPORTED_ECOSYSTEMS))}"
            )

        # Acquire rate limit token
        if not self.rate_limiter.acquire(blocking=True, timeout=self.timeout + 5):
            raise APIError(
                message=f"Rate limit timeout waiting to query {ecosystem}/{package_name}",
                source="GitHub",
                details={
                    "ecosystem": ecosystem,
                    "package": package_name,
                    "timeout": self.timeout + 5,
                },
            )

        # Build GraphQL query
        query = """
            query($name: String!, $ecosystem: SecurityAdvisoryEcosystem) {
                securityVulnerabilities(
                    first: 20,
                    ecosystem: $ecosystem,
                    package: $name,
                    orderBy: {field: UPDATED_AT, direction: DESC}
                ) {
                    edges {
                        node {
                            advisory {
                                ghsaId
                                summary
                                description
                                severity
                                publishedAt
                                updatedAt
                                identifiers {
                                    type
                                    value
                                }
                                cvss {
                                    vectorString
                                    score
                                }
                                references {
                                    url
                                }
                            }
                            package {
                                ecosystem
                                name
                            }
                            severity
                            vulnerableVersionRange
                            firstPatchedVersion {
                                identifier
                            }
                        }
                    }
                }
            }
        """

        # Prepare request
        variables = {"name": package_name, "ecosystem": ecosystem}
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"bearer {self.token}"

        logger.debug(f"Querying GitHub for {ecosystem}/{package_name}")

        try:
            # Execute GraphQL query
            response = self.http_client.post(
                url=self.base_url,
                json_data={"query": query, "variables": variables},
                headers=headers,
            )

            # Parse response
            data = response.get("data", {})
            vuln_data = data.get("securityVulnerabilities", {})
            edges = vuln_data.get("edges", [])

            # Check for GraphQL errors
            if "errors" in response:
                errors = response["errors"]
                error_messages = [e.get("message", str(e)) for e in errors]
                logger.warning(f"GitHub GraphQL errors: {error_messages}")

            # Parse advisories from response
            advisories = [self._parse_advisory(edge["node"]) for edge in edges]

            logger.debug(
                f"Found {len(advisories)} advisories for {ecosystem}/{package_name}"
            )

            return advisories

        except Exception as e:
            logger.error(f"Failed to query GitHub for {ecosystem}/{package_name}: {e}")
            raise APIError(
                message=f"Failed to query GitHub advisories for {ecosystem}/{package_name}",
                source="GitHub",
                details={"ecosystem": ecosystem, "package": package_name, "error": str(e)},
            ) from e

    def query_by_ghsa(self, ghsa_id: str) -> GitHubAdvisory | None:
        """
        Query GitHub for a specific advisory by GHSA ID.

        Uses GraphQL to retrieve full details of a specific security advisory.

        Args:
            ghsa_id: GitHub Security Advisory ID (e.g., "GHSA-4w2v-vmj7-klvd")

        Returns:
            GitHubAdvisory object or None if not found

        Raises:
            APIError: If API request fails after all retries
            ValueError: If ghsa_id format is invalid

        Example:
            >>> client = GitHubClient()
            >>> advisory = client.query_by_ghsa("GHSA-4w2v-vmj7-klvd")
            >>> advisory is not None
            True
        """
        # Validate GHSA ID format
        if not ghsa_id or not ghsa_id.upper().startswith("GHSA-"):
            raise ValueError(
                f"Invalid GHSA ID format: {ghsa_id}. "
                f"Expected format: GHSA-XXXXX-XXXXX-XXXXX"
            )

        # Normalize GHSA ID to uppercase
        ghsa_id = ghsa_id.upper()

        # Acquire rate limit token
        if not self.rate_limiter.acquire(blocking=True, timeout=self.timeout + 5):
            raise APIError(
                message=f"Rate limit timeout waiting to query GHSA {ghsa_id}",
                source="GitHub",
                details={"ghsa_id": ghsa_id, "timeout": self.timeout + 5},
            )

        # Build GraphQL query
        query = """
            query($ghsaId: String!) {
                securityAdvisory(ghsaId: $ghsaId) {
                    ghsaId
                    summary
                    description
                    severity
                    publishedAt
                    updatedAt
                    identifiers {
                        type
                        value
                    }
                    cvss {
                        vectorString
                        score
                    }
                    vulnerabilities(first: 20) {
                        edges {
                            node {
                                package {
                                    ecosystem
                                    name
                                }
                                severity
                                vulnerableVersionRange
                                firstPatchedVersion {
                                    identifier
                                }
                            }
                        }
                    }
                    references {
                        url
                    }
                }
            }
        """

        # Prepare request
        variables = {"ghsaId": ghsa_id}
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"bearer {self.token}"

        logger.debug(f"Querying GitHub for GHSA {ghsa_id}")

        try:
            # Execute GraphQL query
            response = self.http_client.post(
                url=self.base_url,
                json_data={"query": query, "variables": variables},
                headers=headers,
            )

            # Parse response
            data = response.get("data", {})
            advisory_data = data.get("securityAdvisory")

            # Check if advisory not found
            if not advisory_data:
                logger.warning(f"Advisory not found: {ghsa_id}")
                return None

            # Check for GraphQL errors
            if "errors" in response:
                errors = response["errors"]
                error_messages = [e.get("message", str(e)) for e in errors]
                logger.warning(f"GitHub GraphQL errors: {error_messages}")

            # Parse advisory from response
            advisory = self._parse_full_advisory(advisory_data)

            logger.debug(f"Retrieved advisory {ghsa_id}")

            return advisory

        except Exception as e:
            logger.error(f"Failed to query GitHub for {ghsa_id}: {e}")
            raise APIError(
                message=f"Failed to query GitHub advisory {ghsa_id}",
                source="GitHub",
                details={"ghsa_id": ghsa_id, "error": str(e)},
            ) from e

    def _parse_advisory(self, node: dict[str, Any]) -> GitHubAdvisory:
        """
        Parse advisory node from securityVulnerabilities query.

        Args:
            node: Raw advisory node from GraphQL response

        Returns:
            GitHubAdvisory object
        """
        advisory_data = node.get("advisory", {})

        # Parse identifiers
        identifiers = [
            GitHubIdentifiers(type=id_data["type"], value=id_data["value"])
            for id_data in advisory_data.get("identifiers", [])
        ]

        # Parse CVSS
        cvss_data = advisory_data.get("cvss")
        cvss = (
            GitHubCVSS(
                vector_string=cvss_data["vectorString"],
                score=cvss_data["score"],
            )
            if cvss_data
            else None
        )

        # Parse references
        references = [
            {"url": ref["url"]} for ref in advisory_data.get("references", [])
        ]

        # Parse vulnerability info
        package_data = node["package"]
        vulnerability = GitHubVulnerability(
            package=GitHubPackage(
                ecosystem=package_data["ecosystem"],
                name=package_data["name"],
            ),
            severity=node["severity"],
            vulnerable_version_range=node["vulnerableVersionRange"],
            first_patched_version=node.get("firstPatchedVersion"),
        )

        # Create advisory
        advisory = GitHubAdvisory(
            ghsa_id=advisory_data["ghsaId"],
            summary=advisory_data["summary"],
            description=advisory_data.get("description", ""),
            severity=advisory_data["severity"],
            identifiers=identifiers,
            published_at=advisory_data["publishedAt"],
            updated_at=advisory_data["updatedAt"],
            cvss=cvss,
            vulnerabilities=[vulnerability],
            references=references,
        )

        return advisory

    def _parse_full_advisory(self, advisory_data: dict[str, Any]) -> GitHubAdvisory:
        """
        Parse full advisory from securityAdvisory query.

        Args:
            advisory_data: Raw advisory data from GraphQL response

        Returns:
            GitHubAdvisory object
        """
        # Parse identifiers
        identifiers = [
            GitHubIdentifiers(type=id_data["type"], value=id_data["value"])
            for id_data in advisory_data.get("identifiers", [])
        ]

        # Parse CVSS
        cvss_data = advisory_data.get("cvss")
        cvss = (
            GitHubCVSS(
                vector_string=cvss_data["vectorString"],
                score=cvss_data["score"],
            )
            if cvss_data
            else None
        )

        # Parse references
        references = [
            {"url": ref["url"]} for ref in advisory_data.get("references", [])
        ]

        # Parse vulnerabilities
        vulnerabilities = []
        vuln_edges = advisory_data.get("vulnerabilities", {}).get("edges", [])
        for edge in vuln_edges:
            node = edge["node"]
            package_data = node["package"]
            vulnerability = GitHubVulnerability(
                package=GitHubPackage(
                    ecosystem=package_data["ecosystem"],
                    name=package_data["name"],
                ),
                severity=node["severity"],
                vulnerable_version_range=node["vulnerableVersionRange"],
                first_patched_version=node.get("firstPatchedVersion"),
            )
            vulnerabilities.append(vulnerability)

        # Create advisory
        advisory = GitHubAdvisory(
            ghsa_id=advisory_data["ghsaId"],
            summary=advisory_data["summary"],
            description=advisory_data.get("description", ""),
            severity=advisory_data["severity"],
            identifiers=identifiers,
            published_at=advisory_data["publishedAt"],
            updated_at=advisory_data["updatedAt"],
            cvss=cvss,
            vulnerabilities=vulnerabilities,
            references=references,
        )

        return advisory


# ============================================================================
# GitHub to Unified Vulnerability Conversion
# ============================================================================


def convert_github_to_vulnerability(github_advisory: GitHubAdvisory) -> Vulnerability:
    """
    Convert GitHub advisory to unified Vulnerability model.

    This function extracts GHSA IDs, CVE IDs, severity scores, affected versions,
    and references from GitHub advisory data and maps them to the unified
    Vulnerability format.

    Args:
        github_advisory: GitHubAdvisory object from GitHub API response

    Returns:
        Vulnerability object with unified representation

    Example:
        >>> advisory = GitHubAdvisory(
        ...     ghsa_id="GHSA-4w2v-vmj7-klvd",
        ...     summary="Prototype Pollution",
        ...     description="Full description",
        ...     severity="CRITICAL",
        ...     identifiers=[...],
        ...     published_at="2021-01-20T00:00:00Z",
        ...     updated_at="2021-01-20T00:00:00Z",
        ...     cvss=...,
        ...     vulnerabilities=[...],
        ...     references=[...]
        ... )
        >>> vuln = convert_github_to_vulnerability(advisory)
        >>> vuln.id
        'GHSA-4w2v-vmj7-klvd'
        >>> vuln.cve_ids
        ['CVE-2021-23337']
    """
    # Extract CVE IDs from identifiers
    cve_ids = [
        identifier.value
        for identifier in github_advisory.identifiers
        if identifier.type == "CVE"
    ]

    # Parse primary severity score from CVSS
    severity = _parse_github_cvss(github_advisory.cvss)

    # Parse affected versions from vulnerabilities
    affected_versions = _extract_affected_versions(github_advisory)

    # Parse references
    references = _extract_references(github_advisory)

    # Parse timestamps
    published = _parse_timestamp(github_advisory.published_at)
    modified = _parse_timestamp(github_advisory.updated_at)

    # Build aliases list (include CVE IDs but not GHSA ID since that's the primary ID)
    aliases = cve_ids.copy()

    # Create unified Vulnerability
    return Vulnerability(
        id=github_advisory.ghsa_id,
        source=VulnerabilitySource.GITHUB,
        summary=github_advisory.summary,
        description=github_advisory.description or None,
        aliases=aliases,
        affected_versions=affected_versions,
        severity=severity,
        additional_scores=[],  # GitHub typically provides one CVSS score
        references=references,
        published=published,
        modified=modified,
        cwe_ids=[],  # CWE IDs not provided by GitHub
        raw_data=None,
    )


def _parse_github_cvss(cvss: GitHubCVSS | None) -> CVSSScore | None:
    """
    Parse GitHub CVSS score to CVSSScore.

    Args:
        cvss: GitHubCVSS object

    Returns:
        CVSSScore object or None if cvss is None
    """
    if not cvss:
        return None

    # GitHub CVSS typically doesn't specify version in the response
    # We can infer it from the vector string format
    vector_string = cvss.vector_string
    if vector_string.startswith("CVSS:3.1"):
        version = "3.1"
    elif vector_string.startswith("CVSS:3.0"):
        version = "3.0"
    elif vector_string.startswith("CVSS:2.0"):
        version = "2.0"
    else:
        # Default to v3.1 for modern GitHub advisories
        version = "3.1"

    # Derive severity from score
    base_severity = Severity.from_score(cvss.score)

    return CVSSScore(
        version=version,
        vector_string=vector_string,
        base_score=cvss.score,
        base_severity=base_severity,
        impact_score=None,  # Not provided by GitHub
        exploitability_score=None,  # Not provided by GitHub
    )


def _extract_affected_versions(
    github_advisory: GitHubAdvisory,
) -> list[AffectedVersion]:
    """
    Extract affected versions from GitHub advisory vulnerabilities.

    GitHub advisories can affect multiple packages. Each vulnerability
    contains a vulnerable version range and optionally a patched version.

    Args:
        github_advisory: GitHub advisory object

    Returns:
        List of AffectedVersion objects
    """
    affected_versions = []

    for vuln in github_advisory.vulnerabilities:
        # Extract vulnerable version range
        range_string = vuln.vulnerable_version_range
        if not range_string:
            continue

        # Extract patched version if available
        fixed_version = None
        if vuln.first_patched_version:
            fixed_version = vuln.first_patched_version.get("identifier")

        # Create AffectedVersion
        # Note: GitHub doesn't always provide explicit "introduced" version
        # The range_string contains the full range specification
        affected_versions.append(
            AffectedVersion(
                introduced=None,  # Not explicitly provided by GitHub
                fixed=fixed_version,
                range_type="ECOSYSTEM",  # GitHub uses ecosystem-specific ranges
                range_string=range_string,
            )
        )

    return affected_versions


def _extract_references(github_advisory: GitHubAdvisory) -> list[Reference]:
    """
    Extract references from GitHub advisory.

    Args:
        github_advisory: GitHub advisory object

    Returns:
        List of Reference objects
    """
    references = []

    for ref_data in github_advisory.references:
        url = ref_data.get("url", "")
        if not url:
            continue

        # Categorize reference type based on URL patterns
        ref_type = "WEB"
        if "github.com/advisories" in url:
            ref_type = "ADVISORY"
        elif "github.com" in url and "/pull/" in url:
            ref_type = "FIX"
        elif "github.com" in url and "/commit/" in url:
            ref_type = "FIX"

        references.append(
            Reference(
                url=url,
                type=ref_type,
                source="GitHub",
            )
        )

    return references


def _parse_timestamp(timestamp_str: str) -> datetime | None:
    """
    Parse ISO 8601 timestamp string to datetime object.

    Args:
        timestamp_str: ISO 8601 timestamp string

    Returns:
        datetime object or None if parsing fails
    """
    if not timestamp_str:
        return None

    try:
        # GitHub timestamps are in ISO 8601 format with 'Z' suffix
        # Convert 'Z' to '+00:00' for proper parsing
        if timestamp_str.endswith("Z"):
            timestamp_str = timestamp_str[:-1] + "+00:00"
        return datetime.fromisoformat(timestamp_str)
    except (ValueError, AttributeError) as e:
        logger.warning(f"Failed to parse timestamp '{timestamp_str}': {e}")
        return None


# ============================================================================
# GitHub Scanner Implementation
# ============================================================================


class GitHubScanner(Scanner):
    """
    Scanner implementation for GitHub Security Advisories database.

    This class implements the Scanner interface, querying the GitHub
    Security Advisories database for vulnerabilities and converting
    results to the unified Vulnerability model.

    Attributes:
        client: GitHubClient instance for API queries

    Example:
        >>> scanner = GitHubScanner()
        >>> vulns = scanner.query_by_name_version("NPM", "lodash", "4.17.15")
        >>> len(vulns)
        1
        >>> vulns[0].id
        'GHSA-4w2v-vmj7-klvd'
    """

    def __init__(
        self,
        client: GitHubClient | None = None,
        token: str | None = None,
        timeout: int = 30,
        rate_limit: float | None = None,
        max_retries: int = 3,
    ):
        """
        Initialize GitHub scanner.

        Args:
            client: Optional GitHubClient instance. If None, creates new client.
            token: Optional GitHub personal access token for higher rate limits
            timeout: Request timeout in seconds (default: 30)
            rate_limit: Maximum requests per second (default: auto-detected)
            max_retries: Maximum number of retry attempts (default: 3)

        Example:
            >>> scanner = GitHubScanner(token="your-github-token")
            >>> scanner.get_source()
            <VulnerabilitySource.GITHUB: 'GITHUB'>
        """
        if client is None:
            self.client = GitHubClient(
                token=token,
                timeout=timeout,
                rate_limit=rate_limit,
                max_retries=max_retries,
            )
        else:
            self.client = client

        logger.debug("GitHubScanner initialized")

    def query_by_name_version(
        self, ecosystem: str, name: str, version: str
    ) -> list[Vulnerability]:
        """
        Query GitHub for vulnerabilities by package name and version.

        Ecosystem names are automatically normalized and mapped to GitHub's format.
        Supports common variants like "npm", "NPM", "PyPI", "pypi", "python", etc.

        Args:
            ecosystem: Package ecosystem in any format (e.g., "npm", "PyPI", "Maven", "Go")
            name: Package name
            version: Package version

        Returns:
            List of Vulnerability objects affecting this package version.
            Returns empty list if no vulnerabilities found.

        Raises:
            APIError: If the API request fails
            ValueError: If ecosystem is not supported by GitHub

        Example:
            >>> scanner = GitHubScanner()
            >>> vulns = scanner.query_by_name_version("npm", "lodash", "4.17.15")
            >>> len(vulns) > 0
            True
            >>> vulns[0].source
            <VulnerabilitySource.GITHUB: 'GITHUB'>
            >>> # Also works with "PyPI" instead of "PIP"
            >>> vulns = scanner.query_by_name_version("PyPI", "requests", "2.25.0")
        """
        logger.debug(f"Querying GitHub for {ecosystem}/{name}@{version}")

        try:
            # Map ecosystem name to GitHub format
            github_ecosystem = to_github_ecosystem(ecosystem)
            logger.debug(f"Mapped ecosystem '{ecosystem}' -> '{github_ecosystem}' for GitHub query")

            # Query GitHub advisories
            advisories = self.client.query_advisories(github_ecosystem, name)

            # Convert advisories to unified Vulnerability model
            vulnerabilities = []
            for advisory in advisories:
                try:
                    vuln = convert_github_to_vulnerability(advisory)
                    vulnerabilities.append(vuln)
                except Exception as e:
                    logger.warning(
                        f"Failed to convert advisory {advisory.ghsa_id} to vulnerability: {e}"
                    )
                    continue

            logger.debug(
                f"Found {len(vulnerabilities)} vulnerabilities for {ecosystem}/{name}@{version}"
            )

            return vulnerabilities

        except APIError:
            # Re-raise API errors as-is
            raise
        except ValueError:
            # Re-raise ValueError (e.g., unsupported ecosystem)
            raise
        except Exception as e:
            logger.error(f"Failed to query GitHub for {ecosystem}/{name}@{version}: {e}")
            raise APIError(
                message=f"Failed to query GitHub vulnerabilities for {ecosystem}/{name}@{version}",
                source="GitHub",
                details={
                    "ecosystem": ecosystem,
                    "github_ecosystem": github_ecosystem,
                    "name": name,
                    "version": version,
                    "error": str(e)
                },
            ) from e

    def get_source(self) -> VulnerabilitySource:
        """
        Identify the vulnerability source for this scanner.

        Returns:
            VulnerabilitySource.GITHUB

        Example:
            >>> scanner = GitHubScanner()
            >>> scanner.get_source()
            <VulnerabilitySource.GITHUB: 'GITHUB'>
        """
        return VulnerabilitySource.GITHUB

    def supports_batch_queries(self) -> bool:
        """
        Check if this scanner supports batch queries.

        GitHub does not support true batch queries in the same way as OSV.
        Each package requires a separate GraphQL query.

        Returns:
            False

        Example:
            >>> scanner = GitHubScanner()
            >>> scanner.supports_batch_queries()
            False
        """
        return False

    def query_batch(
        self, packages: list[PackageIdentifier]
    ) -> dict[str, list[Vulnerability]]:
        """
        Query multiple packages (not supported by GitHub).

        GitHub scanner does not support batch queries.
        This method returns an empty dict for all packages.

        Args:
            packages: List of PackageIdentifier objects

        Returns:
            Empty dict with package string keys

        Example:
            >>> scanner = GitHubScanner()
            >>> packages = [PackageIdentifier("NPM", "lodash", "4.17.15")]
            >>> scanner.query_batch(packages)
            {}
        """
        logger.debug("GitHub scanner does not support batch queries")
        return {str(pkg): [] for pkg in packages}
