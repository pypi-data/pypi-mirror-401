"""
NVD (National Vulnerability Database) API client.

This module provides a client for querying the NVD database,
along with conversion utilities to transform NVD responses into
the unified Vulnerability model.

NVD API v2.0 requires an API key for practical use.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from binary_sbom.vulnscan.exceptions import APIError
from binary_sbom.vulnscan.types import (
    AffectedVersion,
    CVSSScore,
    NVDCVE,
    NVDMetric,
    NVDReference,
    NVDResponse,
    NVDWeakness,
    PackageIdentifier,
    Reference,
    Severity,
    Vulnerability,
    VulnerabilitySource,
)
from binary_sbom.vulnscan.utils.http_client import HttpClient
from binary_sbom.vulnscan.utils.rate_limiter import RateLimiter


logger = logging.getLogger(__name__)


class NVDClient:
    """
    Client for National Vulnerability Database (NVD) API v2.0.

    NVD provides authoritative CVE data from the US government.
    API key recommended for higher rate limits (50 req/30s vs 5 req/30s).

    This client implements query by CVE ID using the GET /cves/2.0 endpoint.
    It includes rate limiting, retry logic, and proper error handling.

    Attributes:
        api_key: Optional NVD API key for higher rate limits
        base_url: Base URL for NVD API
        http_client: HTTP client with retry logic
        rate_limiter: Rate limiter for API requests

    Example:
        >>> client = NVDClient(api_key="your-api-key")
        >>> result = client.query_cve("CVE-2021-23337")
        >>> len(result.vulnerabilities)
        1
    """

    # Default rate limits: 5 req/30s without key, 50 req/30s with key
    DEFAULT_RATE_LIMIT_NO_KEY = 5.0 / 30.0  # ~0.167 req/s
    DEFAULT_RATE_LIMIT_WITH_KEY = 50.0 / 30.0  # ~1.67 req/s

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://services.nvd.nist.gov/rest/json/cves/2.0",
        timeout: int = 30,
        rate_limit: float | None = None,
        max_retries: int = 3,
    ):
        """
        Initialize NVD client.

        Args:
            api_key: Optional NVD API key for higher rate limits
            base_url: Base URL for NVD CVE API (default: NVD v2.0 endpoint)
            timeout: Request timeout in seconds (default: 30)
            rate_limit: Maximum requests per second (default: auto-detected based on API key)
            max_retries: Maximum number of retry attempts (default: 3)

        Example:
            >>> client = NVDClient(api_key="your-api-key", timeout=60)
            >>> client.api_key == "your-api-key"
            True
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        # Initialize HTTP client with retry logic
        self.http_client = HttpClient(
            retry_max=max_retries,
            timeout=timeout,
        )

        # Auto-detect rate limit based on API key presence
        if rate_limit is None:
            rate_limit = (
                self.DEFAULT_RATE_LIMIT_WITH_KEY
                if api_key
                else self.DEFAULT_RATE_LIMIT_NO_KEY
            )

        # Initialize rate limiter
        self.rate_limiter = RateLimiter(
            requests_per_second=rate_limit,
            capacity=int(rate_limit * 2),  # Allow burst up to 2x rate
        )

        logger.debug(
            f"NVDClient initialized with base_url={self.base_url}, "
            f"api_key={'***' if api_key else 'none'}, rate_limit={rate_limit:.3f}"
        )

    def query_cve(self, cve_id: str) -> NVDResponse:
        """
        Query NVD for a specific CVE by ID.

        Uses the GET /cves/2.0 endpoint with the cveId parameter to retrieve
        detailed information about a specific CVE. The request is rate limited
        and includes automatic retry on transient failures.

        Args:
            cve_id: CVE identifier (e.g., "CVE-2021-23337")

        Returns:
            NVDResponse containing CVE details. Returns empty response if CVE not found.

        Raises:
            APIError: If API request fails after all retries
            ValueError: If cve_id format is invalid

        Example:
            >>> client = NVDClient()
            >>> result = client.query_cve("CVE-2021-23337")
            >>> len(result.vulnerabilities) > 0
            True
        """
        # Validate CVE ID format
        if not cve_id or not cve_id.upper().startswith("CVE-"):
            raise ValueError(f"Invalid CVE ID format: {cve_id}. Expected format: CVE-YYYY-NNNN...")

        # Normalize CVE ID to uppercase
        cve_id = cve_id.upper()

        # Acquire rate limit token
        if not self.rate_limiter.acquire(blocking=True, timeout=self.timeout + 5):
            raise APIError(
                message=f"Rate limit timeout waiting to query CVE {cve_id}",
                source="NVD",
            )

        # Build request headers with API key if provided
        headers = {}
        if self.api_key:
            headers["apiKey"] = self.api_key

        # Build query parameters
        params = {"cveId": cve_id, "isExactMatch": "true"}

        logger.debug(f"Querying NVD for {cve_id}")

        try:
            # Make GET request to /cves/2.0
            response_data = self.http_client.get(
                self.base_url,
                params=params,
                headers=headers if headers else None,
            )

            # Parse response
            return self._parse_response(response_data)

        except Exception as e:
            # Re-raise API errors as-is
            if isinstance(e, APIError):
                raise
            # Wrap other exceptions
            raise APIError(
                message=f"Failed to query NVD for {cve_id}: {str(e)}",
                source="NVD",
            ) from e

    def _parse_response(self, response_data: dict[str, Any]) -> NVDResponse:
        """
        Parse NVD API response into NVDResponse.

        Args:
            response_data: Raw JSON response from NVD API

        Returns:
            NVDResponse with parsed vulnerabilities

        Example:
            >>> client = NVDClient()
            >>> raw_data = {"vulnerabilities": [{"cve": {"id": "CVE-2021-23337", ...}}]}
            >>> response = client._parse_response(raw_data)
            >>> isinstance(response, NVDResponse)
            True
        """
        # Handle empty response
        if not response_data or "vulnerabilities" not in response_data:
            logger.debug("NVD response contains no vulnerabilities")
            return NVDResponse(
                results_per_page=0,
                start_index=0,
                total_results=0,
                vulnerabilities=[],
            )

        vulns_data = response_data.get("vulnerabilities", [])
        if not vulns_data:
            logger.debug("NVD response contains empty vulnerabilities list")
            return NVDResponse(
                results_per_page=response_data.get("resultsPerPage", 0),
                start_index=response_data.get("startIndex", 0),
                total_results=response_data.get("totalResults", 0),
                vulnerabilities=[],
            )

        # Parse each vulnerability
        vulnerabilities = []
        for vuln_dict in vulns_data:
            try:
                cve = self._parse_cve(vuln_dict.get("cve", {}))
                vulnerabilities.append({"cve": cve})
            except Exception as e:
                logger.warning(
                    f"Failed to parse NVD CVE: {e}, skipping. "
                    f"Data: {vuln_dict.get('cve', {}).get('id', 'unknown')}"
                )
                continue

        logger.debug(f"Parsed {len(vulnerabilities)} vulnerabilities from NVD response")

        return NVDResponse(
            results_per_page=response_data.get("resultsPerPage", len(vulnerabilities)),
            start_index=response_data.get("startIndex", 0),
            total_results=response_data.get("totalResults", len(vulnerabilities)),
            vulnerabilities=vulnerabilities,
        )

    def _parse_cve(self, cve_data: dict[str, Any]) -> NVDCVE:
        """
        Parse a single NVD CVE from API response.

        Args:
            cve_data: Raw CVE data from NVD API

        Returns:
            NVDCVE object with parsed data

        Example:
            >>> client = NVDClient()
            >>> cve_data = {
            ...     "id": "CVE-2021-23337",
            ...     "published": "2021-01-20T18:15:14.590",
            ...     "descriptions": [{"lang": "en", "value": "Test"}]
            ... }
            >>> cve = client._parse_cve(cve_data)
            >>> cve.id
            'CVE-2021-23337'
        """
        # Extract basic fields
        cve_id = cve_data.get("id", "")
        published = cve_data.get("published", "")
        last_modified = cve_data.get("lastModified", "")
        descriptions = cve_data.get("descriptions", [])

        # Parse metrics (CVSS scores)
        metrics = {}
        for metric_type, metric_list in cve_data.get("metrics", {}).items():
            parsed_metrics = []
            for metric_data in metric_list:
                try:
                    metric = self._parse_metric(metric_data)
                    parsed_metrics.append(metric)
                except Exception as e:
                    logger.warning(f"Failed to parse NVD metric: {e}")
                    continue
            if parsed_metrics:
                metrics[metric_type] = parsed_metrics

        # Parse weaknesses (CWE IDs)
        weaknesses = []
        for weakness_data in cve_data.get("weaknesses", []):
            try:
                weakness = NVDWeakness(description=weakness_data.get("description", []))
                weaknesses.append(weakness)
            except Exception as e:
                logger.warning(f"Failed to parse NVD weakness: {e}")
                continue

        # Parse references
        references = []
        for ref_data in cve_data.get("references", []):
            try:
                reference = NVDReference(
                    url=ref_data.get("url", ""),
                    source=ref_data.get("source", ""),
                    tags=ref_data.get("tags"),
                )
                references.append(reference)
            except Exception as e:
                logger.warning(f"Failed to parse NVD reference: {e}")
                continue

        return NVDCVE(
            id=cve_id,
            published=published,
            last_modified=last_modified,
            descriptions=descriptions,
            metrics=metrics,
            weaknesses=weaknesses,
            references=references,
        )

    def _parse_metric(self, metric_data: dict[str, Any]) -> NVDMetric:
        """
        Parse CVSS metric from NVD API response.

        Args:
            metric_data: Raw metric data from NVD API

        Returns:
            NVDMetric object with parsed data

        Example:
            >>> client = NVDClient()
            >>> metric_data = {
            ...     "cvssData": {
            ...         "version": "3.1",
            ...         "vectorString": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
            ...         "baseScore": 9.8
            ...     },
            ...     "exploitabilityScore": 3.9,
            ...     "impactScore": 5.9
            ... }
            >>> metric = client._parse_metric(metric_data)
            >>> metric.cvss_data["baseScore"]
            9.8
        """
        cvss_data = metric_data.get("cvssData", {})
        exploitability_score = metric_data.get("exploitabilityScore")
        impact_score = metric_data.get("impactScore")

        return NVDMetric(
            cvss_data=cvss_data,
            exploitability_score=exploitability_score,
            impact_score=impact_score,
        )


