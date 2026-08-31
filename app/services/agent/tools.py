from app.services.rag.retrieval import retrieve_retailstar_docs

def search_knowledge_base(question: str) -> dict:
    result = retrieve_retailstar_docs(
        question,
        top_k=3,
    )
    results = [
        {
        "content": chunk.content,
        "source": chunk.source_file,
        }
        for chunk in result.chunks
    ]

    return {
        "status"    : "success",
        "results": results,  
        "results_count": len(results),
    }