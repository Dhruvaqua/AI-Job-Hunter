import streamlit as st
import pandas as pd

from api import get_jobs, get_candidates
from utils import load_css, sidebar

load_css()
sidebar()

st.title("📊 Dashboard")
st.caption("Overview of your AI Job Hunter platform")

jobs = get_jobs()
candidates = get_candidates()

total_jobs = len(jobs)
total_candidates = len(candidates)

recommended = 0
average_score = 0

scores = []

if candidates:

    candidate = candidates[0]

    from api import get_recommendations

    recommendations = get_recommendations(candidate["id"])

    if isinstance(recommendations, list):

        recommended = len(
            [r for r in recommendations if r["score"] >= 80]
        )

        scores = [r["score"] for r in recommendations]

        if scores:
            average_score = sum(scores) / len(scores)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Jobs",
    total_jobs,
)

col2.metric(
    "Candidates",
    total_candidates,
)

col3.metric(
    "Recommended",
    recommended,
)

col4.metric(
    "Average Match",
    f"{average_score:.0f}%"
)

st.divider()

if scores:

    df = pd.DataFrame(
        {
            "Score": scores
        }
    )

    st.subheader("Recommendation Score Distribution")

    st.bar_chart(df)

st.divider()

if jobs:

    st.subheader("Latest Jobs")

    latest = pd.DataFrame(jobs[:10])

    st.dataframe(
        latest[
            [
                "title",
                "company",
                "location",
            ]
        ],
        use_container_width=True,
    )