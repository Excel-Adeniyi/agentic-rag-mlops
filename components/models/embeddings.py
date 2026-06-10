from sentence_transformers import SentenceTransformer

from components.config.constants import EMBEDDING_MODEL
# Load embedding model and connect to knowledge base

model = SentenceTransformer(EMBEDDING_MODEL)
