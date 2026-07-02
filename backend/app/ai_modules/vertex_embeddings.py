import logging
from typing import List
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class VertexEmbeddingService:
    """
    Renamed internally to use BAAI/bge-small-en-v1.5 (Local HuggingFace Open Source)
    but class name kept the same to maintain backwards compatibility with existing imports.
    """
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self.model_name = model_name
        self.initialized = False
        self.model = None

    def initialize(self):
        if self.initialized:
            return

        try:
            logger.info(f"Initializing Local Embedding Model '{self.model_name}'...")
            self.model = SentenceTransformer(self.model_name)
            self.initialized = True
            logger.info(f"Local Embedding Model '{self.model_name}' initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize local model: {e}")
            raise

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of strings locally using bge-small.
        Returns a list of 384-dimensional float arrays.
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
