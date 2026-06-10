from components import collection, model, decompose_query

def retrieve_context(question, n_results=3):
    """Embed the question and retrieve relevant chunks from ChromaDB"""
    question_embedding = model.encode(question).tolist()
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )
    return results['documents'][0], results['distances'][0]



def multi_query_retrieve(question, n_results=3):
    """
    Retrieve separately for each sub-query and combine results
    """
    sub_queries = decompose_query(question)
    
    all_docs = []
    all_ids = []
    all_distances = []
    
    for sub_query in sub_queries:
        embedding = model.encode(sub_query).tolist()
        results = collection.query(
            query_embeddings=[embedding],
            n_results=n_results
        )
        
        for doc, dist, id in zip(
            results['documents'][0],
            results['distances'][0],
            results['ids'][0]
        ):
            # Avoid duplicate chunks
            if id not in all_ids:
                all_docs.append(doc)
                all_ids.append(id)
                all_distances.append(dist)
    
    print(f"Multi-query retrieved {len(all_docs)} unique chunks total")
    return all_docs, all_distances

