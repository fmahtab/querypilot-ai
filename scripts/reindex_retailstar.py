from app.services.rag.indexer import index_retailstar_docs


if __name__ == "__main__":
    result = index_retailstar_docs()

    print(f"Re-indexing complete.")
    print(f"Chunks indexed: {result.chunk_count}")