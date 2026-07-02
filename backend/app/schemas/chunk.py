"""
Domain model representing a chunk of a document.

Chunks are the fundamental unit used throughout the AI pipeline.
Every embedding, retrieval result, graph node, and LLM context
originates from a Chunk.
"""

from pathlib import Path

from pydantic import BaseModel, Field


class Chunk(BaseModel):
    """
    Represents a chunk extracted from a document.
    """

    #
    # Identity
    #
    id: str

    #
    # Parent document
    #
    document_id: str

    source: Path

    #
    # Chunk position
    #
    chunk_index: int

    start_char: int

    end_char: int

    #
    # Chunk content
    #
    content: str

    #
    # Additional metadata
    #
    metadata: dict[str, str | int | float | bool] = Field(default_factory=dict)
