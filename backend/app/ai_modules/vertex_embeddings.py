import os
import logging
from typing import List
import google.generativeai as genai

logger = logging.getLogger(__name__)

class VertexEmbeddingService:
    """
    Renamed internally to use Google AI Studio (Free Tier) instead of Vertex AI, 
    but class name kept the same to maintain backwards compatibility with existing imports.
    """
    def __init__(self, model_name: str = "models/text-embedding-004"):
        self.model_name = model_name
        self.initialized = False

    def initialize(self):
        if self.initialized:
            return

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY not set. Embedding generation will fail.")
            return

        try:
            genai.configure(api_key=api_key)
            self.initialized = True
            logger.info(f"Google AI Studio Embedding Model '{self.model_name}' initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Google AI Studio TextEmbeddingModel: {e}")
            raise

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of strings using Google AI Studio.
        """
        if not self.initialized:
            self.initialize()
            
        try:
            # genai.embed_content accepts a list of strings
            result = genai.embed_content(
                model=self.model_name,
                content=texts,
                task_type="retrieval_document",
            )
            return result['embedding']
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

# Singleton instance exported for use across the application
vertex_embeddings = VertexEmbeddingService()
