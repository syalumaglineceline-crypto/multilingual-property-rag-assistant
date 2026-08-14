from app.rag.embeddings import embed_query
from app.rag.vector_store import PropertyVectorStore


class RetrievalService:
    def __init__(self) -> None:
        self.store = PropertyVectorStore()

    def retrieve(
        self,
        question: str,
        top_k: int,
    ) -> list[dict]:
        if self.store.count() == 0:
            return []

        query_embedding = embed_query(question)

        raw = self.store.query(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        ids = raw.get("ids", [[]])[0]
        documents = raw.get("documents", [[]])[0]
        metadatas = raw.get("metadatas", [[]])[0]
        distances = raw.get("distances", [[]])[0]

        results = []

        for rank, (
            chunk_id,
            text,
            metadata,
            distance,
        ) in enumerate(
            zip(
                ids,
                documents,
                metadatas,
                distances,
            ),
            start=1,
        ):
            metadata = metadata or {}

            results.append({
                "rank": rank,
                "source": metadata.get("source", "unknown"),
                "chunk_id": chunk_id,
                "chunk_index": int(
                    metadata.get("chunk_index", -1)
                ),
                "text": text or "",
                "distance": (
                    float(distance)
                    if distance is not None
                    else None
                ),
            })

        return results
