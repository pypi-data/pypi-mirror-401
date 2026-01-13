"""
YAML frontmatter parsing for CGD documents.

Per VALIDATOR_REFERENCE.md §2.1:
- Line-based delimiter detection (entire line is exactly `---`)
- File must start with `---` on line 1
"""

from typing import Optional, Tuple, Dict, Any, List
import yaml

from ..types import FrontmatterExtraction, CGDFrontmatter, HITLClaim, ValidationError
from .normalize import normalize_unicode


def extract_frontmatter(content: str) -> Optional[FrontmatterExtraction]:
    """
    Extract YAML frontmatter from document content.
    Returns None if no valid frontmatter block found.
    """
    lines = content.split("\n")

    # Line 1 must be exactly `---` (trailing whitespace OK, leading whitespace NOT OK)
    if not lines or lines[0].rstrip() != "---":
        return None

    # Find closing delimiter
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            frontmatter_lines = lines[1:i]
            frontmatter = "\n".join(frontmatter_lines)

            # Calculate body start offset
            body_start_offset = 0
            for j in range(i + 1):
                body_start_offset += len(lines[j]) + 1  # +1 for \n

            return FrontmatterExtraction(
                frontmatter=frontmatter,
                body_start=i + 2,  # 1-indexed, line after closing ---
                body_start_offset=body_start_offset,
            )

    return None  # No closing delimiter


def parse_yaml(yaml_content: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Parse YAML content.
    Returns (data, error) tuple.
    
    Per VALIDATOR_REFERENCE.md §1.2: Keys are normalized (smart quotes, em-dashes)
    to ensure cross-language parity with TypeScript implementation.
    """
    try:
        data = yaml.safe_load(yaml_content)
        if not isinstance(data, dict):
            return None, "YAML content is not a mapping"
        # Normalize keys per §1.2 - handles smart quotes, em-dashes in keys
        normalized_data = {normalize_unicode(str(k)): v for k, v in data.items()}
        return normalized_data, None
    except yaml.YAMLError as e:
        return None, str(e)


def validate_frontmatter_schema(
    data: Dict[str, Any]
) -> Tuple[Optional[CGDFrontmatter], List[ValidationError]]:
    """
    Validate and cast parsed YAML to CGDFrontmatter.
    """
    errors: List[ValidationError] = []

    required_fields = [
        "clarity-gate-version",
        "processed-date",
        "processed-by",
        "clarity-status",
        "hitl-status",
        "hitl-pending-count",
        "points-passed",
        "hitl-claims",
    ]

    # Check required fields
    for field_name in required_fields:
        if field_name not in data:
            errors.append(
                ValidationError(
                    code="C2",
                    severity="error",
                    message=f"Missing required field: {field_name}",
                )
            )

    if errors:
        return None, errors

    # Validate hitl-claims is a list
    if not isinstance(data["hitl-claims"], list):
        errors.append(
            ValidationError(
                code="C2",
                severity="error",
                message="hitl-claims must be a list (use [] for empty)",
            )
        )
        return None, errors

    # Parse hitl-claims
    hitl_claims: List[HITLClaim] = []
    for item in data["hitl-claims"]:
        if isinstance(item, dict):
            hitl_claims.append(
                HITLClaim(
                    claim=str(item.get("claim", "")),
                    confirmed_by=item.get("confirmed-by"),
                    date=item.get("date"),
                )
            )
        else:
            hitl_claims.append(HITLClaim(claim=str(item)))

    # Build frontmatter object
    frontmatter = CGDFrontmatter(
        clarity_gate_version=str(data["clarity-gate-version"]),
        processed_date=str(data["processed-date"]),
        processed_by=str(data["processed-by"]),
        clarity_status=data["clarity-status"],
        hitl_status=data["hitl-status"],
        hitl_pending_count=int(data["hitl-pending-count"]),
        points_passed=str(data["points-passed"]),
        hitl_claims=hitl_claims,
    )

    # Add optional fields if present
    if "body-sha256" in data:
        frontmatter.body_sha256 = str(data["body-sha256"])
    if "rag-ingestable" in data:
        raw_value = data["rag-ingestable"]
        if not isinstance(raw_value, bool):
            errors.append(
                ValidationError(
                    code="C18",
                    severity="error",
                    message=f"rag-ingestable must be boolean, got {type(raw_value).__name__}",
                )
            )
        else:
            frontmatter.rag_ingestable = raw_value
    if "exclusions-coverage" in data:
        frontmatter.exclusions_coverage = float(data["exclusions-coverage"])
    if "exceptions-reason" in data:
        frontmatter.exceptions_reason = str(data["exceptions-reason"])
    if "exceptions-ids" in data:
        ids = data["exceptions-ids"]
        frontmatter.exceptions_ids = [str(x) for x in ids] if isinstance(ids, list) else [str(ids)]

    return frontmatter, errors