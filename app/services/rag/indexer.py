from pathlib import Path

from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.session import SessionLocal
from app.schemas.rag import IndexResult
from app.services.rag import ingest_retailstar_docs
from app.services.rag.embedding import embed_chunks
from app.services.rag.repository import replace_all_chunks


def index_retailstar_docs(
    docs_dir: Path | str | None = None,
    db: Session | None = None,
) -> IndexResult:
    owns_session = db is None
    session = db or SessionLocal()

    try:
        chunks = ingest_retailstar_docs(docs_dir)
        if not chunks:
            return IndexResult(chunk_count=0)

        embeddings = embed_chunks(chunks)
        chunk_count = replace_all_chunks(
            session,
            chunks,
            embeddings,
            settings.openai_embedding_model,
        )
        return IndexResult(chunk_count=chunk_count)
    finally:
        if owns_session:
            session.close()
