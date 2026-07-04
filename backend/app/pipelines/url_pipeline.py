from urllib.parse import urlparse
from ..services.scraper import scrape_url
from .text_pipeline import process_text_claim

def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def process_url_claim(url: str, is_deep: bool = False) -> dict:
    """Fetches URL content using the internal scraper and processes it as text."""
    # 1. URL Validation
    if not is_valid_url(url):
        return {"error": "Invalid URL provided.", "verdict": "Unverified"}
        
    try:
        # 2. Web Scraping / Extraction
        body = scrape_url(url)
        
        if not body or not body.strip():
            # Fallback logic: If content is blocked behind a bot-protection firewall,
            # pass the raw URL alongside a direct request for Gemini to look it up via Search Grounding instead.
            limited_text = f"Please research this specific URL link directly using your live search tool: {url}"
        else:
            # Limit the text length to avoid token limits
            limited_text = body[:10000] 
        
        # 3. Pass to evaluation pipeline
        return process_text_claim(limited_text, is_deep=is_deep)
        
    except Exception as e:
        return {"error": f"Failed to process URL: {str(e)}", "verdict": "Unverified"}
