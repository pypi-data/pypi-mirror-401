"""
CGD (Clarity-Gated Document) Validator.
Implements rules C0-C21 per VALIDATOR_REFERENCE.md.
"""

import re
from datetime import datetime
from typing import List, Tuple

from ..types import (
    ValidationResult,
    ValidationError,
    CGDFrontmatter,
    CGDParseResult,
    ValidateOptions,
    ComputedFields,
    PointsPassedResult,
)
from ..parser import (
    preprocess_content,
    extract_frontmatter,
    parse_yaml,
    validate_frontmatter_schema,
    find_end_marker,
    validate_end_marker,
    check_end_marker_consistency,
    parse_exclusion_blocks,
    calculate_exclusions_coverage,
    validate_exception_ids,
)
from ..compute import compute_body_hash, compute_rag_ingestable_with_version


def parse_cgd(content: str) -> CGDParseResult:
    """Parse a CGD document into structured components."""
    errors: List[ValidationError] = []
    normalized = preprocess_content(content)

    # Extract frontmatter
    extraction = extract_frontmatter(normalized)

    if not extraction:
        # C1: Missing frontmatter
        if not normalized.startswith("---"):
            errors.append(
                ValidationError(
                    code="C1",
                    severity="error",
                    message="Missing YAML frontmatter (file must start with ---)",
                    line=1,
                )
            )
        else:
            errors.append(
                ValidationError(
                    code="C1",
                    severity="error",
                    message="Unclosed YAML frontmatter (missing closing ---)",
                    line=1,
                )
            )

        return CGDParseResult(
            frontmatter=None,
            frontmatter_raw=None,
            frontmatter_end_line=0,
            body=normalized,
            body_start_line=1,
            end_marker=None,
            exclusion_blocks=[],
            parse_errors=errors,
        )

    # Parse YAML
    yaml_data, yaml_error = parse_yaml(extraction.frontmatter)

    if yaml_error or not yaml_data:
        # C0: YAML syntax error
        errors.append(
            ValidationError(
                code="C0",
                severity="error",
                message=f"YAML syntax error: {yaml_error or 'unknown error'}",
                line=1,
            )
        )

        return CGDParseResult(
            frontmatter=None,
            frontmatter_raw=extraction.frontmatter,
            frontmatter_end_line=extraction.body_start - 1,
            body=normalized[extraction.body_start_offset :],
            body_start_line=extraction.body_start,
            end_marker=None,
            exclusion_blocks=[],
            parse_errors=errors,
        )

    # Validate frontmatter schema (C2 errors)
    frontmatter, schema_errors = validate_frontmatter_schema(yaml_data)
    errors.extend(schema_errors)

    # Extract body
    body = normalized[extraction.body_start_offset :]

    # Find end marker
    end_marker = find_end_marker(normalized)

    # Parse exclusion blocks (from body only)
    exclusion_blocks, exclusion_errors = parse_exclusion_blocks(body, extraction.body_start)
    errors.extend(exclusion_errors)

    return CGDParseResult(
        frontmatter=frontmatter,
        frontmatter_raw=extraction.frontmatter,
        frontmatter_end_line=extraction.body_start - 1,
        body=body,
        body_start_line=extraction.body_start,
        end_marker=end_marker,
        exclusion_blocks=exclusion_blocks,
        parse_errors=errors,
    )


def validate_points_passed(value: str) -> PointsPassedResult:
    """
    Validate points-passed field format.
    Valid: "1-9", "1,3,5", "1-4,7,9", individual numbers 1-9
    """
    points: set = set()
    parts = [p.strip() for p in value.split(",")]

    for part in parts:
        if part == "":
            return PointsPassedResult(
                valid=False, points=[], error="Empty item in points-passed list"
            )

        # Check for range (e.g., "1-4")
        if "-" in part:
            range_parts = [p.strip() for p in part.split("-")]
            if len(range_parts) != 2:
                return PointsPassedResult(
                    valid=False, points=[], error=f'Invalid range format: "{part}"'
                )

            try:
                start = int(range_parts[0])
                end = int(range_parts[1])
            except ValueError:
                return PointsPassedResult(
                    valid=False, points=[], error=f'Non-numeric range: "{part}"'
                )

            if start > end:
                return PointsPassedResult(
                    valid=False, points=[], error=f'Inverted range: "{part}"'
                )

            if start < 1 or end > 9:
                return PointsPassedResult(
                    valid=False, points=[], error=f'Range out of bounds (1-9): "{part}"'
                )

            for i in range(start, end + 1):
                points.add(i)
        else:
            # Single number
            try:
                num = int(part)
            except ValueError:
                return PointsPassedResult(
                    valid=False, points=[], error=f'Non-numeric value: "{part}"'
                )

            if num < 1 or num > 9:
                return PointsPassedResult(
                    valid=False, points=[], error=f"Point out of range (1-9): {num}"
                )

            points.add(num)

    return PointsPassedResult(valid=True, points=sorted(points))


