"""
src/reporting/report.py
=======================
Take the list of scored resumes and write:
  * outputs/screening_results.csv      -> the machine-readable table
  * outputs/screening_results.json     -> full detail (matched/missed skills)
  * outputs/screening_report.md        -> a human-readable shortlist report
  * outputs/score_chart.png            -> a bar chart (matplotlib, optional)

WHY MULTIPLE FORMATS
--------------------
CSV  -> you open it in Excel / pandas for analysis.
JSON -> other programs (or a Streamlit dashboard) can read it.
MD   -> you paste it straight into the GitHub repo as documentation.
PNG  -> a visual for the README / screenshots folder.
"""

import json
import os

import pandas as pd

from src.config import (
    OUTPUT_CSV, OUTPUT_JSON, OUTPUT_MARKDOWN, OUTPUT_CHART,
    SHORTLIST_THRESHOLD,
)


def _rank(results: list) -> list:
    """Sort results best-first and add a rank number."""
    ranked = sorted(results, key=lambda r: r["score"], reverse=True)
    for i, r in enumerate(ranked, start=1):
        r["rank"] = i
    return ranked


def save_csv(results: list) -> str:
    df = pd.DataFrame([
        {
            "rank": r["rank"],
            "resume": r["resume_name"],
            "score": r["score"],
            "keyword_score": r["keyword_score"],
            "similarity": r["similarity"],
            "decision": r["decision"],
            "matched_skills": "; ".join(r["matched_skills"]),
            "missed_skills": "; ".join(r["missed_skills"]),
        }
        for r in results
    ])
    df.to_csv(OUTPUT_CSV, index=False)
    return OUTPUT_CSV


def save_json(results: list) -> str:
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    return OUTPUT_JSON


def save_markdown(results: list, job_title: str = "Role") -> str:
    shortlisted = [r for r in results if r["decision"] == "SHORTLIST"]
    rejected = [r for r in results if r["decision"] == "REJECT"]

    lines = []
    lines.append("# Resume Screening Report\n")
    lines.append(f"**Role:** {job_title}  ")
    lines.append(f"**Shortlist threshold:** {SHORTLIST_THRESHOLD}  ")
    lines.append(f"**Resumes processed:** {len(results)}  ")
    lines.append(f"**Shortlisted:** {len(shortlisted)} | **Rejected:** {len(rejected)}\n")

    lines.append("## Ranking\n")
    lines.append("| Rank | Resume | Score | Keyword | Similarity | Decision |")
    lines.append("|---:|---|---:|---:|---:|---|")
    for r in results:
        lines.append(
            f"| {r['rank']} | {r['resume_name']} | {r['score']:.1f} "
            f"| {r['keyword_score']:.1f} | {r['similarity']:.1f} | {r['decision']} |"
        )
    lines.append("")

    lines.append("## Shortlisted candidates\n")
    if shortlisted:
        for r in shortlisted:
            lines.append(f"- **{r['resume_name']}** — score {r['score']:.1f}")
    else:
        lines.append("- _None_")
    lines.append("")

    lines.append("## Skill gaps per candidate\n")
    for r in results:
        missed = ", ".join(r["missed_skills"]) if r["missed_skills"] else "none"
        lines.append(f"- **{r['resume_name']}** — missing: {missed}")
    lines.append("")

    with open(OUTPUT_MARKDOWN, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return OUTPUT_MARKDOWN


def save_chart(results: list) -> str:
    """Bar chart of scores, coloured by decision. Skipped if matplotlib absent."""
    try:
        import matplotlib
        matplotlib.use("Agg")  # no GUI needed
        import matplotlib.pyplot as plt
    except Exception as e:
        print(f"  [WARN] matplotlib not available, skipping chart: {e}")
        return ""

    names = [r["resume_name"].replace("resume_", "").replace(".pdf", "")
             .replace(".docx", "").replace(".txt", "") for r in results]
    scores = [r["score"] for r in results]
    colors = ["#2e8b57" if r["decision"] == "SHORTLIST" else "#c0392b"
              for r in results]

    plt.figure(figsize=(10, 5))
    bars = plt.bar(names, scores, color=colors)
    plt.axhline(SHORTLIST_THRESHOLD, color="navy", linestyle="--",
                label=f"Threshold = {SHORTLIST_THRESHOLD}")
    plt.title("Resume Screening Scores")
    plt.ylabel("Score (0-100)")
    plt.xlabel("Candidate")
    plt.xticks(rotation=30, ha="right")
    plt.ylim(0, 100)
    plt.legend()

    for bar, s in zip(bars, scores):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                 f"{s:.0f}", ha="center", fontsize=9)

    plt.tight_layout()
    plt.savefig(OUTPUT_CHART, dpi=120)
    plt.close()
    return OUTPUT_CHART


def generate_reports(results: list, job_title: str = "Role") -> dict:
    """Run every report writer; return the paths that were written."""
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    ranked = _rank(results)

    paths = {
        "csv": save_csv(ranked),
        "json": save_json(ranked),
        "markdown": save_markdown(ranked, job_title),
    }
    chart = save_chart(ranked)
    if chart:
        paths["chart"] = chart
    return paths
