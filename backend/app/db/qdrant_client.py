import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class QdrantMockClient:
    """
    Mock client for Qdrant Vector DB for the MVP.
    In production, this connects to Qdrant Cloud and queries semantic embeddings.
    """
    
    def __init__(self, host="localhost", port=6333):
        self.host = host
        self.port = port
        logger.info(f"Initialized Qdrant Mock Client at {self.host}:{self.port}")
        
    def search(self, collection_name: str, query_vector: List[float], limit: int = 5) -> List[Dict]:
        """
        Mock search function that returns static verification hits based on 
        known data points.
        """
        # Return mock hits
        return [
            {
                "id": 1,
                "score": 0.94,
                "payload": {
                    "source": "PIB Fact Check",
                    "text": "The Reserve Bank of India (RBI) has not issued any new Rs 1000 currency notes.",
                    "url": "https://pib.gov.in/factcheck/rbi-notes"
                }
            }
        ]
        
    def upsert(self, collection_name: str, vectors: List[Dict]):
        """Mock upsert function."""
        logger.info(f"Upserted {len(vectors)} vectors into Qdrant collection {collection_name}")
        return True

qdrant_client = QdrantMockClient()
