import os
import logging
from typing import List
try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False

logger = logging.getLogger(__name__)

class VertexEmbeddingService:
    """
    Service updated to support advanced multilingual RAG models.
    Falls back to deterministic mock embeddings if sentence-transformers is not installed
    or fails to load, preventing server boot failures and heavy memory usage.
    """
    def __init__(self):
        self.model_name = os.getenv("RAG_EMBEDDING_MODEL", "BAAI/bge-m3")
        self.initialized = False
        self.model = None

    def initialize(self):
        if self.initialized:
            return

        if not HAS_SENTENCE_TRANSFORMERS:
            logger.warning("sentence-transformers is not installed. Using lightweight deterministic mock embeddings.")
            self.initialized = True
            return

        try:
            logger.info(f"Initializing Local Embedding Model '{self.model_name}'...")
            # trust_remote_code=True is required for models like Nomic Embed
            self.model = SentenceTransformer(self.model_name, trust_remote_code=True)
            self.initialized = True
            logger.info(f"Local Embedding Model '{self.model_name}' initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize local model: {e}. Falling back to deterministic mock embeddings.")
            self.initialized = True

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of strings.
        """
        if not self.initialized:
            self.initialize()
            
        if not HAS_SENTENCE_TRANSFORMERS or self.model is None:
            import hashlib
            import random
            results = []
            for text in texts:
                sha = hashlib.sha256(text.encode('utf-8')).digest()
                seed = int.from_bytes(sha, byteorder='big')
                rng = random.Random(seed)
                vec = [rng.uniform(-1.0, 1.0) for _ in range(1024)]
                magnitude = sum(x*x for x in vec) ** 0.5
                if magnitude > 0:
                    vec = [x / magnitude for x in vec]
                results.append(vec)
            return results

        try:
            # model.encode returns a numpy array, we convert to python float lists
            embeddings = self.model.encode(texts, normalize_embeddings=True)
            return [emb.tolist() for emb in embeddings]
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            import hashlib
            import random
            results = []
            for text in texts:
                sha = hashlib.sha256(text.encode('utf-8')).digest()
                seed = int.from_bytes(sha, byteorder='big')
                rng = random.Random(seed)
                vec = [rng.uniform(-1.0, 1.0) for _ in range(1024)]
                magnitude = sum(x*x for x in vec) ** 0.5
                if magnitude > 0:
                    vec = [x / magnitude for x in vec]
                results.append(vec)
            return results

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
