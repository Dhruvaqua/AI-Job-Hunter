import streamlit as st

from utils import load_css, sidebar

load_css()
sidebar()

st.title("🤖 AI Job Hunter")

st.caption(
    "AI-powered Job Discovery and Resume Matching Platform"
)

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.markdown("## 🚀 Features")

    st.write("✅ Resume Parsing")

    st.write("✅ AI Resume Analysis")

    st.write("✅ ATS Score")

    st.write("✅ Job Search")

    st.write("✅ Smart Recommendations")

    st.write("✅ AI Career Assistant")

with col2:

    st.markdown("## 🛠 Tech Stack")

    st.write("FastAPI")

    st.write("Streamlit")

    st.write("SQLAlchemy")

    st.write("SQLite")

    st.write("Ollama")

    st.write("Llama 3.2")

st.divider()

st.info(
    "Upload your resume and start discovering AI-powered job matches."
)