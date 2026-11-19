"""
src/extractors/text.py
======================
Read a plain-text (.txt) resume. Kept as its own module so the folder
layout is symmetric and a beginner can see where each format is handled.
"""

def extract_txt(path: str) -> str:
    # utf-8 + errors="ignore" so a weird character never crashes the run.
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip()
    except Exception as e:
        print(f"  [WARN] Could not read {path}: {e}")
        return ""
