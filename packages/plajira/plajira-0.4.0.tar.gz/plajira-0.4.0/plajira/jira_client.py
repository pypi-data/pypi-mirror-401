"""Jira Cloud API client using urllib (no external dependencies).

Handles:
- Authentication (Basic auth with API token)
- Issue CRUD operations
- Status transitions
- Comments
"""

from __future__ import annotations

import base64
import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass
class JiraIssue:
    """Represents a Jira issue."""
    key: str
    summary: str
    status: str
    updated: str  # ISO timestamp
    project_key: str = ""
    issue_type: str = ""
    labels: list[str] | None = None


@dataclass
class JiraTransition:
    """Represents an available status transition."""
    id: str
    name: str


class JiraError(Exception):
    """Exception for Jira API errors."""

    def __init__(self, message: str, status_code: int | None = None, response: str = ""):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class JiraClient:
    """Jira Cloud REST API client."""

    def __init__(self, url: str, email: str, token: str):
        """Initialize client with Jira credentials.

        Args:
            url: Jira Cloud URL (e.g., https://company.atlassian.net)
            email: User email for authentication
            token: API token (not password)
        """
        self.base_url = url.rstrip("/")
        self.email = email
        self.token = token

        # Build auth header
        credentials = f"{email}:{token}"
        encoded = base64.b64encode(credentials.encode()).decode()
        self._auth_header = f"Basic {encoded}"

    def _request(
        self,
        method: str,
        endpoint: str,
        data: dict | None = None,
        params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make an HTTP request to Jira API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., "issue/CSD-42")
            data: Request body (will be JSON encoded)
            params: Query parameters

        Returns:
            Parsed JSON response

        Raises:
            JiraError: On API error
        """
        url = f"{self.base_url}/rest/api/3/{endpoint}"

        if params:
            query_string = "&".join(f"{k}={urllib.request.quote(str(v))}" for k, v in params.items())
            url = f"{url}?{query_string}"

        headers = {
            "Authorization": self._auth_header,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        body = json.dumps(data).encode() if data else None

        req = urllib.request.Request(url, data=body, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                response_body = response.read().decode()
                if response_body:
                    return json.loads(response_body)
                return {}
        except urllib.error.HTTPError as e:
            error_body = ""
            try:
                error_body = e.read().decode()
            except Exception:
                pass
            raise JiraError(
                f"Jira API error: {e.code} {e.reason}",
                status_code=e.code,
                response=error_body,
            ) from e
        except urllib.error.URLError as e:
            raise JiraError(f"Network error: {e.reason}") from e

    def test_connection(self) -> str:
        """Test authentication by fetching current user.

        Returns:
            Display name of authenticated user

        Raises:
            JiraError: On authentication failure
        """
        result = self._request("GET", "myself")
        return result.get("displayName", result.get("emailAddress", "Unknown"))

    def get_issue(self, issue_key: str) -> JiraIssue:
        """Fetch a single issue by key.

        Args:
            issue_key: Issue key (e.g., "CSD-42")

        Returns:
            JiraIssue object

        Raises:
            JiraError: On API error (including 404)
        """
        result = self._request(
            "GET",
            f"issue/{issue_key}",
            params={"fields": "summary,status,updated,project,issuetype,labels"},
        )

        fields = result.get("fields", {})
        return JiraIssue(
            key=result.get("key", issue_key),
            summary=fields.get("summary", ""),
            status=fields.get("status", {}).get("name", ""),
            updated=fields.get("updated", ""),
            project_key=fields.get("project", {}).get("key", ""),
            issue_type=fields.get("issuetype", {}).get("name", ""),
            labels=fields.get("labels"),
        )

    def search_issues(
        self,
        jql: str,
        max_results: int = 100,
        fields: str = "summary,status,updated",
    ) -> list[JiraIssue]:
        """Search for issues using JQL.

        Args:
            jql: JQL query string
            max_results: Maximum number of results
            fields: Comma-separated field names

        Returns:
            List of JiraIssue objects
        """
        result = self._request(
            "GET",
            "search",
            params={
                "jql": jql,
                "maxResults": str(max_results),
                "fields": fields,
            },
        )

        issues = []
        for issue_data in result.get("issues", []):
            fields_data = issue_data.get("fields", {})
            issues.append(JiraIssue(
                key=issue_data.get("key", ""),
                summary=fields_data.get("summary", ""),
                status=fields_data.get("status", {}).get("name", ""),
                updated=fields_data.get("updated", ""),
            ))

        return issues

    def create_issue(
        self,
        project_key: str,
        summary: str,
        issue_type: str = "Task",
        description: str | None = None,
        labels: list[str] | None = None,
    ) -> str:
        """Create a new issue.

        Args:
            project_key: Project key (e.g., "CSD")
            summary: Issue summary/title
            issue_type: Issue type name (e.g., "Task", "Bug")
            description: Optional description text
            labels: Optional list of labels

        Returns:
            Created issue key (e.g., "CSD-42")
        """
        fields: dict[str, Any] = {
            "project": {"key": project_key},
            "summary": summary,
            "issuetype": {"name": issue_type},
        }

        if description:
            # Atlassian Document Format (ADF)
            fields["description"] = {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": description}],
                    }
                ],
            }

        if labels:
            fields["labels"] = labels

        result = self._request("POST", "issue", data={"fields": fields})
        return result.get("key", "")

    def get_transitions(self, issue_key: str) -> list[JiraTransition]:
        """Get available transitions for an issue.

        Args:
            issue_key: Issue key (e.g., "CSD-42")

        Returns:
            List of available transitions
        """
        result = self._request("GET", f"issue/{issue_key}/transitions")

        transitions = []
        for trans in result.get("transitions", []):
            transitions.append(JiraTransition(
                id=trans.get("id", ""),
                name=trans.get("name", ""),
            ))

        return transitions

    def transition_issue(self, issue_key: str, transition_id: str) -> None:
        """Execute a transition on an issue.

        Args:
            issue_key: Issue key (e.g., "CSD-42")
            transition_id: Transition ID from get_transitions()

        Raises:
            JiraError: On failure
        """
        self._request(
            "POST",
            f"issue/{issue_key}/transitions",
            data={"transition": {"id": transition_id}},
        )

    def find_transition_to_status(
        self,
        issue_key: str,
        target_status: str,
    ) -> JiraTransition | None:
        """Find a transition that leads to the target status.

        Args:
            issue_key: Issue key
            target_status: Desired status name (e.g., "Done")

        Returns:
            JiraTransition if found, None otherwise
        """
        transitions = self.get_transitions(issue_key)

        # Try exact match first
        for trans in transitions:
            if trans.name.lower() == target_status.lower():
                return trans

        # Try partial match
        for trans in transitions:
            if target_status.lower() in trans.name.lower():
                return trans

        return None

    def add_comment(self, issue_key: str, comment_text: str) -> None:
        """Add a comment to an issue.

        Args:
            issue_key: Issue key (e.g., "CSD-42")
            comment_text: Comment text

        Raises:
            JiraError: On failure
        """
        # Atlassian Document Format (ADF)
        body = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": comment_text}],
                    }
                ],
            }
        }

        self._request("POST", f"issue/{issue_key}/comment", data=body)

    def get_issue_url(self, issue_key: str) -> str:
        """Get the web URL for an issue.

        Args:
            issue_key: Issue key (e.g., "CSD-42")

        Returns:
            Full URL to view issue in browser
        """
        return f"{self.base_url}/browse/{issue_key}"
