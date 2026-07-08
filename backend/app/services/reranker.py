import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

_reranker_model = None

def get_reranker_model():
    global _reranker_model
    if _reranker_model is None:
        try:
            from FlagEmbedding import FlagReranker
            logger.info("Initializing BGE Reranker local model...")
            _reranker_model = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True)
            logger.info("BGE Reranker initialized successfully.")
        except ImportError:
            logger.error("FlagEmbedding is not installed. Reranking cannot be performed.")
            return None
        except Exception as e:
            logger.error(f"Failed to initialize BGE Reranker Model: {str(e)}")
            return None
    return _reranker_model

def rerank_results(query: str, documents: List[Dict[str, Any]], top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Reranks a list of documents based on a query using the BGE Reranker.
    
    Args:
        query (str): The search query.
        documents (List[Dict]): The initial retrieved documents. Must contain a 'content' field.
        top_k (int): Number of top results to return.
        
    Returns:
        List[Dict]: The reranked documents with added 'rerank_score' field.
    """
    if not documents:
        return []
        
    reranker = get_reranker_model()
    
    if not reranker:
        logger.warning("Reranker not available. Returning original results.")
        return documents[:top_k]

    try:
        # Prepare pairs for the reranker: (query, doc_content)
        pairs = [[query, doc.get("content", "")] for doc in documents]
        
        # Compute scores
        scores = reranker.compute_score(pairs, normalize=True)
        
        # Add scores to documents
        for i, doc in enumerate(documents):
            doc["rerank_score"] = scores[i]
            
        # Sort by rerank_score descending
        reranked_docs = sorted(documents, key=lambda x: x["rerank_score"], reverse=True)
        
        return reranked_docs[:top_k]
    except Exception as e:
        logger.error(f"Error during reranking: {e}")
        return documents[:top_k]
