"""Similarity scoring for duplicate detection.

Provides:
- Levenshtein ratio (fuzzy string matching)
- Word overlap (Jaccard similarity)
- Combined similarity score
- Suspected duplicate detection
"""

from __future__ import annotations


def levenshtein_ratio(s1: str, s2: str) -> float:
    """Compute similarity ratio between two strings (0.0 to 1.0).

    Uses Levenshtein distance normalized by the longer string length.
    """
    if s1 == s2:
        return 1.0

    len1, len2 = len(s1), len(s2)
    if len1 == 0 or len2 == 0:
        return 0.0

    # Create distance matrix
    # Use single row optimization for memory efficiency
    prev_row = list(range(len2 + 1))
    curr_row = [0] * (len2 + 1)

    for i in range(1, len1 + 1):
        curr_row[0] = i
        for j in range(1, len2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            curr_row[j] = min(
                prev_row[j] + 1,      # deletion
                curr_row[j - 1] + 1,  # insertion
                prev_row[j - 1] + cost  # substitution
            )
        prev_row, curr_row = curr_row, prev_row

    distance = prev_row[len2]
    max_len = max(len1, len2)
    return 1.0 - (distance / max_len)


def word_overlap(
    text1: str,
    text2: str,
    stopwords: set[str] | None = None
) -> float:
    """Compute Jaccard similarity of significant words (excluding stopwords).

    Returns value between 0.0 and 1.0.
    """
    if stopwords is None:
        stopwords = set()

    words1 = set(text1.lower().split()) - stopwords
    words2 = set(text2.lower().split()) - stopwords

    if not words1 or not words2:
        return 0.0

    intersection = len(words1 & words2)
    union = len(words1 | words2)

    return intersection / union if union > 0 else 0.0


def has_continuation_keyword(text: str, keywords: list[str]) -> bool:
    """Check if text contains any continuation keyword."""
    text_lower = text.lower()
    for keyword in keywords:
        if keyword.lower() in text_lower:
            return True
    return False


def similarity_score(
    new_item: str,
    existing_item: str,
    stopwords: set[str] | None = None,
    continuation_keywords: list[str] | None = None,
) -> float:
    """Compute combined similarity score between two items.

    Score components:
    - 40% fuzzy string similarity (Levenshtein)
    - 40% word overlap (Jaccard excluding stopwords)
    - 20% bonus if new item contains continuation keyword

    Returns value between 0.0 and 1.0.
    """
    if stopwords is None:
        stopwords = set()
    if continuation_keywords is None:
        continuation_keywords = []

    # Fuzzy string similarity
    fuzzy = levenshtein_ratio(new_item, existing_item)

    # Word overlap
    overlap = word_overlap(new_item, existing_item, stopwords)

    # Continuation keyword boost
    continuation_boost = 0.2 if has_continuation_keyword(new_item, continuation_keywords) else 0.0

    return 0.4 * fuzzy + 0.4 * overlap + continuation_boost


def is_suspected_duplicate(
    new_item: str,
    existing_items: list[str],
    stopwords: set[str] | None = None,
    continuation_keywords: list[str] | None = None,
) -> tuple[bool, str | None]:
    """Check if a new item is a suspected duplicate of any existing item.

    An item is flagged as suspected duplicate if ANY of:
    A. Contains a continuation keyword
    B. >=40% significant word overlap with any existing item
    C. Levenshtein similarity >= 0.5 with any existing item

    Returns:
        (is_duplicate, reason): Boolean and reason string if duplicate
    """
    if stopwords is None:
        stopwords = set()
    if continuation_keywords is None:
        continuation_keywords = []

    # Check A: Continuation keywords
    if has_continuation_keyword(new_item, continuation_keywords):
        return True, "contains continuation keyword"

    new_words = set(new_item.lower().split()) - stopwords

    for existing in existing_items:
        # Check B: Word overlap >= 50%
        existing_words = set(existing.lower().split()) - stopwords
        if new_words and existing_words:
            intersection = len(new_words & existing_words)
            # Check overlap relative to new item's words
            if intersection / len(new_words) >= 0.4:
                return True, f"significant word overlap with '{existing}'"

        # Check C: Levenshtein >= 0.5
        ratio = levenshtein_ratio(new_item, existing)
        if ratio >= 0.5:
            return True, f"high similarity ({ratio:.0%}) with '{existing}'"

    return False, None


def rank_by_similarity(
    new_item: str,
    existing_items: list[tuple[str, str, str]],  # (normalized_text, jira_key, jira_status)
    stopwords: set[str] | None = None,
    continuation_keywords: list[str] | None = None,
    min_score: float = 0.1,
) -> list[tuple[str, str, str, float]]:
    """Rank existing items by similarity to new item.

    Returns list of (normalized_text, jira_key, jira_status, score)
    sorted by score descending, filtered to score >= min_score.
    """
    if stopwords is None:
        stopwords = set()
    if continuation_keywords is None:
        continuation_keywords = []

    scored: list[tuple[str, str, str, float]] = []

    for normalized, jira_key, jira_status in existing_items:
        score = similarity_score(
            new_item,
            normalized,
            stopwords,
            continuation_keywords,
        )
        if score >= min_score:
            scored.append((normalized, jira_key, jira_status, score))

    # Sort by score descending
    scored.sort(key=lambda x: x[3], reverse=True)

    return scored
