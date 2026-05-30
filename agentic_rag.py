import chromadb
from sentence_transformers import SentenceTransformer
import ollama

# Load embedding model and connect to knowledge base
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("mlops_knowledge_base")

print(f"Connected to knowledge base: {collection.count()} chunks available\n")

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
        "configure", "setup", "install", "deploy"
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

    response = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': decision_prompt}]
    )
    
    decision = response['message']['content'].strip().upper()
    return "RETRIEVE" in decision

def retrieve_context(question, n_results=3):
    """Embed the question and retrieve relevant chunks from ChromaDB"""
    question_embedding = model.encode(question).tolist()
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )
    return results['documents'][0], results['distances'][0]

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

    response = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': evaluation_prompt}]
    )
    
    decision = response['message']['content'].strip().upper()
    return "SUFFICIENT" in decision

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

    response = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response['message']['content']

def agentic_rag(question):
    """
    The full agentic pipeline with two decision points.
    """
    print(f"Question: {question}")
    print("-" * 60)
    
    # Decision 1: Should we retrieve?
    needs_retrieval = should_retrieve(question)
    print(f"Agent Decision 1 - Retrieve: {needs_retrieval}")
    
    if not needs_retrieval:
        print("Agent chose DIRECT answer (no retrieval needed)")
        answer = generate_answer(question, context=None)
        print(f"\nAnswer:\n{answer}\n")
        return answer
    
    # Retrieve context
    context, distances = retrieve_context(question)
    print(f"Retrieved {len(context)} chunks (distances: {[f'{d:.3f}' for d in distances]})")
    
    # Decision 2: Is context sufficient?
    sufficient = is_context_sufficient(question, context)
    print(f"Agent Decision 2 - Context sufficient: {sufficient}")
    
    if not sufficient:
        print("Agent re-retrieving with more results...")
        context, distances = retrieve_context(question, n_results=5)
        print(f"Retrieved {len(context)} chunks on retry")
    
    # Generate grounded answer
    answer = generate_answer(question, context=context)
    print(f"\nAnswer:\n{answer}\n")
    return answer

# Test with your three query types
print("=" * 60)
print("TEST 1: General knowledge query")
print("=" * 60)
question1 = input("Enter a general knowledge question (e.g. 'What is Kubernetes?'): ")
agentic_rag(question1)
# agentic_rag("What is Kubernetes?")

print("=" * 60)
print("TEST 2: Symptom-based query")
print("=" * 60)
question2 = input("Enter a symptom-based question (e.g. 'My pod keeps crashing, what should I do?'): ")
agentic_rag(question2)
# agentic_rag("My pod keeps crashing, what should I do?")

print("=" * 60)
print("TEST 3: Comparative query")
print("=" * 60)
question3 = input("Enter a comparative question (e.g. 'What is the difference between a namespace and a deployment?'): ")
agentic_rag(question3)
# agentic_rag("What is the difference between a namespace and a deployment?")