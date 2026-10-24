from pathlib import Path
import os
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.schemas import QuestionRequest
from app.rag.indexer import index_pdf
from app.rag.retriever import retrieve_chunks
from app.rag.vector_store import (
    get_qdrant_client,
    get_document_catalog,
    delete_session_documents,
)
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


@app.get("/documents")
def list_documents(x_session_id: str | None = Header(default=None, alias="X-Session-ID")):
    """List all currently indexed PDFs and their chunk counts for the current session."""
    try:
        return {"documents": get_document_catalog(client, COLLECTION_NAME, session_id=x_session_id)}
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Could not list indexed documents: {type(exc).__name__}: {exc}"
        ) from exc


@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    x_session_id: str | None = Header(default=None, alias="X-Session-ID")
):
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    safe_name = Path(file.filename).name
    session_dir = os.path.join(UPLOAD_DIR, x_session_id or "default")
    os.makedirs(session_dir, exist_ok=True)
    file_path = os.path.join(session_dir, safe_name)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        chunk_count = index_pdf(
            client=client,
            collection_name=COLLECTION_NAME,
            pdf_path=file_path,
            session_id=x_session_id
        )
    except Exception as exc:
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
def ask_question(
    request: QuestionRequest,
    x_session_id: str | None = Header(default=None, alias="X-Session-ID")
):
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Please enter a question.")

    try:
        retrieved_chunks = retrieve_chunks(
            client,
            COLLECTION_NAME,
            question,
            session_id=x_session_id
        )

        if not retrieved_chunks:
            return {
                "question": question,
                "answer": "The provided research paper does not contain enough information to answer this question.",
                "sources": []
            }

        context_parts = []
        for chunk in retrieved_chunks:
            page_number = chunk.get("page_number")
            page_label = f"Page {page_number}" if page_number is not None else "Page number unavailable"
            context_parts.append(
                f"[Source: {chunk['source']} | {page_label} | "
                f"Chunk {chunk.get('chunk_id', 'unknown')}]\n{chunk['text']}"
            )

        answer = generate_answer(
            question,
            "\n\n".join(context_parts)
        )

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
        raise HTTPException(
            status_code=502,
            detail=f"Question answering failed: {type(exc).__name__}: {exc}"
        ) from exc


@app.post("/session/reset")
def reset_session(x_session_id: str | None = Header(default=None, alias="X-Session-ID")):
    """Reset the current browser session by deleting its indexed vectors and uploaded files."""
    if x_session_id:
        try:
            delete_session_documents(client, COLLECTION_NAME, x_session_id)
            session_dir = os.path.join(UPLOAD_DIR, x_session_id)
            if os.path.exists(session_dir):
                shutil.rmtree(session_dir, ignore_errors=True)
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Could not reset session: {type(exc).__name__}: {exc}"
            ) from exc
    return {"message": "Session reset successfully"}
