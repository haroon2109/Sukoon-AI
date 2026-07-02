import os
import json
import logging
from app.ai_modules.vertex_embeddings import vertex_embeddings
from app.services.qdrant_service import qdrant_service

logger = logging.getLogger(__name__)

VECTOR_STORE_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "vector_store.json")

class RAGService:
    def __init__(self):
        self.vector_store = []
        self._load_local_fallback()

    def _load_local_fallback(self):
        """Loads a local JSON fallback in case Qdrant is offline."""
        if os.path.exists(VECTOR_STORE_FILE):
            with open(VECTOR_STORE_FILE, "r", encoding="utf-8") as f:
                self.vector_store = json.load(f)
        else:
            logger.warning(f"Local fallback vector store not found at {VECTOR_STORE_FILE}")

    def retrieve_context(self, claim: str, top_k: int = 3) -> list:
        """
        Retrieves relevant context.
        Tier 1: Semantic vector search using Qdrant (Fact-checks, News, Gov, WHO).
        Tier 2: Falls back to the local mock data if Qdrant fails or is empty.
        """
        if not claim:
            return []

        try:
            # 1. Generate the Local HuggingFace vector (1024 dimensions via BGE-M3 by default)
            query_vector = vertex_embeddings.get_embedding(claim)
            if not query_vector:
                return []

            # 2. Attempt Qdrant search
            qdrant_results = qdrant_service.search(query_vector=query_vector, top_k=top_k)
            
            if qdrant_results:
                logger.info(f"Successfully retrieved {len(qdrant_results)} results from Qdrant.")
                return qdrant_results
            else:
                logger.debug("Qdrant search returned no results. Proceeding to fallback.")
                
        except Exception as e:
            logger.error(f"Failed to query Qdrant: {e}")

        # Tier 2: Fallback to lexical matching if Supabase is offline
        logger.info("Falling back to local RAG matching.")
        return self._local_lexical_fallback(claim, top_k)

    def _local_lexical_fallback(self, claim: str, top_k: int = 3) -> list:
        """Simple bag-of-words fallback."""
        import re
        words = set(re.findall(r'\w+', claim.lower()))
        stop_words = {'the', 'is', 'in', 'at', 'of', 'on', 'and', 'a', 'to', 'for', 'it', 'that', 'this', 'with'}
        claim_words = words - stop_words

        if not claim_words or not self.vector_store:
            return []

        scored_results = []
        for doc in self.vector_store:
            doc_text = doc.get("title", "") + " " + doc.get("text", "")
            doc_words = set(re.findall(r'\w+', doc_text.lower())) - stop_words
            
            if not doc_words:
                continue
                
            intersection = len(claim_words.intersection(doc_words))
            union = len(claim_words.union(doc_words))
            similarity = intersection / union if union > 0 else 0
            
            if similarity > 0.05:
                scored_results.append((similarity, doc))

        scored_results.sort(key=lambda x: x[0], reverse=True)
        
        final_results = []
        for sim, doc in scored_results[:top_k]:
            doc_copy = doc.copy()
            doc_copy["similarity"] = float(sim)
            final_results.append(doc_copy)
            
        return final_results

rag_service = RAGService()
