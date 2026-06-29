import json
from google import genai
from google.genai import types
from pydantic import BaseModel
from app.core.config import settings

gemini_key = settings.GEMINI_API_KEY or "DUMMY_KEY"
client = genai.Client(api_key=gemini_key)

# Strict Pydantic Schema to enforce clean structured outputs
class FactCheckResponse(BaseModel):
    verdict: str  # Must strictly be "TRUE", "FALSE", or "UNVERIFIED"
    explanation: str

class GeminiClient:
    def __init__(self):
        self.model_name = 'gemini-2.5-flash'
        
        self.config = types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            temperature=0.0,
            response_mime_type="application/json",
            response_schema=FactCheckResponse,
            system_instruction=(
                "You are the autonomous truth engine of Sukoon AI. Your goal is community peace through accuracy. "
                "You MUST look up the claim using Google Search to cross-reference facts.\n\n"
                "CRITICAL RULES:\n"
                "1. If Google Search grounding results directly support the claim or demonstrate it is an established factual truth (historical, legal, geographic, scientific, or general public knowledge), you MUST mark the verdict as 'TRUE'.\n"
                "2. Do NOT assume a statement is false simply because it is missing from a fake news database.\n"
                "3. Only declare a statement 'FALSE' if authoritative grounding sources explicitly contradict it, or label it a hoax or rumor.\n"
                "4. If there is absolutely zero evidence or conflicting reports make it impossible to verify, mark it as 'UNVERIFIED'.\n\n"
                "Provide a highly objective, neutral summary of your search findings in the explanation field."
            )
        )

    def _extract_grounding_sources(self, response) -> list:
        sources = []
        try:
            if not response.candidates:
                return sources
            metadata = response.candidates[0].grounding_metadata
            for chunk in metadata.grounding_chunks:
                if getattr(chunk, 'web', None) and getattr(chunk.web, 'uri', None):
                    sources.append(chunk.web.uri)
        except Exception:
            pass
        return list(set(sources))

    def generate(self, prompt: str) -> dict:
        try:
            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=self.config
            )
            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
                
            result_json = json.loads(raw_text.strip())
            grounding_sources = self._extract_grounding_sources(response)
            if grounding_sources:
                result_json['grounding_sources'] = grounding_sources
                
            return result_json
        except Exception as e:
            return {"verdict": "UNVERIFIED", "explanation": f"Fallback triggered: {str(e)}"}

llm_client = GeminiClient()
