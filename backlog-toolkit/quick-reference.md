# Quick Reference

Cheat sheets and quick guides for common backlog management tasks.

## Status Values

| Status | Emoji | Meaning | When to Use |
|--------|-------|---------|-------------|
| Not Started | ⭕ | Item not yet started | New items, items in backlog |
| In Progress | ⏳ | Currently being worked on | Active development, assigned to sprint |
| Completed | ✅ | Finished and verified | Done, tested, deployed |

### Status Lifecycle

```
⭕ Not Started → ⏳ In Progress → ✅ Completed
```

**Notes:**
- Items can move from In Progress back to Not Started if work is paused
- Completed items should not be reopened (create new item instead)
- Update status daily for active items

## Priority Levels

| Priority | Emoji | Meaning | When to Use |
|----------|-------|---------|-------------|
| Critical | 🔴 | Must fix/implement immediately | Blocks core functionality, security issues, data loss |
| High | 🟠 | Should be addressed soon | Important features, significant user impact |
| Medium | 🟡 | Nice to have | Moderate value, can wait |
| Low | 🟢 | Future consideration | Low priority, can be deferred |

### Priority Guidelines

**🔴 Critical:**
- Blocks core functionality
- Security vulnerabilities
- Data loss risks
- Production outages
- Must be fixed/implemented immediately

**🟠 High:**
- Important features for MVP
- Significant user value
- High user demand
- Should be addressed in next 1-2 sprints

**🟡 Medium:**
- Nice to have features
- Moderate user value
- Can wait for future sprints
- No immediate urgency

**🟢 Low:**
- Future considerations
- Low user value
- Can be deferred indefinitely
- Nice-to-have enhancements

## Story Points Guide

### Fibonacci Sequence

Use Fibonacci sequence for story point estimation:
- **1 Point**: Trivial task, < 1 hour
- **2 Points**: Simple task, 1-4 hours
- **3 Points**: Small task, 4-8 hours
- **5 Points**: Medium task, 1-2 days
- **8 Points**: Large task, 2-3 days
- **13 Points**: Very large task, 3-5 days (consider breaking down)

### Estimation Factors

Consider these factors when estimating:

1. **Complexity**: How complex is the task?
   - Simple logic: 1-2 points
   - Moderate complexity: 3-5 points
   - High complexity: 8-13 points

2. **Uncertainty**: How much is unknown?
   - Clear requirements: Lower points
   - Unclear requirements: Higher points
   - Research needed: Add points

3. **Effort**: How much work is required?
   - Small changes: 1-3 points
   - Medium changes: 5-8 points
   - Large changes: 13+ points (break down)

4. **Risk**: What are the risks?
   - Low risk: Standard points
   - Medium risk: Add 1-2 points
   - High risk: Add 3-5 points

### Story Point Examples

| Task | Points | Reasoning |
|------|--------|-----------|
| Fix typo in error message | 1 | Trivial, < 1 hour |
| Add new API endpoint | 3 | Small task, 4-8 hours |
| Implement user authentication | 13 | Large task, multiple days |
| Update database schema | 5 | Medium task, 1-2 days |
| Add unit tests | 2 | Simple task, 1-4 hours |

### Breaking Down Large Stories

If a story is 13+ points:
1. **Break it down** into smaller stories
2. **Aim for 5-8 points** per story
3. **Keep user value** in each story
4. **Identify dependencies** between stories

## File Naming Conventions

### Feature Requests
- **Format**: `FR-XXX-feature-name.md`
- **Example**: `FR-042-user-authentication.md`
- **Rules**: 
  - Use kebab-case for feature names
  - Zero-pad numbers (001, 042, not 1, 42)
  - Keep names descriptive but concise

### Bug Fixes
- **Format**: `BF-XXX-bug-description.md`
- **Example**: `BF-015-email-validation-plus-sign.md`
- **Rules**:
  - Use kebab-case for descriptions
  - Zero-pad numbers
  - Be specific in description

### Sprints
- **Format**: `sprint-XX-sprint-name.md`
- **Example**: `sprint-05-user-authentication.md`
- **Rules**:
  - Zero-pad numbers (01, 05, not 1, 5)
  - Use descriptive sprint name
  - Keep consistent naming

### Product Backlog
- **Format**: `product-backlog.md`
- **Location**: Root of backlog directory
- **Rules**:
  - Single file for main backlog
  - Update regularly
  - Keep sorted by priority

