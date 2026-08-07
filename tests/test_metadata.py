from app.rag.vector_store import get_qdrant_client

client = get_qdrant_client()

points = client.scroll(
    collection_name="research_papers",
    limit=1
)[0]

print(points[0].payload)

client.close()