# Application Factory

## Overview

OpsMind uses the **Application Factory** pattern to create and configure the FastAPI application.

Rather than constructing the application directly inside `main.py`, the application is created by a dedicated factory function.

```python
app = create_app(settings)
```

This approach separates application creation from application execution, making the system easier to configure, test, and extend.

---

# Why Use an Application Factory?

Small applications often instantiate the web framework directly:

```python
app = FastAPI()
```

While this works for simple projects, it becomes difficult to manage as the application grows.

Large applications usually need to configure:

- Logging
- Dependency Injection
- Middleware
- Routers
- Startup Tasks
- Shutdown Tasks
- Authentication
- Monitoring
- Metrics
- Feature Flags

If everything is initialized inside `main.py`, that file quickly becomes difficult to maintain.

The Application Factory solves this problem by centralizing initialization.

---

# Factory Function

In OpsMind the factory is implemented as:

```python
def create_app(settings: Settings) -> FastAPI:
```

Instead of relying on global state, the factory receives a validated `Settings` object and uses it to configure the application.

The function then returns a fully initialized FastAPI instance.

---

# Startup Flow

Application startup follows this sequence:

```
main.py
      │
      ▼
create_app(settings)
      │
      ├── Configure logging
      │
      ├── Create FastAPI application
      │
      ├── Register lifespan manager
      │
      ├── Store application settings
      │
      ├── Register API routers
      │
      ▼
Application Ready
```

Each initialization step has a dedicated responsibility.

---

# Responsibilities

The Application Factory is responsible for:

- Creating the FastAPI application
- Configuring centralized logging
- Registering lifecycle events
- Registering API routers
- Storing shared application state
- Preparing the application for execution

It intentionally avoids implementing business logic.

---

# Logging Configuration

One of the first startup steps is configuring the logging system.

```python
configure_logging(settings)
```

Logging must be available before the application begins processing requests.

This ensures that startup failures and initialization events are captured.

---

# Application Metadata

The factory configures application metadata:

```python
FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)
```

This information appears automatically in:

- OpenAPI documentation
- Swagger UI
- API metadata

Keeping metadata inside the configuration system ensures consistency across environments.

---

# Lifespan Registration

The factory connects the application's lifecycle manager.

```python
lifespan=lifespan
```

The lifespan manager handles:

- Startup initialization
- Resource preparation
- Shutdown cleanup

Separating lifecycle management keeps startup logic independent of application creation.

---

# Application State

OpsMind stores shared objects inside the FastAPI application state.

Example:

```python
app.state.settings = settings
```

This makes configuration available throughout the application without relying on global variables.

Future shared resources may include:

- Database clients
- Vector databases
- Graph databases
- LLM clients
- Embedding models

---

# Router Registration

The factory registers all API endpoints.

```python
app.include_router(api_router)
```

Each router remains independent and focuses on a single feature.

Examples:

- Health API
- Search API
- Ingestion API
- Administration API

Central registration provides a clear overview of all exposed endpoints.

---

# Why Not Put Everything in main.py?

Using `main.py` for all initialization introduces several problems:

- Difficult to test
- Tight coupling
- Poor organization
- Harder to extend
- Difficult to reuse

The Application Factory isolates initialization from execution, resulting in cleaner and more maintainable code.

---

# Benefits

Using an Application Factory provides several advantages:

## Testability

Tests can create isolated application instances with different configurations.

Example:

```python
app = create_app(test_settings)
```

This avoids modifying global state during testing.

---

## Environment Flexibility

Different environments can initialize the application with different settings.

Examples:

- Development
- Testing
- Staging
- Production

No application code needs to change.

---

## Extensibility

New infrastructure can be added without changing the application's entry point.

Future examples include:

- Authentication middleware
- Rate limiting
- Prometheus metrics
- OpenTelemetry tracing
- CORS configuration

Each feature becomes another initialization step inside the factory.

---

# Relationship with Other Components

The Application Factory acts as the central coordinator during startup.

```
                 create_app()
                      │
      ┌───────────────┼───────────────┐
      │               │               │
      ▼               ▼               ▼
 Logging        Lifespan        API Routers
      │               │               │
      ▼               ▼               ▼
 Ready         Initialize      Endpoints
```

After initialization is complete, the application begins accepting requests.

---

# Design Principles

The Application Factory reflects several software engineering principles:

- Separation of Concerns
- Dependency Injection
- Single Responsibility Principle
- Explicit Configuration
- Testability
- Modularity

These principles make OpsMind easier to understand, maintain, and evolve over time.

---

# Future Evolution

As OpsMind grows, additional initialization steps will be added to the factory, including:

- Database connections
- Vector store initialization
- Graph database clients
- Ollama client
- LangGraph runtime
- Background task scheduler
- Observability integrations
- Plugin loading

The factory provides a single, predictable location for configuring application-wide infrastructure while keeping business logic separate.
