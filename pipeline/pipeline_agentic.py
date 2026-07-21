from components import (
    should_retrieve,
    is_comparative_query,
    multi_query_retrieve,
    retrieve_context,
    retrieve_context_expanded,
    is_meta_question,
    is_context_sufficient,
    generate_answer,
    collection
)

def agentic_rag(question):
    """
    The full agentic pipeline with two decision points:
    1. Pre-retrieval routing (retrieve or direct)
    2. Post-retrieval context evaluation (sufficient or insufficient)
    """
    print("Pipeline: Agentic RAG")
    print(f"Question: {question}")

    if is_meta_question(question):
        return generate_answer(question), []

    needs_retrieval = should_retrieve(question)
    print(f"Agent Decision 1 - Retrieve: {needs_retrieval}")

    if not needs_retrieval:
        return generate_answer(question, context=None), []

    if is_comparative_query(question):
        context, distances = multi_query_retrieve(question)
    else:
        context, distances = retrieve_context(question)

    sufficient = is_context_sufficient(question, context)
    print(f"Agent Decision 2 - Context sufficient: {sufficient}")

    if not sufficient:
        context, distances = retrieve_context_expanded(question, n_results=5)

    return generate_answer(question, context=context), context