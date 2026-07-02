from pathlib import Path

import pytest

from backend.app.chunking.base import Chunker
from backend.app.chunking.fixed import FixedSizeChunker
from backend.app.schemas.chunk import Chunk
from backend.app.schemas.document import Document


def test_chunk_creation() -> None:
    chunk = Chunk(
        id="chunk-1",
        document_id="doc-1",
        source=Path("README.md"),
        chunk_index=0,
        start_char=0,
        end_char=42,
        content="Hello OpsMind",
    )

    assert chunk.document_id == "doc-1"
    assert chunk.chunk_index == 0
    assert chunk.content == "Hello OpsMind"


def test_chunker_is_abstract() -> None:
    with pytest.raises(TypeError):
        Chunker()


def test_fixed_chunker_creates_multiple_chunks() -> None:

    text = "A" * 2500

    document = Document(
        id="doc1",
        source=Path("sample.txt"),
        content=text,
    )

    chunker = FixedSizeChunker(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = chunker.chunk(document)

    assert len(chunks) == 3

    assert chunks[0].chunk_index == 0
    assert chunks[1].chunk_index == 1
    assert chunks[2].chunk_index == 2


def test_chunk_overlap() -> None:

    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    document = Document(
        id="doc1",
        source=Path("sample.txt"),
        content=text,
    )

    chunker = FixedSizeChunker(
        chunk_size=10,
        chunk_overlap=2,
    )

    chunks = chunker.chunk(document)

    assert chunks[0].content == "ABCDEFGHIJ"

    assert chunks[1].content == "IJKLMNOPQR"

    assert chunks[2].content == "QRSTUVWXYZ"


def test_invalid_chunk_size() -> None:

    with pytest.raises(ValueError):
        FixedSizeChunker(chunk_size=0)


def test_invalid_overlap() -> None:

    with pytest.raises(ValueError):
        FixedSizeChunker(
            chunk_size=100,
            chunk_overlap=100,
        )
