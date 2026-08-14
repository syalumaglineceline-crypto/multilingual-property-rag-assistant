from __future__ import annotations

import os
from typing import Any

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


SYSTEM_PROMPT = """
You are a multilingual assistant for source-grounded UK property-market information.

Follow these rules strictly:

1. Answer using only the retrieved source excerpts provided to you.
2. Do not use outside knowledge to fill gaps.
3. If the sources do not contain enough information to answer the question,
   clearly say that the available sources are insufficient.
4. Respond in the same language as the user's question unless the user
   explicitly asks for another language.
5. Cite factual statements using source numbers such as [1], [2], or [3].
6. Never invent a citation or refer to a source that was not provided.
7. Keep the answer concise and factual.
8. Do not provide personalised mortgage, legal, financial, investment,
   or property-valuation advice.
"""


def build_context(chunks: list[dict[str, Any]]) -> str:
    """Convert retrieved chunks into numbered source excerpts."""

    if not chunks:
        return "No relevant source excerpts were retrieved."

    context_blocks = []

    for number, chunk in enumerate(chunks, start=1):
        source = chunk.get("source", "unknown")
        chunk_id = chunk.get("chunk_id", "unknown")
        text = chunk.get("text", "").strip()

        context_blocks.append(
            f"[{number}] Source: {source}\n"
            f"Chunk ID: {chunk_id}\n"
            f"{text}"
        )

    return "\n\n".join(context_blocks)


class AnswerGenerator:
    """Generate source-grounded answers from retrieved document chunks."""

    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured."
            )

        self.model = os.getenv(
            "OPENAI_MODEL",
            "gpt-5-mini",
        )

        self.client = OpenAI(api_key=api_key)

    def generate(
        self,
        question: str,
        chunks: list[dict[str, Any]],
    ) -> str:
        """Generate an answer grounded only in retrieved chunks."""

        context = build_context(chunks)

        prompt = f"""
User question:
{question}

Retrieved source excerpts:
{context}

Generate a source-grounded answer to the user's question.

Every factual claim should include the relevant source number,
for example [1] or [2].

If the retrieved excerpts do not support an answer, do not guess.
State that the available sources do not contain enough information.
"""

        response = self.client.responses.create(
            model=self.model,
            instructions=SYSTEM_PROMPT,
            input=prompt,
        )

        answer = response.output_text.strip()

        if not answer:
            return (
                "The system could not generate a grounded answer "
                "from the available sources."
            )

        return answer
