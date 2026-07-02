import pytest

from backend.app.ingestion.text_loader import TextLoader


def test_missing_file() -> None:
    loader = TextLoader()

    with pytest.raises(FileNotFoundError):
        loader.load("does_not_exist.txt")
