"""Configuration loading and state management for plajira.

Handles:
- .env file parsing (JIRA_URL, JIRA_EMAIL, JIRA_TOKEN)
- .plajira file parsing (YAML config + JSON state)
- State persistence (preserving user's config section)
"""

from __future__ import annotations

import json
import os
import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# Marker that separates config (YAML) from state (JSON)
STATE_MARKER = "# === STATE (managed by plajira, do not edit below) ==="


@dataclass
class JiraConfig:
    """Jira connection configuration."""
    url: str = ""
    email: str = ""
    token: str = ""


@dataclass
class Defaults:
    """Default values for issue creation."""
    project_key: str = ""
    issue_type: str = "Task"


@dataclass
class MarkerMapping:
    """Configuration for a .plan marker character."""
    description: str = ""
    jira_status: str = ""
    on_new: str = "create"  # "create" or "ignore"
    project_key: str | None = None  # Override defaults
    issue_type: str | None = None   # Override defaults
    labels: list[str] = field(default_factory=list)


@dataclass
class TrackedItem:
    """State for a tracked item (UUID → Jira mapping)."""
    jira_issue_key: str
    jira_status: str
    lines: list[str]  # Normalized line texts that map to this item
    last_synced_marker: str
    last_synced_date: str
    last_synced_commit: str
    last_synced_timestamp: str  # ISO format


