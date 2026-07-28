import streamlit as st

from api import (
    get_candidates,
    get_recommendations,
)

st.title("🎯 Job Recommendations")

candidates = get_candidates()

candidate = st.selectbox(
    "Candidate",
    candidates,
    format_func=lambda x: x["name"],
)

if st.button("Find Jobs", use_container_width=True):

    jobs = get_recommendations(candidate["id"])

    for job in jobs[:20]:

        with st.container():

            st.subheader(job["title"])

            st.write(job["company"])

            st.progress(job["score"] / 100)

            st.write(f"**Score:** {job['score']}")

            st.write(f"**Recommendation:** {job['recommendation']}")

            st.divider()