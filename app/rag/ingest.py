from hashlib import sha256
from pathlib import Path

from app.rag.chunking import chunk_text
from app.rag.document_loader import (
    discover_documents,
    load_document,
)
from app.rag.embeddings import embed_texts
from app.rag.vector_store import PropertyVectorStore


def make_chunk_id(
    source: str,
    chunk_index: int,
    text: str,
) -> str:
    payload = f"{source}|{chunk_index}|{text}"
    digest = sha256(
        payload.encode("utf-8")
    ).hexdigest()[:20]

    return f"{Path(source).stem}-{chunk_index}-{digest}"


def ingest_directory(
    raw_dir: Path = Path("data/raw"),
) -> dict:
    documents = discover_documents(raw_dir)

    if not documents:
        return {
            "documents": 0,
            "chunks": 0,
            "message": f"No supported documents found in {raw_dir}.",
        }

    store = PropertyVectorStore()
    total_chunks = 0

    for path in documents:
        text = load_document(path)
        chunks = chunk_text(text)

        if not chunks:
            continue

        ids = []
        texts = []
        metadatas = []

        for chunk in chunks:
            chunk_id = make_chunk_id(
                source=str(path),
                chunk_index=chunk.index,
                text=chunk.text,
            )

            ids.append(chunk_id)
            texts.append(chunk.text)
            metadatas.append({
                "source": path.name,
                "source_path": str(path),
                "chunk_index": chunk.index,
            })

        embeddings = embed_texts(texts)

        store.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        total_chunks += len(chunks)

    return {
        "documents": len(documents),
        "chunks": total_chunks,
        "message": "Ingestion completed.",
    }
