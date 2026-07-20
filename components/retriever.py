from components import collection, model, decompose_query, expand_query


def retrieve_context(question, n_results=3):
    """Embed the question and retrieve relevant chunks from ChromaDB"""
    question_embedding = model.encode(question).tolist()
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )
    return results['documents'][0], results['distances'][0]


def retrieve_context_expanded(question, n_results=3):
    """
    Retrieve using query expansion: rewrites the user query into documentation-style
    variants before embedding, so natural language like 'how to restart docker
    container' finds the right docs. Used as a fallback when plain retrieval
    (retrieve_context) doesn't return sufficient context, since blending in
    LLM-rewritten variants can pull in off-topic chunks for queries that already
    match well on their own.
    """
    variants = expand_query(question)
    # Always include the original query
    all_queries = [question] + [v for v in variants if v != question]

    seen_ids = set()
    all_docs = []
    all_distances = []

    for q in all_queries:
        embedding = model.encode(q).tolist()
        results = collection.query(
            query_embeddings=[embedding],
            n_results=n_results,
            include=["documents", "distances"],
        )
        for doc, dist, doc_id in zip(
            results["documents"][0],
            results["distances"][0],
            results["ids"][0],
        ):
            if doc_id not in seen_ids:
                seen_ids.add(doc_id)
                all_docs.append(doc)
                all_distances.append(dist)

    # Sort by distance (ascending = most similar first) and return top n_results
    ranked = sorted(zip(all_distances, all_docs), key=lambda x: x[0])
    top_docs = [doc for _, doc in ranked[:n_results]]
    top_dists = [dist for dist, _ in ranked[:n_results]]

    print(f"Query expansion retrieved {len(seen_ids)} unique chunks, returning top {len(top_docs)}")
    return top_docs, top_dists



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

