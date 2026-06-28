import os
import logging
from typing import List
import vertexai
from vertexai.language_models import TextEmbeddingModel

logger = logging.getLogger(__name__)

class VertexEmbeddingService:
    def __init__(self, model_name: str = "textembedding-gecko@003"):
        self.model_name = model_name
        self.initialized = False
        self.model = None

    def initialize(self):
        if self.initialized:
            return

        project_id = os.getenv("GCP_PROJECT_ID")
        region = os.getenv("GCP_REGION", "us-central1")

        if not project_id:
            logger.warning("GCP_PROJECT_ID not set. Vertex AI embeddings might fail if default credentials are not configured.")
        else:
            vertexai.init(project=project_id, location=region)

        try:
            self.model = TextEmbeddingModel.from_pretrained(self.model_name)
            self.initialized = True
            logger.info(f"Vertex AI TextEmbeddingModel '{self.model_name}' initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize Vertex AI TextEmbeddingModel: {e}")
            raise

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of strings.
        """
        if not self.initialized:
            self.initialize()
            
        try:
            embeddings = self.model.get_embeddings(texts)
            return [embedding.values for embedding in embeddings]
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise

    def get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single string.
        """
        embeddings = self.get_embeddings([text])
        if embeddings:
            return embeddings[0]
        return []

vertex_embeddings = VertexEmbeddingService()
