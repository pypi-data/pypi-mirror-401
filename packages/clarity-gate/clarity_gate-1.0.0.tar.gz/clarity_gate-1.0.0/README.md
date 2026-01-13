# clarity-gate

Pre-ingestion verification for epistemic quality in RAG systems.

> **Core Question:** "If another LLM reads this document, will it mistake assumptions for facts?"

## Status

⚠️ **v0.1.0 is a placeholder release** to reserve the package name. Full validation is coming soon.

For working validators now, use the existing packages:
- `pip install cgd-validator`
- `pip install sot-validator`

Or use the [Claude skill](https://github.com/frmoretto/clarity-gate/blob/main/SKILL.md) directly.

---

## What It Does

Clarity Gate validates documents before they enter knowledge bases, ensuring:
- Claims are properly marked as hypotheses vs. established facts
- Projections have uncertainty markers
- Assumptions are explicit, not buried
- Data is internally consistent

## Installation

```bash
pip install clarity-gate
```

## CLI Usage

```bash
# Validate a Clarity-Gated Document
clarity-gate validate-cgd document.cgd

# Validate a Source of Truth file
clarity-gate validate-sot reference.sot

# Auto-detect format
clarity-gate check document.md

# Options
clarity-gate validate-cgd document.cgd --json      # JSON output
clarity-gate validate-cgd document.cgd --strict    # Treat warnings as errors
```

## Programmatic Usage

```python
from clarity_gate import validate_cgd, validate_sot, validate

result = validate_cgd("path/to/document.cgd")

if result.valid:
    print("Document passes all checks")
    print(f"RAG-ingestable: {result.metadata.rag_ingestable}")
else:
    for error in result.errors:
        print(f"[{error.rule}] {error.message}")
```

## Document Formats

### CGD (Clarity-Gated Document)

Documents that have been verified for epistemic quality:
- YAML frontmatter with verification status
- Epistemic markers inline (e.g., `*(not specified)*`)
- HITL verification records
- End marker: `Clarity Gate: CLEAR | REVIEWED`

### SOT (Source of Truth)

Authoritative reference documents:
- Strict structure requirements
- Staleness tracking with markers: `[STABLE]`, `[CHECK]`, `[VOLATILE]`
- Verified claims with citations

## Specification

This validator implements:
- [CGD_FORMAT.md v1.2](https://github.com/frmoretto/clarity-gate/blob/main/docs/CGD_FORMAT.md) — 24 CGD rules
- [SOT_FORMAT.md v1.2](https://github.com/frmoretto/clarity-gate/blob/main/docs/SOT_FORMAT.md) — 7 SOT rules
- [VALIDATOR_REFERENCE.md v1.2](https://github.com/frmoretto/clarity-gate/blob/main/docs/VALIDATOR_REFERENCE.md) — Implementation guide

## Related Packages

| Package | Purpose |
|---------|---------|
| `clarity-gate` | Unified validator (this package) |
| `claritygate` | Alias → redirects here |
| `cgd-validator` | Legacy CGD validator |
| `sot-validator` | Legacy SOT validator |

## Links

- [clarity-gate](https://github.com/frmoretto/clarity-gate) — Main project repository
- [arxiparse.org](https://arxiparse.org) — Live implementation for scientific papers
- [LessWrong post](https://www.lesswrong.com/posts/...) — Research writeup

## License

CC-BY-4.0
