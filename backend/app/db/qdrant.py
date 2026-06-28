import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
import logging

logger = logging.getLogger(__name__)

class QdrantStore:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QdrantStore, cls).__new__(cls)
            cls._instance.client = None
            cls._instance.initialized = False
        return cls._instance

    def initialize(self):
        if self.initialized:
            return

        url = os.getenv("QDRANT_URL")
        api_key = os.getenv("QDRANT_API_KEY")

        if not url or not api_key:
            logger.warning("QDRANT_URL or QDRANT_API_KEY not set. Falling back to in-memory Qdrant for testing.")
            self.client = QdrantClient(":memory:")
        else:
            self.client = QdrantClient(url=url, api_key=api_key)
        
        self.initialized = True
        logger.info("Qdrant client initialized.")

    def get_client(self) -> QdrantClient:
        if not self.initialized:
            self.initialize()
        return self.client

    def ensure_collection_exists(self, collection_name: str, vector_size: int = 768):
        client = self.get_client()
        if not client.collection_exists(collection_name=collection_name):
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
            logger.info(f"Created Qdrant collection '{collection_name}' with size {vector_size}")

qdrant_store = QdrantStore()
