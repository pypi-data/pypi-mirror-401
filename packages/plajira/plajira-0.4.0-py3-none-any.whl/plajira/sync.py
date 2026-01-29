"""Core sync logic for plajira.

Handles:
- Processing new items (create/skip/link)
- Status transitions
- Conflict resolution
- Commit message selection
- Execution with progress reporting
"""

from __future__ import annotations

import webbrowser
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from . import ui
from .config import Config, save_config
from .diff import (
    ChangedItem,
    ConflictItem,
    NewItem,
    SyncDiff,
    check_for_conflict,
    parse_jira_timestamp,
)
from .git_reader import CommitInfo, find_commits_touching_line, get_commit_timestamp
from .jira_client import JiraClient, JiraError
from .similarity import rank_by_similarity

if TYPE_CHECKING:
    from .plan_parser import PlanItem


@dataclass
class CreateAction:
    """Action to create a new Jira issue."""
    plan_item: "PlanItem"
    project_key: str
    issue_type: str
    target_status: str
    labels: list[str]
    description: str = ""
    # Linked lines that will share the same UUID
    linked_lines: list[str] = field(default_factory=list)


@dataclass
class TransitionAction:
    """Action to transition a Jira issue."""
    plan_item: "PlanItem"
    item_uuid: str
    jira_key: str
    from_status: str
    to_status: str
    comment: str = ""


@dataclass
class LinkAction:
    """Action to link a line to an existing item (no Jira change)."""
    normalized_text: str
    item_uuid: str
    jira_key: str


@dataclass
class SyncPlan:
    """Planned sync actions."""
    creates: list[CreateAction] = field(default_factory=list)
    transitions: list[TransitionAction] = field(default_factory=list)
    links: list[LinkAction] = field(default_factory=list)
    skipped_conflicts: list[ConflictItem] = field(default_factory=list)
    skipped_new: list[NewItem] = field(default_factory=list)  # Items user said "not now"

    @property
    def has_actions(self) -> bool:
        """Check if there are any actions to execute."""
        return bool(self.creates or self.transitions or self.links)


def _get_commits_for_item(
    plan_item: "PlanItem",
    plan_file: str,
) -> list[CommitInfo]:
    """Get commits that touched an item's line."""
    # Search for the normalized text in diffs
    return find_commits_touching_line(
        plan_file,
        plan_item.normalized_text,
        pushed_only=True,
    )


def _select_commit_messages(
    commits: list[CommitInfo],
    item_text: str,
) -> str:
    """Interactively select commit messages to include as comment."""
    if not commits:
        return ""

    if len(commits) == 1:
        # Single commit - use automatically
        return commits[0].message

    # Multiple commits - let user select
    print(f"\n{ui.dim('The following commits touched this item:')}")
    for i, commit in enumerate(commits, 1):
        print(f"  [{i}] {ui.dim(commit.short_hash)} ({commit.date_str}): \"{commit.message}\"")

    selected = ui.prompt_select_numbers(
        "\nSelect messages to include in Jira comment",
        len(commits),
        default=str(len(commits)),  # Default to most recent
    )

    if selected is None:
        return ""

    messages = [commits[i - 1].message for i in selected]
    return "\n\n".join(messages)


def _handle_new_item(
    new_item: NewItem,
    config: Config,
    jira: JiraClient,
    plan_file: str,
    pending_creates: list[CreateAction],
    gojira: bool = False,
) -> CreateAction | LinkAction | None:
    """Handle a new item interactively.

    Returns:
        - CreateAction if user wants to create
        - LinkAction if user links to existing
        - None if user skips or defers
    """
    text = new_item.plan_item.normalized_text
    marker = new_item.plan_item.marker

    # Show the item
    dup_tag = f" {ui.warning('[SUSPECTED DUPLICATE]')}" if new_item.is_suspected_duplicate else ""
    print(f"\n{ui.bold('New item:')} \"{text}\"{dup_tag}")

    mapping = config.get_mapping(marker)

    # Check on_new policy
    if mapping and mapping.on_new == "ignore":
        print(f"  {ui.dim(f'Marker {marker} has on_new=ignore, skipping.')}")
        return None

    # In gojira mode, auto-create unless it's a suspected duplicate
    if gojira and not new_item.is_suspected_duplicate:
        choice = "y"
        print(f"  {ui.gojira('Auto-creating...')}")
    else:
        choices = [
            ("y", "Create new Jira issue"),
            ("n", "Not now (ask again next sync)"),
            ("d", "Duplicate - link to existing item"),
            ("s", "Skip (don't track in Jira)"),
        ]
        choice = ui.prompt_choices("", choices, default="y" if not new_item.is_suspected_duplicate else "d")

    if choice == "y":
        # Create new issue
        project_key = (mapping.project_key if mapping and mapping.project_key
                       else config.defaults.project_key)
        issue_type = (mapping.issue_type if mapping and mapping.issue_type
                      else config.defaults.issue_type)
        target_status = mapping.jira_status if mapping else ""
        labels = mapping.labels if mapping else []

        # Get commit messages for description
        commits = _get_commits_for_item(new_item.plan_item, plan_file)
        description = _select_commit_messages(commits, text) if commits else ""

        return CreateAction(
            plan_item=new_item.plan_item,
            project_key=project_key,
            issue_type=issue_type,
            target_status=target_status,
            labels=labels,
            description=description,
        )

    elif choice == "d":
        # Link to existing
        return _handle_duplicate_linking(new_item, config, jira, pending_creates)

    elif choice == "s":
        # Skip - ask if permanent
        always = ui.prompt_yes_no(f"Always skip \"{ui.truncate(text, 40)}\"?", default=False)
        if always:
            config.add_to_skip(text)
            save_config(config)
            print(f"  {ui.dim('Added to skip list.')}")
        return None

    else:  # choice == "n"
        return None


