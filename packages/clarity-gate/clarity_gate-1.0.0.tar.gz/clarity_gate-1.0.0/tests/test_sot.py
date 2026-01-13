from clarity_gate.validators import validate_sot


def test_sot_minimal_valid_passes() -> None:
    content = """# Company Revenue Data -- Source of Truth

**Last Updated:** 2026-01-10
**Owner:** Finance Team
**Status:** ASSESSED
**Version:** 1.0

## Verification Status

This document has been verified by the Finance Team.

## Verified Data

| Metric | Value | Source |
|--------|-------|--------|
| Q4 2025 Revenue | $10.5M | Financial Reports |
| YoY Growth | 15% | Calculated |

## Estimates (NOT VERIFIED)

- 2026 Revenue Projection: $12M (based on current trends)

## Unknown / Data Not Available

- Competitor market share data
"""

    result = validate_sot(content)
    assert result.valid is True
    assert result.document_type == "sot"
    assert result.errors == []
