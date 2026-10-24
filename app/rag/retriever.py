from app.rag.embeddings import get_embedding_model
from app.rag.vector_store import get_document_catalog, search_vectors


class RetrievedChunk(str):
    """
    Subclass of str holding text and metadata.
    Enables str operations (join, slicing) as well as dictionary-style access (.get, [])
    and direct attribute access.
    """
    def __new__(cls, text: str, **kwargs):
        obj = super().__new__(cls, text)
        obj._meta = kwargs
        for k, v in kwargs.items():
            setattr(obj, k, v)
        return obj

    def get(self, key, default=None):
        if key == "text":
            return str(self)
        return self._meta.get(key, default)

    def __getitem__(self, key):
        if isinstance(key, str):
            if key == "text":
                return str(self)
            return self._meta[key]
        return super().__getitem__(key)


def retrieve_chunks(
    client,
    collection_name,
    question,
    top_k_per_document=3,
    max_documents=8,
    session_id=None
):
    """
    Search each indexed document in the session separately so a global top-k result
    does not accidentally exclude passages from one of the uploaded papers.
    """
    embedding_model = get_embedding_model()
    query_vector = embedding_model.embed_query(question)

    catalog = get_document_catalog(client, collection_name, session_id=session_id)
    if not catalog:
        return []

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
            source_file=source_file,
            session_id=session_id
        )

        for result in results:
            point_id = str(result.id)
            if point_id in seen_point_ids:
                continue
            seen_point_ids.add(point_id)

            payload = result.payload or {}
            text = payload.get("text")
            if not text:
                continue

            retrieved.append(
                RetrievedChunk(
                    text,
                    source=payload.get("source", source_file),
                    document_id=payload.get("document_id"),
                    chunk_id=payload.get("chunk_id"),
                    page_number=payload.get("page_number"),
                    score=getattr(result, "score", None)
                )
            )

    # Prioritize higher-scoring passages first while preserving multi-document representation
    retrieved.sort(
        key=lambda chunk: getattr(chunk, "score", None) if getattr(chunk, "score", None) is not None else -1.0,
        reverse=True
    )

    return retrieved
