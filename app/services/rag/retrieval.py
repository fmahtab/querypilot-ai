from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.session import SessionLocal
from app.schemas.rag import RetrievedChunk, RetrievalResult
from app.services.rag.embedding import embed_query
from app.services.rag.repository import search_similar_chunks

MIN_TOP_K = 1
MAX_TOP_K = 20


def retrieve_retailstar_docs(
    question: str,
    top_k: int | None = None,
    db: Session | None = None,
) -> RetrievalResult:
    normalized_question = question.strip()
    if not normalized_question:
        raise ValueError("Question must not be empty.")

    limit = top_k if top_k is not None else settings.rag_top_k
    if not MIN_TOP_K <= limit <= MAX_TOP_K:
        raise ValueError(f"top_k must be between {MIN_TOP_K} and {MAX_TOP_K}.")
    owns_session = db is None
    session = db or SessionLocal()

    try:
        query_embedding = embed_query(normalized_question)
        rows = search_similar_chunks(
            session,
            query_embedding,
            limit,
            settings.openai_embedding_model,
        )

        chunks = [
            RetrievedChunk(
                chunk_id=row.chunk_id,
                content=row.content,
                metadata=row.chunk_metadata,
                cosine_similarity=cosine_similarity,
                source_file=row.source_file,
            )
            for row, cosine_similarity in rows
        ]

        return RetrievalResult(
            question=normalized_question,
            top_k=limit,
            chunks=chunks,
        )
    finally:
        if owns_session:
            session.close()
