# Quick Start Guide: Reusable Backlog Package

This guide helps you quickly adopt the backlog management templates and processes for your project.

## 📦 What You Get

A complete backlog management system with:
- ✅ 4 ready-to-use templates (Feature Request, Bug Fix, Product Backlog Table, Sprint Planning)
- ✅ 2 process documentation files (Backlog Management Process, Product Backlog Structure)
- ✅ All content is generic and adaptable to any project

## ⚡ 5-Minute Setup

### Step 1: Copy Files (2 minutes)

```bash
# Navigate to your project
cd /path/to/your/project

# Copy the package to your project-management directory
cp -r backlog-toolkit/* project-management/
```

Or manually copy:
- `templates/` directory → your `project-management/` folder
- `processes/` directory → your `project-management/` folder

### Step 2: Create Directory Structure (1 minute)

```bash
cd project-management
mkdir -p backlog/features
mkdir -p backlog/bugs
mkdir -p sprints
```

### Step 3: Create Your First Backlog (2 minutes)

1. **Create main backlog table**:
   ```bash
   cp docs/templates/product-backlog-table-template.md backlog/product-backlog.md
   ```

2. **Create your first feature request**:
   ```bash
   cp docs/templates/feature-request-template.md backlog/features/FR-001-your-first-feature.md
   # Edit FR-001-your-first-feature.md and fill in the details
   ```

3. **Add entry to backlog table**:
   - Open `backlog/product-backlog.md`
   - Add a row to the Feature Requests table
   - Link to your feature file: `[FR-001](features/FR-001-your-first-feature.md)`

## 🎯 Essential Customization

### 1. Update File Paths (5 minutes)

Search and replace in all template files:
- `artifacts/phase-5-management/` → your path structure
- Update any platform-specific paths

### 2. Update ID Format (Optional, 2 minutes)

If you don't want FR-XXX / BF-XXX format:
- Search for "FR-XXX" and "BF-XXX" in templates
- Replace with your format (e.g., "FEAT-XXX", "BUG-XXX")

### 3. Update Platform References (5 minutes)

In bug fix template, update the Environment section:
- Replace Android/iOS references with your platform
- Update browser/server environment details as needed

## 📋 Daily Workflow

### Adding a New Feature

1. Copy `docs/templates/feature-request-template.md`
2. Save as `backlog/features/FR-XXX-feature-name.md`
3. Fill in all sections
4. Add row to `backlog/product-backlog.md` table
5. Done!

### Reporting a Bug

1. Copy `docs/templates/bug-fix-template.md`
2. Save as `backlog/bugs/BF-XXX-bug-description.md`
3. Fill in steps to reproduce, expected/actual behavior
4. Add row to `backlog/product-backlog.md` table
5. Done!

### Planning a Sprint

1. Copy `docs/templates/sprint-planning-template.md`
2. Save as `sprints/sprint-XX-sprint-name.md`
3. Add user stories from backlog
4. Break down into tasks
5. Track progress during sprint

## 🔑 Key Concepts

### Status Lifecycle
- ⭕ **Not Started**: Just created, not worked on yet
- ⏳ **In Progress**: Currently being developed
- ✅ **Completed**: Done, tested, verified

### Priority Levels
- 🔴 **Critical**: Must fix/implement immediately
- 🟠 **High**: Should do soon
- 🟡 **Medium**: Nice to have
- 🟢 **Low**: Future consideration

### Story Points (Fibonacci)
- 1, 2, 3, 5, 8, 13
- Use to estimate effort/complexity
- Not time-based, relative sizing

## 📖 Next Steps

1. **Review examples**: Look at filled-out examples in [examples/](examples/)
2. **Review templates**: Look through files in [templates/](templates/)
3. **Understand processes**: Read files in [processes/](processes/)
4. **Check quick reference**: See [quick-reference.md](quick-reference.md) for cheat sheets
5. **Start using**: Create your first feature request or bug fix!

## ❓ Common Questions

**Q: Do I need all templates?**  
A: No. Start with Feature Request and Bug Fix templates. Add Sprint Planning if using sprints.

**Q: Can I change the ID format?**  
A: Yes! Search and replace FR-XXX/BF-XXX with your format.

**Q: How often should I update the backlog?**  
A: Update status daily for active items. Refine the backlog weekly/bi-weekly.

**Q: What if I don't use sprints?**  
A: Skip the Sprint Planning template. Use the backlog table to track work without sprints.

**Q: Can I customize the templates?**  
A: Absolutely! They're designed to be adapted. Add/remove sections as needed.

## 🎓 Learning Resources

- **Templates**: See `docs/templates/` directory for detailed template files
- **Processes**: See `docs/processes/` directory for workflow documentation
- **Template Catalog**: See `template-catalog.md` for template selection guide
- **README**: See `README.md` for package overview

---

**Need Help?** Review the detailed documentation in the package or check the source project for examples.

