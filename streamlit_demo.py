"""
Recruiter-facing demo mode.

This app intentionally does not require FastAPI, SQLite, Ollama, or API keys.
It demonstrates the core product loop:
Resume -> extraction -> live job discovery -> transparent matching -> apply.
Deploy this file directly on Streamlit Community Cloud.
"""

import re
from datetime import date
import requests
import pdfplumber
import streamlit as st

st.set_page_config(page_title="AI Job Hunter — Live Demo", page_icon="🎯", layout="wide")

SKILLS = {
    "python","sql","fastapi","rest","rest api","docker","kubernetes","aws","gcp",
    "google cloud","bigquery","mysql","postgresql","mongodb","git","github",
    "java","javascript","typescript","react","node","express","etl","elt",
    "data engineering","data pipelines","llm","rag","ollama","gemini",
    "agentic ai","prompt engineering","microservices","sqlalchemy"
}

ALIASES = {
    "google cloud": "gcp",
    "google cloud platform": "gcp",
    "rest api": "rest",
    "postgres": "postgresql",
    "genai": "llm",
    "generative ai": "llm",
}

def parse_resume(uploaded):
    data = uploaded.getvalue()
    with open("/tmp/resume.pdf", "wb") as f:
        f.write(data)

    pages = []
    with pdfplumber.open("/tmp/resume.pdf") as pdf:
        for page in pdf.pages[:5]:
            pages.append(page.extract_text() or "")
    text = "\n".join(pages)
    low = text.lower()

    skills = set()
    for skill in SKILLS:
        if re.search(r"(?<![a-z0-9+#])" + re.escape(skill) + r"(?![a-z0-9+#])", low):
            skills.add(ALIASES.get(skill, skill))

    locations = [
        "Hyderabad","Bengaluru","Bangalore","Chennai","Pune","Mumbai",
        "Delhi","Gurgaon","Gurugram","Noida","Kolkata","Ahmedabad","India"
    ]
    location = next((x for x in locations if re.search(r"\b"+re.escape(x.lower())+r"\b", low)), "India")

    years = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\+?\s*(?:years|year|yrs|yr)\b", low)]
    ranges = re.findall(r"\b(20\d{2})\s*[-–]\s*(20\d{2}|present|current)\b", low)
    current = date.today().year
    for start, end in ranges:
        end_year = current if end in ("present","current") else int(end)
        if int(start) <= end_year:
            years.append((end_year-int(start)))

    experience = round(max(years), 1) if years else 0
    return text, sorted(skills), location, experience

@st.cache_data(ttl=3600)
def himalayas_search(query, country="India"):
    r = requests.get(
        "https://himalayas.app/jobs/api/search",
        params={"q": query, "country": country, "sort": "recent", "limit": 20},
        timeout=20,
    )
    r.raise_for_status()
    return r.json().get("jobs", [])

def score(candidate_skills, candidate_location, candidate_exp, job):
    text = ((job.get("title") or "") + " " + (job.get("description") or "")).lower()
    job_skills = set()
    for s in SKILLS:
        if re.search(r"(?<![a-z0-9+#])" + re.escape(s) + r"(?![a-z0-9+#])", text):
            job_skills.add(ALIASES.get(s, s))

    matched = candidate_skills & job_skills
    missing = job_skills - candidate_skills
    skill_score = round((len(matched)/len(job_skills))*60) if job_skills else 20

    loc_text = " ".join([
        str(job.get("companyName") or ""),
        str(job.get("description") or ""),
        " ".join(job.get("locationRestrictions") or []),
    ]).lower()
    location_ok = "worldwide" in loc_text or "india" in loc_text or "remote" in loc_text
    if candidate_location.lower() in loc_text:
        location_ok = True

    location_score = 20 if location_ok else 0

    exp_matches = [float(x) for x in re.findall(
        r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years|year|yrs|yr)\b", text
    )]
    required = max(exp_matches) if exp_matches else None
    if required is None:
        exp_score = 20
    elif candidate_exp >= required:
        exp_score = 20
    elif candidate_exp + 0.5 >= required:
        exp_score = 10
    else:
        exp_score = 0

    total = min(skill_score + location_score + exp_score, 100)
    return total, sorted(matched), sorted(missing), required

st.title("🎯 AI Job Hunter — Live Recruiter Demo")
st.caption("Upload a resume → discover current remote/India opportunities → see transparent fit scoring.")

resume = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if not resume:
    st.info("This demo is intentionally self-contained. No account or API key is required.")
    st.stop()

try:
    text, skills, location, experience = parse_resume(resume)
except Exception as exc:
    st.error(f"Could not parse this PDF: {exc}")
    st.stop()

c1,c2,c3 = st.columns(3)
c1.metric("Detected location", location)
c2.metric("Detected experience", f"{experience:g} years")
c3.metric("Detected skills", len(skills))

with st.expander("Resume profile"):
    st.write(", ".join(skills) or "No supported skills detected.")

queries = ["software engineer", "backend engineer", "data engineer", "python engineer"]
all_jobs = {}
with st.spinner("Fetching current remote/India listings..."):
    for q in queries:
        try:
            for job in himalayas_search(q):
                key = job.get("guid") or job.get("applicationLink")
                if key:
                    all_jobs[key] = job
        except Exception:
            continue

if not all_jobs:
    st.warning("No jobs were returned by the live source right now.")
    st.stop()

ranked = []
candidate_skills = set(skills)
for job in all_jobs.values():
    result = score(candidate_skills, location, experience, job)
    ranked.append((result, job))

ranked.sort(key=lambda x: x[0][0], reverse=True)

st.success(f"{len(ranked)} live listings analysed.")

for (fit, matched, missing, required), job in ranked[:20]:
    title = job.get("title") or "Untitled"
    company = job.get("companyName") or "Unknown company"
    st.subheader(f"{title} — {company}")
    st.write(f"**Fit:** {fit}/100  •  **Experience floor detected:** {required if required is not None else 'Not stated'}")
    if matched:
        st.write("**Matched:** " + ", ".join(matched))
    if missing:
        st.write("**Missing:** " + ", ".join(missing[:10]))
    st.link_button("Open original listing", job.get("applicationLink") or job.get("guid"))
    st.divider()

st.caption("Job data source: Himalayas public jobs API. Listings remain owned by their original publishers.")
