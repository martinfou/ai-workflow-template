# Integrations Documentation

**Purpose**: Document all **outbound** integrations — REST, SOAP, and message queues — and provide integration architecture diagrams. Optionally document **inbound** integration points (webhooks, callbacks) when the project exposes them. Code and configuration are the source of truth.

**Related**: [06-diagrams-mermaid.md](06-diagrams-mermaid.md), [07-anti-hallucination.md](07-anti-hallucination.md), [08-canonical-examples.md](08-canonical-examples.md)

---

## Discovery

| Where to look | What to find |
|---------------|--------------|
| **REST** | `RestTemplate`, `WebClient`, or HTTP client beans; config for base URL, auth; service classes that perform outbound HTTP calls. |
| **SOAP** | `WebServiceTemplate`, WSDL definitions, client beans; config for WSDL URL and security. |
| **Messaging** | `@JmsListener`, `@KafkaListener`, Kafka/RabbitMQ producers; config for broker URL, queue/topic names, consumer groups. |
| **Inbound** | Webhook controllers, callback endpoints; document only what is implemented in the repo. |

Trace from the class that performs the call or handles the message; cite class and method for every documented operation.

---

## REST outbound

For each REST **client** (outbound call from this application), document only what is in code or config:

| Element | Source | Rule |
|---------|--------|------|
| **URL / base URL** | Config, `RestTemplate`/`WebClient` bean, or constant | Base URL and any path prefix. |
| **Authentication** | Code and config | Type (API key, OAuth, basic, etc.) and where it is set (e.g. header name, config key). Do not assume auth. |
| **Operations** | Code | List of operations: HTTP method + path (or description) and purpose (e.g. “GET /accounts — fetch account by ID”). |
| **Retries** | Code/config | Retry count, backoff, conditions (e.g. on 5xx only) when present. |
| **Timeouts** | Code/config | Connect and read timeouts when set. |

If the code implements **idempotency** (e.g. idempotency key header, retry with same key), document it and cite where it is set; do not assume idempotency without code evidence.

---

## SOAP

For each SOAP integration:

| Element | Source | Rule |
|---------|--------|------|
| **WSDL** | Config or code | WSDL URL or path (e.g. from `WsdlDefinition`, config property). |
| **Operations** | Code / WSDL | Key operations (name, purpose). |
| **Request/response types** | Code / WSDL | Main request and response types or elements when used in code. |
| **Security** | Code/config | WS-Security, certificates, or other security when present. |

Do not invent operations or types not present in WSDL or in the code that uses the client.

---

## Message queues

For each queue or topic (JMS, Kafka, RabbitMQ, etc.):

| Element | Source | Rule |
|---------|--------|------|
| **Queues / topics** | Config, listener annotations, producer code | Names and purpose (consume vs produce). |
| **Message format** | Code | DTO class, or schema reference (e.g. JSON schema), or “see class X”. |
| **Consumer group / subscription** | Config/code | Consumer group (Kafka), subscription (e.g. Rabbit), or equivalent. |
| **Delivery semantics** | Code/config | At-least-once, at-most-once, exactly-once when documented or configured (e.g. Kafka `enable.idempotence`). |

Document both consumers and producers; cite listener methods and producer send calls.

---

## Integration diagrams

| Diagram | Content | Location |
|---------|---------|----------|
| **Overview** | One Mermaid diagram (graph or flowchart) showing this application and all external systems (REST APIs, SOAP services, queues/topics) with direction of calls (inbound/outbound). | `docs/integrations/overview.md` |
| **Per-integration** | Optional sequence diagram per integration (e.g. “When we call Payment API”) showing this app and the external system for a representative operation. Use when it clarifies the flow. | Same file or dedicated file per integration |

Follow [06-diagrams-mermaid.md](06-diagrams-mermaid.md) for style.