@dataclass
class Config:
    """Full plajira configuration and state."""
    # Config section (user-editable)
    jira: JiraConfig = field(default_factory=JiraConfig)
    defaults: Defaults = field(default_factory=Defaults)
    mappings: dict[str, MarkerMapping] = field(default_factory=dict)
    continuation_keywords: list[str] = field(default_factory=list)
    stopwords: set[str] = field(default_factory=set)

    # State section (managed by plajira)
    items: dict[str, TrackedItem] = field(default_factory=dict)  # UUID → TrackedItem
    skip: list[str] = field(default_factory=list)  # Normalized texts to skip

    # Internal: raw config text for preservation
    _config_text: str = ""

    def get_mapping(self, marker: str) -> MarkerMapping | None:
        """Get mapping for a marker character."""
        return self.mappings.get(marker)

    def find_item_by_line(self, normalized_text: str) -> tuple[str, TrackedItem] | None:
        """Find tracked item containing this normalized line text.

        Returns (uuid, item) or None if not found.
        """
        for item_uuid, item in self.items.items():
            if normalized_text in item.lines:
                return (item_uuid, item)
        return None

    def is_skipped(self, normalized_text: str) -> bool:
        """Check if this text is in the skip list."""
        return normalized_text in self.skip

    def add_item(
        self,
        normalized_text: str,
        jira_issue_key: str,
        jira_status: str,
        marker: str,
        date: str,
        commit: str,
    ) -> str:
        """Add a new tracked item. Returns the generated UUID."""
        item_uuid = str(uuid.uuid4())
        self.items[item_uuid] = TrackedItem(
            jira_issue_key=jira_issue_key,
            jira_status=jira_status,
            lines=[normalized_text],
            last_synced_marker=marker,
            last_synced_date=date,
            last_synced_commit=commit,
            last_synced_timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        return item_uuid

    def link_line_to_item(self, normalized_text: str, item_uuid: str) -> None:
        """Add a line text to an existing item's lines list."""
        if item_uuid in self.items:
            if normalized_text not in self.items[item_uuid].lines:
                self.items[item_uuid].lines.append(normalized_text)

    def add_to_skip(self, normalized_text: str) -> None:
        """Add text to skip list."""
        if normalized_text not in self.skip:
            self.skip.append(normalized_text)

    def remove_from_skip(self, normalized_text: str) -> bool:
        """Remove text from skip list. Returns True if it was present."""
        if normalized_text in self.skip:
            self.skip.remove(normalized_text)
            return True
        return False

    def unlink_line(self, normalized_text: str) -> bool:
        """Remove a line from tracking. Returns True if found and removed."""
        for item_uuid, item in list(self.items.items()):
            if normalized_text in item.lines:
                item.lines.remove(normalized_text)
                # If no lines left, remove the entire item
                if not item.lines:
                    del self.items[item_uuid]
                return True
        return False

    def update_item(
        self,
        item_uuid: str,
        jira_status: str,
        marker: str,
        date: str,
        commit: str,
    ) -> None:
        """Update a tracked item after successful sync."""
        if item_uuid in self.items:
            item = self.items[item_uuid]
            item.jira_status = jira_status
            item.last_synced_marker = marker
            item.last_synced_date = date
            item.last_synced_commit = commit
            item.last_synced_timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def load_env(filepath: str = ".env") -> dict[str, str]:
    """Load environment variables from .env file."""
    env: dict[str, str] = {}
    try:
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    # Strip quotes if present
                    value = value.strip()
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    env[key.strip()] = value
    except FileNotFoundError:
        pass
    return env


def _parse_yaml_value(value: str) -> Any:
    """Parse a YAML scalar value."""
    value = value.strip()

    # Empty
    if not value:
        return ""

    # Quoted string
    if (value.startswith('"') and value.endswith('"')) or \
       (value.startswith("'") and value.endswith("'")):
        return value[1:-1]

    # Inline list [item1, item2]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        items = []
        for item in inner.split(","):
            item = item.strip()
            if (item.startswith('"') and item.endswith('"')) or \
               (item.startswith("'") and item.endswith("'")):
                item = item[1:-1]
            items.append(item)
        return items

    # Inline empty dict {}
    if value == "{}":
        return {}

    # Boolean
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False

    # None/null
    if value.lower() in ("null", "~"):
        return None

    # Number
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        pass

    # Plain string
    return value


def _parse_yaml_config(yaml_text: str) -> dict[str, Any]:
    """Parse the YAML config section into a nested dict.

    Handles a subset of YAML:
    - Nested dicts (indentation-based)
    - String values (quoted and unquoted)
    - Lists (- item syntax and [inline] syntax)
    - Comments (# ...) are skipped
    """
    result: dict[str, Any] = {}

    # Stack of (indent, container, parent_container, key_in_parent)
    # parent_container and key_in_parent are used when this container might become a list
    stack: list[tuple[int, dict, dict | None, str | None]] = [(-1, result, None, None)]

    lines = yaml_text.split("\n")

    for line in lines:
        # Skip empty lines and comments
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Calculate indentation
        indent = len(line) - len(line.lstrip())

        # Pop stack to find container at correct indentation
        while len(stack) > 1 and stack[-1][0] >= indent:
            stack.pop()

        current_indent, current_container, parent_container, key_in_parent = stack[-1]

        # Check if this is a list item
        if stripped.startswith("- "):
            item_value = stripped[2:].strip()
            parsed_value = _parse_yaml_value(item_value)

            # If we have a parent with a key, we might need to convert empty dict to list
            if parent_container is not None and key_in_parent is not None:
                current_value = parent_container.get(key_in_parent)
                if isinstance(current_value, dict) and not current_value:
                    # Convert empty dict to list
                    parent_container[key_in_parent] = [parsed_value]
                    # Update stack to point to the new list
                    stack[-1] = (current_indent, parent_container[key_in_parent], parent_container, key_in_parent)
                elif isinstance(current_value, list):
                    current_value.append(parsed_value)
            continue

        # Parse key: value
        if ":" in stripped:
            colon_idx = stripped.index(":")
            key = stripped[:colon_idx].strip()
            value_part = stripped[colon_idx + 1:].strip()

            # Remove quotes from key if present
            if (key.startswith('"') and key.endswith('"')) or \
               (key.startswith("'") and key.endswith("'")):
                key = key[1:-1]

            if value_part:
                # Value on same line
                parsed_value = _parse_yaml_value(value_part)
                current_container[key] = parsed_value
            else:
                # No value - could be nested dict or list (we'll find out)
                # Create empty dict as placeholder
                new_dict: dict[str, Any] = {}
                current_container[key] = new_dict
                # Push with parent info so we can convert to list if needed
                stack.append((indent, new_dict, current_container, key))

    return result


def _build_config_from_dict(data: dict[str, Any], env: dict[str, str]) -> Config:
    """Build Config object from parsed dict and environment."""
    config = Config()

    config_section = data.get("config", {})

    # Jira config
    jira_data = config_section.get("jira", {})
    config.jira = JiraConfig(
        url=env.get("JIRA_URL", jira_data.get("url", "")),
        email=env.get("JIRA_EMAIL", ""),
        token=env.get("JIRA_TOKEN", ""),
    )

    # Defaults
    defaults_data = config_section.get("defaults", {})
    config.defaults = Defaults(
        project_key=defaults_data.get("project_key", ""),
        issue_type=defaults_data.get("issue_type", "Task"),
    )

    # Mappings
    mappings_data = config_section.get("mappings", {})
    for marker, mapping_data in mappings_data.items():
        if isinstance(mapping_data, dict):
            config.mappings[marker] = MarkerMapping(
                description=mapping_data.get("description", ""),
                jira_status=mapping_data.get("jira_status", ""),
                on_new=mapping_data.get("on_new", "create"),
                project_key=mapping_data.get("project_key"),
                issue_type=mapping_data.get("issue_type"),
                labels=mapping_data.get("labels", []),
            )

    # Continuation keywords
    config.continuation_keywords = config_section.get("continuation_keywords", [])

    # Stopwords (convert to set)
    config.stopwords = set(config_section.get("stopwords", []))

    return config


def _parse_state_from_json(state_json: str, config: Config) -> None:
    """Parse JSON state section and populate config.items and config.skip."""
    try:
        state_data = json.loads(state_json)
    except json.JSONDecodeError:
        return

    # Parse items
    items_data = state_data.get("items", {})
    for item_uuid, item_data in items_data.items():
        config.items[item_uuid] = TrackedItem(
            jira_issue_key=item_data.get("jira_issue_key", ""),
            jira_status=item_data.get("jira_status", ""),
            lines=item_data.get("lines", []),
            last_synced_marker=item_data.get("last_synced_marker", ""),
            last_synced_date=item_data.get("last_synced_date", ""),
            last_synced_commit=item_data.get("last_synced_commit", ""),
            last_synced_timestamp=item_data.get("last_synced_timestamp", ""),
        )

    # Parse skip list
    config.skip = state_data.get("skip", [])


def _state_to_json(config: Config) -> str:
    """Serialize state section to JSON."""
    state = {
        "items": {},
        "skip": config.skip,
    }

    for item_uuid, item in config.items.items():
        state["items"][item_uuid] = {
            "jira_issue_key": item.jira_issue_key,
            "jira_status": item.jira_status,
            "lines": item.lines,
            "last_synced_marker": item.last_synced_marker,
            "last_synced_date": item.last_synced_date,
            "last_synced_commit": item.last_synced_commit,
            "last_synced_timestamp": item.last_synced_timestamp,
        }

    return json.dumps(state, indent=2)


def load_config(plajira_path: str = ".plajira", env_path: str = ".env") -> Config:
    """Load configuration from .plajira file and .env file.

    The .plajira file has two sections separated by STATE_MARKER:
    1. Config section (YAML) - user-editable
    2. State section (JSON) - managed by plajira
    """
    env = load_env(env_path)

    if not os.path.exists(plajira_path):
        raise FileNotFoundError(f"Config file not found: {plajira_path}")

    with open(plajira_path, encoding="utf-8") as f:
        content = f.read()

    # Split at state marker
    if STATE_MARKER in content:
        config_text, state_text = content.split(STATE_MARKER, 1)
        state_text = state_text.strip()
    else:
        config_text = content
        state_text = ""

    # Parse YAML config
    config_data = _parse_yaml_config(config_text)
    config = _build_config_from_dict(config_data, env)
    config._config_text = config_text

    # Parse JSON state
    if state_text:
        _parse_state_from_json(state_text, config)

    return config


def save_config(config: Config, plajira_path: str = ".plajira") -> None:
    """Save configuration to .plajira file.

    Preserves the user's config section verbatim and updates only the state section.
    """
    state_json = _state_to_json(config)

    content = config._config_text
    if not content.endswith("\n"):
        content += "\n"
    content += "\n"
    content += STATE_MARKER + "\n"
    content += state_json + "\n"

    with open(plajira_path, "w", encoding="utf-8") as f:
        f.write(content)


def create_default_config(jira_url: str, project_key: str) -> str:
    """Create default .plajira config content."""
    return f"""# ============================================================
# CONFIGURATION (user-editable)
# ============================================================
config:
  jira:
    url: "{jira_url}"
    # Credentials loaded from .env: JIRA_EMAIL, JIRA_TOKEN

  defaults:
    project_key: "{project_key}"
    issue_type: "Task"

  # Character mappings define behavior for each .plan prefix
  mappings:
    "?":
      description: "In progress / planned"
      jira_status: "In Progress"
      on_new: create

    "*":
      description: "Accomplished that day"
      jira_status: "Done"
      on_new: create

    "!":
      description: "Idea for future work"
      jira_status: "Backlog"
      on_new: create
      labels: ["idea"]

    "+":
      description: "Accomplished later"
      jira_status: "Done"
      on_new: ignore

    "~":
      description: "Abandoned"
      jira_status: "Won't Do"
      on_new: ignore

  # Words that suggest an item is revisiting previous work
  continuation_keywords:
    - "continue"
    - "finish"
    - "complete"
    - "wrap up"
    - "finalize"
    - "resume"
    - "more"
    - "further"
    - "additional"

  # Common words to ignore when computing similarity
  stopwords:
    - "the"
    - "a"
    - "an"
    - "on"
    - "for"
    - "to"
    - "with"
    - "and"
    - "or"
    - "in"
    - "of"

"""


def create_env_example() -> str:
    """Create .env.example content."""
    return """# Jira Cloud credentials
# Copy this file to .env and fill in your values
# Make sure to add .env to .gitignore!

JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_TOKEN=your-api-token-here
"""
