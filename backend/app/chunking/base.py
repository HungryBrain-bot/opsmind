from abc import ABC, abstractmethod

from backend.app.schemas.chunk import Chunk
from backend.app.schemas.document import Document


class Chunker(ABC):
    """
    Base interface for all chunking implementations.
    """

    @abstractmethod
    def chunk(self, document: Document) -> list[Chunk]:
        """
        Split a document into chunks.
        """
        raise NotImplementedError
