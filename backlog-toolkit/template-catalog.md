# Template Catalog

Quick reference guide for all available templates in this package. Use this catalog to find the right template for your needs.

## Quick Reference Table

| Template | Use Case | Prerequisites | Output | Time to Complete | Priority |
|----------|----------|---------------|--------|-----------------|----------|
| [Feature Request](templates/feature-request-template.md) | New feature or enhancement | Requirements, user needs | FR-XXX.md | 15-30 min | 🟠 High |
| [Bug Fix](templates/bug-fix-template.md) | Bug report or fix | Bug details, reproduction steps | BF-XXX.md | 10-20 min | 🟠 High |
| [Sprint Planning](templates/sprint-planning-template.md) | Sprint setup and tracking | Backlog items, team capacity | sprint-XX.md | 1-2 hours | 🟡 Medium |
| [Product Backlog Table](templates/product-backlog-table-template.md) | Central backlog tracking | Feature requests, bug fixes | product-backlog.md | 30-60 min | 🟠 High |

## Template Selection Guide

### When to Use Each Template

#### Feature Request Template
**Use when:**
- Adding a new feature to the product
- Requesting an enhancement to existing functionality
- Documenting a user story or requirement
- Planning work that adds value to users

**Don't use for:**
- Bug fixes (use Bug Fix Template)
- Technical tasks without user value (consider breaking down)
- Questions or discussions (use issue tracker)

**Example scenarios:**
- "Add user authentication"
- "Implement search functionality"
- "Create dashboard for analytics"
- "Add dark mode theme"

#### Bug Fix Template
**Use when:**
- Reporting a bug or defect
- Documenting unexpected behavior
- Tracking a fix for an issue
- Documenting workarounds

**Don't use for:**
- New features (use Feature Request Template)
- Enhancement requests (use Feature Request Template)
- Questions (use issue tracker or documentation)

**Example scenarios:**
- "Login fails with special characters in email"
- "Dashboard shows incorrect totals"
- "App crashes on mobile devices"
- "API returns 500 error for invalid input"

#### Sprint Planning Template
**Use when:**
- Planning a new sprint
- Tracking sprint progress
- Breaking down user stories into tasks
- Documenting sprint goals and deliverables

**Don't use for:**
- Individual backlog items (use Feature Request or Bug Fix)
- Long-term roadmap (use separate planning document)
- Release planning (use separate document)

**Example scenarios:**
- "Sprint 5: User Authentication"
- "Sprint 6: Search & Filtering"
- "Sprint 7: Performance Optimization"

#### Product Backlog Table Template
**Use when:**
- Creating the main backlog overview
- Tracking all feature requests and bug fixes
- Providing stakeholders with backlog status
- Prioritizing and organizing work

**Don't use for:**
- Detailed item information (use individual templates)
- Sprint-specific tracking (use Sprint Planning Template)
- Task-level tracking (use Sprint Planning Template)

**Example scenarios:**
- "Main product backlog"
- "Q1 2025 Backlog"
- "MVP Backlog"

## Use Case Matrix

| Scenario | Primary Template | Secondary Template | Notes |
|----------|------------------|-------------------|-------|
| New feature idea | Feature Request | Product Backlog Table | Add to backlog after creation |
| Bug discovered | Bug Fix | Product Backlog Table | Add to backlog, prioritize |
| Sprint planning | Sprint Planning | Feature Request / Bug Fix | Reference backlog items |
| Backlog overview | Product Backlog Table | All templates | Links to detailed items |
| User story | Feature Request | Sprint Planning | Break down in sprint |
| Technical task | Feature Request | Sprint Planning | Ensure it has user value |
| Enhancement | Feature Request | Product Backlog Table | Treat as new feature |
| Critical bug | Bug Fix | Product Backlog Table | High priority, may skip backlog |

## Template Dependencies

```
Product Backlog Table
    ├── Feature Request (links to)
    ├── Bug Fix (links to)
    └── Sprint Planning (references items from)

Sprint Planning
    ├── Feature Request (includes stories from)
    └── Bug Fix (includes bugs from)

Feature Request / Bug Fix
    └── Product Backlog Table (added to)
```

## Template Selection Flowchart

```
Start: What do you need to document?
│
├─ New feature or enhancement?
│  └─> Use Feature Request Template
│
├─ Bug or defect?
│  └─> Use Bug Fix Template
│
├─ Planning a sprint?
│  └─> Use Sprint Planning Template
│
└─ Need backlog overview?
   └─> Use Product Backlog Table Template
```

## Template Comparison

### Feature Request vs. Bug Fix

| Aspect | Feature Request | Bug Fix |
|--------|----------------|---------|
| **Purpose** | Add new functionality | Fix existing functionality |
| **Focus** | User value, business case | Problem, reproduction, solution |
| **Structure** | User story, acceptance criteria | Steps to reproduce, root cause |
| **Priority** | Often based on value | Often based on impact |
| **Estimation** | Story points for effort | Story points for complexity |

### Sprint Planning vs. Product Backlog

| Aspect | Sprint Planning | Product Backlog |
|--------|----------------|-----------------|
| **Scope** | Single sprint | Entire product |
| **Timeframe** | 1-3 weeks | Ongoing |
| **Detail Level** | Tasks and breakdown | High-level items |
| **Updates** | Daily during sprint | Weekly/bi-weekly |
| **Purpose** | Execution tracking | Prioritization |

## Integration with Other Tools

### GitHub Issues
- Use templates to structure issue descriptions
- Copy template content into issue body
- Link issues to backlog items

### Jira
- Use templates as issue templates
- Map template fields to Jira fields
- Import backlog items from templates

### Linear
- Use templates for issue creation
- Structure descriptions using templates
- Sync with backlog table

### Notion
- Use templates as database templates
- Create pages from templates
- Link pages in backlog database

## Best Practices

### Template Selection
1. **Start simple**: Use Feature Request and Bug Fix for most work
2. **Add structure gradually**: Add Sprint Planning when using sprints
3. **Maintain overview**: Always keep Product Backlog Table updated
4. **Link everything**: Connect templates through references

### Template Usage
1. **Copy templates, not examples**: Always start from templates
2. **Fill all sections**: Don't skip required fields
3. **Update regularly**: Keep status and dates current
4. **Link properly**: Use correct relative paths

### Template Customization
1. **Adapt to your needs**: Add/remove sections as needed
2. **Keep consistency**: Use same structure across items
3. **Document changes**: Note customizations in your project
4. **Share with team**: Ensure everyone uses same templates

## Examples

See [examples/](examples/) directory for filled-out examples of each template:
- [Feature Request Example](examples/feature-request-example.md)
- [Bug Fix Example](examples/bug-fix-example.md)
- [Sprint Planning Example](examples/sprint-planning-example.md)
- [Product Backlog Example](examples/product-backlog-example.md)

## Quick Links

- [Feature Request Template](templates/feature-request-template.md)
- [Bug Fix Template](templates/bug-fix-template.md)
- [Sprint Planning Template](templates/sprint-planning-template.md)
- [Product Backlog Table Template](templates/product-backlog-table-template.md)
- [Examples Directory](examples/)
- [Quick Start Guide](quick-start.md)
- [Quick Reference](quick-reference.md)

---

**Last Updated**: 2025-01-27  
**Version**: 1.1.0

