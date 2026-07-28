import streamlit as st

from api import (
    get_candidates,
    get_jobs,
    ai_explain,
)

st.title("🤖 AI Career Assistant")

candidates = get_candidates()
jobs = get_jobs()

if not candidates:
    st.warning("No candidates found.")
    st.stop()

if not jobs:
    st.warning("No jobs found.")
    st.stop()


candidate = st.selectbox(
    "Select Candidate",
    candidates,
    format_func=lambda x: x["name"],
)

job = st.selectbox(
    "Select Job",
    jobs,
    format_func=lambda x: f'{x["title"]} - {x["company"]}',
)

if st.button("Generate AI Explanation"):

    with st.spinner("Thinking..."):

        result = ai_explain(
            candidate["id"],
            job["id"],
        )

    st.success("Done")

    st.markdown(result["ai_explanation"])