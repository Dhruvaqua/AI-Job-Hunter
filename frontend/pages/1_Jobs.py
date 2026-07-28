import streamlit as st
import pandas as pd

from api import get_jobs

st.title("💼 Jobs")

try:
    jobs = get_jobs()

except Exception as e:
    st.error(e)
    st.stop()

if len(jobs) == 0:
    st.warning("No jobs found.")
    st.stop()

df = pd.DataFrame(jobs)

display_columns = [
    "title",
    "company",
    "location",
]

st.dataframe(
    df[display_columns],
    use_container_width=True,
)

st.divider()

selected_job = st.selectbox(
    "Select Job",
    jobs,
    format_func=lambda x: f'{x["title"]} - {x["company"]}',
)

st.subheader(selected_job["title"])

col1, col2 = st.columns(2)

with col1:
    st.write("### Company")
    st.write(selected_job["company"])

    st.write("### Location")
    st.write(selected_job["location"])

with col2:
    st.write("### Required Skills")

    if selected_job.get("required_skills"):
        st.write(selected_job["required_skills"])
    else:
        st.info("No skills extracted.")

st.write("### Description")

description = selected_job.get("description")

if description:
    st.write(description)

else:
    st.info("Description not available.")