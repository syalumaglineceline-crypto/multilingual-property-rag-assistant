from pydantic import BaseModel, Field


class RetrieveRequest(BaseModel):
    question: str = Field(..., min_length=2)
    top_k: int = Field(default=4, ge=1, le=10)


class SourceChunk(BaseModel):
    rank: int
    source: str
    chunk_id: str
    chunk_index: int
    text: str
    distance: float | None = None


class RetrieveResponse(BaseModel):
    question: str
    results: list[SourceChunk]


class AskRequest(BaseModel):
    question: str = Field(..., min_length=2)
    top_k: int = Field(default=4, ge=1, le=10)


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceChunk]


class HealthResponse(BaseModel):
    status: str
    app: str


class StatsResponse(BaseModel):
    collection: str
    indexed_chunks: int
    embedding_model: str
