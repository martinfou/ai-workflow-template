"""MCP tools: script wrappers and file-writing tools."""

import os
import re
import subprocess
from datetime import date
from pathlib import Path

from fastmcp import FastMCP

from .bootstrap import ensure_project_management, get_pm_path, get_project_root

mcp = FastMCP(name="Project Management", version="0.1.0")


def _github_enabled() -> bool:
    """True if GitHub integration is configured."""
    return bool(os.environ.get("GITHUB_TOKEN"))


def _get_scripts_dir() -> Path:
    """Scripts live only under mcp-project-management/scripts/."""
    pkg_dir = Path(__file__).resolve().parent
    # parent.parent = mcp-project-management project root (parent of src/)
    project_root = pkg_dir.parent.parent
    return project_root / "scripts"


def _run_script(script_name: str, *args: str, cwd: Path | None = None) -> str:
    """Run a project-management script and return stdout+stderr. Scripts live under mcp-project-management/."""
    root = cwd or get_project_root()
    scripts_dir = _get_scripts_dir()
    script = scripts_dir / script_name

    if not script.exists():
        return f"Error: Script not found: {script}"

    try:
        result = subprocess.run(
            [str(script), *args],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=120,
        )
        out = result.stdout or ""
        err = result.stderr or ""
        if result.returncode != 0 and err:
            out = f"{out}\n--- stderr ---\n{err}" if out else err
        if result.returncode != 0:
            out = f"{out}\n(exit code: {result.returncode})"
        return out or "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Script timed out after 120 seconds"
    except Exception as e:
        return f"Error running script: {e}"


# --- Script tools ---


@mcp.tool
def validate_backlog(
    backlog_dir: str = "project-management/backlog",
) -> str:
    """Use this tool after modifying any markdown file in the backlog to ensure references are not broken. Returns a list of orphan references or validation errors. Fix any errors returned by this tool immediately."""
    return _run_script("validate-backlog.sh", backlog_dir)


@mcp.tool
def backlog_metrics(
    stats: bool = False,
    backlog_dir: str = "project-management/backlog",
    sprints_dir: str = "project-management/sprints",
) -> str:
    """Computes backlog health: items by status, aging, velocity, story points. Use stats=True ONLY to update the product-backlog.md stats block."""
    args = []
    if stats:
        args.append("--stats")
    args.extend([backlog_dir, sprints_dir])
    return _run_script("backlog-metrics.sh", *args)


@mcp.tool
def check_links(
    scan_dir: str = "project-management",
    base_dir: str = ".",
) -> str:
    """Use this tool after editing markdown to check for broken links. Returns a report of broken URLs. Fix any broken links immediately."""
    return _run_script("check-links.sh", scan_dir, base_dir)


@mcp.tool
def generate_release_notes_draft(
    commit_count: int = 20,
    auto: bool = False,
    dry_run: bool = False,
) -> str:
    """Use this tool to generate a release notes draft from recent commits. Use auto=True to automatically append to RELEASE_NOTES.md. Use dry_run=True to preview. Note: auto and dry_run are mutually exclusive."""
    args = []
    if auto:
        args.append("--auto")
    elif dry_run:
        args.append("--dry-run")
    args.append(str(commit_count))
    return _run_script("generate-release-notes-draft.sh", *args)


@mcp.tool
def validate_backlog_integrity(
    backlog_dir: str = "project-management/backlog",
) -> str:
    """Use this tool to check backlog integrity: orphan refs, missing files, duplicate IDs, Fibonacci story points. Fix any errors returned by this tool immediately."""
    return _run_script("validate-backlog-integrity.sh", backlog_dir)


@mcp.tool
def visualize_dependencies(
    backlog_dir: str = "project-management/backlog",
) -> str:
    """Generates Mermaid flowchart of dependencies between user stories and defects."""
    return _run_script("visualize-dependencies.sh", backlog_dir)


