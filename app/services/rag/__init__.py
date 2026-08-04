from pathlib import Path
from typing import Any

from app.core.config import settings
from app.schemas.rag import DocumentChunk
from app.services.rag.chunker import chunk_by_headings
from app.services.rag.loader import load_all_markdown_files


def ingest_retailstar_docs(docs_dir: Path | str | None = None) -> list[DocumentChunk]:
    path = Path(docs_dir) if docs_dir is not None else Path(settings.retailstar_docs_path)
    chunks: list[DocumentChunk] = []

    for source_file, front_matter, body in load_all_markdown_files(path):
        for chunk_index, section in enumerate(chunk_by_headings(body)):
            metadata: dict[str, Any] = {
                **front_matter,
                "source_file": source_file,
                "heading": section["heading"],
                "heading_level": section["heading_level"],
                "section_path": section["section_path"],
                "chunk_index": chunk_index,
            }
            chunks.append(
                DocumentChunk(
                    chunk_id=f"{source_file}::chunk-{chunk_index:03d}",
                    content=section["content"],
                    metadata=metadata,
                )
            )

    return chunks


from app.services.rag.indexer import index_retailstar_docs

__all__ = ["ingest_retailstar_docs", "index_retailstar_docs"]
