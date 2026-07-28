import streamlit as st

from api import upload_resume

st.title("📄 Upload Resume")

resume = st.file_uploader(
    "Choose PDF Resume",
    type=["pdf"],
)

if resume:

    if st.button("Upload Resume", use_container_width=True):

        with st.spinner("Uploading..."):

            result = upload_resume(resume)

        st.success("Resume Uploaded")

        candidate = result["candidate"]

        st.subheader(candidate["name"])

        st.write(candidate["email"])

        st.write(candidate["phone"])

        st.write("### Skills")

        st.write(", ".join(candidate["skills"]))