"""
Vulnerability database API clients.

This package provides clients for querying various vulnerability databases:
- OSV (Open Source Vulnerabilities) - Primary data source
- NVD (National Vulnerability Database) - CVE validation
- GitHub Security Advisories - GitHub-specific vulnerabilities

Includes scanner implementations that convert database-specific responses
to the unified Vulnerability model.

Example:
    >>> from binary_sbom.vulnscan.clients import OSVClient, OSVScanner
    >>> client = OSVClient()
    >>> vulns = client.query_package("npm", "lodash", "4.17.15")
    >>> scanner = OSVScanner()
    >>> vulns = scanner.query_by_name_version("npm", "lodash", "4.17.15")
"""

from binary_sbom.vulnscan.clients.github import (
    GitHubClient,
    GitHubScanner,
    convert_github_to_vulnerability,
)
from binary_sbom.vulnscan.clients.nvd import NVDClient, NVDScanner, convert_nvd_to_vulnerability
from binary_sbom.vulnscan.clients.osv import OSVClient, OSVScanner, convert_osv_to_vulnerability

__all__ = [
    "OSVClient",
    "OSVScanner",
    "convert_osv_to_vulnerability",
    "NVDClient",
    "NVDScanner",
    "convert_nvd_to_vulnerability",
    "GitHubClient",
    "GitHubScanner",
    "convert_github_to_vulnerability",
]
