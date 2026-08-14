from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv(
        "APP_NAME",
        "Multilingual Property RAG Assistant",
    )
    chroma_path: str = os.getenv(
        "CHROMA_PATH",
        "data/chroma",
    )
    chroma_collection: str = os.getenv(
        "CHROMA_COLLECTION",
        "uk_property_sources",
    )
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    )
    default_top_k: int = int(
        os.getenv("DEFAULT_TOP_K", "4")
    )


settings = Settings()
