"""Tests for config module."""

import os
import tempfile
import unittest

from plajira.config import (
    Config,
    load_config,
    load_env,
    save_config,
    create_default_config,
)


class TestLoadEnv(unittest.TestCase):
    """Tests for .env file loading."""

    def setUp(self):
        """Create a temporary directory."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def _write_env(self, content: str) -> str:
        """Write content to a temporary .env file and return path."""
        path = os.path.join(self.temp_dir, ".env")
        with open(path, "w") as f:
            f.write(content)
        return path

    def test_basic_parsing(self):
        """Test basic key=value parsing."""
        path = self._write_env("FOO=bar\nBAZ=qux")
        env = load_env(path)
        self.assertEqual(env["FOO"], "bar")
        self.assertEqual(env["BAZ"], "qux")

    def test_quoted_values(self):
        """Test quoted values."""
        path = self._write_env('FOO="bar baz"\nBAR=\'qux\'')
        env = load_env(path)
        self.assertEqual(env["FOO"], "bar baz")
        self.assertEqual(env["BAR"], "qux")

    def test_comments(self):
        """Test comment lines are ignored."""
        path = self._write_env("# comment\nFOO=bar\n# another comment")
        env = load_env(path)
        self.assertEqual(len(env), 1)
        self.assertEqual(env["FOO"], "bar")

    def test_empty_lines(self):
        """Test empty lines are ignored."""
        path = self._write_env("FOO=bar\n\nBAZ=qux\n")
        env = load_env(path)
        self.assertEqual(len(env), 2)

    def test_missing_file(self):
        """Test missing file returns empty dict."""
        env = load_env("/nonexistent/path/.env")
        self.assertEqual(env, {})

    def test_equals_in_value(self):
        """Test values containing equals sign."""
        path = self._write_env("URL=https://example.com?foo=bar")
        env = load_env(path)
        self.assertEqual(env["URL"], "https://example.com?foo=bar")


class TestLoadConfig(unittest.TestCase):
    """Tests for .plajira config loading."""

    def setUp(self):
        """Create a temporary directory."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def _write_config(self, content: str) -> str:
        """Write content to a temporary .plajira file and return path."""
        path = os.path.join(self.temp_dir, ".plajira")
        with open(path, "w") as f:
            f.write(content)
        return path

    def _write_env(self, content: str) -> str:
        """Write content to a temporary .env file and return path."""
        path = os.path.join(self.temp_dir, ".env")
        with open(path, "w") as f:
            f.write(content)
        return path

    def test_load_basic_config(self):
        """Test loading basic config."""
        config_content = """config:
  jira:
    url: "https://test.atlassian.net"
  defaults:
    project_key: "TEST"
    issue_type: "Task"
  mappings:
    "?":
      description: "In progress"
      jira_status: "In Progress"
      on_new: create
  continuation_keywords:
    - "continue"
  stopwords:
    - "the"

# === STATE (managed by plajira, do not edit below) ===
{"items": {}, "skip": []}
"""
        env_content = """JIRA_URL=https://test.atlassian.net
JIRA_EMAIL=test@example.com
JIRA_TOKEN=secret
"""
        config_path = self._write_config(config_content)
        env_path = self._write_env(env_content)

        config = load_config(config_path, env_path)

        self.assertEqual(config.jira.url, "https://test.atlassian.net")
        self.assertEqual(config.jira.email, "test@example.com")
        self.assertEqual(config.jira.token, "secret")
        self.assertEqual(config.defaults.project_key, "TEST")
        self.assertEqual(config.defaults.issue_type, "Task")
        self.assertIn("?", config.mappings)
        self.assertEqual(config.mappings["?"].jira_status, "In Progress")
        self.assertEqual(config.continuation_keywords, ["continue"])
        self.assertEqual(config.stopwords, {"the"})

    def test_load_state(self):
        """Test loading state section."""
        config_content = """config:
  jira:
    url: "https://test.atlassian.net"
  defaults:
    project_key: "TEST"
  mappings: {}
  continuation_keywords: []
  stopwords: []

# === STATE (managed by plajira, do not edit below) ===
{"items": {"uuid-1": {"jira_issue_key": "TEST-1", "jira_status": "Done", "lines": ["foo"], "last_synced_marker": "*", "last_synced_date": "2026-01-01", "last_synced_commit": "abc", "last_synced_timestamp": "2026-01-01T00:00:00Z"}}, "skip": ["lunch"]}
"""
        config_path = self._write_config(config_content)

        config = load_config(config_path, "/nonexistent/.env")

        self.assertEqual(len(config.items), 1)
        self.assertIn("uuid-1", config.items)
        self.assertEqual(config.items["uuid-1"].jira_issue_key, "TEST-1")
        self.assertEqual(config.items["uuid-1"].lines, ["foo"])
        self.assertEqual(config.skip, ["lunch"])

    def test_missing_file(self):
        """Test missing config file raises error."""
        with self.assertRaises(FileNotFoundError):
            load_config("/nonexistent/.plajira")


