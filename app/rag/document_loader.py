from pathlib import Path

from pypdf import PdfReader


SUPPORTED_SUFFIXES = {".pdf", ".txt", ".md"}


def load_document(path: Path) -> str:
    suffix = path.suffix.lower()

    if suffix not in SUPPORTED_SUFFIXES:
        raise ValueError(
            f"Unsupported file type: {suffix}. "
            f"Supported types: {sorted(SUPPORTED_SUFFIXES)}"
        )

    if suffix in {".txt", ".md"}:
        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    reader = PdfReader(str(path))

    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        extracted = page.extract_text() or ""
        if extracted.strip():
            pages.append(
                f"[Page {page_number}]\n{extracted.strip()}"
            )

    return "\n\n".join(pages)


def discover_documents(raw_dir: Path) -> list[Path]:
    if not raw_dir.exists():
        return []

    return sorted(
        path
        for path in raw_dir.rglob("*")
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_SUFFIXES
    )
