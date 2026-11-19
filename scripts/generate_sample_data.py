#!/usr/bin/env python3
"""
=====================================================================
 scripts/generate_sample_data.py
=====================================================================
 Generates the SAMPLE DATA used by the Automated Resume Screening Tool.

 WHY THIS EXISTS
 ---------------
 You do not need real resumes (and you should NOT use real people's
 resumes for privacy reasons). This script creates:

   1. 8 synthetic resumes as .pdf files   -> resumes/
   2. 1 synthetic resume as .docx         -> resumes/ (DOCX support demo)
   3. 1 plain-text job description        -> data/job_description.txt
   4. 1 required-skills CSV               -> data/required_skills.csv

 The resumes are intentionally written so that some candidates match the
 job description well (they should be shortlisted) and some match poorly
 (they should be rejected). This makes the demo predictable.

 HOW TO RUN
----------
    python scripts/generate_sample_data.py

 You only need to run this ONCE. The files it creates are committed to
 the repo so other people can run your tool without generating data.
======================================================================
"""

import os

# ---- Paths are always resolved relative to the PROJECT ROOT ----------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESUMES_DIR = os.path.join(ROOT, "resumes")
DATA_DIR = os.path.join(ROOT, "data")

os.makedirs(RESUMES_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)


# ---------------------------------------------------------------------
# 1. JOB DESCRIPTION + REQUIRED SKILLS
# ---------------------------------------------------------------------
# This is the role we are "hiring" for. The screening tool compares every
# resume against this text.

JOB_DESCRIPTION = """\
Job Title: Junior Python Developer (Data & Automation Team)
Location: Hyderabad / Remote
Experience: 0-2 years

About the role
We are looking for a Junior Python Developer to join our Data &
Automation team. You will build internal tools, clean datasets, and
automate repetitive reports.

Responsibilities
- Write clean, testable Python code for data pipelines.
- Build and query SQL databases to serve analytics dashboards.
- Automate Excel/manual reporting using Python scripts.
- Work with pandas and NumPy to clean and analyse data.
- Build simple machine learning prototypes with scikit-learn.
- Use Git/GitHub for version control and code reviews.
- Communicate findings to non-technical stakeholders.

Required skills (must-have)
- Python programming
- pandas
- NumPy
- SQL
- Git / GitHub
- Data cleaning & EDA
- Problem solving & communication

Nice to have
- Machine learning basics (scikit-learn)
- Streamlit or Flask dashboards
- NLP / text processing
- Docker basics
- Linux command line
"""

# Required skills are the keywords the scorer looks for inside each
# resume. "Nice to have" skills are weighted lower by main.py.
REQUIRED_SKILLS = [
    # (skill name, category, weight)  weight 1.0 = must-have, 0.5 = nice-to-have
    ("Python",            "Programming",  1.0),
    ("pandas",            "Libraries",    1.0),
    ("NumPy",             "Libraries",    1.0),
    ("SQL",               "Databases",    1.0),
    ("Git",               "Tools",        1.0),
    ("GitHub",            "Tools",        1.0),
    ("data cleaning",     "Data Skills",  1.0),
    ("EDA",               "Data Skills",  1.0),
    ("communication",     "Soft Skills",  1.0),
    ("scikit-learn",      "ML",           0.5),
    ("Streamlit",         "Frameworks",   0.5),
    ("machine learning",  "ML",           0.5),
    ("NLP",               "ML",           0.5),
    ("Linux",             "Tools",        0.5),
    ("Docker",            "Tools",        0.5),
]


# ---------------------------------------------------------------------
# 2. SYNTHETIC RESUMES
# ---------------------------------------------------------------------
# Each resume is a dict. `match_level` controls how many of the required
# skills appear in the text:
#   "strong"  -> contains almost all must-have skills  (score ~ 75-90)
#   "medium"  -> contains about half                    (score ~ 45-60)
#   "weak"    -> contains very few                     (score ~ 15-30)
#
# We write the skills NATURALLY into sentences, exactly like a real
# resume, so you can see that the tool works on real-world text.

