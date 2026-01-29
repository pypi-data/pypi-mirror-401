"""
OSV (Open Source Vulnerabilities) API client.

This module provides a client for querying the OSV database,
along with conversion utilities to transform OSV responses into
the unified Vulnerability model.

OSV is the primary vulnerability data source - no authentication required.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from binary_sbom.vulnscan.exceptions import APIError
from binary_sbom.vulnscan.types import (
    AffectedVersion,
    CVSSScore,
    OSVAffected,
    OSVEvent,
    OSVPackage,
    OSVQueryResponse,
    OSVRange,
    OSVSeverity,
    OSVVuln,
    PackageIdentifier,
    Reference,
    Severity,
    Vulnerability,
    VulnerabilitySource,
)
from binary_sbom.vulnscan.utils.http_client import HttpClient
from binary_sbom.vulnscan.utils.rate_limiter import RateLimiter
from binary_sbom.vulnscan.utils.cache import VulnerabilityCache


logger = logging.getLogger(__name__)


class OSVClient:
    """
    Client for Open Source Vulnerabilities (OSV) API.

    OSV provides vulnerability data for 15+ package ecosystems
    including npm, PyPI, Maven, Go, and more.

    This client implements query by package name and version using the
    POST /v1/query endpoint. It includes rate limiting, retry logic,
    and proper error handling.

    Attributes:
        base_url: Base URL for OSV API
        http_client: HTTP client with retry logic
        rate_limiter: Rate limiter for API requests

    Example:
        >>> client = OSVClient()
        >>> result = client.query_package("npm", "lodash", "4.17.15")
        >>> len(result.vulns)
        1
    """

    # Default rate limit: 10 requests per second (recommended for OSV)
    DEFAULT_RATE_LIMIT = 10.0

    # Supported OSV ecosystems
    SUPPORTED_ECOSYSTEMS = {
        "PyPI",
        "npm",
        "Go",
        "Maven",
        "NuGet",
        "CRAN",
        "RubyGems",
        "Cargo",
        "Hex",
        "Pub",
        "Composer",
        "Linux",
        "Debian",
        "Alpine",
        "OSS-Fuzz",
    }

    def __init__(
        self,
        base_url: str = "https://api.osv.dev/v1",
        timeout: int = 30,
        rate_limit: float | None = None,
        max_retries: int = 3,
        cache: VulnerabilityCache | None = None,
    ):
        """
        Initialize OSV client.

        Args:
            base_url: Base URL for OSV API (default: https://api.osv.dev/v1)
            timeout: Request timeout in seconds (default: 30)
            rate_limit: Maximum requests per second (default: 10.0)
            max_retries: Maximum number of retry attempts (default: 3)
            cache: Optional cache for storing query results

        Example:
            >>> client = OSVClient(timeout=60, rate_limit=5.0)
            >>> client.base_url
            'https://api.osv.dev/v1'
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.cache = cache

        # Initialize HTTP client with retry logic
        self.http_client = HttpClient(
            retry_max=max_retries,
            timeout=timeout,
        )

        # Initialize rate limiter
        rate_limit = rate_limit or self.DEFAULT_RATE_LIMIT
        self.rate_limiter = RateLimiter(
            requests_per_second=rate_limit,
            capacity=int(rate_limit * 2),  # Allow burst up to 2x rate
        )

        cache_status = "enabled" if cache else "disabled"
        logger.debug(f"OSVClient initialized with base_url={self.base_url}, rate_limit={rate_limit}, cache={cache_status}")

    def query_package(
        self, ecosystem: str, name: str, version: str
    ) -> OSVQueryResponse:
        """
        Query OSV for vulnerabilities in a specific package version.

        Uses the POST /v1/query endpoint to find vulnerabilities affecting
        the specified package version. The request is rate limited and
        includes automatic retry on transient failures.

        Args:
            ecosystem: Package ecosystem (e.g., "npm", "PyPI", "Maven")
            name: Package name
            version: Package version

        Returns:
            OSVQueryResponse containing matching vulnerabilities.
            Returns empty response if no vulnerabilities found.

        Raises:
            APIError: If API request fails after all retries
            ValueError: If ecosystem is not supported

        Example:
            >>> client = OSVClient()
            >>> result = client.query_package("npm", "lodash", "4.17.15")
            >>> vulns = result.vulns
            >>> len(vulns) > 0
            True
        """
        # Check cache first if enabled
        if self.cache:
            cache_key = self.cache.make_key("osv", ecosystem, name, version)
            cached_result = self.cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for OSV query {ecosystem}/{name}@{version}")
                return OSVQueryResponse(vulns=cached_result.get("vulns", []))

        # Validate ecosystem
        if ecosystem not in self.SUPPORTED_ECOSYSTEMS:
            logger.warning(f"Potentially unsupported ecosystem: {ecosystem}")

        # Acquire rate limit token
        if not self.rate_limiter.acquire(blocking=True, timeout=self.timeout + 5):
            raise APIError(
                message=f"Rate limit timeout waiting to query {ecosystem}/{name}@{version}",
                source="OSV",
            )

        # Build request body
        request_body = {
            "package": {
                "name": name,
                "ecosystem": ecosystem,
            },
            "version": version,
        }

        logger.debug(f"Querying OSV for {ecosystem}/{name}@{version}")

        try:
            # Make POST request to /v1/query
            url = f"{self.base_url}/query"
            response_data = self.http_client.post(url, json=request_body)

            # Parse response
            result = self._parse_query_response(response_data)

            # Store in cache if enabled
            if self.cache and result.vulns is not None:
                cache_key = self.cache.make_key("osv", ecosystem, name, version)
                self.cache.put(cache_key, {"vulns": result.vulns})
                logger.debug(f"Cached OSV query result for {ecosystem}/{name}@{version}")

            return result

        except Exception as e:
            # Re-raise API errors as-is
            if isinstance(e, APIError):
                raise
            # Wrap other exceptions
            raise APIError(
                message=f"Failed to query OSV for {ecosystem}/{name}@{version}: {str(e)}",
                source="OSV",
            ) from e

    def _parse_query_response(self, response_data: dict[str, Any]) -> OSVQueryResponse:
        """
        Parse OSV query API response into OSVQueryResponse.

        Args:
            response_data: Raw JSON response from OSV API

        Returns:
            OSVQueryResponse with parsed vulnerabilities

        Example:
            >>> client = OSVClient()
            >>> raw_data = {"vulns": [{"id": "GHSA-xxx", ...}]}
            >>> response = client._parse_query_response(raw_data)
            >>> isinstance(response, OSVQueryResponse)
            True
        """
        # Handle empty response
        if not response_data or "vulns" not in response_data:
            logger.debug("OSV response contains no vulnerabilities")
            return OSVQueryResponse(vulns=[])

        vulns_data = response_data.get("vulns", [])
        if not vulns_data:
            logger.debug("OSV response contains empty vulns list")
            return OSVQueryResponse(vulns=[])

        # Parse each vulnerability
        vulns = []
        for vuln_data in vulns_data:
            try:
                vuln = self._parse_vulnerability(vuln_data)
                vulns.append(vuln)
            except Exception as e:
                logger.warning(f"Failed to parse OSV vulnerability: {e}, skipping. Data: {vuln_data.get('id', 'unknown')}")
                continue

        logger.debug(f"Parsed {len(vulns)} vulnerabilities from OSV response")
        return OSVQueryResponse(vulns=vulns)

    def _parse_vulnerability(self, vuln_data: dict[str, Any]) -> OSVVuln:
        """
        Parse a single OSV vulnerability from API response.

        Args:
            vuln_data: Raw vulnerability data from OSV API

        Returns:
            OSVVuln object with parsed data

        Example:
            >>> client = OSVClient()
            >>> vuln_data = {
            ...     "id": "GHSA-xxx",
            ...     "summary": "Test vuln",
            ...     "details": "Details",
            ...     "modified": "2024-01-01T00:00:00Z",
            ...     "published": "2024-01-01T00:00:00Z",
            ...     "affected": [],
            ...     "severity": [],
            ...     "references": [],
            ...     "aliases": []
            ... }
            >>> vuln = client._parse_vulnerability(vuln_data)
            >>> vuln.id
            'GHSA-xxx'
        """
        # Required fields
        vuln_id = vuln_data.get("id", "")
        details = vuln_data.get("details", "")
        modified = vuln_data.get("modified", "")
        published = vuln_data.get("published", "")

        # Optional fields
        summary = vuln_data.get("summary")
        aliases = vuln_data.get("aliases", [])

        # Parse affected packages
        affected = []
        for affected_data in vuln_data.get("affected", []):
            try:
                affected_pkg = self._parse_affected(affected_data)
                affected.append(affected_pkg)
            except Exception as e:
                logger.warning(f"Failed to parse affected package: {e}")

        # Parse severity information
        severity = []
        for severity_data in vuln_data.get("severity", []):
            try:
                severity_item = self._parse_severity(severity_data)
                severity.append(severity_item)
            except Exception as e:
                logger.warning(f"Failed to parse severity: {e}")

        # Parse references
        references = []
        for ref_data in vuln_data.get("references", []):
            try:
                ref = self._parse_reference(ref_data)
                references.append(ref)
            except Exception as e:
                logger.warning(f"Failed to parse reference: {e}")

        return OSVVuln(
            id=vuln_id,
            summary=summary,
            details=details,
            modified=modified,
            published=published,
            affected=affected,
            severity=severity,
            references=references,
            aliases=aliases,
        )

    def _parse_affected(self, affected_data: dict[str, Any]) -> OSVAffected:
        """
        Parse affected package information.

        Args:
            affected_data: Raw affected package data

        Returns:
            OSVAffected object
        """
        # Parse package info
        pkg_data = affected_data.get("package", {})
        package = OSVPackage(
            name=pkg_data.get("name", ""),
            ecosystem=pkg_data.get("ecosystem", ""),
        )

        # Parse version ranges
        ranges = []
        for range_data in affected_data.get("ranges", []):
            try:
                range_type = range_data.get("type", "SEMVER")
                events = []

                for event_data in range_data.get("events", []):
                    event = OSVEvent(
                        introduced=event_data.get("introduced"),
                        fixed=event_data.get("fixed"),
                    )
                    events.append(event)

                version_range = OSVRange(type=range_type, events=events)
                ranges.append(version_range)

            except Exception as e:
                logger.warning(f"Failed to parse version range: {e}")

        return OSVAffected(package=package, ranges=ranges)

    def _parse_severity(self, severity_data: dict[str, Any]) -> OSVSeverity:
        """
        Parse severity information.

        Args:
            severity_data: Raw severity data

        Returns:
            OSVSeverity object
        """
        return OSVSeverity(
            type=severity_data.get("type", ""),
            score=severity_data.get("score", ""),
            calculations=severity_data.get("calculations"),
        )

    def _parse_reference(self, ref_data: dict[str, Any]) -> Reference:
        """
        Parse reference URL.

        Args:
            ref_data: Raw reference data

        Returns:
            Reference object
        """
        return Reference(
            url=ref_data.get("url", ""),
            type=ref_data.get("type", "WEB"),
            source="OSV",
        )

    def batch_query(self, packages: list[PackageIdentifier]) -> list[OSVQueryResponse]:
        """
        Query OSV for multiple packages in a single request.

        Uses the POST /v1/querybatch endpoint for efficient batch queries.
        This reduces the number of API calls when scanning multiple packages.

        Args:
            packages: List of PackageIdentifier objects

        Returns:
            List of OSVQueryResponse objects, one per package, in the same order
            as the input packages list. Each response contains vulnerabilities
            for the corresponding package.

        Raises:
            APIError: If API request fails after all retries
            ValueError: If packages list is empty

        Example:
            >>> client = OSVClient()
            >>> packages = [
            ...     PackageIdentifier("npm", "lodash", "4.17.15"),
            ...     PackageIdentifier("npm", "webpack", "5.0.0")
            ... ]
            >>> results = client.batch_query(packages)
            >>> len(results)
            2
            >>> len(results[0].vulns) > 0
            True
        """
        if not packages:
            raise ValueError("packages list cannot be empty")

        # Check cache for each package if enabled
        cached_results = {}
        uncached_packages = []
        uncached_indices = []

        if self.cache:
            for idx, pkg in enumerate(packages):
                cache_key = self.cache.make_key("osv", pkg.ecosystem, pkg.name, pkg.version)
                cached_result = self.cache.get(cache_key)
                if cached_result is not None:
                    cached_results[idx] = OSVQueryResponse(vulns=cached_result.get("vulns", []))
                    logger.debug(f"Cache hit for OSV query {pkg.ecosystem}/{pkg.name}@{pkg.version}")
                else:
                    uncached_packages.append(pkg)
                    uncached_indices.append(idx)

        # If all packages were cached, return cached results
        if cached_results and len(cached_results) == len(packages):
            logger.debug(f"Batch query fully cached ({len(packages)} packages)")
            results = [cached_results[idx] for idx in range(len(packages))]
            return results

        # Use full list if cache not enabled or partial cache miss
        packages_to_query = uncached_packages if self.cache else packages

        # Acquire rate limit token (batch queries still count as one request)
        if not self.rate_limiter.acquire(blocking=True, timeout=self.timeout + 5):
            raise APIError(
                message=f"Rate limit timeout waiting for batch query of {len(packages_to_query)} packages",
                source="OSV",
            )

        # Build request body
        queries = []
        for pkg in packages_to_query:
            queries.append({
                "package": {
                    "name": pkg.name,
                    "ecosystem": pkg.ecosystem,
                },
                "version": pkg.version,
            })

        request_body = {"queries": queries}

        logger.debug(f"Querying OSV for batch of {len(packages_to_query)} packages")

        try:
            # Make POST request to /v1/querybatch
            url = f"{self.base_url}/querybatch"
            response_data = self.http_client.post(url, json=request_body)

            # Parse batch response - returns list of responses (one per package)
            api_results = self._parse_batch_response(response_data)

            # Store API results in cache and merge with cached results
            results = []
            api_idx = 0

            for idx in range(len(packages)):
                if idx in cached_results:
                    # Use cached result
                    results.append(cached_results[idx])
                else:
                    # Use API result
                    api_result = api_results[api_idx]

                    # Store in cache if enabled
                    if self.cache and api_result.vulns is not None:
                        pkg = packages_to_query[api_idx]
                        cache_key = self.cache.make_key("osv", pkg.ecosystem, pkg.name, pkg.version)
                        self.cache.put(cache_key, {"vulns": api_result.vulns})
                        logger.debug(f"Cached OSV batch query result for {pkg.ecosystem}/{pkg.name}@{pkg.version}")

                    results.append(api_result)
                    api_idx += 1

            return results

        except Exception as e:
            # Re-raise API errors as-is
            if isinstance(e, APIError):
                raise
            # Wrap other exceptions
            raise APIError(
                message=f"Failed to query OSV batch: {str(e)}",
                source="OSV",
            ) from e

    def _parse_batch_response(self, response_data: dict[str, Any]) -> list[OSVQueryResponse]:
        """
        Parse OSV batch query API response.

        The batch API returns results in the same order as the queries.
        Each result corresponds to the query at the same index.

        Args:
            response_data: Raw JSON response from OSV batch query API

        Returns:
            List of OSVQueryResponse objects, one per query, in the same order

        Example:
            >>> client = OSVClient()
            >>> raw_data = {"results": [{"vulns": [...]}, {"vulns": [...]}]}
            >>> responses = client._parse_batch_response(raw_data)
            >>> len(responses)
            2
            >>> isinstance(responses[0], OSVQueryResponse)
            True
        """
        # Handle empty response
        if not response_data or "results" not in response_data:
            logger.debug("OSV batch response contains no results")
            return []

        results_data = response_data.get("results", [])
        if not results_data:
            logger.debug("OSV batch response contains empty results list")
            return []

        # Parse each result individually to maintain mapping
        responses = []
        for result_data in results_data:
            # Parse each result as a query response
            query_response = self._parse_query_response(result_data)
            responses.append(query_response)

        logger.debug(f"Parsed {len(responses)} package responses from batch query")
        return responses


# ============================================================================
# OSV to Unified Vulnerability Conversion
# ============================================================================


def convert_osv_to_vulnerability(osv_vuln: OSVVuln) -> Vulnerability:
    """
    Convert OSV vulnerability to unified Vulnerability model.

    This function extracts CVE IDs, severity scores, affected versions,
    and references from OSV vulnerability data and maps them to the
    unified Vulnerability format.

    Args:
        osv_vuln: OSVVuln object from OSV API response

    Returns:
        Vulnerability object with unified representation

    Example:
        >>> osv_vuln = OSVVuln(
        ...     id="GHSA-4w2v-vmj7-klvd",
        ...     summary="Prototype Pollution",
        ...     details="Detailed description",
        ...     modified="2021-01-20T00:00:00Z",
        ...     published="2021-01-20T00:00:00Z",
        ...     aliases=["CVE-2021-23337"],
        ...     severity=[...],
        ...     affected=[...],
        ...     references=[...]
        ... )
        >>> vuln = convert_osv_to_vulnerability(osv_vuln)
        >>> vuln.id
        'GHSA-4w2v-vmj7-klvd'
        >>> vuln.cve_ids
        ['CVE-2021-23337']
    """
    # Extract CVE IDs from aliases
    cve_ids = [alias for alias in osv_vuln.aliases if alias.startswith("CVE-")]

    # Parse primary severity score
    severity = _extract_primary_severity(osv_vuln)

    # Parse additional severity scores
    additional_scores = _extract_additional_severities(osv_vuln)

    # Parse affected versions
    affected_versions = _extract_affected_versions(osv_vuln)

    # Parse references
    references = osv_vuln.references

    # Parse timestamps
    published = _parse_timestamp(osv_vuln.published)
    modified = _parse_timestamp(osv_vuln.modified)

    # Create unified Vulnerability
    return Vulnerability(
        id=osv_vuln.id,
        source=VulnerabilitySource.OSV,
        summary=osv_vuln.summary or osv_vuln.details.split("\n")[0] if osv_vuln.details else osv_vuln.id,
        description=osv_vuln.details,
        aliases=osv_vuln.aliases,
        affected_versions=affected_versions,
        severity=severity,
        additional_scores=additional_scores,
        references=references,
        published=published,
        modified=modified,
        cwe_ids=[],  # CWE IDs not provided by OSV
        raw_data=None,  # Raw data can be stored if needed
    )


def _extract_primary_severity(osv_vuln: OSVVuln) -> CVSSScore | None:
    """
    Extract primary CVSS score from OSV vulnerability.

    Prioritizes CVSS_V3 scores over other types. Returns the highest
    scoring CVSS V3 score if multiple exist.

    Args:
        osv_vuln: OSV vulnerability object

    Returns:
        CVSSScore object or None if no severity found
    """
    if not osv_vuln.severity:
        return None

    # Filter for CVSS_V3 severity scores
    cvss_v3_scores = [
        s for s in osv_vuln.severity
        if s.type and "CVSS_V3" in s.type.upper()
    ]

    if not cvss_v3_scores:
        # Fall back to first available severity
        if osv_vuln.severity:
            return _parse_osv_severity(osv_vuln.severity[0])
        return None

    # Sort by base score (highest first)
    def get_base_score(osv_sev: OSVSeverity) -> float:
        if osv_sev.calculations and "baseScore" in osv_sev.calculations:
            return float(osv_sev.calculations["baseScore"])
        return 0.0

    cvss_v3_scores.sort(key=get_base_score, reverse=True)

    # Return highest scoring CVSS V3
    return _parse_osv_severity(cvss_v3_scores[0])


def _extract_additional_severities(osv_vuln: OSVVuln) -> list[CVSSScore]:
    """
    Extract additional CVSS scores from OSV vulnerability.

    Returns all severity scores except the primary one.

    Args:
        osv_vuln: OSV vulnerability object

    Returns:
        List of additional CVSSScore objects
    """
    if not osv_vuln.severity or len(osv_vuln.severity) <= 1:
        return []

    # Get primary severity
    primary = _extract_primary_severity(osv_vuln)

    # Parse all severities
    all_scores = []
    for osv_severity in osv_vuln.severity:
        try:
            cvss = _parse_osv_severity(osv_severity)
            if cvss and cvss != primary:
                all_scores.append(cvss)
        except Exception as e:
            logger.warning(f"Failed to parse additional severity: {e}")
            continue

    return all_scores


def _parse_osv_severity(osv_severity: OSVSeverity) -> CVSSScore | None:
    """
    Parse OSV severity object to CVSSScore.

    Args:
        osv_severity: OSVSeverity object

    Returns:
        CVSSScore object or None if parsing fails
    """
    # Extract CVSS version from type
    severity_type = osv_severity.type or ""
    if "CVSS_V3" in severity_type.upper():
        version = "3.1"
    elif "CVSS_V2" in severity_type.upper():
        version = "2.0"
    else:
        version = "3.1"  # Default to v3.1

    # Extract vector string
    vector_string = osv_severity.score or ""

    # Extract base score and severity from calculations
    base_score = 0.0
    base_severity = Severity.UNKNOWN

    if osv_severity.calculations:
        base_score = float(osv_severity.calculations.get("baseScore", 0.0))

        # Parse base severity
        severity_str = osv_severity.calculations.get("baseSeverity", "")
        try:
            base_severity = Severity(severity_str.upper())
        except ValueError:
            # If not a valid severity enum, derive from score
            base_severity = Severity.from_score(base_score)

    # If no severity in calculations, derive from score
    if base_severity == Severity.UNKNOWN and base_score > 0:
        base_severity = Severity.from_score(base_score)

    # If still unknown, return None
    if base_severity == Severity.UNKNOWN:
        return None

    return CVSSScore(
        version=version,
        vector_string=vector_string,
        base_score=base_score,
        base_severity=base_severity,
    )


def _extract_affected_versions(osv_vuln: OSVVuln) -> list[AffectedVersion]:
    """
    Extract affected version ranges from OSV vulnerability.

    Parses version ranges from all affected packages and converts
    them to AffectedVersion objects.

    Args:
        osv_vuln: OSV vulnerability object

    Returns:
        List of AffectedVersion objects
    """
    affected_versions = []

    for affected in osv_vuln.affected:
        for range_obj in affected.ranges:
            # Extract range type
            range_type = range_obj.type or "SEMVER"

            # Process events to find introduced and fixed versions
            for event in range_obj.events:
                if event.introduced:
                    # Create AffectedVersion for introduced version
                    affected_versions.append(AffectedVersion(
                        introduced=event.introduced,
                        fixed=None,
                        range_type=range_type,
                    ))

                if event.fixed:
                    # Create AffectedVersion for fixed version
                    affected_versions.append(AffectedVersion(
                        introduced=None,
                        fixed=event.fixed,
                        range_type=range_type,
                    ))

    return affected_versions


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
        # Try parsing with timezone
        if timestamp_str.endswith("Z"):
            timestamp_str = timestamp_str[:-1] + "+00:00"
        return datetime.fromisoformat(timestamp_str)
    except (ValueError, AttributeError) as e:
        logger.warning(f"Failed to parse timestamp '{timestamp_str}': {e}")
        return None


# ============================================================================
# OSV Scanner Implementation
# ============================================================================


class OSVScanner:
    """
    Scanner implementation for OSV (Open Source Vulnerabilities) database.

    This class implements the Scanner interface, querying the OSV database
    for vulnerabilities and converting results to the unified Vulnerability model.

    Attributes:
        client: OSVClient instance for API queries

    Example:
        >>> scanner = OSVScanner()
        >>> vulns = scanner.query_by_name_version("npm", "lodash", "4.17.15")
        >>> len(vulns)
        1
        >>> vulns[0].id
        'GHSA-4w2v-vmj7-klvd'
    """

    def __init__(
        self,
        client: OSVClient | None = None,
        timeout: int = 30,
        rate_limit: float | None = None,
        max_retries: int = 3,
    ):
        """
        Initialize OSV scanner.

        Args:
            client: Optional OSVClient instance. If None, creates new client.
            timeout: Request timeout in seconds (default: 30)
            rate_limit: Maximum requests per second (default: 10.0)
            max_retries: Maximum number of retry attempts (default: 3)

        Example:
            >>> scanner = OSVScanner(timeout=60, rate_limit=5.0)
            >>> scanner.get_source()
            <VulnerabilitySource.OSV: 'OSV'>
        """
        if client is None:
            self.client = OSVClient(
                timeout=timeout,
                rate_limit=rate_limit,
                max_retries=max_retries,
            )
        else:
            self.client = client

        logger.debug(f"OSVScanner initialized with client: {self.client.base_url}")

    def query_by_name_version(
        self, ecosystem: str, name: str, version: str
    ) -> list[Vulnerability]:
        """
        Query OSV for vulnerabilities by package name and version.

        Queries the OSV database using the package identifier, then converts
        OSVVuln results to unified Vulnerability objects.

        Args:
            ecosystem: Package ecosystem (e.g., "npm", "PyPI", "Maven", "Go")
            name: Package name (e.g., "lodash", "requests", "webpack")
            version: Package version (e.g., "4.17.15", "2.28.0")

        Returns:
            List of Vulnerability objects affecting this package version.
            Returns empty list if no vulnerabilities found.

        Raises:
            APIError: If the API request fails
            PackageNotFoundError: If package is not found in OSV database
            InvalidVersionError: If version format is invalid

        Example:
            >>> scanner = OSVScanner()
            >>> vulns = scanner.query_by_name_version("npm", "lodash", "4.17.15")
            >>> len(vulns) > 0
            True
            >>> vulns[0].source
            <VulnerabilitySource.OSV: 'OSV'>
        """
        # Query OSV database
        osv_response = self.client.query_package(ecosystem, name, version)

        # Convert OSVVuln objects to unified Vulnerability objects
        vulnerabilities = []
        for osv_vuln in osv_response.vulns:
            try:
                vuln = convert_osv_to_vulnerability(osv_vuln)
                vulnerabilities.append(vuln)
            except Exception as e:
                logger.warning(
                    f"Failed to convert OSV vulnerability {osv_vuln.id} to unified format: {e}"
                )
                continue

        logger.debug(
            f"OSVScanner found {len(vulnerabilities)} vulnerabilities for {ecosystem}/{name}@{version}"
        )
        return vulnerabilities

    def get_source(self) -> VulnerabilitySource:
        """
        Identify the vulnerability source for this scanner.

        Returns:
            VulnerabilitySource.OSV

        Example:
            >>> scanner = OSVScanner()
            >>> scanner.get_source()
            <VulnerabilitySource.OSV: 'OSV'>
        """
        return VulnerabilitySource.OSV

    def supports_batch_queries(self) -> bool:
        """
        Check if this scanner supports batch queries.

        OSV supports batch queries via the /v1/querybatch endpoint.

        Returns:
            True (OSV supports batch queries)

        Example:
            >>> scanner = OSVScanner()
            >>> scanner.supports_batch_queries()
            True
        """
        return True

    def query_batch(
        self, packages: list[PackageIdentifier]
    ) -> dict[PackageIdentifier, list[Vulnerability]]:
        """
        Query multiple packages in a single batch request.

        Uses the OSV batch query endpoint for efficient querying of
        multiple packages. Makes a single API call instead of N individual calls.

        Args:
            packages: List of PackageIdentifier objects

        Returns:
            Dictionary mapping each PackageIdentifier to its list of
            Vulnerability objects. Packages with no vulnerabilities
            have empty lists.

        Raises:
            APIError: If the batch API request fails
            ValueError: If packages list is empty

        Example:
            >>> scanner = OSVScanner()
            >>> packages = [
            ...     PackageIdentifier("npm", "lodash", "4.17.15"),
            ...     PackageIdentifier("npm", "express", "4.17.1")
            ... ]
            >>> results = scanner.query_batch(packages)
            >>> results[packages[0]][0].source
            <VulnerabilitySource.OSV: 'OSV'>
        """
        if not packages:
            raise ValueError("packages list cannot be empty")

        # Query OSV with batch request (single API call)
        osv_responses = self.client.batch_query(packages)

        # Build results dictionary mapping packages to their vulnerabilities
        # OSV returns responses in the same order as the queries
        results = {}
        for i, pkg in enumerate(packages):
            # Get corresponding response for this package
            osv_response = osv_responses[i] if i < len(osv_responses) else None

            # Convert OSVVuln objects to unified Vulnerability objects
            vulnerabilities = []
            if osv_response:
                for osv_vuln in osv_response.vulns:
                    try:
                        vuln = convert_osv_to_vulnerability(osv_vuln)
                        vulnerabilities.append(vuln)
                    except Exception as e:
                        logger.warning(
                            f"Failed to convert OSV vulnerability {osv_vuln.id} to unified format: {e}"
                        )
                        continue

            results[pkg] = vulnerabilities

        logger.debug(
            f"OSVScanner batch query completed for {len(packages)} packages, "
            f"found vulnerabilities for {sum(1 for v in results.values() if v)} packages"
        )

        return results
