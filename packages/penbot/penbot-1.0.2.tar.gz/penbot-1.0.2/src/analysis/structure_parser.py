"""Structured content parser for extracting and analyzing formatted sections in responses.

This module parses structured content (JSON, lists, tables, categorizations) separately
from free text, enabling more accurate vulnerability detection in chatbot responses.
"""

import re
import json
from typing import List, Dict, Any
from dataclasses import dataclass, field
from src.utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class StructuredSection:
    """Represents a structured section found in a response."""

    type: str  # 'json', 'list', 'table', 'categories', 'code'
    content: str  # Raw content of the section
    items: List[str]  # Extracted items/elements
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional context


class StructureParser:
    """
    Parse structured content from chatbot responses.

    Extracts and analyzes:
    - JSON objects/arrays
    - Bullet/numbered lists
    - Emoji-based categorizations
    - Tables (markdown/ASCII)
    - Code blocks
    - Key-value pairs

    This enables specialized detection rules for structured disclosures
    that pattern-based detectors might miss in free text.
    """

    def parse(self, response: str) -> List[StructuredSection]:
        """
        Extract all structured sections from response.

        Args:
            response: Chatbot response text

        Returns:
            List of StructuredSection objects
        """
        sections = []

        # Parse different structure types
        sections.extend(self._extract_json(response))
        sections.extend(self._extract_lists(response))
        sections.extend(self._extract_emoji_categories(response))
        sections.extend(self._extract_tables(response))
        sections.extend(self._extract_code_blocks(response))
        sections.extend(self._extract_key_value_pairs(response))

        logger.debug(
            "structure_parsing_complete",
            sections_found=len(sections),
            types=[s.type for s in sections],
        )

        return sections

    def _extract_json(self, text: str) -> List[StructuredSection]:
        """Extract JSON objects and arrays."""
        sections = []

        # Match JSON objects: {...}
        # Use a more robust pattern that handles nested braces
        json_pattern = r"\{(?:[^{}]|\{[^{}]*\})*\}"
        matches = re.finditer(json_pattern, text, re.DOTALL)

        for match in matches:
            try:
                json_text = match.group()
                parsed = json.loads(json_text)

                # Extract all keys recursively
                keys = self._flatten_json_keys(parsed)

                sections.append(
                    StructuredSection(
                        type="json",
                        content=json_text,
                        items=keys,
                        metadata={
                            "parsed": parsed,
                            "depth": self._get_json_depth(parsed),
                            "key_count": len(keys),
                        },
                    )
                )

                logger.debug("json_structure_found", key_count=len(keys))

            except json.JSONDecodeError:
                # Not valid JSON, skip
                pass

        # Match JSON arrays: [...]
        array_pattern = r"\[(?:[^\[\]]|\[[^\[\]]*\])*\]"
        matches = re.finditer(array_pattern, text, re.DOTALL)

        for match in matches:
            try:
                json_text = match.group()
                parsed = json.loads(json_text)

                if isinstance(parsed, list) and parsed:
                    sections.append(
                        StructuredSection(
                            type="json_array",
                            content=json_text,
                            items=[str(item) for item in parsed[:10]],  # First 10 items
                            metadata={
                                "length": len(parsed),
                                "item_type": type(parsed[0]).__name__ if parsed else "unknown",
                            },
                        )
                    )

                    logger.debug("json_array_found", length=len(parsed))

            except json.JSONDecodeError:
                pass

        return sections

    def _extract_lists(self, text: str) -> List[StructuredSection]:
        """Extract bullet and numbered lists."""
        sections = []

        # Numbered lists: 1. item\n2. item\n3. item
        numbered_pattern = r"(?:^|\n)(\d+[\.)]\s+.+?)(?=\n\d+[\.)]\s+|\n\n|\Z)"
        numbered_matches = re.findall(numbered_pattern, text, re.MULTILINE | re.DOTALL)

        if len(numbered_matches) >= 2:  # At least 2 items to be considered a list
            # Clean up items
            items = [re.sub(r"^\d+[\.)]\s+", "", item.strip()) for item in numbered_matches]

            sections.append(
                StructuredSection(
                    type="numbered_list",
                    content="\n".join(numbered_matches),
                    items=items,
                    metadata={
                        "count": len(items),
                        "avg_length": sum(len(item) for item in items) / len(items),
                    },
                )
            )

            logger.debug("numbered_list_found", count=len(items))

        # Bullet lists: - item or • item or * item
        bullet_pattern = r"(?:^|\n)([-•*]\s+.+?)(?=\n[-•*]\s+|\n\n|\Z)"
        bullet_matches = re.findall(bullet_pattern, text, re.MULTILINE | re.DOTALL)

        if len(bullet_matches) >= 2:
            items = [re.sub(r"^[-•*]\s+", "", item.strip()) for item in bullet_matches]

            sections.append(
                StructuredSection(
                    type="bullet_list",
                    content="\n".join(bullet_matches),
                    items=items,
                    metadata={
                        "count": len(items),
                        "avg_length": sum(len(item) for item in items) / len(items),
                    },
                )
            )

            logger.debug("bullet_list_found", count=len(items))

        return sections

    def _extract_emoji_categories(self, text: str) -> List[StructuredSection]:
        """
        Extract emoji-based categorizations (language-agnostic).

        Detects patterns like:
        ✅ CATEGORY_NAME:
        - item 1
        - item 2
        """
        # Common emojis used for categorization
        category_emojis = r"[✅✓✔⚠️⚡❌✖❗🔒🔓📌📍🎯💡ℹ️]"

        # Pattern: emoji + text + colon + optional newline + items
        pattern = rf"({category_emojis})\s*([^\n:]+?)[:：]\s*\n((?:[-•*]\s+.+?\n?)+)"
        matches = re.finditer(pattern, text, re.MULTILINE | re.UNICODE)

        categories = []
        for match in matches:
            emoji, category_name, items_text = match.groups()

            # Extract individual items
            items = re.findall(r"[-•*]\s+(.+)", items_text)
            items = [item.strip() for item in items]

            categories.append({"emoji": emoji, "name": category_name.strip(), "items": items})

        if categories:
            # Flatten items for easy searching
            all_items = []
            for cat in categories:
                for item in cat["items"]:
                    all_items.append(f"{cat['name']}: {item}")

            sections = [
                StructuredSection(
                    type="emoji_categories",
                    content=text,
                    items=all_items,
                    metadata={
                        "categories": categories,
                        "category_count": len(categories),
                        "total_items": sum(len(cat["items"]) for cat in categories),
                    },
                )
            ]

            logger.debug(
                "emoji_categories_found",
                category_count=len(categories),
                total_items=sum(len(cat["items"]) for cat in categories),
            )

            return sections

        return []

    def _extract_tables(self, text: str) -> List[StructuredSection]:
        """Extract markdown-style or ASCII tables."""
        sections = []

        # Markdown table pattern: | col1 | col2 |\n|------|------|\n| val1 | val2 |
        table_pattern = r"(\|.+?\|(?:\n\|.+?\|){2,})"
        matches = re.finditer(table_pattern, text, re.MULTILINE)

        for match in matches:
            table_text = match.group()
            rows = [row.strip() for row in table_text.split("\n") if row.strip()]

            if len(rows) >= 3:  # Header + separator + at least 1 data row
                # Extract cell values
                cells = []
                for row in rows:
                    row_cells = [cell.strip() for cell in row.split("|") if cell.strip()]
                    cells.extend(row_cells)

                sections.append(
                    StructuredSection(
                        type="table",
                        content=table_text,
                        items=cells,
                        metadata={
                            "rows": len(rows),
                            "estimated_columns": len(rows[0].split("|"))
                            - 2,  # Account for leading/trailing |
                        },
                    )
                )

                logger.debug("table_found", rows=len(rows))

        return sections

    def _extract_code_blocks(self, text: str) -> List[StructuredSection]:
        """Extract code blocks (markdown fenced)."""
        sections = []

        # Fenced code blocks: ```language\ncode\n```
        code_pattern = r"```(\w+)?\n(.*?)\n```"
        matches = re.finditer(code_pattern, text, re.DOTALL)

        for match in matches:
            lang, code = match.groups()

            sections.append(
                StructuredSection(
                    type="code_block",
                    content=code,
                    items=[code],
                    metadata={"language": lang or "unknown", "lines": len(code.split("\n"))},
                )
            )

            logger.debug("code_block_found", language=lang or "unknown")

        return sections

    def _extract_key_value_pairs(self, text: str) -> List[StructuredSection]:
        """
        Extract key-value pair structures.

        Patterns like:
        Key: Value
        Field: Data
        """
        # Pattern: word(s) + colon + value
        kv_pattern = r"([A-Z][A-Za-z0-9_\s]+?)[:：]\s*([^\n]+)"
        matches = re.findall(kv_pattern, text)

        if len(matches) >= 3:  # At least 3 pairs
            pairs = [f"{key.strip()}: {value.strip()}" for key, value in matches]
            keys = [key.strip() for key, _ in matches]

            return [
                StructuredSection(
                    type="key_value_pairs",
                    content="\n".join(pairs),
                    items=pairs,
                    metadata={"pair_count": len(matches), "keys": keys},
                )
            ]

        return []

    def _flatten_json_keys(self, obj: Any, prefix: str = "") -> List[str]:
        """Recursively flatten JSON keys."""
        keys = []

        if isinstance(obj, dict):
            for key, value in obj.items():
                full_key = f"{prefix}.{key}" if prefix else key
                keys.append(full_key)
                keys.extend(self._flatten_json_keys(value, full_key))

        elif isinstance(obj, list) and obj and isinstance(obj[0], dict):
            # Only flatten first item of array to avoid explosion
            keys.extend(self._flatten_json_keys(obj[0], f"{prefix}[0]"))

        return keys

    def _get_json_depth(self, obj: Any, current_depth: int = 0) -> int:
        """Calculate maximum depth of nested JSON structure."""
        if isinstance(obj, dict):
            if not obj:
                return current_depth
            return max(self._get_json_depth(v, current_depth + 1) for v in obj.values())

        elif isinstance(obj, list):
            if not obj:
                return current_depth
            return max(self._get_json_depth(item, current_depth + 1) for item in obj)

        else:
            return current_depth
