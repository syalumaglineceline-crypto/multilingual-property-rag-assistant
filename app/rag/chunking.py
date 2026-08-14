from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:
    index: int
    text: str


def chunk_text(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 200,
) -> list[TextChunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")

    if overlap < 0:
        raise ValueError("overlap cannot be negative.")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size.")

    cleaned = "\n".join(
        line.strip()
        for line in text.replace("\r\n", "\n").split("\n")
        if line.strip()
    ).strip()

    if not cleaned:
        return []

    chunks: list[TextChunk] = []
    start = 0
    index = 0
    n = len(cleaned)

    while start < n:
        proposed_end = min(start + chunk_size, n)
        end = proposed_end

        if proposed_end < n:
            boundary = cleaned.rfind("\n", start, proposed_end)

            if boundary <= start + chunk_size // 2:
                boundary = cleaned.rfind(". ", start, proposed_end)

                if boundary > start + chunk_size // 2:
                    boundary += 1

            if boundary > start + chunk_size // 2:
                end = boundary

        chunk = cleaned[start:end].strip()

        if chunk:
            chunks.append(TextChunk(index=index, text=chunk))
            index += 1

        if end >= n:
            break

        start = max(end - overlap, start + 1)

    return chunks
