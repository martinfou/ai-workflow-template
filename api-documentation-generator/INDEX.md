# Documentation Generator — Index

**What this is**: The single, authoritative instruction set for generating and maintaining documentation for **Spring Boot** (REST APIs) and **Spring Batch** applications. Designed for **LLMs** (consistent, traceable, non-hallucinated output) and **humans** (developers, analysts, auditors, management).

**Context**: Financial institution in Canada. Documentation must be accurate, traceable to code, and suitable for compliance, handover, and audit.

**Version**: 1.0 · **Last updated**: 2026-03-17

---

## Why this exists

- **Single source of truth**: One place for “how we document” so every pass (human or LLM) produces consistent, comparable docs.
- **Traceability**: Every factual claim links to code or config — no invented endpoints, status codes, or business rules.
- **Audit-ready**: Code references (file, class, method or config key) support compliance and handover.

---

## Principles

| Principle | Meaning |
|-----------|---------|
| **Code is source of truth** | Document only what exists in code, config, or build files. Never invent endpoints, auth, or status codes. |
| **Mermaid only** | All charts and diagrams use Mermaid. No ASCII art, no checked-in PNG/SVG for architecture or flow. |
| **Trace and explain** | For each endpoint/job: follow controller → service → database (and back); describe what the system does in **business terms**. |

---

## Scope

| In scope | Out of scope |
|----------|---------------|
| Spring Boot REST APIs (controllers, services, persistence) | Non-Spring or non-JVM stacks (document only what exists) |
| Spring Batch jobs, steps, readers, writers, processors | Invented or assumed behaviour |
| Business rules (state transitions, calculations) from code/comments/Javadoc | Business rules not traceable to code |
| Outbound integrations (REST, SOAP, message queues) | Third-party API docs (only our usage) |
| Deployment, environment variables, database schema (from repo) | Deployment or schema not in repo |
| Mermaid-only diagrams; critique and consistency flow | Other diagram formats; docs without critique |

---

## Quick start

**LLM**

1. Read [00-how-to-use-this-guide.md](00-how-to-use-this-guide.md) and [01-project-detection.md](01-project-detection.md).
2. Detect project type (Spring Boot REST, Spring Batch, or both), then apply guides 02–05 and 06–07.
3. Generate docs from [08-canonical-examples.md](08-canonical-examples.md), then run [09-critique-and-consistency.md](09-critique-and-consistency.md) until the report is clean or the human approves exceptions.

**Human**

- Start with this INDEX and [00-how-to-use-this-guide.md](00-how-to-use-this-guide.md).
- Use [08-canonical-examples.md](08-canonical-examples.md) to see what “good” looks like.
- Use [09-critique-and-consistency.md](09-critique-and-consistency.md) to review generated docs.

---

## Document map

| # | Document | Content |
|---|----------|---------|
| [00](00-how-to-use-this-guide.md) | How to use this guide | LLM + human flow, order of operations, output structure |
| [01](01-project-detection.md) | Project detection | Detect Spring Boot vs Spring Batch from code and build |
| [02](02-rest-api-documentation.md) | REST API | Endpoint discovery, per-endpoint content, grouping, diagrams |
| [03](03-batch-documentation.md) | Batch | Job discovery, per-job content, flowcharts, step diagrams |
| [04](04-business-rules.md) | Business rules | Source (code/comments/Javadoc), format, scope, anti-hallucination |
| [05](05-integrations.md) | Integrations | REST, SOAP, message queues, diagrams |
| [06](06-diagrams-mermaid.md) | Diagrams (Mermaid) | Mermaid only, style, avoiding lexical errors |
| [07](07-anti-hallucination.md) | Anti-hallucination | Code as source of truth; never invent, assume, or guess |
| [08](08-canonical-examples.md) | Canonical examples | Templates per doc type (endpoint, job, rule, integration) |
| [09](09-critique-and-consistency.md) | Critique and consistency | When to critique, checklist, report and fix process |
| [10](10-other-doc-types.md) | Other doc types | Deployment, environment variables, database schema |

---

## How to use (LLM)

1. **Start**: [00-how-to-use-this-guide.md](00-how-to-use-this-guide.md) — role, flow, order of operations.
2. **Detect**: [01-project-detection.md](01-project-detection.md) — Spring Boot (REST), Spring Batch, or both.
3. **Apply guides**: REST → [02](02-rest-api-documentation.md), Batch → [03](03-batch-documentation.md), Business rules → [04](04-business-rules.md), Integrations → [05](05-integrations.md).
4. **Diagrams**: [06-diagrams-mermaid.md](06-diagrams-mermaid.md) — Mermaid-only rules and style.
5. **Anti-hallucination**: [07-anti-hallucination.md](07-anti-hallucination.md) — what you must never do.
6. **Examples**: [08-canonical-examples.md](08-canonical-examples.md) — match structure exactly.
7. **Critique**: [09-critique-and-consistency.md](09-critique-and-consistency.md) — checklist, inconsistency report, fix, re-check.
8. **Other**: [10-other-doc-types.md](10-other-doc-types.md) — deployment, env, DB schema.

**Output**: Write all generated documentation under `/docs`, using the structure in [00-how-to-use-this-guide.md](00-how-to-use-this-guide.md#output-structure-best-practice).

---

## How to use (human)

- **Onboarding / handover**: Read this INDEX and 00-how-to-use-this-guide.md. Use 08-canonical-examples.md to see what “good” looks like.
- **Reviewing generated docs**: Use the checklist in 09-critique-and-consistency.md.
- **Audit / compliance**: Code is source of truth; every factual claim must be traceable to code (see 07-anti-hallucination.md). Require a **code reference** (file and symbol) for every endpoint, job, rule, and integration claim.
