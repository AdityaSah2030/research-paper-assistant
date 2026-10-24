import os
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    FilterSelector,
)


def get_qdrant_client():
    return QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )


def create_collection(client, collection_name="research_papers", vector_size=3072):
    """Create the collection only when absent; never delete it during upload."""
    if client.collection_exists(collection_name=collection_name):
        info = client.get_collection(collection_name=collection_name)
        current_size = info.config.params.vectors.size

        if current_size != vector_size:
            raise ValueError(
                f"Qdrant collection uses {current_size}-dimensional vectors, "
                f"but the current embedding model produced {vector_size}. "
                "Use a compatible collection/model or create a new collection."
            )
        return

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE
        )
    )


def upload_vectors(
    client,
    collection_name,
    chunks,
    vectors,
    source_file,
    chunk_metadata=None,
    document_id=None
):
    """Upsert one document with unique vector IDs and page-level metadata."""
    if len(chunks) != len(vectors):
        raise ValueError("Chunk count and embedding count do not match.")

    chunk_metadata = chunk_metadata or [{} for _ in chunks]
    if len(chunk_metadata) != len(chunks):
        raise ValueError("Chunk metadata count does not match chunk count.")

    document_id = document_id or str(uuid.uuid4())
    points = []

    for idx, (chunk, vector, metadata) in enumerate(
        zip(chunks, vectors, chunk_metadata)
    ):
        payload = {
            "text": chunk,
            "source": source_file,
            "document_id": document_id,
            "chunk_id": idx,
        }

        page_number = metadata.get("page_number")
        if page_number is not None:
            payload["page_number"] = page_number

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload=payload
            )
        )

    if points:
        client.upsert(
            collection_name=collection_name,
            points=points,
            wait=True
        )

    return document_id


def delete_other_versions_of_document(
    client,
    collection_name,
    source_file,
    keep_document_id
):
    """
    Replace an earlier upload with the same filename only.
    Other filenames/documents in the collection are preserved.
    Legacy points without document_id are also removed for this filename.
    """
    client.delete(
        collection_name=collection_name,
        points_selector=FilterSelector(
            filter=Filter(
                must=[
                    FieldCondition(
                        key="source",
                        match=MatchValue(value=source_file)
                    )
                ],
                must_not=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=keep_document_id)
                    )
                ]
            )
        ),
        wait=True
    )


def get_document_catalog(client, collection_name):
    """Return unique filenames and indexed chunk counts from Qdrant payloads."""
    documents = {}
    offset = None

    while True:
        points, next_offset = client.scroll(
            collection_name=collection_name,
            limit=256,
            offset=offset,
            with_payload=["source"]
        )

        for point in points:
            payload = point.payload or {}
            source = payload.get("source")
            if not source:
                continue

            if source not in documents:
                documents[source] = {"file_name": source, "chunks_indexed": 0}
            documents[source]["chunks_indexed"] += 1

        if next_offset is None:
            break
        offset = next_offset

    return sorted(documents.values(), key=lambda item: item["file_name"].lower())


def search_vectors(client, collection_name, query_vector, limit=3, source_file=None):
    query_filter = None
    if source_file:
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="source",
                    match=MatchValue(value=source_file)
                )
            ]
        )

    response = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        query_filter=query_filter,
        limit=limit,
        with_payload=True
    )
    return response.points
