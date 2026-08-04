from typing import Any

from pydantic import BaseModel


class DocumentChunk(BaseModel):
    chunk_id: str
    content: str
    metadata: dict[str, Any]


class IndexResult(BaseModel):
    chunk_count: int
