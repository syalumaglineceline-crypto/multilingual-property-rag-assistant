from typing import Any

from sentence_transformers import CrossEncoder


RERANKER_MODEL = (
    "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"
)

_reranker = None


def get_reranker() -> CrossEncoder:
    """Load the multilingual reranker only when first needed."""

    global _reranker

    if _reranker is None:
        _reranker = CrossEncoder(RERANKER_MODEL)

    return _reranker


def rerank_results(
    question: str,
    results: list[dict[str, Any]],
    top_k: int = 4,
) -> list[dict[str, Any]]:
    """
    Rerank retrieved passages using a multilingual cross-encoder.

    The cross-encoder jointly evaluates the user question and
    each candidate passage, providing a relevance score for
    second-stage retrieval ranking.
    """

    if not results:
        return []

    model = get_reranker()

    pairs = [
        (
            question,
            result.get("text", ""),
        )
        for result in results
    ]

    scores = model.predict(pairs)

    scored_results = []

    for result, score in zip(results, scores):
        reranked = result.copy()
        reranked["_rerank_score"] = float(score)
        scored_results.append(reranked)

    scored_results.sort(
        key=lambda item: item["_rerank_score"],
        reverse=True,
    )

    selected = scored_results[:top_k]

    for rank, result in enumerate(selected, start=1):
        result["rank"] = rank
        result.pop("_rerank_score", None)

    return selected
