"""
NVD (National Vulnerability Database) Client Module

This module provides a client for interacting with the NIST National Vulnerability
Database (NVD) API v2.0. It includes NVD-specific endpoints for retrieving CVE
(CVE - Common Vulnerabilities and Exposures) data, vulnerability details, and
security metrics with appropriate rate limiting.

NVD API Documentation: https://nvd.nist.gov/developers/vulnerabilities
"""

from typing import Any, Dict, Optional, cast

from binary_sbom.clients.base import BaseHTTPClient, HTTPClientError


class NVDClientError(HTTPClientError):
    """Exception raised when an NVD client request fails."""

    pass


class NVDClient(BaseHTTPClient):
    """
    Client for the NIST National Vulnerability Database (NVD) API v2.0.

    This client provides methods for querying CVE data from the NVD API with
    built-in rate limiting to respect NVD's API usage policies. The NVD API
    rate limits are approximately 5 requests per 30 seconds for the public API,
    though limits may vary based on API key status.

    Attributes:
        base_url (str): NVD API v2.0 base URL.
        api_key (Optional[str]): NVD API key for increased rate limits (optional).
        timeout (int): Connection and read timeout in seconds.
        max_retries (int): Maximum number of retry attempts for failed requests.
        retry_backoff_factor (float): Multiplier for exponential backoff calculation.
        rate_limit_delay (float): Minimum delay between requests in seconds.
        user_agent (str): User-Agent header for HTTP requests.

    Args:
        api_key: NVD API key for increased rate limits (default: None).
        timeout: Connection and read timeout in seconds (default: 30).
        max_retries: Maximum number of retry attempts (default: 3).
        retry_backoff_factor: Exponential backoff multiplier (default: 0.5).
        rate_limit_delay: Minimum delay between requests in seconds (default: 6.0).
            NVD recommends approximately 6 seconds between requests without an API key.
        user_agent: User-Agent string for HTTP requests (default: "Binary-SBOM/0.1.0").

    Raises:
        ValueError: If timeout, max_retries, or rate_limit_delay are invalid.

    Example:
        >>> client = NVDClient()
        >>> cve_data = client.get_cve("CVE-2021-44228")
        >>> print(cve_data["id"])
        'CVE-2021-44228'

        >>> # With API key for higher rate limits
        >>> client = NVDClient(api_key="your-api-key-here", rate_limit_delay=1.0)
        >>> results = client.search_cves(keyword="apache")
    """

    # NVD API v2.0 base URL
    base_url: str = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        retry_backoff_factor: float = 0.5,
        rate_limit_delay: float = 6.0,
        user_agent: str = "Binary-SBOM/0.1.0",
    ) -> None:
        """
        Initialize the NVDClient with NVD-specific configuration.

        Args:
            api_key: NVD API key for increased rate limits (optional).
            timeout: Connection and read timeout in seconds.
            max_retries: Maximum number of retry attempts.
            retry_backoff_factor: Multiplier for exponential backoff calculation.
            rate_limit_delay: Minimum delay between requests in seconds.
                NVD recommends ~6 seconds without API key, ~1 second with API key.
            user_agent: User-Agent string for HTTP requests.
        """
        # Initialize base client
        super().__init__(
            timeout=timeout,
            max_retries=max_retries,
            retry_backoff_factor=retry_backoff_factor,
            rate_limit_delay=rate_limit_delay,
            user_agent=user_agent,
        )

        # Store API key and add to headers if provided
        self.api_key: Optional[str] = api_key
        if api_key:
            self.headers["apiKey"] = api_key

    def get_cve(self, cve_id: str) -> Dict[str, Any]:
        """
        Retrieve details for a specific CVE by ID.

        Fetches comprehensive vulnerability information including CVSS scores,
        affected products, references, and descriptions for a single CVE.

        Args:
            cve_id: CVE identifier (e.g., "CVE-2021-44228").

        Returns:
            Dictionary containing CVE vulnerability data. Structure includes:
                - id: CVE identifier
                - sourceIdentifier: Source of the CVE data
                - published: Published date
                - lastModified: Last modified date
                - vulnStatus: Vulnerability status
                - descriptions: List of descriptions
                - metrics: CVSS scores and impact metrics
                - references: List of reference links
                - configurations: Affected product configurations

        Raises:
            ValueError: If cve_id is empty or invalid format.
            HTTPClientError: If the request fails.
            NVDClientError: If CVE is not found or data is invalid.

        Example:
            >>> client = NVDClient()
            >>> cve = client.get_cve("CVE-2021-44228")
            >>> print(cve["id"])
            'CVE-2021-44228'
        """
        # Validate CVE ID format
        if not cve_id:
            raise ValueError(
                "CVE ID cannot be empty. "
                "Provide a valid CVE identifier (e.g., 'CVE-2021-44228')."
            )

        cve_id = cve_id.strip().upper()
        if not cve_id.startswith("CVE-"):
            raise ValueError(
                f"Invalid CVE ID format: {cve_id}. "
                "CVE ID must start with 'CVE-' (e.g., 'CVE-2021-44228')."
            )

        # Make request to NVD API
        try:
            response = self.get("", params={"cveId": cve_id})

            # Parse JSON response
            import json

            data: Dict[str, Any] = cast(Dict[str, Any], json.loads(response))

            # Check if CVE was found
            if "totalResults" in data and data["totalResults"] == 0:
                raise NVDClientError(
                    f"CVE {cve_id} not found in NVD database. "
                    "Verify the CVE ID and try again."
                )

            # Extract CVE data from response
            if "vulnerabilities" not in data or not data["vulnerabilities"]:
                raise NVDClientError(
                    f"Invalid response format for CVE {cve_id}. "
                    "Expected 'vulnerabilities' field in response."
                )

            # Return the first (and should be only) CVE
            return cast(Dict[str, Any], data["vulnerabilities"][0]["cve"])

        except json.JSONDecodeError as e:
            raise NVDClientError(
                f"Failed to parse JSON response for CVE {cve_id}: {e}"
            ) from e
        except (KeyError, IndexError) as e:
            raise NVDClientError(
                f"Unexpected response structure for CVE {cve_id}: {e}"
            ) from e

    def search_cves(
        self,
        keyword: Optional[str] = None,
        cpe_name: Optional[str] = None,
        cvss_severity: Optional[str] = None,
        is_vulnerable: bool = True,
        results_per_page: int = 20,
        start_index: int = 0,
    ) -> Dict[str, Any]:
        """
        Search for CVEs matching specific criteria.

        Queries the NVD database for CVEs based on various filters including
        keywords, CPE names, CVSS severity, and more.

        Args:
            keyword: Keyword search string (optional).
            cpe_name: CPE (Common Platform Enumeration) identifier (optional).
            cvss_severity: CVSS severity filter (optional).
                Valid values: "LOW", "MEDIUM", "HIGH", "CRITICAL".
            is_vulnerable: Filter for vulnerable configurations (default: True).
            results_per_page: Number of results per page (default: 20, max: 2000).
            start_index: Starting index for pagination (default: 0).

        Returns:
            Dictionary containing search results with the following structure:
                - totalResults: Total number of matching CVEs
                - startIndex: Starting index of current page
                - resultsPerPage: Number of results per page
                - vulnerabilities: List of CVE entries

        Raises:
            ValueError: If parameters are invalid.
            HTTPClientError: If the request fails.
            NVDClientError: If the search fails or returns invalid data.

        Example:
            >>> client = NVDClient()
            >>> results = client.search_cves(keyword="log4j", results_per_page=10)
            >>> print(f"Found {results['totalResults']} CVEs")
            Found 42 CVEs
        """
        # Validate results_per_page
        if results_per_page < 1 or results_per_page > 2000:
            raise ValueError(
                f"results_per_page must be between 1 and 2000, got {results_per_page}. "
                "NVD API maximum is 2000 results per page."
            )

        # Validate start_index
        if start_index < 0:
            raise ValueError(
                f"start_index must be non-negative, got {start_index}. "
                "Use 0 for the first page of results."
            )

        # Validate cvss_severity if provided
        valid_severities = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        if cvss_severity and cvss_severity.upper() not in valid_severities:
            raise ValueError(
                f"Invalid CVSS severity: {cvss_severity}. "
                f"Valid values: {', '.join(valid_severities)}."
            )

        # Build query parameters
        params: Dict[str, Any] = {
            "resultsPerPage": results_per_page,
            "startIndex": start_index,
        }

        # Add optional filters
        if keyword:
            params["keyword"] = keyword

        if cpe_name:
            params["cpeName"] = cpe_name

        if cvss_severity:
            params["cvssSeverity"] = cvss_severity.upper()

        if is_vulnerable:
            params["isVulnerable"] = str(is_vulnerable).lower()

        # Make request to NVD API
        try:
            response = self.get("", params=params)

            # Parse JSON response
            import json

            data: Dict[str, Any] = cast(Dict[str, Any], json.loads(response))

            # Validate response structure
            if "vulnerabilities" not in data:
                raise NVDClientError(
                    "Invalid response format from NVD API. "
                    "Expected 'vulnerabilities' field in search results."
                )

            return data

        except json.JSONDecodeError as e:
            raise NVDClientError(f"Failed to parse JSON response: {e}") from e

    def get_cves_by_cpe(
        self,
        cpe_name: str,
        results_per_page: int = 20,
        start_index: int = 0,
    ) -> Dict[str, Any]:
        """
        Retrieve all CVEs for a specific CPE (Common Platform Enumeration).

        Queries for vulnerabilities affecting a specific product or platform
        identified by its CPE identifier.

        Args:
            cpe_name: CPE identifier (e.g., "cpe:2.3:a:apache:log4j:2.14.1:*:*:*:*:*:*:*").
            results_per_page: Number of results per page (default: 20, max: 2000).
            start_index: Starting index for pagination (default: 0).

        Returns:
            Dictionary containing CVE entries for the specified CPE.

        Raises:
            ValueError: If cpe_name is empty or parameters are invalid.
            HTTPClientError: If the request fails.
            NVDClientError: If the search fails or returns invalid data.

        Example:
            >>> client = NVDClient()
            >>> cves = client.get_cves_by_cpe(
            ...     "cpe:2.3:a:apache:log4j:2.14.1:*:*:*:*:*:*:*"
            ... )
            >>> print(f"Found {cves['totalResults']} CVEs for this CPE")
        """
        # Validate CPE name
        if not cpe_name:
            raise ValueError(
                "CPE name cannot be empty. "
                "Provide a valid CPE identifier (e.g., 'cpe:2.3:a:vendor:product:version:*:*:*:*:*:*:*')."
            )

        return self.search_cves(
            cpe_name=cpe_name,
            results_per_page=results_per_page,
            start_index=start_index,
        )

    def get_cves_by_severity(
        self,
        severity: str,
        keyword: Optional[str] = None,
        results_per_page: int = 20,
        start_index: int = 0,
    ) -> Dict[str, Any]:
        """
        Retrieve CVEs filtered by CVSS severity level.

        Queries for vulnerabilities with a specific severity rating.

        Args:
            severity: CVSS severity level ("LOW", "MEDIUM", "HIGH", or "CRITICAL").
            keyword: Optional keyword search filter.
            results_per_page: Number of results per page (default: 20, max: 2000).
            start_index: Starting index for pagination (default: 0).

        Returns:
            Dictionary containing CVE entries matching the severity level.

        Raises:
            ValueError: If severity is invalid or parameters are invalid.
            HTTPClientError: If the request fails.
            NVDClientError: If the search fails or returns invalid data.

        Example:
            >>> client = NVDClient()
            >>> critical_cves = client.get_cves_by_severity("CRITICAL", keyword="apache")
            >>> print(f"Found {critical_cves['totalResults']} critical CVEs")
        """
        # Validate severity
        severity = severity.upper()
        valid_severities = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        if severity not in valid_severities:
            raise ValueError(
                f"Invalid severity: {severity}. "
                f"Valid values: {', '.join(valid_severities)}."
            )

        return self.search_cves(
            keyword=keyword,
            cvss_severity=severity,
            results_per_page=results_per_page,
            start_index=start_index,
        )


__all__ = [
    "NVDClient",
    "NVDClientError",
]
