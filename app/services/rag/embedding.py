from openai import OpenAI

from app.core.config import settings
from app.schemas.rag import DocumentChunk


def build_embed_text(chunk: DocumentChunk) -> str:
    title = chunk.metadata.get("title", "")
    section_path = chunk.metadata.get("section_path", [])
    section = " > ".join(section_path) if section_path else ""

    parts = [f"Document: {title}"]
    if section:
        parts.append(f"Section: {section}")
    parts.append(chunk.content)
    return "\n\n".join(parts)


def embed_chunks(
    chunks: list[DocumentChunk],
    client: OpenAI | None = None,
) -> list[list[float]]:
    if not chunks:
        return []

    openai_client = client or OpenAI(api_key=settings.openai_api_key)
    texts = [build_embed_text(chunk) for chunk in chunks]

    response = openai_client.embeddings.create(
        model=settings.openai_embedding_model,
        input=texts,
        dimensions=settings.embedding_dimensions,
    )

    return [item.embedding for item in response.data]
