"""
Severity summarization utilities.

This module provides utilities for calculating vulnerability
severity summaries and statistics.

Implementation for Phase 6, Subtask 6.2.
"""

import logging
from typing import Dict, List

from binary_sbom.vulnscan.types import (
    ScanResult,
    Severity,
    Vulnerability,
)

logger = logging.getLogger(__name__)


class SeveritySummarizer:
    """
    Calculates severity summaries for vulnerability scan results.

    Aggregates vulnerabilities by severity level (Critical, High, Medium, Low)
    and provides formatted output for display.

    Example:
        >>> summarizer = SeveritySummarizer()
        >>> summary = summarizer.summarize_vulnerabilities(vuln_list)
        >>> print(summary)
        {'CRITICAL': 3, 'HIGH': 7, 'MEDIUM': 4, 'LOW': 1}
    """

    def summarize_vulnerabilities(self, vulnerabilities: List[Vulnerability]) -> Dict[str, int]:
        """
        Calculate severity counts from a list of vulnerabilities.

        Counts vulnerabilities by their highest severity level across
        all CVSS scores (primary and additional).

        Args:
            vulnerabilities: List of Vulnerability objects

        Returns:
            Dictionary mapping severity levels to counts with keys:
            'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'

        Example:
            >>> summarizer = SeveritySummarizer()
            >>> vulns = [vuln1, vuln2, vuln3]
            >>> summary = summarizer.summarize_vulnerabilities(vulns)
            >>> summary['CRITICAL']
            1
        """
        severity_counts = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
        }

        for vuln in vulnerabilities:
            highest_severity = vuln.get_highest_severity()
            if highest_severity is None:
                logger.debug(f"Vulnerability {vuln.id} has no severity information, skipping")
                continue

            severity_str = highest_severity.value
            if severity_str in severity_counts:
                severity_counts[severity_str] += 1
            else:
                logger.debug(
                    f"Vulnerability {vuln.id} has unknown severity: {severity_str}"
                )

        logger.debug(
            f"Calculated severity summary: {severity_counts['CRITICAL']} Critical, "
            f"{severity_counts['HIGH']} High, {severity_counts['MEDIUM']} Medium, "
            f"{severity_counts['LOW']} Low"
        )

        return severity_counts

    def summarize(self, result: ScanResult) -> Dict[str, int]:
        """
        Calculate severity counts from scan result.

        Extracts severity information from ScanResult's severity_summary field.
        This is a convenience method for accessing already-calculated summaries.

        Args:
            result: ScanResult object

        Returns:
            Dictionary mapping severity levels to counts

        Example:
            >>> summarizer = SeveritySummarizer()
            >>> summary = summarizer.summarize(scan_result)
            >>> print(summary)
            {'CRITICAL': 3, 'HIGH': 7, 'MEDIUM': 4, 'LOW': 1}
        """
        # ScanResult already calculates severity_summary in __post_init__
        # Just return it, ensuring all severity levels are present
        return {
            "CRITICAL": result.severity_summary.get("CRITICAL", 0),
            "HIGH": result.severity_summary.get("HIGH", 0),
            "MEDIUM": result.severity_summary.get("MEDIUM", 0),
            "LOW": result.severity_summary.get("LOW", 0),
        }

    def format_summary(
        self, summary: Dict[str, int], include_total: bool = True
    ) -> str:
        """
        Format severity summary for display.

        Creates a human-readable string showing vulnerability counts
        by severity level.

        Args:
            summary: Dictionary mapping severity levels to counts
            include_total: Whether to include total count (default: True)

        Returns:
            Formatted string representation

        Example:
            >>> summarizer = SeveritySummarizer()
            >>> summary = {'CRITICAL': 3, 'HIGH': 7, 'MEDIUM': 4, 'LOW': 1}
            >>> print(summarizer.format_summary(summary))
            Critical: 3, High: 7, Medium: 4, Low: 1 (Total: 15)
        """
        parts = [
            f"Critical: {summary['CRITICAL']}",
            f"High: {summary['HIGH']}",
            f"Medium: {summary['MEDIUM']}",
            f"Low: {summary['LOW']}",
        ]

        result = ", ".join(parts)

        if include_total:
            total = sum(summary.values())
            result += f" (Total: {total})"

        return result

    def get_total_count(self, summary: Dict[str, int]) -> int:
        """
        Calculate total vulnerability count from summary.

        Args:
            summary: Dictionary mapping severity levels to counts

        Returns:
            Total number of vulnerabilities

        Example:
            >>> summarizer = SeveritySummarizer()
            >>> summary = {'CRITICAL': 3, 'HIGH': 7}
            >>> summarizer.get_total_count(summary)
            10
        """
        return sum(summary.values())

    def has_critical_vulnerabilities(self, summary: Dict[str, int]) -> bool:
        """
        Check if summary contains any Critical vulnerabilities.

        Args:
            summary: Dictionary mapping severity levels to counts

        Returns:
            True if Critical count > 0, False otherwise

        Example:
            >>> summarizer = SeveritySummarizer()
            >>> summary = {'CRITICAL': 1, 'HIGH': 5}
            >>> summarizer.has_critical_vulnerabilities(summary)
            True
        """
        return summary.get("CRITICAL", 0) > 0

    def get_severity_percentage(
        self, summary: Dict[str, int], severity: Severity
    ) -> float:
        """
        Calculate percentage of vulnerabilities at a given severity level.

        Args:
            summary: Dictionary mapping severity levels to counts
            severity: Severity level to calculate percentage for

        Returns:
            Percentage (0.0 - 100.0), or 0.0 if no vulnerabilities

        Example:
            >>> summarizer = SeveritySummarizer()
            >>> summary = {'CRITICAL': 5, 'HIGH': 5, 'MEDIUM': 0, 'LOW': 0}
            >>> summarizer.get_severity_percentage(summary, Severity.CRITICAL)
            50.0
        """
        total = self.get_total_count(summary)
        if total == 0:
            return 0.0

        count = summary.get(severity.value, 0)
        return (count / total) * 100.0
