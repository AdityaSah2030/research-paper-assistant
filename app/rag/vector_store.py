import os
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)


def get_qdrant_client():
    return QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )


def create_collection(
    client,
    collection_name="research_papers",
    vector_size=3072
):
    # Do not treat every Qdrant error as "collection missing".
    if client.collection_exists(collection_name=collection_name):
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
    """
    Store chunks with unique point IDs so different documents/chunks
    cannot overwrite one another.
    """
    if len(chunks) != len(vectors):
        raise ValueError("The number of chunks and vectors must match.")

    chunk_metadata = chunk_metadata or [{} for _ in chunks]
    if len(chunk_metadata) != len(chunks):
        raise ValueError("The number of chunk metadata records must match.")

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
        if metadata.get("page_number") is not None:
            payload["page_number"] = metadata["page_number"]

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


def search_vectors(
    client,
    collection_name,
    query_vector,
    limit=3
):
    return client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=limit,
        with_payload=True
    ).points
