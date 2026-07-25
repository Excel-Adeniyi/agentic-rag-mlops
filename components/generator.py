from components import LLM_MODEL, llm_client, is_meta_question

SCOPE_RESPONSE = """I am an MLOps documentation assistant specialising in three tools: 
Kubernetes, Docker and Jenkins. I can help with:
- Kubernetes: pod management, deployments, namespaces, troubleshooting
- Docker: container commands, networking, image management
- Jenkins: pipeline configuration, CI/CD troubleshooting

I do not have documentation for other MLOps tools such as cloud platforms, 
model serving frameworks, or CI/CD alternatives outside Jenkins."""

def generate_answer(question, context=None):
    """Generate a final answer, with or without context"""
    if is_meta_question(question):
        return SCOPE_RESPONSE

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
        messages=[{'role': 'user', 'content': prompt}],
        options={'temperature': 0}
    )
    return response['message']['content']