# ============================================================================
# NVD to Unified Vulnerability Conversion
# ============================================================================


def convert_nvd_to_vulnerability(nvd_cve: NVDCVE) -> Vulnerability:
    """
    Convert NVD CVE to unified Vulnerability model.

    This function extracts CVE IDs, CVSS scores, CWE IDs, descriptions,
    and references from NVD CVE data and maps them to the unified
    Vulnerability format.

    Args:
        nvd_cve: NVDCVE object from NVD API response

    Returns:
        Vulnerability object with unified representation

    Example:
        >>> nvd_cve = NVDCVE(
        ...     id="CVE-2021-23337",
        ...     published="2021-01-20T18:15:14.590",
        ...     last_modified="2021-01-20T18:15:14.590",
        ...     descriptions=[{"lang": "en", "value": "Prototype pollution..."}],
        ...     metrics={"cvssMetricV31": [...]},
        ...     weaknesses=[...],
        ...     references=[...]
        ... )
        >>> vuln = convert_nvd_to_vulnerability(nvd_cve)
        >>> vuln.id
        'CVE-2021-23337'
        >>> vuln.source
        <VulnerabilitySource.NVD: 'NVD'>
    """
    # Extract CVE ID
    cve_id = nvd_cve.id

    # Parse primary severity score (prioritize CVSS v3.1, then v3.0, then v2.0)
    severity = _extract_primary_severity(nvd_cve)

    # Parse additional severity scores
    additional_scores = _extract_additional_severities(nvd_cve)

    # Extract CWE IDs
    cwe_ids = _extract_cwe_ids(nvd_cve)

    # Parse description (use English description if available)
    description = None
    for desc in nvd_cve.descriptions:
        if desc.get("lang") == "en":
            description = desc.get("value")
            break

    # Use first 100 chars of description as summary
    summary = description[:100] + "..." if description and len(description) > 100 else description or cve_id

    # Parse references
    references = _extract_references(nvd_cve)

    # Parse timestamps
    published = _parse_timestamp(nvd_cve.published)
    modified = _parse_timestamp(nvd_cve.last_modified)

    # Create unified Vulnerability
    return Vulnerability(
        id=cve_id,
        source=VulnerabilitySource.NVD,
        summary=summary,
        description=description,
        aliases=[],  # NVD doesn't provide aliases
        affected_versions=[],  # NVD doesn't provide specific version ranges
        severity=severity,
        additional_scores=additional_scores,
        references=references,
        published=published,
        modified=modified,
        cwe_ids=cwe_ids,
        raw_data=None,
    )