RESUMES = [
    {
        "filename": "resume_01_Aarav_Menon.pdf",
        "name": "Aarav Menon",
        "match_level": "strong",
        "text": """\
AARAV MENON
Junior Python Developer | Hyderabad
aarav.menon@example.com | +91-98765-43210

SUMMARY
Detail-oriented computer science graduate with strong Python programming
skills and a passion for data automation. Experienced in building data
pipelines with pandas and NumPy, writing SQL queries, and collaborating
through Git and GitHub. Strong problem solving and communication skills.

TECHNICAL SKILLS
- Languages: Python, SQL, basic Linux command line
- Libraries: pandas, NumPy, matplotlib
- Tools: Git, GitHub, VS Code, Docker basics
- Data: data cleaning, EDA, Excel automation
- ML: scikit-learn basics, machine learning projects

EXPERIENCE
Data Automation Intern | SampleTech Solutions | Jan 2024 - Jun 2024
- Automated weekly Excel reports using Python scripts, saving 10 hours/week.
- Cleaned messy customer datasets with pandas and performed EDA.
- Wrote SQL queries to pull sales data for the analytics team.
- Documented code and shared updates on GitHub with the team.

PROJECTS
Resume Keyword Analyzer
- Built a Python tool that parses resumes and ranks them with pandas
  and scikit-learn, presenting results in a Streamlit dashboard.
Communication: presented project findings to non-technical stakeholders.

EDUCATION
B.Tech Computer Science | Sample University | 2024
"""
    },
    {
        "filename": "resume_02_Siya_Kulkarni.pdf",
        "name": "Siya Kulkarni",
        "match_level": "strong",
        "text": """\
SIYA KULKARNI
Python Developer & Data Analyst | Pune
siya.kulkarni@example.com | +91-98123-45678

PROFILE
Analytical graduate skilled in Python programming, pandas and NumPy for
data cleaning and EDA. Comfortable writing SQL, using Git/GitHub for
version control, and explaining results with clear communication.

SKILLS
- Python programming, SQL, pandas, NumPy
- Data cleaning, EDA, Excel dashboards
- Git, GitHub, Linux terminal
- machine learning with scikit-learn, NLP basics
- Strong problem solving and communication

EXPERIENCE
Analytics Intern | DataBridge Labs | May 2024 - Nov 2024
- Built pandas pipelines for data cleaning of 50k+ row datasets.
- Created EDA notebooks and shared them via GitHub.
- Automated a manual SQL reporting task with a Python script.
- Used scikit-learn for a small machine learning prototype.

PROJECTS
Sales Dashboard with Streamlit
- Built a Streamlit app on top of SQL data with pandas and NumPy.
- Practiced NLP on customer reviews for a sentiment project.
Worked on Linux servers during the internship; used Docker once.

EDUCATION
B.Sc Statistics | Sample University | 2023
"""
    },
    {
        "filename": "resume_03_Rohan_Desai.pdf",
        "name": "Rohan Desai",
        "match_level": "medium",
        "text": """\
ROHAN DESAI
Software Developer | Bengaluru
rohan.desai@example.com | +91-99000-12345

SUMMARY
Computer science graduate focused on web development and databases.
Familiar with Python programming and SQL, and version control with Git.

SKILLS
- Python programming, JavaScript, HTML/CSS
- SQL, PostgreSQL
- Git, GitHub
- Basic data cleaning in Excel

EXPERIENCE
Web Developer Intern | WebCraft Studio | Jun 2024 - Dec 2024
- Built internal tools with Python for the support team.
- Wrote SQL views to power team dashboards.
- Collaborated using Git and GitHub pull requests.
- Improved communication with daily stand-ups.

PROJECTS
Employee Leave Tracker
- Python + SQL app to track leave requests; used pandas once.
- Deployed on a basic Linux box.

EDUCATION
B.E Computer Science | Sample University | 2024
"""
    },
    {
        "filename": "resume_04_Ananya_Iyer.docx",
        "name": "Ananya Iyer",
        "match_level": "medium",
        "text": """\
ANANYA IYER
Data Analyst | Chennai
ananya.iyer@example.com | +91-98444-77777

SUMMARY
Detail-oriented analyst with experience in Excel and SQL. Learning
Python programming and pandas for data cleaning and automation.
Good communication and teamwork skills.

SKILLS
- SQL, Excel, basic Python programming
- Data cleaning, EDA basics
- Git (basic), GitHub (basic)
- Communication, documentation

EXPERIENCE
Reporting Analyst | InsightWorks | Jul 2023 - Present
- Run weekly SQL reports and clean data before analysis.
- Documented processes; strong communication with stakeholders.
- Started automating reports with pandas.

PROJECTS
Customer Churn Spreadsheet
- Performed EDA on customer data; used Python scripts for data cleaning.
- Shared notes on GitHub.

EDUCATION
B.Com Computer Applications | Sample University | 2023
"""
    },
    {
        "filename": "resume_05_Kabir_Sharma.pdf",
        "name": "Kabir Sharma",
        "match_level": "weak",
        "text": """\
KABIR SHARMA
Marketing Associate | Mumbai
kabir.sharma@example.com | +91-90000-55555

SUMMARY
Creative marketing professional with experience in social media
campaigns, content writing and client communication.

SKILLS
- Content writing, social media marketing
- Communication, teamwork
- Excel basics, Canva

EXPERIENCE
Marketing Intern | BrightAds | Jan 2024 - Jun 2024
- Wrote campaign content and managed social media.
- Communicated with clients and prepared presentations.

EDUCATION
B.A Marketing | Sample University | 2024
"""
    },
    {
        "filename": "resume_06_Meera_Nair.pdf",
        "name": "Meera Nair",
        "match_level": "weak",
        "text": """\
MEERA NAIR
HR Intern | Kochi
meera.nair@example.com | +91-97777-88888

SUMMARY
HR graduate interested in recruitment and employee engagement.
Strong communication and coordination skills.

SKILLS
- Recruitment coordination, HR administration
- Communication, Excel
- Basic data entry

EXPERIENCE
HR Intern | PeopleFirst HR | Mar 2024 - Aug 2024
- Screened resumes manually and scheduled interviews.
- Communicated with candidates and maintained records.

EDUCATION
BBA Human Resources | Sample University | 2024
"""
    },
    {
        "filename": "resume_07_Arjun_Rao.pdf",
        "name": "Arjun Rao",
        "match_level": "strong",
        "text": """\
ARJUN RAO
Python Developer | Hyderabad
arjun.rao@example.com | +91-98111-22222

SUMMARY
Backend-focused developer with strong Python programming, SQL and
automation skills. Uses pandas and NumPy for data tasks, Git/GitHub
for collaboration, and has machine learning basics with scikit-learn.

SKILLS
- Python programming, SQL, Linux
- pandas, NumPy, data cleaning, EDA
- Git, GitHub, Docker, Streamlit
- NLP projects, machine learning with scikit-learn
- Communication, problem solving

EXPERIENCE
Automation Intern | AutoMetrics | Feb 2024 - Jul 2024
- Wrote Python scripts to clean data with pandas and NumPy.
- Built SQL queries and stored results in Git/GitHub repos.
- Prototyped a Streamlit dashboard for the team.
- Ran data cleaning pipelines on Linux servers.

PROJECTS
NLP Resume Matcher
- Used scikit-learn and NLP techniques to rank resumes by
  machine learning similarity, wrapped in a small Streamlit UI.
Communication: demoed the tool to the engineering team.

EDUCATION
B.Tech IT | Sample University | 2024
"""
    },
    {
        "filename": "resume_08_Diya_Patel.pdf",
        "name": "Diya Patel",
        "match_level": "medium",
        "text": """\
DIYA PATEL
Junior Developer | Surat
diya.patel@example.com | +91-99222-33333

SUMMARY
Recent graduate with Python programming basics, SQL knowledge and
an interest in data analysis. Good communication skills.

SKILLS
- Python programming, SQL basics
- Excel, data cleaning basics
- Git basics
- Communication

EXPERIENCE
Support Engineer Intern | TechServe | Sep 2024 - Dec 2024
- Wrote simple Python scripts to fix data issues.
- Used SQL to fetch customer records.
- Practiced communication with the support team.

PROJECTS
Student Records App
- Small Python + SQL app; touched on pandas for EDA.

EDUCATION
BCA | Sample University | 2024
"""
    },
]


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def write_pdf(path, text):
    """Render `text` to a simple PDF using reportlab."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.units import cm

    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=1.5 * cm, bottomMargin=1.5 * cm,
    )
    styles = getSampleStyleSheet()
    # A slightly smaller body style keeps each resume on 1-2 pages.
    body = ParagraphStyle("body", parent=styles["Normal"], fontSize=9.5, leading=13)
    title = ParagraphStyle("title", parent=styles["Title"], fontSize=15)

    story = []
    for i, raw_line in enumerate(text.splitlines()):
        line = raw_line.strip()
        if not line:
            continue
        if i == 0:
            story.append(Paragraph(line, title))
        else:
            # Escape ampersands etc. for reportlab mini-HTML.
            safe = (line.replace("&", "&amp;")
                        .replace("<", "&lt;")
                        .replace(">", "&gt;"))
            story.append(Paragraph(safe, body))
    doc.build(story)


def write_docx(path, text):
    """Render `text` to a .docx file using python-docx."""
    from docx import Document

    doc = Document()
    lines = [ln.strip() for ln in text.splitlines()]
    doc.add_heading(lines[0], level=1)
    for line in lines[1:]:
        if line:
            doc.add_paragraph(line)
    doc.save(path)


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------
def main():
    # 1) Job description
    with open(os.path.join(DATA_DIR, "job_description.txt"), "w") as f:
        f.write(JOB_DESCRIPTION)

    # 2) Required skills CSV
    with open(os.path.join(DATA_DIR, "required_skills.csv"), "w") as f:
        f.write("skill,category,weight\n")
        for skill, category, weight in REQUIRED_SKILLS:
            f.write(f'"{skill}","{category}",{weight}\n')

    # 3) Resumes
    for r in RESUMES:
        path = os.path.join(RESUMES_DIR, r["filename"])
        if r["filename"].endswith(".docx"):
            write_docx(path, r["text"])
            print(f"[DOCX] {r['filename']}  ({r['match_level']} match)")
        else:
            write_pdf(path, r["text"])
            print(f"[PDF ] {r['filename']}  ({r['match_level']} match)")

    print("\nAll sample data created in:")
    print("  -", RESUMES_DIR)
    print("  -", DATA_DIR)
    print("Expected scores: strong ~75-90, medium ~40-60, weak ~10-30")


if __name__ == "__main__":
    main()
