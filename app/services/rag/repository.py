from datetime import datetime

from sqlalchemy.orm import Session

from app.models.rag_chunk import RagChunk
from app.schemas.rag import DocumentChunk


def delete_all_chunks(db: Session) -> None:
    db.query(RagChunk).delete()
    db.commit()


def insert_chunks(
    db: Session,
    chunks: list[DocumentChunk],
    embeddings: list[list[float]],
    embedding_model: str,
) -> int:
    now = datetime.utcnow()
    rows = []

    for chunk, embedding in zip(chunks, embeddings, strict=True):
        version = chunk.metadata.get("version")
        document_version = str(version) if version is not None else None

        rows.append(
            RagChunk(
                chunk_id=chunk.chunk_id,
                source_file=chunk.metadata["source_file"],
                content=chunk.content,
                embedding=embedding,
                embedding_model=embedding_model,
                chunk_metadata=chunk.metadata,
                document_version=document_version,
                created_at=now,
                updated_at=now,
            )
        )

    db.add_all(rows)
    db.commit()
    return len(rows)


def replace_all_chunks(
    db: Session,
    chunks: list[DocumentChunk],
    embeddings: list[list[float]],
    embedding_model: str,
) -> int:
    now = datetime.utcnow()
    db.query(RagChunk).delete()

    rows = []
    for chunk, embedding in zip(chunks, embeddings, strict=True):
        version = chunk.metadata.get("version")
        document_version = str(version) if version is not None else None

        rows.append(
            RagChunk(
                chunk_id=chunk.chunk_id,
                source_file=chunk.metadata["source_file"],
                content=chunk.content,
                embedding=embedding,
                embedding_model=embedding_model,
                chunk_metadata=chunk.metadata,
                document_version=document_version,
                created_at=now,
                updated_at=now,
            )
        )

    db.add_all(rows)
    db.commit()
    return len(rows)
