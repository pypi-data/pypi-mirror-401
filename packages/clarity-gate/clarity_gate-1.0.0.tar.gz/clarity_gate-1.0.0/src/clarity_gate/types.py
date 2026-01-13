"""
Type definitions for clarity-gate validator.
Implements v1.2 specification.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Literal


# Type aliases
ClarityStatus = Literal["CLEAR", "UNCLEAR"]
HITLStatus = Literal["PENDING", "REVIEWED", "REVIEWED_WITH_EXCEPTIONS"]
DocumentType = Literal["cgd", "sot", "unknown"]
Severity = Literal["error", "warn"]


@dataclass
class ValidationError:
    """A validation error or warning."""

    code: str  # S1, C0, C12a, etc.
    severity: Severity
    message: str
    line: Optional[int] = None
    column: Optional[int] = None


@dataclass
class ComputedFields:
    """Computed fields from validation."""

    rag_ingestable: bool
    body_hash: Optional[str] = None
    exclusions_coverage: Optional[float] = None


@dataclass
class ValidationResult:
    """Result of document validation."""

    valid: bool
    document_type: DocumentType
    errors: List[ValidationError]
    warnings: List[ValidationError]
    computed: Optional[ComputedFields] = None
    metadata: Optional[dict] = None


@dataclass
class ValidateOptions:
    """Options for validation."""

    strict: bool = False  # Treat warnings as errors
    compute_hash: bool = False  # Compute body-sha256


@dataclass
class HITLClaim:
    """A HITL claim entry."""

    claim: str
    confirmed_by: Optional[str] = None
    date: Optional[str] = None


@dataclass
class CGDFrontmatter:
    """Parsed CGD frontmatter."""

    clarity_gate_version: str
    processed_date: str
    processed_by: str
    clarity_status: ClarityStatus
    hitl_status: HITLStatus
    hitl_pending_count: int
    points_passed: str
    hitl_claims: List[HITLClaim]
    # Optional fields
    body_sha256: Optional[str] = None
    rag_ingestable: Optional[bool] = None
    exclusions_coverage: Optional[float] = None
    exceptions_reason: Optional[str] = None
    exceptions_ids: Optional[List[str]] = None


@dataclass
class ExclusionBlock:
    """A parsed exclusion block."""

    id: str
    begin_line: int
    end_line: int
    begin_offset: int
    end_offset: int


@dataclass
class EndMarker:
    """Parsed end marker."""

    clarity: str
    hitl: str
    line: int
    separator_line: int


@dataclass
class CGDParseResult:
    """Result of parsing a CGD document."""

    frontmatter: Optional[CGDFrontmatter]
    frontmatter_raw: Optional[str]
    frontmatter_end_line: int
    body: str
    body_start_line: int
    end_marker: Optional[EndMarker]
    exclusion_blocks: List[ExclusionBlock]
    parse_errors: List[ValidationError]


@dataclass
class SOTMetadata:
    """Parsed SOT metadata."""

    title: str
    last_updated: str
    owner: str
    status: Literal["ASSESSED", "UNASSESSED"]
    version: str


@dataclass
class StructuredClaim:
    """A structured claim in an SOT document."""

    type: Literal["table-row", "bullet"]
    line: int
    section: Literal["verified", "estimates", "unknown"]
    content: str
    is_assessed: bool
    assessment_reason: Optional[str] = None


@dataclass
class FrontmatterExtraction:
    """Result of frontmatter extraction."""

    frontmatter: str
    body_start: int  # Line number (1-indexed)
    body_start_offset: int  # Character offset


@dataclass
class PointsPassedResult:
    """Result of points-passed validation."""

    valid: bool
    points: List[int]
    error: Optional[str] = None