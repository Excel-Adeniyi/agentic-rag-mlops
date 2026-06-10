import chromadb
from sentence_transformers import SentenceTransformer
import ollama

print("All three libraries are installed and can be imported successfully.")

# Test the embedding model loads
model = SentenceTransformer('all-MiniLM-L6-v2')
print("SentenceTransformer model loaded successfully.")

# Test Ollama connection
response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": "Hello, Ollama!"}])
print("Ollama response:", response['message']['content'])