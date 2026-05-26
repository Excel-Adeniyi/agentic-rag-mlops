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
    Decision 1: Ask the LLM whether this question needs
    retrieval from the knowledge base or can be answered directly.
    """
    decision_prompt = f"""You are an MLOps assistant deciding whether to search 
a documentation knowledge base before answering.

Question: {question}

Does this question require searching technical documentation to answer accurately,
or is it general knowledge you can answer directly?

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
agentic_rag("What is Kubernetes?")

print("=" * 60)
print("TEST 2: Symptom-based query")
print("=" * 60)
agentic_rag("My pod keeps crashing, what should I do?")

print("=" * 60)
print("TEST 3: Comparative query")
print("=" * 60)
agentic_rag("What is the difference between a namespace and a deployment?")