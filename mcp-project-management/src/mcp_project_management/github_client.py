"""GitHub API client for Issues and Projects v2."""

import os
import re
import subprocess
from typing import Any

from github import Github
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Labels required for backlog items
ITEM_LABELS = frozenset(
    {"user-story", "defect", "technical-debt", "retrospective-improvement"}
)
PRIORITY_LABELS = frozenset(
    {"priority:critical", "priority:high", "priority:medium", "priority:low"}
)
REQUIRED_LABELS = ITEM_LABELS | PRIORITY_LABELS

# Status column names (GitHub Projects often use "Todo" not "To Do")
STATUS_TODO = "Todo"
STATUS_IN_PROGRESS = "In Progress"
STATUS_DONE = "Done"


def _parse_git_remote() -> tuple[str, str] | None:
    """Parse owner/repo from git remote origin URL. Returns (owner, repo) or None."""
    try:
        from .bootstrap import get_project_root

        cwd = str(get_project_root())
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=cwd,
        )
        if result.returncode != 0 or not result.stdout.strip():
            return None
        url = result.stdout.strip()
        # ssh: git@github.com:owner/repo.git
        # https: https://github.com/owner/repo.git
        m = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?$", url)
        if m:
            return m.group(1), m.group(2)
    except Exception:
        pass
    return None


