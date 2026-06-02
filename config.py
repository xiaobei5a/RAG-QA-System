import os

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-r1:7b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 3
PERSIST_DIRECTORY = "./chroma_db"
UPLOAD_DIRECTORY = "./uploaded_documents"