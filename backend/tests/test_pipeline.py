from backend.app.chunking.fixed import FixedSizeChunker
from backend.app.ingestion.pipeline import IngestionPipeline
from backend.app.ingestion.text_loader import TextLoader


def test_pipeline_ingests_document(tmp_path) -> None:
    file = tmp_path / "sample.txt"

    file.write_text(
        "Hello OpsMind! " * 100,
        encoding="utf-8",
    )

    pipeline = IngestionPipeline(
        loader=TextLoader(),
        chunker=FixedSizeChunker(
            chunk_size=100,
            chunk_overlap=20,
        ),
    )

    result = pipeline.ingest(str(file))

    assert result.document.content.startswith("Hello")

    assert len(result.chunks) > 0

    assert result.chunks[0].document_id == result.document.id
