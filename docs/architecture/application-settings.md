# Application Settings

## Overview

Every production application requires configuration.

Examples include:

- Application name
- Environment (Development, Testing, Production)
- Database connection strings
- API ports
- Logging configuration
- LLM endpoints
- API keys
- Feature flags

Rather than hardcoding these values throughout the codebase, OpsMind centralizes all configuration using **Pydantic Settings**.

This provides a single, strongly typed source of truth for application configuration.

---

# Why Centralize Configuration?

Imagine a project where configuration values are scattered throughout the code.

```
api.py
PORT = 8000

logging.py
LOG_LEVEL = "INFO"

llm.py
OLLAMA_HOST = "http://localhost:11434"

database.py
DB_URL = "..."
```

This creates several problems:

- Difficult to change
- Duplicate values
- Inconsistent environments
- Poor maintainability

Instead, OpsMind stores all configuration in one place.

```
Settings
      │
      ├── API
      ├── Logging
      ├── Directories
      ├── LLM
      └── Future Components
```

---

# The Settings Class

OpsMind defines a single configuration model.

```python
class Settings(BaseSettings):
```

Unlike a normal Python class, `BaseSettings` automatically loads values from environment variables and `.env` files.

This removes the need for manually reading configuration files.

---

# Environment Variables

Pydantic automatically maps environment variables into Python attributes.

Example:

```
APP_NAME=OpsMind
APP_VERSION=0.1.0
API_PORT=8000
```

becomes

```python
settings.app_name
settings.app_version
settings.api_port
```

No parsing logic is required.

---

# Configuration Validation

One of the biggest advantages of Pydantic Settings is automatic validation.

Consider:

```
API_PORT=abc
```

Since `api_port` is defined as an integer,

```python
api_port: int
```

the application immediately raises an error during startup.

Instead of failing later at runtime, configuration issues are detected as early as possible.

---

# Type Safety

Every configuration value has an explicit type.

Example:

```python
api_port: int

log_level: str

enable_console_logging: bool

data_dir: Path
```

This prevents accidental misuse and improves IDE support.

---

# Configuration Groups

To improve readability, settings are organized into logical sections.

Example:

```
Application
API
LLM
Logging
Directories
```

This organization makes the configuration file easier to navigate as the project grows.

---

# Directory Configuration

OpsMind stores important filesystem locations as configuration values.

Example:

```python
data_dir: Path

logs_dir: Path

models_dir: Path
```

Using `Path` objects provides several benefits:

- Cross-platform compatibility
- Cleaner file operations
- Better readability
- Reduced string manipulation

Example:

```python
settings.data_dir / "processed"
```

instead of

```python
"data/processed"
```

---

# Logging Configuration

Logging behavior is fully configurable.

Current options include:

```python
log_level

log_format

enable_console_logging

enable_file_logging

log_file
```

Changing logging behavior requires only updating configuration rather than modifying application code.

---

# Environment Awareness

Applications often behave differently depending on where they are running.

Examples:

Development

```
Debug Logging
```

Production

```
Warning Logging
```

Testing

```
Temporary Directories
```

The `app_env` setting allows the application to adjust its behavior based on the active environment.

---

# The .env File

During development, configuration is typically stored inside a `.env` file.

Example:

```
APP_NAME=OpsMind

APP_VERSION=0.1.0

APP_ENV=development

API_HOST=0.0.0.0

API_PORT=8000
```

The `.env` file is loaded automatically by Pydantic.

---

# Why Not Commit .env?

Environment files often contain sensitive information.

Examples:

- API Keys
- Database Passwords
- Cloud Credentials
- Authentication Tokens

These values should never be committed to version control.

Instead, projects usually include:

```
.env.example
```

which documents the required configuration without exposing secrets.

---

# Dependency Injection

The Settings object is injected into application components rather than created repeatedly.

Example:

```python
@router.get("/health")
def health(
    settings: Settings = Depends(get_settings),
):
```

This provides:

- Consistency
- Testability
- Loose coupling

---

# Startup Flow

Configuration is loaded once during application startup.

```
.env
      │
      ▼
Pydantic Settings
      │
      ▼
Settings Object
      │
      ▼
Dependency Injection
      │
      ▼
Entire Application
```

Every component receives the same validated configuration.

---

# Benefits

Using centralized settings provides several advantages.

## Single Source of Truth

Configuration exists in one location.

---

## Type Safety

Incorrect values are detected immediately.

---

## Validation

Startup fails fast if configuration is invalid.

---

## Environment Flexibility

Development, testing, and production environments can each provide their own configuration without changing the application code.

---

## Better Developer Experience

Strong typing provides:

- IDE autocompletion
- Static analysis
- Improved readability

---

# Future Configuration

As OpsMind grows, additional configuration sections will be added.

Examples include:

## Embeddings

```
embedding_model

embedding_dimension
```

---

## Vector Database

```
vector_provider

collection_name

index_name
```

---

## Graph Database

```
neo4j_uri

neo4j_username

neo4j_password
```

---

## LLM

```
ollama_host

model_name

temperature

max_tokens
```

---

## Observability

```
metrics_enabled

tracing_enabled

prometheus_port
```

---

## Security

```
jwt_secret

api_key

cors_origins
```

---

# Design Principles

The Settings module follows several core engineering principles:

- Single Source of Truth
- Explicit Configuration
- Type Safety
- Fail Fast
- Environment Independence
- Dependency Injection
- Production Readiness

These principles ensure that configuration remains reliable, maintainable, and scalable as OpsMind evolves from a local development project into a production-grade AI platform.

---

# Future Evolution

Today, the Settings class primarily manages application metadata, logging, directories, and the Ollama endpoint.

As OpsMind evolves into a full GraphRAG platform, it will become the central configuration hub for every infrastructure component, including embedding models, vector databases, graph databases, observability services, authentication, and deployment settings.

By centralizing configuration from the beginning, OpsMind avoids scattered constants and creates a consistent foundation for future growth.
