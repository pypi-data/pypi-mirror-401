"""Text normalization utilities to prevent detector evasion.

This module provides text normalization functions to handle various
obfuscation techniques like unicode tricks, homoglyphs, zero-width
characters, and bidirectional text manipulation.
"""

import re
import unicodedata
from typing import Dict


# Homoglyph mapping - common lookalikes to ASCII
HOMOGLYPH_MAP = {
    # Cyrillic to Latin
    "а": "a",
    "е": "e",
    "о": "o",
    "р": "p",
    "с": "c",
    "у": "y",
    "х": "x",
    "А": "A",
    "В": "B",
    "Е": "E",
    "К": "K",
    "М": "M",
    "Н": "H",
    "О": "O",
    "Р": "P",
    "С": "C",
    "Т": "T",
    "Х": "X",
    # Greek to Latin
    "α": "a",
    "β": "b",
    "γ": "g",
    "δ": "d",
    "ε": "e",
    "ζ": "z",
    "η": "h",
    "θ": "th",
    "ι": "i",
    "κ": "k",
    "λ": "l",
    "μ": "m",
    "ν": "n",
    "ξ": "x",
    "ο": "o",
    "π": "p",
    "ρ": "r",
    "σ": "s",
    "τ": "t",
    "υ": "u",
    "φ": "ph",
    "χ": "ch",
    "ψ": "ps",
    "ω": "o",
    "Α": "A",
    "Β": "B",
    "Γ": "G",
    "Δ": "D",
    "Ε": "E",
    "Ζ": "Z",
    "Η": "H",
    "Θ": "TH",
    "Ι": "I",
    "Κ": "K",
    "Λ": "L",
    "Μ": "M",
    "Ν": "N",
    "Ξ": "X",
    "Ο": "O",
    "Π": "P",
    "Ρ": "R",
    "Σ": "S",
    "Τ": "T",
    "Υ": "U",
    "Φ": "PH",
    "Χ": "CH",
    "Ψ": "PS",
    "Ω": "O",
    # Common substitutions
    "０": "0",
    "１": "1",
    "２": "2",
    "３": "3",
    "４": "4",
    "５": "5",
    "６": "6",
    "７": "7",
    "８": "8",
    "９": "9",
    "ⅰ": "i",
    "ⅱ": "ii",
    "ⅲ": "iii",
    "ⅳ": "iv",
    "ⅴ": "v",
    "ⅵ": "vi",
    "ⅶ": "vii",
    "ⅷ": "viii",
    "ⅸ": "ix",
    "ⅹ": "x",
    # Math and special alphanumerics
    "𝐚": "a",
    "𝐛": "b",
    "𝐜": "c",
    "𝐝": "d",
    "𝐞": "e",
    "𝗮": "a",
    "𝗯": "b",
    "𝗰": "c",
    "𝗱": "d",
    "𝗲": "e",
    "𝘢": "a",
    "𝘣": "b",
    "𝘤": "c",
    "𝘥": "d",
    "𝘦": "e",
    "𝙖": "a",
    "𝙗": "b",
    "𝙘": "c",
    "𝙙": "d",
    "𝙚": "e",
}


# Zero-width and invisible characters
ZERO_WIDTH_CHARS = [
    "\u200b",  # Zero-width space
    "\u200c",  # Zero-width non-joiner
    "\u200d",  # Zero-width joiner
    "\ufeff",  # Zero-width no-break space (BOM)
    "\u2060",  # Word joiner
    "\u2062",  # Invisible times
    "\u2063",  # Invisible separator
    "\u2064",  # Invisible plus
]


# Bidirectional text override characters
BIDI_CHARS = [
    "\u202a",  # Left-to-right embedding
    "\u202b",  # Right-to-left embedding
    "\u202c",  # Pop directional formatting
    "\u202d",  # Left-to-right override
    "\u202e",  # Right-to-left override
    "\u2066",  # Left-to-right isolate
    "\u2067",  # Right-to-left isolate
    "\u2068",  # First strong isolate
    "\u2069",  # Pop directional isolate
]


