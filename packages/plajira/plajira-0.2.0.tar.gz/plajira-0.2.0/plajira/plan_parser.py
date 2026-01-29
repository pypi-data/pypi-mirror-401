"""Parser for .plan files.

Handles:
- Date headers (> YYYY-MM-DD)
- Item lines (* text, ? text, ! text, + text, ~ text)
- Text normalization
- Duplicate line detection
"""

from __future__ import annotations

import re
from dataclasses import dataclass


# Valid markers for .plan items
VALID_MARKERS = {"*", "?", "!", "+", "~"}

# Regex patterns
DATE_PATTERN = re.compile(r"^>\s*(\d{4}-\d{2}-\d{2})\s*$")
ITEM_PATTERN = re.compile(r"^([*?!+~])\s+(.+)$")


@dataclass
class PlanItem:
    """A single item from a .plan file."""
    marker: str           # *, ?, !, +, or ~
    raw_text: str         # Original text after marker
    normalized_text: str  # Normalized for matching
    date: str             # YYYY-MM-DD from preceding date header
    line_number: int      # 1-indexed line number in file


@dataclass
class DuplicateError:
    """Information about duplicate line texts found in .plan."""
    normalized_text: str
    occurrences: list[tuple[int, str, str]]  # (line_number, date, raw_line)


def normalize_text(text: str) -> str:
    """Normalize text for matching.

    1. Convert to lowercase
    2. Strip leading/trailing whitespace
    3. Collapse multiple spaces to single space
    """
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def parse_plan_file(filepath: str) -> tuple[list[PlanItem], list[DuplicateError]]:
    """Parse a .plan file and return items and any duplicate errors.

    Returns:
        (items, duplicates): List of parsed items and list of duplicate errors.
                            If duplicates is non-empty, the file is invalid.
    """
    items: list[PlanItem] = []
    current_date = ""
    line_number = 0

    # Track normalized texts to detect duplicates
    # Maps normalized_text -> list of (line_number, date, raw_line)
    seen_texts: dict[str, list[tuple[int, str, str]]] = {}

    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line_number += 1
            line = line.rstrip("\n\r")

            # Skip empty lines
            if not line.strip():
                continue

            # Check for date header
            date_match = DATE_PATTERN.match(line)
            if date_match:
                current_date = date_match.group(1)
                continue

            # Check for item line
            item_match = ITEM_PATTERN.match(line)
            if item_match:
                marker = item_match.group(1)
                raw_text = item_match.group(2)
                normalized = normalize_text(raw_text)

                # Track for duplicate detection
                if normalized not in seen_texts:
                    seen_texts[normalized] = []
                seen_texts[normalized].append((line_number, current_date, line))

                items.append(PlanItem(
                    marker=marker,
                    raw_text=raw_text,
                    normalized_text=normalized,
                    date=current_date,
                    line_number=line_number,
                ))

            # Lines not matching any pattern are ignored

    # Check for duplicates
    duplicates: list[DuplicateError] = []
    for normalized, occurrences in seen_texts.items():
        if len(occurrences) > 1:
            duplicates.append(DuplicateError(
                normalized_text=normalized,
                occurrences=occurrences,
            ))

    return items, duplicates


def get_latest_item_state(items: list[PlanItem]) -> dict[str, PlanItem]:
    """Get the latest state of each unique item.

    Since the same normalized text can appear multiple times with different
    markers (e.g., ? on day 1, * on day 2), we need the most recent version.

    However, the spec says duplicate text is an error, so this function
    assumes no duplicates exist. It returns a dict mapping normalized_text
    to the single PlanItem for that text.

    If duplicates exist, later items will overwrite earlier ones (which is
    fine because parse_plan_file already detected the error).
    """
    result: dict[str, PlanItem] = {}
    for item in items:
        result[item.normalized_text] = item
    return result


def validate_plan_file(filepath: str) -> list[DuplicateError]:
    """Validate a .plan file for duplicate lines.

    Returns list of duplicate errors (empty if valid).
    """
    _, duplicates = parse_plan_file(filepath)
    return duplicates
