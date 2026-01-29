"""Tests for diff module."""

import unittest
from datetime import datetime

from plajira.config import Config, TrackedItem
from plajira.diff import (
    ChangedItem,
    check_for_conflict,
    compute_diff,
    parse_jira_timestamp,
)
from plajira.plan_parser import PlanItem


class TestParseJiraTimestamp(unittest.TestCase):
    """Tests for Jira timestamp parsing."""

    def test_standard_format(self):
        """Test standard Jira timestamp format."""
        ts = parse_jira_timestamp("2026-01-08T16:45:00.000+0000")
        self.assertEqual(ts.year, 2026)
        self.assertEqual(ts.month, 1)
        self.assertEqual(ts.day, 8)

    def test_without_milliseconds(self):
        """Test timestamp without milliseconds."""
        ts = parse_jira_timestamp("2026-01-08T16:45:00+0000")
        self.assertEqual(ts.year, 2026)

    def test_utc_format(self):
        """Test UTC Z format."""
        ts = parse_jira_timestamp("2026-01-08T16:45:00Z")
        self.assertEqual(ts.year, 2026)


class TestComputeDiff(unittest.TestCase):
    """Tests for diff computation."""

    def test_new_item(self):
        """Test new item detection."""
        config = Config()
        items = [
            PlanItem(
                marker="?",
                raw_text="new task",
                normalized_text="new task",
                date="2026-01-08",
                line_number=1,
            )
        ]

        diff = compute_diff(items, config)

        self.assertEqual(len(diff.new_items), 1)
        self.assertEqual(diff.new_items[0].plan_item.normalized_text, "new task")

    def test_tracked_unchanged(self):
        """Test tracked item with no changes."""
        config = Config()
        config.add_item(
            normalized_text="tracked task",
            jira_issue_key="TEST-1",
            jira_status="In Progress",
            marker="?",
            date="2026-01-07",
            commit="abc",
        )

        items = [
            PlanItem(
                marker="?",
                raw_text="tracked task",
                normalized_text="tracked task",
                date="2026-01-08",
                line_number=1,
            )
        ]

        diff = compute_diff(items, config)

        self.assertEqual(len(diff.up_to_date_items), 1)
        self.assertEqual(len(diff.changed_items), 0)

    def test_tracked_changed(self):
        """Test tracked item with marker change."""
        config = Config()
        config.add_item(
            normalized_text="tracked task",
            jira_issue_key="TEST-1",
            jira_status="In Progress",
            marker="?",
            date="2026-01-07",
            commit="abc",
        )
        # Add mapping for the new marker
        from plajira.config import MarkerMapping
        config.mappings["*"] = MarkerMapping(
            description="Done",
            jira_status="Done",
            on_new="create",
        )

        items = [
            PlanItem(
                marker="*",  # Changed from ? to *
                raw_text="tracked task",
                normalized_text="tracked task",
                date="2026-01-08",
                line_number=1,
            )
        ]

        diff = compute_diff(items, config)

        self.assertEqual(len(diff.changed_items), 1)
        self.assertEqual(diff.changed_items[0].old_marker, "?")
        self.assertEqual(diff.changed_items[0].new_marker, "*")
        self.assertEqual(diff.changed_items[0].target_status, "Done")

    def test_skipped_item(self):
        """Test skipped item detection."""
        config = Config()
        config.add_to_skip("lunch")

        items = [
            PlanItem(
                marker="*",
                raw_text="lunch",
                normalized_text="lunch",
                date="2026-01-08",
                line_number=1,
            )
        ]

        diff = compute_diff(items, config)

        self.assertEqual(len(diff.skipped_items), 1)
        self.assertEqual(len(diff.new_items), 0)

    def test_suspected_duplicate(self):
        """Test suspected duplicate flagging."""
        config = Config()
        config.continuation_keywords = ["continue"]
        config.add_item(
            normalized_text="implement foo",
            jira_issue_key="TEST-1",
            jira_status="In Progress",
            marker="?",
            date="2026-01-07",
            commit="abc",
        )

        items = [
            PlanItem(
                marker="?",
                raw_text="continue foo work",
                normalized_text="continue foo work",
                date="2026-01-08",
                line_number=1,
            )
        ]

        diff = compute_diff(items, config)

        self.assertEqual(len(diff.new_items), 1)
        self.assertTrue(diff.new_items[0].is_suspected_duplicate)


class TestCheckForConflict(unittest.TestCase):
    """Tests for conflict detection."""

    def test_no_conflict_plan_newer(self):
        """Test no conflict when plan is newer."""
        changed = ChangedItem(
            plan_item=PlanItem(
                marker="*",
                raw_text="task",
                normalized_text="task",
                date="2026-01-08",
                line_number=1,
            ),
            item_uuid="uuid-1",
            tracked_item=TrackedItem(
                jira_issue_key="TEST-1",
                jira_status="In Progress",
                lines=["task"],
                last_synced_marker="?",
                last_synced_date="2026-01-07",
                last_synced_commit="abc",
                last_synced_timestamp="2026-01-07T00:00:00Z",
            ),
            old_marker="?",
            new_marker="*",
            old_status="In Progress",
            target_status="Done",
        )

        # Plan change at timestamp 1704844800 (2024-01-10)
        # Jira updated earlier
        conflict = check_for_conflict(
            changed,
            jira_updated="2024-01-08T00:00:00Z",
            plan_commit_timestamp=1704844800,
        )

        self.assertIsNone(conflict)

    def test_conflict_jira_newer(self):
        """Test conflict when Jira is newer."""
        changed = ChangedItem(
            plan_item=PlanItem(
                marker="*",
                raw_text="task",
                normalized_text="task",
                date="2026-01-08",
                line_number=1,
            ),
            item_uuid="uuid-1",
            tracked_item=TrackedItem(
                jira_issue_key="TEST-1",
                jira_status="In Progress",
                lines=["task"],
                last_synced_marker="?",
                last_synced_date="2026-01-07",
                last_synced_commit="abc",
                last_synced_timestamp="2026-01-07T00:00:00Z",
            ),
            old_marker="?",
            new_marker="*",
            old_status="In Progress",
            target_status="Done",
        )

        # Plan change at timestamp 1704672000 (2024-01-08)
        # Jira updated later
        conflict = check_for_conflict(
            changed,
            jira_updated="2024-01-10T00:00:00Z",
            plan_commit_timestamp=1704672000,
        )

        self.assertIsNotNone(conflict)
        self.assertEqual(conflict.item_uuid, "uuid-1")


if __name__ == "__main__":
    unittest.main()