def remove_zero_width_chars(text: str) -> str:
    """Remove zero-width and invisible Unicode characters.

    Args:
        text: Input text

    Returns:
        Text with zero-width characters removed
    """
    for char in ZERO_WIDTH_CHARS:
        text = text.replace(char, "")
    return text


def remove_bidi_chars(text: str) -> str:
    """Remove bidirectional text control characters.

    Args:
        text: Input text

    Returns:
        Text with bidi characters removed
    """
    for char in BIDI_CHARS:
        text = text.replace(char, "")
    return text


def replace_homoglyphs(text: str) -> str:
    """Replace homoglyphs with ASCII equivalents.

    Args:
        text: Input text

    Returns:
        Text with homoglyphs replaced
    """
    result = []
    for char in text:
        result.append(HOMOGLYPH_MAP.get(char, char))
    return "".join(result)


def normalize_unicode(text: str, form: str = "NFKC") -> str:
    """Normalize Unicode using specified form.

    NFKC (Compatibility Decomposition, followed by Canonical Composition)
    is most aggressive and converts things like ① to 1, ﬁ to fi, etc.

    Args:
        text: Input text
        form: Unicode normalization form (NFC, NFD, NFKC, NFKD)

    Returns:
        Normalized text
    """
    return unicodedata.normalize(form, text)


def remove_soft_hyphens(text: str) -> str:
    """Remove soft hyphens (invisible break hints).

    Args:
        text: Input text

    Returns:
        Text with soft hyphens removed
    """
    return text.replace("\u00ad", "")


def collapse_whitespace(text: str) -> str:
    """Collapse multiple whitespace to single space.

    Args:
        text: Input text

    Returns:
        Text with normalized whitespace
    """
    return re.sub(r"\s+", " ", text).strip()


def normalize_text(text: str, aggressive: bool = True) -> str:
    """Apply full text normalization pipeline.

    This is the main function to use for detector input normalization.
    It applies all transformations to maximize detection and prevent evasion.

    Args:
        text: Input text to normalize
        aggressive: If True, applies all normalizations including homoglyphs

    Returns:
        Fully normalized text

    Example:
        >>> text = "Hеllo\\u200bWorld"  # Cyrillic 'е' + zero-width space
        >>> normalize_text(text)
        'Hello World'
    """
    if not text:
        return text

    # Step 1: Remove invisible/zero-width characters
    text = remove_zero_width_chars(text)
    text = remove_soft_hyphens(text)

    # Step 2: Remove bidirectional text controls
    text = remove_bidi_chars(text)

    # Step 3: Unicode normalization (NFKC is most aggressive)
    text = normalize_unicode(text, form="NFKC")

    # Step 4: Replace homoglyphs (optional but recommended)
    if aggressive:
        text = replace_homoglyphs(text)

    # Step 5: Collapse whitespace
    text = collapse_whitespace(text)

    return text


def normalize_for_comparison(text: str) -> str:
    """Normalize text for case-insensitive comparison.

    Applies normalization and converts to lowercase.

    Args:
        text: Input text

    Returns:
        Normalized lowercase text
    """
    return normalize_text(text, aggressive=True).lower()


def get_normalization_stats(original: str, normalized: str) -> Dict[str, int]:
    """Get statistics about what was normalized.

    Useful for logging and debugging obfuscation attempts.

    Args:
        original: Original text
        normalized: Normalized text

    Returns:
        Dictionary with normalization statistics
    """
    stats = {
        "length_change": len(original) - len(normalized),
        "zero_width_removed": sum(1 for c in original if c in ZERO_WIDTH_CHARS),
        "bidi_removed": sum(1 for c in original if c in BIDI_CHARS),
        "homoglyphs_replaced": sum(1 for c in original if c in HOMOGLYPH_MAP),
        "had_soft_hyphens": "\u00ad" in original,
    }
    stats["total_changes"] = sum(
        v for k, v in stats.items() if k != "length_change" and isinstance(v, int)
    )
    return stats
