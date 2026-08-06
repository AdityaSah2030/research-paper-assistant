from app.rag.vector_store import (
    get_qdrant_client,
    create_collection
)

client = get_qdrant_client()

create_collection(client)

print(client.get_collections())