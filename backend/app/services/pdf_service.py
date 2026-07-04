"""
pdf_service.py
--------------
Two jobs:
1. Pull the text out of a PDF, page by page.
2. Cut that text into small overlapping "chunks" that are easier for
   an AI model to search through and reason about.
"""

import fitz  # this is PyMuPDF, imported under the name "fitz"


def extract_text_by_page(filepath: str) -> list[dict]:
    """
    Returns a list like:
    [{"page": 1, "text": "..."}, {"page": 2, "text": "..."}, ...]
    """
    pages = []
    doc = fitz.open(filepath)
    for page_number, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        if text:
            pages.append({"page": page_number, "text": text})
    doc.close()
    return pages


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> list[str]:
    """
    Splits a long string into overlapping chunks.

    Why overlap? If we cut a sentence exactly in half between two chunks,
    we might lose meaning. A little overlap means important context is
    less likely to get cut off awkwardly.

    chunk_size and overlap are measured in characters here (simple and
    good enough for a learning project; production systems often chunk
    by tokens instead).
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def process_pdf_into_chunks(filepath: str) -> list[dict]:
    """
    Combines the two functions above: extract text per page, then chunk
    each page's text. Returns a flat list of chunks, each tagged with
    the page number it came from.
    """
    pages = extract_text_by_page(filepath)
    all_chunks = []

    for page in pages:
        page_chunks = chunk_text(page["text"])
        for chunk in page_chunks:
            all_chunks.append({"page": page["page"], "content": chunk})

    return all_chunks
