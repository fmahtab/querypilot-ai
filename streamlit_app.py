import httpx
import streamlit as st
from app.services.evals.runner import run_evals


st.set_page_config(
    page_title="QueryPilot AI",
    page_icon="📊",
    layout="wide",
)

st.title("QueryPilot AI")
st.caption("AI-powered business analytics copilot for RetailStar")

if "messages" not in st.session_state:
    st.session_state.messages = []


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

    clear_button = st.button(
        "Clear conversation",
    )
    if clear_button:
        st.session_state.messages = []
        st.rerun()
       
    if ask_button:
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            history = [
                {
                    "role": message["role"],
                    "content": message["content"],
                }
                for message in st.session_state.messages
            ]
            with st.spinner("Thinking..."):

                response = httpx.post(
                    "http://localhost:8000/ask",
                    json={
                        "question": question,
                        "history": history
                    },
                    timeout=30.0,
                )

                data = response.json()
                st.session_state.messages.append(
                    {
                        "role": "user",
                        "content": question,
                    }
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": data["answer"],
                        "sources": data["sources"],
                        "requires_database": data["requires_database"]
                    }
                )
                
                st.rerun()
            
    messages = st.session_state.messages
    if len(messages) >= 2:
        latest_turn = messages[-2:]
        older_messages = messages[:-2]
    else:
        latest_turn = messages
        older_messages = []

    # Display most recent turn
    if latest_turn:
        st.subheader("Latest Response")

    for message in latest_turn:
            with st.chat_message(message["role"]):
                st.write(message["content"])

                if message["role"] == "assistant":
                    if message.get("sources"):
                        st.caption(
                            "Sources: " + ", ".join(message["sources"])
                        )

    # Display older conversation
    if older_messages:
            st.subheader("History")
            for message in older_messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

                    if message["role"] == "assistant":
                        if message.get("sources"):
                            st.caption(
                                "Sources: " + ", ".join(message["sources"])
                            )



    


with eval_tab:
    st.subheader("Eval Results")
    run_eval_button = st.button(
        "Run Evaluations",
        type="primary",
    )
    if run_eval_button:
        with st.spinner("Running evaluations..."):
            eval_results = run_evals()
            st.metric(
                "Score",
                f"{eval_results['score']:.1f}%",
            )

            st.write(
                f"Passed: {eval_results['passed_cases']} / "
                f"{eval_results['total_cases']}"
            )

            st.subheader("Evaluation Details")

            for result in eval_results["results"]:
                if result["passed"]:
                    st.success(f"PASS | {result['question']}")
                else:
                    st.error(f"FAIL | {result['question']}")

                    for check in result["checks"]:
                        if not check["passed"]:
                            st.write(f"- {check['message']}")

            