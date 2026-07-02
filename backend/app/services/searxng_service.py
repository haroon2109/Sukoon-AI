import os
import httpx
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Configurable SEARXNG URL, defaults to a public instance
SEARXNG_URL = os.getenv("SEARXNG_URL", "https://searx.be/search")

class SearxngService:
    """
    Service to query a SearXNG instance for live web search context.
    Aggregates results from multiple search engines privately.
    """
    
    async def search(self, query: str, top_k: int = 3) -> str:
        """
        Executes a search against SearXNG and returns formatted top results.
        """
        if not query.strip():
            return "No web records found: empty query."
            
        try:
            params = {
                "q": query,
                "format": "json"
            }
            logger.info(f"[SearXNG] Querying live web for: {query[:50]}...")
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(SEARXNG_URL, params=params)
                
            if response.status_code != 200:
                logger.error(f"[SearXNG] Error response: {response.status_code}")
                return "SearXNG search failed."
                
            data = response.json()
            results = data.get("results", [])
            
            if not results:
                return "SearXNG search returned no live web results."
                
            formatted_results = []
            for i, res in enumerate(results[:top_k]):
                title = res.get("title", "No Title")
                content = res.get("content", "")
                url = res.get("url", "#")
                
                # Format each result cleanly
                formatted_results.append(f"Result {i+1}:\nTitle: {title}\nSnippet: {content}\nSource: {url}")
                
            final_output = "\n\n".join(formatted_results)
            return f"Found {len(formatted_results)} live web records:\n{final_output}"
            
        except Exception as e:
            logger.error(f"[SearXNG] Request failed: {str(e)}")
            return "SearXNG search failed due to timeout or connection error."

searxng_service = SearxngService()
