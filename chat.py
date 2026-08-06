from app.rag.retriever import retrieve_chunks
from app.rag.vector_store import get_qdrant_client

from app.llm.gemini_client import generate_answer

COLLECTION_NAME = "research_papers"

client = get_qdrant_client()

while True:

    question = input("\nAsk a question: ")

    if question.lower() in [
        "exit",
        "quit",
        "q",
        "/q"
    ]:
        break
    
    retrieved_chunks = retrieve_chunks(
        client,
        COLLECTION_NAME,
        question
    )

    context = "\n\n".join(
        chunk["text"]
        for chunk in retrieved_chunks
    )

    answer = generate_answer(
        question,
        context
    )

    print("\nAnswer:")
    print(answer)

    print("\nSources:")

    for chunk in retrieved_chunks:
        print(
            f"- {chunk['source']} "
            f"(Chunk #{chunk['chunk_id']})"
        )

client.close()