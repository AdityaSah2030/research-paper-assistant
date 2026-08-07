from fastapi import (
    FastAPI,
    UploadFile,
    File
)

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import os

from app.api.schemas import QuestionRequest

from app.rag.indexer import index_pdf
from app.rag.retriever import retrieve_chunks
from app.rag.vector_store import get_qdrant_client

from app.llm.gemini_client import generate_answer


app = FastAPI(
    title="Research Paper Assistant API",
    version="1.0.0"
)

app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)

COLLECTION_NAME = "research_papers"

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

client = get_qdrant_client()


# =========================
# FRONTEND
# =========================

@app.get("/")
def frontend():
    return FileResponse(
        "frontend/index.html"
    )


# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =========================
# UPLOAD PDF
# =========================

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(
            await file.read()
        )

    chunk_count = index_pdf(
        client,
        COLLECTION_NAME,
        file_path
    )

    return {
        "message": "PDF uploaded successfully",
        "file_name": file.filename,
        "chunks_indexed": chunk_count
    }


# =========================
# ASK QUESTION
# =========================

@app.post("/ask")
def ask_question(
    request: QuestionRequest
):

    retrieved_chunks = retrieve_chunks(
        client,
        COLLECTION_NAME,
        request.question
    )

    if not retrieved_chunks:
        return {
            "question": request.question,
            "answer": "The provided research paper does not contain enough information to answer this question.",
            "sources": []
        }

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