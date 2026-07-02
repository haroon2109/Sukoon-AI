import os
import uuid
import logging
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models

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
        
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        
        try:
            if qdrant_url and qdrant_api_key:
                logger.info("Initializing Qdrant Cloud client...")
                self.client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
            else:
                logger.info("Initializing local in-memory Qdrant client (stateless)...")
                self.client = QdrantClient(":memory:")
                
            self._ensure_collection()
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant: {e}")
            self.client = None

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
        Inserts documents into Qdrant. 
        Expected document format: {"vector": [float, ...], "payload": {"title": "...", "text": "...", "source": "..."}}
        """
        if not self.client:
            logger.error("Qdrant client not initialized.")
            return False
            
        points = []
        for doc in documents:
            point_id = str(uuid.uuid4())
            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=doc["vector"],
                    payload=doc.get("payload", {})
                )
            )
            
        if points:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Inserted {len(points)} documents into Qdrant.")
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
