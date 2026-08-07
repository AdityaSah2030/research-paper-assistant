from fastapi import FastAPI

from app.api.schemas import QuestionRequest

from app.rag.retriever import retrieve_chunks
from app.rag.vector_store import get_qdrant_client

from app.llm.gemini_client import generate_answer

app = FastAPI(
    title="Research Paper Assistant API",
    version="1.0.0"
)

COLLECTION_NAME = "research_papers"

client = get_qdrant_client()

@app.get("/")
def root():
    return {
        "message": "Research Paper Assistant API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    retrieved_chunks = retrieve_chunks(
        client,
        COLLECTION_NAME,
        request.question
    )

    context = "\n\n".join(
        chunk["text"]
        for chunk in retrieved_chunks
    )

    answer = generate_answer(
        request.question,
        context
    )

    return {
        "question": request.question,
        "answer": answer,
        "sources": [
            {
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"]
            }
            for chunk in retrieved_chunks
        ]
    }