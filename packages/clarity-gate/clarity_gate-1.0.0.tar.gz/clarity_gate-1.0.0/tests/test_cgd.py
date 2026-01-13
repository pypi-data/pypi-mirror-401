import pytest

from clarity_gate.validators import validate_cgd


def _make_cgd(frontmatter_lines: list[str], body: str = "Body\n") -> str:
    fm = "\n".join(frontmatter_lines)
    return (
        "---\n"
        f"{fm}\n"
        "---\n\n"
        f"{body}\n"
        "---\n"
        "Clarity Gate: CLEAR | REVIEWED\n"
    )


def test_cgd_valid_minimal_passes() -> None:
    content = _make_cgd(
        [
            'clarity-gate-version: "1.2"',
            "processed-date: 2026-01-10",
            "processed-by: test",
            "clarity-status: CLEAR",
            "hitl-status: REVIEWED",
            "hitl-pending-count: 0",
            "points-passed: 1-9",
            "hitl-claims: []",
        ],
        body="Minimal\n",
    )
    result = validate_cgd(content)
    assert result.valid is True
    assert result.document_type == "cgd"
    assert result.errors == []
    assert result.computed.rag_ingestable is True


def test_cgd_c0_invalid_yaml_unclosed_inline_list() -> None:
    content = _make_cgd(
        [
            'clarity-gate-version: "1.2"',
            "processed-date: 2026-01-10",
            "processed-by: test",
            "clarity-status: CLEAR",
            "hitl-status: REVIEWED",
            "hitl-pending-count: 0",
            "points-passed: 1-9",
            "hitl-claims: [",
        ],
        body="Unclosed bracket\n",
    )
    result = validate_cgd(content)
    assert result.valid is False
    assert any(e.code == "C0" for e in result.errors)


def test_cgd_c18_rag_ingestable_must_be_boolean() -> None:
    content = _make_cgd(
        [
            'clarity-gate-version: "1.2"',
            "processed-date: 2026-01-10",
            "processed-by: test",
            "clarity-status: CLEAR",
            "hitl-status: REVIEWED",
            "hitl-pending-count: 0",
            "points-passed: 1-9",
            "hitl-claims: []",
            'rag-ingestable: "true"',
        ],
        body="Bad type\n",
    )
    result = validate_cgd(content)
    assert result.valid is False
    assert any(e.code == "C18" for e in result.errors)


def test_cgd_future_major_version_forces_computed_not_ingestable() -> None:
    content = _make_cgd(
        [
            'clarity-gate-version: "2.0"',
            "processed-date: 2026-01-10",
            "processed-by: test",
            "clarity-status: CLEAR",
            "hitl-status: REVIEWED",
            "hitl-pending-count: 0",
            "points-passed: 1-9",
            "hitl-claims: []",
        ],
        body="Future major\n",
    )
    result = validate_cgd(content)
    assert result.valid is True
    assert any(w.code == "C22" for w in result.warnings)
    assert result.computed.rag_ingestable is False


def test_cgd_future_major_declared_true_triggers_c19() -> None:
    content = _make_cgd(
        [
            'clarity-gate-version: "2.0"',
            "processed-date: 2026-01-10",
            "processed-by: test",
            "clarity-status: CLEAR",
            "hitl-status: REVIEWED",
            "hitl-pending-count: 0",
            "points-passed: 1-9",
            "hitl-claims: []",
            "rag-ingestable: true",
        ],
        body="Future major declared ingestable\n",
    )
    result = validate_cgd(content)
    assert result.valid is True
    assert any(w.code == "C22" for w in result.warnings)
    assert any(w.code == "C19" for w in result.warnings)
    assert result.computed.rag_ingestable is False
