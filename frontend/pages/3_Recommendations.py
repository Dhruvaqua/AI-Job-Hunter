import streamlit as st

from api import (
    get_candidates,
    get_recommendations,
)
from utils import load_css, sidebar

load_css()
sidebar()

st.title("🎯 AI Recommendations")

candidates = get_candidates()

if not candidates:
    st.warning("No candidates found. Upload a resume first.")
    st.stop()

candidate = st.selectbox(
    "Select Candidate",
    candidates,
    format_func=lambda x: x["name"],
)

if st.button(
    "Generate Recommendations",
    use_container_width=True,
):

    with st.spinner("Finding best matches..."):

        recommendations = get_recommendations(
            candidate["id"]
        )

    if isinstance(recommendations, dict):
        st.error(recommendations)
        st.stop()

    st.success(f"Found {len(recommendations)} matching jobs")

    st.divider()

    for job in recommendations[:20]:

        if job["score"] >= 90:
            badge = "🟢 Excellent"

        elif job["score"] >= 75:
            badge = "🟡 Good"

        else:
            badge = "🔴 Weak"

        with st.expander(
            f"{badge} {job['title']} • {job['score']}%"
        ):

            col1, col2 = st.columns([3, 1])

            with col1:

                st.write(f"### {job['title']}")
                st.write(f"🏢 {job['company']}")
                st.write(f"📍 {job['location']}")
                st.write(f"Recommendation: **{job['recommendation']}**")

            with col2:

                st.metric(
                    "Score",
                    f"{job['score']}%"
                )

            if job["strengths"]:
                st.success("\n".join(job["strengths"]))

            if job["missing_skills"]:
                st.warning(
                    "Missing Skills:\n\n"
                    + "\n".join(job["missing_skills"])
                )

            if job["improvements"]:
                st.info(
                    "\n".join(job["improvements"])
                )

st.divider()

st.caption(
    "AI Job Hunter • Built with FastAPI • Streamlit • Ollama"
)