"""
src/utils/similarity.py
=======================
Compute the cosine similarity between a resume and the job description.

TWO BACKENDS, ONE FUNCTION
--------------------------
- If scikit-learn is installed we use its TfidfVectorizer (fast, standard).
- If not, we fall back to a tiny hand-written TF-IDF + cosine using NumPy.

Both return a number between 0.0 (nothing in common) and 1.0 (identical).
This keeps the project runnable on ANY machine, even one without sklearn.
"""

import math
import re

import numpy as np


# ----------------------------------------------------------------------
# Hand-written TF-IDF (used only if scikit-learn is unavailable)
# ----------------------------------------------------------------------
def _tokenize(text: str):
    return re.findall(r"[a-z0-9\+\.#]+", text.lower())


def _tfidf_vectors(docs):
    """Return a list of TF-IDF vectors (as dicts: term -> weight)."""
    n_docs = len(docs)
    doc_tokens = [_tokenize(d) for d in docs]

    # document frequency
    df = {}
    for tokens in doc_tokens:
        for term in set(tokens):
            df[term] = df.get(term, 0) + 1

    # idf = log( (1 + N) / (1 + df) ) + 1   (sklearn's smooth formula)
    idf = {t: math.log((1 + n_docs) / (1 + c)) + 1 for t, c in df.items()}

    vectors = []
    for tokens in doc_tokens:
        tf = {}
        for t in tokens:
            tf[t] = tf.get(t, 0) + 1
        # raw term frequency * idf
        vec = {t: f * idf[t] for t, f in tf.items()}
        vectors.append(vec)
    return vectors


def _cosine_dict(v1, v2):
    """Cosine similarity between two sparse vectors (dicts)."""
    common = set(v1) & set(v2)
    if not common:
        return 0.0
    dot = sum(v1[t] * v2[t] for t in common)
    norm1 = math.sqrt(sum(x * x for x in v1.values()))
    norm2 = math.sqrt(sum(x * x for x in v2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def cosine_similarity_tfidf(text_a: str, text_b: str) -> float:
    """
    Cosine similarity of two documents using TF-IDF.

    Tries scikit-learn first; if unavailable, uses the built-in NumPy
    implementation above. Returns a float in [0, 1].
    """
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer

        vec = TfidfVectorizer().fit_transform([text_a, text_b])
        sim = (vec[0] * vec[1].T).toarray()[0][0]
        return float(sim)
    except Exception:
        va, vb = _tfidf_vectors([text_a, text_b])
        return float(_cosine_dict(va, vb))


if __name__ == "__main__":
    a = "python pandas numpy sql data cleaning machine learning"
    b = "i love python and pandas for data cleaning and machine learning"
    c = "marketing social media content writing campaigns"
    print("similar(a,b) =", round(cosine_similarity_tfidf(a, b), 3))
    print("similar(a,c) =", round(cosine_similarity_tfidf(a, c), 3))
