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


class SkillExtractor:

    @staticmethod
    def extract(text: str):
        text = text.lower()

        return sorted(
            [
                skill
                for skill in TECH_STACK
                if skill in text
            ]
        )