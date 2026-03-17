# API / Batch Documentation Generator

This folder contains the **instruction set** for generating and maintaining documentation for Spring Boot and Spring Batch projects — for both **LLMs** and **humans** — plus (when present) a **questionnaire** to capture requirements.

---

## Where to start

| You are… | Start here |
|----------|------------|
| **LLM** | [INDEX.md](INDEX.md) → [00-how-to-use-this-guide.md](00-how-to-use-this-guide.md). Use the numbered guides in order; generate under `/docs`. |
| **Human** | [INDEX.md](INDEX.md). Use [08-canonical-examples.md](08-canonical-examples.md) for “what good looks like” and [09-critique-and-consistency.md](09-critique-and-consistency.md) to review. |

The **canonical** instruction set may also live in **`../docs/`**. If so, [../docs/INDEX.md](../docs/INDEX.md) is the same index; prefer the version your workflow uses (this folder or `../docs/`).

---

## Contents of this folder

| Item | Description |
|------|-------------|
| [INDEX.md](INDEX.md) | Index, scope, principles, document map, quick start. |
| 00-how-to-use-this-guide.md … 10-other-doc-types.md | Instruction guides (use in order 00 → 10 as needed). |
| questionnaire.html | *(If present)* Static HTML questionnaire; use “Generate copy-paste block” to paste answers into chat. |

---

## Where generated docs go

All **generated** documentation (API, batch, business rules, integrations, deployment) is written under **`/docs`** (repo root), using the structure in [00-how-to-use-this-guide.md](00-how-to-use-this-guide.md#output-structure-best-practice). This folder holds only the **instructions**; it does not hold the generated output.

---

## Version

Instruction set version: **1.0**. See [INDEX.md](INDEX.md) for last updated date.
