import json
import logging
from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)

def search_web(query: str, max_results: int = 3) -> list:
    """
    Searches the web using DuckDuckGo and returns top snippets.
    Useful for getting up-to-date information on claims.
    """
    try:
        results = []
        with DDGS() as ddgs:
            # text() generator returns dicts with 'title', 'href', and 'body'
            for idx, r in enumerate(ddgs.text(query, max_results=max_results)):
                results.append({
                    "title": r.get("title", ""),
                    "snippet": r.get("body", ""),
                    "url": r.get("href", "")
                })
        return results
    except Exception as e:
        logger.error(f"DuckDuckGo search failed: {e}")
        return []
