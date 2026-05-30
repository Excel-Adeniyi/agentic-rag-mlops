# Agentic RAG for MLOps Pipeline Documentation and Troubleshooting

A local, privacy-first Retrieval-Augmented Generation (RAG) system that helps engineers query MLOps pipeline documentation using natural language. Built as part of an MSc Computer Science dissertation at Glasgow Caledonian University (2026).

> **Status:** Baseline RAG pipeline complete and verified. Agentic layer in active development.
> **Project Board:** Dissertation progress is tracked on the GitHub Project board [View dissertation progress](https://github.com/users/Excel-Adeniyi/projects/5)
---

## What It Does

Engineers working across MLOps tooling (Kubernetes, Docker, Jenkins, Ansible) spend significant time navigating fragmented documentation. This system allows an engineer to ask a natural language question and receive a grounded, accurate answer retrieved directly from a local knowledge base, without relying on cloud APIs or exposing sensitive infrastructure details.

**Example**

```
Question:  How do I restart a pod?
Answer:    To restart a Kubernetes pod, use the command:
           kubectl rollout restart deployment <deployment-name>.
           This recreates the pods in the deployment.
```

The system correctly retrieved this answer even though the question mentioned "pod" and the document described "deployment". Semantic retrieval understands meaning, not just keywords.

---

## Architecture

### Baseline Pipeline (built and verified)

```
User question
     ↓
Embed the question (SentenceTransformer → vector)
     ↓
Retrieve from ChromaDB (closest docs by meaning)
     ↓
Build grounded prompt (context + question)
     ↓
Generate with Llama 3.2 (local via Ollama)
     ↓
Grounded answer
```

### Agentic Layer (in development)

The agentic extension adds an LLM agent that:
- Decides whether retrieval is needed for a given query
- Evaluates whether retrieved context is sufficient to answer
- Re-retrieves with a refined query if the context is inadequate
- Routes complex queries through multi-step reasoning before generation

This is the core research contribution of the dissertation: evaluating whether agentic decision-making measurably improves response quality over a fixed RAG pipeline, specifically for MLOps documentation queries that vary widely in complexity.

---

## Tech Stack

| Component | Technology |
|---|---|
| Language model | Llama 3.2 via Ollama (local) |
| Embeddings | SentenceTransformers (all-MiniLM-L6-v2) |
| Vector store | ChromaDB |
| Orchestration | Python |
| Future: agent layer | LangChain |

**Runs entirely offline. No API keys. No cloud. No cost.**

---

## Getting Started

### Prerequisites

- Mac or Linux machine
- Python 3.11
- [Ollama](https://ollama.com) installed and running locally
- Llama 3.2 pulled via Ollama

```bash
ollama pull llama3.2
```

### Installation

```bash
# Clone the repo
git clone https://github.com/Excel-Adeniyi/agentic-rag-mlops.git
cd agentic-rag-mlops

# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies (in this order)
pip install "numpy<2"
pip install torch
pip install sentence-transformers chromadb ollama
```

> **Note:** The install order matters on Intel Macs. NumPy must be pinned below 2.0 for compatibility with the current torch version available on x86_64 architecture.

### Run the baseline pipeline

```bash
python3 rag_pipeline.py
```

---

## Project Structure

```
agentic-rag-mlops/
├── rag_pipeline.py        # Baseline RAG pipeline (complete)
├── requirements.txt       # Python dependencies
├── .gitignore
└── README.md
```

More modules will be added as the agentic layer is built out.

---

## Research Questions

1. How does an agentic retrieval layer affect response accuracy compared to a standard RAG pipeline when querying MLOps documentation?
2. What retrieval strategies does the agent select for different query types, and how do these decisions affect output quality?
3. What evaluation metrics most effectively capture the usefulness of generated responses in a developer and operations context?

---

## Author

**Ezekiel Adeniyi**
MSc Computer Science, Glasgow Caledonian University
[LinkedIn](https://www.linkedin.com/in/) | [GitHub](https://github.com/Excel-Adeniyi)

---

## License

MIT License. See [LICENSE](LICENSE) for details.