from app.rag.embeddings import get_embedding_model
from app.rag.vector_store import get_document_catalog, search_vectors


def retrieve_chunks(
    client,
    collection_name,
    question,
    top_k_per_document=2,
    max_documents=8
):
    """
    Search each indexed document separately so a global top-k result does not
    accidentally exclude every passage from one of the uploaded papers.
    """
    embedding_model = get_embedding_model()
    query_vector = embedding_model.embed_query(question)

    catalog = get_document_catalog(client, collection_name)
    catalog = catalog[:max_documents]

    retrieved = []
    seen_point_ids = set()

    for document in catalog:
        source_file = document["file_name"]

        results = search_vectors(
            client,
            collection_name,
            query_vector,
            limit=top_k_per_document,
            source_file=source_file
        )

        for result in results:
            if str(result.id) in seen_point_ids:
                continue
            seen_point_ids.add(str(result.id))

            payload = result.payload or {}
            text = payload.get("text")
            if not text:
                continue

            retrieved.append({
                "text": text,
                "source": payload.get("source", source_file),
                "document_id": payload.get("document_id"),
                "chunk_id": payload.get("chunk_id"),
                "page_number": payload.get("page_number"),
                "score": getattr(result, "score", None)
            })

    return retrieved
