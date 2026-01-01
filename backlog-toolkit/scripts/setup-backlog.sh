#!/bin/bash
# Setup Backlog Structure Script
# Creates the basic folder structure for backlog management

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLKIT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Create project-management at the root of backlog-toolkit
BACKLOG_DIR="${TOOLKIT_DIR}/project-management"
FEATURES_DIR="${BACKLOG_DIR}/backlog/features"
BUGS_DIR="${BACKLOG_DIR}/backlog/bugs"
SPRINTS_DIR="${BACKLOG_DIR}/sprints"
DOCS_DIR="${BACKLOG_DIR}/docs"
TEMPLATES_DIR="${DOCS_DIR}/templates"
PROCESSES_DIR="${DOCS_DIR}/processes"

echo -e "${BLUE}Setting up backlog management structure in backlog-toolkit...${NC}"
echo -e "${BLUE}Creating project-management folder at: ${BACKLOG_DIR}${NC}"
echo ""
echo -e "${YELLOW}Note: This creates an example structure in the backlog-toolkit project.${NC}"
echo -e "${YELLOW}For your own project, copy this structure or customize as needed.${NC}"
echo ""

# Create directory structure
echo -e "${GREEN}Creating directory structure...${NC}"
mkdir -p "${FEATURES_DIR}"
mkdir -p "${BUGS_DIR}"
mkdir -p "${SPRINTS_DIR}"
mkdir -p "${DOCS_DIR}"

echo -e "  ✓ Created: ${FEATURES_DIR}"
echo -e "  ✓ Created: ${BUGS_DIR}"
echo -e "  ✓ Created: ${SPRINTS_DIR}"
echo -e "  ✓ Created: ${DOCS_DIR}"
echo ""

# Ask if user wants to copy templates
read -p "Copy templates directory? (y/n) [y]: " COPY_TEMPLATES
COPY_TEMPLATES=${COPY_TEMPLATES:-y}

