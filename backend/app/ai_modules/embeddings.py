import os
import logging
from typing import List, Optional
from google import genai
from google.genai.errors import APIError

logger = logging.getLogger(__name__)

def get_gemini_client() -> Optional[genai.Client]:
    """
    Initializes and returns the GenAI Client if an API key is available.
    Automatically looks for GEMINI_API_KEY or GOOGLE_API_KEY in the environment.
    """
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        logger.warning(
            "Google Gen AI API key missing from environment variables. "
            "Falling back to local logging. Embeddings cannot be generated."
        )
        return None
        
    try:
        # The modern SDK automatically hooks into standard environment keys,
        # but passing it explicitly guarantees safety across deployment containers.
        return genai.Client(api_key=api_key)
    except Exception as e:
        logger.error(f"Failed to initialize Google GenAI Client: {str(e)}")
        return None

def generate_text_embedding(
    text: str, 
    model: str = "gemini-embedding-001", 
    dimensions: Optional[int] = 768
) -> List[float]:
    """
    Generates real semantic vector embeddings using Google's Gen AI SDK.
    
    Args:
        text (str): The raw document text or query string to embed.
        model (str): The foundational embedding model to use.
        dimensions (int): Optional dimensionality truncation (e.g., 768 for pgvector compatibility).
        
    Returns:
        List[float]: The generated mathematical vector array.
    """
    if not text or not text.strip():
        raise ValueError("Input text string cannot be empty.")
        
    client = get_gemini_client()
    
    # Critical Hackathon Fallback: Avoid throwing unhandled 500 crashes if key goes missing mid-demo
    if not client:
        logger.critical("CRITICAL: Generating a temporary zeroed mock vector due to missing API key context.")
        return [0.0] * (dimensions if dimensions else 3072)

    try:
        # Utilizing the standardized models utility pattern from the new SDK
        response = client.models.embed_content(
            model=model,
            contents=text,
            # Matryoshka Representation Learning parameter to match your vector storage dimensions
            config={"output_dimensionality": dimensions} if dimensions else None
        )
        
        # Extracts the raw floats from the structured response payload
        if response.embeddings and len(response.embeddings) > 0:
            return response.embeddings[0].values
        else:
            raise ValueError("API returned an empty embedding list payload.")

    except APIError as api_err:
        logger.error(f"Google Gen AI API Error encountered: {api_err.message}")
        raise api_err
    except Exception as e:
        logger.error(f"Unexpected failure inside the embedding generation pipeline: {str(e)}")
        raise e
