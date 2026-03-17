"""MCP resources: pm:// URIs for project-management content."""

import re
from pathlib import Path

from .bootstrap import ensure_project_management, get_pm_path
from .tools import mcp


def _read(path: Path) -> str:
    """Read file or return not-found message."""
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"Not found: {path}"


def _list_items(dir_path: Path, pattern: str, id_pattern: str) -> str:
    """List items (US-XXX, DEF-XXX, etc.) with titles."""
    if not dir_path.exists():
        return "No items found."
    lines = []
    for f in sorted(dir_path.glob(pattern)):
        id_match = re.search(id_pattern, f.name)
        if id_match:
            item_id = id_match.group(0)
            title = ""
            try:
                content = f.read_text(encoding="utf-8")
                for line in content.split("\n"):
                    if line.startswith("# ") and item_id in line:
                        title = line.replace("# ", "").replace(item_id, "").replace("-", "").strip()
                        break
                    if line.startswith("**") and "Title" not in line:
                        pass
            except Exception:
                pass
            lines.append(f"- **{item_id}**: {title or f.stem}")
    return "\n".join(lines) if lines else "No items found."


@mcp.resource("pm://index")
def get_index() -> str:
    """Project Management Index — entry point for AI-assisted project management."""
    ensure_project_management()
    pm = get_pm_path()
    return _read(pm / "INDEX.md") or _read(pm / "index.md")


@mcp.resource("pm://glossary")
def get_glossary() -> str:
    """Terminology and definitions for consistent project-management language."""
    ensure_project_management()
    return _read(get_pm_path() / "glossary.md")


@mcp.resource("pm://product-backlog")
def get_product_backlog() -> str:
    """Product backlog with user stories, defects, and technical debt."""
    ensure_project_management()
    return _read(get_pm_path() / "backlog" / "product-backlog.md")


@mcp.resource("pm://github/backlog")
def get_github_backlog() -> str:
    """Backlog from GitHub Issues when GITHUB_TOKEN is set. Lists user stories, defects, technical debt."""
    import os

    if not os.environ.get("GITHUB_TOKEN"):
        return "GITHUB_TOKEN not set. Set it to fetch backlog from GitHub."
    try:
        from .github_client import GitHubClient

        client = GitHubClient()
        if not client.is_configured:
            return "GitHub not configured: set GITHUB_OWNER and GITHUB_REPO."
        lines = ["# Backlog (GitHub)\n"]
        for label, name in [
            ("user-story", "User Stories"),
            ("defect", "Defects"),
            ("technical-debt", "Technical Debt"),
        ]:
            issues = client.list_issues_by_labels([label], state="open")
            lines.append(f"\n## {name}\n")
            for i in issues:
                lines.append(f"- #{i['number']} {i['title']}")
        return "\n".join(lines)
    except Exception as e:
        return f"GitHub error: {e}"


@mcp.resource("pm://processes/{process}")
def get_process(process: str) -> str:
    """Process document (e.g. backlog-management, sprint-planning, doc-code-consistency)."""
    ensure_project_management()
    return _read(get_pm_path() / "processes" / f"{process}.md")


@mcp.resource("pm://criteria/{criteria}")
def get_criteria(criteria: str) -> str:
    """Quality gate criteria (e.g. definition-of-ready, definition-of-done)."""
    ensure_project_management()
    return _read(get_pm_path() / "criteria" / f"{criteria}.md")


@mcp.resource("pm://backlog/user-stories/{id}")
def get_user_story(id: str) -> str:
    """User story by ID (e.g. US-001)."""
    ensure_project_management()
    root = get_pm_path() / "backlog" / "user-stories"
    for f in root.glob(f"{id}*.md"):
        return _read(f)
    return f"User story not found: {id}"


@mcp.resource("pm://backlog/defects/{id}")
def get_defect(id: str) -> str:
    """Defect by ID (e.g. DEF-001)."""
    ensure_project_management()
    root = get_pm_path() / "backlog" / "defects"
    for f in root.glob(f"{id}*.md"):
        return _read(f)
    return f"Defect not found: {id}"


@mcp.resource("pm://sprints/{id}")
def get_sprint(id: str) -> str:
    """Sprint document by ID (e.g. sprint-01)."""
    ensure_project_management()
    root = get_pm_path() / "sprints"
    for f in root.glob(f"{id}*.md"):
        return _read(f)
    return f"Sprint not found: {id}"


@mcp.resource("pm://backlog/user-stories")
def list_user_stories() -> str:
    """List all user story IDs and titles for discovery."""
    ensure_project_management()
    pm = get_pm_path()
    return _list_items(
        pm / "backlog" / "user-stories",
        "US-*.md",
        r"US-\d+",
    )


@mcp.resource("pm://backlog/defects")
def list_defects() -> str:
    """List all defect IDs and titles."""
    ensure_project_management()
    pm = get_pm_path()
    return _list_items(
        pm / "backlog" / "defects",
        "DEF-*.md",
        r"DEF-\d+",
    )


@mcp.resource("pm://sprints")
def list_sprints() -> str:
    """List all sprint IDs and names."""
    ensure_project_management()
    pm = get_pm_path()
    return _list_items(
        pm / "sprints",
        "sprint-*.md",
        r"sprint-\d+",
    )
