"""
Exclusion block parsing for CGD documents.

Per VALIDATOR_REFERENCE.md §2.3:
- Stack discipline: no nesting, no overlap, no duplicate IDs
- Markers inside fenced code blocks are ignored
- ID format: [A-Za-z0-9][A-Za-z0-9._-]{0,63}
"""

import re
from typing import List, Tuple, Optional

from ..types import ExclusionBlock, ValidationError


# Regex patterns for exclusion markers (exact match required per spec)
BEGIN_PATTERN = re.compile(
    r"<!--\s*CG-EXCLUSION:BEGIN\s+id=([A-Za-z0-9][A-Za-z0-9._-]{0,63})\s*-->"
)
END_PATTERN = re.compile(
    r"<!--\s*CG-EXCLUSION:END\s+id=([A-Za-z0-9][A-Za-z0-9._-]{0,63})\s*-->"
)
CODE_FENCE_PATTERN = re.compile(r"^(`{3,}|~{3,})")


def parse_exclusion_blocks(
    content: str, body_start_line: int = 1
) -> Tuple[List[ExclusionBlock], List[ValidationError]]:
    """
    Parse exclusion blocks from document content.
    Enforces stack discipline per spec.
    """
    errors: List[ValidationError] = []
    blocks: List[ExclusionBlock] = []
    stack: List[dict] = []  # {id, line, offset}
    seen_ids: set = set()

    in_code_fence = False
    code_fence_char = ""
    code_fence_length = 0

    lines = content.split("\n")
    char_offset = 0

    for i, line in enumerate(lines):
        line_num = body_start_line + i

        # Track code fence state
        # Per spec §2.3: same character, equal or greater length
        fence_match = CODE_FENCE_PATTERN.match(line.lstrip())  # lstrip() to handle indented fences
        if fence_match:
            fence_str = fence_match.group(1)
            if not in_code_fence:
                # Opening fence
                in_code_fence = True
                code_fence_char = fence_str[0]
                code_fence_length = len(fence_str)
            elif fence_str[0] == code_fence_char and len(fence_str) >= code_fence_length:
                # Closing fence: same char AND length >= opening length
                in_code_fence = False
                code_fence_char = ""
                code_fence_length = 0
            # Note: if chars don't match or length is shorter, fence stays open

        # Skip markers inside code fences
        if in_code_fence:
            char_offset += len(line) + 1
            continue

        # Check for BEGIN marker
        begin_match = BEGIN_PATTERN.search(line)
        if begin_match:
            id_ = begin_match.group(1)

            # Check for nesting (C12b)
            if stack:
                errors.append(
                    ValidationError(
                        code="C12b",
                        severity="error",
                        message=f'Nested exclusion block: "{id_}" inside "{stack[-1]["id"]}"',
                        line=line_num,
                    )
                )

            # Check for duplicate ID (C12d)
            if id_ in seen_ids:
                errors.append(
                    ValidationError(
                        code="C12d",
                        severity="error",
                        message=f'Duplicate exclusion id: "{id_}"',
                        line=line_num,
                    )
                )

            stack.append({"id": id_, "line": line_num, "offset": char_offset})
            seen_ids.add(id_)
            char_offset += len(line) + 1
            continue

        # Check for END marker
        end_match = END_PATTERN.search(line)
        if end_match:
            id_ = end_match.group(1)

            if not stack:
                # END without BEGIN (C12a)
                errors.append(
                    ValidationError(
                        code="C12a",
                        severity="error",
                        message=f'Exclusion END without BEGIN: "{id_}"',
                        line=line_num,
                    )
                )
            elif stack[-1]["id"] != id_:
                # Interleaved blocks (C12c)
                errors.append(
                    ValidationError(
                        code="C12c",
                        severity="error",
                        message=f'Interleaved exclusion blocks: expected END for "{stack[-1]["id"]}", got "{id_}"',
                        line=line_num,
                    )
                )
            else:
                # Valid close
                begin = stack.pop()
                blocks.append(
                    ExclusionBlock(
                        id=id_,
                        begin_line=begin["line"],
                        end_line=line_num,
                        begin_offset=begin["offset"],
                        end_offset=char_offset + len(line) + 1,  # +1 for trailing newline per §6.4
                    )
                )

        char_offset += len(line) + 1

    # Check for unclosed blocks (C12a)
    for unclosed in stack:
        errors.append(
            ValidationError(
                code="C12a",
                severity="error",
                message=f'Unclosed exclusion block: "{unclosed["id"]}"',
                line=unclosed["line"],
            )
        )

    return blocks, errors


def calculate_exclusion_bytes(content: str, blocks: List[ExclusionBlock]) -> int:
    """Calculate total bytes covered by exclusion blocks."""
    total = 0
    for block in blocks:
        total += block.end_offset - block.begin_offset
    return total


def calculate_exclusions_coverage(content: str, blocks: List[ExclusionBlock]) -> float:
    """
    Calculate exclusions coverage ratio using byte lengths per spec §6.4.
    BUG-053 fix: Extract actual block content and compute true byte length
    instead of approximating with uniform ratio.
    """
    if not content:
        return 0.0
    content_bytes = len(content.encode("utf-8"))
    if content_bytes == 0:
        return 0.0

    excluded_bytes = 0
    for block in blocks:
        # Extract actual block content using character offsets and compute true byte length
        block_text = content[block.begin_offset:block.end_offset]
        excluded_bytes += len(block_text.encode("utf-8"))

    return excluded_bytes / content_bytes


def validate_exception_ids(
    blocks: List[ExclusionBlock], exception_ids: Optional[List[str]]
) -> List[ValidationError]:
    """Validate exclusion IDs against exceptions-ids list."""
    errors: List[ValidationError] = []

    if not exception_ids:
        return errors

    block_ids = {b.id for b in blocks}

    for id_ in exception_ids:
        if id_ not in block_ids:
            errors.append(
                ValidationError(
                    code="C15",
                    severity="error",
                    message=f'exceptions-ids references non-existent exclusion block: "{id_}"',
                )
            )

    return errors