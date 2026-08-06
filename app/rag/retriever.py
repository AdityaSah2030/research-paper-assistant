from app.rag.embeddings import get_embedding_model
from app.rag.vector_store import search_vectors


def retrieve_chunks(
    client,
    collection_name,
    question,
    top_k=3
):
    embedding_model = get_embedding_model()

    query_vector = embedding_model.embed_query(
        question
    )

    results = search_vectors(
        client,
        collection_name,
        query_vector,
        limit=top_k
    )

    return [
        result.payload["text"]
        for result in results
    ]