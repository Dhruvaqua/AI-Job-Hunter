import streamlit as st

st.set_page_config(
    page_title="AI Job Hunter",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI Job Hunter")

st.markdown("---")

c1, c2 = st.columns(2)

with c1:

    st.info(
        """
### 📄 Resume

- Upload Resume
- Parse PDF
- Extract Skills
- Store Candidate
"""
    )

    st.success(
        """
### 💼 Jobs

- Import Jobs
- Search Jobs
- Filter Jobs
"""
    )

with c2:

    st.warning(
        """
### 🎯 AI

- Match Resume
- ATS Score
- Recommendations
"""
    )

    st.error(
        """
### 🤖 LLM

- Explain Match
- Resume Advice
- Career Guidance
"""
    )

st.markdown("---")

st.header("Project Status")

st.progress(0.80)

st.write("**80% Complete**")

st.caption("Use the left sidebar to explore the application.")