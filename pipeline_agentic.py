from components import should_retrieve, is_comparative_query, multi_query_retrieve, retrieve_context, is_context_sufficient, generate_answer, collection

print(f"Connected to knowledge base: {collection.count()} chunks available\n")


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
    
    # Check if comparative query needs multi-query retrieval
    if is_comparative_query(question):
        print("Using multi-query retrieval for comparative query")
        context, distances = multi_query_retrieve(question)
        print(f"Multi-query retrieved {len(context)} chunks")
    else:
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
# print("=" * 60)
# print("TEST 1: General knowledge query")
# print("=" * 60)
# question1 =  'What is Kubernetes?'
# agentic_rag(question1)
# # agentic_rag("What is Kubernetes?")

# print("=" * 60)
# print("TEST 2: Symptom-based query")
# print("=" * 60)
# question2 =  'My pod keeps crashing, what should I do?'
# agentic_rag(question2)
# # agentic_rag("My pod keeps crashing, what should I do?")

print("=" * 60)
print("TEST 3: Comparative query")
print("=" * 60)
question3 =  'What is the difference between a namespace and a deployment?' 
agentic_rag(question3)
# agentic_rag("What is the difference between a namespace and a deployment?")