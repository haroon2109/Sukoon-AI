import re
import requests
from bs4 import BeautifulSoup
import logging
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)

URL_REGEX = re.compile(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')

def is_url(text: str) -> bool:
    """Checks if the provided text is a URL."""
    return bool(URL_REGEX.match(text.strip()))

def scrape_url(url: str) -> str:
    """
    Fetches and extracts the main text content from a URL using a hybrid approach:
    1. Tier 1 (Playwright): Dynamic rendering for JS-heavy sites.
    2. Tier 2 (Requests): Fast static fallback if Playwright fails.
    """
    html_content = ""
    
    # Tier 1: Try Playwright for dynamic sites
    try:
        logger.info(f"Attempting to scrape with Playwright (Dynamic): {url}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            # Short timeout to avoid hanging the verification loop
            page.goto(url, timeout=10000, wait_until="domcontentloaded")
            html_content = page.content()
            browser.close()
    except Exception as e:
        logger.warning(f"Playwright scraping failed for {url}. Falling back to Requests. Error: {e}")
        
    # Tier 2: Fallback to Requests
    if not html_content:
        try:
            logger.info(f"Attempting to scrape with Requests (Static): {url}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            html_content = response.text
        except Exception as e:
            logger.error(f"Both scraping tiers failed for URL {url}: {e}")
            return ""

    # Parse with Beautiful Soup
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
            
        text = soup.get_text(separator=' ')
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        logger.error(f"BeautifulSoup parsing failed: {e}")
        return ""
