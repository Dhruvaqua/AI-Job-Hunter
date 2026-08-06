# 🤖 AI Job Hunter

An AI-powered job search platform that automatically discovers software engineering jobs, parses resumes, evaluates ATS compatibility, recommends matching opportunities, and provides AI-generated career insights.

Built to demonstrate backend engineering, REST API design, AI integration, automation, and full-stack development skills.

---

## Features

### Resume Intelligence
- Upload PDF resumes
- Automatic resume parsing
- Candidate profile creation
- Skill extraction
- Experience extraction

### Job Aggregation
- Fetch jobs from Greenhouse
- Fetch jobs from Lever
- Duplicate detection
- Local job database
- Company and keyword filtering

### AI Recommendation Engine
- Candidate-to-job matching
- Skill overlap scoring
- Location matching
- Recommendation ranking
- Match explanations

### ATS Resume Analysis
- Resume scoring
- Missing keyword detection
- Resume improvement suggestions
- ATS compatibility analysis

### AI Career Assistant
- Local LLM integration using Ollama
- Personalized job explanations
- Resume improvement guidance
- AI-generated career advice

### Dashboard
- Candidate analytics
- Job statistics
- Recommendation overview
- Interactive charts

---

# Architecture

```
                  Resume PDF
                      │
                      ▼
             Resume Parser
                      │
                      ▼
             Candidate Profile
                      │
                      ▼
     AI Recommendation Engine
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
    ATS Analysis            AI Assistant
          │                       │
          └───────────┬───────────┘
                      ▼
                 Streamlit UI
                      │
                      ▼
                FastAPI Backend
                      │
      ┌───────────────┴───────────────┐
      ▼                               ▼
 Greenhouse API                  Lever API
```

---

# Tech Stack

## Backend

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn

## Frontend

- Streamlit

## AI

- Ollama
- Llama 3.2

## Data Processing

- pdfplumber
- Requests

---

# Project Structure

```
app/
│
├── ai/
├── api/
├── database/
├── models/
├── schemas/
├── services/
├── utils/
│
frontend/
│
├── Home.py
├── api.py
├── style.css
└── pages/
```

---

# API Modules

| Module | Purpose |
|---------|----------|
| Jobs | Job CRUD |
| Search | Fetch Greenhouse & Lever jobs |
| Resume | Resume upload & parsing |
| Candidate | Candidate management |
| ATS | Resume scoring |
| AI | AI explanations |
| Recommendations | Job matching |

---

# Screenshots

## Home

_Add screenshot_

---

## Resume Upload

_Add screenshot_

---

## Job Search

_Add screenshot_

---

## Recommendations

_Add screenshot_

---

## AI Assistant

_Add screenshot_

---

## Dashboard

_Add screenshot_

---

# Installation

## Clone

```bash
git clone https://github.com/YOUR_USERNAME/ai-job-hunter.git

cd ai-job-hunter
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Start Ollama

```bash
ollama serve
```

Pull the model

```bash
ollama pull llama3.2
```

---

## Run Backend

```bash
python -m uvicorn app.main:app --reload
```

---

## Run Frontend

```bash
streamlit run frontend/Home.py
```

---

# Future Improvements

- Authentication
- PostgreSQL support
- Docker deployment
- Redis caching
- Email job alerts
- Background scheduler
- Semantic vector search
- Multi-resume management
- Interview preparation
- Cover letter generation

---

# Skills Demonstrated

- REST API Development
- Backend Engineering
- Database Design
- Clean Architecture
- AI Integration
- Resume Parsing
- Recommendation Systems
- LLM Prompt Engineering
- Full Stack Development
- API Integration

---

# Author

**Dhruv**

Software Engineer passionate about Backend Development, AI Applications, and Automation.

---

# License

MIT License