def _handle_duplicate_linking(
    new_item: NewItem,
    config: Config,
    jira: JiraClient,
    pending_creates: list[CreateAction],
) -> LinkAction | CreateAction | None:
    """Handle linking a suspected duplicate to an existing item."""
    text = new_item.plan_item.normalized_text

    # Build list of existing items for ranking
    existing_items: list[tuple[str, str, str]] = []

    # Add tracked items
    for item_uuid, item in config.items.items():
        for line in item.lines:
            existing_items.append((line, item.jira_issue_key, item.jira_status))

    # Add pending creates (not yet in Jira)
    for create in pending_creates:
        existing_items.append((create.plan_item.normalized_text, "(pending)", create.target_status))

    if not existing_items:
        print(f"  {ui.dim('No existing items to link to.')}")
        return _fallback_after_duplicate(new_item, config, jira)

    # Rank by similarity
    ranked = rank_by_similarity(
        text,
        existing_items,
        config.stopwords,
        config.continuation_keywords,
        min_score=0.1,
    )

    if not ranked:
        print(f"  {ui.dim('No similar items found.')}")
        return _fallback_after_duplicate(new_item, config, jira)

    print(f"\n{ui.dim('Possible matches (ranked by similarity):')}")

    for i, (line_text, jira_key, status, score) in enumerate(ranked[:5], 1):
        status_str = ui.format_status(status) if jira_key != "(pending)" else ui.dim("(pending)")
        key_str = ui.format_issue_key(jira_key) if jira_key != "(pending)" else ui.dim("(pending)")
        print(f"\n[{i}] \"{line_text}\" ({key_str}, {status_str}) - score: {score:.2f}")

        link_this = ui.prompt_yes_no(f"    Link \"{ui.truncate(text, 30)}\" to this?", default=False)

        if link_this:
            if jira_key == "(pending)":
                # Link to pending create
                for create in pending_creates:
                    if create.plan_item.normalized_text == line_text:
                        create.linked_lines.append(text)
                        print(f"  {ui.dim('Linked. Both lines will share the same Jira issue.')}")
                        # Return a marker that we handled it via pending create
                        return LinkAction(
                            normalized_text=text,
                            item_uuid="",  # Will be set when create executes
                            jira_key="(pending)",
                        )
            else:
                # Link to existing tracked item
                found = config.find_item_by_line(line_text)
                if found:
                    item_uuid, _ = found
                    config.link_line_to_item(text, item_uuid)
                    print(f"  {ui.dim(f'Linked. \"{ui.truncate(text, 30)}\" now tracks {jira_key}.')}")
                    return LinkAction(
                        normalized_text=text,
                        item_uuid=item_uuid,
                        jira_key=jira_key,
                    )

    # User rejected all matches
    print(f"\n{ui.dim('No match selected.')}")
    return _fallback_after_duplicate(new_item, config, jira)


