from fastapi import FastAPI, HTTPException

from app.config import settings
from app.rag.generator import AnswerGenerator
from app.rag.service import RetrievalService
from app.schemas import (
    AskRequest,
    AskResponse,
    HealthResponse,
    RetrieveRequest,
    RetrieveResponse,
    StatsResponse,
)


app = FastAPI(
    title=settings.app_name,
    version="0.2.0",
    description=(
        "Multilingual RAG API for source-grounded "
        "UK property information."
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


@app.post("/ask", response_model=AskResponse)
def ask(
    request: AskRequest,
) -> AskResponse:
    service = RetrievalService()

    results = service.retrieve(
        question=request.question,
        top_k=request.top_k,
    )

    if not results:
        return AskResponse(
            question=request.question,
            answer=(
                "I could not find enough information "
                "in the available sources to answer this question."
            ),
            sources=[],
        )

    try:
        generator = AnswerGenerator()

        answer = generator.generate(
            question=request.question,
            chunks=results,
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    return AskResponse(
        question=request.question,
        answer=answer,
        sources=results,
    )
