import os
import shutil
from app.rag.vector_store import (
    get_qdrant_client,
    get_document_catalog,
    delete_session_documents,
)
from app.rag.indexer import index_pdf
from app.rag.retriever import retrieve_chunks

def run_tests():
    client = get_qdrant_client()
    session_1 = "test_sess_alpha"
    session_2 = "test_sess_beta"
    collection = "research_papers"

    print("Cleaning any existing test session points...")
    delete_session_documents(client, collection, session_1)
    delete_session_documents(client, collection, session_2)

    # 1. New session starts empty
    catalog_1 = get_document_catalog(client, collection, session_id=session_1)
    print("Catalog for fresh session 1:", catalog_1)
    assert catalog_1 == [], "Fresh session must have empty catalog!"

    # 2. Upload first PDF into session 1
    sample_pdf_1 = "data/sample_papers/attention.pdf"
    count_1 = index_pdf(client, collection, sample_pdf_1, session_id=session_1)
    print(f"Indexed {sample_pdf_1} in session 1: {count_1} chunks")
    assert count_1 > 0

    catalog_1 = get_document_catalog(client, collection, session_id=session_1)
    print("Catalog for session 1 after uploading attention.pdf:", catalog_1)
    assert len(catalog_1) == 1
    assert catalog_1[0]["file_name"] == "attention.pdf"
    assert catalog_1[0]["chunks_indexed"] == count_1

    # Verify session 2 is still completely empty
    catalog_2 = get_document_catalog(client, collection, session_id=session_2)
    print("Catalog for session 2 (should be empty):", catalog_2)
    assert catalog_2 == [], "Session 2 must be completely isolated and empty!"

    # 3. Create a second mock PDF and upload into session 1
    # We can copy attention.pdf as second_paper.pdf to test multi-PDF in the same session
    sample_pdf_2 = "data/sample_papers/second_paper.pdf"
    shutil.copyfile(sample_pdf_1, sample_pdf_2)
    try:
        count_2 = index_pdf(client, collection, sample_pdf_2, session_id=session_1)
        print(f"Indexed {sample_pdf_2} in session 1: {count_2} chunks")
        assert count_2 > 0

        catalog_1 = get_document_catalog(client, collection, session_id=session_1)
        print("Catalog for session 1 after uploading second_paper.pdf:", catalog_1)
        # Both papers must be listed!
        assert len(catalog_1) == 2, f"Expected 2 papers, got {len(catalog_1)}"
        filenames = [doc["file_name"] for doc in catalog_1]
        assert "attention.pdf" in filenames
        assert "second_paper.pdf" in filenames

        # 4. Re-upload attention.pdf in session 1 - should replace without duplicates
        count_reupload = index_pdf(client, collection, sample_pdf_1, session_id=session_1)
        catalog_after_reupload = get_document_catalog(client, collection, session_id=session_1)
        print("Catalog after re-uploading attention.pdf:", catalog_after_reupload)
        assert len(catalog_after_reupload) == 2
        for doc in catalog_after_reupload:
            if doc["file_name"] == "attention.pdf":
                assert doc["chunks_indexed"] == count_reupload, f"Expected {count_reupload}, got {doc['chunks_indexed']}"
            elif doc["file_name"] == "second_paper.pdf":
                assert doc["chunks_indexed"] == count_2

        # 5. Retrieve chunks across multiple papers in session 1
        chunks = retrieve_chunks(client, collection, "What is the Transformer architecture?", session_id=session_1)
        print(f"Retrieved {len(chunks)} chunks across papers")
        assert len(chunks) > 0
        sources_found = set(c["source"] for c in chunks)
        print(f"Sources in retrieved chunks: {sources_found}")
        for c in chunks:
            assert c["source"] in filenames
            assert c.get("page_number") is not None or c.get("page_number") is None

        # 6. Test session reset
        print("Resetting session 1...")
        delete_session_documents(client, collection, session_1)
        catalog_reset = get_document_catalog(client, collection, session_id=session_1)
        print("Catalog after reset:", catalog_reset)
        assert catalog_reset == [], "Session 1 must be empty after reset!"

        print("\nALL MULTI-SESSION TESTS PASSED SUCCESSFULLY!")
    finally:
        if os.path.exists(sample_pdf_2):
            os.remove(sample_pdf_2)
        delete_session_documents(client, collection, session_1)
        delete_session_documents(client, collection, session_2)
        client.close()

if __name__ == "__main__":
    run_tests()
