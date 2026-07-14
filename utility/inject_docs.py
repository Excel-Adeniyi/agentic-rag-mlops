import os
import chromadb
from sentence_transformers import SentenceTransformer

# Configuration
from components.config.constants import CHUNK_SIZE, CHUNK_OVERLAP, BATCH_SIZE, DOCS_DIR
def chunk_text(text, chunk_size, overlap):
    """Split text into chunks with specified size and overlap."""
    chunks = []
    start = 0
    # Loop through the text and create chunks
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip(): # Only add non-empty chunks
            chunks.append(chunk)
        start = end - overlap # Move start forward by chunk size minus overlap
    return chunks   

def load_docs(folder):
    """Load all markdown files from docs folder"""
    docs = {}
    for filename in os.listdir(folder):
        if filename.endswith(".md"):
            filepath = os.path.join(folder, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                docs[filename] = f.read()
            print(f"Loaded: {filename} ({len(docs[filename])} characters)")
    return docs

# Load documents
print("Loading documents...")
documents = load_docs(DOCS_DIR)


#chunk all documents into smaller pieces to fit within LLM context window
print("\nChunking documents...")
all_chunks = []
all_chunk_ids = []
all_metadata = []

for filename, content in documents.items():
    chunks = chunk_text(content, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"{filename}: {len(chunks)} chunks created.")
    for i, chunk in enumerate(chunks):
        all_chunks.append(chunk)
        all_chunk_ids.append(f"{filename}_chunk_{i}")
        all_metadata.append({"source": filename, "chunk_index": i})
        
        
print(f"Total chunks created: {len(all_chunks)}")

#Embedding the documents and adding them to the collection in ChromaDB
print("\nEmbedding and adding chunks to ChromaDB...")
model = SentenceTransformer('all-MiniLM-L6-v2')

print("Creating ChromaDB client and collection...")
client = chromadb.PersistentClient(path="./chroma_db")

#Delete existing collection if it exists to start fresh
try:
    client.delete_collection(name="mlops_knowledge_base")
    print("Existing collection deleted.")
except:
    pass

collection = client.create_collection(name="mlops_knowledge_base")

# Embed in Batch to avoid memory issues with large documents

for i in range(0, len(all_chunks), BATCH_SIZE):
    batch_chunks = all_chunks[i:i+BATCH_SIZE]
    batch_ids = all_chunk_ids[i:i+BATCH_SIZE]
    batch_metadata = all_metadata[i:i+BATCH_SIZE]
    
    print(f"Processing batch {i//BATCH_SIZE + 1} ({len(batch_chunks)} chunks)...")
    
    # Get embeddings for the batch
    embeddings = model.encode(batch_chunks).tolist()
    
    # Add to ChromaDB collection
    collection.add(
        ids=batch_ids,
        embeddings=embeddings,
        documents=batch_chunks,
        metadatas=batch_metadata
    )
    print(f" Stored batch {i//BATCH_SIZE + 1} ({len(batch_chunks)} chunks) in ChromaDB.")
    print(f" Total chunks stored so far: {collection.count()}")
print("Your Knowledge base is ready!")