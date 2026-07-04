import logging
from app.core.celery_app import celery_app
from app.services.scraper import scrape_url
from app.ai_modules.embeddings import generate_text_embedding
from app.db.supabase_client import supabase_client

logger = logging.getLogger(__name__)

@celery_app.task(name="pipelines.verify_content_stream", bind=True, max_retries=3)
def verify_content_stream(self, target_url: str) -> dict:
    """
    Asynchronous Celery task that coordinates live scraping, semantic 
    embedding generation via Gemini, and RAG verification lookup.
    """
    logger.info(f"Starting real-time evaluation pipeline for job {self.request.id}")
    
    try:
        # Phase 1: Real-time Scraping & Content Extraction
        logger.info(f"Scraping content metadata from source: {target_url}")
        
        raw_text = scrape_url(target_url)
        
        if not raw_text or len(raw_text.strip()) < 10:
            return {
                "status": "SKIPPED",
                "reason": "Insufficient text content extracted from source to perform truth valuation."
            }

        # Phase 2: Real Embedding Generation via text-embedding-004 / gemini-embedding-001
        logger.info("Passing payload to Gemini Embedding API context...")
        # Generates a 768-dimensional Matryoshka vector optimized for database storage
        query_vector = generate_text_embedding(text=raw_text, dimensions=768)

        # Phase 3: Real Database RAG Match Lookup via pgvector
        logger.info("Executing semantic vector match across verified truth indices...")
        
        # Invoke your PostgreSQL stored procedure via the Supabase client
        # Matches the vector input to catch historical matches or known debunked articles
        db_response = supabase_client.rpc(
            "match_verified_claims",
            {
                "query_embedding": query_vector,
                "match_threshold": 0.82,  # Confidence rating score minimum
                "match_count": 3          # Return top 3 historical matches
            }
        ).execute()
        
        rag_hits = db_response.data if hasattr(db_response, 'data') else []

        # Phase 4: Construct Decision Intelligence State Payload
        is_misinformation_match = len(rag_hits) > 0
        highest_confidence = rag_hits[0].get("similarity", 0.0) if is_misinformation_match else 0.0
        
        logger.info(f"Pipeline verification finalized. Hits discovered: {len(rag_hits)}")
        return {
            "status": "COMPLETED",
            "source_url": target_url,
            "has_known_matches": is_misinformation_match,
            "highest_similarity_score": highest_confidence,
            "contextual_references": rag_hits,
            "extracted_metadata": {
                "title": "Unknown",
                "author": "Unknown"
            }
        }

    except Exception as exc:
        logger.error(f"Pipeline execution stalled on attempt {self.request.retries}: {str(exc)}")
        # Automatic exponential backoff retry rule if a network timeout occurs
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
