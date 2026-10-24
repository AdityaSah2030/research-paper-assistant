from app.rag.embeddings import get_embedding_model
from app.rag.vector_store import search_vectors


def retrieve_chunks(
    client,
    collection_name,
    question,
    top_k=5
):
    embedding_model = get_embedding_model()
    query_vector = embedding_model.embed_query(question)

    results = search_vectors(
        client,
        collection_name,
        query_vector,
        limit=top_k
    )

    retrieved = []
    for result in results:
        payload = result.payload or {}
        if not payload.get("text"):
            continue

        retrieved.append({
            "text": payload["text"],
            "source": payload.get("source", "Unknown document"),
            "document_id": payload.get("document_id"),
            "chunk_id": payload.get("chunk_id"),
            "page_number": payload.get("page_number"),
            "score": getattr(result, "score", None)
        })

    return retrieved
