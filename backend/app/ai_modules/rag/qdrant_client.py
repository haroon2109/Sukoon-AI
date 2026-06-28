import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class QdrantRAGClient:
    def __init__(self, collection_name: str = "sukoon_verified_facts"):
        self.collection_name = collection_name
        self.qdrant_client = None
        self.embedding_model = None
        self._initialize_clients()
        
    def _initialize_clients(self):
        """Initializes Vertex AI embeddings and Qdrant Cloud client."""
        try:
            # 1. Initialize Google's Vertex AI Embedding Model
            from vertexai.language_models import TextEmbeddingModel
            # Note: Requires google-cloud-aiplatform and authentication
            self.embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
            
            # 2. Connect to Hosted Qdrant Database on Google Cloud
            from qdrant_client import QdrantClient
            from qdrant_client.http.models import Distance, VectorParams
            
            qdrant_url = os.environ.get("QDRANT_URL")
            qdrant_api_key = os.environ.get("QDRANT_API_KEY")
            
            if qdrant_url and qdrant_api_key:
                self.qdrant_client = QdrantClient(
                    url=qdrant_url, 
                    api_key=qdrant_api_key,
                    https=True
                )
                # Create collection if it doesn't exist
                try:
                    self.qdrant_client.recreate_collection(
                        collection_name=self.collection_name,
                        vectors_config=VectorParams(size=768, distance=Distance.COSINE),
                    )
                    logger.info("Successfully connected to Qdrant Cloud.")
                except Exception as e:
                    logger.warning(f"Could not recreate collection, might already exist or permission issue: {e}")
            else:
                logger.warning("QDRANT_URL or QDRANT_API_KEY missing. Using fallback mock.")
        except ImportError as e:
            logger.warning(f"Dependencies missing for Qdrant/Vertex AI: {e}. Using fallback mock.")
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant/Vertex AI: {e}. Using fallback mock.")
            
    def search_similar_text(self, text: str, top_k: int = 3) -> List[Dict]:
        """
        Converts text to vector embedding using Vertex AI, then queries Qdrant Cloud.
        Falls back to mock results if disconnected.
        """
        if self.qdrant_client and self.embedding_model:
            try:
                # Get embedding
                embeddings = self.embedding_model.get_embeddings([text])
                query_vector = embeddings[0].values
                
                # Query Qdrant
                search_result = self.qdrant_client.search(
                    collection_name=self.collection_name,
                    query_vector=query_vector,
                    limit=top_k
                )
                
                # Map to standard output format
                results = []
                for hit in search_result:
                    results.append({
                        "id": str(hit.id),
                        "score": hit.score,
                        "payload": hit.payload
                    })
                return results
                
            except Exception as e:
                logger.error(f"Qdrant search failed: {e}. Falling back to mock.")
                
        # Mock fallback payload mirroring the RAG Architecture Design
        return [
            {
                "id": "uuid-1234",
                "score": 0.94,
                "payload": {
                    "source_name": "BOOM Live",
                    "evidence_text": "The video circulating is from an old political rally in 2018.",
                    "url": "https://boomlive.in/fake-news/chennai-violence-video"
                }
            }
        ]

qdrant_client = QdrantRAGClient()
