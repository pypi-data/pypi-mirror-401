"""Compute differences between .plan, state, and Jira.

Categorizes items as:
- New: Not tracked, not skipped
- Changed: Tracked, marker differs from last synced
- Skipped: In skip list
- Up to date: Tracked, no changes
- Conflicts: Jira updated more recently than plan change
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from .config import Config, TrackedItem
from .plan_parser import PlanItem
from .similarity import is_suspected_duplicate


@dataclass
class NewItem:
    """A new item not currently tracked."""
    plan_item: PlanItem
    is_suspected_duplicate: bool
    duplicate_reason: str | None = None


@dataclass
class ChangedItem:
    """A tracked item whose marker has changed."""
    plan_item: PlanItem
    item_uuid: str
    tracked_item: TrackedItem
    old_marker: str
    new_marker: str
    old_status: str      # From state
    target_status: str   # From mapping


@dataclass
class ConflictItem:
    """A tracked item where Jira was updated more recently."""
    plan_item: PlanItem
    item_uuid: str
    tracked_item: TrackedItem
    plan_change_time: datetime
    jira_change_time: datetime
    jira_status: str        # Current Jira status
    target_status: str      # What plan wants
    jira_updated_by: str    # Who updated Jira (if known)


@dataclass
class SkippedItem:
    """An item in the skip list."""
    plan_item: PlanItem


@dataclass
class UpToDateItem:
    """A tracked item with no changes needed."""
    plan_item: PlanItem
    item_uuid: str
    tracked_item: TrackedItem


@dataclass
class SyncDiff:
    """Complete diff between plan and tracked state."""
    new_items: list[NewItem] = field(default_factory=list)
    changed_items: list[ChangedItem] = field(default_factory=list)
    conflict_items: list[ConflictItem] = field(default_factory=list)
    skipped_items: list[SkippedItem] = field(default_factory=list)
    up_to_date_items: list[UpToDateItem] = field(default_factory=list)

    @property
    def total_items(self) -> int:
        """Total number of items processed."""
        return (
            len(self.new_items) +
            len(self.changed_items) +
            len(self.conflict_items) +
            len(self.skipped_items) +
            len(self.up_to_date_items)
        )

    @property
    def has_changes(self) -> bool:
        """Check if there are any items requiring action."""
        return bool(self.new_items or self.changed_items)


def compute_diff(
    plan_items: list[PlanItem],
    config: Config,
) -> SyncDiff:
    """Compute what needs to sync between plan and tracked state.

    This is a local-only diff (no Jira API calls). Conflict detection
    requires additional Jira timestamp data to be added separately.

    Args:
        plan_items: Parsed items from .plan file
        config: Configuration with tracked state

    Returns:
        SyncDiff with categorized items
    """
    diff = SyncDiff()

    # Build list of all tracked line texts for duplicate detection
    all_tracked_texts: list[str] = []
    for item in config.items.values():
        all_tracked_texts.extend(item.lines)

    for plan_item in plan_items:
        normalized = plan_item.normalized_text

        # Check if skipped
        if config.is_skipped(normalized):
            diff.skipped_items.append(SkippedItem(plan_item=plan_item))
            continue

        # Check if tracked
        found = config.find_item_by_line(normalized)

        if found is None:
            # New item - check if marker has on_new: ignore
            mapping = config.get_mapping(plan_item.marker)
            if mapping and mapping.on_new == "ignore":
                # Silently ignore - markers like + and ~ only transition existing items
                continue

            # Check for suspected duplicate
            is_dup, reason = is_suspected_duplicate(
                normalized,
                all_tracked_texts,
                config.stopwords,
                config.continuation_keywords,
            )
            diff.new_items.append(NewItem(
                plan_item=plan_item,
                is_suspected_duplicate=is_dup,
                duplicate_reason=reason,
            ))
        else:
            item_uuid, tracked_item = found

            # Check if marker changed
            if plan_item.marker != tracked_item.last_synced_marker:
                # Get target status from mapping
                mapping = config.get_mapping(plan_item.marker)
                target_status = mapping.jira_status if mapping else ""

                diff.changed_items.append(ChangedItem(
                    plan_item=plan_item,
                    item_uuid=item_uuid,
                    tracked_item=tracked_item,
                    old_marker=tracked_item.last_synced_marker,
                    new_marker=plan_item.marker,
                    old_status=tracked_item.jira_status,
                    target_status=target_status,
                ))
            else:
                diff.up_to_date_items.append(UpToDateItem(
                    plan_item=plan_item,
                    item_uuid=item_uuid,
                    tracked_item=tracked_item,
                ))

    return diff


def parse_jira_timestamp(timestamp_str: str) -> datetime:
    """Parse Jira timestamp to datetime.

    Jira uses format: 2026-01-08T16:45:00.000+0000
    """
    # Handle various Jira timestamp formats
    formats = [
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(timestamp_str, fmt)
        except ValueError:
            continue

    # Fallback: try to parse just the date/time part
    try:
        return datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
    except ValueError:
        pass

    # Last resort: return epoch
    return datetime.fromtimestamp(0)


def check_for_conflict(
    changed_item: ChangedItem,
    jira_updated: str,
    plan_commit_timestamp: int,
) -> ConflictItem | None:
    """Check if a changed item has a Jira conflict.

    Args:
        changed_item: The changed item to check
        jira_updated: Jira 'updated' timestamp string
        plan_commit_timestamp: Unix timestamp of the git commit

    Returns:
        ConflictItem if Jira was updated more recently, None otherwise
    """
    jira_time = parse_jira_timestamp(jira_updated)
    plan_time = datetime.fromtimestamp(plan_commit_timestamp, tz=timezone.utc)

    # Make both timezone-naive for comparison (all in UTC)
    if jira_time.tzinfo is not None:
        jira_time = jira_time.replace(tzinfo=None)
    plan_time = plan_time.replace(tzinfo=None)

    if jira_time > plan_time:
        return ConflictItem(
            plan_item=changed_item.plan_item,
            item_uuid=changed_item.item_uuid,
            tracked_item=changed_item.tracked_item,
            plan_change_time=plan_time,
            jira_change_time=jira_time,
            jira_status=changed_item.old_status,
            target_status=changed_item.target_status,
            jira_updated_by="",  # Would need additional API call
        )

    return None
