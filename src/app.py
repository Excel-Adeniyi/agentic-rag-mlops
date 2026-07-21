import os
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
for _p in (_ROOT, _ROOT / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import streamlit as st
from application import build_default_app_service

# Page config
st.set_page_config(
    page_title="MLOps Doc Assistant",
    page_icon="🔧",
    layout="wide"
)

if "app_service" not in st.session_state:
    st.session_state.app_service = build_default_app_service()

if "history" not in st.session_state:
    st.session_state.history = []

app_service = st.session_state.app_service

st.title("🔧 MLOps Documentation Assistant")
st.caption("Agentic RAG for Kubernetes, Docker and Jenkins Documentation")

with st.sidebar:
    st.header("System Info")
    st.write("**LLM:** Llama 3.2 via Ollama")
    st.write("**Evaluator:** Qwen 2.5 via Ollama")
    st.write("**Vector Store:** ChromaDB")
    st.write("**Embeddings:** all-MiniLM-L6-v2")
    st.write("**Knowledge Base:** 730 chunks")
    st.divider()
    mode = st.radio(
        "Select Pipeline:",
        ["Agentic RAG", "Baseline RAG", "Compare Both"]
    )
    run_eval = st.checkbox("Run Ragas Evaluation", value=True)
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.history = []
        st.rerun()

# Render history
for entry in st.session_state.history:
    with st.chat_message("user"):
        st.write(entry["query"])

    with st.chat_message("assistant"):
        if entry["mode"] == "Compare Both":
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Baseline RAG")
                st.write(entry["baseline"]["answer"])
                st.caption(f"Response time: {entry['baseline']['response_time']:.1f}s")
                if entry["baseline"].get("evaluation"):
                    ev = entry["baseline"]["evaluation"]
                    st.metric("Faithfulness", f"{ev['faithfulness']:.2f}")
                    st.metric("Answer Relevancy", f"{ev['answer_relevancy']:.2f}")
                    st.metric("Context Precision", f"{ev['context_precision']:.2f}")
                elif entry["baseline"].get("evaluation_error"):
                    st.warning(entry["baseline"]["evaluation_error"])
            with col2:
                st.subheader("Agentic RAG")
                st.write(entry["agentic"]["answer"])
                st.caption(f"Response time: {entry['agentic']['response_time']:.1f}s")
                if entry["agentic"].get("evaluation"):
                    ev = entry["agentic"]["evaluation"]
                    st.metric("Faithfulness", f"{ev['faithfulness']:.2f}")
                    st.metric("Answer Relevancy", f"{ev['answer_relevancy']:.2f}")
                    st.metric("Context Precision", f"{ev['context_precision']:.2f}")
                elif entry["agentic"].get("evaluation_error"):
                    st.warning(entry["agentic"]["evaluation_error"])
        else:
            st.subheader(f"{entry['mode']} Response")
            st.write(entry["answer"])
            st.caption(f"Response time: {entry['response_time']:.1f}s")
            if entry.get("evaluation"):
                ev = entry["evaluation"]
                m1, m2, m3 = st.columns(3)
                m1.metric("Faithfulness", f"{ev['faithfulness']:.2f}")
                m2.metric("Answer Relevancy", f"{ev['answer_relevancy']:.2f}")
                m3.metric("Context Precision", f"{ev['context_precision']:.2f}")
            elif entry.get("evaluation_error"):
                st.warning(entry["evaluation_error"])

# Chat input
query = st.chat_input("Ask a question about Kubernetes, Docker or Jenkins...")

if query:
    with st.chat_message("user"):
        st.write(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = app_service.run_query(mode, query, run_eval=run_eval)

        if mode == "Compare Both":
            baseline = response["baseline"]
            agentic = response["agentic"]
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Baseline RAG")
                st.write(baseline.answer)
                st.caption(f"Response time: {baseline.response_time:.1f}s")
                if baseline.evaluation:
                    st.metric("Faithfulness", f"{baseline.evaluation.faithfulness:.2f}")
                    st.metric("Answer Relevancy", f"{baseline.evaluation.answer_relevancy:.2f}")
                    st.metric("Context Precision", f"{baseline.evaluation.context_precision:.2f}")
                elif baseline.evaluation_error:
                    st.warning(baseline.evaluation_error)

            with col2:
                st.subheader("Agentic RAG")
                st.write(agentic.answer)
                st.caption(f"Response time: {agentic.response_time:.1f}s")
                if agentic.evaluation:
                    st.metric("Faithfulness", f"{agentic.evaluation.faithfulness:.2f}")
                    st.metric("Answer Relevancy", f"{agentic.evaluation.answer_relevancy:.2f}")
                    st.metric("Context Precision", f"{agentic.evaluation.context_precision:.2f}")
                elif agentic.evaluation_error:
                    st.warning(agentic.evaluation_error)

            entry = {
                "query": query,
                "mode": mode,
                "baseline": {
                    "answer": baseline.answer,
                    "response_time": baseline.response_time,
                    "evaluation": vars(baseline.evaluation) if baseline.evaluation else None,
                    "evaluation_error": baseline.evaluation_error,
                },
                "agentic": {
                    "answer": agentic.answer,
                    "response_time": agentic.response_time,
                    "evaluation": vars(agentic.evaluation) if agentic.evaluation else None,
                    "evaluation_error": agentic.evaluation_error,
                },
            }

        else:
            result = response["result"]
            st.subheader(f"{mode} Response")
            st.write(result.answer)
            st.caption(f"Response time: {result.response_time:.1f}s")
            if result.evaluation:
                m1, m2, m3 = st.columns(3)
                m1.metric("Faithfulness", f"{result.evaluation.faithfulness:.2f}")
                m2.metric("Answer Relevancy", f"{result.evaluation.answer_relevancy:.2f}")
                m3.metric("Context Precision", f"{result.evaluation.context_precision:.2f}")
            elif result.evaluation_error:
                st.warning(result.evaluation_error)

            entry = {
                "query": query,
                "mode": mode,
                "answer": result.answer,
                "response_time": result.response_time,
                "evaluation": vars(result.evaluation) if result.evaluation else None,
                "evaluation_error": result.evaluation_error,
            }

        st.session_state.history.append(entry)
