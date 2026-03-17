# Anti-Hallucination: Code as Source of Truth

**Purpose**: Code is the **source of truth**. The LLM must not invent, assume, or guess. Every factual claim in the documentation must be traceable to code, configuration, or build files.

**Related**: [02-rest-api-documentation.md](02-rest-api-documentation.md), [03-batch-documentation.md](03-batch-documentation.md), [04-business-rules.md](04-business-rules.md), [05-integrations.md](05-integrations.md), [09-critique-and-consistency.md](09-critique-and-consistency.md)

---

## Golden rules

| Rule | Meaning |
|------|---------|
| **Document only what exists** | In the codebase (source, config, Gradle/Maven). |
| **Code wins** | When documentation and code conflict, update the documentation to match the code (or flag the discrepancy in the critique report for human decision). |
| **No invented content** | Do not add endpoints, job steps, status codes, or business rules that are not present in code or explicitly stated in comments/Javadoc. |

---

## What the LLM must never do

1. **Invent endpoints**  
   Do not document REST paths or methods that are not implemented in controllers (or equivalent). Every endpoint in the docs must correspond to a mapping in code.

2. **Assume authentication**  
   Do not state that an endpoint “requires authentication” or “uses OAuth” unless the code or config explicitly shows it (e.g. security config, annotations, interceptors).

3. **Guess status codes**  
   Do not document HTTP status codes (e.g. “returns 400 on validation error”) unless the controller or exception handler actually returns that status. If only 200 is returned in code, document 200; do not add “typically 400 for …” without a code reference.

4. **Invent business rules**  
   See [04-business-rules.md](04-business-rules.md): every rule must have a code reference (file, class, method or comment location).

5. **Invent integration behaviour**  
   Do not document REST/SOAP/queue operations, retries, or timeouts that are not present in code or config.

6. **Assume “standard” behaviour**  
   Do not fill in “usual” or “standard” semantics (e.g. idempotency, ordering) unless the code or config explicitly implements or documents them.

---

## How to stay grounded

| Practice | Action |
|----------|--------|
| **Trace** | For each endpoint or job step, follow the code path and document only what you see. |
| **Cite** | For each factual claim (status code, transition, calculation, integration detail), point to the file and symbol (class/method or config key). |
| **Gap vs invent** | If something is missing (e.g. no explicit error handling), say “Not present in code” or “Not documented in code” rather than inventing behaviour. The critique step can list such gaps for human follow-up. |
| **Positive phrasing for gaps** | Prefer “Error handling for X is not present in the codebase” or “Status code for validation failure not explicitly returned in Controller or ControllerAdvice” over vague wording. Keeps the doc accurate and actionable. |

---

## Red lines (document invalid until fixed)

If any of the following occur, the generated documentation is **not** acceptable until corrected:

1. An **endpoint, job, or integration** is documented that **does not exist** in code.
2. A **status code, auth behaviour, or business rule** is stated **without a code reference**.
3. A **diagram** shows participants or flows **not present** in code.

Fix these before presenting the doc as complete; the critique report must flag them as **blocker**.
