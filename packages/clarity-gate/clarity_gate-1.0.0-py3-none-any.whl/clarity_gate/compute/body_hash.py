"""
Body SHA-256 computation for CGD documents.

Per CGD_FORMAT.md §3.10:
1. Read UTF-8 (BOM ok)
2. CRLF → LF
3. Remove YAML frontmatter (if starts with ---)
4. Remove end marker (if last two non-ws lines are --- + Clarity Gate: ...)
5. Remove trailing blank lines
6. SHA-256 → lowercase hex (64 chars)
"""

import hashlib


def compute_body_hash(content: str) -> str:
    """Compute body-sha256 per specification."""
    # 1. Handle BOM (remove if present)
    text = content
    if text and ord(text[0]) == 0xFEFF:
        text = text[1:]

    # 2. Normalize CRLF to LF
    text = text.replace("\r\n", "\n")

    # 3. Remove frontmatter if present
    if text.startswith("---\n"):
        lines = text.split("\n")
        frontmatter_end = -1

        for i in range(1, len(lines)):
            if lines[i].rstrip() == "---":  # Per §2.1: only trailing whitespace allowed
                frontmatter_end = i
                break

        if frontmatter_end != -1:
            # Remove frontmatter (including closing ---)
            text = "\n".join(lines[frontmatter_end + 1 :])

    # 4. Remove end marker if present (last two non-ws lines)
    lines = text.split("\n")
    last_non_empty_idx = -1
    second_last_non_empty_idx = -1

    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip():
            if last_non_empty_idx == -1:
                last_non_empty_idx = i
            elif second_last_non_empty_idx == -1:
                second_last_non_empty_idx = i
                break

    if (
        second_last_non_empty_idx >= 0
        and lines[second_last_non_empty_idx].strip() == "---"
        and lines[last_non_empty_idx].strip().startswith("Clarity Gate:")
    ):
        # Remove from separator line onwards
        lines = lines[:second_last_non_empty_idx]

    # 5. Remove trailing blank lines
    while lines and not lines[-1].strip():
        lines.pop()

    # 6. Compute SHA-256
    body = "\n".join(lines)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()