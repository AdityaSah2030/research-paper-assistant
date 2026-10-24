import os
import uuid

from app.rag.loader import load_pdf_pages
from app.rag.chunker import chunk_text
from app.rag.embeddings import get_embedding_model
from app.rag.vector_store import (
    create_collection,
    upload_vectors,
    delete_other_versions_of_document,
)


def index_pdf(client, collection_name, pdf_path):
    """
    Index a PDF page-by-page. Existing documents are preserved.
    Re-uploading a filename replaces only that filename's older vectors.
    """
    pages = load_pdf_pages(pdf_path)

    chunks = []
    chunk_metadata = []

    for page in pages:
        for chunk in chunk_text(page["text"]):
            chunks.append(chunk)
            chunk_metadata.append({"page_number": page["page_number"]})

    if not chunks:
        raise ValueError("No text chunks could be created from this PDF.")

    embedding_model = get_embedding_model()
    vectors = embedding_model.embed_documents(chunks)

    if not vectors:
        raise ValueError("The embedding model returned no vectors.")

    create_collection(
        client,
        collection_name=collection_name,
        vector_size=len(vectors[0])
    )

    source_file = os.path.basename(pdf_path)
    document_id = str(uuid.uuid4())

    # Add the new version first. Only after successful upsert do we remove
    # older vectors for this same filename; other papers remain untouched.
    saved_document_id = upload_vectors(
        client=client,
        collection_name=collection_name,
        chunks=chunks,
        vectors=vectors,
        source_file=source_file,
        chunk_metadata=chunk_metadata,
        document_id=document_id
    )

    delete_other_versions_of_document(
        client,
        collection_name,
        source_file,
        saved_document_id
    )

    return len(chunks)
