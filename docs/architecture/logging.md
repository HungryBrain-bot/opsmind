# Centralized Logging

## Overview

Logging is one of the most important aspects of any production application.

Without logging, diagnosing failures becomes extremely difficult.

Questions such as:

- Why did the application crash?
- Which API received the request?
- Which document failed to load?
- Which embedding model was used?
- How long did retrieval take?
- Which LLM generated the response?

become almost impossible to answer.

For this reason, OpsMind treats logging as a first-class architectural component rather than an afterthought.

---

# Why Centralized Logging?

Imagine every module configuring its own logger.

```
api.py

logging.basicConfig(...)
```

```
search.py

logging.basicConfig(...)
```

```
ingestion.py

logging.basicConfig(...)
```

Every module now behaves differently.

Problems include:

- Different formats
- Different log levels
- Duplicate messages
- Difficult maintenance
- Inconsistent output

Instead, OpsMind configures logging exactly once during application startup.

```
Application Startup
        │
        ▼
configure_logging()
        │
        ▼
Root OpsMind Logger
        │
        ├──────── API
        ├──────── Ingestion
        ├──────── Retrieval
        ├──────── Graph
        ├──────── LLM
        └──────── Services
```

Every component uses the same logging configuration.

---

# Logging Architecture

OpsMind uses a dedicated logging module.

```
backend/app/core/logging.py
```

This module is responsible for:

- Logger configuration
- Formatter selection
- Console logging
- File logging
- JSON logging
- Logger creation

No other module configures logging.

---

# Logger Hierarchy

The application uses a root logger.

```
opsmind
```

Every module receives a child logger.

Example:

```
opsmind.api.health

opsmind.ingestion.text_loader

opsmind.retrieval.search

opsmind.graph.builder
```

This hierarchy makes it easy to determine where a log message originated.

---

# Logger Creation

Instead of creating loggers manually,

```python
logging.getLogger(__name__)
```

OpsMind uses a helper function.

```python
logger = get_logger(__name__)
```

This automatically places the logger inside the OpsMind namespace.

Example:

```
backend.app.api.health
```

becomes

```
opsmind.api.health
```

This keeps log names shorter and easier to read.

---

# Log Levels

Different log levels communicate different severities.

| Level | Purpose |
|--------|----------|
| DEBUG | Detailed debugging information |
| INFO | Normal application events |
| WARNING | Unexpected but recoverable situations |
| ERROR | Operation failed |
| CRITICAL | Application cannot continue |

Current development primarily uses:

```
INFO
```

As the platform grows, DEBUG logs will become increasingly valuable during troubleshooting.

---

# Text Logging

The default formatter produces human-readable output.

Example:

```
2026-06-20 10:31:54

INFO

opsmind.api.health

health.check.requested
```

This format is ideal during development.

---

# JSON Logging

OpsMind also supports structured JSON logging.

Example:

```json
{
    "timestamp": "...",
    "level": "INFO",
    "logger": "opsmind.api.health",
    "message": "health.check.requested",
    "module": "health",
    "function": "health",
    "line": 27
}
```

Structured logs are significantly easier for machines to process.

---

# Why JSON?

Monitoring systems prefer structured data.

Examples include:

- Splunk
- Microsoft Sentinel
- Elastic
- Grafana Loki
- Azure Monitor

Instead of parsing plain text,

```
INFO health.check.requested
```

they can directly index fields like

```
level

timestamp

module

function

line
```

This enables powerful filtering and dashboards.

---

# Console Logging

During development, logs are written directly to the terminal.

```
INFO application.started

INFO health.check.requested
```

This provides immediate feedback while coding.

---

# File Logging

For persistent storage, OpsMind supports log files.

Example:

```
logs/

opsmind.log
```

File logging allows investigation of previous application runs after the process has stopped.

---

# Rotating Log Files

Instead of allowing log files to grow indefinitely, OpsMind uses a rotating file handler.

```
5 MB
```

When the file reaches its size limit:

```
opsmind.log
```

becomes

```
opsmind.log.1
```

A new log file is then created automatically.

This prevents disk usage from growing without bound.

---

# Configurable Logging

Logging behavior is controlled entirely through application settings.

Current options include:

```
log_level

log_format

enable_console_logging

enable_file_logging

log_file
```

Changing logging behavior requires only configuration changes.

No application code needs modification.

---

# Duplicate Log Prevention

Development servers often reload automatically.

Without proper configuration, every reload creates duplicate handlers.

Example:

```
INFO Application Started

INFO Application Started
```

To prevent this,

```python
logger.handlers.clear()
```

removes existing handlers before configuring new ones.

---

# Propagation

OpsMind disables log propagation.

```python
logger.propagate = False
```

Without this setting, messages would also be forwarded to Python's root logger, producing duplicate output.

---

# Logging During Startup

Logging is configured before the application begins serving requests.

Startup sequence:

```
Load Settings
      │
      ▼
Configure Logging
      │
      ▼
Create FastAPI
      │
      ▼
Run Lifespan
      │
      ▼
Accept Requests
```

This ensures startup failures are also recorded.

---

# Logging Philosophy

OpsMind primarily logs events rather than implementation details.

Good example:

```
document.loaded

embedding.created

graph.generated

search.completed
```

Poor example:

```
Entering function

Variable x = 123

Loop iteration 4
```

Logs should describe **meaningful system events**, not every line of execution.

---

# Future Logging

As OpsMind evolves, logging will include:

## Performance

```
retrieval.duration

embedding.duration

llm.duration
```

---

## GraphRAG

```
entities.extracted

relationships.created

graph.nodes

graph.edges
```

---

## AI

```
prompt.sent

tokens.used

model.selected
```

---

## Observability

```
request.id

trace.id

correlation.id

session.id
```

---

## Security

```
authentication.failed

authorization.denied

api.rate_limit
```

---

# Relationship with Other Components

Logging is shared across the entire platform.

```
               Logging
                   │
    ┌──────────────┼──────────────┐
    │              │              │
    ▼              ▼              ▼
API          Ingestion      Retrieval
    │              │              │
    ▼              ▼              ▼
Graph          Services         LLM
```

Every component reports its activity through the centralized logging system.

---

# Design Principles

The logging system follows several engineering principles:

- Centralized Configuration
- Structured Logging
- Observability
- Consistency
- Separation of Concerns
- Configurability
- Production Readiness
- Fail Fast

These principles ensure that logs remain useful for developers during local development and scalable enough for enterprise monitoring systems.

---

# Future Evolution

Logging will eventually become part of a broader observability strategy.

Future integrations may include:

- OpenTelemetry
- Prometheus
- Grafana
- Azure Monitor
- Microsoft Sentinel
- Splunk
- Distributed tracing
- Correlation IDs
- Request metrics

By establishing a centralized logging architecture early, OpsMind creates a strong foundation for monitoring, troubleshooting, and operating production AI systems at scale.