def _extract_primary_severity(nvd_cve: NVDCVE) -> CVSSScore | None:
    """
    Extract primary CVSS score from NVD CVE.

    Prioritizes CVSS v3.1 over v3.0 over v2.0. Returns the highest
    scoring metric from the prioritized version.

    Args:
        nvd_cve: NVD CVE object

    Returns:
        CVSSScore object or None if no metrics found
    """
    if not nvd_cve.metrics:
        return None

    # Prioritize CVSS versions
    for metric_type in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
        if metric_type in nvd_cve.metrics:
            metrics_list = nvd_cve.metrics[metric_type]
            if metrics_list:
                # Sort by base score (highest first)
                def get_base_score(metric: NVDMetric) -> float:
                    return metric.cvss_data.get("baseScore", 0.0)

                metrics_list.sort(key=get_base_score, reverse=True)
                return _parse_nvd_metric(metrics_list[0], metric_type)

    return None


def _extract_additional_severities(nvd_cve: NVDCVE) -> list[CVSSScore]:
    """
    Extract additional CVSS scores from NVD CVE.

    Returns all severity scores except the primary one.

    Args:
        nvd_cve: NVD CVE object

    Returns:
        List of additional CVSSScore objects
    """
    if not nvd_cve.metrics:
        return []

    # Get primary severity
    primary = _extract_primary_severity(nvd_cve)

    # Parse all metrics
    all_scores = []
    for metric_type, metrics_list in nvd_cve.metrics.items():
        for metric in metrics_list:
            try:
                cvss = _parse_nvd_metric(metric, metric_type)
                if cvss and cvss != primary:
                    all_scores.append(cvss)
            except Exception as e:
                logger.warning(f"Failed to parse additional NVD metric: {e}")
                continue

    return all_scores


