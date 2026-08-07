from app.rag.loader import load_pdf
from app.rag.chunker import chunk_text
from app.rag.embeddings import get_embedding_model

from app.rag.vector_store import (
    create_collection,
    upload_vectors
)

import os


def index_pdf(
    client,
    collection_name,
    pdf_path
):
    pdf_text = load_pdf(pdf_path)

    chunks = chunk_text(pdf_text)

    embedding_model = get_embedding_model()

    vectors = embedding_model.embed_documents(
        chunks
    )

    try:
        client.delete_collection(
            collection_name=collection_name
        )
    except:
        pass

    create_collection(
        client,
        collection_name=collection_name,
        vector_size=3072
    )

    upload_vectors(
        client,
        collection_name,
        chunks,
        vectors,
        source_file=os.path.basename(
            pdf_path
        )
    )

    return len(chunks)