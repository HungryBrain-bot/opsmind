# Application Lifecycle

## Overview

Every application has a lifecycle.

It starts, performs useful work, and eventually shuts down.

During these phases, the application often needs to prepare resources before serving requests and clean them up before exiting.

OpsMind manages these responsibilities using FastAPI's **Lifespan** mechanism.

This provides a centralized location for startup and shutdown tasks, ensuring that the application enters and exits a well-defined state.

---

# What is an Application Lifecycle?

An application's lifecycle consists of two primary phases:

```
Application Start
        │
        ▼
Initialization
        │
        ▼
Serve Requests
        │
        ▼
Shutdown
```

Each phase has different responsibilities.

Startup prepares the application.

Shutdown releases resources safely.

---

# Why Do We Need a Lifecycle?

A simple application might only create a FastAPI instance and immediately begin accepting requests.

As systems grow, additional initialization becomes necessary.

Examples include:

- Creating directories
- Connecting to databases
- Loading machine learning models
- Initializing vector databases
- Connecting to graph databases
- Registering background workers
- Verifying external services

Without a lifecycle manager, this logic becomes scattered throughout the application.

OpsMind keeps all startup and shutdown logic in one place.

---

# Lifespan in FastAPI

FastAPI provides a built-in lifecycle mechanism through the `lifespan` parameter.

```python
FastAPI(
    lifespan=lifespan,
)
```

The lifespan function is executed automatically by FastAPI.

Developers do not need to call it manually.

---

# Startup Flow

During startup, the following sequence occurs.

```
Load Configuration
        │
        ▼
Configure Logging
        │
        ▼
Create FastAPI Application
        │
        ▼
Run Lifespan Startup
        │
        ▼
Application Ready
```

Only after startup completes does FastAPI begin accepting requests.

---

# Shutdown Flow

When the application stops, FastAPI executes the shutdown portion of the lifespan.

```
Stop Accepting Requests
        │
        ▼
Run Shutdown Tasks
        │
        ▼
Release Resources
        │
        ▼
Application Exit
```

This ensures that resources are cleaned up properly.

---

# Current Responsibilities

At the current stage of OpsMind, the lifecycle performs two main tasks.

## Directory Initialization

Required application directories are created automatically.

Examples include:

```
data/

logs/

models/

data/raw/

data/processed/

data/embeddings/
```

This guarantees that required folders exist before any processing begins.

---

## Startup Logging

The lifecycle records application startup information.

Example:

```
Application Started

Version: 0.1.0

Environment: Development
```

This provides visibility into each application launch.

---

## Shutdown Logging

When the application exits, a shutdown event is logged.

Example:

```
Application Stopped
```

Although simple today, this provides the foundation for more advanced shutdown procedures.

---

# Why Separate Startup from the Factory?

The Application Factory creates the FastAPI application.

The Lifecycle prepares the runtime environment.

These are different responsibilities.

```
Application Factory
        │
Creates Application
```

```
Lifecycle
        │
Prepares Application
```

Separating them keeps each component focused on a single purpose.

---

# Lifecycle Responsibilities

The lifecycle should manage infrastructure.

Examples include:

- Creating directories
- Opening database connections
- Loading models
- Starting schedulers
- Registering background tasks
- Validating external services
- Initializing caches

It should **not** contain business logic.

For example, processing documents or answering user queries does not belong in the lifecycle.

---

# Current Lifecycle Architecture

```
Application Startup
        │
        ▼
Lifespan
        │
        ├──────── Create Directories
        │
        ├──────── Log Startup
        │
        ▼
Application Ready
```

During shutdown:

```
Application Shutdown
        │
        ▼
Lifespan
        │
        └──────── Log Shutdown
```

---

# Why Create Directories Automatically?

Rather than expecting users to manually create folders, OpsMind prepares its required filesystem structure automatically.

Benefits include:

- Easier installation
- Fewer runtime errors
- Consistent project layout
- Better developer experience

If a required directory already exists, no changes are made.

---

# Relationship with Settings

The lifecycle does not hardcode filesystem paths.

Instead, it retrieves them from the application's configuration.

Example:

```python
settings.data_dir

settings.logs_dir

settings.models_dir
```

This allows directory locations to be changed without modifying lifecycle code.

---

# Relationship with Logging

Logging is configured before the lifecycle begins.

This allows startup events to be recorded immediately.

```
Settings
      │
      ▼
Logging
      │
      ▼
Lifecycle
      │
      ▼
Application Ready
```

If startup fails, the failure is still captured in the logs.

---

# Future Responsibilities

As OpsMind evolves, the lifecycle will initialize additional infrastructure.

Examples include:

## LLM Initialization

```
Connect to Ollama

Verify Model Availability
```

---

## Vector Database

```
Create Collection

Verify Index
```

---

## Graph Database

```
Connect to Neo4j

Verify Schema
```

---

## Background Services

```
Task Scheduler

Queue Workers

Health Monitors
```

---

## Observability

```
OpenTelemetry

Metrics Exporter

Tracing
```

---

## AI Components

```
Load Embedding Model

Initialize LangGraph

Register Agents
```

---

# Error Handling

If a critical startup task fails, the application should fail immediately.

For example:

```
Unable to connect to Vector Database
```

The application should not continue running in a partially initialized state.

This follows the **Fail Fast** principle.

---

# Benefits

Using a dedicated lifecycle provides several advantages.

## Centralized Initialization

All startup tasks are located in one place.

---

## Predictable Startup

Resources are prepared before requests are accepted.

---

## Safe Shutdown

Resources are released cleanly.

---

## Better Maintainability

Infrastructure concerns remain separate from business logic.

---

## Easier Testing

Startup tasks can be tested independently from request handling.

---

# Design Principles

The lifecycle implementation reflects several engineering principles:

- Separation of Concerns
- Single Responsibility Principle
- Explicit Initialization
- Fail Fast
- Production Readiness
- Infrastructure Isolation

These principles help ensure that OpsMind starts and stops in a predictable, maintainable, and reliable manner.

---

# Future Evolution

Today, the lifecycle primarily creates directories and records startup and shutdown events.

As OpsMind grows into a production-grade AI platform, the lifecycle will become responsible for initializing every major infrastructure component, including embedding models, vector databases, graph databases, LangGraph workflows, background services, and observability tools.

By establishing a dedicated lifecycle early, OpsMind creates a scalable foundation for managing increasingly complex application infrastructure while keeping startup behavior organized and predictable.
