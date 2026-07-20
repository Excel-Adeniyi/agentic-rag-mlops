from components import LLM_MODEL, llm_client

"""This component evaluates whether the retrieved context is sufficient to answer the question accurately.
It is used as a decision point in the agentic RAG pipeline.
"""

def is_context_sufficient(question, context):
    """
    Decision 2: Ask the LLM whether the retrieved context
    is good enough to answer the question properly.
    """
    evaluation_prompt = f"""You are evaluating whether retrieved documentation 
is sufficient to answer a question accurately.

Question: {question}

Retrieved context:
{chr(10).join(context)}

Is this context sufficient to give a complete, accurate answer?
Reply with ONLY one word: SUFFICIENT or INSUFFICIENT"""

    response = llm_client.chat(
        model=LLM_MODEL,
        messages=[{'role': 'user', 'content': evaluation_prompt}],
        options={'temperature': 0}
    )
    
    decision = response['message']['content'].strip().upper()
    return "SUFFICIENT" in decision