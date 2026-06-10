from components import LLM_MODEL, llm_client

def decompose_query(question):
    """
    Ask Llama 3.2 to break a comparative query into sub-queries
    """
    decompose_prompt = f"""You are an MLOps documentation assistant with expertise in 
Kubernetes, Docker and Jenkins.

Break this comparative question into exactly 2 simple sub-queries.
Each sub-query should focus on ONE concept only and start with "What is" or "How does".
Keep each sub-query within the same tool domain as the original question.

Examples:
- "difference between docker run and docker start" -> "What is docker run?" and "What is docker start?"
- "difference between namespace and deployment" -> "What is a Kubernetes namespace?" and "What is a Kubernetes deployment?"
- "difference between declarative and scripted pipeline" -> "What is a Jenkins declarative pipeline?" and "What is a Jenkins scripted pipeline?"

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

