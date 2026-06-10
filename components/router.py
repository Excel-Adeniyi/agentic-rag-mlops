from components import LLM_MODEL, llm_client

"""This module contains the routing logic to decide how to handle each query:
- Is it a comparative query that needs decomposition?
- Should we retrieve from the knowledge base or answer directly?
"""

def is_comparative_query(question):
    """
    Detect whether a query is comparative and needs multi-query retrieval
    """
    question_lower = question.lower()
    
    comparative_patterns = [
        "difference between",
        "which is better",
        "better than",
        " vs ",
        "versus",
        "compare",
        "comparison",
        "when to use",
        "should i use",
        " or ",
    ]
    
    for pattern in comparative_patterns:
        if pattern in question_lower:
            print(f"Comparative query detected: '{pattern}' pattern matched")
            return True
    
    return False


def should_retrieve(question):
    """
    Hybrid routing: rule-based for obvious cases,
    LLM-based for ambiguous ones.
    """
    question_lower = question.lower()
    # Rule-based DIRECT: clearly general knowledge questions
    direct_patterns = [
        "what is kubernetes",
        "what is docker", 
        "what is jenkins",
        "what is ansible",
        "what is a container",
        "what is devops",
        "what is mlops"
    ]
    
    for pattern in direct_patterns:
        if pattern in question_lower:
            print("Routing: Rule-based DIRECT")
            return False
    # Rule-based RETRIEVE: clearly needs documentation
    retrieve_patterns = [
        "how do i", "how to", "command", "kubectl",
        "error", "crash", "failing", "not working",
        "difference between", "compare", "vs ",
        "configure", "setup", "install", "deploy",
            "stuck", "pipeline", "jenkins", "docker",
    "cannot", "unable", "failed", "issue"
    ]
    for pattern in retrieve_patterns:
        if pattern in question_lower:
            print("Routing: Rule-based RETRIEVE")
            return True
    # Ambiguous: ask the LLM
    print("Routing: LLM decision")
    decision_prompt = f"""You are an MLOps assistant. Does this question 
require searching Kubernetes documentation to answer accurately?

Question: {question}

Reply with ONLY one word: RETRIEVE or DIRECT"""

    response = llm_client.chat(
        model=LLM_MODEL,
        messages=[{'role': 'user', 'content': decision_prompt}]
    )
    
    decision = response['message']['content'].strip().upper()
    return "RETRIEVE" in decision


