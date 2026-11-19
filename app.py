"""
app.py  -  optional Streamlit dashboard
=======================================
A friendly web UI for the same engine in src/.

RUN IT:
    pip install streamlit
    streamlit run app.py

Then open the local URL it prints (usually http://localhost:8501).

WHAT YOU CAN DO HERE
--------------------
1. Pick the job description (.txt) file.
2. Pick the folder holding resumes (.pdf/.docx/.txt).
3. Adjust the shortlist threshold with a slider.
4. Click "Run screening" and see:
     - a ranked table of every candidate
     - the shortlist vs reject split
     - a bar chart of scores
     - which skills each candidate is missing

This is OPTIONAL - main.py does the same work from the terminal.
"""

import os
import sys

# Make src importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st  # noqa: E402

from src.config import (  # noqa: E402
    JOB_DESCRIPTION_FILE, REQUIRED_SKILLS_FILE, RESUMES_DIR,
    SHORTLIST_THRESHOLD,
)
from src.core.scoring import score_resume  # noqa: E402
from src.extractors import extract_text  # noqa: E402
from src.reporting.report import generate_reports  # noqa: E402
from src.utils.skills import load_skills  # noqa: E402

st.set_page_config(page_title="Resume Screening Tool", page_icon="🗂️")

st.title("🗂️ Automated Resume Screening Tool")
st.caption("A student project that simulates an ATS resume screen, fully offline.")

st.sidebar.header("Inputs")

jd_path = st.sidebar.text_input("Job description file", value=JOB_DESCRIPTION_FILE)
resumes_dir = st.sidebar.text_input("Resumes folder", value=RESUMES_DIR)
skills_path = st.sidebar.text_input("Skills CSV", value=REQUIRED_SKILLS_FILE)
threshold = st.sidebar.slider("Shortlist threshold", 0.0, 100.0,
                              SHORTLIST_THRESHOLD, 5.0)

run = st.sidebar.button("Run screening")


def load_jd(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def discover(directory):
    files = []
    for ext in (".pdf", ".docx", ".txt"):
        files.extend(
            os.path.join(directory, f)
            for f in os.listdir(directory) if f.lower().endswith(ext)
        )
    return sorted(files)


if run:
    if not os.path.isdir(resumes_dir):
        st.error(f"Resumes folder not found: {resumes_dir}")
    elif not os.path.isfile(jd_path):
        st.error(f"Job description not found: {jd_path}")
    else:
        import src.config as cfg
        cfg.SHORTLIST_THRESHOLD = threshold

        job_text = load_jd(jd_path)
        skills = load_skills(skills_path)
        resume_files = discover(resumes_dir)

        if not resume_files:
            st.warning("No resumes found in that folder.")
        else:
            with st.spinner("Screening resumes..."):
                results = []
                for path in resume_files:
                    raw = extract_text(path)
                    name = os.path.basename(path)
                    if not raw.strip():
                        results.append({
                            "resume_name": name, "score": 0.0,
                            "keyword_score": 0.0, "similarity": 0.0,
                            "matched_skills": [], "missed_skills": [s["skill"] for s in skills],
                            "decision": "REJECT",
                        })
                        continue
                    r = score_resume(raw, job_text, skills)
                    r["resume_name"] = name
                    results.append(r)

                results.sort(key=lambda r: r["score"], reverse=True)
                for i, r in enumerate(results, 1):
                    r["rank"] = i

            shortlisted = [r for r in results if r["decision"] == "SHORTLIST"]
            rejected = [r for r in results if r["decision"] == "REJECT"]

            st.success(
                f"**{len(shortlisted)}** of {len(results)} candidates shortlisted "
                f"(threshold = {threshold})."
            )

            st.subheader("Ranking")
            st.dataframe([
                {
                    "Rank": r["rank"],
                    "Resume": r["resume_name"],
                    "Score": round(r["score"], 1),
                    "Keyword %": round(r["keyword_score"], 1),
                    "Similarity %": round(r["similarity"], 1),
                    "Decision": r["decision"],
                }
                for r in results
            ], use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### ✅ Shortlisted")
                for r in shortlisted:
                    st.write(f"**{r['resume_name']}** — {r['score']:.1f}")
            with col2:
                st.markdown("#### ❌ Rejected")
                for r in rejected:
                    st.write(f"{r['resume_name']} — {r['score']:.1f}")

            st.subheader("Score chart")
            chart_path = generate_reports(results, job_title="Screening run")["chart"]
            if chart_path and os.path.exists(chart_path):
                st.image(chart_path, use_container_width=True)

            st.subheader("Skill gaps")
            for r in results:
                missed = ", ".join(r["missed_skills"]) if r["missed_skills"] else "none"
                st.markdown(f"**{r['resume_name']}** — missing: {missed}")

            st.caption("Reports were also written to outputs/ (CSV, JSON, Markdown).")
