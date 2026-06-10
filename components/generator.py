from components import LLM_MODEL, llm_client

def generate_answer(question, context=None):
    """Generate a final answer, with or without context"""
    if context:
        prompt = f"""You are an expert MLOps assistant. 
Answer the question using ONLY the context provided below.
If the context does not contain the answer, say so honestly.

Context:
{chr(10).join(context)}

Question: {question}

Answer:"""
    else:
        prompt = f"""You are an expert MLOps assistant.
Answer this question from your general knowledge:

Question: {question}

Answer:"""

    response = llm_client.chat(
        model=LLM_MODEL,
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response['message']['content']
