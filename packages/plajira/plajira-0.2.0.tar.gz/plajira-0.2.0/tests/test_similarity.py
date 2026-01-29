"""Tests for similarity module."""

import unittest

from plajira.similarity import (
    has_continuation_keyword,
    is_suspected_duplicate,
    levenshtein_ratio,
    rank_by_similarity,
    similarity_score,
    word_overlap,
)


class TestLevenshteinRatio(unittest.TestCase):
    """Tests for Levenshtein ratio calculation."""

    def test_identical_strings(self):
        """Test identical strings return 1.0."""
        self.assertEqual(levenshtein_ratio("hello", "hello"), 1.0)

    def test_empty_strings(self):
        """Test empty strings."""
        self.assertEqual(levenshtein_ratio("", ""), 1.0)
        self.assertEqual(levenshtein_ratio("hello", ""), 0.0)
        self.assertEqual(levenshtein_ratio("", "hello"), 0.0)

    def test_single_char_diff(self):
        """Test single character difference."""
        ratio = levenshtein_ratio("hello", "hallo")
        self.assertGreater(ratio, 0.7)  # Should be high similarity

    def test_completely_different(self):
        """Test completely different strings."""
        ratio = levenshtein_ratio("abc", "xyz")
        self.assertLess(ratio, 0.5)  # Should be low similarity

    def test_typo_detection(self):
        """Test typo detection has high similarity."""
        ratio = levenshtein_ratio("implement foobarbaz", "implement foobarbz")
        self.assertGreater(ratio, 0.9)


class TestWordOverlap(unittest.TestCase):
    """Tests for word overlap (Jaccard similarity)."""

    def test_identical_words(self):
        """Test identical word sets."""
        self.assertEqual(word_overlap("foo bar", "foo bar"), 1.0)

    def test_no_overlap(self):
        """Test no overlapping words."""
        self.assertEqual(word_overlap("foo bar", "baz qux"), 0.0)

    def test_partial_overlap(self):
        """Test partial overlap."""
        overlap = word_overlap("foo bar baz", "bar baz qux")
        # intersection: {bar, baz} = 2
        # union: {foo, bar, baz, qux} = 4
        # Jaccard = 2/4 = 0.5
        self.assertEqual(overlap, 0.5)

    def test_with_stopwords(self):
        """Test stopword exclusion."""
        stopwords = {"the", "a", "an"}
        overlap = word_overlap(
            "the foo bar",
            "a foo bar",
            stopwords=stopwords,
        )
        # Without stopwords: {foo, bar} vs {foo, bar} = 1.0
        self.assertEqual(overlap, 1.0)

    def test_empty_after_stopwords(self):
        """Test when all words are stopwords."""
        stopwords = {"the", "a"}
        overlap = word_overlap("the a", "the", stopwords=stopwords)
        self.assertEqual(overlap, 0.0)


class TestHasContinuationKeyword(unittest.TestCase):
    """Tests for continuation keyword detection."""

    def test_has_keyword(self):
        """Test text with continuation keyword."""
        keywords = ["continue", "finish", "complete"]
        self.assertTrue(has_continuation_keyword("continue foo work", keywords))
        self.assertTrue(has_continuation_keyword("finish the task", keywords))

    def test_no_keyword(self):
        """Test text without continuation keyword."""
        keywords = ["continue", "finish", "complete"]
        self.assertFalse(has_continuation_keyword("start new task", keywords))

    def test_case_insensitive(self):
        """Test case insensitive matching."""
        keywords = ["continue"]
        self.assertTrue(has_continuation_keyword("CONTINUE work", keywords))

    def test_keyword_as_substring(self):
        """Test keyword found as substring in text."""
        keywords = ["continue"]
        # "continue" is found as substring in "discontinue"
        self.assertTrue(has_continuation_keyword("discontinue the work", keywords))


class TestSimilarityScore(unittest.TestCase):
    """Tests for combined similarity score."""

    def test_identical_texts(self):
        """Test identical texts have high score."""
        score = similarity_score("implement foo", "implement foo")
        self.assertGreater(score, 0.7)

    def test_with_continuation_boost(self):
        """Test continuation keyword boost."""
        keywords = ["continue"]
        score_without = similarity_score("work on foo", "foo work", continuation_keywords=[])
        score_with = similarity_score("continue foo work", "foo work", continuation_keywords=keywords)

        # Score with continuation keyword should be higher due to 0.2 boost
        self.assertGreater(score_with, score_without)

    def test_different_texts(self):
        """Test different texts have lower score."""
        score = similarity_score("implement foo", "review bar")
        self.assertLess(score, 0.5)


class TestIsSuspectedDuplicate(unittest.TestCase):
    """Tests for suspected duplicate detection."""

    def test_continuation_keyword_triggers(self):
        """Test continuation keyword triggers suspected duplicate."""
        keywords = ["continue"]
        is_dup, reason = is_suspected_duplicate(
            "continue foo work",
            ["foo work"],
            continuation_keywords=keywords,
        )
        self.assertTrue(is_dup)
        self.assertIn("continuation", reason.lower())

    def test_high_word_overlap_triggers(self):
        """Test high word overlap triggers suspected duplicate."""
        is_dup, reason = is_suspected_duplicate(
            "implement foo for bar",
            ["implement foo for baz"],
        )
        self.assertTrue(is_dup)

    def test_high_levenshtein_triggers(self):
        """Test high Levenshtein similarity triggers suspected duplicate."""
        # Use single-word items to avoid word overlap triggering first
        is_dup, reason = is_suspected_duplicate(
            "foobarbaz",
            ["foobarbz"],  # typo - no word overlap, only levenshtein
        )
        self.assertTrue(is_dup)
        self.assertIn("similarity", reason.lower())

    def test_no_duplicate_for_different_text(self):
        """Test different text is not suspected duplicate."""
        is_dup, reason = is_suspected_duplicate(
            "review documentation",
            ["implement feature"],
        )
        self.assertFalse(is_dup)
        self.assertIsNone(reason)

    def test_empty_existing_items(self):
        """Test with no existing items."""
        is_dup, reason = is_suspected_duplicate("new item", [])
        self.assertFalse(is_dup)


class TestRankBySimilarity(unittest.TestCase):
    """Tests for similarity ranking."""

    def test_ranking_order(self):
        """Test items are ranked by similarity descending."""
        existing = [
            ("implement foo", "CSD-1", "Done"),
            ("review bar", "CSD-2", "Done"),
            ("implement foo bar", "CSD-3", "Done"),
        ]

        ranked = rank_by_similarity("implement foo", existing)

        # "implement foo" should be first (exact match)
        self.assertEqual(ranked[0][0], "implement foo")
        self.assertEqual(ranked[0][1], "CSD-1")

        # Scores should be descending
        scores = [r[3] for r in ranked]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_min_score_filter(self):
        """Test items below min_score are filtered."""
        existing = [
            ("completely different text", "CSD-1", "Done"),
        ]

        ranked = rank_by_similarity("implement foo", existing, min_score=0.5)

        # Should be filtered out due to low similarity
        self.assertEqual(len(ranked), 0)


if __name__ == "__main__":
    unittest.main()
