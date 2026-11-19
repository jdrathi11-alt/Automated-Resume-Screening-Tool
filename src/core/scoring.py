"""
src/core/scoring.py
===================
The brain of the tool: turns a resume + job description into a SCORE.

HOW THE SCORE WORKS (0 - 100)
-----------------------------
score = KEYWORD_WEIGHT * keyword_score  +  SIMILARITY_WEIGHT * similarity_score

  keyword_score    = (sum of weights of skills found / sum of all weights) * 100
                     -> "Did the resume contain the required keywords?"
  similarity_score = cosine_similarity(TF-IDF(resume), TF-IDF(job_desc)) * 100
                     -> "Does the resume 'talk about' the same things as
                        the job description, even with different wording?"

Blending BOTH is better than keywords alone:
  - keywords catch exact skill names ("pandas", "SQL"),
  - TF-IDF cosine catches related wording ("automated reporting" ~ "automation").

The weights live in src/config.py so you can tune them.

DECISION RULE
-------------
  score >= SHORTLIST_THRESHOLD  ->  SHORTLIST
  otherwise                     ->  REJECT
"""

from src.config import KEYWORD_WEIGHT, SIMILARITY_WEIGHT, SHORTLIST_THRESHOLD
from src.utils.skills import find_skills_in_text
from src.utils.similarity import cosine_similarity_tfidf


def score_resume(resume_text: str, job_text: str, skills: list) -> dict:
    """
    Score ONE resume against the job description.

    Parameters
    ----------
    resume_text : str   (already extracted, NOT yet cleaned)
    job_text    : str   (job description text)
    skills      : list  (from load_skills)

    Returns
    -------
    dict with keys:
        matched_skills, missed_skills, keyword_score,
        similarity, score, decision
    """
    # --- 1) clean both texts (same rules for both) --------------------
    from src.utils.text import clean_text

    resume_clean = clean_text(resume_text)
    job_clean = clean_text(job_text)

    # --- 2) keyword matching -----------------------------------------
    matched, missed, raw, maxw = find_skills_in_text(resume_clean, skills)
    keyword_score = (raw / maxw * 100) if maxw > 0 else 0.0

    # --- 3) semantic similarity --------------------------------------
    # If the resume is empty, similarity is 0 (avoid div-by-zero weirdness).
    if resume_clean.strip() and job_clean.strip():
        similarity = cosine_similarity_tfidf(resume_clean, job_clean) * 100.0
    else:
        similarity = 0.0

    # --- 4) blend -----------------------------------------------------
    score = KEYWORD_WEIGHT * keyword_score + SIMILARITY_WEIGHT * similarity

    # --- 5) decision --------------------------------------------------
    decision = "SHORTLIST" if score >= SHORTLIST_THRESHOLD else "REJECT"

    return {
        "matched_skills": matched,
        "missed_skills": missed,
        "keyword_score": round(keyword_score, 2),
        "similarity": round(similarity, 2),
        "score": round(score, 2),
        "decision": decision,
    }
