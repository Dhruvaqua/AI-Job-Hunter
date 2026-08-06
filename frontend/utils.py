import streamlit as st


def load_css():

    with open("frontend/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )


def sidebar():

    with st.sidebar:

        st.title("🤖 AI Job Hunter")

        st.caption("AI Powered Career Platform")

        st.divider()

        st.success("🟢 Backend Online")

        st.info("🧠 Ollama Ready")

        st.metric(
            "Jobs",
            "218+",
        )

        st.metric(
            "Candidates",
            "1",
        )

        st.metric(
            "AI Features",
            "6",
        )

        st.divider()

        st.caption("Built with ❤️ using FastAPI + Ollama")