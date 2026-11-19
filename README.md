# 🗂️ Automated Resume Screening Tool

A beginner-friendly, fully-offline Python project that simulates how a real
**Applicant Tracking System (ATS)** screens resumes against a job description.
It extracts text from PDF/DOCX resumes, cleans it, matches required skills,
computes a TF-IDF cosine-similarity score, ranks candidates, and writes a
shortlist report (CSV + JSON + Markdown + chart).

> ⚠️ This is a **student simulation**. It does NOT connect to any real
> company ATS, and it uses **synthetic resumes** (no real people's data).

---

## 🎯 Why this project exists

Recruiters receive hundreds of resumes per opening. Real ATS tools shortlist
candidates by comparing each resume against the job description using
**keywords, skills, experience, education** and overall text similarity.
This project reproduces that pipeline on a small scale so you can:

- Understand how resume screening actually works under the hood.
- Practice Python, file I/O, regex, pandas, and NLP (TF-IDF + cosine similarity).
- Show a complete, runnable project on GitHub.

---

## ✨ Features

- 📄 **Multi-format input** — reads `.pdf` (pypdf, fallback pdfplumber),
  `.docx` (python-docx), and `.txt` resumes.
- 🧹 **Text cleaning** — lower-casing, whitespace normalisation, symbol stripping.
- 🔑 **Keyword matching** — counts required skills found in each resume
  (must-have vs nice-to-have, weighted).
- 📐 **Semantic similarity** — TF-IDF vectorization + cosine similarity
  between resume and job description (scikit-learn, with a NumPy fallback).
- 🧮 **Blended score (0–100)** — 60% keyword match + 40% similarity.
- ✅ **Shortlist / reject decision** at a configurable threshold (default 60).
- 📊 **Reports** — CSV, JSON, Markdown, and a matplotlib bar chart.
- 🌐 **Optional Streamlit dashboard** (`app.py`).

---

## 🏗️ Architecture

```
 resume files (PDF/DOCX/TXT)          job description (.txt)
        │                                    │
        ▼                                    ▼
 ┌─────────────────┐                ┌──────────────────┐
 │  Text Extractors│                │  required_skills │
 │  src/extractors │                │  data/*.csv      │
 └────────┬────────┘                └────────┬─────────┘
          │ raw text                         │ skill list
          ▼                                  ▼
 ┌─────────────────┐                ┌──────────────────┐
 │  clean_text()   │                │  load_skills()   │
 └────────┬────────┘                └────────┬─────────┘
          │ cleaned text                     │ weights
          └──────────────┬───────────────────┘
                         ▼
              ┌──────────────────────┐
              │  score_resume()      │
              │  keyword match       │
              │  + TF-IDF cosine     │
              │  → score 0-100       │
              └──────────┬───────────┘
                         ▼
              ┌──────────────────────┐
              │  decision & ranking  │
              │  SHORTLIST / REJECT  │
              └──────────┬───────────┘
                         ▼
        CSV / JSON / Markdown report + score chart
```

**Data flow:** upload → extract → clean → match skills → compute similarity →
score → rank → shortlist/reject → report.

---

## 📁 Folder structure

```
Automated-Resume-Screening-Tool/
├── main.py                  # CLI entry point (terminal)
├── app.py                   # optional Streamlit dashboard
├── requirements.txt         # pip dependencies
├── .gitignore
├── README.md
├── resumes/                 # input resumes (PDF/DOCX/TXT) - sample data
├── data/                    # job description + required-skills CSV
├── src/
│   ├── config.py            # paths + scoring weights + threshold
│   ├── extractors/          # pdf.py, docx.py, text.py
│   ├── core/scoring.py      # the scoring engine
│   ├── utils/               # text.py, skills.py, similarity.py
│   └── reporting/report.py  # CSV/JSON/MD/chart writers
├── outputs/                 # generated reports (CSV, JSON, MD, PNG)
├── scripts/                 # generate_sample_data.py
├── images/                  # screenshots for the README
└── docs/                    # setup & interview guides
```

---

## ⚙️ Setup & run

```bash
# 1) clone / download the repo, then:
cd Automated-Resume-Screening-Tool

# 2) (recommended) virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3) install dependencies
pip install -r requirements.txt

# 4) (optional) regenerate the sample resumes
python scripts/generate_sample_data.py

# 5) run the screener
python main.py
```

**CLI options:**

```bash
python main.py --resumes resumes --jd data/job_description.txt
python main.py --threshold 70      # change the shortlist cut-off
python main.py --no-chart          # skip the PNG chart
```

**Dashboard (optional):**

```bash
pip install streamlit
streamlit run app.py
```

---

## 📈 Sample output

```
[4] Found resumes          : 8

  resume_07_Arjun_Rao.pdf   score=80.8 -> SHORTLIST
  resume_01_Aarav_Menon.pdf score=77.8 -> SHORTLIST
  resume_02_Siya_Kulkarni.pdf score=77.2 -> SHORTLIST
  resume_04_Ananya_Iyer.docx score=53.0 -> REJECT
  resume_03_Rohan_Desai.pdf score=50.6 -> REJECT
  resume_08_Diya_Patel.pdf  score=47.7 -> REJECT
  resume_06_Meera_Nair.pdf  score=9.2  -> REJECT
  resume_05_Kabir_Sharma.pdf score=8.3 -> REJECT

SHORTLISTED: 3 / 8 candidates
```

Reports land in `outputs/`:
`screening_results.csv`, `screening_results.json`,
`screening_report.md`, `score_chart.png`.

---

## 🧠 How the score is calculated

```
score = 0.60 * keyword_score + 0.40 * similarity_score

keyword_score  = (weight of matched skills / total weight) * 100
similarity     = cosine_similarity(TF-IDF(resume), TF-IDF(job_desc)) * 100
```

- **Keyword match** catches exact skill names ("pandas", "SQL").
- **TF-IDF cosine** catches related wording even when the exact keyword
  is absent ("automated reporting" ≈ "automation").
- Weights live in `src/config.py` — tune `KEYWORD_WEIGHT`,
  `SIMILARITY_WEIGHT`, `SHORTLIST_THRESHOLD`.

---

## 🧪 Tests

A small self-check that the scoring behaves sanely:

```bash
python scripts/run_tests.py
```

---

## 📚 Learning outcomes

- File I/O across formats (PDF, DOCX, TXT)
- Text preprocessing with regex
- TF-IDF vectorization & cosine similarity
- Weighted scoring heuristics
- Structured reporting (CSV/JSON/Markdown)
- Modular project layout, CLI args, virtual environments

---

## 🚀 Stretch goals

- OCR for scanned PDFs (Tesseract / pytesseract)
- NER for years of experience & education parsing
- Embedding-based similarity (sentence-transformers)
- Bias audit & explainability notes
- Docker container for one-command runs

---

## ⚖️ Ethics note

Real hiring tools must be fair, explainable, and privacy-compliant.
This project uses only synthetic data and makes no real hiring decisions.

---

## 📄 License

MIT — free to use for learning and portfolio purposes.
