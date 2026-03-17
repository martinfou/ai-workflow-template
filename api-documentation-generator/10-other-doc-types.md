# Other Document Types

**Purpose**: Cover documentation for **deployment**, **environment variables**, **configuration properties**, and **database schema**. Code and configuration remain the source of truth.

**Related**: [07-anti-hallucination.md](07-anti-hallucination.md)

---

## Deployment

**Purpose**: How to build, run, and deploy the application — only what exists in the repo or referenced deployment config.

| Topic | Source | Rule |
|-------|--------|------|
| **Build and run** | README, Dockerfile, CI config | How to build (Gradle/Maven command) and run (e.g. `java -jar`, `spring-boot:run`, or container command). Cite the file. |
| **Deployment targets** | Scripts or CI/CD (e.g. GitHub Actions, Jenkins) | List environments and targets defined in config; do not assume environments not present. |
| **Prerequisites** | Code or config | Runtime (e.g. JVM version), database or message broker requirements as stated in code or config. |
| **Artifacts** | Build or config | What is produced (e.g. JAR name, image name) when defined in code/config. |

Do not invent deployment steps or environments not present in the project.

---

## Environment variables

| Topic | Source | Rule |
|-------|--------|------|
| **Discovery** | `application.properties`, `application.yml`, `@Value`, and any `Environment` or config property usage. Optional: deployment config (e.g. Kubernetes manifests, Docker Compose) if in repo. | — |
| **Format** | — | Table: Variable name \| Required/Optional \| Description (from code or comment) \| Default (if any in code/config). |
| **Scope** | — | Document only variables that appear in the codebase or in config files in the repo. Do not add “typical” or “standard” variables (e.g. “JAVA_HOME”) unless the project explicitly references them. |

Place in `docs/deployment.md` (or a dedicated `docs/environment-variables.md`) under a clear “Environment variables” section.

---

## Configuration properties (Spring Boot)

| Topic | Source | Rule |
|-------|--------|------|
| **Discovery** | `@ConfigurationProperties` classes and their usage. | — |
| **Content** | — | Document the prefix, main properties (name, type, description from field or comment), and default values when set in code. |
| **Scope** | — | Only properties that appear in the codebase; no invented properties. Optionally merge with environment variables in one table if the same keys are used. |

---

## Database schema

| Topic | Source | Rule |
|-------|--------|------|
| **Source** | Prefer code. Use JPA entities, Flyway/Liquibase migrations, or other schema-defining artifacts in the repo. | If the project has no schema in repo (e.g. DB maintained elsewhere), state that and do not invent a schema. |
| **Content** | — | For each entity or table: name, main columns (name, type, nullable), and key relationships (e.g. FK). Optionally a Mermaid ER diagram derived from entities/migrations. When using Flyway/Liquibase, note schema or migration version (e.g. V1__create_accounts.sql) for traceability. |
| **Scope** | — | Do not invent tables or columns. If only a subset of columns is used in code, you may document only those and note “Other columns may exist in DB; not referenced in code.” |

Place in `docs/deployment.md` under “Database schema” or in a separate `docs/database-schema.md` if the schema is large.
