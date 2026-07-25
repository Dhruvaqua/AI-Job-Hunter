from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./jobs.db")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")