@mcp.tool
def lint_project_management() -> str:
    """Runs full lint: backlog validation, links, forbidden terminology, newline-at-EOF."""
    return _run_script("lint-project-management.sh")


@mcp.tool
def prepare_gap_check() -> str:
    """Use this tool to list changed files and evaluate whether the documentation matches the code before you commit."""
    return _run_script("prepare-gap-check.sh")


# --- File-writing helpers ---


def _slug(text: str) -> str:
    """Create filename slug from title."""
    s = re.sub(r"[^\w\s-]", "", text.lower())
    s = re.sub(r"[-\s]+", "-", s).strip("-")
    return s[:50] if s else "item"


def _next_id(prefix: str, pm: Path) -> str:
    """Get next ID (US-001, DEF-001, TD-001)."""
    if prefix == "US":
        dir_path = pm / "backlog" / "user-stories"
    elif prefix == "DEF":
        dir_path = pm / "backlog" / "defects"
    elif prefix == "TD":
        dir_path = pm / "backlog" / "technical-debt"
    else:
        return f"{prefix}-001"

    if not dir_path.exists():
        return f"{prefix}-001"

    max_n = 0
    for f in dir_path.glob(f"{prefix}-*.md"):
        m = re.search(rf"{prefix}-(\d+)", f.name)
        if m:
            max_n = max(max_n, int(m.group(1)))
    return f"{prefix}-{max_n + 1:03d}"


def _priority_emoji(priority: str) -> str:
    p = priority.lower()
    if "critical" in p:
        return "🔴"
    if "high" in p:
        return "🟠"
    if "medium" in p:
        return "🟡"
    return "🟢"


def _priority_label(priority: str) -> str:
    """Map priority to GitHub label."""
    p = priority.lower()
    if "critical" in p:
        return "priority:critical"
    if "high" in p:
        return "priority:high"
    if "medium" in p:
        return "priority:medium"
    return "priority:low"


def _build_user_story_body(
    item_id: str,
    title: str,
    description: str,
    acceptance_criteria: str,
    user_story_format: str,
    dependencies: str,
    priority: str,
    story_points: int,
) -> str:
    """Build markdown body for user story issue."""
    today = date.today().isoformat()
    emoji = _priority_emoji(priority)
    ac = acceptance_criteria.strip() or "(to be defined)"
    ac_lines = "\n".join(f"- [ ] {c.strip()}" for c in ac.split("\n") if c.strip()) if ac != "(to be defined)" else ac
    us_fmt = user_story_format or 'As a [user type], I want [functionality], so that [benefit].'
    deps = dependencies.strip() or "- (none)"
    dep_lines = "\n".join(f"- {d.strip()}" for d in deps.split("\n") if d.strip()) if deps != "- (none)" else deps
    return f"""# User Story: {item_id} - {title}

**Status**: ⭕ To Do
**Priority**: {emoji} {priority}
**Story Points**: {story_points} (Fibonacci: 1, 2, 3, 5, 8, 13)
**Created**: {today}
**Updated**: {today}

## Description

{description}

## User Story

{us_fmt}

## Acceptance Criteria

{ac_lines}

## Dependencies

{dep_lines}
"""


def _build_defect_body(
    item_id: str,
    title: str,
    description: str,
    steps_to_reproduce: str,
    expected_behavior: str,
    actual_behavior: str,
    priority: str,
    story_points: int,
) -> str:
    """Build markdown body for defect issue."""
    today = date.today().isoformat()
    emoji = _priority_emoji(priority)
    steps = steps_to_reproduce.strip() or "1. (to be documented)"
    expected = expected_behavior.strip() or "(to be documented)"
    actual = actual_behavior.strip() or "(to be documented)"
    return f"""# Defect: {item_id} - {title}

**Status**: ⭕ To Do
**Priority**: {emoji} {priority}
**Story Points**: {story_points}
**Created**: {today}
**Updated**: {today}

## Description

{description}

## Steps to Reproduce

{steps}

## Expected Behavior

{expected}

## Actual Behavior

{actual}
"""


