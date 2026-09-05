import re

import pdfplumber

from app.config import (
    MAX_RESUME_PAGES,
    MAX_RESUME_TEXT_LENGTH,
)


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
        text_parts = []

        with pdfplumber.open(file_path) as pdf:

            for page_number, page in enumerate(
                pdf.pages,
                start=1,
            ):

                if page_number > MAX_RESUME_PAGES:
                    break

                page_text = page.extract_text()

                if page_text:
                    text_parts.append(
                        page_text
                    )

                current_length = sum(
                    len(part)
                    for part in text_parts
                )

                if current_length >= MAX_RESUME_TEXT_LENGTH:
                    break

        text = "\n".join(text_parts)

        return text[:MAX_RESUME_TEXT_LENGTH]

    @staticmethod
    def parse_resume(text: str):
        email = ResumeService.extract_email(
            text
        )

        phone = ResumeService.extract_phone(
            text
        )

        skills = ResumeService.extract_skills(
            text
        )

        experience = ResumeService.extract_experience(
            text
        )

        name = (
            text.split("\n")[0].strip()
            if text.strip()
            else "Unknown"
        )

        return {
            "name": name[:200],
            "email": email[:254],
            "phone": phone[:50],
            "skills": skills[:50],
            "experience": experience,
        }

    @staticmethod
    def extract_email(text: str):
        match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text,
        )

        return (
            match.group(0)
            if match
            else ""
        )

    @staticmethod
    def extract_phone(text: str):
        match = re.search(
            r"(\+?\d[\d\s\-]{8,}\d)",
            text,
        )

        return (
            match.group(0)
            if match
            else ""
        )

    @staticmethod
    def extract_skills(text: str):
        lower = text.lower()

        return sorted(
            [
                tech
                for tech in TECH_STACK
                if tech in lower
            ]
        )

    @staticmethod
    def extract_experience(text: str):
        matches = re.findall(
            r"(\d+)\+?\s*(?:years|year|yrs|yr)",
            text.lower(),
        )

        if not matches:
            return 0

        return max(
            map(int, matches)
        )