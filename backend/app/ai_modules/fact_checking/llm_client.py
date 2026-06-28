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
            temperature=0.2,
            response_mime_type="application/json",
            system_instruction="You are Sukoon AI. Check the user input against live, trusted news sources using Google Search and provide a peace/truth verdict."
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
            result_json = json.loads(response.text)
            
            # Inject grounding sources into the final JSON response
            grounding_sources = self._extract_grounding_sources(response)
            if grounding_sources:
                result_json['grounding_sources'] = grounding_sources
                
            return result_json
        except Exception as e:
            return {"error": str(e), "raw_response": getattr(response, 'text', '') if 'response' in locals() else ''}

llm_client = GeminiClient()
