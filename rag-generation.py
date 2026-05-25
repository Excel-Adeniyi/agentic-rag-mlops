import chromadb
from sentence_transformers import SentenceTransformer
import ollama

# Each string is a "document" - a piece of knowledge the system can retrieve.
documents = [
    "To restart a Kubernetes pod, use the command: kubectl rollout restart deployment <deployment-name>. This recreates the pods in the deployment.",
    "To view logs from a Kubernetes pod, use: kubectl logs <pod-name>. Add -f to follow the logs in real time.",
    "A Docker container that keeps crashing usually has an error in its startup command. Check logs with: docker logs <container-id>.",
    "To list all running Docker containers, use: docker ps. To include stopped containers, use: docker ps -a.",
    "Jenkins build failures are often caused by missing environment variables or incorrect pipeline syntax. Check the console output for the specific error.",
    "To check the status of all pods in a Kubernetes namespace, run: kubectl get pods -n <namespace>."
]


# Load the embedding model

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


# Create a ChromaDB client and collection

client = chromadb.PersistentClient(path="./chroma_db")
#If you have a local ChromaDB server running, you can connect to it like this:
collection = client.get_or_create_collection(name="mlops_knowledge_base")

#Embedding the documents and adding them to the collection

# Quick check that our documents loaded

for i, doc in enumerate(documents):
    embedding = embedding_model.encode(doc).tolist()  # Get the embedding for the document
    collection.add(
        ids=[f"doc_{i}"],  # Unique ID for each document
        embeddings=[embedding],  # The embedding vector
        documents=[doc]  # The original document
    )
    

# --- RETRIEVAL ---
# Take a user question and find the most relevant documents

question = "How do I restart a pod?"

# Embed the question using the SAME model we used for the documents
# This is critical - both must be in the same vector space to compare
question_embedding = embedding_model.encode(question).tolist()

# Ask ChromaDB for the 2 most similar documents
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=2
)

print(f"\nQuestion: {question}\n")
print("Most relevant documents retrieved:")
for i, doc in enumerate(results['documents'][0]):
    distance = results['distances'][0][i]


#combined the retrieval results into a single string to send to the LLM    
retrieved_docs = results['documents'][0]
context = "\n".join(retrieved_docs)   


# Build a prompt that grounds the LLM in our retrieved context
# This is "prompt engineering" - we explicitly tell the LLM to use the retrieved information to answer the question
prompt = f"""
You are an expert MLOps assistant. Answer the question using ONLY the context provided below.
If the context does not contain the answer, say so honestly.

Context:
{context}

Question:
{question}

Answer:
"""

# Send the prompt to llama3.2 runnning locally via Ollama
print("\n Generating grounded answer with Llama 3.2 ...\n")
response = ollama.chat(model = 'llama3.2', messages=[{"role": "user", "content": prompt}])

print("=" * 60)
print("Generated Answer:")
print("=" * 60)
print(response['message']['content'])
