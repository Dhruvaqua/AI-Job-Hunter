import re
from datetime import date
import pdfplumber

from app.config import MAX_RESUME_PAGES, MAX_RESUME_TEXT_LENGTH

TECH_STACK = {
    "python", "java", "c++", "javascript", "typescript", "react", "angular",
    "vue", "node", "express", "fastapi", "django", "flask", "spring",
    "sql", "mysql", "postgresql", "mongodb", "redis", "docker", "kubernetes",
    "aws", "azure", "gcp", "google cloud", "bigquery", "git", "github", "linux",
    "graphql", "rest", "rest api", "microservices", "pydantic", "sqlalchemy",
    "etl", "elt", "data engineering", "data pipelines", "llm", "rag",
    "ollama", "gemini", "agentic ai", "prompt engineering", "fastapi",
}

KNOWN_LOCATIONS = [
    "Hyderabad", "Bangalore", "Bengaluru", "Chennai", "Pune", "Mumbai",
    "Delhi", "Gurgaon", "Gurugram", "Noida", "Kolkata", "Ahmedabad",
    "Jaipur", "India", "Remote",
]

class ResumeService:
    @staticmethod
    def extract_text(file_path: str) -> str:
        parts = []
        with pdfplumber.open(file_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                if page_number > MAX_RESUME_PAGES:
                    break
                page_text = page.extract_text() or ""
                if page_text:
                    parts.append(page_text)
                if sum(len(p) for p in parts) >= MAX_RESUME_TEXT_LENGTH:
                    break
        return "\n".join(parts)[:MAX_RESUME_TEXT_LENGTH]

    @staticmethod
    def parse_resume(text: str):
        return {
            "name": (text.split("\n")[0].strip() if text.strip() else "Unknown")[:200],
            "email": ResumeService.extract_email(text)[:254],
            "phone": ResumeService.extract_phone(text)[:50],
            "location": ResumeService.extract_location(text),
            "skills": ResumeService.extract_skills(text)[:100],
            "experience": ResumeService.extract_experience(text),
        }

    @staticmethod
    def extract_email(text: str):
        m = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
        return m.group(0) if m else ""

    @staticmethod
    def extract_phone(text: str):
        m = re.search(r"(\+?\d[\d\s\-]{8,}\d)", text)
        return m.group(0) if m else ""

    @staticmethod
    def extract_location(text: str):
        lower = text.lower()
        for location in KNOWN_LOCATIONS:
            if re.search(r"\b" + re.escape(location.lower()) + r"\b", lower):
                return "Bengaluru" if location.lower() == "bengaluru" else location
        return "India"

    @staticmethod
    def extract_skills(text: str):
        lower = text.lower()
        found = []
        for skill in TECH_STACK:
            if re.search(r"(?<![a-z0-9+#])" + re.escape(skill) + r"(?![a-z0-9+#])", lower):
                found.append(skill)
        return sorted(set(found))

    @staticmethod
    def extract_experience(text: str):
        lower = text.lower()

        explicit = re.findall(r"(\d+(?:\.\d+)?)\+?\s*(?:years|year|yrs|yr)", lower)
        values = [float(x) for x in explicit]

        # Handles common resume date ranges such as "Oct 2024 - Aug 2026".
        ranges = re.findall(
            r"\b(20\d{2})\s*[-–]\s*(20\d{2}|present|current)\b",
            lower,
        )
        months = 0
        current_year = date.today().year
        for start, end in ranges:
            end_year = current_year if end in ("present", "current") else int(end)
            start_year = int(start)
            if end_year >= start_year:
                months += min((end_year - start_year) * 12, 120)

        if months:
            values.append(months / 12)

        return round(max(values), 1) if values else 0.0
