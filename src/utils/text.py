"""
src/utils/text.py
=================
Small text helpers. Every resume and every job description passes through
clean_text() BEFORE matching, so the matcher is not confused by messy
characters, weird spacing, or upper/lower case.

WHAT "CLEANING" MEANS HERE
--------------------------
1. Replace non-breaking spaces and tabs with a normal space.
2. Collapse many spaces / newlines into ONE space.
3. Lower-case everything (so "Python" == "python").
4. Keep letters, digits, spaces and a few safe symbols.
   (We do NOT strip punctuation inside words like "c++" style skills,
    but for this beginner project we keep it simple and safe.)
"""

import re


def clean_text(text: str) -> str:
    """Return a normalised, lower-cased, single-spaced version of text."""
    if not text:
        return ""

    # 1) common invisible characters -> space
    text = text.replace(" ", " ").replace("\t", " ").replace("\r", " ")

    # 2) lower case
    text = text.lower()

    # 3) keep only letters, digits, spaces and a small safe set of symbols
    #    ( + . # - are common in skills like "c++", ".net", "c#", "3d")
    text = re.sub(r"[^a-z0-9\+\.\#\-\s]", " ", text)

    # 4) collapse any run of whitespace into a single space
    text = re.sub(r"\s+", " ", text).strip()

    return text


def tokenize(text: str) -> list:
    """Split cleaned text into a list of words (tokens)."""
    return [tok for tok in text.split(" ") if tok]


if __name__ == "__main__":
    sample = "Hello, WORLD!   I love  Python 3.11 & C++...\n\nLet's go."
    print("raw     :", repr(sample))
    print("cleaned :", repr(clean_text(sample)))
    print("tokens  :", tokenize(clean_text(sample)))
