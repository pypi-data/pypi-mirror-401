"""
Ecosystem mapping utility for vulnerability scanning.

This module provides functions to normalize and map ecosystem names across
different vulnerability databases (OSV, NVD, GitHub).

Different vulnerability databases use different ecosystem naming conventions:
- OSV: "npm", "PyPI", "Maven", "Go", "RubyGems"
- GitHub: "NPM", "PIP", "MAVEN", "GO", "GEM"
- Common variants: "pypi", "pip", "python", "npm", "node", etc.

This module provides bidirectional mapping to support all common variants.
"""

import logging
from typing import Dict, Optional


logger = logging.getLogger(__name__)


# ============================================================================
# Ecosystem Mapping Constants
# ============================================================================


# Canonical ecosystem names (OSV standard - most widely used)
CANONICAL_ECOSYSTEMS = {
    "npm",  # JavaScript/Node.js
    "PyPI",  # Python
    "Maven",  # Java
    "Go",  # Go modules
    "RubyGems",  # Ruby
    "Cargo",  # Rust (crates.io)
    "Hex",  # Elixir
    "Pub",  # Dart
    "Composer",  # PHP
    "NuGet",  # .NET
    "CRAN",  # R
    "Linux",  # Linux kernel
    "Debian",  # Debian packages
    "Alpine",  # Alpine Linux
    "OSS-Fuzz",  # Google OSS-Fuzz projects
}


# Mapping from common ecosystem name variants to canonical names
_ECOSYSTEM_ALIASES: Dict[str, str] = {
    # JavaScript/Node.js
    "npm": "npm",
    "NPM": "npm",
    "node": "npm",
    "Node": "npm",
    "NODE": "npm",
    "nodejs": "npm",
    "NodeJS": "npm",
    "NODEJS": "npm",
    # Python
    "PyPI": "PyPI",
    "pypi": "PyPI",
    "PIP": "PyPI",
    "pip": "PyPI",
    "python": "PyPI",
    "Python": "PyPI",
    "PYTHON": "PyPI",
    # Java
    "Maven": "Maven",
    "MAVEN": "Maven",
    "maven": "Maven",
    "java": "Maven",
    "Java": "Maven",
    "JAVA": "Maven",
    # Go
    "Go": "Go",
    "go": "Go",
    "GO": "Go",
    "golang": "Go",
    "Golang": "Go",
    "GOLANG": "Go",
    # Ruby
    "RubyGems": "RubyGems",
    "rubygems": "RubyGems",
    "RUBYGEMS": "RubyGems",
    "gem": "RubyGems",
    "Gem": "RubyGems",
    "GEM": "RubyGems",
    "ruby": "RubyGems",
    "Ruby": "RubyGems",
    "RUBY": "RubyGems",
    # Rust
    "Cargo": "Cargo",
    "cargo": "Cargo",
    "CARGO": "Cargo",
    "rust": "Cargo",
    "Rust": "Cargo",
    "RUST": "Cargo",
    "crates": "Cargo",
    "Crates": "Cargo",
    "CRATES": "Cargo",
    "crates.io": "Cargo",
    # Elixir
    "Hex": "Hex",
    "hex": "Hex",
    "HEX": "Hex",
    "elixir": "Hex",
    "Elixir": "Hex",
    "ELIXIR": "Hex",
    # Dart
    "Pub": "Pub",
    "pub": "Pub",
    "PUB": "Pub",
    "dart": "Pub",
    "Dart": "Pub",
    "DART": "Pub",
    # PHP
    "Composer": "Composer",
    "composer": "Composer",
    "COMPOSER": "Composer",
    "php": "Composer",
    "PHP": "Composer",
    "packagist": "Composer",
    "Packagist": "Composer",
    # .NET
    "NuGet": "NuGet",
    "nuget": "NuGet",
    "NUGET": "NuGet",
    "dotnet": "NuGet",
    "DotNet": "NuGet",
    "DOTNET": "NuGet",
    ".NET": "NuGet",
    # R
    "CRAN": "CRAN",
    "cran": "CRAN",
    "r": "CRAN",
    "R": "CRAN",
    # Linux
    "Linux": "Linux",
    "linux": "Linux",
    "LINUX": "Linux",
    "kernel": "Linux",
    # Debian
    "Debian": "Debian",
    "debian": "Debian",
    "DEBIAN": "Debian",
    # Alpine
    "Alpine": "Alpine",
    "alpine": "Alpine",
    "ALPINE": "Alpine",
    # OSS-Fuzz
    "OSS-Fuzz": "OSS-Fuzz",
    "oss-fuzz": "OSS-Fuzz",
    "OSS_Fuzz": "OSS-Fuzz",
    "oss_fuzz": "OSS-Fuzz",
}


