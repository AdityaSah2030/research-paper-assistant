from pypdf import PdfReader


def load_pdf_pages(pdf_path: str) -> list[dict]:
    """Extract non-empty PDF pages while preserving 1-based page numbers."""
    reader = PdfReader(pdf_path)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append({
                "page_number": page_number,
                "text": text
            })

    if not pages:
        raise ValueError(
            "No extractable text was found. The PDF may be scanned or empty."
        )

    return pages


def load_pdf(pdf_path: str) -> str:
    """Backward-compatible helper returning the whole PDF as text."""
    return "\n".join(page["text"] for page in load_pdf_pages(pdf_path))
