# Critique and Consistency

**Purpose**: Define when and how the LLM critiques generated documentation, what checklist to use, and how to report and fix inconsistencies. Follow industry best practice for review and consistency.

**Related**: [00-how-to-use-this-guide.md](00-how-to-use-this-guide.md), [07-anti-hallucination.md](07-anti-hallucination.md), [08-canonical-examples.md](08-canonical-examples.md)

---

## When to run the critique

- **After** generating or updating a batch of documentation (e.g. all REST endpoints, all batch jobs, or one full pass over `docs/`).
- **Before** considering documentation “done” — so that inconsistencies are fixed in the same session or explicitly accepted by a human.

The LLM runs the critique as part of the flow in [00-how-to-use-this-guide.md](00-how-to-use-this-guide.md#order-of-operations) (step 5).

---

## Before you start

Ensure you have: (1) generated docs under `docs/` per the output structure, (2) access to the same codebase that was documented, (3) the checklist below. Run the checklist systematically and record pass/fail and any findings.

---

## Checklist (what to verify)

Use this checklist when critiquing. For each item, confirm **pass** or list **failures**.

### 1. Completeness

- [ ] Every endpoint present in code is documented under `docs/api/` (or equivalent).
- [ ] Every Job defined in code is documented under `docs/batch/`.
- [ ] Every outbound integration (REST client, SOAP client, queue producer/consumer) is documented under `docs/integrations/`.

### 2. Code as source of truth

- [ ] No documented endpoint, step, or operation that does not exist in code.
- [ ] No stated status code, auth, or business rule without a code reference (file/class/method or config).
- [ ] No invented retries, timeouts, or delivery semantics not present in code/config.

### 3. Structure and examples

- [ ] Each endpoint doc follows the structure in [08-canonical-examples.md](08-canonical-examples.md#example-1-rest-endpoint-single-endpoint).
- [ ] Each job doc follows the structure in [08-canonical-examples.md](08-canonical-examples.md#example-2-batch-job).
- [ ] Business rules and integrations follow the table/list format and include a source column or “Source: …”.

### 4. Diagrams

- [ ] All diagrams are Mermaid only ([06-diagrams-mermaid.md](06-diagrams-mermaid.md)).
- [ ] Labels with special characters (e.g. paths) are quoted to avoid lexical errors.
- [ ] Overview, per-endpoint sequence, and per-endpoint flow exist as required by 02; job flows and decision steps as required by 03.

### 5. Cross-references and naming

- [ ] Job names, step names, and paths in docs match code exactly (no typos or assumed names).
- [ ] Links between docs (e.g. overview → endpoint, job → step) are correct and not broken.
- [ ] Terminology is consistent (e.g. same name for the same external system or queue).

### 6. Inconsistencies

- [ ] No contradiction between two doc files (e.g. different status codes for the same endpoint).
- [ ] No contradiction between doc and code; where they differ, code wins and the doc must be updated or the discrepancy called out in the report.

---

## What counts as an inconsistency

| Type | Description | Resolution |
|------|-------------|------------|
| **Doc vs code** | Documentation says X (e.g. “returns 201”), code does Y (e.g. returns 200). | Update doc to match code; code is source of truth. |
| **Doc vs doc** | Two docs state different facts (e.g. same endpoint, different path). | Reconcile with code; fix the wrong doc. |
| **Missing reference** | A business rule or integration detail has no code reference. | Add the reference or remove the claim. |
| **Missing coverage** | Code has an endpoint/job/integration that has no doc. | Add the missing doc. |
| **Invented content** | Doc describes behaviour not present in code. | Remove the invented content or add a clear “Not in code” / “Assumed for discussion” note only if the human explicitly requests it. |

---

## Inconsistency report format

Produce a report in this format (e.g. in the chat or in `docs/critique-report.md`):

```markdown
## Documentation critique report — [Date]

### Completeness
- [Pass / Fail] [Any missing endpoints, jobs, or integrations listed.]

### Code as source of truth
- [Pass / Fail] [Any invented or unreferenced claims listed.]

### Structure and examples
- [Pass / Fail] [Any deviations from canonical examples.]

### Diagrams
- [Pass / Fail] [Any non-Mermaid or broken diagrams.]

### Cross-references and naming
- [Pass / Fail] [Any broken links or naming mismatches.]

### Inconsistencies (doc vs code, doc vs doc)
- [List each: location, issue, recommended fix, **Severity**: Blocker | Minor.]

**Severity**: **Blocker** = doc invalid until fixed (invented endpoint, missing code reference, doc/code contradiction). **Minor** = style, broken link, or optional improvement.

### Human decisions
- [To be filled after human review: accept exception, request change, etc.]

### Sign-off
- [ ] All blocker issues resolved or explicitly accepted by human.
- [ ] Human approval for any remaining exceptions: _________________
```

---

## After the report: fix and re-run

1. **Fix** all blocker issues and as many minor issues as practical.
2. **Re-run** the full checklist after any change that adds/removes endpoints, jobs, or integrations, or that changes status codes, auth, or business rules.
3. **Re-run criteria**: Re-run until all items pass or the human approves remaining exceptions. Then documentation can be considered complete for that pass.
