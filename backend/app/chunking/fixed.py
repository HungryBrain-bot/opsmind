"""
Fixed-size text chunking implementation.

This chunker splits a document into fixed-size overlapping chunks using
a sliding window algorithm. Overlap preserves context between adjacent
chunks, improving retrieval quality for downstream embedding and RAG
pipelines.
"""

from backend.app.chunking.base import Chunker
from backend.app.schemas.chunk import Chunk
from backend.app.schemas.document import Document


class FixedSizeChunker(Chunker):
    """
    Splits a document into fixed-size overlapping chunks.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> None:
        """
        Initialize the chunker.

        Args:
            chunk_size:
                Maximum number of characters per chunk.

            chunk_overlap:
                Number of overlapping characters shared between
                consecutive chunks.

        Raises:
            ValueError:
                If the chunking configuration is invalid.
        """

        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative")

        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, document: Document) -> list[Chunk]:
        """
        Split a document into overlapping chunks.

        Args:
            document:
                The document to split.

        Returns:
            A list of Chunk objects.
        """

        text = document.content

        # Empty documents produce no chunks.
        if not text:
            return []

        chunks: list[Chunk] = []

        start = 0
        index = 0

        while start < len(text):

            end = min(start + self.chunk_size, len(text))

            chunk_text = text[start:end]

            chunks.append(
                Chunk(
                    id=f"{document.id}-{index}",
                    document_id=document.id,
                    source=document.source,
                    chunk_index=index,
                    start_char=start,
                    end_char=end,
                    content=chunk_text,
                    metadata=document.metadata.copy(),
                )
            )

            # Reached the end of the document.
            if end == len(text):
                break

            # Advance the sliding window while preserving overlap.
            start = end - self.chunk_overlap
            index += 1

        return chunks
