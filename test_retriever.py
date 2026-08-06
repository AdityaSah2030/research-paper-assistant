from app.rag.loader import load_pdf
from app.rag.chunker import chunk_text
from app.rag.embeddings import get_embedding_model

from app.rag.vector_store import (
    get_qdrant_client,
    create_collection,
    upload_vectors
)

from app.rag.retriever import retrieve_chunks


print("Loading PDF...")
pdf_text = load_pdf(
    "data/sample_papers/attention.pdf"
)

chunks = chunk_text(pdf_text)

print("Generating embeddings...")
embedding_model = get_embedding_model()

vectors = embedding_model.embed_documents(
    chunks
)

client = get_qdrant_client()

try:
    client.delete_collection(
        collection_name="research_papers"
    )
except:
    pass

create_collection(client)

upload_vectors(
    client,
    "research_papers",
    chunks,
    vectors
)

question = "What optimizer was used?"

print(f"\nQuestion: {question}\n")

results = retrieve_chunks(
    client,
    "research_papers",
    question
)

for i, chunk in enumerate(results, start=1):
    print(f"\n--- Result {i} ---\n")
    print(chunk[:1000])

client.close()