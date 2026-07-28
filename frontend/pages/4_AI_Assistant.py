import streamlit as st

from api import (
    ai_explain,
    get_candidates,
    get_jobs,
)

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

if st.button("Generate AI Analysis", use_container_width=True):

    with st.spinner("Thinking..."):

        result = ai_explain(
            candidate["id"],
            job["id"],
        )

    st.success("Analysis Complete")

    st.write(result["response"])