import re
from typing import Any


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by",
    "for", "from", "how", "in", "is", "it", "of", "on",
    "the", "to", "was", "were", "what", "when", "which",
}


def _normalise_tokens(text: str) -> list[str]:
    """Convert text into simple comparable tokens."""

    tokens = re.findall(r"\b[\w£%.-]+\b", text.lower())

    normalised = []

    for token in tokens:
        if len(token) > 4 and token.endswith("s") and not token.endswith("ss"):
            token = token[:-1]

        if token not in STOP_WORDS:
            normalised.append(token)

    return normalised


def _query_bigrams(tokens: list[str]) -> list[str]:
    """Create consecutive two-word phrases from query tokens."""

    return [
        f"{tokens[i]} {tokens[i + 1]}"
        for i in range(len(tokens) - 1)
    ]


def rerank_results(
    question: str,
    results: list[dict[str, Any]],
    top_k: int = 4,
) -> list[dict[str, Any]]:
    """
    Rerank semantic-search results using lightweight lexical signals.

    Combines:
    - original vector similarity
    - important query-term overlap
    - query phrase overlap
    - matching numeric/date information
    """

    query_tokens = _normalise_tokens(question)
    query_token_set = set(query_tokens)
    query_bigrams = _query_bigrams(query_tokens)

    query_numbers = set(
        re.findall(r"\b\d+(?:[.,]\d+)?\b", question.lower())
    )

    scored_results = []

    for result in results:
        text = result.get("text", "")
        text_lower = text.lower()
        text_tokens = set(_normalise_tokens(text))

        # Semantic similarity from Chroma distance.
        distance = result.get("distance")

        if distance is None:
            semantic_score = 0.0
        else:
            semantic_score = 1.0 / (1.0 + distance)

        # Important query-word overlap.
        if query_token_set:
            lexical_score = (
                len(query_token_set & text_tokens)
                / len(query_token_set)
            )
        else:
            lexical_score = 0.0

        # Reward passages containing consecutive query concepts.
        phrase_matches = sum(
            1 for phrase in query_bigrams
            if phrase in text_lower
        )

        if query_bigrams:
            phrase_score = phrase_matches / len(query_bigrams)
        else:
            phrase_score = 0.0

        # Reward exact year/date/number matches.
        text_numbers = set(
            re.findall(r"\b\d+(?:[.,]\d+)?\b", text_lower)
        )

        if query_numbers:
            number_score = (
                len(query_numbers & text_numbers)
                / len(query_numbers)
            )
        else:
            number_score = 0.0

        final_score = (
            0.45 * semantic_score
            + 0.30 * lexical_score
            + 0.15 * phrase_score
            + 0.10 * number_score
        )

        reranked = result.copy()
        reranked["_rerank_score"] = final_score
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
