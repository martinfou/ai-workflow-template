# REST API Documentation

**Purpose**: Define how to discover, document, and diagram every REST endpoint in a Spring Boot project. Documentation must trace controller → service → database → mapper and explain behaviour in **business terms**.

**Related**: [01-project-detection.md](01-project-detection.md), [06-diagrams-mermaid.md](06-diagrams-mermaid.md), [07-anti-hallucination.md](07-anti-hallucination.md), [08-canonical-examples.md](08-canonical-examples.md)

**Context**: Financial institution in Canada. Use industry best practice for grouping and structure.

---

## Discovery

Infer endpoints from **code and configuration**; use OpenAPI/Swagger when present.

| Source | What to do |
|--------|------------|
| **Code** | Scan for `@RestController`, `@Controller`, and WebFlux equivalents. Extract path, HTTP method, and handler from `@RequestMapping`, `@GetMapping`, `@PostMapping`, etc. Resolve base paths from class-level `@RequestMapping` and `application.properties`/`application.yml` context path. |
| **Build** | Gradle: `build.gradle` / `build.gradle.kts`. Maven: `pom.xml`. Note Spring Boot and web starter versions. |
| **OpenAPI / Swagger** | If present (e.g. `springdoc-openapi`, `springfox`), use as **additional input** for paths, methods, and DTOs. Reconcile with code: **code remains source of truth**; document any discrepancy (e.g. “OpenAPI lists X but implementation does Y”) in the doc or critique report. |

**Discovery checklist**: For each controller class, list every mapped method; combine class-level and method-level paths; include context path from config. Ensure no endpoint is missed and none is invented.

---

## Status codes and security (code only)

| Topic | Rule |
|-------|------|
| **Status codes** | Derive from controller return types and **exception handlers** only. Scan `@ExceptionHandler`, `@ControllerAdvice`, `@RestControllerAdvice`; document every status code returned in handler methods (e.g. `ResponseEntity.status(400)`, `@ResponseStatus(INTERNAL_SERVER_ERROR)`). Do **not** add status codes that only appear in OpenAPI or in comments. |
| **Security** | Document authentication/authorization **only when present in code**. Look for: `SecurityFilterChain`, `@PreAuthorize`, `@Secured`, `@RolesAllowed`, method security, or auth-related filters/interceptors. Cite the class and method; do not assume “secured by default.” |

---

## Per-endpoint: what must be documented

For **every** endpoint, document the following. Only include what you can **derive from code or config**; do not invent.

| Element | Source | Rule |
|---------|--------|------|
| **Path** | Controller mapping | Full path (including context path if set). |
| **Method** | Annotation | GET, POST, PUT, PATCH, DELETE, etc. |
| **Request body** | Method params, DTOs | Type and main fields; required vs optional from `@Valid`, `@NotNull`, etc. |
| **Response body** | Return type, DTOs | Type and main fields; note wrapper (e.g. `ResponseEntity`, generic wrapper). |
| **Status codes** | Code only | Only status codes that appear in code (e.g. `ResponseEntity.status(HttpStatus.X)`). Do not guess “typical” codes. |
| **Parameters** | Method params | Query, path, header: name, type, required/optional, validation (from annotations). |
| **What it actually does** | Trace through code | Follow controller → service → repository/mapper → database (and back). Summarise in **business terms** (e.g. “Creates a new account and returns the account ID” rather than “calls AccountService.create”). |

**Trace rule**: For each endpoint, follow the call path from the controller method through service(s), repository/mapper, and database. Document this path and then write a short business-facing summary. Reference source (e.g. `AccountController.createAccount`, `AccountService.create`, `AccountRepository.save`).

---

## Grouping

Use **industry best practice** for a financial institution:

- Prefer **domain-oriented** grouping (e.g. Accounts, Payments, Reporting) when the codebase is organised by domain.
- Alternatively group **by controller** (e.g. “Account API”, “Payment API”) when that matches the code layout.
- If OpenAPI tags are present and consistent with code, you may use them for grouping; state that grouping follows OpenAPI tags.

In the output structure under `docs/api/`, use one overview plus either:

- **By domain**: `docs/api/endpoints/by-domain/<domain>.md` — one file per domain (e.g. `accounts.md`, `payments.md`); each file can contain multiple endpoints for that domain.
- **By controller**: `docs/api/endpoints/by-controller/<ControllerName>.md` — one file per controller; each file contains all endpoints of that controller.

Choose **one** strategy for the project and state it in `docs/api/overview.md`. Ensure every endpoint appears in **exactly one** place and is listed in the overview table.

---

## Diagrams (Mermaid only)

Produce three levels:

| Level | Content | Location |
|-------|---------|----------|
| **1. Overview** | One Mermaid diagram (flowchart or graph) showing all documented endpoints or endpoint groups (e.g. boxes per domain or per controller with main paths). | `docs/api/overview.md` |
| **2. Per-endpoint sequence** | For each endpoint, one Mermaid sequence diagram: caller → Controller → Service → Repository/Mapper → Database (and back). Only participants and calls that exist in code. | Endpoint’s doc (e.g. `docs/api/endpoints/.../<name>.md`) |
| **3. Per-endpoint flow** | For each endpoint, one Mermaid flowchart showing logical flow (decisions, loops, error paths) within the controller and service layer as derived from code. | Same as endpoint doc |

Follow [06-diagrams-mermaid.md](06-diagrams-mermaid.md) for style (e.g. quoting labels with special characters).
