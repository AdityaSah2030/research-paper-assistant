from app.rag.loader import load_pdf
from app.rag.chunker import chunk_text
from app.rag.embeddings import get_embedding_model

from app.rag.vector_store import (
    get_qdrant_client,
    create_collection,
    upload_vectors
)

COLLECTION_NAME = "research_papers"

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

client = get_qdrant_client()

try:
    client.delete_collection(
        collection_name=COLLECTION_NAME
    )
except:
    pass

create_collection(
    client,
    collection_name=COLLECTION_NAME,
    vector_size=3072
)

upload_vectors(
    client,
    COLLECTION_NAME,
    chunks,
    vectors,
    source_file="attention.pdf"
)

print(f"Indexed {len(chunks)} chunks.")

client.close()