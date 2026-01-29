"""Command-line interface for plajira.

Commands:
- init: Initialize plajira in current directory
- status: Preview sync changes
- sync: Synchronize with Jira
- link: Manually link a line to Jira issue
- unlink: Remove tracking for a line
- list: Show tracked items
- unskip: Remove line from skip list
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from . import __version__, ui
from .config import (
    Config,
    create_default_config,
    create_env_example,
    load_config,
    save_config,
)
from .diff import compute_diff
from .git_reader import GitError, get_unpushed_commits, has_remote_tracking_branch, is_git_repo
from .jira_client import JiraClient, JiraError
from .plan_parser import normalize_text, parse_plan_file
from .sync import build_sync_plan, execute_sync, show_sync_summary


def find_plan_file() -> str | None:
    """Find .plan file in current directory."""
    if os.path.exists(".plan"):
        return ".plan"
    # Check for any file ending in .plan
    for f in os.listdir("."):
        if f.endswith(".plan") and os.path.isfile(f):
            return f
    return None


def cmd_init(args: argparse.Namespace) -> int:
    """Initialize plajira configuration."""
    # Check for git repo
    if not is_git_repo():
        ui.print_error("Not a git repository. plajira requires git.")
        return 1

    # Find .plan file
    plan_file = find_plan_file()
    if plan_file:
        print(f"Found: {plan_file}")
    else:
        plan_file = ui.prompt("Plan file name", default=".plan")
        if not os.path.exists(plan_file):
            ui.print_error(f"File not found: {plan_file}")
            return 1

    # Check for existing .plajira
    if os.path.exists(".plajira"):
        if not ui.prompt_yes_no("Existing .plajira found. Overwrite?", default=False):
            print("Aborted.")
            return 1

    # Get Jira configuration
    print()
    jira_url = ui.prompt("Jira URL", default="https://your-domain.atlassian.net")
    project_key = ui.prompt("Default project key", default="")

    if not jira_url or not project_key:
        ui.print_error("Jira URL and project key are required.")
        return 1

    # Create .plajira
    config_content = create_default_config(jira_url, project_key)
    with open(".plajira", "w", encoding="utf-8") as f:
        f.write(config_content)
    print(f"\n{ui.check_mark()} Created .plajira")

    # Create .env.example
    env_content = create_env_example()
    with open(".env.example", "w", encoding="utf-8") as f:
        f.write(env_content)
    print(f"{ui.check_mark()} Created .env.example")

    print(f"\n{ui.dim('Copy .env.example to .env and add your Jira credentials.')}")
    print(f"{ui.dim('Make sure to add .env to .gitignore!')}")
    print(f"\nRun '{ui.bold('plajira sync')}' to perform initial synchronization.")

    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """Show sync status without making changes."""
    # Check for git repo
    if not is_git_repo():
        ui.print_error("Not a git repository. plajira requires git.")
        return 1

    # Check for remote tracking branch
    if not has_remote_tracking_branch():
        ui.print_error("No upstream branch. Run 'git push -u origin <branch>' first.")
        return 1

    # Find plan file
    plan_file = find_plan_file()
    if not plan_file:
        ui.print_error("No .plan file found in current directory.")
        return 1

    # Load config
    try:
        config = load_config()
    except FileNotFoundError:
        ui.print_error("No .plajira file found. Run 'plajira init' first.")
        return 1

    # Check for duplicates
    print("Checking .plan for duplicate lines...", end=" ")
    items, duplicates = parse_plan_file(plan_file)

    if duplicates:
        print(ui.error("ERROR"))
        print(f"\n{ui.error('Duplicate line text found in .plan:')}")
        for dup in duplicates:
            print(f"\n  Normalized: \"{dup.normalized_text}\"")
            for line_num, date, raw_line in dup.occurrences:
                print(f"    Line {line_num} ({date}): \"{raw_line}\"")
        print(f"\n{ui.dim('Each item must have unique text. Please rename one of these lines.')}")
        return 1

    print(ui.success("OK"))

    # Parse plan
    print(f"Parsing .plan... {len(items)} items")

    # Check git status
    try:
        unpushed = get_unpushed_commits()
        pushed_count = "all" if not unpushed else f"{len(unpushed)} unpushed"
        print(f"Checking git status... {pushed_count} commits")
        if unpushed:
            ui.print_warning(f"{len(unpushed)} unpushed commits - those items won't be synced")
    except GitError as e:
        ui.print_error(str(e))
        return 1

    # Compute diff
    diff = compute_diff(items, config)

    # Show summary
    if diff.new_items:
        print(f"\n{ui.bold('New items:')}")
        for new_item in diff.new_items:
            dup_tag = " [SUSPECTED DUPLICATE]" if new_item.is_suspected_duplicate else ""
            print(f"  {ui.bullet()} \"{new_item.plan_item.normalized_text}\"{dup_tag}")

    if diff.changed_items:
        print(f"\n{ui.bold('Status changes:')}")
        for changed in diff.changed_items:
            print(f"  {ui.bullet()} {ui.format_issue_key(changed.tracked_item.jira_issue_key)} "
                  f"\"{ui.truncate(changed.plan_item.normalized_text, 40)}\": "
                  f"{changed.old_status} -> {changed.target_status}")

    # Show counts instead of full lists
    counts = []
    if diff.skipped_items:
        counts.append(f"Skipped: {len(diff.skipped_items)}")
    counts.append(f"Up to date: {len(diff.up_to_date_items)}")
    print(f"\n{ui.dim('  '.join(counts))}")

    # Interactive menu
    if diff.has_changes or diff.skipped_items or config.items:
        while True:
            options = []
            if diff.has_changes:
                options.append("[s] Sync")
            if diff.skipped_items:
                options.append("[v] View skip list")
            if config.items:
                options.append("[l] List tracked")
            options.append("[q] Quit")

            print(f"\n{ui.dim('  '.join(options))}")
            choice = ui.prompt("", default="q").lower()

            if choice == "q" or choice == "":
                break
            elif choice == "s" and diff.has_changes:
                return _run_sync_from_status(config, items, plan_file)
            elif choice == "v" and diff.skipped_items:
                _show_skip_list_interactive(config, diff)
            elif choice == "l" and config.items:
                _show_tracked_items(config)
    else:
        print(f"\n{ui.dim('Nothing to sync.')}")

    return 0


def _show_skip_list_interactive(config: Config, diff) -> None:
    """Show skip list with option to unskip."""
    skip_items = [s.plan_item.normalized_text for s in diff.skipped_items]
    page_size = 10
    page = 0
    total_pages = (len(skip_items) + page_size - 1) // page_size

    while True:
        start = page * page_size
        end = min(start + page_size, len(skip_items))
        page_items = skip_items[start:end]

        print(f"\n{ui.bold('Skip list:')} ({start + 1}-{end} of {len(skip_items)})")
        for i, text in enumerate(page_items, start + 1):
            print(f"  [{i}] \"{text}\"")

        # Build options
        opts = []
        if page > 0:
            opts.append("[p] Prev")
        if page < total_pages - 1:
            opts.append("[n] Next")
        opts.extend(["[u] Unskip", "[q] Back"])
        print(f"\n{ui.dim('  '.join(opts))}")

        choice = ui.prompt("", default="q").lower()

        if choice == "q" or choice == "":
            break
        elif choice == "n" and page < total_pages - 1:
            page += 1
        elif choice == "p" and page > 0:
            page -= 1
        elif choice == "u":
            # Prompt for which item to unskip
            try:
                num = int(ui.prompt("Enter number to unskip", default=""))
                if 1 <= num <= len(skip_items):
                    text = skip_items[num - 1]
                    config.remove_from_skip(text)
                    save_config(config)
                    ui.print_success(f"Removed \"{text}\" from skip list.")
                    break
            except ValueError:
                pass


def _show_tracked_items(config: Config) -> None:
    """Show all tracked items."""
    items_list = list(config.items.values())
    page_size = 10
    page = 0
    total_pages = max(1, (len(items_list) + page_size - 1) // page_size)

    while True:
        start = page * page_size
        end = min(start + page_size, len(items_list))
        page_items = items_list[start:end]

        print(f"\n{ui.bold('Tracked items:')} ({start + 1}-{end} of {len(items_list)})")
        for item in page_items:
            print(f"\n  {ui.format_issue_key(item.jira_issue_key)} ({ui.format_status(item.jira_status)})")
            for line in item.lines:
                print(f"    {ui.bullet()} \"{line}\"")

        # Build options
        opts = []
        if page > 0:
            opts.append("[p] Prev")
        if page < total_pages - 1:
            opts.append("[n] Next")
        opts.append("[q] Back")
        print(f"\n{ui.dim('  '.join(opts))}")

        choice = ui.prompt("", default="q").lower()

        if choice == "q" or choice == "":
            break
        elif choice == "n" and page < total_pages - 1:
            page += 1
        elif choice == "p" and page > 0:
            page -= 1


def _run_sync_from_status(config: Config, items: list, plan_file: str) -> int:
    """Run sync from status menu (config and items already loaded)."""
    # Check credentials
    if not config.jira.url or not config.jira.email or not config.jira.token:
        ui.print_error("Jira credentials not configured. Check .env file.")
        return 1

    # Initialize Jira client
    jira = JiraClient(config.jira.url, config.jira.email, config.jira.token)

    # Test connection
    print("\nConnecting to Jira...", end=" ")
    try:
        user = jira.test_connection()
        print(ui.success(f"OK (logged in as {user})"))
    except JiraError as e:
        print(ui.error("FAILED"))
        ui.print_error(f"Could not connect to Jira: {e}")
        return 1

    # Compute diff
    diff = compute_diff(items, config)

    if not diff.has_changes:
        print(f"\n{ui.dim('Nothing to sync. Everything is up to date.')}")
        return 0

    # Build sync plan
    plan = build_sync_plan(diff, config, jira, plan_file)

    # Show summary and confirm
    if not show_sync_summary(plan, config):
        print(f"\n{ui.dim('Sync cancelled. No changes made.')}")
        return 0

    # Execute
    print()
    successes, failures = execute_sync(plan, config, jira, ".plajira")

    # Final summary
    print()
    if failures == 0:
        ui.print_success(f"Sync complete. {successes} items updated.")
    else:
        ui.print_warning(f"Partial sync: {successes} succeeded, {failures} failed.")
        print(f"{ui.dim('Run plajira sync again to retry failed items.')}")

    return 0 if failures == 0 else 1


def cmd_sync(args: argparse.Namespace) -> int:
    """Synchronize .plan with Jira."""
    # Check for git repo
    if not is_git_repo():
        ui.print_error("Not a git repository. plajira requires git.")
        return 1

    # Check for remote tracking branch
    if not has_remote_tracking_branch():
        ui.print_error("No upstream branch. Run 'git push -u origin <branch>' first.")
        return 1

    # Find plan file
    plan_file = find_plan_file()
    if not plan_file:
        ui.print_error("No .plan file found in current directory.")
        return 1

    # Load config
    try:
        config = load_config()
    except FileNotFoundError:
        ui.print_error("No .plajira file found. Run 'plajira init' first.")
        return 1

    # Check credentials
    if not config.jira.url or not config.jira.email or not config.jira.token:
        ui.print_error("Jira credentials not configured. Check .env file.")
        return 1

    # Check for duplicates
    print("Checking .plan for duplicate lines...", end=" ")
    items, duplicates = parse_plan_file(plan_file)

    if duplicates:
        print(ui.error("ERROR"))
        print(f"\n{ui.error('Duplicate line text found in .plan:')}")
        for dup in duplicates:
            print(f"\n  Normalized: \"{dup.normalized_text}\"")
            for line_num, date, raw_line in dup.occurrences:
                print(f"    Line {line_num} ({date}): \"{raw_line}\"")
        print(f"\n{ui.dim('Each item must have unique text. Please rename one of these lines.')}")
        return 1

    print(ui.success("OK"))

    # Parse plan
    print(f"Parsing .plan... {len(items)} items")

    # Check git status
    try:
        unpushed = get_unpushed_commits()
        if unpushed:
            ui.print_warning(f"{len(unpushed)} unpushed commits - those items won't be synced")
    except GitError as e:
        ui.print_error(str(e))
        return 1

    # Initialize Jira client
    jira = JiraClient(config.jira.url, config.jira.email, config.jira.token)

    # Test connection
    print("Connecting to Jira...", end=" ")
    try:
        user = jira.test_connection()
        print(ui.success(f"OK (logged in as {user})"))
    except JiraError as e:
        print(ui.error("FAILED"))
        ui.print_error(f"Could not connect to Jira: {e}")
        return 1

    # Load state
    print(f"Loading state... {len(config.items)} tracked items")

    # Compute diff
    diff = compute_diff(items, config)

    if not diff.has_changes:
        print(f"\n{ui.dim('Nothing to sync. Everything is up to date.')}")
        return 0

    # Build sync plan
    plan = build_sync_plan(diff, config, jira, plan_file)

    # Show summary and confirm
    if not show_sync_summary(plan, config):
        print(f"\n{ui.dim('Sync cancelled. No changes made.')}")
        return 0

    # Execute
    print()
    successes, failures = execute_sync(plan, config, jira, ".plajira")

    # Final summary
    print()
    if failures == 0:
        ui.print_success(f"Sync complete. {successes} items updated.")
    else:
        ui.print_warning(f"Partial sync: {successes} succeeded, {failures} failed.")
        print(f"{ui.dim('Run plajira sync again to retry failed items.')}")

    return 0 if failures == 0 else 1


def cmd_link(args: argparse.Namespace) -> int:
    """Manually link a .plan line to a Jira issue."""
    # Load config
    try:
        config = load_config()
    except FileNotFoundError:
        ui.print_error("No .plajira file found. Run 'plajira init' first.")
        return 1

    # Check credentials
    if not config.jira.url or not config.jira.email or not config.jira.token:
        ui.print_error("Jira credentials not configured. Check .env file.")
        return 1

    # Normalize the line text
    line_text = normalize_text(args.line_text)
    jira_key = args.jira_key.upper()

    # Check if already tracked
    found = config.find_item_by_line(line_text)
    if found:
        _, item = found
        ui.print_error(f"\"{line_text}\" is already linked to {item.jira_issue_key}")
        return 1

    # Check if in skip list
    if config.is_skipped(line_text):
        ui.print_warning(f"\"{line_text}\" is in the skip list. Use 'plajira unskip' first.")
        return 1

    # Find plan file and verify line exists
    plan_file = find_plan_file()
    if plan_file:
        items, _ = parse_plan_file(plan_file)
        item_texts = [i.normalized_text for i in items]
        if line_text not in item_texts:
            ui.print_warning(f"\"{line_text}\" not found in .plan file (proceeding anyway)")

    # Initialize Jira client and fetch issue
    jira = JiraClient(config.jira.url, config.jira.email, config.jira.token)

    print(f"Fetching {jira_key}...", end=" ")
    try:
        issue = jira.get_issue(jira_key)
        print(ui.success(f"found: \"{issue.summary}\" ({ui.format_status(issue.status)})"))
    except JiraError as e:
        print(ui.error("FAILED"))
        ui.print_error(f"Could not fetch issue: {e}")
        return 1

    # Confirm
    if not ui.prompt_yes_no(f"\nLink \"{line_text}\" -> {jira_key}?", default=True):
        print("Aborted.")
        return 0

    # Add to state
    config.add_item(
        normalized_text=line_text,
        jira_issue_key=jira_key,
        jira_status=issue.status,
        marker="?",  # Default marker
        date="",
        commit="",
    )

    save_config(config)
    ui.print_success("Linked.")

    return 0


def cmd_unlink(args: argparse.Namespace) -> int:
    """Remove tracking for a .plan line."""
    # Load config
    try:
        config = load_config()
    except FileNotFoundError:
        ui.print_error("No .plajira file found. Run 'plajira init' first.")
        return 1

    # Normalize the line text
    line_text = normalize_text(args.line_text)

    # Check if tracked
    found = config.find_item_by_line(line_text)
    if not found:
        ui.print_error(f"\"{line_text}\" is not being tracked.")
        return 1

    _, item = found
    jira_key = item.jira_issue_key

    # Confirm
    if not ui.prompt_yes_no(f"Unlink \"{line_text}\" from {jira_key}?", default=False):
        print("Aborted.")
        return 0

    # Remove
    config.unlink_line(line_text)
    save_config(config)

    ui.print_success(f"Unlinked. {jira_key} still exists in Jira.")

    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """Show all tracked items."""
    # Load config
    try:
        config = load_config()
    except FileNotFoundError:
        ui.print_error("No .plajira file found. Run 'plajira init' first.")
        return 1

    if not config.items and not config.skip:
        print(f"{ui.dim('No tracked items or skip list entries.')}")
        return 0

    if config.items:
        _show_tracked_items(config)

    if config.skip:
        _show_skip_list(config)

    return 0


def _show_skip_list(config: Config) -> None:
    """Show skip list with pagination (non-interactive, no unskip option)."""
    page_size = 10
    page = 0
    total_pages = max(1, (len(config.skip) + page_size - 1) // page_size)

    while True:
        start = page * page_size
        end = min(start + page_size, len(config.skip))
        page_items = config.skip[start:end]

        print(f"\n{ui.bold('Skip list:')} ({start + 1}-{end} of {len(config.skip)})")
        for text in page_items:
            print(f"  {ui.bullet()} \"{text}\"")

        # Build options
        opts = []
        if page > 0:
            opts.append("[p] Prev")
        if page < total_pages - 1:
            opts.append("[n] Next")
        opts.append("[q] Back")
        print(f"\n{ui.dim('  '.join(opts))}")

        choice = ui.prompt("", default="q").lower()

        if choice == "q" or choice == "":
            break
        elif choice == "n" and page < total_pages - 1:
            page += 1
        elif choice == "p" and page > 0:
            page -= 1


def cmd_unskip(args: argparse.Namespace) -> int:
    """Remove a line from the skip list."""
    # Load config
    try:
        config = load_config()
    except FileNotFoundError:
        ui.print_error("No .plajira file found. Run 'plajira init' first.")
        return 1

    # Normalize the line text
    line_text = normalize_text(args.line_text)

    # Check if in skip list
    if not config.is_skipped(line_text):
        ui.print_error(f"\"{line_text}\" is not in the skip list.")
        return 1

    # Remove
    config.remove_from_skip(line_text)
    save_config(config)

    ui.print_success(f"Removed \"{line_text}\" from skip list.")
    print(f"{ui.dim('Will prompt on next sync if this item appears in .plan.')}")

    return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="plajira",
        description="Sync your .plan file with Jira Cloud",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"plajira {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init
    init_parser = subparsers.add_parser("init", help="Initialize plajira configuration")
    init_parser.set_defaults(func=cmd_init)

    # status
    status_parser = subparsers.add_parser("status", help="Preview sync changes")
    status_parser.set_defaults(func=cmd_status)

    # sync
    sync_parser = subparsers.add_parser("sync", help="Synchronize with Jira")
    sync_parser.set_defaults(func=cmd_sync)

    # link
    link_parser = subparsers.add_parser("link", help="Link a line to Jira issue")
    link_parser.add_argument("line_text", help="Text from .plan line (without marker)")
    link_parser.add_argument("jira_key", help="Jira issue key (e.g., CSD-42)")
    link_parser.set_defaults(func=cmd_link)

    # unlink
    unlink_parser = subparsers.add_parser("unlink", help="Remove tracking for a line")
    unlink_parser.add_argument("line_text", help="Text from .plan line")
    unlink_parser.set_defaults(func=cmd_unlink)

    # list
    list_parser = subparsers.add_parser("list", help="Show tracked items")
    list_parser.set_defaults(func=cmd_list)

    # unskip
    unskip_parser = subparsers.add_parser("unskip", help="Remove line from skip list")
    unskip_parser.add_argument("line_text", help="Text to remove from skip list")
    unskip_parser.set_defaults(func=cmd_unskip)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    try:
        return args.func(args)
    except KeyboardInterrupt:
        print(f"\n{ui.dim('Interrupted.')}")
        return 130
    except Exception as e:
        ui.print_error(f"Unexpected error: {e}")
        if os.environ.get("PLAJIRA_DEBUG"):
            raise
        return 1


if __name__ == "__main__":
    sys.exit(main())
