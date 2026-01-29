"""
Metadata filtering module for Binary SBOM Generator.

This module provides filter configuration and filtering logic for controlling
which metadata categories are included in SPDX output. Filtering is applied
at the document generation stage without modifying the analyzer.
"""

from dataclasses import dataclass, field
from typing import Optional, Set


@dataclass
class FilterConfig:
    """
    Configuration for metadata filtering in SPDX document generation.

    This dataclass encapsulates filter settings based on CLI flags, controlling
    which metadata categories are included in the generated SPDX document.

    Attributes:
        mode: Filtering mode - 'include', 'exclude', 'minimal', or 'all'
            - 'include': Only include specified categories
            - 'exclude': Include all except specified categories
            - 'minimal': Include only basic_info (name, type, architecture, entrypoint)
            - 'all': Include all categories (default, no filtering)
        categories: Set of category names affected by the filter mode.
            Valid categories: 'basic_info', 'sections', 'dependencies'
        include_type: Whether to include 'type' field (computed from mode/categories)
        include_architecture: Whether to include 'architecture' field (computed)
        include_entrypoint: Whether to include 'entrypoint' field (computed)
        include_sections: Whether to include 'sections' field (computed)
        include_dependencies: Whether to include 'dependencies' field (computed)

    Example:
        >>> # Minimal output mode
        >>> config = FilterConfig(mode='minimal')
        >>> config.include_type  # True
        True
        >>> config.include_sections  # False
        False

        >>> # Include specific categories
        >>> config = FilterConfig(mode='include', categories={'basic_info', 'sections'})
        >>> config.include_dependencies  # False
        False
    """
    mode: str = 'all'
    categories: Set[str] = field(default_factory=set)

    # Granular field flags (computed from mode and categories)
    include_type: bool = True
    include_architecture: bool = True
    include_entrypoint: bool = True
    include_sections: bool = True
    include_dependencies: bool = True

    def __post_init__(self):
        """
        Compute granular inclusion flags from mode and categories.

        This method runs automatically after dataclass initialization to set
        the individual field inclusion flags based on the filtering mode and
        specified categories.
        """
        # Ensure categories is a set
        if not isinstance(self.categories, set):
            self.categories = set(self.categories)

        # Default: include all fields (mode='all' or no filtering)
        self.include_type = True
        self.include_architecture = True
        self.include_entrypoint = True
        self.include_sections = True
        self.include_dependencies = True

        # Apply mode-based filtering
        if self.mode == 'minimal':
            # Minimal mode: basic_info only (exclude sections and dependencies)
            self.include_sections = False
            self.include_dependencies = False

        elif self.mode == 'include':
            # Include mode: only specified categories
            if 'basic_info' not in self.categories:
                self.include_type = False
                self.include_architecture = False
                self.include_entrypoint = False
            if 'sections' not in self.categories:
                self.include_sections = False
            if 'dependencies' not in self.categories:
                self.include_dependencies = False

        elif self.mode == 'exclude':
            # Exclude mode: all except specified categories
            if 'basic_info' in self.categories:
                self.include_type = False
                self.include_architecture = False
                self.include_entrypoint = False
            if 'sections' in self.categories:
                self.include_sections = False
            if 'dependencies' in self.categories:
                self.include_dependencies = False

    def should_include_field(self, field_name: str) -> bool:
        """
        Check if a specific metadata field should be included.

        This method provides a convenient way to check field inclusion without
        accessing individual flags directly.

        Args:
            field_name: Name of the metadata field ('type', 'architecture',
                'entrypoint', 'sections', 'dependencies')

        Returns:
            True if the field should be included, False otherwise

        Raises:
            ValueError: If field_name is not a recognized field

        Example:
            >>> config = FilterConfig(mode='minimal')
            >>> config.should_include_field('type')
            True
            >>> config.should_include_field('sections')
            False
        """
        field_map = {
            'type': self.include_type,
            'architecture': self.include_architecture,
            'entrypoint': self.include_entrypoint,
            'sections': self.include_sections,
            'dependencies': self.include_dependencies,
        }

        if field_name not in field_map:
            raise ValueError(
                f"Unknown field: {field_name}. "
                f"Valid fields: {list(field_map.keys())}"
            )

        return field_map[field_name]


def create_filter_config(
    include_sections: Optional[str] = None,
    exclude_sections: Optional[str] = None,
    exclude_dependencies: bool = False,
    minimal_output: bool = False
) -> Optional[FilterConfig]:
    """
    Create a FilterConfig object from CLI flag values.

    This function converts validated CLI flag parameters into a FilterConfig
    object that can be passed to the SPDX document generator. All validation
    should be performed in the CLI before calling this function.

    Args:
        include_sections: Comma-separated list of categories to include.
            Valid values: basic_info, sections, dependencies.
            Example: "basic_info,sections"
        exclude_sections: Comma-separated list of categories to exclude.
            Valid values: basic_info, sections, dependencies.
            Example: "dependencies"
        exclude_dependencies: Boolean flag to exclude all dependency information.
            Equivalent to exclude_sections="dependencies".
        minimal_output: Boolean flag for minimal output (basic_info only).
            Equivalent to include_sections="basic_info".

    Returns:
        FilterConfig object with appropriate settings, or None if no filtering
        is requested (all flags are default values).

    Raises:
        ValueError: If invalid category names are provided (should be caught
            by CLI validation before calling this function).

    Example:
        >>> # Minimal output
        >>> config = create_filter_config(minimal_output=True)
        >>> config.mode
        'minimal'

        >>> # Include specific categories
        >>> config = create_filter_config(include_sections="basic_info,sections")
        >>> config.mode
        'include'
        >>> config.categories
        {'basic_info', 'sections'}

        >>> # No filtering (default)
        >>> config = create_filter_config()
        >>> config
        None
    """
    # Priority 1: Minimal output flag
    if minimal_output:
        return FilterConfig(
            mode='minimal',
            categories={'basic_info'}
        )

    # Priority 2: Exclude dependencies flag
    if exclude_dependencies:
        return FilterConfig(
            mode='exclude',
            categories={'dependencies'}
        )

    # Priority 3: Include sections flag
    if include_sections:
        categories = set(cat.strip() for cat in include_sections.split(','))
        return FilterConfig(
            mode='include',
            categories=categories
        )

    # Priority 4: Exclude sections flag
    if exclude_sections:
        categories = set(cat.strip() for cat in exclude_sections.split(','))
        return FilterConfig(
            mode='exclude',
            categories=categories
        )

    # No filtering requested
    return None


__all__ = [
    'FilterConfig',
    'create_filter_config',
]
