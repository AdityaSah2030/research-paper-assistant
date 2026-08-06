from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

def get_qdrant_client():
    return QdrantClient(path="./qdrant_data")


def create_collection(client):
    client.create_collection(
        collection_name="research_papers",
        vectors_config=VectorParams(
            size=3072,
            distance=Distance.COSINE
        )
    )


def upload_vectors(
    client,
    collection_name,
    chunks,
    vectors
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
                    "text": chunk
                }
            )
        )

    client.upsert(
        collection_name=collection_name,
        points=points
    )