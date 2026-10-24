from pypdf import PdfReader


def load_pdf_pages(pdf_path: str) -> list[dict]:
    """
    Extract text page by page so chunks can retain accurate page numbers.
    Page numbers are 1-based, matching the PDF viewer.
    """
    reader = PdfReader(pdf_path)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        extracted_text = page.extract_text() or ""
        if extracted_text.strip():
            pages.append({
                "page_number": page_number,
                "text": extracted_text
            })

    if not pages:
        raise ValueError("No extractable text found in this PDF.")

    return pages


def load_pdf(pdf_path: str) -> str:
    """Load a PDF and return all extracted text (backward-compatible helper)."""
    return "\n".join(page["text"] for page in load_pdf_pages(pdf_path))