def _build_technical_debt_body(
    item_id: str,
    title: str,
    description: str,
    impact: str,
    proposed_solution: str,
    priority: str,
    story_points: int,
) -> str:
    """Build markdown body for technical debt issue."""
    today = date.today().isoformat()
    emoji = _priority_emoji(priority)
    impact_text = impact.strip() or "(to be documented)"
    solution_text = proposed_solution.strip() or "(to be documented)"
    return f"""# Technical Debt: {item_id} - {title}

**Status**: ⭕ To Do
**Priority**: {emoji} {priority}
**Story Points**: {story_points}
**Created**: {today}
**Updated**: {today}

## Description

{description}

## Impact

{impact_text}

## Proposed Solution

{solution_text}
"""


def _add_backlog_row(
    pm: Path,
    section: str,
    row: str,
) -> None:
    """Insert a row into the product backlog table."""
    pb = pm / "backlog" / "product-backlog.md"
    if not pb.exists():
        return
    content = pb.read_text(encoding="utf-8")
    today = date.today().isoformat()

    # Find the section table and insert before the closing |
    # Pattern: ## User Stories ... | ID | ... | \n|----|... then we insert before next ##
    section_header = f"## {section}"
    if section_header not in content:
        return

    # Find the table body (after header row |----|----|...)
    parts = content.split(section_header, 1)
    if len(parts) < 2:
        return
    after_header = parts[1]
    # Table ends at next ## or ---
    table_end = re.search(r"\n(## |---)", after_header)
    if table_end:
        table_content = after_header[: table_end.start()]
    else:
        table_content = after_header

    # Check if table has only header row (no data rows)
    lines = table_content.strip().split("\n")
    # Header is | ID | Title | ... ; separator is |----|----| ; data rows follow
    # Insert our row after the separator line
    new_row = row + "\n"
    for i, line in enumerate(lines):
        if re.match(r"^\|[-:\s|]+\|", line):  # separator row
            lines.insert(i + 1, row)
            break
    else:
        lines.append(row)

    new_table = "\n".join(lines) + "\n"
    if table_end:
        rest = after_header[table_end.start() :]
    else:
        rest = ""
    # Preserve blank line between section header and table
    new_after = "\n\n" + new_table + rest
    new_content = parts[0] + section_header + new_after
    new_content = re.sub(
        r"\*\*Last Updated\*\*: \d{4}-\d{2}-\d{2}",
        f"**Last Updated**: {today}",
        new_content,
        count=1,
    )
    pb.write_text(new_content, encoding="utf-8")


# --- File-writing tools ---


