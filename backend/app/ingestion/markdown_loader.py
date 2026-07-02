from pathlib import Path
from uuid import uuid4

from backend.app.ingestion.loader import DocumentLoader
from backend.app.schemas.document import Document


class MarkdownLoader(DocumentLoader):
    """
    Loads markdown files.
    """

    def load(self, source: str) -> Document:
        path = Path(source)

        if not path.exists():
            raise FileNotFoundError(path)

        if path.suffix.lower() != ".md":
            raise ValueError("MarkdownLoader only supports .md files")

        content = path.read_text(encoding="utf-8")

        return Document(
            id=str(uuid4()),
            source=path,
            content=content,
            metadata={
                "type": "markdown",
            },
        )
