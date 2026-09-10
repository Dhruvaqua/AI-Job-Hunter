import streamlit as st

from utils import load_css, sidebar
from api import (
    ai_explain,
    get_candidates,
    get_jobs,
    interview_questions,
    learning_roadmap,
    resume_tailor,
)


st.set_page_config(
    page_title="AI Assistant",
    layout="wide",
)

load_css()
sidebar()

st.title("🤖 AI Career Assistant")

try:
    candidates = get_candidates()
    jobs = get_jobs()

except Exception as e:
    st.error(f"Unable to load data from backend: {e}")
    st.stop()


if not candidates:
    st.warning("No candidates found. Please upload a resume first.")
    st.stop()


if not jobs:
    st.warning("No jobs found. Please collect or add jobs first.")
    st.stop()


candidate = st.selectbox(
    "Candidate",
    candidates,
    format_func=lambda x: x["name"],
)

job = st.selectbox(
    "Job",
    jobs,
    format_func=lambda x: f'{x["title"]} - {x["company"]}',
)


tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Job Analysis",
        "Resume Tailoring",
        "Interview Prep",
        "Learning Roadmap",
    ]
)


with tab1:

    if st.button(
        "Analyze Job",
        use_container_width=True,
    ):

        with st.spinner("Analyzing job..."):

            try:
                result = ai_explain(
                    candidate["id"],
                    job["id"],
                )

                st.markdown(result["response"])

            except Exception as e:
                st.error(f"AI analysis failed: {e}")


with tab2:

    if st.button(
        "Tailor Resume",
        use_container_width=True,
    ):

        with st.spinner("Generating tailored resume advice..."):

            try:
                result = resume_tailor(
                    candidate["id"],
                    job["id"],
                )

                st.markdown(result["response"])

            except Exception as e:
                st.error(f"Resume tailoring failed: {e}")


with tab3:

    if st.button(
        "Generate Interview Questions",
        use_container_width=True,
    ):

        with st.spinner("Preparing interview questions..."):

            try:
                result = interview_questions(
                    candidate["id"],
                    job["id"],
                )

                st.markdown(result["response"])

            except Exception as e:
                st.error(f"Interview preparation failed: {e}")


with tab4:

    if st.button(
        "Generate Learning Roadmap",
        use_container_width=True,
    ):

        with st.spinner("Building learning roadmap..."):

            try:
                result = learning_roadmap(
                    candidate["id"],
                    job["id"],
                )

                st.markdown(result["response"])

            except Exception as e:
                st.error(f"Learning roadmap generation failed: {e}")