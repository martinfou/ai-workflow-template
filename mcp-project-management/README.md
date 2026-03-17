# MCP Project Management Server

Exposes the project-management philosophy and processes as an MCP (Model Context Protocol) server for AI clients (Cursor, Claude Desktop, OpenCode, etc.).

## Features

- **Scripts**: Live only under `mcp-project-management/scripts/` (MCP server uses no other location)
- **Tools**: Validate backlog, metrics, check links, release notes, create user stories/defects/technical debt
- **Resources**: `pm://` URIs for INDEX, glossary, product backlog, processes, criteria, backlog items
- **Prompts**: Workflow templates for sprint planning, retrospectives, doc-code consistency, etc.
- **Bootstrap**: Creates `project-management/` structure when missing (any repo)

## Setup

We recommend using `uvx` for a zero-install, frictionless setup. Alternatively, you can use a local virtual environment.

### Option 1: Zero-Install via uvx (Recommended)

**Cursor** — Add to MCP settings (e.g. `~/.cursor/mcp.json` or project `.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "project-management": {
      "command": "uvx",
      "args": ["mcp-project-management"],
      "cwd": "/path/to/your/repo"
    }
  }
}
```

*(Note: For local development before publishing to PyPI, use `"args": ["--from", "/path/to/mcp-project-management", "mcp-project-management"]` instead).*

**Claude Desktop** — Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "project-management": {
      "command": "uvx",
      "args": ["mcp-project-management"],
      "cwd": "/path/to/your/repo"
    }
  }
}
```

**OpenCode** — Similar MCP config; set `cwd` to your repo root.

### Option 2: Local Virtual Environment

```bash
cd mcp-project-management
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

Then configure your MCP client to point to the local `.venv`:

```json
{
  "mcpServers": {
    "project-management": {
      "command": "/path/to/mcp-project-management/.venv/bin/python",
      "args": ["-m", "mcp_project_management.server"],
      "cwd": "/path/to/your/repo"
    }
  }
}
```

### 3. Environment variables (optional)

- `PROJECT_ROOT` — Override project root (default: `cwd`)
- `PM_PATH` — Override project-management path (default: `project-management`)

### 4. GitHub integration (optional)

When `GITHUB_TOKEN` is set, create/list/update tools use GitHub Issues and Projects instead of (or in addition to) markdown files.

**Environment variables**:

| Variable | Purpose |
|----------|---------|
| `GITHUB_TOKEN` | PAT with `repo` and `project` scopes |
| `GITHUB_OWNER` | Org or user (optional if from git remote) |
| `GITHUB_REPO` | Repo name (optional if from git remote) |
| `GITHUB_PROJECT_NUMBER` | Project number (e.g. 1, 2) for kanban workflow |

**Setup**:

1. Create a GitHub Project (v2) with Status field options: Todo, In Progress, Done. Optional: Story Points (Number) field.
2. Set `GITHUB_TOKEN` (and optionally owner/repo/project).
3. Run `setup_github_project` tool to ensure labels exist.
4. Create user stories, defects, technical debt via tools — they become GitHub issues.

**Fallback**: If `GITHUB_TOKEN` is not set, tools use file-based backlog (backward compatible).

## Tools

| Tool | Description |
|------|-------------|
| `validate_backlog` | Validate backlog structure, naming, cross-refs |
| `backlog_metrics` | Backlog health, aging, velocity |
| `check_links` | Check markdown links |
| `generate_release_notes_draft` | Draft from commits (supports `--auto`) |
| `validate_backlog_integrity` | Orphan refs, duplicates, Fibonacci |
| `visualize_dependencies` | Mermaid dependency graph |
| `lint_project_management` | Full lint |
| `prepare_gap_check` | Pre-commit doc-code consistency reminder |
| `create_user_story` | Create US-XXX and add to backlog (GitHub or file) |
| `create_defect` | Create DEF-XXX and add to backlog (GitHub or file) |
| `create_technical_debt` | Create TD-XXX and add to backlog (GitHub or file) |
| `setup_github_project` | Ensure GitHub labels and project columns (when GITHUB_TOKEN set) |
| `list_backlog` | List backlog items from GitHub |
| `get_backlog_metrics_github` | Aggregate metrics from GitHub |
| `update_issue_status` | Move issue between Todo / In Progress / Done |
| `update_issue` | Update issue title, body, labels |
| `sync_backlog_to_markdown` | Generate product-backlog.md from GitHub |

## Resources (pm://)

- `pm://index` — Project Management Index
- `pm://glossary` — Terminology
- `pm://product-backlog` — Product backlog (file-based)
- `pm://github/backlog` — Backlog from GitHub (when GITHUB_TOKEN set)
- `pm://processes/{name}` — Process docs
- `pm://criteria/{name}` — DoR, DoD, etc.
- `pm://backlog/user-stories` — List all user stories
- `pm://backlog/user-stories/{id}` — User story by ID
- `pm://backlog/defects` — List all defects
- `pm://backlog/defects/{id}` — Defect by ID
- `pm://sprints` — List all sprints
- `pm://sprints/{id}` — Sprint by ID

## Run manually

```bash
python -m mcp_project_management.server
```

Uses stdio transport by default (for MCP clients).
