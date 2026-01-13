"""
clarity-gate - Pre-ingestion verification for epistemic quality in RAG systems.

Implements:
- CGD_FORMAT.md v1.2 (25 validation rules)
- SOT_FORMAT.md v1.2 (7 validation rules)
- VALIDATOR_REFERENCE.md v1.2
"""

from typing import Literal

from .types import (
    ValidationResult,
    ValidationError,
    ValidateOptions,
    ComputedFields,
    DocumentType,
    ClarityStatus,
    HITLStatus,
    Severity,
    CGDFrontmatter,
    HITLClaim,
    ExclusionBlock,
    SOTMetadata,
    StructuredClaim,
)
from .validators import validate_cgd, validate_sot
from .compute import compute_body_hash, compute_rag_ingestable
from .parser import (
    extract_frontmatter,
    parse_yaml,
    find_end_marker,
    parse_exclusion_blocks,
    normalize_unicode,
    preprocess_content,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Types
    "ValidationResult",
    "ValidationError",
    "ValidateOptions",
    "ComputedFields",
    "DocumentType",
    "ClarityStatus",
    "HITLStatus",
    "Severity",
    "CGDFrontmatter",
    "HITLClaim",
    "ExclusionBlock",
    "SOTMetadata",
    "StructuredClaim",
    # Validators
    "validate",
    "validate_cgd",
    "validate_sot",
    "detect_type",
    # Compute
    "compute_body_hash",
    "compute_rag_ingestable",
    # Parser (advanced usage)
    "extract_frontmatter",
    "parse_yaml",
    "find_end_marker",
    "parse_exclusion_blocks",
    "normalize_unicode",
    "preprocess_content",
]


def detect_type(content: str) -> DocumentType:
    """
    Detect document type from content.

    - CGD: Has YAML frontmatter with clarity-gate-version field
    - SOT: H1 title contains "-- Source of Truth"
    - unknown: Neither pattern matched
    """
    normalized = preprocess_content(content)

    # Check for CGD (YAML frontmatter with clarity-gate-version)
    if normalized.startswith("---\n") or normalized.startswith("---\r"):
        lines = normalized.split("\n")
        in_frontmatter = True

        for i in range(1, len(lines)):
            line = lines[i].strip()

            if line == "---":
                in_frontmatter = False
                break

            if line.startswith("clarity-gate-version:"):
                return "cgd"

            if not in_frontmatter:
                break

    # Check for SOT (H1 with "-- Source of Truth")
    normalized_content = normalize_unicode(normalized)
    import re

    title_match = re.search(r"^#\s+(.+)$", normalized_content, re.MULTILINE)

    if title_match and "-- Source of Truth" in title_match.group(1):
        return "sot"

    return "unknown"


def validate(content: str, options: ValidateOptions = None) -> ValidationResult:
    """
    Auto-detect document type and validate.

    Args:
        content: Document content as string
        options: Validation options

    Returns:
        Validation result with errors, warnings, and computed fields

    Example:
        >>> from clarity_gate import validate
        >>>
        >>> result = validate(document_content)
        >>>
        >>> if result.valid:
        ...     print('Document is valid')
        ...     print('RAG ingestable:', result.computed.rag_ingestable)
        ... else:
        ...     print('Errors:', result.errors)
    """
    if options is None:
        options = ValidateOptions()

    doc_type = detect_type(content)

    if doc_type == "cgd":
        return validate_cgd(content, options)

    if doc_type == "sot":
        return validate_sot(content, options)

    return ValidationResult(
        valid=False,
        document_type="unknown",
        errors=[
            ValidationError(
                code="E0",
                severity="error",
                message='Unable to detect document type. Expected CGD (YAML frontmatter with clarity-gate-version) or SOT (H1 with "-- Source of Truth")',
            )
        ],
        warnings=[],
    )