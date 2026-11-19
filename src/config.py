"""
src/config.py
=============
Single place for every path and tuning knob in the project.

WHY: if all settings live in one file, a beginner can change behaviour
(like the shortlist cut-off) without reading the whole code base.
"""

import os

# ----------------------------------------------------------------------
# Paths (always relative to the PROJECT ROOT, not this file)
# ----------------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RESUMES_DIR = os.path.join(ROOT, "resumes")          # input resumes (.pdf/.docx/.txt)
DATA_DIR = os.path.join(ROOT, "data")                # job description + skills
OUTPUTS_DIR = os.path.join(ROOT, "outputs")          # generated reports
IMAGES_DIR = os.path.join(ROOT, "images")            # charts / screenshots
DOCS_DIR = os.path.join(ROOT, "docs")                # guides

JOB_DESCRIPTION_FILE = os.path.join(DATA_DIR, "job_description.txt")
REQUIRED_SKILLS_FILE = os.path.join(DATA_DIR, "required_skills.csv")

OUTPUT_CSV = os.path.join(OUTPUTS_DIR, "screening_results.csv")
OUTPUT_JSON = os.path.join(OUTPUTS_DIR, "screening_results.json")
OUTPUT_MARKDOWN = os.path.join(OUTPUTS_DIR, "screening_report.md")
OUTPUT_CHART = os.path.join(OUTPUTS_DIR, "score_chart.png")

# ----------------------------------------------------------------------
# SCORING TUNING KNOBS
# ----------------------------------------------------------------------
# The final score is a weighted blend of two signals:
#   keyword_score  -> % of required skills found in the resume
#   similarity     -> TF-IDF cosine similarity between resume & job text
KEYWORD_WEIGHT = 0.60      # 60% weight to exact skill matching
SIMILARITY_WEIGHT = 0.40   # 40% weight to overall semantic similarity

# Cut-off for the shortlist. Score >= 60 -> SHORTLIST, else REJECT.
SHORTLIST_THRESHOLD = 60.0

# Resume file extensions we know how to read
SUPPORTED_EXTENSIONS = (".pdf", ".docx", ".txt")
