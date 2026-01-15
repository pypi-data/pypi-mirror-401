"""Tests for plan_parser module."""

import os
import tempfile
import unittest

from plajira.plan_parser import (
    normalize_text,
    parse_plan_file,
    validate_plan_file,
)


class TestNormalizeText(unittest.TestCase):
    """Tests for text normalization."""

    def test_basic_normalization(self):
        """Test basic lowercase and strip."""
        self.assertEqual(normalize_text("Implement Foo"), "implement foo")

    def test_collapse_spaces(self):
        """Test collapsing multiple spaces."""
        self.assertEqual(normalize_text("implement   foo   bar"), "implement foo bar")

    def test_strip_whitespace(self):
        """Test stripping leading/trailing whitespace."""
        self.assertEqual(normalize_text("  implement foo  "), "implement foo")

    def test_combined(self):
        """Test all normalizations together."""
        self.assertEqual(
            normalize_text("  Implement   FOO  "),
            "implement foo",
        )


class TestParsePlanFile(unittest.TestCase):
    """Tests for plan file parsing."""

    def setUp(self):
        """Create a temporary plan file."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def _write_plan(self, content: str) -> str:
        """Write content to a temporary plan file and return path."""
        path = os.path.join(self.temp_dir, ".plan")
        with open(path, "w") as f:
            f.write(content)
        return path

    def test_parse_basic(self):
        """Test parsing basic plan file."""
        content = """> 2026-01-07
* foo feedback
? implement bar
"""
        path = self._write_plan(content)
        items, duplicates = parse_plan_file(path)

        self.assertEqual(len(items), 2)
        self.assertEqual(len(duplicates), 0)

        self.assertEqual(items[0].marker, "*")
        self.assertEqual(items[0].normalized_text, "foo feedback")
        self.assertEqual(items[0].date, "2026-01-07")

        self.assertEqual(items[1].marker, "?")
        self.assertEqual(items[1].normalized_text, "implement bar")

    def test_parse_all_markers(self):
        """Test parsing all valid markers."""
        content = """> 2026-01-07
* accomplished
? in progress
! idea
+ done later
~ abandoned
"""
        path = self._write_plan(content)
        items, duplicates = parse_plan_file(path)

        self.assertEqual(len(items), 5)
        markers = [item.marker for item in items]
        self.assertEqual(markers, ["*", "?", "!", "+", "~"])

    def test_parse_multiple_dates(self):
        """Test parsing with multiple date headers."""
        content = """> 2026-01-07
* foo

> 2026-01-08
* bar
"""
        path = self._write_plan(content)
        items, duplicates = parse_plan_file(path)

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].date, "2026-01-07")
        self.assertEqual(items[1].date, "2026-01-08")

    def test_ignore_invalid_lines(self):
        """Test that invalid lines are ignored."""
        content = """> 2026-01-07
* valid item
this is not a valid line
# comment line
  indented text
"""
        path = self._write_plan(content)
        items, duplicates = parse_plan_file(path)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].normalized_text, "valid item")

    def test_detect_duplicates(self):
        """Test duplicate detection."""
        content = """> 2026-01-07
? implement foo

> 2026-01-08
? implement foo
"""
        path = self._write_plan(content)
        items, duplicates = parse_plan_file(path)

        self.assertEqual(len(items), 2)
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0].normalized_text, "implement foo")
        self.assertEqual(len(duplicates[0].occurrences), 2)

    def test_same_text_different_markers_is_duplicate(self):
        """Test that same text with different markers is still a duplicate."""
        content = """> 2026-01-07
? implement foo

> 2026-01-08
* implement foo
"""
        path = self._write_plan(content)
        items, duplicates = parse_plan_file(path)

        # This IS a duplicate according to the spec
        # "same exact normalized text cannot appear on multiple lines"
        self.assertEqual(len(duplicates), 1)

    def test_line_numbers(self):
        """Test that line numbers are correctly tracked."""
        content = """> 2026-01-07

* item one

* item two
"""
        path = self._write_plan(content)
        items, duplicates = parse_plan_file(path)

        self.assertEqual(items[0].line_number, 3)
        self.assertEqual(items[1].line_number, 5)


class TestValidatePlanFile(unittest.TestCase):
    """Tests for plan file validation."""

    def setUp(self):
        """Create a temporary plan file."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def _write_plan(self, content: str) -> str:
        """Write content to a temporary plan file and return path."""
        path = os.path.join(self.temp_dir, ".plan")
        with open(path, "w") as f:
            f.write(content)
        return path

    def test_valid_file(self):
        """Test validation of valid file."""
        content = """> 2026-01-07
* foo
? bar
"""
        path = self._write_plan(content)
        duplicates = validate_plan_file(path)
        self.assertEqual(len(duplicates), 0)

    def test_invalid_file_with_duplicates(self):
        """Test validation of file with duplicates."""
        content = """> 2026-01-07
* foo

> 2026-01-08
? foo
"""
        path = self._write_plan(content)
        duplicates = validate_plan_file(path)
        self.assertEqual(len(duplicates), 1)


if __name__ == "__main__":
    unittest.main()