@mcp.tool
def create_user_story(
    title: str,
    description: str,
    acceptance_criteria: str = "",
    priority: str = "Medium",
    story_points: int = 2,
    user_story_format: str = "",
    dependencies: str = "",
) -> str:
    """Use this tool to create a user story and add it to the product backlog. Valid priorities: Critical, High, Medium, Low. Story points must be a Fibonacci number (1, 2, 3, 5, 8, 13)."""
    if _github_enabled():
        try:
            from .github_client import GitHubClient
            from .github_client import STATUS_TODO

            client = GitHubClient()
            if not client.is_configured:
                return "GitHub not configured: set GITHUB_OWNER and GITHUB_REPO (or use a git remote)."
            client.ensure_labels()
            item_id = client.get_next_id("US")
            body = _build_user_story_body(
                item_id, title, description, acceptance_criteria,
                user_story_format, dependencies, priority, story_points,
            )
            labels = ["user-story", _priority_label(priority)]
            issue_num, node_id = client.create_issue(title=f"{item_id}: {title}", body=body, labels=labels)
            if client._project_number is not None:
                client.add_issue_to_project(node_id, status=STATUS_TODO, story_points=story_points)
            return f"Created GitHub issue #{issue_num} {item_id}: {title} and added to project."
        except Exception as e:
            return f"GitHub error: {e}"

    ensure_project_management()
    pm = get_pm_path()
    root = get_project_root()

    item_id = _next_id("US", pm)
    slug = _slug(title)
    filename = f"{item_id}-{slug}.md"
    filepath = pm / "backlog" / "user-stories" / filename

    template_path = pm / "templates" / "user-story-template.md"
    if not template_path.exists():
        from importlib.resources import files

        data = files("mcp_project_management") / "data"
        tpl = (data / "user-story-template.md").read_text(encoding="utf-8")
    else:
        tpl = template_path.read_text(encoding="utf-8")

    today = date.today().isoformat()
    emoji = _priority_emoji(priority)

    content = tpl.replace("[ID]", item_id)
    content = content.replace("[Story Title]", title)
    content = content.replace("[X]", str(story_points))
    content = content.replace("[YYYY-MM-DD]", today)
    content = content.replace("🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low", f"{emoji} {priority}")
    content = content.replace(
        "[Clear description of the user story. Explain what needs to be built and why.]",
        description,
    )
    if user_story_format:
        content = content.replace(
            'As a [user type: e.g., "registered user", "admin", "mobile app user"], \nI want [functionality: e.g., "to filter search results by date"], \nso that [benefit: e.g., "I can quickly find recent items"].',
            user_story_format,
        )
    if acceptance_criteria:
        ac_lines = "\n".join(f"- [ ] {c.strip()}" for c in acceptance_criteria.split("\n") if c.strip())
        content = content.replace(
            "- [ ] Criterion 1 (specific, testable)\n- [ ] Criterion 2 (specific, testable)\n- [ ] Criterion 3 (specific, testable)",
            ac_lines or "- [ ] (to be defined)",
        )
    if dependencies:
        dep_lines = "\n".join(f"- {d.strip()}" for d in dependencies.split("\n") if d.strip())
        content = content.replace(
            "- [Dependency 1 - what must be completed first]\n- [Dependency 2 - what must be completed first]",
            dep_lines,
        )

    content = content.replace("(user-stories/US-001-story-name.md)", f"user-stories/{filename}")
    filepath.write_text(content, encoding="utf-8")

    rel_link = f"user-stories/{filename}"
    row = f"| [{item_id}]({rel_link}) | {title[:50]} | {emoji} {priority} | {story_points} | ⭕ | - | {today} | {today} |"
    _add_backlog_row(pm, "User Stories", row)

    return f"Created {filepath.relative_to(root)} and added to product backlog."


