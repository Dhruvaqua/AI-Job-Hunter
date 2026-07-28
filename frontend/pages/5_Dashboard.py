import streamlit as st

from api import (
    get_jobs,
    get_candidates,
)

st.title("📊 Dashboard")

jobs = get_jobs()
candidates = get_candidates()

st.metric(
    "Jobs",
    len(jobs),
)

st.metric(
    "Candidates",
    len(candidates),
)

st.divider()

companies = {}

for job in jobs:

    company = job["company"]

    companies[company] = companies.get(company, 0) + 1

st.subheader("Top Companies")

for company, count in sorted(
    companies.items(),
    key=lambda x: x[1],
    reverse=True,
)[:10]:

    st.write(f"**{company}** — {count} jobs")

st.divider()

locations = {}

for job in jobs:

    location = job["location"]

    locations[location] = locations.get(location, 0) + 1

st.subheader("Top Locations")

for location, count in sorted(
    locations.items(),
    key=lambda x: x[1],
    reverse=True,
)[:10]:

    st.write(f"**{location}** — {count} jobs")