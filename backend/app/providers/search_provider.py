import logging
from duckduckgo_search import DDGS
from typing import List

logger = logging.getLogger(__name__)

class DuckDuckGoSearchProvider:
    """
    Provides real-time web search capabilities using DuckDuckGo to retrieve
    external evidence for claim verification.
    """
    
    def __init__(self):
        self.ddgs = DDGS()
        
    def search(self, query: str, max_results: int = 3) -> List[dict]:
        logger.info(f"Executing DDG search for query: {query}")
        results = []
        try:
            raw_results = self.ddgs.text(query, max_results=max_results)
            for r in raw_results:
                results.append({
                    "title": r.get("title", ""),
                    "link": r.get("href", ""),
                    "snippet": r.get("body", "")
                })
            return results
        except Exception as e:
            logger.error(f"DDG Search failed: {e}")
            return []

search_provider = DuckDuckGoSearchProvider()