# Mapping from canonical names to GitHub ecosystem names
_CANONICAL_TO_GITHUB: Dict[str, str] = {
    "npm": "NPM",
    "PyPI": "PIP",
    "Maven": "MAVEN",
    "Go": "GO",
    "RubyGems": "GEM",
    "Cargo": "CARGO",
    "Hex": "HEX",
    "Pub": "PUB",
    "Composer": "COMPOSER",
    "NuGet": "NUGET",
}


# Reverse mapping from GitHub names to canonical
_GITHUB_TO_CANONICAL: Dict[str, str] = {
    v: k for k, v in _CANONICAL_TO_GITHUB.items()
}


# ============================================================================
# Public API
# ============================================================================


def normalize_ecosystem(ecosystem: str) -> str:
    """
    Normalize ecosystem name to canonical form.

    Converts any common ecosystem name variant to the canonical OSV-style name.
    If the ecosystem is not recognized, it is returned as-is (case-normalized).

    Args:
        ecosystem: Ecosystem name in any variant (e.g., "npm", "NPM", "pypi", "PyPI")

    Returns:
        Canonical ecosystem name (e.g., "npm", "PyPI", "Maven")

    Examples:
        >>> normalize_ecosystem("npm")
        'npm'
        >>> normalize_ecosystem("NPM")
        'npm'
        >>> normalize_ecosystem("pypi")
        'PyPI'
        >>> normalize_ecosystem("PIP")
        'PyPI'
        >>> normalize_ecosystem("python")
        'PyPI'
        >>> normalize_ecosystem("MAVEN")
        'Maven'
        >>> normalize_ecosystem("golang")
        'Go'
        >>> normalize_ecosystem("rubygems")
        'RubyGems'
        >>> normalize_ecosystem("unknown-ecosystem")
        'unknown-ecosystem'
    """
    if not ecosystem:
        return ecosystem

    # Look up in aliases mapping
    canonical = _ECOSYSTEM_ALIASES.get(ecosystem)

    if canonical:
        logger.debug(f"Normalized ecosystem '{ecosystem}' -> '{canonical}'")
        return canonical

    # If not found, return as-is but log warning
    logger.debug(
        f"Ecosystem '{ecosystem}' not found in mapping, returning as-is"
    )
    return ecosystem


def to_github_ecosystem(ecosystem: str) -> str:
    """
    Convert canonical ecosystem name to GitHub ecosystem name.

    Args:
        ecosystem: Canonical ecosystem name (e.g., "npm", "PyPI", "Maven")

    Returns:
        GitHub ecosystem name (e.g., "NPM", "PIP", "MAVEN")
        Returns original ecosystem if no mapping exists

    Examples:
        >>> to_github_ecosystem("npm")
        'NPM'
        >>> to_github_ecosystem("PyPI")
        'PIP'
        >>> to_github_ecosystem("Maven")
        'MAVEN'
        >>> to_github_ecosystem("Go")
        'GO'
        >>> to_github_ecosystem("RubyGems")
        'GEM'
        >>> to_github_ecosystem("unknown")
        'unknown'
    """
    # First normalize to canonical form
    canonical = normalize_ecosystem(ecosystem)

    # Then map to GitHub format
    github_name = _CANONICAL_TO_GITHUB.get(canonical)

    if github_name:
        logger.debug(f"Mapped '{canonical}' -> GitHub ecosystem '{github_name}'")
        return github_name

    # If not found, return canonical name
    logger.debug(
        f"No GitHub mapping for '{canonical}', returning as-is"
    )
    return canonical


