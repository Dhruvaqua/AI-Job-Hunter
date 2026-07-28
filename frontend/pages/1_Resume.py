import streamlit as st

from api import upload_resume

st.title("📄 Resume Upload")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"],
)

if uploaded_file:

    with st.spinner("Parsing resume..."):
        result = upload_resume(uploaded_file)

    st.success("Resume uploaded successfully!")

    st.subheader("Candidate")

    st.json(result["candidate"])

    st.metric(
        "Candidate ID",
        result["candidate_id"],
    )