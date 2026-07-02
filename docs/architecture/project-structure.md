# Project Structure

## Overview

OpsMind follows a modular, feature-oriented project structure designed to support long-term maintainability, scalability, and extensibility.

Rather than organizing code around frameworks or technologies, the project is organized around responsibilities. Each package has a clearly defined purpose and communicates with other components through well-defined interfaces.

This approach minimizes coupling between modules while making the system easier to understand, test, and extend.

---

# Goals

The project structure is designed to achieve several engineering goals:

- Clear separation of responsibilities
- Modular architecture
- High testability
- Easy onboarding for new contributors
- Independent evolution of components
- Production-ready organization
- Support for future AI and GraphRAG capabilities

---

# Directory Layout

```
OpsMind/

backend/
    app/
        api/
        clients/
        chunking/
        config/
        core/
        graph/
        ingestion/
        llm/
        retrieval/
        schemas/
        services/

    tests/

data/
    raw/
    processed/
    embeddings/

docs/
    architecture/
    adr/
    guides/

logs/

models/

scripts/
```

---

# Root Directory

The repository root contains project-wide resources.

| Directory | Purpose |
|------------|----------|
| backend | Application source code |
| data | Documents and generated artifacts |
| docs | Project documentation |
| logs | Runtime log files |
| models | Downloaded AI models |
| scripts | Utility scripts |

Keeping these concerns separated prevents application logic from becoming mixed with generated data or operational resources.

---

# backend/

The `backend` directory contains the complete FastAPI application.

```
backend/
    app/
    tests/
```

Application code and automated tests are intentionally separated.

This keeps production code isolated from testing infrastructure while allowing tests to mirror the application's package structure.

---

# app/

The `app` package contains the application's implementation.

Each subpackage represents a specific responsibility.

```
app/
    api/
    clients/
    chunking/
    config/
    core/
    graph/
    ingestion/
    llm/
    retrieval/
    schemas/
    services/
```

---

# api/

Contains HTTP endpoints exposed by FastAPI.

Responsibilities include:

- Request validation
- Dependency injection
- Calling business logic
- Returning responses

API routes should remain thin and should not contain business logic.

---

# clients/

Contains integrations with external systems.

Examples include:

- Ollama
- OpenAI
- Azure OpenAI
- Neo4j
- Qdrant
- Chroma
- Elasticsearch

Keeping external integrations isolated makes them easy to replace or mock during testing.

---

# chunking/

Responsible for converting documents into smaller chunks suitable for embedding and retrieval.

Future implementations include:

- Fixed-size chunking
- Recursive chunking
- Semantic chunking
- Markdown-aware chunking
- Code-aware chunking

Chunking is intentionally separated from ingestion because different chunking strategies may be applied to the same document.

---

# config/

Contains application configuration.

Responsibilities include:

- Environment variables
- Configuration validation
- Global settings

Centralizing configuration ensures consistent behavior across the application.

---

# core/

Contains infrastructure shared throughout the application.

Examples include:

- Logging
- Lifecycle management
- Dependency injection
- Exception handling

The `core` package provides foundational services used by many other modules.

---

# graph/

Reserved for GraphRAG functionality.

Future responsibilities include:

- Entity extraction
- Relationship extraction
- Graph construction
- Graph traversal
- Knowledge graph updates

Keeping graph functionality isolated prevents unnecessary coupling with retrieval or ingestion.

---

# ingestion/

Responsible for loading documents into the system.

Examples include:

- Text loader
- Markdown loader
- PDF loader
- DOCX loader

The ingestion layer reads documents but does not perform chunking or embedding.

---

# llm/

Contains integrations with language models.

Future components include:

- Prompt builders
- Chat models
- Completion models
- Agent interfaces

Separating LLM functionality allows different providers to be supported without affecting the rest of the system.

---

# retrieval/

Responsible for retrieving relevant information during question answering.

Future capabilities include:

- Vector search
- Keyword search
- Hybrid retrieval
- Graph retrieval
- Ranking

Retrieval is independent of document ingestion, allowing indexing and querying to evolve separately.

---

# schemas/

Contains shared data models.

Examples include:

- Document
- Chunk
- GraphNode
- GraphEdge
- API responses

Using centralized schemas ensures consistent data representation across the application.

---

# services/

Contains business logic.

Unlike API routes, services implement the application's behavior.

Future examples include:

- SearchService
- IngestionService
- GraphService
- EmbeddingService

Keeping business logic here improves testability and prevents duplication across API endpoints.

---

# tests/

Contains automated tests.

Tests mirror the application structure whenever possible.

Example:

```
app/
    ingestion/
        text_loader.py

tests/
    test_text_loader.py
```

This convention makes related implementation and tests easy to locate.

---

# data/

Stores runtime data generated by the application.

```
data/
    raw/
    processed/
    embeddings/
```

### raw/

Original documents before processing.

### processed/

Normalized or cleaned versions of documents.

### embeddings/

Serialized embeddings and related vector artifacts.

Separating these stages allows processing pipelines to be resumed or repeated without losing the original input.

---

# docs/

Contains project documentation.

Documentation evolves alongside the implementation and includes:

- Architecture guides
- ADRs
- Development guides

Treating documentation as part of the codebase improves maintainability and onboarding.

---

# logs/

Stores runtime log files when file logging is enabled.

Keeping logs outside the application packages prevents operational artifacts from mixing with source code.

---

# models/

Stores downloaded AI models.

Examples include:

- Ollama models
- Sentence Transformers
- Local embedding models

Separating models avoids committing large binary files to version control.

---

# scripts/

Contains utility scripts used during development and maintenance.

Examples include:

- Database initialization
- Model downloads
- Data migration
- Batch ingestion

Scripts are intentionally isolated from application logic because they are executed independently.

---

# Design Principles

The project structure reflects several core engineering principles:

- Single Responsibility Principle
- Separation of Concerns
- Dependency Inversion
- Modular Design
- Testability
- Extensibility

Each directory has a single, well-defined responsibility, reducing complexity and making future enhancements easier to implement.

---

# Future Evolution

As OpsMind grows, additional modules will be introduced while preserving the same architectural philosophy.

Planned additions include:

- Multi-agent orchestration
- GraphRAG pipelines
- Observability engine
- Security analysis modules
- Workflow automation
- Plugin architecture

Because responsibilities are clearly separated, these features can be added without requiring major changes to the existing project structure.