@mcp.tool
def create_defect(
    title: str,
    description: str,
    steps_to_reproduce: str = "",
    expected_behavior: str = "",
    actual_behavior: str = "",
    priority: str = "Medium",
    story_points: int = 2,
) -> str:
    """Use this tool to create a defect and add it to the product backlog. Valid priorities: Critical, High, Medium, Low. Story points must be a Fibonacci number (1, 2, 3, 5, 8, 13)."""
    if _github_enabled():
        try:
            from .github_client import GitHubClient
            from .github_client import STATUS_TODO

            client = GitHubClient()
            if not client.is_configured:
                return "GitHub not configured: set GITHUB_OWNER and GITHUB_REPO (or use a git remote)."
            client.ensure_labels()
            item_id = client.get_next_id("DEF")
            body = _build_defect_body(
                item_id, title, description, steps_to_reproduce,
                expected_behavior, actual_behavior, priority, story_points,
            )
            labels = ["defect", _priority_label(priority)]
            issue_num, node_id = client.create_issue(title=f"{item_id}: {title}", body=body, labels=labels)
            if client._project_number is not None:
                client.add_issue_to_project(node_id, status=STATUS_TODO, story_points=story_points)
            return f"Created GitHub issue #{issue_num} {item_id}: {title} and added to project."
        except Exception as e:
            return f"GitHub error: {e}"

    ensure_project_management()
    pm = get_pm_path()
    root = get_project_root()

    item_id = _next_id("DEF", pm)
    slug = _slug(title)
    filename = f"{item_id}-{slug}.md"
    filepath = pm / "backlog" / "defects" / filename

    template_path = pm / "templates" / "defect-template.md"
    if not template_path.exists():
        from importlib.resources import files

        data = files("mcp_project_management") / "data"
        tpl = (data / "defect-template.md").read_text(encoding="utf-8")
    else:
        tpl = template_path.read_text(encoding="utf-8")

    today = date.today().isoformat()
    emoji = _priority_emoji(priority)

    content = tpl.replace("[ID]", item_id)
    content = content.replace("[Defect Description]", title)
    content = content.replace("[X]", str(story_points))
    content = content.replace("[YYYY-MM-DD]", today)
    content = content.replace("🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low", f"{emoji} {priority}")
    content = content.replace(
        "[Clear, concise description of the defect. One or two sentences summarizing the issue.]",
        description,
    )
    if steps_to_reproduce:
        steps_lines = "\n".join(f"{i+1}. {s.strip()}" for i, s in enumerate(steps_to_reproduce.split("\n")) if s.strip())
        content = content.replace(
            "1. [Step 1 - specific action: e.g., \"Navigate to Settings > Profile\"]\n2. [Step 2 - specific action: e.g., \"Enter email: 'user+test@example.com'\"]\n3. [Step 3 - specific action: e.g., \"Click 'Save' button\"]\n4. [Observed behavior - what happens: e.g., \"Error message appears: 'Invalid email format'\"]",
            steps_lines or "1. (to be documented)",
        )
    if expected_behavior:
        content = content.replace("[What should happen when following the steps above.]", expected_behavior)
    if actual_behavior:
        content = content.replace("[What actually happens when following the steps above. Include error messages, crashes, incorrect behavior, etc.]", actual_behavior)

    content = content.replace("(defects/DEF-001-defect-description.md)", f"defects/{filename}")
    filepath.write_text(content, encoding="utf-8")

    rel_link = f"defects/{filename}"
    row = f"| [{item_id}]({rel_link}) | {title[:50]} | {emoji} {priority} | {story_points} | ⭕ | - | {today} | {today} |"
    _add_backlog_row(pm, "Defects", row)

    return f"Created {filepath.relative_to(root)} and added to product backlog."


@mcp.tool
def create_technical_debt(
    title: str,
    description: str,
    impact: str = "",
    proposed_solution: str = "",
    priority: str = "Medium",
    story_points: int = 2,
) -> str:
    """Use this tool to create a technical debt item and add it to the product backlog. Valid priorities: Critical, High, Medium, Low. Story points must be a Fibonacci number (1, 2, 3, 5, 8, 13)."""
    if _github_enabled():
        try:
            from .github_client import GitHubClient
            from .github_client import STATUS_TODO

            client = GitHubClient()
            if not client.is_configured:
                return "GitHub not configured: set GITHUB_OWNER and GITHUB_REPO (or use a git remote)."
            client.ensure_labels()
            item_id = client.get_next_id("TD")
            body = _build_technical_debt_body(
                item_id, title, description, impact, proposed_solution, priority, story_points,
            )
            labels = ["technical-debt", _priority_label(priority)]
            issue_num, node_id = client.create_issue(title=f"{item_id}: {title}", body=body, labels=labels)
            if client._project_number is not None:
                client.add_issue_to_project(node_id, status=STATUS_TODO, story_points=story_points)
            return f"Created GitHub issue #{issue_num} {item_id}: {title} and added to project."
        except Exception as e:
            return f"GitHub error: {e}"

    ensure_project_management()
    pm = get_pm_path()
    root = get_project_root()

    item_id = _next_id("TD", pm)
    slug = _slug(title)
    filename = f"{item_id}-{slug}.md"
    filepath = pm / "backlog" / "technical-debt" / filename

    template_path = pm / "templates" / "technical-debt-template.md"
    if not template_path.exists():
        from importlib.resources import files

        data = files("mcp_project_management") / "data"
        tpl = (data / "technical-debt-template.md").read_text(encoding="utf-8")
    else:
        tpl = template_path.read_text(encoding="utf-8")

    today = date.today().isoformat()
    emoji = _priority_emoji(priority)

    content = tpl.replace("[ID]", item_id)
    content = content.replace("[Short Description]", title)
    content = content.replace("[X]", str(story_points))
    content = content.replace("[YYYY-MM-DD]", today)
    content = content.replace("🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low", f"{emoji} {priority}")
    content = content.replace(
        "[What technical debt exists? What needs to be improved or refactored?]",
        description,
    )
    if impact:
        content = content.replace("[Why does this matter? What risks or costs does it impose?]", impact)
    if proposed_solution:
        content = content.replace("[How will this be addressed? High-level approach.]", proposed_solution)

    content = content.replace("(technical-debt/TD-001-description.md)", f"technical-debt/{filename}")
    filepath.write_text(content, encoding="utf-8")

    rel_link = f"technical-debt/{filename}"
    row = f"| [{item_id}]({rel_link}) | {title[:50]} | {emoji} {priority} | {story_points} | ⭕ | - | {today} | {today} |"
    _add_backlog_row(pm, "Technical Debt", row)

    return f"Created {filepath.relative_to(root)} and added to product backlog."


