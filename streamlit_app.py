import httpx
import streamlit as st


st.set_page_config(
    page_title="QueryPilot AI",
    page_icon="📊",
    layout="wide",
)

st.title("QueryPilot AI")
st.caption("AI-powered business analytics copilot for RetailStar")

ask_tab, eval_tab = st.tabs(
    ["Ask QueryPilot", "Evaluations"]
)

with ask_tab:
    st.subheader("Ask QueryPilot")
    question = st.text_area(
        "Ask a question about RetailStar",
        placeholder="e.g. What is considered low inventory?",
    )

    ask_button = st.button(
        "Ask QueryPilot",
        type="primary",
    )

    if ask_button:
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            response = httpx.post(
                "http://localhost:8000/ask",
                json={"question": question},
                timeout=30.0,
            )

            data = response.json()

            st.subheader("Answer")
            st.write(data["answer"])

            if data["sources"]:
                st.subheader("Sources")
                for source in data["sources"]:
                    st.write(f"- {source}")
            if data["requires_database"]:
                st.info("This question requires RetailStar database access.")

with eval_tab:
    st.subheader("Evaluation Results")