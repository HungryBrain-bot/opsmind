# Dependency Injection

## Overview

OpsMind uses **Dependency Injection (DI)** to provide shared resources throughout the application without tightly coupling components together.

Instead of allowing classes and API endpoints to create their own dependencies, those dependencies are supplied by the framework.

This results in code that is easier to maintain, easier to test, and significantly more modular.

---

# What is Dependency Injection?

Dependency Injection is a software design pattern in which an object receives the resources it depends on from an external source rather than creating them itself.

Instead of this:

```python
class SearchService:

    def __init__(self):
        self.settings = Settings()
```

we inject the dependency:

```python
class SearchService:

    def __init__(self, settings: Settings):
        self.settings = settings
```

The service no longer needs to know **how** the settings are created.

It only knows that it requires them.

---

# Why is this Important?

Without dependency injection, every component becomes responsible for creating its own dependencies.

For example:

```
API
 │
 ├── creates Settings
 ├── creates Logger
 ├── creates Database
 └── creates LLM Client
```

This creates several problems:

- Tight coupling
- Difficult testing
- Duplicate initialization
- Inconsistent configuration

Dependency Injection removes these responsibilities.

---

# Dependency Injection in FastAPI

FastAPI includes a built-in dependency injection system based on the `Depends()` function.

Example:

```python
from fastapi import Depends

@router.get("/health")
def health(
    settings: Settings = Depends(get_settings),
):
    ...
```

FastAPI automatically executes the dependency function before calling the endpoint.

The returned object is then injected into the endpoint.

---

# Dependency Providers

Dependencies are supplied through small provider functions.

Example:

```python
def get_settings() -> Settings:
    return settings
```

The provider has a single responsibility:

Return the application's configuration.

The endpoint never needs to know where those settings came from.

---

# Request Flow

When a request reaches an endpoint, FastAPI performs dependency resolution automatically.

```
Incoming Request
        │
        ▼
Dependency Resolution
        │
        ▼
get_settings()
        │
        ▼
Settings Object
        │
        ▼
Health Endpoint
```

The endpoint receives a fully initialized object.

---

# Current Dependencies

At the current stage of OpsMind, dependency injection is used for:

- Application Settings

Future dependencies will include:

- Ollama Client
- Embedding Model
- Vector Database
- Graph Database
- Search Service
- Graph Service
- Ingestion Pipeline
- Authentication Service

Each dependency will have its own provider function.

---

# Why Not Use Global Variables?

A common beginner approach is:

```python
settings = Settings()

logger = Logger()

database = Database()
```

While this works initially, it introduces several issues.

## Hidden Dependencies

The component silently relies on global state.

This makes it difficult to understand what the component actually requires.

---

## Difficult Testing

Suppose a test needs different settings.

Without dependency injection:

```python
settings.app_env = "testing"
```

Every test now modifies shared global state.

Tests become unreliable.

---

## Poor Flexibility

Replacing a dependency becomes difficult.

Example:

Production:

```
Ollama Client
```

Testing:

```
Mock LLM
```

Dependency Injection allows this replacement without changing application code.

---

# Benefits

Using dependency injection provides several advantages.

## Loose Coupling

Components only depend on interfaces or objects they receive.

They do not construct their own dependencies.

---

## Better Testability

Tests can inject fake or mock objects.

Example:

```python
fake_settings = TestSettings()

service = SearchService(fake_settings)
```

No production configuration is required.

---

## Reusability

Components become reusable because they no longer rely on global application state.

---

## Maintainability

Changing how a dependency is created only affects the provider function.

Consumers remain unchanged.

---

# Dependency Graph

The dependency relationships inside OpsMind currently look like this.

```
                Settings
                    │
                    ▼
            get_settings()
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
Health Endpoint          Future Services
```

As the project grows, additional providers will extend this graph.

---

# Future Dependency Providers

OpsMind will eventually expose providers similar to:

```python
get_settings()

get_logger()

get_vector_store()

get_graph_store()

get_embedding_model()

get_llm_client()

get_search_service()

get_graph_service()

get_ingestion_pipeline()
```

Each provider has a single responsibility.

---

# Dependency Lifetime

Different resources require different lifetimes.

Some dependencies should exist once for the entire application.

Examples:

- Settings
- Logger
- Embedding Model

Others may exist per request.

Examples:

- Authentication Context
- Request Metadata
- User Session

FastAPI's dependency system supports these different lifetimes naturally.

---

# Design Principles

Dependency Injection supports several engineering principles used throughout OpsMind.

- Separation of Concerns
- Dependency Inversion Principle
- Single Responsibility Principle
- Testability
- Explicit Dependencies
- Loose Coupling

These principles make the codebase easier to extend while minimizing unintended interactions between components.

---

# Future Evolution

As OpsMind evolves into a GraphRAG platform, dependency injection will become even more important.

Future components—including vector databases, graph databases, LLM providers, embedding models, observability services, and LangGraph workflows—will all be injected through dedicated providers.

This ensures that individual components remain independent, replaceable, and easy to test while allowing the application infrastructure to evolve without affecting business logic.