def _fallback_after_duplicate(
    new_item: NewItem,
    config: Config,
    jira: JiraClient,
) -> CreateAction | None:
    """Fallback options after user rejects duplicate matches."""
    choices = [
        ("y", "Create new Jira issue"),
        ("n", "Not now (ask again next sync)"),
        ("s", "Skip (don't track in Jira)"),
    ]

    choice = ui.prompt_choices("", choices, default="n")

    if choice == "y":
        marker = new_item.plan_item.marker
        mapping = config.get_mapping(marker)

        project_key = (mapping.project_key if mapping and mapping.project_key
                       else config.defaults.project_key)
        issue_type = (mapping.issue_type if mapping and mapping.issue_type
                      else config.defaults.issue_type)
        target_status = mapping.jira_status if mapping else ""
        labels = mapping.labels if mapping else []

        return CreateAction(
            plan_item=new_item.plan_item,
            project_key=project_key,
            issue_type=issue_type,
            target_status=target_status,
            labels=labels,
        )

    elif choice == "s":
        text = new_item.plan_item.normalized_text
        always = ui.prompt_yes_no(f"Always skip \"{ui.truncate(text, 40)}\"?", default=False)
        if always:
            config.add_to_skip(text)
            save_config(config)
            print(f"  {ui.dim('Added to skip list.')}")

    return None


def _handle_changed_item(
    changed: ChangedItem,
    config: Config,
    jira: JiraClient,
    plan_file: str,
) -> TransitionAction | ConflictItem | None:
    """Handle a status change, checking for conflicts."""
    # Fetch current Jira state
    try:
        issue = jira.get_issue(changed.tracked_item.jira_issue_key)
    except JiraError as e:
        if e.status_code == 404:
            print(f"\n{ui.warning(f'Issue {changed.tracked_item.jira_issue_key} not found in Jira (deleted?)')}")
            print(f"  \"{changed.plan_item.normalized_text}\"")
            choice = ui.prompt_choices(
                "What would you like to do?",
                [
                    ("u", "Unlink (stop tracking this item)"),
                    ("s", "Skip for now"),
                ],
            )
            if choice == "u":
                config.unlink_line(changed.plan_item.normalized_text)
                save_config(config)
                print(f"  {ui.dim('Removed from tracking.')}")
            return None
        raise

    # Get commit timestamp for this change
    commits = _get_commits_for_item(changed.plan_item, plan_file)
    if not commits:
        # No pushed commits touch this item - skip it
        print(f"  {ui.dim('No pushed commits for this item yet. Push your changes first.')}")
        return None

    plan_timestamp = commits[0].timestamp

    # Check for conflict
    conflict = check_for_conflict(changed, issue.updated, plan_timestamp)

    if conflict:
        # Update conflict with actual Jira status
        conflict.jira_status = issue.status
        return conflict

    # No conflict - prepare transition
    comment = _select_commit_messages(commits, changed.plan_item.normalized_text)

    return TransitionAction(
        plan_item=changed.plan_item,
        item_uuid=changed.item_uuid,
        jira_key=changed.tracked_item.jira_issue_key,
        from_status=issue.status,
        to_status=changed.target_status,
        comment=comment,
    )


def _handle_conflict(
    conflict: ConflictItem,
    jira: JiraClient,
) -> TransitionAction | None:
    """Handle a conflict interactively."""
    print(f"\n{ui.warning_mark()} {ui.bold('CONFLICT:')} \"{conflict.plan_item.normalized_text}\" ({ui.format_issue_key(conflict.tracked_item.jira_issue_key)})")
    print()
    print(f"  Your .plan shows: {ui.format_marker(conflict.plan_item.marker)} ({conflict.target_status})")
    print(f"    Changed: {conflict.plan_change_time.strftime('%Y-%m-%d %H:%M')}")
    print()
    print(f"  Jira shows: {ui.format_status(conflict.jira_status)}")
    print(f"    Changed: {conflict.jira_change_time.strftime('%Y-%m-%d %H:%M')}")
    print()
    print(f"  {ui.dim('Jira was updated MORE RECENTLY than your .plan change.')}")

    choices = [
        ("s", "Skip this item (recommended)"),
        ("v", "View Jira issue in browser"),
        ("o", "Override: force .plan status to Jira (dangerous!)"),
    ]

    while True:
        choice = ui.prompt_choices("", choices, default="s")

        if choice == "s":
            return None

        elif choice == "v":
            url = jira.get_issue_url(conflict.tracked_item.jira_issue_key)
            print(f"  Opening: {url}")
            webbrowser.open(url)
            # Continue loop to let user choose again

        elif choice == "o":
            confirmed = ui.prompt_confirm(
                f"Are you SURE you want to override?\n"
                f"This will change {conflict.tracked_item.jira_issue_key} from "
                f"\"{conflict.jira_status}\" to \"{conflict.target_status}\".",
                confirm_text="override",
            )
            if confirmed:
                return TransitionAction(
                    plan_item=conflict.plan_item,
                    item_uuid=conflict.item_uuid,
                    jira_key=conflict.tracked_item.jira_issue_key,
                    from_status=conflict.jira_status,
                    to_status=conflict.target_status,
                )
            # If not confirmed, continue loop


