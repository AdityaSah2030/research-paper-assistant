from app.rag.loader import load_pdf

pdf_text = load_pdf(
    "data/sample_papers/attention.pdf"
)

print(f"Characters extracted: {len(pdf_text)}")
print()
print(pdf_text[:1000])