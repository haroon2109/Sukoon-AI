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

    def get_embedding(self, text: str) -> set:
        """
        Mock embedding generator using simple bag-of-words for lexical overlap
        instead of random hashing to prevent noise.
        """
        import re
        words = re.findall(r'\w+', text.lower())
        # Filter out common stop words to improve basic matching
        stop_words = {'the', 'is', 'in', 'at', 'of', 'on', 'and', 'a', 'to', 'for', 'it', 'that', 'this', 'with'}
        return set([w for w in words if w not in stop_words])

    def retrieve_context(self, claim: str, top_k: int = 3) -> list:
        """
        Retrieves relevant context by calculating Jaccard similarity between
        the claim words and stored document words.
        """
        if not self.vector_store:
            return []

        try:
            claim_words = self.get_embedding(claim)
        except Exception as e:
            logger.error(f"Failed to embed claim: {e}")
            return []
            
        if not claim_words:
            return []

        scored_results = []
        for doc in self.vector_store:
            # We compute the embedding on the fly for the doc if not stored as words, 
            # but actually vector_store has random float arrays right now from generate_data.py
            # So let's just use the doc's "title" and "text" to compute overlap dynamically
            doc_text = doc.get("title", "") + " " + doc.get("text", "")
            doc_words = self.get_embedding(doc_text)
            
            if not doc_words:
                continue
                
            intersection = len(claim_words.intersection(doc_words))
            union = len(claim_words.union(doc_words))
            similarity = intersection / union if union > 0 else 0
            
            # Enforce a minimum threshold so we don't return completely unrelated junk!
            if similarity > 0.05:
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
