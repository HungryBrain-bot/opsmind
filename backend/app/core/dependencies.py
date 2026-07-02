from fastapi import Depends

from backend.app.chunking.fixed import FixedSizeChunker
from backend.app.config.settings import Settings, settings
from backend.app.ingestion.pipeline import IngestionPipeline
from backend.app.ingestion.text_loader import TextLoader


def get_settings() -> Settings:
    """
    Return the application settings instance.
    """
    return settings


def get_text_loader() -> TextLoader:
    return TextLoader()


def get_fixed_chunker(
    settings: Settings = Depends(get_settings),
) -> FixedSizeChunker:

    return FixedSizeChunker(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )


def get_ingestion_pipeline(
    loader: TextLoader = Depends(get_text_loader),
    chunker: FixedSizeChunker = Depends(get_fixed_chunker),
) -> IngestionPipeline:

    return IngestionPipeline(
        loader=loader,
        chunker=chunker,
    )