def build_sync_plan(
    diff: SyncDiff,
    config: Config,
    jira: JiraClient,
    plan_file: str,
    gojira: bool = False,
) -> SyncPlan:
    """Build a sync plan by processing diff items interactively."""
    plan = SyncPlan()
    pending_creates: list[CreateAction] = []

    # Phase 1: Handle new items
    if diff.new_items:
        ui.print_header(f"Processing {len(diff.new_items)} new items")

        for new_item in diff.new_items:
            result = _handle_new_item(new_item, config, jira, plan_file, pending_creates, gojira=gojira)

            if isinstance(result, CreateAction):
                pending_creates.append(result)
            elif isinstance(result, LinkAction):
                if result.jira_key != "(pending)":
                    plan.links.append(result)
                # (pending) links are handled via pending_creates.linked_lines
            else:
                plan.skipped_new.append(new_item)

    plan.creates = pending_creates

    # Phase 2: Handle status changes
    if diff.changed_items:
        ui.print_header(f"Processing {len(diff.changed_items)} status changes")

        for changed in diff.changed_items:
            print(f"\n{ui.bullet()} {ui.format_issue_key(changed.tracked_item.jira_issue_key)} "
                  f"\"{ui.truncate(changed.plan_item.normalized_text, 40)}\": "
                  f"{ui.format_marker(changed.old_marker)} {ui.dim('->')} {ui.format_marker(changed.new_marker)}")

            result = _handle_changed_item(changed, config, jira, plan_file)

            if isinstance(result, TransitionAction):
                plan.transitions.append(result)
            elif isinstance(result, ConflictItem):
                # Handle conflict
                resolution = _handle_conflict(result, jira)
                if resolution:
                    plan.transitions.append(resolution)
                else:
                    plan.skipped_conflicts.append(result)

    return plan


def show_sync_summary(plan: SyncPlan, config: Config, gojira: bool = False) -> bool:
    """Show sync summary and prompt for confirmation."""
    if not plan.has_actions:
        print(f"\n{ui.dim('Nothing to sync.')}")
        return False

    print(f"\n{ui.bold('plajira sync: Ready to update Jira')}")
    print("=" * 40)

    if plan.creates:
        print(f"\n{ui.bold(f'CREATE ({len(plan.creates)} issues):')}")
        for create in plan.creates:
            linked_count = len(create.linked_lines)
            linked_str = f" (+{linked_count} linked)" if linked_count else ""
            print(f"\n  {ui.bullet()} \"{create.plan_item.normalized_text}\"{linked_str}")
            print(f"    -> {create.project_key} / {create.issue_type} / {create.target_status}")
            if create.labels:
                print(f"    Labels: {create.labels}")
            if create.description:
                desc_preview = ui.truncate(create.description.replace("\n", " "), 60)
                print(f"    Description: \"{desc_preview}\"")

    if plan.transitions:
        print(f"\n{ui.bold(f'TRANSITION ({len(plan.transitions)} issues):')}")
        for trans in plan.transitions:
            print(f"\n  {ui.bullet()} {ui.format_issue_key(trans.jira_key)} \"{ui.truncate(trans.plan_item.normalized_text, 40)}\"")
            print(f"    {ui.format_status(trans.from_status)} -> {ui.format_status(trans.to_status)}")
            if trans.comment:
                comment_preview = ui.truncate(trans.comment.replace("\n", " "), 60)
                print(f"    Comment: \"{comment_preview}\"")

    if plan.links:
        print(f"\n{ui.bold(f'LINK ({len(plan.links)} items):')}")
        for link in plan.links:
            print(f"  {ui.bullet()} \"{link.normalized_text}\" -> {ui.format_issue_key(link.jira_key)}")

    if plan.skipped_conflicts:
        print(f"\n{ui.bold(f'SKIP ({len(plan.skipped_conflicts)} conflicts):')}")
        for conflict in plan.skipped_conflicts:
            print(f"  {ui.bullet()} {ui.format_issue_key(conflict.tracked_item.jira_issue_key)} "
                  f"\"{ui.truncate(conflict.plan_item.normalized_text, 40)}\"")
            print(f"    {ui.dim('Jira updated more recently')}")

    print("\n" + "-" * 40)
    if gojira:
        print(ui.gojira("Auto-confirming..."))
        return True
    return ui.prompt_yes_no("Proceed with updates?", default=False)


