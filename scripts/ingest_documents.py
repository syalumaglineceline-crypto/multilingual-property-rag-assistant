from pathlib import Path

from app.rag.ingest import ingest_directory


if __name__ == "__main__":
    result = ingest_directory(
        Path("data/raw")
    )

    print("Documents:", result["documents"])
    print("Chunks:", result["chunks"])
    print(result["message"])