# --- GitHub tools ---


@mcp.tool
def setup_github_project() -> str:
    """Ensure GitHub labels and project columns exist. Run when GITHUB_TOKEN is set. Requires GITHUB_PROJECT_NUMBER for project setup."""
    if not _github_enabled():
        return "GITHUB_TOKEN not set. Set it to enable GitHub integration."
    try:
        from .github_client import GitHubClient

        client = GitHubClient()
        if not client.is_configured:
            return "GitHub not configured: set GITHUB_OWNER and GITHUB_REPO (or use a git remote)."
        client.ensure_labels()
        msg = "Labels created/verified."
        if client._project_number is not None:
            msg += " " + client.ensure_project_columns()
        else:
            msg += " GITHUB_PROJECT_NUMBER not set; project columns not configured."
        return msg
    except Exception as e:
        return f"GitHub setup error: {e}"


@mcp.tool
def list_backlog(
    labels: str = "user-story,defect,technical-debt",
    state: str = "open",
) -> str:
    """List backlog items from GitHub. Use when GITHUB_TOKEN is set. labels: comma-separated; state: open or closed."""
    if not _github_enabled():
        return "GITHUB_TOKEN not set. Use backlog_metrics or pm://product-backlog for file-based backlog."
    try:
        from .github_client import GitHubClient

        client = GitHubClient()
        if not client.is_configured:
            return "GitHub not configured."
        label_list = [lb.strip() for lb in labels.split(",") if lb.strip()]
        lines = []
        for lb in label_list:
            issues = client.list_issues_by_labels([lb], state=state)
            lines.append(f"\n## {lb}")
            for i in issues:
                lines.append(f"- #{i['number']} {i['title']} ({i['state']})")
        return "\n".join(lines) if lines else "No issues found."
    except Exception as e:
        return f"GitHub error: {e}"


@mcp.tool
def get_backlog_metrics_github() -> str:
    """Aggregate backlog metrics from GitHub: count by label, by status. Use when GITHUB_TOKEN is set."""
    if not _github_enabled():
        return "GITHUB_TOKEN not set. Use backlog_metrics for file-based metrics."
    try:
        from .github_client import GitHubClient

        client = GitHubClient()
        if not client.is_configured:
            return "GitHub not configured."
        lines = ["## Backlog metrics (GitHub)"]
        for label in ["user-story", "defect", "technical-debt"]:
            open_issues = client.list_issues_by_labels([label], state="open")
            closed_issues = client.list_issues_by_labels([label], state="closed")
            lines.append(f"\n### {label}")
            lines.append(f"- Open: {len(open_issues)}")
            lines.append(f"- Closed: {len(closed_issues)}")
        return "\n".join(lines)
    except Exception as e:
        return f"GitHub error: {e}"


