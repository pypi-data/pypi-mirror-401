# plajira

Sync your `.plan` file with Jira Cloud.

plajira is a command-line tool that bridges your personal `.plan` file with Jira, keeping your task tracking in sync without leaving your editor.

## Features

- **Zero intrusion**: Your `.plan` file is never modified by plajira
- **Git-aware**: Only syncs items from commits that have been pushed
- **Timestamp-aware**: Detects conflicts when Jira was updated more recently
- **Interactive**: Every action requires confirmation
- **Portable**: Python standard library only (no external dependencies)

## Installation

```bash
pip install plajira
```

Or install from source:

```bash
git clone https://github.com/plajira/plajira.git
cd plajira
pip install -e .
```

## Quick Start

1. Initialize plajira in a directory containing your `.plan` file:

```bash
plajira init
```

2. Copy `.env.example` to `.env` and add your Jira credentials:

```bash
cp .env.example .env
# Edit .env with your Jira URL, email, and API token
```

3. Run your first sync:

```bash
plajira sync
```

## .plan File Format

```
> 2026-01-07
* foo feedback
+ implement bar
! review baz spreadsheet
? begin legend mode implementation

> 2026-01-08
* touch base on foo feedback
* implement bar
? continue legend mode implementation
~ old abandoned idea
```

### Markers

| Marker | Meaning | Jira Status | Creates new issue? |
|--------|---------|-------------|-------------------|
| `?` | In progress / planned | In Progress | Yes |
| `*` | Accomplished that day | Done | Yes |
| `!` | Idea for future work | Backlog | Yes |
| `+` | Accomplished later (was `?`) | Done | No - transitions only |
| `~` | Abandoned (was `?`) | Won't Do | No - transitions only |

Note: `+` and `~` are for transitioning items that were previously tracked as `?`. They won't create new Jira issues.

## Commands

### `plajira init`

Initialize plajira configuration in the current directory.

### `plajira status`

Preview what would happen on sync, with an interactive menu.

```
$ plajira status

Checking .plan for duplicate lines... OK
Parsing .plan... 34 items
Checking git status... all commits

New items:
  • "research spec" [SUSPECTED DUPLICATE]
  • "baz spreadsheet"

Status changes:
  • CSD-42 "implement foobar": In Progress -> Done

Skipped: 3  Up to date: 28

[s] Sync  [v] View skip list  [l] List tracked  [q] Quit
```

Press `v` to view the skip list, then `u` to unskip items interactively.

### `plajira sync`

Synchronize your `.plan` with Jira.

```
$ plajira sync

New item: "implement foobar"

  [y] Create new Jira issue
  [n] Not now (ask again next sync)
  [d] Duplicate - link to existing item
  [s] Skip (don't track in Jira)

Choice [y]: y

✓ Created CSD-72 "implement foobar"
```

### `plajira link <text> <jira-key>`

Manually link a `.plan` line to an existing Jira issue.

```
$ plajira link "implement foobar" CSD-42

Fetching CSD-42... found: "Implement foobar" (In Progress)

Link "implement foobar" -> CSD-42? [y/N]: y

✓ Linked.
```

### `plajira unlink <text>`

Remove tracking for a line (doesn't affect Jira).

### `plajira list`

Show all tracked items and skip list.

### `plajira unskip <text>`

Remove a line from the skip list.

## Configuration

Configuration is stored in `.plajira` (YAML format). Credentials are in `.env`.

### .env

```
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_TOKEN=your-api-token
```

Get your API token from: https://id.atlassian.com/manage-profile/security/api-tokens

### .plajira

The configuration file has two sections:

1. **config** (user-editable): Jira settings, marker mappings, keywords
2. **state** (managed by plajira): Tracked items and skip list

## Duplicate Detection

plajira automatically detects suspected duplicates using:

- Continuation keywords ("continue", "finish", etc.)
- Word overlap (≥50% of significant words)
- Fuzzy matching (Levenshtein similarity ≥60%)

When a suspected duplicate is found, you can link it to an existing item instead of creating a new Jira issue.

## Conflict Resolution

If someone else updates a Jira issue after you changed your `.plan`, plajira detects the conflict:

```
⚠️  CONFLICT: "implement foo" (CSD-42)

Your .plan shows: * (Done)
  Changed: 2026-01-08 14:32

Jira shows: Blocked
  Changed: 2026-01-08 16:45

Jira was updated MORE RECENTLY than your .plan change.

  [s] Skip this item (recommended)
  [v] View Jira issue in browser
  [o] Override: force .plan status to Jira (dangerous!)

Choice [s/v/o]:
```

## Requirements

- Python 3.8+
- Git repository with a remote tracking branch
- Jira Cloud account with API access

## License

MIT
