from app.rag.loader import load_pdf
from app.rag.chunker import chunk_text
from app.rag.embeddings import get_embedding_model

from app.rag.vector_store import (
    get_qdrant_client,
    create_collection,
    upload_vectors
)

print("Loading PDF...")
pdf_text = load_pdf(
    "data/sample_papers/attention.pdf"
)

print("Chunking...")
chunks = chunk_text(pdf_text)

print("Generating embeddings...")
embedding_model = get_embedding_model()

vectors = embedding_model.embed_documents(
    chunks
)

print("Creating Qdrant collection...")
client = get_qdrant_client()

create_collection(client)

print("Uploading vectors...")
upload_vectors(
    client,
    "research_papers",
    chunks,
    vectors
)

print("Upload successful!")

print(
    client.count(
        collection_name="research_papers"
    )
)

client.close()