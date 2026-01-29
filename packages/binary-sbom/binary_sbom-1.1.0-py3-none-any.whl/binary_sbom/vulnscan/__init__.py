"""
Vulnerability scanning package for Binary SBOM Generator.

This package provides vulnerability scanning capabilities by integrating
with multiple vulnerability databases (OSV, NVD, GitHub Advisories).

Modules:
    types: Core data types and models for vulnerability findings
    exceptions: Exception classes for vulnerability scanning errors
    clients: API clients for OSV, NVD, and GitHub databases
    scanners: Vulnerability scanner implementations
    aggregation: Deduplication and summarization utilities
    config: Configuration management
    utils: HTTP client, rate limiter, caching, and cancellation utilities
"""

from binary_sbom.vulnscan.types import (
    AffectedVersion,
    CVSSScore,
    GitHubAdvisory,
    GitHubCVSS,
    GitHubIdentifiers,
    GitHubPackage,
    GitHubVulnerability,
    NVDReference,
    NVDResponse,
    NVDCVE,
    NVDCVSSData,
    NVDMetric,
    NVDWeakness,
    OSVAffected,
    OSVEvent,
    OSVPackage,
    OSVQueryResponse,
    OSVRange,
    OSVSeverity,
    OSVVuln,
    PackageIdentifier,
    Reference,
    ScanResult,
    Severity,
    Vulnerability,
    VulnerabilityMatch,
    VulnerabilitySource,
)

from binary_sbom.vulnscan.exceptions import (
    VulnerabilityScanError,
    APIError,
    RateLimitError,
    AuthenticationError,
    PackageNotFoundError,
    InvalidVersionError,
    ConfigurationError,
    CacheError,
    TimeoutError,
    CancellationError,
)

__all__ = [
    # Core types
    "PackageIdentifier",
    "Severity",
    "VulnerabilitySource",
    "CVSSScore",
    "AffectedVersion",
    "Reference",
    "Vulnerability",
    "VulnerabilityMatch",
    "ScanResult",
    # OSV types
    "OSVSeverity",
    "OSVPackage",
    "OSVEvent",
    "OSVRange",
    "OSVAffected",
    "OSVVuln",
    "OSVQueryResponse",
    # NVD types
    "NVDCVSSData",
    "NVDMetric",
    "NVDReference",
    "NVDWeakness",
    "NVDCVE",
    "NVDResponse",
    # GitHub types
    "GitHubIdentifiers",
    "GitHubCVSS",
    "GitHubPackage",
    "GitHubVulnerability",
    "GitHubAdvisory",
    # Exceptions
    "VulnerabilityScanError",
    "APIError",
    "RateLimitError",
    "AuthenticationError",
    "PackageNotFoundError",
    "InvalidVersionError",
    "ConfigurationError",
    "CacheError",
    "TimeoutError",
    "CancellationError",
]
