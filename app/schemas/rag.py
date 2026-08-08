from typing import Any

from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    chunk_id: str
    content: str
    metadata: dict[str, Any]


class IndexResult(BaseModel):
    chunk_count: int


class RetrievedChunk(BaseModel):
    chunk_id: str
    content: str
    metadata: dict[str, Any]
    cosine_similarity: float = Field(
        description=(
            "Cosine similarity derived from pgvector distance (1 - distance). "
            "Theoretical range is -1 to 1; higher values indicate greater similarity."
        )
    )
    source_file: str


class RetrievalResult(BaseModel):
    question: str
    top_k: int
    chunks: list[RetrievedChunk]
