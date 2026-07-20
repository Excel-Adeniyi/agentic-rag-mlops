# pipeline_baseline.py
# Baseline RAG pipeline - fixed five step sequence
# No agent decision making, every query follows the same path

from components import retrieve_context, generate_answer, collection

def baseline_rag(question):
    """
    Fixed five step baseline RAG pipeline:
    1. Embed the question
    2. Retrieve from ChromaDB
    3. Build grounded prompt
    4. Generate with Llama 3.2
    5. Return answer
    """
    context, distances = retrieve_context(question)
    answer = generate_answer(question, context=context)
    return answer, context
