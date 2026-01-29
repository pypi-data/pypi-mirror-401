"""Read-only git operations for plajira.

Handles:
- Checking git repository status
- Determining pushed vs unpushed commits
- Getting commit history for plan file
- Extracting commit messages for specific lines
"""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime


class GitError(Exception):
    """Exception for git operation errors."""
    pass


@dataclass
class CommitInfo:
    """Information about a git commit."""
    hash: str          # Full commit hash
    short_hash: str    # Short commit hash (7 chars)
    timestamp: int     # Unix timestamp (author time)
    message: str       # Commit subject line
    date_str: str      # Human-readable date

    @property
    def iso_timestamp(self) -> str:
        """Get timestamp in ISO format."""
        return datetime.utcfromtimestamp(self.timestamp).strftime("%Y-%m-%dT%H:%M:%SZ")


def _run_git(args: list[str], cwd: str | None = None) -> str:
    """Run a git command and return stdout.

    Args:
        args: Git command arguments (without 'git')
        cwd: Working directory (default: current)

    Returns:
        Command stdout as string

    Raises:
        GitError: On command failure
    """
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=30,
        )
        if result.returncode != 0:
            raise GitError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
        return result.stdout
    except subprocess.TimeoutExpired:
        raise GitError(f"git {' '.join(args)} timed out")
    except FileNotFoundError:
        raise GitError("git executable not found")


def is_git_repo(path: str = ".") -> bool:
    """Check if path is inside a git repository."""
    try:
        _run_git(["rev-parse", "--git-dir"], cwd=path)
        return True
    except GitError:
        return False


def get_repo_root(path: str = ".") -> str:
    """Get the root directory of the git repository.

    Raises:
        GitError: If not in a git repository
    """
    return _run_git(["rev-parse", "--show-toplevel"], cwd=path).strip()


def has_remote_tracking_branch(path: str = ".") -> bool:
    """Check if current branch has a remote tracking branch."""
    try:
        _run_git(["rev-parse", "--abbrev-ref", "@{u}"], cwd=path)
        return True
    except GitError:
        return False


def get_remote_tracking_branch(path: str = ".") -> str:
    """Get the name of the remote tracking branch.

    Raises:
        GitError: If no tracking branch configured
    """
    return _run_git(["rev-parse", "--abbrev-ref", "@{u}"], cwd=path).strip()


def get_unpushed_commits(path: str = ".") -> list[str]:
    """Get list of commit hashes that are local but not pushed.

    Returns:
        List of commit hashes (may be empty)

    Raises:
        GitError: If no remote tracking branch
    """
    if not has_remote_tracking_branch(path):
        raise GitError(
            "No upstream branch. Run 'git push -u origin <branch>' first."
        )

    output = _run_git(["log", "@{u}..HEAD", "--format=%H"], cwd=path)
    commits = [line.strip() for line in output.strip().split("\n") if line.strip()]
    return commits


def get_pushed_commit(path: str = ".") -> str:
    """Get the commit hash of the remote tracking branch head.

    Raises:
        GitError: If no remote tracking branch
    """
    if not has_remote_tracking_branch(path):
        raise GitError(
            "No upstream branch. Run 'git push -u origin <branch>' first."
        )

    return _run_git(["rev-parse", "@{u}"], cwd=path).strip()


def get_commits_for_file(
    filepath: str,
    pushed_only: bool = True,
    path: str = ".",
) -> list[CommitInfo]:
    """Get commits that touched a specific file.

    Args:
        filepath: Path to file (relative to repo root)
        pushed_only: If True, only include pushed commits
        path: Working directory

    Returns:
        List of CommitInfo, newest first
    """
    ref = "@{u}" if pushed_only else "HEAD"

    try:
        output = _run_git(
            ["log", ref, "--format=%H|%at|%s", "--follow", "--", filepath],
            cwd=path,
        )
    except GitError:
        return []

    commits = []
    for line in output.strip().split("\n"):
        if not line.strip() or "|" not in line:
            continue

        parts = line.split("|", 2)
        if len(parts) < 3:
            continue

        commit_hash, timestamp_str, message = parts
        try:
            timestamp = int(timestamp_str)
        except ValueError:
            continue

        date_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")

        commits.append(CommitInfo(
            hash=commit_hash,
            short_hash=commit_hash[:7],
            timestamp=timestamp,
            message=message,
            date_str=date_str,
        ))

    return commits


def get_commit_diff(commit_hash: str, filepath: str, path: str = ".") -> str:
    """Get the diff for a specific file in a commit.

    Returns:
        Diff output as string
    """
    try:
        return _run_git(
            ["show", commit_hash, "--format=", "--", filepath],
            cwd=path,
        )
    except GitError:
        return ""


def find_commits_touching_line(
    filepath: str,
    line_text: str,
    pushed_only: bool = True,
    path: str = ".",
) -> list[CommitInfo]:
    """Find commits where a specific line was added or modified.

    Args:
        filepath: Path to file
        line_text: Text to search for in diffs
        pushed_only: If True, only include pushed commits
        path: Working directory

    Returns:
        List of commits that touched this line, newest first
    """
    all_commits = get_commits_for_file(filepath, pushed_only, path)

    matching_commits = []
    for commit in all_commits:
        diff = get_commit_diff(commit.hash, filepath, path)

        # Look for the line text in added lines (+ prefix)
        # Normalize both for comparison
        line_normalized = line_text.lower().strip()

        for diff_line in diff.split("\n"):
            if diff_line.startswith("+") and not diff_line.startswith("+++"):
                diff_content = diff_line[1:].strip().lower()
                # Check if this added line contains our text
                # We look for the text after stripping the marker
                if line_normalized in diff_content:
                    matching_commits.append(commit)
                    break

    return matching_commits


def get_commit_timestamp(commit_hash: str, path: str = ".") -> int:
    """Get the author timestamp for a commit.

    Returns:
        Unix timestamp
    """
    output = _run_git(["log", "-1", "--format=%at", commit_hash], cwd=path)
    return int(output.strip())


def get_file_last_commit(filepath: str, path: str = ".") -> CommitInfo | None:
    """Get the most recent commit that touched a file.

    Returns:
        CommitInfo or None if file has no history
    """
    commits = get_commits_for_file(filepath, pushed_only=False, path=path)
    return commits[0] if commits else None


def is_file_tracked(filepath: str, path: str = ".") -> bool:
    """Check if a file is tracked by git."""
    try:
        _run_git(["ls-files", "--error-unmatch", filepath], cwd=path)
        return True
    except GitError:
        return False
