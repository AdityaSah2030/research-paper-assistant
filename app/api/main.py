from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import os
import shutil
from pathlib import Path

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
os.makedirs(UPLOAD_DIR, exist_ok=True)

client = get_qdrant_client()


@app.get("/")
def frontend():
    return FileResponse("frontend/index.html")


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    # Avoid path traversal and preserve only the supplied filename.
    safe_name = Path(file.filename).name
    file_path = os.path.join(UPLOAD_DIR, safe_name)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        chunk_count = index_pdf(client, COLLECTION_NAME, file_path)
    except Exception as exc:
        # Keep the detail useful to the client without exposing secrets.
        raise HTTPException(
            status_code=500,
            detail=f"Could not index PDF: {type(exc).__name__}: {exc}"
        ) from exc
    finally:
        await file.close()

    return {
        "message": "PDF uploaded successfully",
        "file_name": safe_name,
        "chunks_indexed": chunk_count
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Please enter a question.")

    try:
        retrieved_chunks = retrieve_chunks(
            client,
            COLLECTION_NAME,
            question
        )

        if not retrieved_chunks:
            return {
                "question": question,
                "answer": "The provided research paper does not contain enough information to answer this question.",
                "sources": []
            }

        context_parts = []
        for chunk in retrieved_chunks:
            page = chunk.get("page_number")
            page_label = f"Page {page}" if page is not None else "Page unknown"
            context_parts.append(
                f"[Source: {chunk['source']} | {page_label} | "
                f"Chunk {chunk.get('chunk_id', 'unknown')}]\n{chunk['text']}"
            )

        context = "\n\n".join(context_parts)
        answer = generate_answer(question, context)

        sources = [
            {
                "source": chunk["source"],
                "document_id": chunk.get("document_id"),
                "chunk_id": chunk.get("chunk_id"),
                "page_number": chunk.get("page_number"),
                "score": chunk.get("score")
            }
            for chunk in retrieved_chunks
        ]

        return {
            "question": question,
            "answer": answer,
            "sources": sources
        }
    except Exception as exc:
        # Avoid a silent generic error; the frontend can show this detail.
        raise HTTPException(
            status_code=502,
            detail=f"Question answering failed: {type(exc).__name__}: {exc}"
        ) from exc
