# Scripts

Scripts to set up, validate backlog structure, templates, and cross-references.

## Available Scripts

### setup-backlog.sh

Creates the basic folder structure for backlog management in the backlog-toolkit project.

**Usage:**
```bash
./scripts/setup-backlog.sh
```

**Note:** This script creates the `project-management/` folder at the root of the backlog-toolkit directory, not in your project. This is for demonstration/example purposes within the toolkit itself.

**What it does:**
- Creates directory structure:
  - `project-management/backlog/features/`
  - `project-management/backlog/bugs/`
  - `project-management/sprints/`
  - `project-management/docs/` (for templates and processes)
- Optionally copies templates directory to `docs/templates/`
- Optionally copies processes directory to `docs/processes/`
- Optionally creates initial product-backlog.md file

**Example:**
```bash
# From your project root
./scripts/setup-backlog.sh

# Or specify a different project root
./scripts/setup-backlog.sh /path/to/your/project
```

**Interactive prompts:**
- Copy templates? (y/n)
- Copy processes? (y/n)
- Create initial product backlog? (y/n)

**Output:**
- Creates all necessary directories
- Copies files if requested
- Shows next steps and helpful commands

### validate-template.sh

Validates that a backlog item template is complete and properly formatted.

**Usage:**
```bash
./scripts/validate-template.sh <template-file.md>
```

**Checks:**
- Required fields are present
- User story format (for feature requests)
- Acceptance criteria count (minimum 3)
- Steps to reproduce (for bug fixes)
- Status and priority emojis
- Placeholder text
- Markdown links

**Example:**
```bash
./scripts/validate-template.sh backlog/features/FR-042-user-authentication.md
```

### validate-backlog.sh

Validates backlog structure, file naming conventions, and cross-references.

**Usage:**
```bash
./scripts/validate-backlog.sh [backlog-directory]
```

**Default:** `project-management/backlog`

**Checks:**
- Directory structure exists
- File naming conventions (FR-XXX-*.md, BF-XXX-*.md)
- Product backlog table structure
- Link references

**Example:**
```bash
./scripts/validate-backlog.sh project-management/backlog
```

### check-links.sh

Checks for broken markdown links in backlog files.

**Usage:**
```bash
./scripts/check-links.sh [backlog-directory] [base-directory]
```

**Default:** 
- `backlog-directory`: `project-management/backlog`
- `base-directory`: `.` (current directory)

**Checks:**
- All markdown links in backlog files
- Relative path resolution
- File existence

**Example:**
```bash
./scripts/check-links.sh project-management/backlog .
```

## Making Scripts Executable

Before using the scripts, make them executable:

```bash
chmod +x scripts/*.sh
```

## Integration

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Validate backlog before commit

./scripts/validate-backlog.sh project-management/backlog
if [ $? -ne 0 ]; then
    echo "Backlog validation failed. Commit aborted."
    exit 1
fi
```

### CI/CD Pipeline

Add to your CI/CD pipeline (GitHub Actions, GitLab CI, etc.):

```yaml
# Example for GitHub Actions
- name: Validate Backlog
  run: |
    chmod +x scripts/*.sh
    ./scripts/validate-backlog.sh project-management/backlog
```

## Exit Codes

- `0`: Validation passed
- `1`: Validation failed (errors found)
- `2`: Script error (file not found, etc.)

## Output

Scripts use color-coded output:
- 🟢 Green: Passed checks
- 🟡 Yellow: Warnings
- 🔴 Red: Errors

## Notes

- Scripts require bash
- Some checks are basic (e.g., link checking may not resolve all relative paths correctly)
- Manual review is still recommended
- Scripts can be customized for your project structure

## Troubleshooting

### Script not executable

```bash
chmod +x scripts/validate-template.sh
```

### Path issues

Update paths in scripts or pass as arguments:
```bash
./scripts/validate-backlog.sh /custom/path/to/backlog
```

### Missing dependencies

Scripts only require bash. No additional dependencies needed.

---

**Last Updated**: 2025-01-27  
**Version**: 1.1.0