if [[ "$COPY_TEMPLATES" =~ ^[Yy]$ ]]; then
    if [ -d "${TOOLKIT_DIR}/templates" ]; then
        echo -e "${GREEN}Copying templates...${NC}"
        mkdir -p "${TEMPLATES_DIR}"
        cp -r "${TOOLKIT_DIR}/templates"/* "${TEMPLATES_DIR}/"
        echo -e "  ✓ Copied templates to ${TEMPLATES_DIR}"
    else
        echo -e "${YELLOW}⚠ Templates directory not found at ${TOOLKIT_DIR}/templates${NC}"
    fi
    echo ""
fi

# Ask if user wants to copy processes
read -p "Copy processes directory? (y/n) [y]: " COPY_PROCESSES
COPY_PROCESSES=${COPY_PROCESSES:-y}

if [[ "$COPY_PROCESSES" =~ ^[Yy]$ ]]; then
    if [ -d "${TOOLKIT_DIR}/processes" ]; then
        echo -e "${GREEN}Copying processes...${NC}"
        mkdir -p "${PROCESSES_DIR}"
        cp -r "${TOOLKIT_DIR}/processes"/* "${PROCESSES_DIR}/"
        echo -e "  ✓ Copied processes to ${PROCESSES_DIR}"
    else
        echo -e "${YELLOW}⚠ Processes directory not found at ${TOOLKIT_DIR}/processes${NC}"
    fi
    echo ""
fi

# Ask if user wants to create initial product backlog
read -p "Create initial product backlog file? (y/n) [y]: " CREATE_BACKLOG
CREATE_BACKLOG=${CREATE_BACKLOG:-y}

if [[ "$CREATE_BACKLOG" =~ ^[Yy]$ ]]; then
    BACKLOG_FILE="${BACKLOG_DIR}/backlog/product-backlog.md"
    
    # Check if template exists
    if [ -f "${TOOLKIT_DIR}/templates/product-backlog-table-template.md" ]; then
        cp "${TOOLKIT_DIR}/templates/product-backlog-table-template.md" "${BACKLOG_FILE}"
        # Update the "Last Updated" date
        TODAY=$(date +%Y-%m-%d)
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s/\[YYYY-MM-DD\]/${TODAY}/g" "${BACKLOG_FILE}"
        else
            # Linux
            sed -i "s/\[YYYY-MM-DD\]/${TODAY}/g" "${BACKLOG_FILE}"
        fi
        echo -e "${GREEN}Created product backlog: ${BACKLOG_FILE}${NC}"
    else
        # Create a basic product backlog if template doesn't exist
        cat > "${BACKLOG_FILE}" << 'EOF'
# Product Backlog

This is the main product backlog tracking all feature requests and bug fixes.

**Last Updated**: [YYYY-MM-DD]

## Feature Requests

| ID | Title | Priority | Points | Status | Sprint | Created | Updated |
|----|-------|----------|--------|--------|--------|---------|---------|

## Bug Fixes

| ID | Title | Priority | Points | Status | Sprint | Created | Updated |
|----|-------|----------|--------|--------|--------|---------|---------|

---

## Status Values

- ⭕ **Not Started**: Item not yet started
- ⏳ **In Progress**: Item currently being worked on
- ✅ **Completed**: Item finished and verified

## Priority Levels

- 🔴 **Critical**: Blocks core functionality, must be fixed/implemented immediately
- 🟠 **High**: Important feature/bug, should be addressed soon
- 🟡 **Medium**: Nice to have, can wait
- 🟢 **Low**: Future consideration, low priority
EOF
        TODAY=$(date +%Y-%m-%d)
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/\[YYYY-MM-DD\]/${TODAY}/g" "${BACKLOG_FILE}"
        else
            sed -i "s/\[YYYY-MM-DD\]/${TODAY}/g" "${BACKLOG_FILE}"
        fi
        echo -e "${GREEN}Created basic product backlog: ${BACKLOG_FILE}${NC}"
    fi
    echo ""
fi

# Create README files
echo -e "${GREEN}Creating README files...${NC}"

# Create main README
cat > "${BACKLOG_DIR}/README.md" << 'EOF'
# Project Management

This directory contains the backlog management structure for this project.

## Structure

```
project-management/
├── backlog/              # Active backlog items
│   ├── product-backlog.md    # Main backlog overview
│   ├── features/            # Feature requests (FR-XXX-*.md)
│   └── bugs/                # Bug fixes (BF-XXX-*.md)
├── sprints/             # Sprint planning documents
│   └── sprint-XX-*.md
└── docs/                # Reference documentation
    ├── templates/       # Template files
    └── processes/       # Process documentation
```

## Quick Start

1. **View the backlog**: Open `backlog/product-backlog.md`
2. **Create a feature**: Copy `docs/templates/feature-request-template.md` to `backlog/features/FR-XXX-name.md`
3. **Create a bug fix**: Copy `docs/templates/bug-fix-template.md` to `backlog/bugs/BF-XXX-name.md`
4. **Plan a sprint**: Copy `docs/templates/sprint-planning-template.md` to `sprints/sprint-XX-name.md`

## Workflow

### Daily Work
- Update status in `backlog/product-backlog.md`
- Work on items in `backlog/features/` or `backlog/bugs/`

### Creating New Items
- Use templates from `docs/templates/`
- Add entry to `backlog/product-backlog.md`
- Follow naming: `FR-XXX-feature-name.md` or `BF-XXX-bug-name.md`

### Sprint Planning
- Create sprint document in `sprints/`
- Reference backlog items
- Update backlog with sprint assignments

## Reference Materials

- **Templates**: See `docs/templates/` for creating new items
- **Processes**: See `docs/processes/` for workflow guidance
- **Documentation**: See `docs/README.md` for detailed reference guide

## Status Values

- ⭕ **Not Started**: Item not yet started
- ⏳ **In Progress**: Item currently being worked on
- ✅ **Completed**: Item finished and verified

## Priority Levels

- 🔴 **Critical**: Must be fixed/implemented immediately
- 🟠 **High**: Should be addressed soon
- 🟡 **Medium**: Nice to have, can wait
- 🟢 **Low**: Future consideration

---

For more information, see the backlog toolkit documentation.
EOF

echo -e "  ✓ Created: ${BACKLOG_DIR}/README.md"

# Create docs README
if [ -d "${DOCS_DIR}" ]; then
    cat > "${DOCS_DIR}/README.md" << 'EOF'
# Reference Documentation

This directory contains reference materials for backlog management.

## Contents

### Templates (`templates/`)

Template files for creating backlog items:

- **feature-request-template.md** - For new features and enhancements
- **bug-fix-template.md** - For bug reports and fixes
- **sprint-planning-template.md** - For sprint planning
- **product-backlog-table-template.md** - For the main backlog table

**Usage:**
1. Copy the appropriate template
2. Fill in all sections
3. Save to the appropriate directory (`backlog/features/` or `backlog/bugs/`)
4. Add entry to `backlog/product-backlog.md`

### Processes (`processes/`)

Process documentation explaining workflows:

- **backlog-management-process.md** - How to manage the backlog
- **product-backlog-structure.md** - Backlog structure and conventions

**Usage:**
- Reference when learning the process
- Review during backlog refinement
- Share with new team members

## Quick Reference

### Creating a Feature Request

```bash
cp docs/templates/feature-request-template.md backlog/features/FR-001-feature-name.md
# Edit FR-001-feature-name.md
# Add entry to backlog/product-backlog.md
```

### Creating a Bug Fix

```bash
cp docs/templates/bug-fix-template.md backlog/bugs/BF-001-bug-description.md
# Edit BF-001-bug-description.md
# Add entry to backlog/product-backlog.md
```

### Planning a Sprint

```bash
cp docs/templates/sprint-planning-template.md sprints/sprint-01-sprint-name.md
# Edit sprint-01-sprint-name.md
# Add user stories from backlog
```

## File Naming Conventions

- **Features**: `FR-XXX-feature-name.md` (e.g., `FR-042-user-authentication.md`)
- **Bugs**: `BF-XXX-bug-description.md` (e.g., `BF-015-email-validation.md`)
- **Sprints**: `sprint-XX-sprint-name.md` (e.g., `sprint-05-user-auth.md`)

Use kebab-case (lowercase with hyphens) for names.

## Best Practices

1. **Always use templates** - Don't create files from scratch
2. **Fill all sections** - Complete templates ensure consistency
3. **Update regularly** - Keep status and dates current
4. **Link properly** - Use correct relative paths in links
5. **Follow naming** - Use consistent ID formats and naming

---

For more help, see the main backlog toolkit documentation.
EOF
    echo -e "  ✓ Created: ${DOCS_DIR}/README.md"
fi

echo ""

# Summary
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Backlog structure setup complete!${NC}"
echo ""
echo -e "${BLUE}Directory structure:${NC}"
echo "  ${BACKLOG_DIR}/"
echo "  ├── README.md"
echo "  ├── backlog/"
echo "  │   ├── product-backlog.md"
echo "  │   ├── features/"
echo "  │   └── bugs/"
echo "  ├── sprints/"
echo "  └── docs/"
echo "      ├── README.md"
echo "      ├── templates/"
echo "      └── processes/"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  1. Create your first feature request:"
echo "     cp ${TEMPLATES_DIR}/feature-request-template.md ${FEATURES_DIR}/FR-001-your-feature.md"
echo ""
echo "  2. Create your first bug fix:"
echo "     cp ${TEMPLATES_DIR}/bug-fix-template.md ${BUGS_DIR}/BF-001-bug-description.md"
echo ""
echo "  3. Add entries to product-backlog.md"
echo ""
echo -e "${BLUE}Note:${NC}"
echo "  This structure was created in the backlog-toolkit project as an example."
echo "  To use in your own project, copy the structure or run setup in your project directory."
echo ""
echo -e "${BLUE}For more help, see:${NC}"
echo "  - Quick Start: ${TOOLKIT_DIR}/quick-start.md"
echo "  - Template Catalog: ${TOOLKIT_DIR}/template-catalog.md"
echo ""