def _parse_nvd_metric(metric: NVDMetric, metric_type: str) -> CVSSScore | None:
    """
    Parse NVD metric to CVSSScore.

    Args:
        metric: NVDMetric object
        metric_type: Metric type (e.g., "cvssMetricV31")

    Returns:
        CVSSScore object or None if parsing fails
    """
    try:
        cvss_data = metric.cvss_data

        # Extract CVSS version
        version = cvss_data.get("version", "3.1")
        if version == "3.1":
            version_str = "3.1"
        elif version == "3.0":
            version_str = "3.0"
        elif version == "2.0":
            version_str = "2.0"
        else:
            version_str = "3.1"

        # Extract vector string
        vector_string = cvss_data.get("vectorString", "")

        # Extract base score
        base_score = float(cvss_data.get("baseScore", 0.0))

        # Extract base severity
        base_severity_str = cvss_data.get("baseSeverity", "")
        try:
            base_severity = Severity(base_severity_str.upper())
        except ValueError:
            # If not a valid severity enum, derive from score
            base_severity = Severity.from_score(base_score)

        # Extract exploitability and impact scores
        exploitability_score = metric.exploitability_score
        impact_score = metric.impact_score

        return CVSSScore(
            version=version_str,
            vector_string=vector_string,
            base_score=base_score,
            base_severity=base_severity,
            impact_score=impact_score,
            exploitability_score=exploitability_score,
        )

    except Exception as e:
        logger.warning(f"Failed to parse NVD metric: {e}")
        return None