@mcp.tool
def update_issue_status(
    issue_number: int,
    new_status: str,
) -> str:
    """Move issue between project columns (Todo / In Progress / Done). Requires GITHUB_TOKEN and GITHUB_PROJECT_NUMBER."""
    if not _github_enabled():
        return "GITHUB_TOKEN not set."
    try:
        from .github_client import GitHubClient

        client = GitHubClient()
        if not client.is_configured:
            return "GitHub not configured."
        ok = client.update_issue_status(issue_number, new_status)
        return f"Updated issue #{issue_number} to {new_status}." if ok else f"Could not update issue #{issue_number}."
    except Exception as e:
        return f"GitHub error: {e}"


@mcp.tool
def update_issue(
    issue_number: int,
    title: str | None = None,
    body: str | None = None,
    labels: str | None = None,
) -> str:
    """Update issue title, body, or labels. Comma-separated labels. Requires GITHUB_TOKEN."""
    if not _github_enabled():
        return "GITHUB_TOKEN not set."
    try:
        from .github_client import GitHubClient

        client = GitHubClient()
        if not client.is_configured:
            return "GitHub not configured."
        repo = client.get_repo()
        issue = repo.get_issue(issue_number)
        if not issue:
            return f"Issue #{issue_number} not found."
        if title is not None:
            issue.edit(title=title)
        if body is not None:
            issue.edit(body=body)
        if labels is not None:
            label_list = [lb.strip() for lb in labels.split(",") if lb.strip()]
            issue.edit(labels=label_list)
        return f"Updated issue #{issue_number}."
    except Exception as e:
        return f"GitHub error: {e}"


@mcp.tool
def sync_backlog_to_markdown() -> str:
    """Generate product-backlog.md from GitHub issues. Use when GITHUB_TOKEN is set. Writes to project-management/backlog/product-backlog.md."""
    if not _github_enabled():
        return "GITHUB_TOKEN not set. Use file-based backlog."
    try:
        from .github_client import GitHubClient

        client = GitHubClient()
        if not client.is_configured:
            return "GitHub not configured."
        ensure_project_management()
        pm = get_pm_path()
        today = date.today().isoformat()

        sections = {"user-story": "User Stories", "defect": "Defects", "technical-debt": "Technical Debt"}
        tables = []
        for label, section in sections.items():
            issues = client.list_issues_by_labels([label], state="open")
            issues.extend(client.list_issues_by_labels([label], state="closed"))
            header = f"| ID | Title | Priority | SP | Status | Sprint | Created | Updated |"
            sep = "|----|-------|----------|----|--------|--------|---------|---------|"
            rows = []
            for i in issues:
                # Parse ID from title (US-001: Title)
                title = i["title"]
                parts = title.split(":", 1)
                item_id = parts[0].strip() if parts else f"#{i['number']}"
                title_short = (parts[1].strip() if len(parts) > 1 else title)[:50]
                labels = i.get("labels") or []
                prio = "Medium"
                for lb in labels:
                    if lb.startswith("priority:"):
                        prio = lb.replace("priority:", "").capitalize()
                        break
                sp = "-"
                status = "⭕" if i["state"] == "open" else "✅"
                rows.append(f"| {item_id} | {title_short} | {prio} | {sp} | {status} | - | - | {today} |")
            table = "\n".join([header, sep] + rows)
            tables.append(f"## {section}\n\n{table}")

        content = f"""# Product Backlog

**Last Updated**: {today}

Generated from GitHub. Run sync_backlog_to_markdown to refresh.

---

""" + "\n\n".join(tables)
        pb = pm / "backlog" / "product-backlog.md"
        pb.parent.mkdir(parents=True, exist_ok=True)
        pb.write_text(content, encoding="utf-8")
        return f"Synced backlog to {pb}."
    except Exception as e:
        return f"GitHub sync error: {e}"
