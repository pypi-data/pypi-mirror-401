"""
OSV (Open Source Vulnerabilities) Client Module

This module provides a client for interacting with the OSV API. OSV is a
vulnerability triage infrastructure for open source projects that provides
a unified API for querying vulnerabilities across multiple ecosystems.

OSV API Documentation: https://osv.dev/docs/
"""

from typing import Any, Dict, Optional, cast

from binary_sbom.clients.base import BaseHTTPClient, HTTPClientError


class OSVClientError(HTTPClientError):
    """Exception raised when an OSV client request fails."""

    pass


class OSVClient(BaseHTTPClient):
    """
    Client for the Open Source Vulnerabilities (OSV) API.

    This client provides methods for querying vulnerability data from the OSV
    database, which aggregates vulnerability information from multiple sources
    and ecosystems. OSV provides a unified API for querying vulnerabilities by
    package, commit hash, or version ranges.

    Attributes:
        base_url (str): OSV API base URL.
        timeout (int): Connection and read timeout in seconds.
        max_retries (int): Maximum number of retry attempts for failed requests.
        retry_backoff_factor (float): Multiplier for exponential backoff calculation.
        rate_limit_delay (float): Minimum delay between requests in seconds.
        user_agent (str): User-Agent header for HTTP requests.

    Args:
        timeout: Connection and read timeout in seconds (default: 30).
        max_retries: Maximum number of retry attempts (default: 3).
        retry_backoff_factor: Exponential backoff multiplier (default: 0.5).
        rate_limit_delay: Minimum delay between requests in seconds (default: 0.1).
            OSV has generous rate limits, but default is conservative.
        user_agent: User-Agent string for HTTP requests (default: "Binary-SBOM/0.1.0").

    Raises:
        ValueError: If timeout, max_retries, or rate_limit_delay are invalid.

    Example:
        >>> client = OSVClient()
        >>> vulns = client.query_vulnerabilities(
        ...     package={"name": "log4j", "ecosystem": "Maven"}
        ... )
        >>> print(f"Found {len(vulns)} vulnerabilities")

        >>> # Query by commit hash
        >>> results = client.query_by_commit("abc123def456")
    """

    # OSV API base URL
    base_url: str = "https://api.osv.dev/v1"

    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 3,
        retry_backoff_factor: float = 0.5,
        rate_limit_delay: float = 0.1,
        user_agent: str = "Binary-SBOM/0.1.0",
    ) -> None:
        """
        Initialize the OSVClient with OSV-specific configuration.

        Args:
            timeout: Connection and read timeout in seconds.
            max_retries: Maximum number of retry attempts.
            retry_backoff_factor: Multiplier for exponential backoff calculation.
            rate_limit_delay: Minimum delay between requests in seconds.
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

    def get_vulnerability(self, vuln_id: str) -> Dict[str, Any]:
        """
        Retrieve details for a specific vulnerability by OSV ID.

        Fetches comprehensive vulnerability information including affected versions,
        severity scores, references, and aliases for a single vulnerability.

        Args:
            vuln_id: OSV vulnerability ID (e.g., "OSV-2021-1234", "CVE-2021-44228").

        Returns:
            Dictionary containing vulnerability data with structure:
                - id: Vulnerability ID
                - summary: Brief description
                - details: Detailed description
                - affected: List of affected package versions
                - severity: Severity scores
                - references: List of reference links
                - aliases: Alternative IDs (CVE, GHSA, etc.)

        Raises:
            ValueError: If vuln_id is empty.
            HTTPClientError: If the request fails.
            OSVClientError: If vulnerability is not found or data is invalid.

        Example:
            >>> client = OSVClient()
            >>> vuln = client.get_vulnerability("OSV-2021-1234")
            >>> print(vuln["id"])
            'OSV-2021-1234'
        """
        # Validate vulnerability ID
        if not vuln_id:
            raise ValueError(
                "Vulnerability ID cannot be empty. "
                "Provide a valid OSV ID (e.g., 'OSV-2021-1234') or CVE ID."
            )

        vuln_id = vuln_id.strip()

        # Make request to OSV API
        try:
            response = self.get(f"/vulns/{vuln_id}")

            # Parse JSON response
            import json

            data: Dict[str, Any] = cast(Dict[str, Any], json.loads(response))

            return data

        except json.JSONDecodeError as e:
            raise OSVClientError(
                f"Failed to parse JSON response for vulnerability {vuln_id}: {e}"
            ) from e

    def query_vulnerabilities(
        self,
        package: Optional[Dict[str, str]] = None,
        commit: Optional[str] = None,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Query for vulnerabilities matching specific criteria.

        Queries the OSV database for vulnerabilities based on package information,
        commit hash, or specific version. At least one query parameter must be
        provided.

        Args:
            package: Package information dictionary containing:
                - name: Package name (required)
                - ecosystem: Ecosystem name (optional, e.g., "PyPI", "Maven", "npm")
                - purl: Package URL (optional, alternative to name+ecosystem)
            commit: Git commit hash to query (optional).
            version: Specific version to query (optional, requires package parameter).

        Returns:
            Dictionary containing query results with structure:
                - vulns: List of matching vulnerability entries
                - total: Total count of vulnerabilities (if available)

        Raises:
            ValueError: If no query parameters are provided or parameters are invalid.
            HTTPClientError: If the request fails.
            OSVClientError: If the query fails or returns invalid data.

        Example:
            >>> client = OSVClient()
            >>> results = client.query_vulnerabilities(
            ...     package={"name": "log4j", "ecosystem": "Maven"}
            ... )
            >>> print(f"Found {len(results['vulns'])} vulnerabilities")
        """
        # Validate at least one query parameter is provided
        if not any([package, commit, version]):
            raise ValueError(
                "At least one query parameter must be provided. "
                "Specify package, commit, or version."
            )

        # Build query payload
        query_payload: Dict[str, Any] = {}

        if package:
            query_payload["package"] = package

        if commit:
            query_payload["commit"] = commit

        if version:
            if not package:
                raise ValueError(
                    "Version parameter requires package parameter. "
                    "Provide package information along with version."
                )
            query_payload["version"] = version

        # Make POST request to OSV API
        try:
            response = self.post("/query", data=query_payload)

            # Parse JSON response
            import json

            data: Dict[str, Any] = cast(Dict[str, Any], json.loads(response))

            return data

        except json.JSONDecodeError as e:
            raise OSVClientError(f"Failed to parse JSON response: {e}") from e

    def query_by_commit(self, commit: str) -> Dict[str, Any]:
        """
        Query for vulnerabilities affecting a specific git commit.

        Queries for vulnerabilities that affect the specific commit hash,
        useful for determining if a particular code change introduces any
        known vulnerabilities.

        Args:
            commit: Git commit hash (short or full form).

        Returns:
            Dictionary containing vulnerability entries affecting the commit.

        Raises:
            ValueError: If commit is empty.
            HTTPClientError: If the request fails.
            OSVClientError: If the query fails or returns invalid data.

        Example:
            >>> client = OSVClient()
            >>> results = client.query_by_commit("abc123def456")
            >>> print(f"Found {len(results['vulns'])} vulnerabilities for commit")
        """
        # Validate commit
        if not commit:
            raise ValueError(
                "Commit hash cannot be empty. "
                "Provide a valid git commit hash."
            )

        return self.query_vulnerabilities(commit=commit.strip())

    def query_by_package(
        self,
        package_name: str,
        ecosystem: Optional[str] = None,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Query for vulnerabilities affecting a specific package.

        Queries for vulnerabilities that affect the specified package,
        optionally filtered by version.

        Args:
            package_name: Name of the package.
            ecosystem: Ecosystem name (e.g., "PyPI", "Maven", "npm", "Go").
                If not provided, some ecosystems may still work based on package name.
            version: Specific version to query (optional).

        Returns:
            Dictionary containing vulnerability entries affecting the package.

        Raises:
            ValueError: If package_name is empty.
            HTTPClientError: If the request fails.
            OSVClientError: If the query fails or returns invalid data.

        Example:
            >>> client = OSVClient()
            >>> results = client.query_by_package("log4j", ecosystem="Maven")
            >>> print(f"Found {len(results['vulns'])} vulnerabilities")
        """
        # Validate package name
        if not package_name:
            raise ValueError(
                "Package name cannot be empty. "
                "Provide a valid package name."
            )

        # Build package dictionary
        package_info: Dict[str, str] = {"name": package_name.strip()}

        if ecosystem:
            package_info["ecosystem"] = ecosystem.strip()

        return self.query_vulnerabilities(package=package_info, version=version)

    def query_batch(self, queries: list[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Query for vulnerabilities using batch requests.

        Performs multiple queries in a single API call for efficiency.

        Args:
            queries: List of query dictionaries, each following the same structure
                as query_vulnerabilities parameters.

        Returns:
            Dictionary containing batch results with structure:
                - results: List of query results in the same order as input queries

        Raises:
            ValueError: If queries list is empty or invalid.
            HTTPClientError: If the request fails.
            OSVClientError: If the batch query fails or returns invalid data.

        Example:
            >>> client = OSVClient()
            >>> queries = [
            ...     {"package": {"name": "log4j", "ecosystem": "Maven"}},
            ...     {"commit": "abc123def456"}
            ... ]
            >>> results = client.query_batch(queries)
        """
        # Validate queries
        if not queries:
            raise ValueError(
                "Queries list cannot be empty. "
                "Provide at least one query to execute."
            )

        if not isinstance(queries, list):
            raise ValueError(
                f"Queries must be a list, got {type(queries).__name__}. "
                "Provide a list of query dictionaries."
            )

        # Build batch payload
        batch_payload = {"queries": queries}

        # Make POST request to OSV batch endpoint
        try:
            response = self.post("/batch", data=batch_payload)

            # Parse JSON response
            import json

            data: Dict[str, Any] = cast(Dict[str, Any], json.loads(response))

            return data

        except json.JSONDecodeError as e:
            raise OSVClientError(f"Failed to parse JSON batch response: {e}") from e


__all__ = [
    "OSVClient",
    "OSVClientError",
]
