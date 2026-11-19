"""
src/extractors/pdf.py
=====================
Extract text from a PDF resume.

STRATEGY (two fallbacks, because PDFs are messy in the real world):
  1. Try pypdf            -> fast, works for most text PDFs.
  2. If that fails/empty  -> try pdfplumber (handles tables better).
  3. If still empty       -> return "" and warn (file may be a scan).

NOTE: a SCANNED PDF is an image, not text. Real ATS tools add OCR
(Tesseract) for those. That is listed as a stretch goal in the README.
"""

def extract_pdf(path: str) -> str:
    text = ""

    # ---- Attempt 1: pypdf -------------------------------------------------
    try:
        from pypdf import PdfReader

        reader = PdfReader(path)
        pages = []
        for page in reader.pages:
            try:
                pages.append(page.extract_text() or "")
            except Exception:
                pages.append("")
        text = "\n".join(pages).strip()
    except Exception as e:  # pragma: no cover - defensive
        print(f"  [WARN] pypdf failed on {path}: {e}")

    # ---- Attempt 2: pdfplumber fallback -----------------------------------
    if not text:
        try:
            import pdfplumber

            with pdfplumber.open(path) as pdf:
                text = "\n".join((p.extract_text() or "") for p in pdf.pages).strip()
        except Exception as e:  # pragma: no cover - defensive
            print(f"  [WARN] pdfplumber failed on {path}: {e}")

    if not text:
        print(f"  [WARN] No text extracted from {path} (scanned PDF?)")

    return text