class GitHubClient:
    """Client for GitHub Issues (REST) and Projects v2 (GraphQL)."""

    def __init__(
        self,
        token: str | None = None,
        owner: str | None = None,
        repo: str | None = None,
        project_number: int | None = None,
    ) -> None:
        self._token = token or os.environ.get("GITHUB_TOKEN")
        self._owner = owner or os.environ.get("GITHUB_OWNER")
        self._repo_name = repo or os.environ.get("GITHUB_REPO")
        self._project_number = project_number
        if self._project_number is None and os.environ.get("GITHUB_PROJECT_NUMBER"):
            try:
                self._project_number = int(os.environ.get("GITHUB_PROJECT_NUMBER", 0))
            except ValueError:
                self._project_number = None

        if not self._owner or not self._repo_name:
            parsed = _parse_git_remote()
            if parsed:
                self._owner, self._repo_name = parsed

        self._gh: Github | None = None
        self._gql_client: Client | None = None
        self._project_id: str | None = None
        self._status_field_id: str | None = None
        self._status_options: dict[str, str] = {}
        self._story_points_field_id: str | None = None

    @property
    def is_configured(self) -> bool:
        """True if token and repo are available."""
        return bool(self._token and self._owner and self._repo_name)

    def _get_gh(self) -> Github:
        if self._gh is None:
            if not self._token:
                raise ValueError("GITHUB_TOKEN is required")
            self._gh = Github(self._token)
        return self._gh

    def _get_gql(self) -> Client:
        if self._gql_client is None:
            if not self._token:
                raise ValueError("GITHUB_TOKEN is required")
            transport = RequestsHTTPTransport(
                url="https://api.github.com/graphql",
                headers={"Authorization": f"Bearer {self._token}"},
            )
            self._gql_client = Client(transport=transport, fetch_schema_from_transport=False)
        return self._gql_client

    def get_repo(self):
        """Get PyGithub Repository object."""
        gh = self._get_gh()
        return gh.get_repo(f"{self._owner}/{self._repo_name}")

    def _resolve_project_id(self) -> str:
        """Resolve project node ID from owner + project number."""
        if self._project_id is not None:
            return self._project_id
        if self._project_number is None:
            raise ValueError("GITHUB_PROJECT_NUMBER is required for project operations")

        client = self._get_gql()
        # Try organization first, then user
        query = gql("""
            query($owner: String!, $number: Int!) {
                org: organization(login: $owner) {
                    projectV2(number: $number) { id }
                }
                user: user(login: $owner) {
                    projectV2(number: $number) { id }
                }
            }
        """)
        result = client.execute(
            query,
            variable_values={"owner": self._owner, "number": self._project_number},
        )
        org = result.get("org") or {}
        user = result.get("user") or {}
        proj = org.get("projectV2") or user.get("projectV2")
        if not proj or not proj.get("id"):
            raise ValueError(
                f"Project #{self._project_number} not found for {self._owner}"
            )
        self._project_id = proj["id"]
        return self._project_id

    def get_project_id(self) -> str:
        """Get project node ID, resolving if needed."""
        return self._resolve_project_id()

    def _fetch_project_fields(self) -> None:
        """Fetch Status and Story Points field IDs from project."""
        if self._status_field_id is not None:
            return
        project_id = self._resolve_project_id()
        client = self._get_gql()
        query = gql("""
            query($id: ID!) {
                node(id: $id) {
                    ... on ProjectV2 {
                        fields(first: 30) {
                            nodes {
                                ... on ProjectV2FieldCommon { id name }
                                ... on ProjectV2SingleSelectField {
                                    id name
                                    options { id name }
                                }
                                ... on ProjectV2Field {
                                    id name
                                }
                            }
                        }
                    }
                }
            }
        """)
        result = client.execute(query, variable_values={"id": project_id})
        node = result.get("node") or {}
        fields = (node.get("fields") or {}).get("nodes") or []
        for f in fields:
            name = (f.get("name") or "").lower()
            if name == "status":
                self._status_field_id = f.get("id")
                opts = f.get("options") or []
                for o in opts:
                    self._status_options[(o.get("name") or "").lower()] = o.get("id", "")
            elif "story" in name and "point" in name:
                self._story_points_field_id = f.get("id")

    def ensure_labels(self) -> None:
        """Create required labels if they don't exist."""
        repo = self.get_repo()
        existing = {lb.name.lower() for lb in repo.get_labels()}
        for label in REQUIRED_LABELS:
            if label.lower() not in existing:
                color = "ededed"
                if "priority" in label:
                    if "critical" in label:
                        color = "b60205"
                    elif "high" in label:
                        color = "d93f0b"
                    elif "medium" in label:
                        color = "fbca04"
                    else:
                        color = "0e8a16"
                repo.create_label(label, color)
                existing.add(label.lower())

    def ensure_project_columns(self) -> str:
        """Ensure project has Status field with Todo/In Progress/Done. Returns status message."""
        self._fetch_project_fields()
        if not self._status_field_id:
            return (
                "Project has no Status field. Create a Status single-select field "
                "with options: Todo, In Progress, Done."
            )
        opts_lower = {k.lower() for k in self._status_options}
        if "todo" not in opts_lower or "in progress" not in opts_lower or "done" not in opts_lower:
            return (
                "Project Status field missing options. Add: Todo, In Progress, Done."
            )
        return "Project columns configured."

    def create_issue(
        self,
        title: str,
        body: str,
        labels: list[str],
    ) -> tuple[int, str]:
        """Create GitHub issue. Returns (issue_number, node_id)."""
        repo = self.get_repo()
        issue = repo.create_issue(title=title, body=body, labels=labels)
        return issue.number, issue.node_id

    def add_issue_to_project(
        self,
        issue_node_id: str,
        status: str = STATUS_TODO,
        story_points: int | None = None,
    ) -> str | None:
        """Add issue to project, set status and story points. Returns project item ID."""
        project_id = self._resolve_project_id()
        client = self._get_gql()
        mutation = gql("""
            mutation($projectId: ID!, $contentId: ID!) {
                addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
                    item { id }
                }
            }
        """)
        result = client.execute(
            mutation,
            variable_values={"projectId": project_id, "contentId": issue_node_id},
        )
        item = (result.get("addProjectV2ItemById") or {}).get("item")
        if not item:
            return None
        item_id = item.get("id")
        if not item_id:
            return None

        self._fetch_project_fields()
        updates: list[dict[str, Any]] = []

        if self._status_field_id and self._status_options:
            status_lower = status.lower()
            option_id = self._status_options.get(status_lower)
            if not option_id:
                for k, v in self._status_options.items():
                    if "todo" in status_lower and "todo" in k:
                        option_id = v
                        break
                    if "progress" in status_lower and "progress" in k:
                        option_id = v
                        break
                    if "done" in status_lower and "done" in k:
                        option_id = v
                        break
            if option_id:
                updates.append(
                    {
                        "fieldId": self._status_field_id,
                        "value": {"singleSelectOptionId": option_id},
                    }
                )

        if story_points is not None and self._story_points_field_id:
            updates.append(
                {
                    "fieldId": self._story_points_field_id,
                    "value": {"number": float(story_points)},
                }
            )

        for u in updates:
            upd_mutation = gql("""
                mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: ProjectV2FieldValue!) {
                    updateProjectV2ItemFieldValue(
                        input: {projectId: $projectId, itemId: $itemId, fieldId: $fieldId, value: $value}
                    ) { projectV2Item { id } }
                }
            """)
            value = u["value"]
            client.execute(
                upd_mutation,
                variable_values={
                    "projectId": project_id,
                    "itemId": item_id,
                    "fieldId": u["fieldId"],
                    "value": value,
                },
            )

        return item_id

    def list_issues_by_labels(
        self,
        labels: list[str],
        state: str = "open",
    ) -> list[dict[str, Any]]:
        """List issues with given labels. Returns list of {number, title, state, labels, body}."""
        repo = self.get_repo()
        issues = repo.get_issues(state=state, labels=labels)
        return [
            {
                "number": i.number,
                "title": i.title,
                "state": i.state,
                "labels": [lb.name for lb in i.labels],
                "body": i.body or "",
                "node_id": i.node_id,
            }
            for i in issues
        ]

    def get_next_id(self, prefix: str) -> str:
        """Get next ID (US-001, DEF-001, etc.) by scanning issue titles."""
        label_map = {
            "US": "user-story",
            "DEF": "defect",
            "TD": "technical-debt",
            "RI": "retrospective-improvement",
        }
        label = label_map.get(prefix, "user-story")
        repo = self.get_repo()
        issues = repo.get_issues(state="all", labels=[label])
        max_n = 0
        pat = re.compile(rf"{prefix}-(\d+)", re.I)
        for i in issues:
            m = pat.search(i.title)
            if m:
                max_n = max(max_n, int(m.group(1)))
        return f"{prefix}-{max_n + 1:03d}"

    def update_issue_status(
        self,
        issue_number: int,
        new_status: str,
    ) -> bool:
        """Move issue's project item to new status column."""
        repo = self.get_repo()
        issue = repo.get_issue(issue_number)
        if not issue:
            return False
        project_id = self._resolve_project_id()
        self._fetch_project_fields()
        if not self._status_field_id or not self._status_options:
            return False

        # Find project item for this issue
        client = self._get_gql()
        query = gql("""
            query($projectId: ID!, $cursor: String) {
                node(id: $projectId) {
                    ... on ProjectV2 {
                        items(first: 100, after: $cursor) {
                            nodes {
                                id
                                content { ... on Issue { number } }
                                fieldValues(first: 20) {
                                    nodes {
                                        ... on ProjectV2ItemFieldSingleSelectValue {
                                            field { ... on ProjectV2FieldCommon { name } }
                                            optionId
                                        }
                                    }
                                }
                            }
                            pageInfo { hasNextPage endCursor }
                        }
                    }
                }
            }
        """)
        cursor = None
        item_id = None
        while True:
            result = client.execute(
                query,
                variable_values={"projectId": project_id, "cursor": cursor},
            )
            node = (result.get("node") or {}).get("items") or {}
            nodes = node.get("nodes") or []
            for n in nodes:
                content = n.get("content") or {}
                if content.get("number") == issue_number:
                    item_id = n.get("id")
                    break
            if item_id:
                break
            pi = node.get("pageInfo") or {}
            if not pi.get("hasNextPage"):
                break
            cursor = pi.get("endCursor")

        if not item_id:
            return False

        status_lower = new_status.lower()
        option_id = self._status_options.get(status_lower)
        if not option_id:
            for k, v in self._status_options.items():
                if "todo" in status_lower and "todo" in k:
                    option_id = v
                    break
                if "progress" in status_lower and "progress" in k:
                    option_id = v
                    break
                if "done" in status_lower and "done" in k:
                    option_id = v
                    break
        if not option_id:
            return False

        mutation = gql("""
            mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: ProjectV2FieldValue!) {
                updateProjectV2ItemFieldValue(
                    input: {projectId: $projectId, itemId: $itemId, fieldId: $fieldId, value: $value}
                ) { projectV2Item { id } }
            }
        """)
        client.execute(
            mutation,
            variable_values={
                "projectId": project_id,
                "itemId": item_id,
                "fieldId": self._status_field_id,
                "value": {"singleSelectOptionId": option_id},
            },
        )
        return True