def from_github_ecosystem(ecosystem: str) -> str:
    """
    Convert GitHub ecosystem name to canonical ecosystem name.

    Args:
        ecosystem: GitHub ecosystem name (e.g., "NPM", "PIP", "MAVEN")

    Returns:
        Canonical ecosystem name (e.g., "npm", "PyPI", "Maven")
        Returns original ecosystem if no mapping exists

    Examples:
        >>> from_github_ecosystem("NPM")
        'npm'
        >>> from_github_ecosystem("PIP")
        'PyPI'
        >>> from_github_ecosystem("MAVEN")
        'Maven'
        >>> from_github_ecosystem("GO")
        'Go'
        >>> from_github_ecosystem("GEM")
        'RubyGems'
        >>> from_github_ecosystem("UNKNOWN")
        'UNKNOWN'
    """
    # Look up in reverse mapping
    canonical = _GITHUB_TO_CANONICAL.get(ecosystem)

    if canonical:
        logger.debug(f"Mapped GitHub '{ecosystem}' -> canonical '{canonical}'")
        return canonical

    # If not found, try normalizing (might be a variant)
    normalized = normalize_ecosystem(ecosystem)

    if normalized != ecosystem:
        logger.debug(
            f"No direct GitHub mapping for '{ecosystem}', "
            f"normalized to '{normalized}'"
        )
        return normalized

    # Return as-is
    logger.debug(f"No canonical mapping for GitHub ecosystem '{ecosystem}', returning as-is")
    return ecosystem


def is_supported_by_github(ecosystem: str) -> bool:
    """
    Check if ecosystem is supported by GitHub Security Advisories.

    Args:
        ecosystem: Ecosystem name in any format

    Returns:
        True if ecosystem is supported by GitHub, False otherwise

    Examples:
        >>> is_supported_by_github("npm")
        True
        >>> is_supported_by_github("PyPI")
        True
        >>> is_supported_by_github("Maven")
        True
        >>> is_supported_by_github("Go")
        True
        >>> is_supported_by_github("RubyGems")
        True
        >>> is_supported_by_github("CRAN")
        False
        >>> is_supported_by_github("Linux")
        False
    """
    # Normalize and map to GitHub format
    github_ecosystem = to_github_ecosystem(ecosystem)

    # Check if it's in GitHub's supported ecosystems
    # (GitHub supports: NPM, PIP, MAVEN, GEM, GO, NUGET, COMPOSER, PUB)
    return github_ecosystem in {
        "NPM", "PIP", "MAVEN", "GEM", "GO", "NUGET", "COMPOSER", "PUB", "CARGO", "HEX"
    }


def is_supported_by_osv(ecosystem: str) -> bool:
    """
    Check if ecosystem is supported by OSV.

    Args:
        ecosystem: Ecosystem name in any format

    Returns:
        True if ecosystem is supported by OSV, False otherwise

    Examples:
        >>> is_supported_by_osv("npm")
        True
        >>> is_supported_by_osv("PyPI")
        True
        >>> is_supported_by_osv("Maven")
        True
        >>> is_supported_by_osv("Go")
        True
        >>> is_supported_by_osv("RubyGems")
        True
        >>> is_supported_by_osv("CRAN")
        True
        >>> is_supported_by_osv("Linux")
        True
    """
    # Normalize to canonical form
    canonical = normalize_ecosystem(ecosystem)
    return canonical in CANONICAL_ECOSYSTEMS
