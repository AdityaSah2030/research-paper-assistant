from fastapi import FastAPI

from app.api.schemas import QuestionRequest

from app.rag.retriever import retrieve_chunks
from app.rag.vector_store import get_qdrant_client

from app.llm.gemini_client import generate_answer

from fastapi import (
    FastAPI,
    UploadFile,
    File
)

import os

from app.rag.indexer import index_pdf

app = FastAPI(
    title="Research Paper Assistant API",
    version="1.0.0"
)

COLLECTION_NAME = "research_papers"

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

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