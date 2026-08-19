from app.services.rag.retrieval import retrieve_retailstar_docs

question = "What is considered low inventory?"
top_k = 3


result = retrieve_retailstar_docs(
    question,
    top_k=top_k,
    db=None,
)

for chunk in result.chunks:
    print(chunk)