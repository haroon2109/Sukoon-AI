import logging
import uuid
from typing import List, Dict, Any

from app.db.qdrant import qdrant_store
from app.ai_modules.vertex_embeddings import vertex_embeddings
from qdrant_client.http.models import PointStruct

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self, collection_name: str = "fact_checks", vector_size: int = 768):
        self.collection_name = collection_name
        self.vector_size = vector_size
        
    def _ensure_initialized(self):
        qdrant_store.ensure_collection_exists(self.collection_name, self.vector_size)
        
    def add_fact_check(self, text: str, metadata: Dict[str, Any] = None):
        """
        Embed a fact-check text and store it in Qdrant along with metadata.
        """
        self._ensure_initialized()
        
        if metadata is None:
            metadata = {}
            
        embedding = vertex_embeddings.get_embedding(text)
        
        point_id = str(uuid.uuid4())
        point = PointStruct(
            id=point_id,
            vector=embedding,
            payload={
                "text": text,
                **metadata
            }
        )
        
        client = qdrant_store.get_client()
        client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )
        logger.info(f"Added fact-check to Qdrant collection '{self.collection_name}' with ID {point_id}")
        return point_id

    def add_fact_checks_batch(self, texts: List[str], metadatas: List[Dict[str, Any]] = None):
        """
        Embed a batch of fact-check texts and store them in Qdrant.
        """
        self._ensure_initialized()
        
        if metadatas is None:
            metadatas = [{} for _ in texts]
            
        embeddings = vertex_embeddings.get_embeddings(texts)
        
        points = []
        for i, embedding in enumerate(embeddings):
            point_id = str(uuid.uuid4())
            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "text": texts[i],
                        **metadatas[i]
                    }
                )
            )
            
        client = qdrant_store.get_client()
        client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        logger.info(f"Added {len(points)} fact-checks to Qdrant collection '{self.collection_name}'")
        return [p.id for p in points]

    def search_similar(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for fact-checks similar to the query.
        """
        self._ensure_initialized()
        
        query_embedding = vertex_embeddings.get_embedding(query)
        
        client = qdrant_store.get_client()
        search_result = client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k
        )
        
        results = []
        for scored_point in search_result:
            results.append({
                "id": scored_point.id,
                "score": scored_point.score,
                "payload": scored_point.payload
            })
            
        return results

rag_service = RAGService()
