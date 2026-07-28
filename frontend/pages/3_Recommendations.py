import streamlit as st

from api import (
    get_candidates,
    get_recommendations,
)

st.title("🎯 AI Recommendations")

candidates = get_candidates()

if not isinstance(candidates, list):
    st.error(candidates)
    st.stop()

if len(candidates) == 0:
    st.warning("Upload a resume first.")
    st.stop()

candidate = st.selectbox(
    "Candidate",
    candidates,
    format_func=lambda x: x["name"],
)

if st.button("Generate Recommendations"):

    jobs = get_recommendations(
        candidate["id"]
    )

    for job in jobs[:10]:

        with st.expander(
            f'{job["title"]} ({job["company"]})'
        ):

            st.metric(
                "Match Score",
                f'{job["score"]}%'
            )

            st.write(
                job["recommendation"]
            )

            st.write("Strengths")

            for item in job["strengths"]:
                st.success(item)

            st.write("Missing Skills")

            for item in job["missing_skills"]:
                st.warning(item)

            st.write("Improvements")

            for item in job["improvements"]:
                st.info(item)