## ID Format Options

Common ID formats you can use:

| Format | Example | Use Case |
|--------|---------|----------|
| FR-XXX | FR-042 | Feature Request (default) |
| FEAT-XXX | FEAT-042 | Feature |
| STORY-XXX | STORY-042 | User Story |
| US-XXX | US-042 | User Story |
| BF-XXX | BF-015 | Bug Fix (default) |
| BUG-XXX | BUG-015 | Bug |
| FIX-XXX | FIX-015 | Fix |

**Customization:**
- Search and replace in templates
- Update config.yaml (if using)
- Document your format in project README

## Common Commands

### Creating a New Feature Request

```bash
# 1. Copy template
cp docs/templates/feature-request-template.md backlog/features/FR-042-feature-name.md

# 2. Edit the file
# 3. Add to product backlog table
```

### Creating a New Bug Fix

```bash
# 1. Copy template
cp docs/templates/bug-fix-template.md backlog/bugs/BF-015-bug-description.md

# 2. Edit the file
# 3. Add to product backlog table
```

### Creating a Sprint

```bash
# 1. Copy template
cp docs/templates/sprint-planning-template.md sprints/sprint-05-sprint-name.md

# 2. Edit the file
# 3. Add user stories from backlog
```

## User Story Format

### Standard Format

```
As a [user type], I want [functionality], so that [benefit].
```

### Examples

- **Good**: "As a registered user, I want to filter search results by date, so that I can quickly find recent items."
- **Good**: "As an admin, I want to export user data to CSV, so that I can generate reports."
- **Bad**: "Add date filter to search" (not a user story)
- **Bad**: "As a user, I want a button, so that I can click it" (no clear benefit)

### User Story Components

1. **User Type**: Who is the user? (registered user, admin, guest, etc.)
2. **Functionality**: What do they want? (action verb + feature)
3. **Benefit**: Why do they want it? (value, outcome)

## Acceptance Criteria Guidelines

### Good Acceptance Criteria

- ✅ **Specific**: Clear and unambiguous
- ✅ **Testable**: Can be verified with tests
- ✅ **Measurable**: Has clear success criteria
- ✅ **Complete**: Covers all scenarios

### Examples

**Good:**
- "User can log in with valid email and password"
- "Error message appears for invalid credentials"
- "Session persists across browser restarts"

**Bad:**
- "Login works" (too vague)
- "User should be happy" (not testable)
- "It should be fast" (not measurable)

## Template Validation Checklist

Before submitting a backlog item, ensure:

### Feature Request
- [ ] User story follows "As a... I want... So that..." format
- [ ] At least 3 acceptance criteria
- [ ] Business value is clear
- [ ] Dependencies identified
- [ ] Story points estimated
- [ ] Priority assigned
- [ ] Technical references included (if applicable)
- [ ] Links are correct

### Bug Fix
- [ ] Steps to reproduce are clear
- [ ] Expected vs. actual behavior documented
- [ ] Environment details complete
- [ ] Priority assigned based on impact
- [ ] Story points estimated
- [ ] Root cause identified (if known)
- [ ] Solution documented (if implemented)

## Quick Tips

### Writing Good Backlog Items
1. **Be specific**: Avoid vague descriptions
2. **Think user-first**: Focus on user value
3. **Make it testable**: Clear acceptance criteria
4. **Estimate realistically**: Use Fibonacci, compare to other items
5. **Prioritize wisely**: Consider value, risk, dependencies

### Managing Backlog
1. **Update daily**: Keep status current
2. **Refine weekly**: Review and clarify items
3. **Break down large items**: Aim for 5-8 points
4. **Remove obsolete items**: Keep backlog clean
5. **Link everything**: Connect related items

### Sprint Planning
1. **Select by priority**: Start with high-priority items
2. **Consider velocity**: Don't overcommit
3. **Break down stories**: Create tasks from stories
4. **Identify dependencies**: Plan accordingly
5. **Set sprint goal**: Clear, measurable objective

## Related Resources

- [Template Catalog](template-catalog.md) - Find the right template
- [Examples](examples/) - See templates in action
- [Glossary](glossary.md) - Terminology definitions
- [Quick Start](quick-start.md) - 5-minute setup guide

---

**Last Updated**: 2025-01-27  
**Version**: 1.1.0

