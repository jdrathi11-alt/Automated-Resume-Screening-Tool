"""
src/extractors/docx.py
======================
Extract text from a .docx resume using python-docx.

We read BOTH paragraphs AND table cells, because some resume templates
put content inside tables (which paragraphs alone would miss).
"""

def extract_docx(path: str) -> str:
    try:
        from docx import Document

        doc = Document(path)

        parts = [p.text for p in doc.paragraphs]

        # Tables are common in resume templates - do not miss them.
        for table in getattr(doc, "tables", []):
            for row in table.rows:
                for cell in row.cells:
                    parts.append(cell.text)

        return "\n".join(parts).strip()

    except Exception as e:
        print(f"  [WARN] python-docx failed on {path}: {e}")
        return ""
