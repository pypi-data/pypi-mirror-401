"""
Utility functions and helpers for vulnerability scanning.

This package provides utilities for:
- HTTP client with retry logic
- Rate limiting
- Caching
- Cancellation support for long-running operations
- Ecosystem name normalization and mapping
- Version matching and parsing

Example:
    >>> from binary_sbom.vulnscan.utils import HttpClient, RateLimiter, RateLimiterManager
    >>> from binary_sbom.vulnscan.utils.ecosystem import normalize_ecosystem, to_github_ecosystem
    >>> client = HttpClient(retry_max=3, timeout=30)
    >>> rate_limiter = RateLimiter(requests_per_second=10)
    >>> manager = RateLimiterManager()
    >>> manager.register("OSV", requests_per_second=10)
    >>> normalize_ecosystem("NPM")
    'npm'
    >>> to_github_ecosystem("PyPI")
    'PIP'
"""

from binary_sbom.vulnscan.utils.http_client import HttpClient
from binary_sbom.vulnscan.utils.rate_limiter import RateLimiter, RateLimiterManager
from binary_sbom.vulnscan.utils.cache import VulnerabilityCache
from binary_sbom.vulnscan.utils.cancellation import (
    CancellationContext,
    with_timeout,
    check_cancellation,
)
from binary_sbom.vulnscan.utils.ecosystem import (
    normalize_ecosystem,
    to_github_ecosystem,
    from_github_ecosystem,
    is_supported_by_github,
    is_supported_by_osv,
)

__all__ = [
    "HttpClient",
    "RateLimiter",
    "RateLimiterManager",
    "VulnerabilityCache",
    "CancellationContext",
    "with_timeout",
    "check_cancellation",
    "normalize_ecosystem",
    "to_github_ecosystem",
    "from_github_ecosystem",
    "is_supported_by_github",
    "is_supported_by_osv",
]
