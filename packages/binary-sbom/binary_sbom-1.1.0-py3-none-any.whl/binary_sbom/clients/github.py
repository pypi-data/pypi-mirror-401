"""
GitHub Client Module

This module provides a client for interacting with the GitHub API, specifically
for fetching security advisory data. GitHub provides comprehensive vulnerability
data for open source projects through the Security Advisory API.

GitHub API Documentation: https://docs.github.com/en/rest/security-advisories
"""

from typing import Any, Dict, Optional, cast

from binary_sbom.clients.base import BaseHTTPClient, HTTPClientError


class GitHubClientError(HTTPClientError):
    """Exception raised when a GitHub client request fails."""

    pass


class GitHubClient(BaseHTTPClient):
    """
    Client for the GitHub API with a focus on security advisories.

    This client provides methods for querying security advisory data from GitHub,
    which includes vulnerability information for open source projects. GitHub
    Security Advisories include CVE data, GHSA IDs, affected packages, and
    severity information.

    Attributes:
        base_url (str): GitHub API base URL.
        token (Optional[str]): GitHub personal access token for authentication (optional).
        timeout (int): Connection and read timeout in seconds.
        max_retries (int): Maximum number of retry attempts for failed requests.
        retry_backoff_factor (float): Multiplier for exponential backoff calculation.
        rate_limit_delay (float): Minimum delay between requests in seconds.
        user_agent (str): User-Agent header for HTTP requests.

    Args:
        token: GitHub personal access token for authenticated requests (default: None).
            Authenticated requests have higher rate limits (5000/hour vs 60/hour).
        timeout: Connection and read timeout in seconds (default: 30).
        max_retries: Maximum number of retry attempts (default: 3).
        retry_backoff_factor: Exponential backoff multiplier (default: 0.5).
        rate_limit_delay: Minimum delay between requests in seconds (default: 0.1).
        user_agent: User-Agent string for HTTP requests (default: "Binary-SBOM/0.1.0").

    Raises:
        ValueError: If timeout, max_retries, or rate_limit_delay are invalid.

    Example:
        >>> client = GitHubClient()
        >>> advisory = client.get_advisory("GHSA-abc1-2345-6789")
        >>> print(advisory["ghsa_id"])
        'GHSA-abc1-2345-6789'

        >>> # With authentication token for higher rate limits
        >>> client = GitHubClient(token="your-token-here")
        >>> advisories = client.query_advisories(package="log4j")
    """

    # GitHub API base URL
    base_url: str = "https://api.github.com"

    def __init__(
        self,
        token: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        retry_backoff_factor: float = 0.5,
        rate_limit_delay: float = 0.1,
        user_agent: str = "Binary-SBOM/0.1.0",
    ) -> None:
        """
        Initialize the GitHubClient with GitHub-specific configuration.

        Args:
            token: GitHub personal access token for authenticated requests (optional).
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

        # Store token and add to headers if provided
        self.token: Optional[str] = token
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def get_advisory(
        self, advisory_id: str, ecosystem: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieve details for a specific security advisory by ID.

        Fetches comprehensive vulnerability information including severity scores,
        affected packages, references, and aliases for a single GitHub Security
        Advisory (GHSA) or CVE.

        Args:
            advisory_id: Advisory identifier (e.g., "GHSA-abc1-2345-6789", "CVE-2021-44228").
            ecosystem: Ecosystem filter for CVE queries (optional).
                For CVE IDs, you may need to specify the ecosystem (e.g., "npm", "maven").

        Returns:
            Dictionary containing advisory data with structure:
                - ghsa_id: GitHub Security Advisory ID
                - summary: Brief description
                - description: Detailed description
                - severity: Severity score
                - cvse: CVSS score and vector string
                - vulnerabilities: List of affected package versions
                - references: List of reference links
                - identifiers: Alternative IDs (CVE, etc.)
                - published_at: Publication timestamp
                - updated_at: Last update timestamp
                - withdrawn_at: Withdrawal timestamp (if withdrawn)

        Raises:
            ValueError: If advisory_id is empty.
            HTTPClientError: If the request fails.
            GitHubClientError: If advisory is not found or data is invalid.

        Example:
            >>> client = GitHubClient()
            >>> advisory = client.get_advisory("GHSA-abc1-2345-6789")
            >>> print(advisory["ghsa_id"])
            'GHSA-abc1-2345-6789'
        """
        # Validate advisory ID
        if not advisory_id:
            raise ValueError(
                "Advisory ID cannot be empty. "
                "Provide a valid GHSA ID (e.g., 'GHSA-abc1-2345-6789') "
                "or CVE ID (e.g., 'CVE-2021-44228')."
            )

        advisory_id = advisory_id.strip()

        # Build endpoint path based on advisory type
        if advisory_id.upper().startswith("GHSA-"):
            # GitHub Security Advisory
            endpoint = f"/advisories/{advisory_id}"
        elif advisory_id.upper().startswith("CVE-"):
            # CVE - query through GitHub's CVE endpoint
            # GitHub advisories can be looked up by CVE, but may need ecosystem
            params: Dict[str, Any] = {}
            if ecosystem:
                params["ecosystem"] = ecosystem
            endpoint = f"/advisories"
            # For CVEs, we need to use query instead of direct lookup
            return self.query_advisories(cve=advisory_id, ecosystem=ecosystem)
        else:
            raise ValueError(
                f"Invalid advisory ID format: {advisory_id}. "
                "Advisory ID must start with 'GHSA-' or 'CVE-' "
                "(e.g., 'GHSA-abc1-2345-6789', 'CVE-2021-44228')."
            )

        # Make request to GitHub API
        try:
            response = self.get(endpoint)

            # Parse JSON response
            import json

            data: Dict[str, Any] = cast(Dict[str, Any], json.loads(response))

            return data

        except json.JSONDecodeError as e:
            raise GitHubClientError(
                f"Failed to parse JSON response for advisory {advisory_id}: {e}"
            ) from e

    def query_advisories(
        self,
        package: Optional[str] = None,
        ecosystem: Optional[str] = None,
        cve: Optional[str] = None,
        severity: Optional[str] = None,
        is_withdrawn: bool = False,
        per_page: int = 20,
        since: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Query for security advisories matching specific criteria.

        Queries the GitHub Security Advisory database for advisories based on
        package information, CVE ID, severity, and other filters.

        Args:
            package: Package name to filter by (optional).
            ecosystem: Ecosystem name (optional).
                Common values: "npm", "maven", "pip", "rubygems", "go", "nuget".
            cve: CVE ID to filter by (optional).
            severity: Severity level filter (optional).
                Valid values: "low", "medium", "high", "critical".
            is_withdrawn: Include withdrawn advisories (default: False).
            per_page: Number of results per page (default: 20, max: 100).
            since: ISO 8601 timestamp to filter advisories updated after this time (optional).

        Returns:
            Dictionary containing query results with structure:
                - advisories: List of matching advisory entries

        Raises:
            ValueError: If parameters are invalid.
            HTTPClientError: If the request fails.
            GitHubClientError: If the query fails or returns invalid data.

        Example:
            >>> client = GitHubClient()
            >>> results = client.query_advisories(package="log4j", ecosystem="maven")
            >>> print(f"Found {len(results['advisories'])} advisories")
        """
        # Validate per_page
        if per_page < 1 or per_page > 100:
            raise ValueError(
                f"per_page must be between 1 and 100, got {per_page}. "
                "GitHub API maximum is 100 results per page."
            )

        # Validate severity if provided
        if severity:
            valid_severities = ["low", "medium", "high", "critical"]
            severity_lower = severity.lower()
            if severity_lower not in valid_severities:
                raise ValueError(
                    f"Invalid severity: {severity}. "
                    f"Valid values: {', '.join(valid_severities)}."
                )

        # Build query parameters
        params: Dict[str, Any] = {"per_page": per_page, "state": "active"}

        # If we want withdrawn advisories, we need to adjust state
        if is_withdrawn:
            params["state"] = "all"

        # Add optional filters
        if package:
            params["package"] = package

        if ecosystem:
            params["ecosystem"] = ecosystem

        if cve:
            params["cve_id"] = cve.strip().upper()

        if severity:
            params["severity"] = severity_lower

        if since:
            params["since"] = since

        # Make request to GitHub API
        try:
            response = self.get("/advisories", params=params)

            # Parse JSON response
            import json

            data = json.loads(response)

            # GitHub returns an array directly, not wrapped in an object
            if isinstance(data, list):
                return {"advisories": data}
            elif isinstance(data, dict) and "advisories" in data:
                return data
            else:
                # Unexpected format
                return {"advisories": data if isinstance(data, list) else [data]}

        except json.JSONDecodeError as e:
            raise GitHubClientError(
                f"Failed to parse JSON response: {e}"
            ) from e

    def query_by_package(
        self, package_name: str, ecosystem: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Query for security advisories affecting a specific package.

        Queries for advisories that affect the specified package in a given
        ecosystem.

        Args:
            package_name: Name of the package.
            ecosystem: Ecosystem name (e.g., "npm", "maven", "pip", "rubygems", "go").

        Returns:
            Dictionary containing advisory entries affecting the package.

        Raises:
            ValueError: If package_name is empty.
            HTTPClientError: If the request fails.
            GitHubClientError: If the query fails or returns invalid data.

        Example:
            >>> client = GitHubClient()
            >>> results = client.query_by_package("log4j", ecosystem="maven")
            >>> print(f"Found {len(results['advisories'])} advisories")
        """
        # Validate package name
        if not package_name:
            raise ValueError(
                "Package name cannot be empty. "
                "Provide a valid package name."
            )

        return self.query_advisories(
            package=package_name.strip(), ecosystem=ecosystem
        )

    def query_by_cve(self, cve_id: str, ecosystem: Optional[str] = None) -> Dict[str, Any]:
        """
        Query for security advisories by CVE identifier.

        Queries for advisories associated with a specific CVE ID.

        Args:
            cve_id: CVE identifier (e.g., "CVE-2021-44228").
            ecosystem: Ecosystem filter (optional, recommended for CVEs).

        Returns:
            Dictionary containing advisory entries for the CVE.

        Raises:
            ValueError: If cve_id is empty or invalid format.
            HTTPClientError: If the request fails.
            GitHubClientError: If the query fails or returns invalid data.

        Example:
            >>> client = GitHubClient()
            >>> results = client.query_by_cve("CVE-2021-44228", ecosystem="maven")
            >>> print(f"Found {len(results['advisories'])} advisories")
        """
        # Validate CVE ID
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

        return self.query_advisories(cve=cve_id, ecosystem=ecosystem)


__all__ = [
    "GitHubClient",
    "GitHubClientError",
]
