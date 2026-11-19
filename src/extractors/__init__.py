"""Extractors: turn resume FILES into plain text.

Supported formats
-----------------
.pdf  -> pypdf (preferred) or pdfplumber (fallback)
.docx -> python-docx
.txt  -> plain read

Every extractor returns a STRING. If a file cannot be read we return an
empty string and log a warning, so one bad file never kills the run.
"""

from .pdf import extract_pdf
from .docx import extract_docx
from .text import extract_txt


def extract_text(filepath: str) -> str:
    """Read any supported resume file and return its text."""
    import os

    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        return extract_pdf(filepath)
    if ext == ".docx":
        return extract_docx(filepath)
    if ext == ".txt":
        return extract_txt(filepath)

    print(f"  [WARN] Unsupported file type: {filepath}")
    return ""