class TestSaveConfig(unittest.TestCase):
    """Tests for config saving."""

    def setUp(self):
        """Create a temporary directory."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_save_preserves_config(self):
        """Test saving preserves the config section."""
        config_text = """# My custom comment
config:
  jira:
    url: "https://test.atlassian.net"
  defaults:
    project_key: "TEST"
"""
        config_path = os.path.join(self.temp_dir, ".plajira")

        # Create a config with the custom text
        config = Config()
        config._config_text = config_text
        config.skip = ["test item"]

        save_config(config, config_path)

        # Read back and verify
        with open(config_path) as f:
            content = f.read()

        # Should preserve the comment
        self.assertIn("# My custom comment", content)
        # Should have state section
        self.assertIn("# === STATE", content)
        self.assertIn('"test item"', content)


class TestConfigMethods(unittest.TestCase):
    """Tests for Config class methods."""

    def test_find_item_by_line(self):
        """Test finding item by line text."""
        config = Config()
        config.add_item(
            normalized_text="foo bar",
            jira_issue_key="TEST-1",
            jira_status="Done",
            marker="*",
            date="2026-01-01",
            commit="abc",
        )

        found = config.find_item_by_line("foo bar")
        self.assertIsNotNone(found)
        uuid, item = found
        self.assertEqual(item.jira_issue_key, "TEST-1")

        not_found = config.find_item_by_line("nonexistent")
        self.assertIsNone(not_found)

    def test_is_skipped(self):
        """Test skip list checking."""
        config = Config()
        config.add_to_skip("lunch")

        self.assertTrue(config.is_skipped("lunch"))
        self.assertFalse(config.is_skipped("meeting"))

    def test_link_line_to_item(self):
        """Test linking additional lines to an item."""
        config = Config()
        item_uuid = config.add_item(
            normalized_text="foo bar",
            jira_issue_key="TEST-1",
            jira_status="Done",
            marker="*",
            date="2026-01-01",
            commit="abc",
        )

        config.link_line_to_item("another line", item_uuid)

        self.assertIn("another line", config.items[item_uuid].lines)

    def test_unlink_line(self):
        """Test unlinking a line."""
        config = Config()
        item_uuid = config.add_item(
            normalized_text="foo bar",
            jira_issue_key="TEST-1",
            jira_status="Done",
            marker="*",
            date="2026-01-01",
            commit="abc",
        )
        config.link_line_to_item("another line", item_uuid)

        # Unlink first line
        result = config.unlink_line("foo bar")
        self.assertTrue(result)
        self.assertNotIn("foo bar", config.items[item_uuid].lines)
        self.assertIn("another line", config.items[item_uuid].lines)

        # Unlink second line (should remove entire item)
        result = config.unlink_line("another line")
        self.assertTrue(result)
        self.assertNotIn(item_uuid, config.items)

    def test_remove_from_skip(self):
        """Test removing from skip list."""
        config = Config()
        config.add_to_skip("lunch")

        result = config.remove_from_skip("lunch")
        self.assertTrue(result)
        self.assertFalse(config.is_skipped("lunch"))

        result = config.remove_from_skip("nonexistent")
        self.assertFalse(result)


class TestCreateDefaultConfig(unittest.TestCase):
    """Tests for default config creation."""

    def test_creates_valid_config(self):
        """Test default config contains required sections."""
        content = create_default_config(
            jira_url="https://test.atlassian.net",
            project_key="TEST",
        )

        self.assertIn("https://test.atlassian.net", content)
        self.assertIn("TEST", content)
        self.assertIn("config:", content)
        self.assertIn("mappings:", content)
        self.assertIn("continuation_keywords:", content)
        self.assertIn("stopwords:", content)


if __name__ == "__main__":
    unittest.main()
