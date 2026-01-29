"""
Vulnerability scanner interface and implementation.

This module provides the main scanner that coordinates queries
to multiple vulnerability databases.

Defines the Scanner interface for querying vulnerabilities by
component name and version, along with the concrete VulnScanner
implementation that aggregates results from multiple sources.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Set

from binary_sbom.vulnscan.exceptions import (
    APIError,
    AuthenticationError,
    CancellationError,
    RateLimitError,
    TimeoutError,
    VulnerabilityScanError,
)
from binary_sbom.vulnscan.types import (
    PackageIdentifier,
    ScanResult,
    Vulnerability,
    VulnerabilitySource,
)
from binary_sbom.vulnscan.utils.cancellation import check_cancellation

logger = logging.getLogger(__name__)


class Scanner(ABC):
    """
    Abstract interface for vulnerability scanners.

    Defines the contract that all vulnerability scanners must implement.
    Scanners query vulnerability databases for known security issues
    in software packages by component name and version.

    Example:
        >>> class MyScanner(Scanner):
        ...     def query_by_name_version(self, ecosystem, name, version):
        ...         # Implementation here
        ...         return []
    """

    @abstractmethod
    def query_by_name_version(
        self, ecosystem: str, name: str, version: str
    ) -> List[Vulnerability]:
        """
        Query vulnerabilities by package name and version.

        This is the core method that all scanners must implement.
        It queries the vulnerability database for known security issues
        affecting the specified package version.

        Args:
            ecosystem: Package ecosystem (e.g., "npm", "PyPI", "Maven", "Go")
            name: Package name (e.g., "lodash", "requests", "webpack")
            version: Package version (e.g., "4.17.15", "2.28.0")

        Returns:
            List of Vulnerability objects affecting this package version.
            Returns empty list if no vulnerabilities found.

        Raises:
            APIError: If the API request fails
            PackageNotFoundError: If package is not found in the database
            InvalidVersionError: If version format is invalid

        Example:
            >>> vulns = scanner.query_by_name_version("npm", "lodash", "4.17.15")
            >>> len(vulns)
            2
            >>> vulns[0].id
            'CVE-2021-23337'
        """
        pass

    @abstractmethod
    def get_source(self) -> VulnerabilitySource:
        """
        Identify the vulnerability source for this scanner.

        Returns:
            VulnerabilitySource enum indicating which database
            this scanner queries (OSV, NVD, GITHUB, or UNKNOWN)

        Example:
            >>> scanner.get_source()
            <VulnerabilitySource.OSV: 'OSV'>
        """
        pass

    def supports_batch_queries(self) -> bool:
        """
        Check if this scanner supports batch queries.

        Returns:
            True if batch queries are supported, False otherwise.
            Default implementation returns False.

        Example:
            >>> scanner.supports_batch_queries()
            True
        """
        return False

    def query_batch(
        self, packages: List[PackageIdentifier]
    ) -> dict[PackageIdentifier, List[Vulnerability]]:
        """
        Query multiple packages in a single batch request.

        Default implementation calls query_by_name_version for each package.
        Scanners that support batch queries should override this method
        for better performance.

        Args:
            packages: List of PackageIdentifier objects

        Returns:
            Dictionary mapping each PackageIdentifier to its list of
            Vulnerability objects. Packages with no vulnerabilities
            have empty lists.

        Raises:
            APIError: If the batch API request fails
            NotImplementedError: If batch queries are not supported

        Example:
            >>> packages = [
            ...     PackageIdentifier("npm", "lodash", "4.17.15"),
            ...     PackageIdentifier("npm", "express", "4.17.1")
            ... ]
            >>> results = scanner.query_batch(packages)
            >>> results[packages[0]][0].id
            'CVE-2021-23337'
        """
        if not self.supports_batch_queries():
            raise NotImplementedError(
                f"{self.__class__.__name__} does not support batch queries"
            )

        results = {}
        for pkg in packages:
            results[pkg] = self.query_by_name_version(
                pkg.ecosystem, pkg.name, pkg.version
            )
        return results


class VulnScanner:
    """
    Main vulnerability scanner coordinating multiple data sources.

    The scanner queries OSV, NVD, and GitHub databases for known
    vulnerabilities in packages, then aggregates and deduplicates results.

    This class implements a facade pattern, providing a simple interface
    for vulnerability scanning while coordinating multiple Scanner
    implementations internally.

    Attributes:
        config: Scanner configuration (optional, can be None)
        sources: Set of enabled vulnerability sources
        scanners: List of Scanner instances for enabled sources

    Example:
        >>> from binary_sbom.vulnscan.scanners import VulnScanner
        >>> scanner = VulnScanner()
        >>> result = scanner.scan_package("npm", "lodash", "4.17.15")
        >>> print(f"Found {result.total_vulnerabilities} vulnerabilities")
        Found 2 vulnerabilities
    """

    def __init__(self, config: Optional[object] = None):
        """
        Initialize vulnerability scanner.

        Args:
            config: Optional configuration object. Can be None for default settings.
                   Configuration will be fully implemented in Phase 2, Subtask 2.4.

        Example:
            >>> scanner = VulnScanner()
            >>> scanner.sources  # Defaults to OSV if no config provided
            {<VulnerabilitySource.OSV: 'OSV'>}
        """
        self.config = config
        self.sources: Set[VulnerabilitySource] = self._init_sources()
        self.scanners: List[Scanner] = []

        # Initialize scanners for enabled sources
        # Scanner implementations will be added in Phase 3-5
        self._init_scanners()

    def _init_sources(self) -> Set[VulnerabilitySource]:
        """
        Initialize enabled vulnerability sources based on config.

        Determines which vulnerability databases should be queried based on:
        1. Configuration object (if provided)
        2. Available API keys
        3. Default fallback (OSV only)

        Returns:
            Set of enabled VulnerabilitySource enums

        Note:
            Full configuration support will be implemented in Phase 2, Subtask 2.4.
            Currently defaults to OSV only.

        Example:
            >>> scanner = VulnScanner()
            >>> scanner._init_sources()
            {<VulnerabilitySource.OSV: 'OSV'>}
        """
        # Default to OSV only if no config provided
        # Full config implementation in Phase 2, Subtask 2.4
        if self.config is None:
            return {VulnerabilitySource.OSV}

        # Configuration-based source selection will be implemented later
        # For now, return OSV as default
        return {VulnerabilitySource.OSV}

    def _init_scanners(self) -> None:
        """
        Initialize Scanner instances for enabled sources.

        Creates Scanner objects for each enabled vulnerability source.
        Initializes OSV, NVD, and GitHub scanners based on configuration
        and available API keys.
        """
        from binary_sbom.vulnscan.clients import OSVScanner, NVDScanner, GitHubScanner

        # Always initialize OSV scanner (no API key required)
        if VulnerabilitySource.OSV in self.sources:
            osv_scanner = OSVScanner()
            self.scanners.append(osv_scanner)
            logger.debug(f"Initialized OSV scanner")

        # Initialize NVD scanner if enabled and API key is available
        if VulnerabilitySource.NVD in self.sources:
            # Check if config has NVD API key
            nvd_api_key = None
            if self.config is not None:
                nvd_api_key = getattr(self.config, "nvd_api_key", None)

            # Only initialize NVD scanner if API key is provided
            # (NVD has very low rate limits without API key)
            if nvd_api_key:
                nvd_scanner = NVDScanner(api_key=nvd_api_key)
                self.scanners.append(nvd_scanner)
                logger.debug(f"Initialized NVD scanner with API key")
            else:
                logger.debug(
                    "NVD source enabled but no API key provided, "
                    "skipping NVD scanner initialization"
                )

        # Initialize GitHub scanner if enabled and token is available
        if VulnerabilitySource.GITHUB in self.sources:
            # Check if config has GitHub token
            github_token = None
            if self.config is not None:
                github_token = getattr(self.config, "github_token", None)

            # GitHub scanner works without token but has higher limits with token
            github_scanner = GitHubScanner(token=github_token)
            self.scanners.append(github_scanner)
            if github_token:
                logger.debug(f"Initialized GitHub scanner with token")
            else:
                logger.debug(f"Initialized GitHub scanner without token")

    def scan_package(
        self,
        ecosystem: str,
        name: str,
        version: str,
        cancellation_context: Optional["CancellationContext"] = None,
    ) -> ScanResult:
        """
        Scan a single package for known vulnerabilities.

        Queries all enabled sources and aggregates results. This method
        coordinates multiple Scanner instances, collects results from each,
        and combines them into a unified ScanResult.

        Args:
            ecosystem: Package ecosystem (e.g., "npm", "PyPI", "Maven")
            name: Package name
            version: Package version
            cancellation_context: Optional context for cancellation support

        Returns:
            ScanResult containing all found vulnerabilities with severity
            summary and source information. Returns empty result if no
            vulnerabilities found.

        Raises:
            APIError: If all sources fail to respond
            PackageNotFoundError: If package not found in any source
            InvalidVersionError: If version format is invalid
            CancellationError: If operation is cancelled via cancellation_context

        Example:
            >>> result = scanner.scan_package("npm", "lodash", "4.17.15")
            >>> result.total_vulnerabilities
            2
            >>> result.severity_summary
            {'CRITICAL': 1, 'HIGH': 1, 'MEDIUM': 0, 'LOW': 0}
        """
        # Create package identifier
        package = PackageIdentifier(ecosystem=ecosystem, name=name, version=version)

        # Check for cancellation before starting
        check_cancellation(cancellation_context)

        # Collect vulnerabilities from all enabled sources
        all_vulnerabilities: List[Vulnerability] = []
        sources_queried: Set[VulnerabilitySource] = set()
        sources_failed: dict[VulnerabilitySource, str] = {}

        # Query each scanner
        for scanner_instance in self.scanners:
            # Check for cancellation before each scanner
            check_cancellation(cancellation_context)

            source = scanner_instance.get_source()
            try:
                vulns = scanner_instance.query_by_name_version(
                    ecosystem, name, version
                )
                all_vulnerabilities.extend(vulns)
                sources_queried.add(source)
                logger.debug(
                    f"Successfully queried {source.value} for "
                    f"{ecosystem}/{name}@{version}: found {len(vulns)} vulnerabilities"
                )
            except CancellationError:
                # Re-raise cancellation errors immediately
                logger.debug(
                    f"Scan of {ecosystem}/{name}@{version} cancelled by user"
                )
                raise
            except RateLimitError as e:
                # Rate limit errors should be logged but don't fail the scan
                error_msg = f"{source.value} API rate limit exceeded"
                if e.retry_after:
                    error_msg += f" (retry after {e.retry_after}s)"
                sources_failed[source] = error_msg
                logger.warning(
                    f"{error_msg} while querying {ecosystem}/{name}@{version}. "
                    f"Continuing with other sources."
                )
            except AuthenticationError as e:
                # Authentication errors indicate configuration issues
                error_msg = f"{source.value} API authentication failed"
                if e.reason:
                    error_msg += f": {e.reason}"
                sources_failed[source] = error_msg
                logger.warning(
                    f"{error_msg} while querying {ecosystem}/{name}@{version}. "
                    f"Continuing with other sources."
                )
            except TimeoutError as e:
                # Timeout errors are transient, log and continue
                error_msg = f"{source.value} API request timed out"
                if e.timeout:
                    error_msg += f" after {e.timeout}s"
                sources_failed[source] = error_msg
                logger.warning(
                    f"{error_msg} while querying {ecosystem}/{name}@{version}. "
                    f"Continuing with other sources."
                )
            except APIError as e:
                # General API errors, log and continue
                error_msg = f"{source.value} API error"
                if e.status_code:
                    error_msg += f" (HTTP {e.status_code})"
                if e.message:
                    error_msg += f": {e.message}"
                sources_failed[source] = error_msg
                logger.warning(
                    f"{error_msg} while querying {ecosystem}/{name}@{version}. "
                    f"Continuing with other sources."
                )
            except VulnerabilityScanError as e:
                # Other vulnerability scanning errors
                error_msg = str(e)
                sources_failed[source] = error_msg
                logger.warning(
                    f"Error querying {source.value} for {ecosystem}/{name}@{version}: "
                    f"{error_msg}. Continuing with other sources."
                )
            except Exception as e:
                # Unexpected errors - log with full traceback
                error_msg = f"Unexpected error: {str(e)}"
                sources_failed[source] = error_msg
                logger.exception(
                    f"Unexpected error querying {source.value} for "
                    f"{ecosystem}/{name}@{version}. Continuing with other sources."
                )

        # Check if all sources failed
        if not sources_queried and len(self.scanners) > 0:
            # All sources failed, raise error with details
            if len(sources_failed) == 1:
                # Single source failed
                failed_source, error_msg = next(iter(sources_failed.items()))
                raise APIError(
                    message=f"All vulnerability sources failed. {failed_source.value}: {error_msg}",
                    source=failed_source.value,
                )
            else:
                # Multiple sources failed
                error_details = "; ".join(
                    [f"{src.value}: {msg}" for src, msg in sources_failed.items()]
                )
                raise APIError(
                    message=f"All vulnerability sources failed: {error_details}",
                    source="multiple",
                )

        # Final cancellation check before returning
        check_cancellation(cancellation_context)

        # Log summary of failures if any
        if sources_failed:
            logger.info(
                f"Completed scan of {ecosystem}/{name}@{version} with {len(sources_failed)} "
                f"failed source(s): {', '.join([s.value for s in sources_failed.keys()])}"
            )

        # Create vulnerability match
        from binary_sbom.vulnscan.types import VulnerabilityMatch

        match = VulnerabilityMatch(package=package, vulnerabilities=all_vulnerabilities)

        # Create scan result
        result = ScanResult(
            packages=[match],
            sources_queried=sources_queried,
        )

        return result

    def scan_batch(
        self,
        packages: List[PackageIdentifier],
        cancellation_context: Optional["CancellationContext"] = None,
    ) -> ScanResult:
        """
        Scan multiple packages for known vulnerabilities.

        Uses batch queries where supported for efficiency. For scanners
        that don't support batch queries, falls back to individual queries.

        Args:
            packages: List of PackageIdentifier objects
            cancellation_context: Optional context for cancellation support

        Returns:
            ScanResult containing all vulnerabilities across all packages.
            Includes summary statistics and severity breakdown.

        Raises:
            APIError: If all sources fail
            InvalidVersionError: If any package version is invalid
            CancellationError: If operation is cancelled via cancellation_context
            NotImplementedError: If batch scanning is not supported

        Example:
            >>> packages = [
            ...     PackageIdentifier("npm", "lodash", "4.17.15"),
            ...     PackageIdentifier("npm", "express", "4.17.1")
            ... ]
            >>> result = scanner.scan_batch(packages)
            >>> result.total_packages
            2
            >>> result.affected_packages
            2
        """
        # Batch scanning will be implemented in Phase 6, Subtask 6.1
        # after deduplication logic is available
        raise NotImplementedError(
            "Batch scanning will be implemented in Phase 6, Subtask 6.1"
        )
