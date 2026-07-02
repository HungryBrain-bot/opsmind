from abc import ABC, abstractmethod

from backend.app.schemas.document import Document


class DocumentLoader(ABC):
    """
    Base class for all document loaders.
    """

    @abstractmethod
    def load(self, source: str) -> Document:
        """
        Load a document from a source.
        """
