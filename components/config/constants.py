import ollama
# All configuration constants
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
CHROMA_PATH = './chroma_db'
COLLECTION_NAME = 'mlops_knowledge_base'
LLM_MODEL = 'llama3.2'
CHUNK_RESULTS = 3
DOCS_DIR = "./docs"  # Directory containing your documents
CHUNK_SIZE = 500  # Number of characters per chunk
CHUNK_OVERLAP = 50  # Number of characters to overlap between chunks
BATCH_SIZE = 50   # Adjust based on your memory constraints
RETRY_RESULTS = 5
llm_client = ollama