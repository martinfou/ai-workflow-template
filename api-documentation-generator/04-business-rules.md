# Business Rules Documentation

**Purpose**: Capture business rules from code, comments, and Javadoc. Focus on **state transitions** and **calculations**. Use a format appropriate for each case; require a **code reference** for every rule to prevent hallucination.

**Related**: [07-anti-hallucination.md](07-anti-hallucination.md), [08-canonical-examples.md](08-canonical-examples.md)

---

## Where rules are captured

| Source | Examples |
|--------|----------|
| **Code** | Conditional logic, validation (e.g. `@Valid`, custom validators), state machine or status transitions, calculation methods. |
| **Comments** | Inline or block comments that describe business logic (e.g. “Business rule: interest is compounded monthly”). |
| **Javadoc** | Method or class Javadoc that states business rules (e.g. “@throws when balance would go negative”). |

Do **not** invent rules from general domain knowledge. If a rule is not stated in code, comments, or Javadoc, do not document it as a business rule; you may note “Possible implicit rule; not found in code” only if the human has asked for speculation, and label it clearly as not code-sourced.

---

## Source quality and how to cite

**Prefer and cite in this order**: (1) executable code (method, validator), (2) inline/block comments in code, (3) Javadoc.

When a rule exists only in comments or Javadoc, still require the exact location (file and line or method) and label it as: **“Documented in comment/Javadoc at …”**.

Every rule must have a **code reference**: file path, class name, method name or line range. No rule without a source.

---

## Format

Use the format that fits the content and keeps the doc scannable for both LLM and human (e.g. auditors, analysts):

| Format | Use when |
|--------|----------|
| **Lists** | Simple list of rules with a short id, description, and source (file, class, method or line). |
| **Tables** | Many rules: Rule ID \| Description \| Type (state transition / calculation / validation) \| Source (code reference). |
| **Mermaid** | Complex state transitions or decision trees: state or flowchart diagram; each transition or branch must be traceable to code (annotate with source in the doc). |

---

## Scope (what to prioritise)

1. **State transitions**: When can an entity move from state A to state B (e.g. order: DRAFT → SUBMITTED → PAID)? Document only transitions **implemented in code**; cite the class/method that enforces or performs the transition.
2. **Calculations**: Interest, fees, taxes, rounding, formulas. Document the formula or logic as in code and cite the method (e.g. `InterestCalculator.applyMonthlyCompound`).

You may also document **validation rules** (e.g. “amount must be positive”) and **authorization rules** (“only role X can do Y”) when they are explicit in code; for each, provide the code reference.

---

## Anti-hallucination for rules

- **Yes**: Require a **code reference** (file path, class name, method name or line range) for every documented rule. No rule without a source.
- **No**: Do not phrase rules as “the system might…” or “typically…” without a code anchor. Prefer “In `OrderService.submit()`, the order moves to SUBMITTED only if …” rather than “The system might submit the order.”
- If a rule exists only in comments or Javadoc (not in executable logic), still cite the comment location and label it as “Documented in comment/Javadoc at …”.