def validate_cgd(content: str, options: ValidateOptions = None) -> ValidationResult:
    """
    Validate CGD document.
    Implements all 26 CGD rules: C0-C21 (with C12 split into C12a-C12d).
    """
    if options is None:
        options = ValidateOptions()

    errors: List[ValidationError] = []
    warnings: List[ValidationError] = []

    # BUG-026: Handle empty/whitespace-only documents gracefully
    if not content or not content.strip():
        return ValidationResult(
            valid=False,
            document_type="cgd",
            errors=[ValidationError(
                code="C1",
                severity="error",
                message="Empty document",
                line=1,
            )],
            warnings=[],
        )

    # Parse document
    parsed = parse_cgd(content)

    # Add parse errors
    for err in parsed.parse_errors:
        if err.severity == "error":
            errors.append(err)
        else:
            warnings.append(err)

    # If no frontmatter, we can't continue with most validation
    if not parsed.frontmatter:
        return ValidationResult(
            valid=False,
            document_type="cgd",
            errors=errors,
            warnings=warnings,
        )

    fm = parsed.frontmatter

    # C6: Validate clarity-status and hitl-status enum values
    VALID_CLARITY_STATUS = ["CLEAR", "UNCLEAR"]
    VALID_HITL_STATUS = ["PENDING", "REVIEWED", "REVIEWED_WITH_EXCEPTIONS"]

    if fm.clarity_status not in VALID_CLARITY_STATUS:
        errors.append(
            ValidationError(
                code="C6",
                severity="error",
                message=f'Invalid clarity-status: "{fm.clarity_status}". Must be CLEAR or UNCLEAR.',
            )
        )

    if fm.hitl_status not in VALID_HITL_STATUS:
        errors.append(
            ValidationError(
                code="C6",
                severity="error",
                message=f'Invalid hitl-status: "{fm.hitl_status}". Must be PENDING, REVIEWED, or REVIEWED_WITH_EXCEPTIONS.',
            )
        )

    # C3: processed-date format and calendar validation (per spec §4.5: compare in UTC)
    DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    if not DATE_REGEX.match(fm.processed_date):
        errors.append(
            ValidationError(
                code="C3",
                severity="error",
                message=f'processed-date must be YYYY-MM-DD format, got "{fm.processed_date}"',
            )
        )
    else:
        try:
            # Validate actual calendar date (not just bounds) - catches Feb 30, Apr 31, etc.
            datetime.strptime(fm.processed_date, "%Y-%m-%d")

            # Check if date is in the future
            from datetime import timezone
            year, month, day = map(int, fm.processed_date.split("-"))
            processed_date_utc = datetime(year, month, day)
            today_utc = datetime.now(timezone.utc).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            today_naive = today_utc.replace(tzinfo=None)

            if processed_date_utc > today_naive:
                errors.append(
                    ValidationError(
                        code="C3",
                        severity="error",
                        message=f"processed-date is in the future: {fm.processed_date}",
                    )
                )
        except ValueError:
            errors.append(
                ValidationError(
                    code="C3",
                    severity="error",
                    message=f"processed-date is not a valid calendar date: {fm.processed_date}",
                )
            )

    # C4: points-passed validation
    points_result = validate_points_passed(fm.points_passed)
    if not points_result.valid:
        errors.append(
            ValidationError(
                code="C4",
                severity="error",
                message=f"Invalid points-passed: {points_result.error}",
            )
        )

    # C5: Missing end marker
    if not parsed.end_marker:
        errors.append(
            ValidationError(
                code="C5",
                severity="error",
                message="Missing end marker (must end with --- followed by Clarity Gate: <status> | <hitl>)",
            )
        )
    else:
        # C6: End marker validation
        end_marker_errors = validate_end_marker(parsed.end_marker)
        errors.extend([e for e in end_marker_errors if e.code == "C6"])

        # Check consistency with frontmatter
        consistency_errors = check_end_marker_consistency(
            parsed.end_marker, fm.clarity_status, fm.hitl_status
        )
        errors.extend(consistency_errors)

        # C7 from end marker
        errors.extend([e for e in end_marker_errors if e.code == "C7"])

    # C7: UNCLEAR with hitl-status != PENDING (frontmatter check)
    if fm.clarity_status == "UNCLEAR" and fm.hitl_status != "PENDING":
        errors.append(
            ValidationError(
                code="C7",
                severity="error",
                message=f"Invalid state: clarity-status UNCLEAR requires hitl-status PENDING, got {fm.hitl_status}",
            )
        )

    # C8: PENDING but hitl-pending-count = 0
    if fm.hitl_status == "PENDING" and fm.hitl_pending_count == 0:
        errors.append(
            ValidationError(
                code="C8",
                severity="error",
                message="hitl-status is PENDING but hitl-pending-count is 0",
            )
        )

    # C9: REVIEWED but hitl-pending-count > 0
    if fm.hitl_status == "REVIEWED" and fm.hitl_pending_count > 0:
        errors.append(
            ValidationError(
                code="C9",
                severity="error",
                message=f"hitl-status is REVIEWED but hitl-pending-count is {fm.hitl_pending_count} (must be 0)",
            )
        )

    # C10: REVIEWED_WITH_EXCEPTIONS but hitl-pending-count > 0
    if fm.hitl_status == "REVIEWED_WITH_EXCEPTIONS" and fm.hitl_pending_count > 0:
        errors.append(
            ValidationError(
                code="C10",
                severity="error",
                message=f"hitl-status is REVIEWED_WITH_EXCEPTIONS but hitl-pending-count is {fm.hitl_pending_count} (must be 0)",
            )
        )

    # Consistency check: hitl-pending-count should match actual pending claims
    if fm.hitl_status == "PENDING" and fm.hitl_claims:
        pending_claims = [c for c in fm.hitl_claims if not c.confirmed_by]
        if len(pending_claims) != fm.hitl_pending_count:
            warnings.append(
                ValidationError(
                    code="C8",
                    severity="warn",
                    message=f"hitl-pending-count ({fm.hitl_pending_count}) doesn't match pending claims count ({len(pending_claims)})",
                )
            )

    # C11: REVIEWED_WITH_EXCEPTIONS but no exclusion blocks
    if fm.hitl_status == "REVIEWED_WITH_EXCEPTIONS" and len(parsed.exclusion_blocks) == 0:
        errors.append(
            ValidationError(
                code="C11",
                severity="error",
                message="hitl-status is REVIEWED_WITH_EXCEPTIONS but no exclusion blocks found",
            )
        )

    # C13: REVIEWED_WITH_EXCEPTIONS requires exceptions-reason and exceptions-ids
    if fm.hitl_status == "REVIEWED_WITH_EXCEPTIONS":
        if not fm.exceptions_reason:
            errors.append(
                ValidationError(
                    code="C13",
                    severity="error",
                    message="hitl-status REVIEWED_WITH_EXCEPTIONS requires exceptions-reason field",
                )
            )
        if not fm.exceptions_ids:
            errors.append(
                ValidationError(
                    code="C13",
                    severity="error",
                    message="hitl-status REVIEWED_WITH_EXCEPTIONS requires non-empty exceptions-ids field",
                )
            )

    # C14: Exclusion blocks without REVIEWED_WITH_EXCEPTIONS
    if parsed.exclusion_blocks and fm.hitl_status != "REVIEWED_WITH_EXCEPTIONS":
        errors.append(
            ValidationError(
                code="C14",
                severity="error",
                message=f"Document has {len(parsed.exclusion_blocks)} exclusion block(s) but hitl-status is {fm.hitl_status} (must be REVIEWED_WITH_EXCEPTIONS)",
            )
        )

    # C15: exceptions-ids references non-existent id
    if fm.exceptions_ids:
        id_errors = validate_exception_ids(parsed.exclusion_blocks, fm.exceptions_ids)
        errors.extend(id_errors)

    # C16: body-sha256 format validation
    if fm.body_sha256 is not None:
        hash_regex = re.compile(r"^[0-9a-f]{64}$")
        if not hash_regex.match(fm.body_sha256):
            errors.append(
                ValidationError(
                    code="C16",
                    severity="error",
                    message="body-sha256 malformed: must be 64 lowercase hex characters",
                )
            )

    # C17: body-sha256 mismatch (warning)
    computed_hash = compute_body_hash(content)
    if fm.body_sha256 is not None and fm.body_sha256 != computed_hash:
        warnings.append(
            ValidationError(
                code="C17",
                severity="warn",
                message=f"body-sha256 mismatch: declared {fm.body_sha256}, computed {computed_hash}",
            )
        )

    # C18: rag-ingestable not boolean
    if fm.rag_ingestable is not None and not isinstance(fm.rag_ingestable, bool):
        errors.append(
            ValidationError(
                code="C18",
                severity="error",
                message=f"rag-ingestable must be boolean, got {type(fm.rag_ingestable).__name__}",
            )
        )

    # Version forward compatibility check
    VERSION_REGEX = re.compile(r"^\d+\.\d+$")
    version = fm.clarity_gate_version
    major_version = 1

    if not isinstance(version, str) or not VERSION_REGEX.match(version):
        errors.append(
            ValidationError(
                code="C2",
                severity="error",
                message=f'clarity-gate-version must be X.Y format (e.g., "1.2"), got "{version}"',
            )
        )
    else:
        try:
            major_version = int(version.split(".")[0])
        except (ValueError, IndexError):
            major_version = 1

        if major_version > 1:
            warnings.append(
                ValidationError(
                    code="C22",
                    severity="warn",
                    message=f"Document uses clarity-gate-version {version} (validator is v1.x). Some features may not be validated.",
                )
            )

    # C19: rag-ingestable disagrees with computed
    computed_ingestable = compute_rag_ingestable_with_version(
        fm.clarity_status,
        fm.hitl_status,
        len(parsed.exclusion_blocks),
        major_version,
    )
    if fm.rag_ingestable is not None and fm.rag_ingestable != computed_ingestable:
        warnings.append(
            ValidationError(
                code="C19",
                severity="warn",
                message=f"rag-ingestable disagrees with computed value: declared {fm.rag_ingestable}, computed {computed_ingestable}",
            )
        )

    # C20: exclusions-coverage invalid
    if fm.exclusions_coverage is not None:
        if not isinstance(fm.exclusions_coverage, (int, float)) or not (
            0 <= fm.exclusions_coverage <= 1
        ):
            errors.append(
                ValidationError(
                    code="C20",
                    severity="error",
                    message=f"exclusions-coverage must be a number between 0 and 1, got {fm.exclusions_coverage}",
                )
            )

    # C21: exclusions-coverage >= 0.50 (warning)
    computed_coverage = calculate_exclusions_coverage(parsed.body, parsed.exclusion_blocks)
    if computed_coverage >= 0.50:
        warnings.append(
            ValidationError(
                code="C21",
                severity="warn",
                message=f"exclusions-coverage is {computed_coverage * 100:.1f}% (≥50% may indicate document should not be ingested)",
            )
        )

    # Deduplicate errors (e.g., C7 can be reported from both frontmatter and end marker)
    seen = set()
    unique_errors = []
    for err in errors:
        key = (err.code, err.message)
        if key not in seen:
            seen.add(key)
            unique_errors.append(err)

    # Build result
    valid = len(unique_errors) == 0
    if options.strict:
        valid = valid and len(warnings) == 0

    return ValidationResult(
        valid=valid,
        document_type="cgd",
        errors=unique_errors,
        warnings=warnings,
        computed=ComputedFields(
            rag_ingestable=computed_ingestable,
            body_hash=computed_hash,
            exclusions_coverage=computed_coverage,
        ),
        metadata={
            "clarity_gate_version": fm.clarity_gate_version,
            "clarity_status": fm.clarity_status,
            "hitl_status": fm.hitl_status,
        },
    )