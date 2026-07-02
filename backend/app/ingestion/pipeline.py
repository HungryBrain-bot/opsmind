"""
Coordinates the document ingestion process.
"""

from backend.app.chunking.base import Chunker
from backend.app.ingestion.loader import DocumentLoader
from backend.app.schemas.ingestion import IngestionResult


class IngestionPipeline:
    """
    Coordinates the document ingestion process.

    Responsibilities
    ----------------
    1. Load a document.
    2. Chunk the document.
    3. Return the complete ingestion result.
    """

    def __init__(
        self,
        loader: DocumentLoader,
        chunker: Chunker,
    ) -> None:
        self.loader = loader
        self.chunker = chunker

    def ingest(self, source: str) -> IngestionResult:
        """
        Load a document and split it into chunks.
        """

        document = self.loader.load(source)

        chunks = self.chunker.chunk(document)

        return IngestionResult(
            document=document,
            chunks=chunks,
        )
