import os
import uuid

from app.rag.loader import load_pdf_pages
from app.rag.chunker import chunk_text
from app.rag.embeddings import get_embedding_model
from app.rag.vector_store import create_collection, upload_vectors


def index_pdf(client, collection_name, pdf_path):
    """
    Index a PDF without deleting existing documents from the collection.
    Each chunk retains the page number from which it was extracted.
    """
    pages = load_pdf_pages(pdf_path)

    chunks = []
    chunk_metadata = []

    for page in pages:
        page_chunks = chunk_text(page["text"])
        for chunk in page_chunks:
            chunks.append(chunk)
            chunk_metadata.append({
                "page_number": page["page_number"]
            })

    if not chunks:
        raise ValueError("No text chunks could be created from this PDF.")

    embedding_model = get_embedding_model()
    vectors = embedding_model.embed_documents(chunks)

    # Ensure the shared collection exists; never delete it during upload.
    create_collection(
        client,
        collection_name=collection_name,
        vector_size=len(vectors[0])
    )

    document_id = str(uuid.uuid4())
    upload_vectors(
        client,
        collection_name,
        chunks,
        vectors,
        source_file=os.path.basename(pdf_path),
        chunk_metadata=chunk_metadata,
        document_id=document_id
    )

    return len(chunks)
