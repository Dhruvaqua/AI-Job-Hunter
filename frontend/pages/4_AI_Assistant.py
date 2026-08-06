import streamlit as st

from utils import load_css, sidebar

load_css()
sidebar()
from api import (
    ai_explain,
    get_candidates,
    get_jobs,
    interview_questions,
    learning_roadmap,
    resume_tailor,
)

st.set_page_config(page_title="AI Assistant", layout="wide")

st.title("🤖 AI Career Assistant")

candidates = get_candidates()
jobs = get_jobs()

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

    if st.button("Analyze Job", use_container_width=True):

        with st.spinner("Thinking..."):

            result = ai_explain(
                candidate["id"],
                job["id"],
            )

        st.markdown(result["response"])


with tab2:

    if st.button("Tailor Resume", use_container_width=True):

        with st.spinner("Generating..."):

            result = resume_tailor(
                candidate["id"],
                job["id"],
            )

        st.markdown(result["response"])


with tab3:

    if st.button("Generate Interview Questions", use_container_width=True):

        with st.spinner("Preparing interview..."):

            result = interview_questions(
                candidate["id"],
                job["id"],
            )

        st.markdown(result["response"])


with tab4:

    if st.button("Generate Learning Roadmap", use_container_width=True):

        with st.spinner("Planning roadmap..."):

            result = learning_roadmap(
                candidate["id"],
                job["id"],
            )

        st.markdown(result["response"])