def _extract_cwe_ids(nvd_cve: NVDCVE) -> list[str]:
    """
    Extract CWE IDs from NVD CVE weaknesses.

    Args:
        nvd_cve: NVD CVE object

    Returns:
        List of CWE IDs (e.g., ["CWE-79", "CWE-20"])
    """
    cwe_ids = []

    for weakness in nvd_cve.weaknesses:
        for desc in weakness.description:
            cwe_id = desc.get("value", "")
            if cwe_id and cwe_id.startswith("CWE-"):
                cwe_ids.append(cwe_id)

    return cwe_ids


def _extract_references(nvd_cve: NVDCVE) -> list[Reference]:
    """
    Extract reference URLs from NVD CVE.

    Args:
        nvd_cve: NVD CVE object

    Returns:
        List of Reference objects
    """
    references = []

    for ref in nvd_cve.references:
        # Determine reference type from tags
        ref_type = "WEB"
        if ref.tags:
            if "Patch" in ref.tags:
                ref_type = "FIX"
            elif "Advisory" in ref.tags:
                ref_type = "ADVISORY"

        references.append(Reference(
            url=ref.url,
            type=ref_type,
            source=ref.source or "NVD",
        ))

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
        # Try parsing with timezone
        if timestamp_str.endswith("Z"):
            timestamp_str = timestamp_str[:-1] + "+00:00"
        return datetime.fromisoformat(timestamp_str)
    except (ValueError, AttributeError) as e:
        logger.warning(f"Failed to parse timestamp '{timestamp_str}': {e}")
        return None


# ============================================================================
# NVD Scanner Implementation
# ============================================================================


