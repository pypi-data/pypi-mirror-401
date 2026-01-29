"""
Vulnerability filtering utilities.

This module provides utilities for filtering vulnerabilities
by various criteria including severity, CVSS score, source,
CWE IDs, and date ranges.

Implementation for Phase 6, Subtask 6.3.
"""

import logging
from datetime import datetime
from typing import List, Optional

from binary_sbom.vulnscan.types import (
    Severity,
    Vulnerability,
    VulnerabilitySource,
)

logger = logging.getLogger(__name__)

# Severity order for comparison (lowest to highest)
SEVERITY_ORDER = {
    Severity.NONE: 0,
    Severity.LOW: 1,
    Severity.MEDIUM: 2,
    Severity.HIGH: 3,
    Severity.CRITICAL: 4,
}


class VulnerabilityFilter:
    """
    Filters vulnerabilities based on various criteria.

    Supports filtering by:
    - Severity level (exact or range)
    - CVSS score (minimum or maximum)
    - Vulnerability source (OSV, NVD, GitHub)
    - CWE ID presence
    - Publication date range
    - Combinations of filters (AND logic)

    Example:
        >>> filter = VulnerabilityFilter()
        >>> critical_only = filter.by_severity(vulns, Severity.CRITICAL)
        >>> high_and_above = filter.by_min_severity(vulns, Severity.HIGH)
        >>> high_score = filter.by_min_cvss_score(vulns, 7.0)
    """

    def by_severity(
        self, vulnerabilities: List[Vulnerability], severity: Severity
    ) -> List[Vulnerability]:
        """
        Filter vulnerabilities by exact severity level.

        Uses the highest severity across all CVSS scores for comparison.
        Vulnerabilities without severity information are excluded.

        Args:
            vulnerabilities: List of Vulnerability objects
            severity: Severity level to filter by

        Returns:
            Filtered list of vulnerabilities with matching severity

        Example:
            >>> filter = VulnerabilityFilter()
            >>> vulns = [vuln1, vuln2, vuln3]
            >>> critical_only = filter.by_severity(vulns, Severity.CRITICAL)
            >>> len(critical_only)
            1
        """
        filtered = []
        for vuln in vulnerabilities:
            highest_severity = vuln.get_highest_severity()
            if highest_severity == severity:
                filtered.append(vuln)
            elif highest_severity is None:
                logger.debug(
                    f"Vulnerability {vuln.id} has no severity information, excluding from filter"
                )

        logger.debug(
            f"Filtered to {len(filtered)} vulnerabilities with severity {severity.value} "
            f"(from {len(vulnerabilities)} total)"
        )

        return filtered

    def by_min_severity(
        self, vulnerabilities: List[Vulnerability], min_severity: Severity
    ) -> List[Vulnerability]:
        """
        Filter vulnerabilities by minimum severity level.

        Returns vulnerabilities with severity >= min_severity.
        Uses the highest severity across all CVSS scores for comparison.
        Vulnerabilities without severity information are excluded.

        Args:
            vulnerabilities: List of Vulnerability objects
            min_severity: Minimum severity level

        Returns:
            Filtered list of vulnerabilities with severity >= min_severity

        Example:
            >>> filter = VulnerabilityFilter()
            >>> vulns = [vuln1, vuln2, vuln3]
            >>> high_and_above = filter.by_min_severity(vulns, Severity.HIGH)
            >>> # Returns HIGH and CRITICAL vulnerabilities
        """
        min_level = SEVERITY_ORDER.get(min_severity, 0)
        filtered = []

        for vuln in vulnerabilities:
            highest_severity = vuln.get_highest_severity()
            if highest_severity is None:
                logger.debug(
                    f"Vulnerability {vuln.id} has no severity information, excluding from filter"
                )
                continue

            severity_level = SEVERITY_ORDER.get(highest_severity, 0)
            if severity_level >= min_level:
                filtered.append(vuln)

        logger.debug(
            f"Filtered to {len(filtered)} vulnerabilities with severity >= {min_severity.value} "
            f"(from {len(vulnerabilities)} total)"
        )

        return filtered

    def by_max_severity(
        self, vulnerabilities: List[Vulnerability], max_severity: Severity
    ) -> List[Vulnerability]:
        """
        Filter vulnerabilities by maximum severity level.

        Returns vulnerabilities with severity <= max_severity.
        Uses the highest severity across all CVSS scores for comparison.
        Vulnerabilities without severity information are excluded.

        Args:
            vulnerabilities: List of Vulnerability objects
            max_severity: Maximum severity level

        Returns:
            Filtered list of vulnerabilities with severity <= max_severity

        Example:
            >>> filter = VulnerabilityFilter()
            >>> vulns = [vuln1, vuln2, vuln3]
            >>> medium_and_below = filter.by_max_severity(vulns, Severity.MEDIUM)
            >>> # Returns LOW, MEDIUM vulnerabilities (excludes HIGH, CRITICAL)
        """
        max_level = SEVERITY_ORDER.get(max_severity, 4)
        filtered = []

        for vuln in vulnerabilities:
            highest_severity = vuln.get_highest_severity()
            if highest_severity is None:
                logger.debug(
                    f"Vulnerability {vuln.id} has no severity information, excluding from filter"
                )
                continue

            severity_level = SEVERITY_ORDER.get(highest_severity, 0)
            if severity_level <= max_level:
                filtered.append(vuln)

        logger.debug(
            f"Filtered to {len(filtered)} vulnerabilities with severity <= {max_severity.value} "
            f"(from {len(vulnerabilities)} total)"
        )

        return filtered

    def by_severity_range(
        self,
        vulnerabilities: List[Vulnerability],
        min_severity: Severity,
        max_severity: Severity,
    ) -> List[Vulnerability]:
        """
        Filter vulnerabilities by severity range.

        Returns vulnerabilities with min_severity <= severity <= max_severity.
        Uses the highest severity across all CVSS scores for comparison.
        Vulnerabilities without severity information are excluded.

        Args:
            vulnerabilities: List of Vulnerability objects
            min_severity: Minimum severity level (inclusive)
            max_severity: Maximum severity level (inclusive)

        Returns:
            Filtered list of vulnerabilities within severity range

        Raises:
            ValueError: If min_severity > max_severity

        Example:
            >>> filter = VulnerabilityFilter()
            >>> vulns = [vuln1, vuln2, vuln3]
            >>> medium_to_high = filter.by_severity_range(vulns, Severity.MEDIUM, Severity.HIGH)
            >>> # Returns only MEDIUM and HIGH vulnerabilities
        """
        min_level = SEVERITY_ORDER.get(min_severity, 0)
        max_level = SEVERITY_ORDER.get(max_severity, 4)

        if min_level > max_level:
            raise ValueError(
                f"min_severity ({min_severity.value}) cannot be greater than "
                f"max_severity ({max_severity.value})"
            )

        filtered = []

        for vuln in vulnerabilities:
            highest_severity = vuln.get_highest_severity()
            if highest_severity is None:
                logger.debug(
                    f"Vulnerability {vuln.id} has no severity information, excluding from filter"
                )
                continue

            severity_level = SEVERITY_ORDER.get(highest_severity, 0)
            if min_level <= severity_level <= max_level:
                filtered.append(vuln)

        logger.debug(
            f"Filtered to {len(filtered)} vulnerabilities with "
            f"{min_severity.value} <= severity <= {max_severity.value} "
            f"(from {len(vulnerabilities)} total)"
        )

        return filtered

    def by_min_cvss_score(
        self, vulnerabilities: List[Vulnerability], min_score: float
    ) -> List[Vulnerability]:
        """
        Filter vulnerabilities by minimum CVSS base score.

        Uses the highest CVSS score across all scores for comparison.
        Vulnerabilities without severity information are excluded.

        Args:
            vulnerabilities: List of Vulnerability objects
            min_score: Minimum CVSS base score (0.0 - 10.0)

        Returns:
            Filtered list of vulnerabilities with CVSS score >= min_score

        Raises:
            ValueError: If min_score is not between 0.0 and 10.0

        Example:
            >>> filter = VulnerabilityFilter()
            >>> vulns = [vuln1, vuln2, vuln3]
            >>> high_score = filter.by_min_cvss_score(vulns, 7.0)
            >>> # Returns vulnerabilities with CVSS >= 7.0
        """
        if not 0.0 <= min_score <= 10.0:
            raise ValueError(f"min_score must be between 0.0 and 10.0, got {min_score}")

        filtered = []

        for vuln in vulnerabilities:
            highest_score = vuln.get_highest_severity()
            if highest_score is None:
                logger.debug(
                    f"Vulnerability {vuln.id} has no severity information, excluding from filter"
                )
                continue

            # Get highest base score from all scores
            if vuln.severity is not None:
                score = vuln.severity.base_score
            else:
                continue

            if score >= min_score:
                filtered.append(vuln)

        logger.debug(
            f"Filtered to {len(filtered)} vulnerabilities with CVSS score >= {min_score} "
            f"(from {len(vulnerabilities)} total)"
        )

        return filtered

    def by_max_cvss_score(
        self, vulnerabilities: List[Vulnerability], max_score: float
    ) -> List[Vulnerability]:
        """
        Filter vulnerabilities by maximum CVSS base score.

        Uses the highest CVSS score across all scores for comparison.
        Vulnerabilities without severity information are excluded.

        Args:
            vulnerabilities: List of Vulnerability objects
            max_score: Maximum CVSS base score (0.0 - 10.0)

        Returns:
            Filtered list of vulnerabilities with CVSS score <= max_score

        Raises:
            ValueError: If max_score is not between 0.0 and 10.0

        Example:
            >>> filter = VulnerabilityFilter()
            >>> vulns = [vuln1, vuln2, vuln3]
            >>> medium_score = filter.by_max_cvss_score(vulns, 6.9)
            >>> # Returns vulnerabilities with CVSS <= 6.9
        """
        if not 0.0 <= max_score <= 10.0:
            raise ValueError(f"max_score must be between 0.0 and 10.0, got {max_score}")

        filtered = []

        for vuln in vulnerabilities:
            highest_score = vuln.get_highest_severity()
            if highest_score is None:
                logger.debug(
                    f"Vulnerability {vuln.id} has no severity information, excluding from filter"
                )
                continue

            # Get highest base score from all scores
            if vuln.severity is not None:
                score = vuln.severity.base_score
            else:
                continue

            if score <= max_score:
                filtered.append(vuln)

        logger.debug(
            f"Filtered to {len(filtered)} vulnerabilities with CVSS score <= {max_score} "
            f"(from {len(vulnerabilities)} total)"
        )

        return filtered

    def by_cvss_score_range(
        self, vulnerabilities: List[Vulnerability], min_score: float, max_score: float
    ) -> List[Vulnerability]:
        """
        Filter vulnerabilities by CVSS base score range.

        Uses the highest CVSS score across all scores for comparison.
        Vulnerabilities without severity information are excluded.

        Args:
            vulnerabilities: List of Vulnerability objects
            min_score: Minimum CVSS base score (0.0 - 10.0)
            max_score: Maximum CVSS base score (0.0 - 10.0)

        Returns:
            Filtered list of vulnerabilities within CVSS score range

        Raises:
            ValueError: If scores are not between 0.0 and 10.0 or min_score > max_score

        Example:
            >>> filter = VulnerabilityFilter()
            >>> vulns = [vuln1, vuln2, vuln3]
            >>> medium_range = filter.by_cvss_score_range(vulns, 4.0, 6.9)
            >>> # Returns vulnerabilities with 4.0 <= CVSS <= 6.9
        """
        if not 0.0 <= min_score <= 10.0:
            raise ValueError(f"min_score must be between 0.0 and 10.0, got {min_score}")
        if not 0.0 <= max_score <= 10.0:
            raise ValueError(f"max_score must be between 0.0 and 10.0, got {max_score}")
        if min_score > max_score:
            raise ValueError(
                f"min_score ({min_score}) cannot be greater than max_score ({max_score})"
            )

        filtered = []

        for vuln in vulnerabilities:
            if vuln.severity is None:
                logger.debug(
                    f"Vulnerability {vuln.id} has no severity information, excluding from filter"
                )
                continue

            score = vuln.severity.base_score
            if min_score <= score <= max_score:
                filtered.append(vuln)

        logger.debug(
            f"Filtered to {len(filtered)} vulnerabilities with "
            f"{min_score} <= CVSS score <= {max_score} "
            f"(from {len(vulnerabilities)} total)"
        )

        return filtered

    def by_source(
        self, vulnerabilities: List[Vulnerability], source: VulnerabilitySource
    ) -> List[Vulnerability]:
        """
        Filter vulnerabilities by source database.

        Args:
            vulnerabilities: List of Vulnerability objects
            source: Vulnerability source to filter by

        Returns:
            Filtered list of vulnerabilities from the specified source

        Example:
            >>> filter = VulnerabilityFilter()
            >>> vulns = [vuln1, vuln2, vuln3]
            >>> osv_only = filter.by_source(vulns, VulnerabilitySource.OSV)
        """
        filtered = [vuln for vuln in vulnerabilities if vuln.source == source]

        logger.debug(
            f"Filtered to {len(filtered)} vulnerabilities from {source.value} "
            f"(from {len(vulnerabilities)} total)"
        )

        return filtered

    def by_sources(
        self, vulnerabilities: List[Vulnerability], sources: List[VulnerabilitySource]
    ) -> List[Vulnerability]:
        """
        Filter vulnerabilities by multiple source databases.

        Returns vulnerabilities from any of the specified sources.

        Args:
            vulnerabilities: List of Vulnerability objects
            sources: List of vulnerability sources to filter by

        Returns:
            Filtered list of vulnerabilities from any of the specified sources

        Example:
            >>> filter = VulnerabilityFilter()
            >>> vulns = [vuln1, vuln2, vuln3]
            >>> osv_and_nvd = filter.by_sources(
            ...     vulns,
            ...     [VulnerabilitySource.OSV, VulnerabilitySource.NVD]
            ... )
        """
        source_set = set(sources)
        filtered = [vuln for vuln in vulnerabilities if vuln.source in source_set]

        logger.debug(
            f"Filtered to {len(filtered)} vulnerabilities from {[s.value for s in sources]} "
            f"(from {len(vulnerabilities)} total)"
        )

        return filtered

    def by_cwe_id(
        self, vulnerabilities: List[Vulnerability], cwe_id: str
    ) -> List[Vulnerability]:
        """
        Filter vulnerabilities that have a specific CWE ID.

        Matches against the cwe_ids list of each vulnerability.

        Args:
            vulnerabilities: List of Vulnerability objects
            cwe_id: CWE ID to filter by (e.g., "CWE-79")

        Returns:
            Filtered list of vulnerabilities with the specified CWE ID

        Example:
            >>> filter = VulnerabilityFilter()
            >>> vulns = [vuln1, vuln2, vuln3]
            >>> xss_vulns = filter.by_cwe_id(vulns, "CWE-79")
        """
        filtered = [
            vuln for vuln in vulnerabilities if cwe_id in vuln.cwe_ids
        ]

        logger.debug(
            f"Filtered to {len(filtered)} vulnerabilities with {cwe_id} "
            f"(from {len(vulnerabilities)} total)"
        )

        return filtered

    def by_has_cwe(
        self, vulnerabilities: List[Vulnerability]
    ) -> List[Vulnerability]:
        """
        Filter vulnerabilities that have any CWE ID assigned.

        Excludes vulnerabilities with empty CWE ID lists.

        Args:
            vulnerabilities: List of Vulnerability objects

        Returns:
            Filtered list of vulnerabilities with at least one CWE ID

        Example:
            >>> filter = VulnerabilityFilter()
            >>> vulns = [vuln1, vuln2, vuln3]
            >>> with_cwe = filter.by_has_cwe(vulns)
        """
        filtered = [vuln for vuln in vulnerabilities if vuln.cwe_ids]

        logger.debug(
            f"Filtered to {len(filtered)} vulnerabilities with CWE IDs "
            f"(from {len(vulnerabilities)} total)"
        )

        return filtered

    def by_date_range(
        self,
        vulnerabilities: List[Vulnerability],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        use_published: bool = True,
    ) -> List[Vulnerability]:
        """
        Filter vulnerabilities by date range.

        Filters based on published date by default. Can use modified date instead.
        Vulnerabilities without the specified date are excluded.

        Args:
            vulnerabilities: List of Vulnerability objects
            start_date: Start of date range (inclusive). If None, no lower bound.
            end_date: End of date range (inclusive). If None, no upper bound.
            use_published: If True, use published date. If False, use modified date.

        Returns:
            Filtered list of vulnerabilities within the date range

        Raises:
            ValueError: If start_date > end_date

        Example:
            >>> filter = VulnerabilityFilter()
            >>> vulns = [vuln1, vuln2, vuln3]
            >>> recent = filter.by_date_range(
            ...     vulns,
            ...     start_date=datetime(2023, 1, 1),
            ...     end_date=datetime(2023, 12, 31)
            ... )
        """
        if start_date and end_date and start_date > end_date:
            raise ValueError(
                f"start_date ({start_date}) cannot be later than end_date ({end_date})"
            )

        filtered = []
        date_field = "published" if use_published else "modified"

        for vuln in vulnerabilities:
            vuln_date = vuln.published if use_published else vuln.modified

            if vuln_date is None:
                logger.debug(
                    f"Vulnerability {vuln.id} has no {date_field} date, excluding from filter"
                )
                continue

            if start_date and vuln_date < start_date:
                continue
            if end_date and vuln_date > end_date:
                continue

            filtered.append(vuln)

        logger.debug(
            f"Filtered to {len(filtered)} vulnerabilities within {date_field} date range "
            f"(from {len(vulnerabilities)} total)"
        )

        return filtered

    def combine_filters(
        self,
        vulnerabilities: List[Vulnerability],
        filters: List[callable],
        require_all: bool = True,
    ) -> List[Vulnerability]:
        """
        Combine multiple filters with AND or OR logic.

        Args:
            vulnerabilities: List of Vulnerability objects
            filters: List of filter functions (each takes List[Vulnerability] and returns List[Vulnerability])
            require_all: If True, apply AND logic (vuln must pass all filters).
                        If False, apply OR logic (vuln must pass at least one filter).

        Returns:
            Filtered list of vulnerabilities

        Example:
            >>> filter = VulnerabilityFilter()
            >>> vulns = [vuln1, vuln2, vuln3]
            >>> critical_osv = filter.combine_filters(
            ...     vulns,
            ...     [
            ...         lambda v: filter.by_severity(v, Severity.CRITICAL),
            ...         lambda v: filter.by_source(v, VulnerabilitySource.OSV)
            ...     ],
            ...     require_all=True
            ... )
            >>> # Returns only CRITICAL vulnerabilities from OSV
        """
        if not filters:
            return vulnerabilities[:]

        if require_all:
            # AND logic: apply filters sequentially
            result = vulnerabilities
            for i, filter_func in enumerate(filters):
                result = filter_func(result)
                logger.debug(
                    f"After filter {i + 1}/{len(filters)}: {len(result)} vulnerabilities remaining"
                )
        else:
            # OR logic: apply all filters and combine results (deduplicated)
            all_results = []
            seen_ids = set()

            for filter_func in filters:
                filtered = filter_func(vulnerabilities)
                for vuln in filtered:
                    if vuln.id not in seen_ids:
                        all_results.append(vuln)
                        seen_ids.add(vuln.id)

            result = all_results

        logger.debug(
            f"Combined {len(filters)} filters with {'AND' if require_all else 'OR'} logic: "
            f"{len(result)} vulnerabilities (from {len(vulnerabilities)} total)"
        )

        return result
