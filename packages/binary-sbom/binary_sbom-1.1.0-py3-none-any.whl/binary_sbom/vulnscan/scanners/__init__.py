"""
Vulnerability scanner implementations.

This package provides scanner implementations that coordinate with
multiple vulnerability databases to find known CVEs for packages.

Classes:
    Scanner: Abstract interface for vulnerability scanners
    VulnScanner: Main scanner coordinating multiple data sources

Example:
    >>> from binary_sbom.vulnscan.scanners import VulnScanner
    >>> scanner = VulnScanner()
    >>> result = scanner.scan_package("npm", "lodash", "4.17.15")
"""

from binary_sbom.vulnscan.scanners.scanner import Scanner, VulnScanner

__all__ = [
    "Scanner",
    "VulnScanner",
]
