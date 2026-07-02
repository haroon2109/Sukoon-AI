import os
import json
import logging
from sqlalchemy import text
from app.db.session import SessionLocal
from app.ai_modules.vertex_embeddings import vertex_embeddings

logger = logging.getLogger(__name__)

VECTOR_STORE_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "vector_store.json")

class RAGService:
    def __init__(self):
        self.vector_store = []
        self._load_local_fallback()

    def _load_local_fallback(self):
        """Loads a local JSON fallback in case the Supabase connection fails."""
        if os.path.exists(VECTOR_STORE_FILE):
            with open(VECTOR_STORE_FILE, "r", encoding="utf-8") as f:
                self.vector_store = json.load(f)
        else:
            logger.warning(f"Local fallback vector store not found at {VECTOR_STORE_FILE}")

    def retrieve_context(self, claim: str, top_k: int = 3) -> list:
        """
        Retrieves relevant context.
        Tier 1: Attempts a true semantic vector search using pgvector on Supabase.
        Tier 2: Falls back to the local mock data if the database isn't connected.
        """
        if not claim:
            return []

        try:
            # 1. Generate the Local HuggingFace vector (384 dimensions via bge-small)
            query_vector = vertex_embeddings.get_embedding(claim)
            if not query_vector:
                return []

            # 2. Attempt Supabase pgvector search
            db = SessionLocal()
            try:
                # This assumes a table named 'documents' with a vector column 'embedding'
                # The query calculates cosine distance (<=>) using pgvector
                # Note: This will fail gracefully if the table doesn't exist or we are on SQLite
                query = text("""
                    SELECT title, text, source, date, 1 - (embedding <=> :vector) AS similarity
                    FROM documents
                    ORDER BY embedding <=> :vector
                    LIMIT :top_k
                """)
                
                # Format the vector as a string array for postgres
                vector_str = f"[{','.join(map(str, query_vector))}]"
                
                result = db.execute(query, {"vector": vector_str, "top_k": top_k}).fetchall()
                
                if result:
                    logger.info("Successfully retrieved RAG context from Supabase pgvector.")
                    return [
                        {
                            "title": row.title,
                            "text": row.text,
                            "source": row.source,
                            "date": row.date,
                            "similarity": float(row.similarity)
                        } for row in result
                    ]
            except Exception as db_e:
                # Log at debug so it doesn't spam warnings if Supabase isn't configured during local dev
                logger.debug(f"pgvector search bypassed (Supabase likely not configured): {db_e}")
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Failed to generate embedding or query database: {e}")

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
