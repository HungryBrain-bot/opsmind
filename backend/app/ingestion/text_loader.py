from pathlib import Path
from uuid import uuid4

from backend.app.ingestion.loader import DocumentLoader
from backend.app.schemas.document import Document


class TextLoader(DocumentLoader):
    """
    Loads plain text files.
    """

    def load(self, source: str) -> Document:
        path = Path(source)

        if not path.exists():
            raise FileNotFoundError(path)

        content = path.read_text(encoding="utf-8")

        return Document(
            id=str(uuid4()),
            source=path,
            content=content,
            metadata={
                "type": "text",
            },
        )
