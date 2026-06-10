from components import LLM_MODEL, llm_client

def decompose_query(question):
    """
    Ask Llama 3.2 to break a comparative query into sub-queries
    """
    decompose_prompt = f"""You are a Kubernetes documentation assistant. 
Break this question into exactly 2 sub-queries about Kubernetes concepts.
Each sub-query must start with "What is a Kubernetes" or "How does Kubernetes".
Keep each sub-query simple and focused on one concept only.

Question: {question}

Reply with ONLY 2 sub-queries, one per line, nothing else."""

    response = llm_client.chat(
        model=LLM_MODEL,
        messages=[{'role': 'user', 'content': decompose_prompt}]
    )
    
    sub_queries = response['message']['content'].strip().split('\n')
    sub_queries = [q.strip() for q in sub_queries if q.strip()]
    
    print(f"Decomposed into {len(sub_queries)} sub-queries:")
    for q in sub_queries:
        print(f"  - {q}")
    
    return sub_queries

