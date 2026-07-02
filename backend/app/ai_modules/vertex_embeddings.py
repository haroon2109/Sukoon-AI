import os
import logging
from typing import List
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class VertexEmbeddingService:
    """
    Service updated to support advanced multilingual RAG models:
    - BAAI/bge-m3 (Default, 1024 dims)
    - intfloat/multilingual-e5-large (1024 dims)
    - nomic-ai/nomic-embed-text-v1.5 (768 dims)
    Maintains class name for backwards compatibility.
    """
    def __init__(self):
        self.model_name = os.getenv("RAG_EMBEDDING_MODEL", "BAAI/bge-m3")
        self.initialized = False
        self.model = None

    def initialize(self):
        if self.initialized:
            return

        try:
            logger.info(f"Initializing Local Embedding Model '{self.model_name}'...")
            # trust_remote_code=True is required for models like Nomic Embed
            self.model = SentenceTransformer(self.model_name, trust_remote_code=True)
            self.initialized = True
            logger.info(f"Local Embedding Model '{self.model_name}' initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize local model: {e}")
            raise

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of strings locally using the configured model.
        Returns a list of float arrays (dimensions depend on the model, e.g., 1024 for BGE-M3).
        """
        if not self.initialized:
            self.initialize()
            
        try:
            # model.encode returns a numpy array, we convert to python float lists
            embeddings = self.model.encode(texts, normalize_embeddings=True)
            return [emb.tolist() for emb in embeddings]
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise

    def get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single string.
        """
        embeddings = self.get_embeddings([text])
        if embeddings:
            return embeddings[0]
        return []

# Singleton instance exported for use across the application
vertex_embeddings = VertexEmbeddingService()
