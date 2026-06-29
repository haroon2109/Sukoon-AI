import validators
from newspaper import Article
from .text_pipeline import process_text_claim

def process_url_claim(url: str, is_deep: bool = False) -> dict:
    """Fetches URL content using newspaper3k and processes it as text."""
    # 1. URL Validation
    if not validators.url(url):
        return {"error": "Invalid URL provided.", "verdict": "Unverified"}
        
    try:
        # 2. Web Scraping / Extraction
        article = Article(url)
        article.download()
        article.parse()
        
        headline = article.title
        body = article.text
        
        if not body or not body.strip():
            # Fallback logic: If content is blocked behind a bot-protection firewall,
            # pass the raw URL alongside a direct request for Gemini to look it up via Search Grounding instead.
            limited_text = f"Please research this specific URL link directly using your live search tool: {url}"
        else:
            combined_text = f"Headline: {headline}\n\nBody:\n{body}"
            # Limit the text length to avoid token limits
            limited_text = combined_text[:10000] 
        
        # 3. Pass to evaluation pipeline
        return process_text_claim(limited_text, is_deep=is_deep)
        
    except Exception as e:
        return {"error": f"Failed to process URL: {str(e)}", "verdict": "Unverified"}
