import os
import json
import logging
import numpy as np
from google import genai

logger = logging.getLogger(__name__)

VECTOR_STORE_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "vector_store.json")

class RAGService:
    def __init__(self):
        self.vector_store = []
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self._load_vector_store()

    def _load_vector_store(self):
        """Loads the pre-computed embeddings and metadata from disk."""
        if os.path.exists(VECTOR_STORE_FILE):
            with open(VECTOR_STORE_FILE, "r", encoding="utf-8") as f:
                self.vector_store = json.load(f)
            logger.info(f"Loaded {len(self.vector_store)} vectors into RAG.")
        else:
            logger.warning(f"Vector store not found at {VECTOR_STORE_FILE}")

    def get_embedding(self, text: str) -> np.ndarray:
        """
        Mock embedding generator for MVP since AI Studio key lacks text-embedding-004.
        Generates a deterministic 128-dimensional vector using text hashing.
        """
        np.random.seed(abs(hash(text)) % (2**32))
        vec = np.random.rand(128)
        vec = vec / np.linalg.norm(vec)
        return vec

    def retrieve_context(self, claim: str, top_k: int = 3) -> list:
        """
        Retrieves relevant context by calculating cosine similarity between
        the claim embedding and stored document embeddings.
        """
        if not self.vector_store:
            return []

        try:
            claim_embedding = self.get_embedding(claim)
        except Exception as e:
            logger.error(f"Failed to embed claim: {e}")
            return []

        scored_results = []
        for doc in self.vector_store:
            doc_emb = np.array(doc["embedding"])
            # Cosine similarity
            similarity = np.dot(claim_embedding, doc_emb) / (np.linalg.norm(claim_embedding) * np.linalg.norm(doc_emb))
            scored_results.append((similarity, doc))

        # Sort by similarity descending
        scored_results.sort(key=lambda x: x[0], reverse=True)
        
        # Return top K results with injected similarity score
        final_results = []
        for sim, doc in scored_results[:top_k]:
            doc_copy = doc.copy()
            doc_copy["similarity"] = float(sim)
            final_results.append(doc_copy)
            
        return final_results

rag_service = RAGService()
