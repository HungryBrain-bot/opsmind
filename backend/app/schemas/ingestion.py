"""
Models used by the ingestion pipeline.
"""

from pydantic import BaseModel

from backend.app.schemas.chunk import Chunk
from backend.app.schemas.document import Document


class IngestionResult(BaseModel):
    """
    Result produced after ingesting a document.
    """

    document: Document
    chunks: list[Chunk]
