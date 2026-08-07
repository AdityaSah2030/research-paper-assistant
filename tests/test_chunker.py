from app.rag.loader import load_pdf
from app.rag.chunker import chunk_text


pdf_text = load_pdf(
    "data/sample_papers/attention.pdf"
)

chunks = chunk_text(pdf_text)

print(f"Total Chunks: {len(chunks)}")

print("\n" + "=" * 50)
print("FIRST CHUNK")
print("=" * 50)

print(chunks[0])

print("\n" + "=" * 50)
print("LAST CHUNK")
print("=" * 50)

print(chunks[-1])