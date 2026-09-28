# Live recruiter demo

## Recommended free setup

### Frontend: Streamlit Community Cloud

Deploy `streamlit_demo.py` from this repository.

1. Open https://share.streamlit.io/
2. Connect GitHub.
3. Select `Dhruvaqua/AI-Job-Hunter`.
4. Main file: `streamlit_demo.py`.
5. Deploy.

The demo does not require FastAPI, SQLite, Ollama, or a secret API key.

Important: Streamlit Community Cloud is free but apps without traffic hibernate after 12 hours, so this is a recruiter demo rather than guaranteed 24/7 infrastructure.

### Full backend

Use Render for `render.yaml` if you want a separately deployed FastAPI API.

Important: Render free web services spin down after 15 minutes without inbound traffic and their local filesystem is ephemeral. Therefore the free tier is not suitable for claiming 24/7 production uptime or durable SQLite storage.

## Why Ollama is not in the public demo

The local Ollama dependency is appropriate for your laptop but is not a practical free 24/7 cloud dependency. The public demo therefore proves the deterministic product path without requiring a private local LLM.

## Recruiter presentation

Put the deployed demo and GitHub repository in LinkedIn Featured:

- Live Demo
- GitHub
- 60–90 second screen recording
- Architecture diagram

Recommended description:

"End-to-end job matching platform built with Python/FastAPI/Streamlit. Parses a resume, discovers live job listings, normalizes skills and location, and produces transparent fit scores with missing-skill explanations."
