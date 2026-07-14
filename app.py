import streamlit as st
from application import build_default_app_service

# Page config
st.set_page_config(
    page_title="MLOps Doc Assistant",
    page_icon="🔧",
    layout="wide"
)

app_service = build_default_app_service()

st.title("🔧 MLOps Documentation Assistant")
st.caption("Agentic RAG for Kubernetes, Docker and Jenkins Documentation")

with st.sidebar:
    st.header("System Info")
    st.write("**LLM:** Llama 3.2 via Ollama")
    st.write("**Evaluator:** Qwen 2.5 via Ollama")
    st.write("**Vector Store:** ChromaDB")
    st.write("**Embeddings:** all-MiniLM-L6-v2")
    st.write("**Knowledge Base:** 719 chunks")
    st.divider()
    mode = st.radio(
        "Select Pipeline:",
        ["Agentic RAG", "Baseline RAG", "Compare Both"]
    )
    run_eval = st.checkbox("Run Ragas Evaluation", value=True)

query = st.text_input("Ask a question about Kubernetes, Docker or Jenkins:")

if query:
    response = app_service.run_query(mode, query, run_eval=run_eval)

    if mode == "Compare Both":
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Baseline RAG")
            baseline = response["baseline"]
            st.write(baseline.answer)
            st.caption(f"Response time: {baseline.response_time:.1f}s")

        with col2:
            st.subheader("Agentic RAG")
            agentic = response["agentic"]
            st.write(agentic.answer)
            st.caption(f"Response time: {agentic.response_time:.1f}s")

        if run_eval:
            st.divider()
            st.subheader("📊 Ragas Evaluation Scores")
            eval_col1, eval_col2 = st.columns(2)

            with eval_col1:
                if baseline.evaluation:
                    st.metric("Faithfulness", f"{baseline.evaluation.faithfulness:.2f}")
                    st.metric("Answer Relevancy", f"{baseline.evaluation.answer_relevancy:.2f}")
                    st.metric("Context Precision", f"{baseline.evaluation.context_precision:.2f}")
                else:
                    st.warning(baseline.evaluation_error)

            with eval_col2:
                if agentic.evaluation:
                    st.metric("Faithfulness", f"{agentic.evaluation.faithfulness:.2f}")
                    st.metric("Answer Relevancy", f"{agentic.evaluation.answer_relevancy:.2f}")
                    st.metric("Context Precision", f"{agentic.evaluation.context_precision:.2f}")
                else:
                    st.warning(agentic.evaluation_error)

    else:
        result = response["result"]
        st.subheader(f"{mode} Response")
        st.write(result.answer)
        st.caption(f"Response time: {result.response_time:.1f}s")

        if run_eval:
            st.divider()
            st.subheader("📊 Ragas Evaluation Scores")
            if result.evaluation:
                m1, m2, m3 = st.columns(3)
                m1.metric("Faithfulness", f"{result.evaluation.faithfulness:.2f}")
                m2.metric("Answer Relevancy", f"{result.evaluation.answer_relevancy:.2f}")
                m3.metric("Context Precision", f"{result.evaluation.context_precision:.2f}")
            else:
                st.warning(result.evaluation_error)
