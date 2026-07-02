"""
Domain model representing a document ingested into OpsMind.

A Document is the canonical representation of a source file before it
is processed into chunks. Every ingestion pipeline begins by producing
a Document from a supported data source.
"""

from pathlib import Path

from pydantic import BaseModel, Field


class Document(BaseModel):
    """
    Represents a document loaded into OpsMind.
    """

    #
    # Identity
    #
    id: str

    #
    # Source
    #
    source: Path

    #
    # Document content
    #
    content: str

    #
    # Additional metadata
    #
    metadata: dict[str, str | int | float | bool] = Field(default_factory=dict)
