"""
src/utils/skills.py
===================
Load the required-skills list and count how many of them appear in a
resume. This is the "keyword matching" half of the score.

WHY SKILLS COME FROM A CSV
--------------------------
Real ATS systems keep a "skills taxonomy" (a controlled list of skills)
that recruiters update. Keeping the list in data/required_skills.csv
means you can change what the tool looks for WITHOUT touching any code.

The CSV has columns: skill,category,weight
  weight 1.0 -> must-have skill
  weight 0.5 -> nice-to-have skill

MATCHING RULE
-------------
A skill counts as FOUND if it appears as a whole phrase in the resume
text (case-insensitive, after cleaning). We use word boundaries so that
looking for "SQL" does not accidentally match the "sql" inside some
other word, and looking for "Git" does not match "digit".
"""

import csv
import re


def load_skills(csv_path: str):
    """
    Return a list of dicts: [{"skill": str, "category": str, "weight": float}, ...]

    If the CSV is missing, return a small default list so the tool still
    runs (useful during development).
    """
    skills = []
    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                skills.append({
                    "skill": (row.get("skill") or "").strip().lower(),
                    "category": (row.get("category") or "").strip(),
                    "weight": float(row.get("weight") or 1.0),
                })
    except FileNotFoundError:
        print(f"  [WARN] {csv_path} not found; using tiny default skill list.")
        skills = [
            {"skill": "python", "category": "Programming", "weight": 1.0},
            {"skill": "sql", "category": "Databases", "weight": 1.0},
            {"skill": "git", "category": "Tools", "weight": 1.0},
        ]
    # Drop any blank rows
    return [s for s in skills if s["skill"]]


def find_skills_in_text(resume_text_clean: str, skills: list):
    """
    Count which skills are present in a CLEANED resume text.

    Returns
    -------
    matched   : list of skill names found
    missed    : list of skill names not found
    raw_score : sum of weights of matched skills
    max_score : sum of all weights (for normalising to 0-100)
    """
    matched, missed = [], []
    raw_score = 0.0
    max_score = 0.0

    for entry in skills:
        skill = entry["skill"]
        weight = entry["weight"]
        max_score += weight

        # \b = word boundary; re.escape so "c++" etc. is safe.
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, resume_text_clean):
            matched.append(skill)
            raw_score += weight
        else:
            missed.append(skill)

    return matched, missed, raw_score, max_score
