"""Parser module exports."""

from .normalize import (
    normalize_unicode,
    normalize_line_endings,
    remove_bom,
    preprocess_content,
)
from .yaml_parser import (
    extract_frontmatter,
    parse_yaml,
    validate_frontmatter_schema,
)
from .end_marker import (
    find_end_marker,
    validate_end_marker,
    check_end_marker_consistency,
)
from .exclusions import (
    parse_exclusion_blocks,
    calculate_exclusion_bytes,
    calculate_exclusions_coverage,
    validate_exception_ids,
)

__all__ = [
    "normalize_unicode",
    "normalize_line_endings",
    "remove_bom",
    "preprocess_content",
    "extract_frontmatter",
    "parse_yaml",
    "validate_frontmatter_schema",
    "find_end_marker",
    "validate_end_marker",
    "check_end_marker_consistency",
    "parse_exclusion_blocks",
    "calculate_exclusion_bytes",
    "calculate_exclusions_coverage",
    "validate_exception_ids",
]