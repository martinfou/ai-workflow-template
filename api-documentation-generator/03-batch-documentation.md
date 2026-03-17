# Batch Documentation

**Purpose**: Define how to discover, document, and diagram every Spring Batch job and its steps. Use industry best practice for discovery and structure.

**Related**: [01-project-detection.md](01-project-detection.md), [06-diagrams-mermaid.md](06-diagrams-mermaid.md), [07-anti-hallucination.md](07-anti-hallucination.md), [08-canonical-examples.md](08-canonical-examples.md)

---

## Discovery

Use **code and configuration** as the source of truth.

| Source | What to do |
|--------|------------|
| **Configuration classes** | Scan for `@Configuration` classes that define a `Job` (e.g. via `JobBuilderFactory`, `JobBuilder`). Collect job names from `JobBuilder.get(...)` or equivalent. |
| **Launchers** | Check `JobLauncher` usages, `@Scheduled` methods, or REST endpoints that start jobs by name — so no job is missed. |
| **Build and config** | Gradle/Maven: confirm `spring-boot-starter-batch` (or `spring-batch-*`). `application*.yml` / `application*.properties`: job names, batch schema, datasources, and any job-specific config. |

**Discovery checklist**: List every `Job` bean and every entry point that launches a job by name. Prefer **inclusion**: document every job; in the critique phase, confirm there are no orphan or duplicate entries.

---

## Per-job: what must be documented

For **every** job, document only what exists in code or config:

| Element | Source | Rule |
|---------|--------|------|
| **Job name** | Job definition | Exact name as in code. |
| **Steps** | Job flow | Ordered list of step names; document flow and any conditional branching. |
| **Chunk size** | Step config | Chunk size (read/process/write) when defined. |
| **Reader** | Step config | Type (e.g. JdbcCursorItemReader, JpaPagingItemReader); source (table, file, queue). |
| **Writer** | Step config | Type; target (table, file, queue). |
| **Processor** | Step config | Type and high-level behaviour (from code); optional transformation or filtering. |
| **Key tables/files** | Reader/Writer config | Input and output tables, file paths, or queue names. |
| **Retry / skip / rollback** | Step config | Retry policy, skip limit, skip conditions, rollback behaviour when present in code. |
| **Scheduling** | Config or launcher | Cron, trigger, or “on-demand” (e.g. REST or manual); only if present in code/config. |
| **Listeners** | Step/Job config | If present: JobExecutionListener, StepExecutionListener, ChunkListener — document callback points and purpose from code. |
| **Partitioning** | Step config | If partition step (PartitionHandler, StepExecutionSplitter), document partition strategy and grid size from code. |

---

## Job-flow diagrams (one per job)

- **One job-flow diagram per job**: Mermaid flowchart showing Step 1 → Step 2 → … including decisions and branching. Each node = one step or decision as in code.
- **Decision steps**: If the job uses `JobExecutionDecider` or conditional flow (e.g. `next().on("FAILED").to(...)`), draw the decision and all branches explicitly. Do not infer branches not present in code.
- **Shared steps**: If a step is reused across jobs, document it once (e.g. in `docs/batch/steps/`) and reference it from each job doc; in the job-flow diagram, show the step by name with a note “(shared)” if helpful.

---

## Per-step sequence and data-flow diagrams

| When | What |
|------|------|
| **Non-trivial step** | One sequence and/or data-flow per step when the step has reader → processor → writer with multiple participants or external calls. |
| **Very simple step** | Short prose may suffice; the doc guide may still require a minimal sequence or data-flow for consistency (see 08 canonical examples). |

| Diagram type | Content |
|--------------|---------|
| **Sequence** | Reader → Processor → Writer; include external systems (DB, queue, file system) as participants when present in code. |
| **Data-flow** | Mermaid flowchart: data source (table/file/queue) → reader → processor → writer → target. Use when it clarifies where data comes from and goes. |

Place per-step diagrams in the job doc (under a “Steps” section) or in `docs/batch/steps/<step-name>.md` if steps are shared or long.
