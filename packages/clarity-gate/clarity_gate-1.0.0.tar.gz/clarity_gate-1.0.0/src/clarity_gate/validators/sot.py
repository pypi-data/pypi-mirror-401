"""
SOT (Source of Truth) Document Validator.
Implements rules S1-S7 per VALIDATOR_REFERENCE.md.
"""

import re
from datetime import datetime
from typing import List, Optional, Dict, Tuple

from ..types import (
    ValidationResult,
    ValidationError,
    SOTMetadata,
    StructuredClaim,
    ValidateOptions,
)
from ..parser import preprocess_content, normalize_unicode


# Section headers for claim sections (case-sensitive per spec §3.2)
CLAIM_SECTION_HEADERS = {
    "verified": re.compile(r"^##\s+Verified\s+Data\s*$"),
    "estimates": re.compile(r"^##\s+Estimates\s+\(NOT\s+VERIFIED\)\s*$"),
    "unknown": re.compile(r"^##\s+Unknown\s+/\s+Data\s+Not\s+Available\s*$"),
}

VERIFICATION_STATUS_HEADER = re.compile(r"^##\s+Verification\s+Status\s*$")


def parse_sot(content: str) -> dict:
    """Parse SOT document structure."""
    errors: List[ValidationError] = []
    normalized = preprocess_content(content)
    lines = normalized.split("\n")

    metadata: Optional[SOTMetadata] = None
    title_line = 0
    verification_status_line: Optional[int] = None

    claim_sections: Dict[str, Optional[Dict[str, int]]] = {
        "verified": None,
        "estimates": None,
        "unknown": None,
    }

    structured_claims: List[StructuredClaim] = []
    prose_in_claim_sections: List[Dict[str, any]] = []

    # Find title (H1 with "-- Source of Truth")
    title = ""
    for i, line in enumerate(lines):
        normalized_line = normalize_unicode(line)
        if normalized_line.startswith("# "):
            title_line = i + 1
            title = normalized_line[2:].strip()
            break

    # Parse metadata block (after title, before first ## section)
    metadata_start = title_line
    metadata_end = len(lines)

    for i in range(title_line, len(lines)):
        if lines[i].startswith("## "):
            metadata_end = i
            break

    # Extract metadata fields
    metadata_lines = lines[metadata_start:metadata_end]
    metadata_fields: Dict[str, str] = {}

    for line in metadata_lines:
        normalized_line = normalize_unicode(line)
        # Match **Field:** value pattern
        match = re.match(r"^\*\*([^*]+):\*\*\s*(.*)$", normalized_line)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            metadata_fields[key] = value

    if all(
        field in metadata_fields
        for field in ["Last Updated", "Owner", "Status", "Version"]
    ):
        metadata = SOTMetadata(
            title=title,
            last_updated=metadata_fields["Last Updated"],
            owner=metadata_fields["Owner"],
            status=metadata_fields["Status"],  # type: ignore
            version=metadata_fields["Version"],
        )

    # Find sections
    current_section: Optional[str] = None
    current_section_start = 0

    for i, line in enumerate(lines):
        line_num = i + 1

        # Check for Verification Status section
        if VERIFICATION_STATUS_HEADER.match(line):
            verification_status_line = line_num
            # Close previous section
            if current_section and current_section != "verification" and claim_sections.get(current_section):
                claim_sections[current_section]["end_line"] = line_num - 1
            current_section = "verification"
            current_section_start = line_num
            continue

        # Check for claim sections
        for section_key, pattern in CLAIM_SECTION_HEADERS.items():
            if pattern.match(line):
                # Close previous section
                if current_section and current_section != "verification" and claim_sections.get(current_section):
                    claim_sections[current_section]["end_line"] = line_num - 1

                current_section = section_key
                current_section_start = line_num
                claim_sections[section_key] = {
                    "start_line": line_num,
                    "end_line": len(lines),  # Will be updated when next section found
                }
                break

        # Check for other H2 sections (close current claim section)
        if line.startswith("## ") and current_section and current_section != "verification":
            is_claim_section = any(p.match(line) for p in CLAIM_SECTION_HEADERS.values())
            if not is_claim_section and claim_sections.get(current_section):
                claim_sections[current_section]["end_line"] = line_num - 1
                current_section = None

        # Parse structured claims in claim sections
        if current_section and current_section != "verification" and current_section in claim_sections:
            section = current_section

            # Table row (starts with |)
            if line.strip().startswith("|") and "---" not in line:
                # Skip header separator rows
                cells = [c.strip() for c in line.split("|") if c.strip()]
                if cells and not all(re.match(r"^[-:]+$", c) for c in cells):
                    structured_claims.append(
                        StructuredClaim(
                            type="table-row",
                            line=line_num,
                            section=section,  # type: ignore
                            content=line.strip(),
                            is_assessed=section == "verified",
                        )
                    )
            # Bullet point (starts with -, *, or +)
            elif re.match(r"^\s*[-*+]\s+", line):
                structured_claims.append(
                    StructuredClaim(
                        type="bullet",
                        line=line_num,
                        section=section,  # type: ignore
                        content=line.strip(),
                        is_assessed=section == "verified",
                    )
                )
            # Numbered list (starts with digit(s) followed by . or ))
            elif re.match(r"^\s*\d+[.)]\s+", line):
                structured_claims.append(
                    StructuredClaim(
                        type="bullet",
                        line=line_num,
                        section=section,  # type: ignore
                        content=line.strip(),
                        is_assessed=section == "verified",
                    )
                )
            # Prose detection (non-empty, non-header, non-table, non-bullet)
            elif (
                line.strip()
                and not line.startswith("#")
                and not line.startswith("|")
                and not line.startswith("```")
            ):
                # Skip if it looks like metadata or is primarily a link
                trimmed = line.strip()
                # Use non-greedy regex to prevent ReDoS (BUG-037)
                is_link = bool(re.match(r"^\[[^\]]+\]\([^)]+\)$", trimmed)) or trimmed.startswith("http://") or trimmed.startswith("https://")
                if not trimmed.startswith("**") and not trimmed.startswith(">") and not is_link:
                    prose_in_claim_sections.append(
                        {"line": line_num, "content": trimmed}
                    )

    return {
        "metadata": metadata,
        "title_line": title_line,
        "verification_status_line": verification_status_line,
        "claim_sections": claim_sections,
        "structured_claims": structured_claims,
        "prose_in_claim_sections": prose_in_claim_sections,
        "parse_errors": errors,
    }


