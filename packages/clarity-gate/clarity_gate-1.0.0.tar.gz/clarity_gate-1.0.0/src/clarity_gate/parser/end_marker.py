"""
End marker parsing for CGD documents.

Per VALIDATOR_REFERENCE.md §2.2:
- Last two non-whitespace lines must be `---` then `Clarity Gate: <clarity> | <hitl>`
- Scan backwards from EOF
"""

import re
from typing import Optional, List

from ..types import EndMarker, ValidationError
from .normalize import normalize_unicode


VALID_CLARITY = ["CLEAR", "UNCLEAR"]
VALID_HITL = ["PENDING", "REVIEWED", "REVIEWED_WITH_EXCEPTIONS"]

END_MARKER_PATTERN = re.compile(
    r"^Clarity Gate:\s*(CLEAR|UNCLEAR)\s*\|\s*(PENDING|REVIEWED|REVIEWED_WITH_EXCEPTIONS)$"
)


def find_end_marker(content: str) -> Optional[EndMarker]:
    """
    Find and parse the end marker from document content.
    Returns None if no valid end marker structure found.
    """
    lines = content.split("\n")

    # Find last two non-whitespace lines (scan backwards)
    non_empty: List[dict] = []

    for i in range(len(lines) - 1, -1, -1):
        trimmed = lines[i].strip()
        if trimmed:
            non_empty.insert(0, {"text": trimmed, "line": i + 1})  # 1-indexed
            if len(non_empty) >= 2:
                break

    if len(non_empty) < 2:
        return None

    # First of the two must be `---`
    if non_empty[0]["text"] != "---":
        return None

    # Second must match `Clarity Gate: <clarity> | <hitl>`
    normalized = normalize_unicode(non_empty[1]["text"])
    match = END_MARKER_PATTERN.match(normalized)

    if not match:
        return None

    return EndMarker(
        clarity=match.group(1),
        hitl=match.group(2),
        line=non_empty[1]["line"],
        separator_line=non_empty[0]["line"],
    )


def validate_end_marker(marker: EndMarker) -> List[ValidationError]:
    """
    Validate end marker values.
    Returns errors if invalid combinations found.
    """
    errors: List[ValidationError] = []

    # Check clarity value
    if marker.clarity not in VALID_CLARITY:
        errors.append(
            ValidationError(
                code="C6",
                severity="error",
                message=f'Invalid clarity-status in end marker: "{marker.clarity}". Must be CLEAR or UNCLEAR',
                line=marker.line,
            )
        )

    # Check hitl value
    if marker.hitl not in VALID_HITL:
        errors.append(
            ValidationError(
                code="C6",
                severity="error",
                message=f'Invalid hitl-status in end marker: "{marker.hitl}". Must be PENDING, REVIEWED, or REVIEWED_WITH_EXCEPTIONS',
                line=marker.line,
            )
        )

    # Check invalid combinations: UNCLEAR cannot be REVIEWED or REVIEWED_WITH_EXCEPTIONS
    if marker.clarity == "UNCLEAR" and marker.hitl in ["REVIEWED", "REVIEWED_WITH_EXCEPTIONS"]:
        errors.append(
            ValidationError(
                code="C7",
                severity="error",
                message=f"Invalid state combination: UNCLEAR cannot have hitl-status {marker.hitl}",
                line=marker.line,
            )
        )

    return errors


def check_end_marker_consistency(
    marker: EndMarker, frontmatter_clarity: str, frontmatter_hitl: str
) -> List[ValidationError]:
    """
    Check that end marker matches frontmatter values.
    """
    errors: List[ValidationError] = []

    if marker.clarity != frontmatter_clarity:
        errors.append(
            ValidationError(
                code="C6",
                severity="error",
                message=f'End marker clarity-status "{marker.clarity}" does not match frontmatter "{frontmatter_clarity}"',
                line=marker.line,
            )
        )

    if marker.hitl != frontmatter_hitl:
        errors.append(
            ValidationError(
                code="C6",
                severity="error",
                message=f'End marker hitl-status "{marker.hitl}" does not match frontmatter "{frontmatter_hitl}"',
                line=marker.line,
            )
        )

    return errors