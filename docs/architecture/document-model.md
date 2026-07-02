# Document Model

## Overview

The Document model represents the first piece of knowledge that enters the OpsMind platform.

Before a document can be chunked, embedded, indexed, searched, or converted into a knowledge graph, it must first be represented in a consistent format.

OpsMind uses a dedicated `Document` schema to provide this standardized representation.

Rather than allowing each component to interpret files differently, every loader produces the same `Document` object.

This creates a clean contract between the ingestion layer and the rest of the platform.

---

# Why Do We Need a Document Model?

A document can originate from many different sources.

Examples include:

- Plain text files
- Markdown files
- PDF documents
- Word documents
- HTML pages
- Security reports
- Log exports
- Wiki pages
- API responses

Although these formats differ, the rest of the system should not care where the data came from.

Instead, every loader converts its input into the same model.

```
Text File
        │
Markdown
        │
PDF
        │
Word
        ▼
    Document
        │
        ▼
Chunking
```

This abstraction simplifies every downstream component.

---

# Responsibilities

The Document model is responsible for representing a complete document after it has been loaded into memory.

It stores:

- A unique identifier
- The source location
- The document content
- Additional metadata

It does **not** perform parsing, chunking, embedding generation, or graph construction.

Those responsibilities belong to other components.

---

# Current Structure

A Document currently contains:

```python
id

source

content

metadata
```

Each field has a specific purpose.

---

## Document ID

Every document receives a globally unique identifier.

Example:

```
7b85d7f8-e9fd-4a8b-b2dc-3fddf01b2df5
```

This identifier remains stable throughout the processing pipeline.

It allows downstream components to associate chunks, embeddings, entities, and graph nodes with their originating document.

---

## Source

The `source` field records where the document originated.

Example:

```python
Path("reports/security_report.md")
```

Keeping the original source improves traceability.

If a problem occurs during processing, the original file can be located immediately.

---

## Content

The content field stores the complete textual representation of the document.

Example:

```
# Security Report

Microsoft Sentinel detected...
```

This field contains the raw text exactly as produced by the document loader.

Subsequent stages such as chunking operate directly on this content.

---

## Metadata

Metadata stores additional information about the document.

Example:

```python
{
    "type": "markdown"
}
```

Metadata provides useful context without modifying the document content itself.

Future metadata may include:

```
author

title

created_date

modified_date

language

classification

security_level

mime_type
```

---

# Separation of Concerns

The Document model intentionally contains very little logic.

Its only responsibility is to represent data.

```
Document
        │
Stores Data
```

```
Loader
        │
Reads Files
```

```
Chunker
        │
Splits Text
```

```
Embedder
        │
Creates Vectors
```

Keeping these responsibilities separate makes the platform easier to understand and maintain.

---

# Relationship with Loaders

Every document loader returns the same object.

Example:

```
Text Loader
        │
        ▼
    Document

Markdown Loader
        │
        ▼
    Document

PDF Loader
        │
        ▼
    Document
```

Because every loader produces identical output, the chunking system never needs to know which loader created the document.

---

# Relationship with Chunking

The Document model serves as the input to the chunking pipeline.

```
Document
      │
      ▼
Chunker
      │
      ▼
Chunks
```

The original document always remains unchanged.

Chunkers generate new `Chunk` objects while preserving a reference to the original document.

---

# Immutability

Once a document has been loaded, it should generally be treated as immutable.

Subsequent processing stages should avoid modifying its content directly.

Instead, they should create new objects representing transformed data.

This approach makes debugging significantly easier because the original document always remains available.

---

# Why Use Pydantic?

The Document model inherits from Pydantic's `BaseModel`.

Benefits include:

- Automatic validation
- Type checking
- Serialization
- JSON support
- IDE autocompletion

For example, assigning an incorrect type immediately raises a validation error.

This prevents invalid data from entering the processing pipeline.

---

# Current Processing Flow

Today's ingestion process looks like this.

```
File
      │
      ▼
Loader
      │
      ▼
Document
```

This simple pipeline forms the foundation for every future capability.

---

# Future Processing Flow

As OpsMind evolves, the document will move through multiple processing stages.

```
File
      │
      ▼
Loader
      │
      ▼
Document
      │
      ▼
Chunker
      │
      ▼
Chunks
      │
      ▼
Embedding Model
      │
      ▼
Vectors
      │
      ▼
Vector Database
      │
      ▼
Retriever
      │
      ▼
LLM
```

The Document model remains the starting point for the entire pipeline.

---

# Future Metadata

As the platform grows, additional metadata fields may be introduced.

Examples include:

```
document_type

checksum

language

file_size

page_count

owner

tenant

created_at

updated_at

tags

classification
```

Keeping this information alongside the document enables richer filtering, search, and governance capabilities.

---

# Benefits

Using a standardized Document model provides several advantages.

## Consistency

Every loader produces the same output.

---

## Extensibility

New document formats can be added without changing downstream components.

---

## Traceability

Every chunk, embedding, and graph node can be traced back to its source document.

---

## Testability

The Document model can be constructed independently during testing.

---

## Maintainability

The ingestion pipeline communicates through well-defined interfaces instead of raw dictionaries or strings.

---

# Design Principles

The Document model follows several core engineering principles:

- Single Responsibility Principle
- Strong Typing
- Separation of Concerns
- Explicit Data Models
- Extensibility
- Traceability
- Production Readiness

These principles ensure that every piece of knowledge entering OpsMind follows a consistent structure before progressing through the remainder of the AI pipeline.

---

# Future Evolution

Today, the Document model represents a loaded text document with minimal metadata.

In future versions, it will evolve into the central representation of knowledge entering the platform, supporting richer metadata, document versioning, content hashing, security classifications, multilingual content, and integrations with enterprise knowledge sources.

Every downstream component—chunking, embeddings, vector search, GraphRAG, and AI agents—will build upon this foundational model.
