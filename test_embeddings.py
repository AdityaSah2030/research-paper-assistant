from app.rag.loader import load_pdf
from app.rag.chunker import chunk_text
from app.rag.embeddings import get_embedding_model

print("Loading PDF...")
pdf_text = load_pdf(
    "data/sample_papers/attention.pdf"
)

print("Chunking...")
chunks = chunk_text(pdf_text)

print(f"Chunks: {len(chunks)}")

embedding_model = get_embedding_model()

print("Creating embeddings for all chunks...")

vectors = embedding_model.embed_documents(
    chunks
)

print(f"Total vectors: {len(vectors)}")
print(f"Vector dimension: {len(vectors[0])}")