import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add backend directory to sys.path to allow imports
backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

# Load environment variables
load_dotenv(dotenv_path=backend_dir / ".env")

def run_test():
    try:
        from app.services.rag_service import rag_service
        
        logger.info("Starting RAG test pipeline...")
        
        # 1. Upsert a test point
        test_claim = "The RBI has issued a new 1000 rupee note."
        test_metadata = {
            "source": "PIB",
            "is_fake": True,
            "url": "https://pib.gov.in/FactCheck/FakeClaim"
        }
        
        logger.info("Adding test fact-check...")
        point_id = rag_service.add_fact_check(test_claim, test_metadata)
        logger.info(f"Successfully added fact-check. ID: {point_id}")
        
        # 2. Query the point
        query = "Did the Reserve Bank release 1000 Rs notes?"
        logger.info(f"Querying for: '{query}'")
        results = rag_service.search_similar(query, top_k=1)
        
        if results:
            logger.info("Search successful! Top result:")
            logger.info(f"Score: {results[0]['score']}")
            logger.info(f"Payload: {results[0]['payload']}")
        else:
            logger.warning("Search completed but no results were found.")
            
        logger.info("RAG test pipeline completed successfully.")
        
    except Exception as e:
        logger.error(f"RAG test pipeline failed: {e}")

if __name__ == "__main__":
    run_test()
