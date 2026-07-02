# Chunk Model

## Overview

Once a document has been divided into smaller pieces, each piece becomes an independent unit of knowledge known as a **Chunk**.

A chunk is much more than a substring of text.

It is a structured object that carries information about **where the text came from**, **its position within the document**, and **how it should be processed** throughout the AI pipeline.

In OpsMind, every embedding, retrieval result, graph node, and AI citation ultimately traces back to a Chunk.

For this reason, the Chunk model is one of the most important data structures in the platform.

---

# Why Not Use Strings?

Consider a simple document.

```
Security Report

↓

"Authentication uses OAuth 2.0."

↓

"Authorization is role based."

↓

"Logs are stored in Sentinel."
```

One approach would be to store each chunk as a plain string.

```
[
    "...",
    "...",
    "..."
]
```

This quickly becomes problematic.

Questions immediately arise:

- Which document did this text come from?
- Which page contained it?
- What was its position?
- Can it be cited?
- Can it be re-embedded?
- Which graph nodes belong to it?

A plain string cannot answer these questions.

---

# The Chunk Model

Instead of storing raw text, OpsMind stores structured objects.

```
Chunk

├── ID

├── Document ID

├── Source

├── Position

├── Character Range

├── Content

└── Metadata
```

Every processing stage receives the same structured representation.

---

# Relationship with the Document

A document is divided into many chunks.

```
Document

↓

Chunk 1

Chunk 2

Chunk 3

Chunk 4
```

Each chunk stores the identifier of its parent document.

```
Document

↓

document_id

↓

Chunk
```

This relationship enables complete traceability.

---

# Chunk ID

Every chunk receives a globally unique identifier.

Example:

```
chunk_01

chunk_02

chunk_03
```

or

```
UUID
```

The identifier allows downstream systems to reference a chunk without relying on its position in memory.

---

# Document ID

Each chunk records the document that created it.

```
Document

↓

Document ID

↓

Chunk
```

This enables:

- Citation generation
- Re-indexing
- Metadata lookup
- Graph construction

---

# Source

The original source file is preserved.

Example:

```
security/runbook.md
```

This allows AI responses to reference the original document.

Future user interfaces may display:

```
Source:

runbook.md
```

alongside generated answers.

---

# Chunk Position

The chunk index records where the chunk appears inside the document.

Example:

```
Chunk 0

Chunk 1

Chunk 2

Chunk 3
```

This enables reconstruction of the original document order.

---

# Character Range

Each chunk records the portion of the document it represents.

Example:

```
Start

0

End

512
```

or

```
512

1024
```

This information is valuable for:

- Highlighting search results
- Rebuilding context
- Visualizing retrieval

---

# Content

The content field stores the actual text.

Example:

```
Authentication uses OAuth 2.0...
```

This text is what later becomes an embedding.

---

# Metadata

Chunks may contain additional metadata.

Example:

```python
{
    "section": "Authentication",
    "page": 12,
    "language": "English"
}
```

Metadata enables filtering during retrieval.

For example:

```
Only search page 10-20

Only search Incident Reports

Only search Markdown files
```

---

# Relationship with Embeddings

Every chunk produces one embedding.

```
Chunk

↓

Embedding Model

↓

Vector
```

The vector database stores vectors alongside the originating chunk.

---

# Relationship with Retrieval

When a user submits a question:

```
Question

↓

Retriever

↓

Relevant Chunks
```

The retriever returns Chunk objects—not raw strings.

This allows the AI to access metadata, citations, and provenance information.

---

# Relationship with GraphRAG

GraphRAG also operates on chunks.

```
Chunk

↓

Entity Extraction

↓

Relationships

↓

Knowledge Graph
```

Each graph node can always be traced back to the originating chunk.

---

# Why Chunks are Immutable

Once created, chunks should generally remain unchanged.

Instead of modifying a chunk, later processing stages attach additional information such as:

- Embeddings
- Graph nodes
- Search scores

Keeping chunks immutable improves reproducibility and debugging.

---

# Benefits of a Dedicated Chunk Model

Using a dedicated model provides several advantages.

## Traceability

Every answer can be traced back to its source.

---

## Reusability

Chunks can be reused by multiple AI pipelines.

---

## Extensibility

Additional fields can be introduced without changing existing interfaces.

---

## Testability

Chunk objects can be created directly in unit tests.

---

## Consistency

Every component exchanges the same structured data model.

---

# Future Metadata

Future versions of OpsMind may enrich chunks with additional information.

Examples include:

```
page_number

section_title

heading_level

language

confidence_score

security_classification

checksum

embedding_version

processing_timestamp

entity_count
```

This additional metadata will improve search quality, governance, and explainability.

---

# Chunk Lifecycle

Throughout the platform, a chunk progresses through multiple stages.

```
Document

↓

Chunk

↓

Embedding

↓

Vector Database

↓

Retriever

↓

Graph Builder

↓

LLM

↓

AI Response
```

Notice that the chunk remains the central unit of knowledge throughout the entire pipeline.

---

# Design Principles

The Chunk model follows several engineering principles.

- Strong Typing
- Separation of Concerns
- Traceability
- Immutability
- Extensibility
- Production Readiness

These principles ensure that every piece of knowledge moving through OpsMind carries sufficient context for retrieval, explainability, and future AI processing.

---

# Future Evolution

Today, the Chunk model stores textual content and its relationship to the original document.

In future versions, chunks will become richer knowledge objects, carrying embeddings, entity references, graph identifiers, ranking information, confidence scores, and security metadata.

Although simple today, the Chunk model is intentionally designed as the central data structure that connects document ingestion, retrieval, GraphRAG, and AI reasoning into a unified processing pipeline.
