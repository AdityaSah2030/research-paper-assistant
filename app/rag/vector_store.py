import os

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

    try:

        client.get_collection(
            collection_name=collection_name
        )

        print(
            f"Collection '{collection_name}' already exists."
        )

    except Exception:

        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )

        print(
            f"Collection '{collection_name}' created."
        )


def upload_vectors(
    client,
    collection_name,
    chunks,
    vectors,
    source_file
):

    points = []

    for idx, (chunk, vector) in enumerate(
        zip(chunks, vectors)
    ):

        points.append(
            PointStruct(
                id=idx,
                vector=vector,
                payload={
                    "text": chunk,
                    "source": source_file,
                    "chunk_id": idx
                }
            )
        )

    client.upsert(
        collection_name=collection_name,
        points=points
    )


def search_vectors(
    client,
    collection_name,
    query_vector,
    limit=3
):

    return client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=limit
    ).points