def execute_sync(
    plan: SyncPlan,
    config: Config,
    jira: JiraClient,
    config_path: str,
    gojira: bool = False,
) -> tuple[int, int]:
    """Execute the sync plan.

    Returns:
        (success_count, failure_count)
    """
    successes = 0
    failures = 0

    # Execute creates
    for create in plan.creates:
        try:
            issue_key = jira.create_issue(
                project_key=create.project_key,
                summary=create.plan_item.raw_text,  # Use raw text for Jira summary
                issue_type=create.issue_type,
                description=create.description or None,
                labels=create.labels or None,
            )

            # Add to state
            item_uuid = config.add_item(
                normalized_text=create.plan_item.normalized_text,
                jira_issue_key=issue_key,
                jira_status=create.target_status,
                marker=create.plan_item.marker,
                date=create.plan_item.date,
                commit="",  # TODO: get from git
            )

            # Link additional lines
            for linked_text in create.linked_lines:
                config.link_line_to_item(linked_text, item_uuid)

            # Try to transition to target status if not default
            # (New issues usually start in "To Do" or similar)
            if create.target_status:
                try:
                    trans = jira.find_transition_to_status(issue_key, create.target_status)
                    if trans:
                        jira.transition_issue(issue_key, trans.id)
                except JiraError:
                    # Non-fatal - issue created but may be in wrong status
                    pass

            ui.print_success(f"Created {ui.format_issue_key(issue_key)} \"{create.plan_item.raw_text}\"")
            successes += 1

            # Save state after each success
            save_config(config, config_path)

        except JiraError as e:
            ui.print_error(f"Failed to create \"{create.plan_item.raw_text}\": {e}")
            failures += 1

    # Execute transitions
    for trans in plan.transitions:
        try:
            # Find the transition
            jira_trans = jira.find_transition_to_status(trans.jira_key, trans.to_status)

            if not jira_trans:
                # Transition not available - in gojira mode, auto-retry once
                if gojira:
                    print(f"\n{ui.warning_mark()} Cannot transition {ui.format_issue_key(trans.jira_key)} to \"{trans.to_status}\"")
                    print(f"  {ui.gojira('Auto-retrying...')}")
                    jira_trans = jira.find_transition_to_status(trans.jira_key, trans.to_status)
                    if jira_trans:
                        pass  # Continue to execute transition
                    else:
                        # Auto-retry failed, now prompt user
                        print(f"  {ui.dim('Transition still not available after retry.')}")

                if not jira_trans:
                    # Ask user what to do
                    print(f"\n{ui.warning_mark()} Cannot transition {ui.format_issue_key(trans.jira_key)} to \"{trans.to_status}\"")
                    print(f"  {ui.dim('This transition is not available from the current status.')}")

                    choices = [
                        ("s", "Skip this transition"),
                        ("v", "View issue in browser"),
                        ("r", "Retry (after manually fixing in Jira)"),
                    ]

                    while True:
                        choice = ui.prompt_choices("What would you like to do?", choices, default="s")

                        if choice == "s":
                            failures += 1
                            break
                        elif choice == "v":
                            url = jira.get_issue_url(trans.jira_key)
                            webbrowser.open(url)
                        elif choice == "r":
                            jira_trans = jira.find_transition_to_status(trans.jira_key, trans.to_status)
                            if jira_trans:
                                break
                            print(f"  {ui.dim('Transition still not available.')}")

                    if not jira_trans:
                        continue

            # Execute transition
            jira.transition_issue(trans.jira_key, jira_trans.id)

            # Add comment if present
            if trans.comment:
                try:
                    jira.add_comment(trans.jira_key, trans.comment)
                except JiraError:
                    # Non-fatal
                    pass

            # Update state
            config.update_item(
                item_uuid=trans.item_uuid,
                jira_status=trans.to_status,
                marker=trans.plan_item.marker,
                date=trans.plan_item.date,
                commit="",
            )

            ui.print_success(f"Transitioned {ui.format_issue_key(trans.jira_key)} to {trans.to_status}")
            successes += 1

            # Save state after each success
            save_config(config, config_path)

        except JiraError as e:
            ui.print_error(f"Failed to transition {trans.jira_key}: {e}")
            failures += 1

    # Save links (these were already added to config during interactive phase)
    if plan.links:
        for link in plan.links:
            ui.print_success(f"Linked \"{link.normalized_text}\" to {ui.format_issue_key(link.jira_key)}")
            successes += 1
        save_config(config, config_path)

    return successes, failures
