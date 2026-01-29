"""
Vulnerability aggregation and deduplication.

This package provides utilities for:
- Merging duplicate vulnerabilities from multiple sources
- Calculating severity summaries
- Filtering vulnerabilities by criteria

Example:
    >>> from binary_sbom.vulnscan.aggregation import Deduplicator, SeveritySummarizer
    >>> dedup = Deduplicator()
    >>> merged = dedup.merge_vulnerabilities(vuln_list)
"""

from binary_sbom.vulnscan.aggregation.deduplicator import Deduplicator
from binary_sbom.vulnscan.aggregation.summarizer import SeveritySummarizer
from binary_sbom.vulnscan.aggregation.filter import VulnerabilityFilter

__all__ = [
    "Deduplicator",
    "SeveritySummarizer",
    "VulnerabilityFilter",
]
