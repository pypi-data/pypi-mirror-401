"""
Unicode normalization for clarity-gate.
Applied to frontmatter keys, end marker, SOT title/metadata only.

Per VALIDATOR_REFERENCE.md §1.2
"""

# Unicode normalization mappings (no case changes)
UNICODE_MAP = {
    "\u2013": "-",  # En dash → hyphen
    "\u2014": "-",  # Em dash → hyphen
    "\u2212": "-",  # Minus sign → hyphen
    "\u2018": "'",  # Left single quote → apostrophe
    "\u2019": "'",  # Right single quote → apostrophe
    "\u201C": '"',  # Left double quote → quote
    "\u201D": '"',  # Right double quote → quote
}


def normalize_unicode(text: str) -> str:
    """
    Normalize unicode characters in text.
    Only normalizes specific characters per spec, does NOT change case.
    """
    result = text
    for char, replacement in UNICODE_MAP.items():
        result = result.replace(char, replacement)
    return result


def normalize_line_endings(text: str) -> str:
    """Normalize line endings: CRLF → LF."""
    return text.replace("\r\n", "\n")


def remove_bom(text: str) -> str:
    """Remove UTF-8 BOM if present."""
    if text and ord(text[0]) == 0xFEFF:
        return text[1:]
    return text


def preprocess_content(text: str) -> str:
    """
    Full preprocessing: BOM removal + line ending normalization.
    Unicode normalization is applied selectively, not here.
    """
    return normalize_line_endings(remove_bom(text))