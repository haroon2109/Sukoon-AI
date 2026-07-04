import os
import uuid
import logging
from typing import List, Dict, Any

try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
    HAS_QDRANT = True
except ImportError:
    HAS_QDRANT = False

logger = logging.getLogger(__name__)

class QdrantService:
    """
    Qdrant vector database wrapper for RAG retrieval.
    Connects to Qdrant Cloud if QDRANT_URL and QDRANT_API_KEY are provided.
    Otherwise falls back to a local memory instance for development/MVP testing.
    """
    def __init__(self):
        self.collection_name = "sukoon_facts"
        self.vector_size = int(os.getenv("QDRANT_VECTOR_SIZE", "1024")) # Default to 1024 for BGE-M3
        
        if not HAS_QDRANT:
            logger.warning("qdrant-client is not installed. Qdrant Service is disabled.")
            self.client = None
            return
            
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        
        # Exponential backoff reconnection parameters for managed Qdrant DB instances
        import time
        max_attempts = 5
        delay = 1.0
        backoff_factor = 2.0
        
        for attempt in range(1, max_attempts + 1):
            try:
                if qdrant_url and qdrant_api_key:
                    logger.info(f"Initializing Qdrant Cloud client (attempt {attempt}/{max_attempts})...")
                    self.client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key, timeout=10.0)
                else:
                    logger.info("Initializing local in-memory Qdrant client (stateless)...")
                    self.client = QdrantClient(":memory:")
                    
                self._ensure_collection()
                break  # Connection successful
            except Exception as e:
                logger.error(f"Qdrant initialization attempt {attempt} failed: {e}", exc_info=True)
                self.client = None
                if attempt == max_attempts:
                    logger.critical("Unable to establish connection to Qdrant cluster after max backoff retries.")
                    break
                logger.info(f"Retrying connection in {delay}s...")
                time.sleep(delay)
                delay *= backoff_factor

    def _ensure_collection(self):
        """Creates the collection if it doesn't exist."""
        if not self.client:
            return
            
        collections = self.client.get_collections().collections
        exists = any(c.name == self.collection_name for c in collections)
        
        if not exists:
            logger.info(f"Creating Qdrant collection '{self.collection_name}' with {self.vector_size} dims...")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size, 
                    distance=models.Distance.COSINE
                )
            )

    def insert_documents(self, documents: List[Dict[str, Any]]):
        """
        Inserts documents into Qdrant using deterministic payload hashing.
        Enforces identical claim text segments override/upsert instead of duplicating.
        """
        if not self.client:
            logger.error("Qdrant client not initialized.")
            return False
            
        import hashlib
        points = []
        for doc in documents:
            payload = doc.get("payload", {})
            # Hash text (or fallback to title or vector) to create a deterministic ID
            text_to_hash = payload.get("text", "") or payload.get("title", "") or str(doc["vector"])
            
            hasher = hashlib.sha256()
            hasher.update(text_to_hash.encode("utf-8"))
            hex_hash = hasher.hexdigest()
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, hex_hash))
            
            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=doc["vector"],
                    payload=payload
                )
            )
            
        if points:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Inserted/Updated {len(points)} documents in Qdrant with deterministic IDs.")
            return True
        return False

    def search(self, query_vector: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Searches Qdrant for the closest vectors.
        """
        if not self.client:
            return []
            
        try:
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k
            )
            
            results = []
            for hit in search_results:
                results.append({
                    "title": hit.payload.get("title", "Unknown Title"),
                    "text": hit.payload.get("text", ""),
                    "source": hit.payload.get("source", "Unknown Source"),
                    "category": hit.payload.get("category", "General"),
                    "similarity": hit.score
                })
            return results
        except Exception as e:
            logger.error(f"Qdrant search failed: {e}")
            return []

qdrant_service = QdrantService()
