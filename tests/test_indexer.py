from app.rag.indexer import index_pdf
from app.rag.vector_store import get_qdrant_client

client = get_qdrant_client()

count = index_pdf(
    client,
    "research_papers",
    "data/sample_papers/attention.pdf"
)

print(
    f"Indexed {count} chunks"
)

client.close()