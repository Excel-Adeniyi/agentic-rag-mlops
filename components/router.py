import re
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


def _is_exact_definition_question(question_lower):
    """
    Returns True only if the question is asking for a bare top-level definition
    of the tool itself (e.g. 'what is kubernetes' / 'what is docker?'),
    NOT sub-concepts like 'what is a kubernetes namespace'.
    """
    # Match "what is <tool>" with nothing substantive after it
    exact_def_pattern = re.compile(
        r"^what\s+is\s+(kubernetes|docker|jenkins|ansible|a\s+container|devops|mlops)[?.]?\s*$"
    )
    return bool(exact_def_pattern.match(question_lower.strip()))


def should_retrieve(question):
    """
    Hybrid routing: rule-based for obvious cases,
    LLM-based for ambiguous ones.

    Retrieve patterns are checked FIRST so that specific questions about
    sub-concepts (e.g. 'what is a kubernetes pod?') are not incorrectly
    short-circuited by the broad direct patterns.
    """
    question_lower = question.lower()

    # Rule-based RETRIEVE: clearly needs documentation
    retrieve_patterns = [
        "how do i", "how to", "command", "kubectl",
        "error", "crash", "failing", "not working",
        "difference between", "compare", "vs ",
        "configure", "setup", "install", "deploy",
        "stuck", "pipeline", "jenkins", "docker", "kubernetes",
        "cannot", "unable", "failed", "issue",
        "pod", "node", "namespace", "deployment", "service",
        "container", "image", "volume", "network",
    ]
    for pattern in retrieve_patterns:
        if pattern in question_lower:
            print(f"Routing: Rule-based RETRIEVE (matched '{pattern}')")
            return True

    # Rule-based DIRECT: bare top-level "what is <tool>" questions only
    if _is_exact_definition_question(question_lower):
        print("Routing: Rule-based DIRECT")
        return False

    # Ambiguous: ask the LLM
    print("Routing: LLM decision")
    decision_prompt = f"""You are an MLOps assistant specialising in Kubernetes, Docker, and Jenkins.
Does this question require searching technical documentation to answer accurately?

Question: {question}

Reply with ONLY one word: RETRIEVE or DIRECT"""

    response = llm_client.chat(
        model=LLM_MODEL,
        messages=[{'role': 'user', 'content': decision_prompt}]
    )

    decision = response['message']['content'].strip().upper()
    return "RETRIEVE" in decision


