from fastapi import FastAPI

from app.config import settings
from app.rag.service import RetrievalService
from app.schemas import (
    HealthResponse,
    RetrieveRequest,
    RetrieveResponse,
    StatsResponse,
)


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=(
        "Multilingual semantic retrieval API for "
        "source-grounded UK property information."
    ),
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        app=settings.app_name,
    )


@app.get("/stats", response_model=StatsResponse)
def stats() -> StatsResponse:
    service = RetrievalService()

    return StatsResponse(
        collection=settings.chroma_collection,
        indexed_chunks=service.store.count(),
        embedding_model=settings.embedding_model,
    )


@app.post("/retrieve", response_model=RetrieveResponse)
def retrieve(
    request: RetrieveRequest,
) -> RetrieveResponse:
    service = RetrievalService()

    results = service.retrieve(
        question=request.question,
        top_k=request.top_k,
    )

    return RetrieveResponse(
        question=request.question,
        results=results,
    )
