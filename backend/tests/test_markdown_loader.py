import pytest

from backend.app.ingestion.markdown_loader import MarkdownLoader


def test_missing_file() -> None:
    loader = MarkdownLoader()

    with pytest.raises(FileNotFoundError):
        loader.load("does_not_exist.txt")


def test_load_markdown(tmp_path) -> None:
    file = tmp_path / "README.md"
    file.write_text("# OpsMind\nHello", encoding="utf-8")

    loader = MarkdownLoader()

    document = loader.load(str(file))

    assert document.content.startswith("# OpsMind")
    assert document.metadata["type"] == "markdown"


def test_invalid_extension(tmp_path) -> None:
    file = tmp_path / "notes.txt"
    file.write_text("hello")

    loader = MarkdownLoader()

    with pytest.raises(ValueError):
        loader.load(str(file))