def validate_sot(content: str, options: ValidateOptions = None) -> ValidationResult:
    """
    Validate SOT document.
    Implements rules S1-S7.
    """
    if options is None:
        options = ValidateOptions()

    errors: List[ValidationError] = []
    warnings: List[ValidationError] = []

    parsed = parse_sot(content)
    normalized = preprocess_content(content)
    normalized_content = normalize_unicode(normalized)

    # S1: Missing "-- Source of Truth" in H1 title
    # Per spec §SOT-003/EDGE-004: Accept both "--" and "-" (em dash normalizes to single hyphen)
    title_match = re.search(r"^#\s+(.+)$", normalized_content, re.MULTILINE)
    if not title_match:
        errors.append(
            ValidationError(
                code="S1",
                severity="error",
                message="Missing H1 title",
                line=1,
            )
        )
    elif "-- Source of Truth" not in title_match.group(1) and "- Source of Truth" not in title_match.group(1):
        errors.append(
            ValidationError(
                code="S1",
                severity="error",
                message='H1 title must contain "-- Source of Truth"',
                line=parsed["title_line"],
            )
        )

    # S2: Missing required metadata
    required_metadata = ["Last Updated", "Owner", "Status", "Version"]
    if not parsed["metadata"]:
        # Find which fields are missing
        found_fields: set = set()
        for line in normalized.split("\n"):
            normalized_line = normalize_unicode(line)
            match = re.match(r"^\*\*([^*]+):\*\*", normalized_line)
            if match:
                found_fields.add(match.group(1).strip())

        for field in required_metadata:
            if field not in found_fields:
                errors.append(
                    ValidationError(
                        code="S2",
                        severity="error",
                        message=f"Missing required metadata: **{field}:**",
                    )
                )

    # S2 (extended): Status must be ASSESSED or UNASSESSED
    VALID_SOT_STATUS = ["ASSESSED", "UNASSESSED"]
    if parsed["metadata"] and parsed["metadata"].status not in VALID_SOT_STATUS:
        errors.append(
            ValidationError(
                code="S2",
                severity="error",
                message=f'Invalid Status: "{parsed["metadata"].status}". Must be ASSESSED or UNASSESSED.',
            )
        )

    # S3: Missing Verification Status section
    if not parsed["verification_status_line"]:
        errors.append(
            ValidationError(
                code="S3",
                severity="error",
                message='Missing "## Verification Status" section',
            )
        )

    # S4: Status ASSESSED but structured claim lacks required signals
    if parsed["metadata"] and parsed["metadata"].status == "ASSESSED":
        verified_claims = [c for c in parsed["structured_claims"] if c.section == "verified"]
        if not verified_claims and parsed["claim_sections"].get("verified"):
            errors.append(
                ValidationError(
                    code="S4",
                    severity="error",
                    message="Status is ASSESSED but no structured claims found in Verified Data section",
                )
            )

    # S5: Last Updated date format and calendar validation (per spec §4.5: compare in UTC)
    DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    if parsed["metadata"] and parsed["metadata"].last_updated:
        if not DATE_REGEX.match(parsed["metadata"].last_updated):
            errors.append(
                ValidationError(
                    code="S5",
                    severity="error",
                    message=f'Last Updated must be YYYY-MM-DD format, got "{parsed["metadata"].last_updated}"',
                )
            )
        else:
            try:
                # Validate actual calendar date (not just bounds) - catches Feb 30, Apr 31, etc.
                datetime.strptime(parsed["metadata"].last_updated, "%Y-%m-%d")

                # Check if date is in the future
                from datetime import timezone
                date_parts = parsed["metadata"].last_updated.split("-")
                year, month, day = int(date_parts[0]), int(date_parts[1]), int(date_parts[2])
                last_updated_utc = datetime(year, month, day)
                today_utc = datetime.now(timezone.utc).replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
                today_naive = today_utc.replace(tzinfo=None)

                if last_updated_utc > today_naive:
                    errors.append(
                        ValidationError(
                            code="S5",
                            severity="error",
                            message=f"Last Updated date is in the future: {parsed['metadata'].last_updated}",
                        )
                    )
            except ValueError:
                errors.append(
                    ValidationError(
                        code="S5",
                        severity="error",
                        message=f"Last Updated is not a valid calendar date: {parsed['metadata'].last_updated}",
                    )
                )

    # S6: Missing at least one Claim Section with structured claim
    has_any_claims = len(parsed["structured_claims"]) > 0
    has_any_claim_section = any(
        parsed["claim_sections"].get(key) for key in ["verified", "estimates", "unknown"]
    )

    if not has_any_claim_section:
        errors.append(
            ValidationError(
                code="S6",
                severity="error",
                message="Missing claim sections (need at least one of: Verified Data, Estimates, Unknown)",
            )
        )
    elif not has_any_claims:
        errors.append(
            ValidationError(
                code="S6",
                severity="error",
                message="Claim sections exist but contain no structured claims (tables or bullets)",
            )
        )

    # S7: Free-form prose inside Claim Sections (warning)
    for prose in parsed["prose_in_claim_sections"]:
        content_preview = prose["content"][:50]
        if len(prose["content"]) > 50:
            content_preview += "..."
        warnings.append(
            ValidationError(
                code="S7",
                severity="warn",
                message=f'Free-form prose in claim section (line {prose["line"]}): "{content_preview}"',
                line=prose["line"],
            )
        )

    valid = len(errors) == 0
    if options.strict:
        valid = valid and len(warnings) == 0

    return ValidationResult(
        valid=valid,
        document_type="sot",
        errors=errors,
        warnings=warnings,
        metadata={
            "title": parsed["metadata"].title if parsed["metadata"] else None,
            "status": parsed["metadata"].status if parsed["metadata"] else None,
        }
        if parsed["metadata"]
        else None,
    )