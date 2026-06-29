import json
from google import genai
from google.genai import types
from app.core.config import settings

# Setup API Key
gemini_key = settings.GEMINI_API_KEY or "DUMMY_KEY"
client = genai.Client(api_key=gemini_key)

class GeminiClient:
    def __init__(self):
        # We use gemini-2.5-flash which natively supports Google Search tools.
        self.model_name = 'gemini-2.5-flash'
        
        # Configure search grounding natively
        self.config = types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            temperature=0.1,
            system_instruction=(
                "You are Sukoon AI, an unbiased, objective fact-checking system. "
                "CRITICAL: You must cross-reference the user input EXCLUSIVELY against recognized "
                "authoritative Indian fact-checkers such as PIB Fact Check, Alt News, and BOOM Live using Google Search. "
                "To do this, append 'site:pib.gov.in OR site:altnews.in OR site:boomlive.in' to your internal search queries. "
                "Do NOT rely on generalized public opinion, blogs, or biased news outlets. "
                "Maintain a purely clinical and factual tone. "
                "Provide an objective peace/truth verdict based strictly on verifiable facts."
            )
        )

    def _extract_grounding_sources(self, response) -> list:
        """Extracts the URIs of the grounding chunks returned by Google Search."""
        sources = []
        try:
            if not response.candidates:
                return sources
            candidate = response.candidates[0]
            if not getattr(candidate, 'grounding_metadata', None):
                return sources
            metadata = candidate.grounding_metadata
            if not getattr(metadata, 'grounding_chunks', None):
                return sources
                
            for chunk in metadata.grounding_chunks:
                if getattr(chunk, 'web', None) and getattr(chunk.web, 'uri', None):
                    sources.append(chunk.web.uri)
        except Exception:
            pass
            
        return list(set(sources))

    def generate(self, prompt: str) -> dict:
        """Generic generation method with Google Search Grounding."""
        try:
            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=self.config
            )
            
            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
                
            result_json = json.loads(raw_text.strip())
            
            # Inject grounding sources into the final JSON response
            grounding_sources = self._extract_grounding_sources(response)
            if grounding_sources:
                result_json['grounding_sources'] = grounding_sources
                
            return result_json
        except Exception as e:
            return {"error": str(e), "raw_response": getattr(response, 'text', '') if 'response' in locals() else ''}

llm_client = GeminiClient()