class NVDScanner:
    """
    Scanner implementation for NVD (National Vulnerability Database).

    This class implements the Scanner interface, querying the NVD database
    for CVEs and converting results to the unified Vulnerability model.

    Note: NVD queries by CVE ID, not by package name/version. This scanner
    is most useful for validating CVEs found by other sources.

    Attributes:
        client: NVDClient instance for API queries

    Example:
        >>> scanner = NVDScanner()
        >>> vuln = scanner.query_by_cve_id("CVE-2021-23337")
        >>> vuln.id
        'CVE-2021-23337'
    """

    def __init__(
        self,
        client: NVDClient | None = None,
        api_key: str | None = None,
        timeout: int = 30,
        rate_limit: float | None = None,
        max_retries: int = 3,
    ):
        """
        Initialize NVD scanner.

        Args:
            client: Optional NVDClient instance. If None, creates new client.
            api_key: Optional NVD API key for higher rate limits
            timeout: Request timeout in seconds (default: 30)
            rate_limit: Maximum requests per second (default: auto-detected)
            max_retries: Maximum number of retry attempts (default: 3)

        Example:
            >>> scanner = NVDScanner(api_key="your-api-key")
            >>> scanner.get_source()
            <VulnerabilitySource.NVD: 'NVD'>
        """
        if client is None:
            self.client = NVDClient(
                api_key=api_key,
                timeout=timeout,
                rate_limit=rate_limit,
                max_retries=max_retries,
            )
        else:
            self.client = client

        logger.debug(f"NVDScanner initialized with api_key={'***' if self.client.api_key else 'none'}")

    def query_by_cve_id(self, cve_id: str) -> Vulnerability | None:
        """
        Query NVD for a specific CVE by ID.

        This is the primary method for NVD scanner since NVD queries
        by CVE ID rather than package name/version.

        Args:
            cve_id: CVE identifier (e.g., "CVE-2021-23337")

        Returns:
            Vulnerability object or None if CVE not found

        Raises:
            APIError: If the API request fails
            ValueError: If cve_id format is invalid

        Example:
            >>> scanner = NVDScanner()
            >>> vuln = scanner.query_by_cve_id("CVE-2021-23337")
            >>> vuln.id if vuln else None
            'CVE-2021-23337'
        """
        # Query NVD database
        nvd_response = self.client.query_cve(cve_id)

        # Check if CVE was found
        if not nvd_response.vulnerabilities:
            logger.debug(f"CVE {cve_id} not found in NVD")
            return None

        # Get first CVE from response
        cve_dict = nvd_response.vulnerabilities[0]
        nvd_cve = cve_dict.get("cve")

        if not nvd_cve:
            logger.warning(f"NVD response for {cve_id} missing CVE data")
            return None

        # Convert NVDCVE to unified Vulnerability
        try:
            vuln = convert_nvd_to_vulnerability(nvd_cve)
            logger.debug(f"NVDScanner retrieved CVE {cve_id}")
            return vuln
        except Exception as e:
            logger.warning(f"Failed to convert NVD CVE {cve_id} to unified format: {e}")
            return None

    def query_by_name_version(
        self, ecosystem: str, name: str, version: str
    ) -> list[Vulnerability]:
        """
        Query NVD for vulnerabilities by package name and version.

        Note: NVD does not support querying by package name/version directly.
        This method is provided for interface compatibility but will
        always return an empty list.

        Use query_by_cve_id() instead to query specific CVEs.

        Args:
            ecosystem: Package ecosystem (ignored for NVD)
            name: Package name (ignored for NVD)
            version: Package version (ignored for NVD)

        Returns:
            Empty list (NVD cannot query by package)

        Example:
            >>> scanner = NVDScanner()
            >>> vulns = scanner.query_by_name_version("npm", "lodash", "4.17.15")
            >>> len(vulns)
            0
        """
        logger.debug(
            f"NVDScanner.query_by_name_version called but NVD does not support "
            f"package queries. Use query_by_cve_id() instead."
        )
        return []

    def get_source(self) -> VulnerabilitySource:
        """
        Identify the vulnerability source for this scanner.

        Returns:
            VulnerabilitySource.NVD

        Example:
            >>> scanner = NVDScanner()
            >>> scanner.get_source()
            <VulnerabilitySource.NVD: 'NVD'>
        """
        return VulnerabilitySource.NVD

    def supports_batch_queries(self) -> bool:
        """
        Check if this scanner supports batch queries.

        NVD does not support batch queries in the traditional sense.
        Returns False.

        Returns:
            False (NVD does not support batch queries)

        Example:
            >>> scanner = NVDScanner()
            >>> scanner.supports_batch_queries()
            False
        """
        return False

    def query_batch(
        self, packages: list[PackageIdentifier]
    ) -> dict[PackageIdentifier, list[Vulnerability]]:
        """
        Query multiple packages in a single batch request.

        Note: NVD does not support batch queries. This method is provided
        for interface compatibility but will return empty results for all packages.

        Args:
            packages: List of PackageIdentifier objects

        Returns:
            Dictionary mapping each PackageIdentifier to an empty list

        Example:
            >>> scanner = NVDScanner()
            >>> packages = [PackageIdentifier("npm", "lodash", "4.17.15")]
            >>> results = scanner.query_batch(packages)
            >>> results[packages[0]]
            []
        """
        logger.debug("NVDScanner.query_batch called but NVD does not support batch queries")
        return {pkg: [] for pkg in packages}
