import re
import pdfplumber


TECH_STACK = {
    "python",
    "java",
    "c++",
    "javascript",
    "typescript",
    "react",
    "angular",
    "vue",
    "node",
    "express",
    "fastapi",
    "django",
    "flask",
    "spring",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "redis",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "git",
    "github",
    "linux",
    "graphql",
    "rest",
}


class ResumeService:

    @staticmethod
    def extract_text(file_path: str) -> str:
        text = ""

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    @staticmethod
    def parse_resume(text: str):
        email = ResumeService.extract_email(text)
        phone = ResumeService.extract_phone(text)
        skills = ResumeService.extract_skills(text)
        experience = ResumeService.extract_experience(text)

        name = text.split("\n")[0].strip()

        return {
            "name": name,
            "email": email,
            "phone": phone,
            "skills": skills,
            "experience": experience,
        }

    @staticmethod
    def extract_email(text: str):
        match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text,
        )
        return match.group(0) if match else ""

    @staticmethod
    def extract_phone(text: str):
        match = re.search(
            r"(\+?\d[\d\s\-]{8,}\d)",
            text,
        )
        return match.group(0) if match else ""

    @staticmethod
    def extract_skills(text: str):
        lower = text.lower()

        return sorted([
            tech
            for tech in TECH_STACK
            if tech in lower
        ])

    @staticmethod
    def extract_experience(text: str):
        matches = re.findall(
            r"(\d+)\+?\s*(?:years|year|yrs|yr)",
            text.lower(),
        )

        if not matches:
            return 0

        return max(map(int, matches))