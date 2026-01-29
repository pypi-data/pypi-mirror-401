"""
Vulnerability deduplication logic.

This module provides utilities for merging duplicate vulnerabilities
from multiple sources (OSV, NVD, GitHub).

Implementation for Phase 6, Subtask 6.1.
"""

import logging
from collections import defaultdict
from dataclasses import replace
from datetime import datetime
from typing import Dict, List, Optional, Set

from binary_sbom.vulnscan.types import (
    AffectedVersion,
    CVSSScore,
    Reference,
    Severity,
    Vulnerability,
    VulnerabilitySource,
)

logger = logging.getLogger(__name__)


class Deduplicator:
    """
    Merges duplicate vulnerabilities from multiple sources.

    When the same vulnerability is reported by OSV, NVD, and GitHub,
    this class merges them into a single entry with the highest severity.

    Deduplication Strategy:
    1. By CVE ID (primary key) - if vulnerability has a CVE ID
    2. By GHSA ID (secondary key) - if vulnerability has GHSA ID but no CVE
    3. By vulnerability ID (fallback) - uses the ID field directly

    Merging Rules:
    - Keeps the highest severity score across all duplicates
    - Combines all aliases from all sources
    - Combines all affected versions
    - Combines all unique references
    - Keeps the earliest published date
    - Keeps the latest modified date
    - Combines all unique CWE IDs
    - Combines all non-primary CVSS scores into additional_scores

    Example:
        >>> dedup = Deduplicator()
        >>> merged = dedup.merge_vulnerabilities(vuln_list)
        >>> print(f"Merged to {len(merged)} unique vulnerabilities")
    """

    def merge_vulnerabilities(
        self, vulnerabilities: List[Vulnerability]
    ) -> List[Vulnerability]:
        """
        Merge duplicate vulnerabilities from multiple sources.

        Args:
            vulnerabilities: List of Vulnerability objects from multiple sources

        Returns:
            List of unique Vulnerability objects with highest severity

        Raises:
            ValueError: If vulnerabilities list is empty

        Example:
            >>> dedup = Deduplicator()
            >>> vuln1 = Vulnerability(
            ...     id="CVE-2021-23337",
            ...     source=VulnerabilitySource.OSV,
            ...     summary="Prototype Pollution",
            ...     severity=CVSSScore(
            ...         version="3.1",
            ...         vector_string="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
            ...         base_score=9.8,
            ...         base_severity=Severity.CRITICAL
            ...     )
            ... )
            >>> vuln2 = Vulnerability(
            ...     id="GHSA-4w2v-vmj7-klvd",
            ...     source=VulnerabilitySource.GITHUB,
            ...     summary="Prototype Pollution",
            ...     aliases=["CVE-2021-23337"],
            ...     severity=CVSSScore(
            ...         version="3.1",
            ...         vector_string="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
            ...         base_score=9.8,
            ...         base_severity=Severity.CRITICAL
            ...     )
            ... )
            >>> merged = dedup.merge_vulnerabilities([vuln1, vuln2])
            >>> len(merged)
            1
        """
        if not vulnerabilities:
            raise ValueError("vulnerabilities list cannot be empty")

        if len(vulnerabilities) == 1:
            logger.debug("Only one vulnerability, no deduplication needed")
            return list(vulnerabilities)

        logger.debug(f"Deduplicating {len(vulnerabilities)} vulnerabilities")

        # Group vulnerabilities by unique identifiers
        duplicate_groups = self._find_duplicates(vulnerabilities)

        logger.debug(
            f"Found {len(duplicate_groups)} unique vulnerability groups "
            f"from {len(vulnerabilities)} total vulnerabilities"
        )

        # Merge each group
        merged_vulnerabilities = []
        for identifier, group in duplicate_groups.items():
            if len(group) == 1:
                # No duplicates, keep as-is
                merged_vulnerabilities.append(group[0])
            else:
                # Merge duplicates
                merged = self._merge_group(group, identifier)
                merged_vulnerabilities.append(merged)
                logger.debug(
                    f"Merged {len(group)} duplicates for {identifier} "
                    f"from sources: {[v.source.value for v in group]}"
                )

        logger.info(
            f"Deduplication complete: {len(vulnerabilities)} → {len(merged_vulnerabilities)} "
            f"({len(vulnerabilities) - len(merged_vulnerabilities)} duplicates removed)"
        )

        return merged_vulnerabilities

    def _find_duplicates(
        self, vulnerabilities: List[Vulnerability]
    ) -> Dict[str, List[Vulnerability]]:
        """
        Group vulnerabilities by unique identifiers.

        Grouping Strategy:
        1. If vulnerability has CVE ID (in id or aliases), group by CVE ID
        2. Else if vulnerability has GHSA ID (in id or aliases), group by GHSA ID
        3. Else group by vulnerability id

        Args:
            vulnerabilities: List of Vulnerability objects

        Returns:
            Dictionary mapping identifier to list of duplicate vulnerabilities

        Example:
            >>> dedup = Deduplicator()
            >>> vuln1 = Vulnerability(
            ...     id="CVE-2021-23337",
            ...     source=VulnerabilitySource.OSV,
            ...     summary="Vuln"
            ... )
            >>> vuln2 = Vulnerability(
            ...     id="GHSA-xxxx",
            ...     source=VulnerabilitySource.GITHUB,
            ...     summary="Vuln",
            ...     aliases=["CVE-2021-23337"]
            ... )
            >>> groups = dedup._find_duplicates([vuln1, vuln2])
            >>> "CVE-2021-23337" in groups
            True
            >>> len(groups["CVE-2021-23337"])
            2
        """
        groups: Dict[str, List[Vulnerability]] = defaultdict(list)

        # Track which vulnerabilities have been grouped
        grouped_indices: Set[int] = set()

        # First pass: group by CVE ID (primary key)
        for idx, vuln in enumerate(vulnerabilities):
            if idx in grouped_indices:
                continue

            # Check for CVE ID
            cve_ids = vuln.cve_ids
            if cve_ids:
                # Use first CVE ID as grouping key
                cve_id = cve_ids[0]
                groups[cve_id].append(vuln)
                grouped_indices.add(idx)

                # Find other vulnerabilities with same CVE ID
                for other_idx, other_vuln in enumerate(vulnerabilities):
                    if other_idx != idx and other_idx not in grouped_indices:
                        if cve_id in other_vuln.cve_ids or cve_id in other_vuln.aliases:
                            groups[cve_id].append(other_vuln)
                            grouped_indices.add(other_idx)

        # Second pass: group remaining by GHSA ID (secondary key)
        for idx, vuln in enumerate(vulnerabilities):
            if idx in grouped_indices:
                continue

            # Check for GHSA ID
            ghsa_ids = vuln.ghsa_ids
            if ghsa_ids:
                # Use first GHSA ID as grouping key
                ghsa_id = ghsa_ids[0]
                groups[ghsa_id].append(vuln)
                grouped_indices.add(idx)

                # Find other vulnerabilities with same GHSA ID
                for other_idx, other_vuln in enumerate(vulnerabilities):
                    if other_idx != idx and other_idx not in grouped_indices:
                        if ghsa_id in other_vuln.ghsa_ids or ghsa_id in other_vuln.aliases:
                            groups[ghsa_id].append(other_vuln)
                            grouped_indices.add(other_idx)

        # Third pass: group remaining by ID (fallback)
        for idx, vuln in enumerate(vulnerabilities):
            if idx in grouped_indices:
                continue

            # Use vulnerability ID as grouping key
            groups[vuln.id].append(vuln)
            grouped_indices.add(idx)

            # Find other vulnerabilities with same ID
            for other_idx, other_vuln in enumerate(vulnerabilities):
                if other_idx != idx and other_idx not in grouped_indices:
                    if vuln.id == other_vuln.id or vuln.id in other_vuln.aliases:
                        groups[vuln.id].append(other_vuln)
                        grouped_indices.add(other_idx)

        return dict(groups)

    def _merge_group(
        self, group: List[Vulnerability], identifier: str
    ) -> Vulnerability:
        """
        Merge a group of duplicate vulnerabilities into a single vulnerability.

        Merging Strategy:
        - ID: Use the identifier (CVE ID preferred, then GHSA, then first ID)
        - Source: Set to first source or "MERGED" if multiple sources
        - Summary: Use summary from highest severity vulnerability
        - Description: Use longest description
        - Aliases: Combine all unique aliases (excluding the ID)
        - Affected versions: Combine all unique affected versions
        - Severity: Keep highest severity score
        - Additional scores: Combine all non-primary scores
        - References: Combine all unique references
        - Published: Keep earliest published date
        - Modified: Keep latest modified date
        - CWE IDs: Combine all unique CWE IDs
        - Raw data: Exclude (not relevant for merged vulnerability)

        Args:
            group: List of duplicate Vulnerability objects
            identifier: Unique identifier for this group (e.g., CVE-2021-23337)

        Returns:
            Merged Vulnerability object

        Example:
            >>> dedup = Deduplicator()
            >>> vuln1 = Vulnerability(
            ...     id="CVE-2021-23337",
            ...     source=VulnerabilitySource.OSV,
            ...     summary="Prototype Pollution",
            ...     severity=CVSSScore(
            ...         version="3.1",
            ...         vector_string="CVSS:3.1/AV:N/.../C:H/I:H/A:H",
            ...         base_score=9.8,
            ...         base_severity=Severity.CRITICAL
            ...     )
            ... )
            >>> vuln2 = Vulnerability(
            ...     id="GHSA-xxxx",
            ...     source=VulnerabilitySource.GITHUB,
            ...     summary="Prototype Pollution in lodash",
            ...     aliases=["GHSA-xxxx"],
            ...     severity=CVSSScore(
            ...         version="3.1",
            ...         vector_string="CVSS:3.1/AV:N/.../C:H/I:H/A:H",
            ...         base_score=9.8,
            ...         base_severity=Severity.CRITICAL
            ...     )
            ... )
            >>> merged = dedup._merge_group([vuln1, vuln2], "CVE-2021-23337")
            >>> merged.id
            'CVE-2021-23337'
            >>> len(merged.aliases) > 0
            True
        """
        if not group:
            raise ValueError("group cannot be empty")

        if len(group) == 1:
            # No merging needed
            return group[0]

        # Sort by severity (highest first) for priority in merging
        sorted_group = sorted(
            group,
            key=lambda v: (
                v.severity.base_score if v.severity else 0,
                v.source.value,
            ),
            reverse=True,
        )

        # Use highest severity vulnerability as base
        base = sorted_group[0]

        # Combine all unique aliases
        all_aliases: Set[str] = set()
        for vuln in group:
            all_aliases.update(vuln.aliases)
            # Also add the ID if it's not the primary identifier
            if vuln.id != identifier and vuln.id not in all_aliases:
                all_aliases.add(vuln.id)

        # Remove the identifier from aliases (it's the primary ID)
        all_aliases.discard(identifier)

        # Combine all unique affected versions
        affected_versions_set = set()
        for vuln in group:
            for av in vuln.affected_versions:
                # Create a hashable representation for deduplication
                av_key = (av.introduced, av.fixed, av.range_type, av.range_string)
                affected_versions_set.add(av_key)

        affected_versions = [
            AffectedVersion(
                introduced=av_key[0],
                fixed=av_key[1],
                range_type=av_key[2],
                range_string=av_key[3],
            )
            for av_key in affected_versions_set
        ]

        # Combine all unique references
        references_set = set()
        for vuln in group:
            for ref in vuln.references:
                # Create hashable key
                ref_key = (ref.url, ref.type)
                references_set.add(ref_key)

        references = [
            Reference(url=ref_key[0], type=ref_key[1])
            for ref_key in references_set
        ]

        # Combine all unique CWE IDs
        cwe_ids_set = set()
        for vuln in group:
            cwe_ids_set.update(vuln.cwe_ids)

        # Find earliest published date
        published = None
        for vuln in group:
            if vuln.published:
                if published is None or vuln.published < published:
                    published = vuln.published

        # Find latest modified date
        modified = None
        for vuln in group:
            if vuln.modified:
                if modified is None or vuln.modified > modified:
                    modified = vuln.modified

        # Find longest description
        description = base.description
        for vuln in group:
            if vuln.description and (
                description is None or len(vuln.description) > len(description)
            ):
                description = vuln.description

        # Combine all additional scores (exclude primary severity)
        additional_scores = []
        for vuln in group:
            if vuln.severity and vuln.severity != base.severity:
                additional_scores.append(vuln.severity)
            additional_scores.extend(vuln.additional_scores)

        # Determine source
        sources = set(v.source for v in group)
        source = base.source if len(sources) == 1 else VulnerabilitySource.UNKNOWN

        # Create merged vulnerability
        merged = replace(
            base,
            id=identifier,
            source=source,
            description=description,
            aliases=sorted(list(all_aliases)),
            affected_versions=affected_versions,
            additional_scores=additional_scores,
            references=references,
            published=published,
            modified=modified,
            cwe_ids=sorted(list(cwe_ids_set)),
            raw_data=None,  # Exclude raw data from merged vulnerability
        )

        return merged
