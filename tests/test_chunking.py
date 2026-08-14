import pytest

from app.rag.chunking import chunk_text


def test_empty_text_returns_no_chunks():
    assert chunk_text("") == []


def test_short_text_returns_one_chunk():
    chunks = chunk_text(
        "UK house prices are influenced by many factors.",
        chunk_size=100,
        overlap=10,
    )

    assert len(chunks) == 1
    assert chunks[0].index == 0
    assert "house prices" in chunks[0].text


def test_overlap_must_be_smaller_than_chunk_size():
    with pytest.raises(ValueError):
        chunk_text(
            "Example text",
            chunk_size=100,
            overlap=100,
        )


def test_long_text_produces_multiple_chunks():
    text = "Property market sentence. " * 100

    chunks = chunk_text(
        text,
        chunk_size=200,
        overlap=30,
    )

    assert len(chunks) > 1
    assert all(chunk.text for chunk in chunks)
