"""
HTTP Clients Package

A collection of HTTP client implementations for external service integrations.
Provides a base HTTP client with common functionality for authentication,
error handling, and request/response processing.
"""

__version__ = "0.1.0"
__author__ = "Binary SBOM Generator Contributors"
__license__ = "MIT"

from binary_sbom.clients.base import BaseHTTPClient, HTTPClientError
from binary_sbom.clients.github import GitHubClient, GitHubClientError
from binary_sbom.clients.nvd import NVDClient, NVDClientError
from binary_sbom.clients.osv import OSVClient, OSVClientError

__all__ = [
    "__version__",
    "BaseHTTPClient",
    "HTTPClientError",
    "NVDClient",
    "NVDClientError",
    "OSVClient",
    "OSVClientError",
    "GitHubClient",
    "GitHubClientError",
]
