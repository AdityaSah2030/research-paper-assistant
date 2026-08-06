from app.rag.loader import load_pdf
from app.rag.chunker import chunk_text
from app.rag.embeddings import get_embedding_model

from app.rag.vector_store import (
    get_qdrant_client,
    create_collection,
    upload_vectors
)

from app.rag.retriever import retrieve_chunks

from app.llm.gemini_client import generate_answer


pdf_text = load_pdf(
    "data/sample_papers/attention.pdf"
)

chunks = chunk_text(pdf_text)

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

question = """
What optimizer was used?
Give all hyperparameters and learning rate details.
"""

retrieved_chunks = retrieve_chunks(
    client,
    "research_papers",
    question
)

context = "\n\n".join(
    retrieved_chunks
)

answer = generate_answer(
    question,
    context
)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(answer)

client.close()