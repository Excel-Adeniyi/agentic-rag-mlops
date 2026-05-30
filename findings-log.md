Finding 4: Knowledge Base Gap vs Pipeline Failure
Date: 29/05/2026
Query: "What is the difference between a namespace and a deployment?"
System behaviour: Agent correctly routed to RETRIEVE. Retrieved 3 chunks. Context evaluated as sufficient. Generated an honest response acknowledging the documentation did not directly address the comparison.
Analysis: The weak answer on this query is not a pipeline failure. It is a knowledge base gap. The ingested Kubernetes documentation does not contain a document that directly compares namespaces and deployments. The agent behaved correctly by retrieving and honestly acknowledging the limitation rather than hallucinating. This distinguishes two distinct failure types in RAG systems: pipeline failures (wrong routing, hallucination) and knowledge base gaps (correct routing, insufficient source material).
Implication: Two solutions exist. First, augment the knowledge base with curated comparison documents. Second, implement multi-query retrieval where the agent retrieves separately for each concept and synthesises the results. The second approach is more generalisable and represents a stronger research contribution.


============================================================
TEST 3: Comparative query
============================================================
Question: What is the difference between a namespace and a deployment?
------------------------------------------------------------
Routing: Rule-based RETRIEVE
Agent Decision 1 - Retrieve: True
Retrieved 3 chunks (distances: ['0.761', '0.908', '0.959'])
Agent Decision 2 - Context sufficient: True

Answer:
The context does not provide enough information to answer the question. The context only provides general information about namespaces, their usage, and working with them, but it doesn't specifically address the difference between a namespace and a deployment. It mentions that resources can be in one namespace or another, but it doesn't clarify what a deployment is in relation to a namespace.