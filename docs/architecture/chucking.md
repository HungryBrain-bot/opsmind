# Chunking

## Overview

Large Language Models (LLMs) cannot efficiently process entire documents at once.

Enterprise documents such as security reports, runbooks, technical manuals, log files, and incident reports may contain thousands or even millions of characters.

Passing an entire document to an LLM is inefficient, expensive, and often impossible due to context window limitations.

To solve this problem, documents are divided into smaller pieces called **chunks**.

Chunking is one of the most critical stages in Retrieval-Augmented Generation (RAG) systems because it directly affects retrieval quality, embedding accuracy, and ultimately the quality of AI-generated answers.

---

# Why Chunking Exists

Consider a security runbook.

```
150 Pages

↓

~250,000 Characters

↓

Impossible to send directly to an LLM
```

Instead, we divide the document into manageable pieces.

```
Document

↓

Chunk 1

Chunk 2

Chunk 3

...

Chunk N
```

Each chunk becomes an independent unit of knowledge.

---

# Why Not Use the Entire Document?

Suppose a user asks:

> How do I restart the Splunk Indexer?

The answer may only exist in three paragraphs of a 200-page manual.

Sending the entire manual wastes:

- Tokens
- Time
- Money
- Context Window

Instead, the retriever only sends the relevant chunks.

```
User Question

↓

Retriever

↓

Relevant Chunks

↓

LLM
```

This dramatically improves efficiency.

---

# Relationship with the Document Model

The ingestion pipeline first creates a Document.

```
File

↓

Loader

↓

Document
```

The chunker then transforms that document into multiple Chunk objects.

```
Document

↓

Chunker

↓

Chunk 1

Chunk 2

Chunk 3
```

The original document is never modified.

---

# Relationship with the Chunk Model

Each chunk contains:

- Unique ID
- Parent Document ID
- Source
- Position
- Character Range
- Content

This allows every chunk to be traced back to its originating document.

```
Document

↓

Chunk

↓

Embedding

↓

Vector

↓

Search Result
```

---

# Chunking Strategies

There is no universally correct chunking strategy.

Different document types require different approaches.

OpsMind is designed to support multiple chunkers.

---

## Fixed Character Chunking

The simplest strategy.

```
1000 Characters

↓

Split Every 500 Characters
```

Advantages

- Fast
- Simple
- Predictable

Disadvantages

- May split sentences
- Loses semantic meaning

---

## Fixed Token Chunking

Instead of characters, chunk sizes are measured in LLM tokens.

```
512 Tokens

↓

512 Tokens

↓

512 Tokens
```

Advantages

- Better aligned with LLM context windows

Disadvantages

- Requires tokenizer support

---

## Sentence Chunking

Chunks end at sentence boundaries.

```
Sentence 1

Sentence 2

Sentence 3

↓

Chunk
```

Advantages

- Preserves grammar
- Better semantic meaning

---

## Paragraph Chunking

Entire paragraphs remain together.

```
Paragraph

↓

Chunk
```

Useful for:

- Documentation
- Books
- Technical Manuals

---

## Semantic Chunking

Instead of using size alone, semantic chunking detects changes in meaning.

```
Authentication

↓

Authorization

↓

Monitoring

↓

Incident Response
```

Each topic becomes a chunk.

Advantages

- High retrieval quality

Disadvantages

- Computationally expensive

---

## Markdown Chunking

Markdown provides natural structure.

```
#

##

###

```

Chunks follow headings instead of character limits.

Ideal for:

- GitHub Repositories
- Documentation
- ADRs
- Wikis

---

# Chunk Overlap

One of the biggest problems in chunking is losing context.

Example:

```
Chunk 1

"...the user authenticates using..."

Chunk 2

"...OAuth 2.0 tokens..."
```

The relationship is broken.

Instead, overlap is introduced.

```
Chunk 1

AAAAAAAAAA

BBBBBBBBBB

Chunk 2

BBBBBBBBBB

CCCCCCCCCC
```

Shared context improves retrieval.

---

# Why Overlap Matters

Without overlap:

```
Sentence Split Here

↓

Information Lost
```

With overlap:

```
Sentence

↓

Repeated

↓

Context Preserved
```

Most production RAG systems use overlap.

---

# Choosing Chunk Size

Smaller chunks

Advantages

- Higher precision
- Less irrelevant information

Disadvantages

- More embeddings
- Larger vector database

---

Larger chunks

Advantages

- More context

Disadvantages

- Lower retrieval precision

---

There is always a trade-off.

OpsMind allows different chunk sizes depending on the document type.

---

# Chunk Metadata

Chunks contain metadata beyond text.

Examples include:

```
document_id

chunk_index

source

page_number

section

language

tags
```

Metadata enables richer filtering during retrieval.

---

# Chunking in OpsMind

OpsMind separates chunking into independent components.

```
Document

↓

Chunker

↓

Chunks
```

The pipeline coordinates chunking, while each Chunker decides **how** to split the document.

This follows the Single Responsibility Principle.

---

# Current Architecture

```
Document

↓

Chunker

↓

Chunk

↓

Embedding

↓

Vector Store
```

The chunker knows nothing about embeddings or vector databases.

---

# Future Chunkers

OpsMind is designed to support multiple implementations.

Examples include:

```
TextChunker

MarkdownChunker

PDFChunker

SentenceChunker

SemanticChunker

CodeChunker

RecursiveChunker
```

New chunkers can be added without changing the ingestion pipeline.

---

# Relationship with Embeddings

Chunking always occurs before embedding generation.

```
Document

↓

Chunks

↓

Embeddings
```

Each chunk receives its own vector representation.

This enables fine-grained semantic search.

---

# Why Chunking Matters

The quality of a RAG system depends heavily on chunk quality.

Poor chunks lead to:

- Poor embeddings
- Poor retrieval
- Hallucinations
- Incorrect answers

Good chunks lead to:

- Better semantic search
- Better GraphRAG
- Better citations
- Better AI responses

Chunking is therefore one of the most important stages in the entire pipeline.

---

# Design Principles

The chunking subsystem follows several engineering principles:

- Separation of Concerns
- Strategy Pattern
- Extensibility
- Testability
- Reusability
- Production Readiness

These principles allow OpsMind to evolve from simple text splitting into sophisticated semantic chunking without changing the surrounding architecture.

---

# Future Evolution

Today, OpsMind provides a basic chunking abstraction and a simple text-based implementation.

As the platform matures, additional chunkers will support semantic segmentation, recursive splitting, code-aware chunking, Markdown structure, PDF layouts, and GraphRAG-specific preprocessing.

By designing chunking as a modular subsystem from the beginning, OpsMind ensures that future improvements in retrieval quality can be introduced with minimal impact on the rest of the platform.
