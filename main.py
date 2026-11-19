#!/usr/bin/env python3
"""
=====================================================================
 Automated Resume Screening Tool  -  main.py
=====================================================================
 A beginner-friendly, fully offline simulation of an ATS resume screen.

 WORKFLOW
 --------
   resumes/ + job description  ->  extract text  ->  clean text
        ->  match required skills  ->  TF-IDF cosine similarity
        ->  weighted score (0-100)  ->  SHORTLIST / REJECT decision
        ->  ranked CSV / JSON / Markdown report + chart

 HOW TO RUN
 ----------
    python main.py
    python main.py --resumes resumes --jd data/job_description.txt
    python main.py --threshold 70          # change the cut-off
    python main.py --no-chart              # skip the PNG chart

 The tool is MODULAR: each step lives in src/. Read the docstrings
 there to learn what each part does.
======================================================================
"""

import argparse
import glob
import os
import sys

# Make `src` importable no matter where you run the script from.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import (  # noqa: E402
    JOB_DESCRIPTION_FILE,
    REQUIRED_SKILLS_FILE,
    RESUMES_DIR,
    SHORTLIST_THRESHOLD,
)
from src.extractors import extract_text  # noqa: E402
from src.utils.skills import load_skills  # noqa: E402
from src.core.scoring import score_resume  # noqa: E402
from src.reporting.report import generate_reports  # noqa: E402


def load_job_description(path: str) -> str:
    """Read the job description text file."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def discover_resumes(directory: str) -> list:
    """Return a sorted list of supported resume files in `directory`."""
    files = []
    for ext in (".pdf", ".docx", ".txt"):
        files.extend(glob.glob(os.path.join(directory, "*" + ext)))
    return sorted(files)


def parse_args():
    p = argparse.ArgumentParser(
        description="Screen resumes against a job description."
    )
    p.add_argument("--resumes", default=RESUMES_DIR,
                   help="folder with resume .pdf/.docx/.txt files")
    p.add_argument("--jd", default=JOB_DESCRIPTION_FILE,
                   help="job description .txt file")
    p.add_argument("--skills", default=REQUIRED_SKILLS_FILE,
                   help="CSV of required skills (skill,category,weight)")
    p.add_argument("--threshold", type=float, default=SHORTLIST_THRESHOLD,
                   help="score needed to shortlist (default 60)")
    p.add_argument("--no-chart", action="store_true",
                   help="skip generating the PNG chart")
    return p.parse_args()


def main():
    args = parse_args()

    print("=" * 65)
    print("  AUTOMATED RESUME SCREENING TOOL  (student project)")
    print("=" * 65)

    # ---- 0) inputs ----------------------------------------------------
    if not os.path.isdir(args.resumes):
        print(f"[ERROR] Resumes folder not found: {args.resumes}")
        print("        Put .pdf/.docx/.txt resumes there, or run:")
        print("        python scripts/generate_sample_data.py")
        return 1

    if not os.path.isfile(args.jd):
        print(f"[ERROR] Job description not found: {args.jd}")
        return 1

    job_text = load_job_description(args.jd)
    skills = load_skills(args.skills)

    # Let --threshold override the config value.
    import src.config as cfg
    cfg.SHORTLIST_THRESHOLD = args.threshold

    print(f"\n[1] Loaded job description : {args.jd}")
    print(f"[2] Loaded required skills : {len(skills)} keywords")
    print(f"[3] Shortlist threshold    : {args.threshold}")

    # ---- 1) find resumes ----------------------------------------------
    resume_files = discover_resumes(args.resumes)
    if not resume_files:
        print(f"[ERROR] No resumes found in {args.resumes}")
        return 1
    print(f"[4] Found resumes          : {len(resume_files)}\n")

    # ---- 2) screen each resume ----------------------------------------
    results = []
    for path in resume_files:
        name = os.path.basename(path)
        raw = extract_text(path)

        # Empty text usually means a scanned PDF - keep it but score 0.
        if not raw.strip():
            print(f"  [!] {name}: no text extracted -> score 0")
            results.append({
                "resume_name": name,
                "score": 0.0, "keyword_score": 0.0, "similarity": 0.0,
                "matched_skills": [], "missed_skills": [s["skill"] for s in skills],
                "decision": "REJECT",
            })
            continue

        res = score_resume(raw, job_text, skills)
        res["resume_name"] = name
        results.append(res)

        print(f"  {name}")
        print(f"     score={res['score']:.1f}  "
              f"(keyword {res['keyword_score']:.1f} + similarity {res['similarity']:.1f})  "
              f"-> {res['decision']}")
        print(f"     matched {len(res['matched_skills'])} skills, "
              f"missed {len(res['missed_skills'])}")

    if not results:
        print("[ERROR] Nothing to score.")
        return 1

    # ---- 3) reports ----------------------------------------------------
    print("\n[5] Generating reports ...")
    if args.no_chart:
        import src.reporting.report as rep
        rep.save_chart = lambda r: ""
    paths = generate_reports(results, job_title="Junior Python Developer")

    for kind, p in paths.items():
        print(f"  - {kind}: {p}")

    # ---- 4) final shortlist -------------------------------------------
    shortlisted = [r for r in results if r["decision"] == "SHORTLIST"]
    print("\n" + "=" * 65)
    print(f"  SHORTLISTED: {len(shortlisted)} / {len(results)} candidates")
    for r in sorted(results, key=lambda x: x["score"], reverse=True):
        if r["decision"] == "SHORTLIST":
            print(f"    {r['score']:5.1f}  {r['resume_name']}")
    print("=" * 65)
    print("Done. Open outputs/screening_results.csv to explore the data.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
