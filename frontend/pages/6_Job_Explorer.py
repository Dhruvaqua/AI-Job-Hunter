import streamlit as st

from utils import load_css, sidebar

load_css()
sidebar()
from api import get_jobs

st.set_page_config(page_title="Job Explorer", page_icon="💼")

st.title("💼 Job Explorer")

jobs = get_jobs()

if not jobs:
    st.warning("No jobs found.")
    st.stop()

companies = sorted({job["company"] for job in jobs})
locations = sorted({job["location"] for job in jobs if job["location"]})

company = st.selectbox(
    "Company",
    ["All"] + companies,
)

location = st.selectbox(
    "Location",
    ["All"] + locations,
)

keyword = st.text_input("Search")

filtered = jobs

if company != "All":
    filtered = [
        j for j in filtered
        if j["company"] == company
    ]

if location != "All":
    filtered = [
        j for j in filtered
        if j["location"] == location
    ]

if keyword:
    keyword = keyword.lower()

    filtered = [
        j
        for j in filtered
        if keyword in j["title"].lower()
        or keyword in (j.get("required_skills") or "").lower()
    ]

st.success(f"{len(filtered)} jobs found")

for job in filtered:

    with st.expander(
        f'{job["title"]} — {job["company"]}'
    ):

        st.write(f"**Location:** {job['location']}")

        st.write(
            f"**Required Skills:** "
            f"{job.get('required_skills') or 'N/A'}"
        )

        st.write("### Description")

        st.write(
            job.get("description")
            or "Description unavailable."
        )

        st.link_button(
            "Apply",
            job["url"],
            use_container_width=True,
        )