import json
from google import genai
from google.genai import types
from pydantic import BaseModel
from app.core.config import settings

# Setup API Key
gemini_key = settings.GEMINI_API_KEY or "DUMMY_KEY"
client = genai.Client(api_key=gemini_key)

# Strict Schema definition to force structured output
class FactCheckResponse(BaseModel):
    verdict: str  # Must strictly be "TRUE", "FALSE", or "UNVERIFIED"
    explanation: str

class GeminiClient:
    def __init__(self):
        self.model_name = 'gemini-2.5-flash'
        
        # Configure search grounding natively with strict schema constraints
        self.config = types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            temperature=0.0,
            response_mime_type="application/json",
            response_schema=FactCheckResponse,
            system_instruction=(
                "You are the Antigravity Autonomous Verification Engine of Sukoon AI.\n"
                "Your core mission is to uphold community peace by verifying information with absolute accuracy.\n\n"
                "When a query is received:\n"
                "1. First evaluate if the statement is a universally established fact (scientific, mathematical, geographic, or general public knowledge like 'water is wet').\n"
                "2. If it is an obvious, universally acknowledged truth, or if live web search grounding results show explicit consensus, you MUST bypass local database restrictions and return a strict verdict of 'TRUE'.\n"
                "3. Do not permit empty local context arrays to mask objective truth. When local databases yield zero matching evidence, rely completely on your live Google Search grounding tools to confirm or debunk the claim.\n"
                "4. Output your response strictly conforming to the requested structural JSON schema with zero conversational commentary or markdown block annotations.\n\n"
                "Provide a highly objective, neutral summary of your search findings in the explanation field."
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
            return {"verdict": "UNVERIFIED", "explanation": f"Failsafe triggered. Processing error: {str(e)}"}

llm_client = GeminiClient()
