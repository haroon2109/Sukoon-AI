import os
import logging
import gc
from typing import List, Optional

logger = logging.getLogger(__name__)

# Use a highly efficient, lightweight model suitable for free tiers
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

def generate_text_embedding(
    text: str, 
    model: str = "minilm", 
    dimensions: Optional[int] = 384
) -> List[float]:
    """
    Generates real semantic vector embeddings using a local sentence-transformers model.
    Implements extreme memory optimization (lazy load + unload).
    """
    if not text or not text.strip():
        raise ValueError("Input text string cannot be empty.")

    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        logger.error("sentence_transformers is not installed. Embeddings cannot be generated.")
        return [0.0] * (dimensions if dimensions else 384)

    try:
        logger.info(f"Loading Embedding Model ({MODEL_NAME}) for current request...")
        # Load directly to CPU for strict memory limited environments
        st_model = SentenceTransformer(MODEL_NAME, device="cpu")
        
        # Encode
        response = st_model.encode([text], show_progress_bar=False)
        if response is not None and len(response) > 0:
            vector = response[0].tolist()
        else:
            raise ValueError("Embedding model returned an empty vector payload.")
            
        # Free memory aggressively
        del st_model
        gc.collect()
        
        return vector

    except Exception as e:
        logger.error(f"Unexpected failure inside the local embedding generation pipeline: {str(e)}")
        # Return fallback zero vector so app doesn't crash entirely during an OOM event
        return [0.0] * (dimensions if dimensions else 384)
