import json
import re
from google import genai
from google.genai import types
from pydantic import BaseModel
from app.core.config import settings

# Setup API Key
gemini_key = settings.GEMINI_API_KEY or "DUMMY_KEY"
client = genai.Client(api_key=gemini_key)

class GeminiClient:
    def __init__(self):
        self.model_name = 'gemini-2.5-flash'
        
        self.config = types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            temperature=0.0,
            system_instruction=(
                "You are the objective truth engine of Sukoon AI, an advanced misinformation detection platform. "
                "Your goal is community peace through ACCURATE fact-checking. "
                "Evaluate the claim carefully using your knowledge and any search results. "
                "Respond ONLY with a valid JSON object. Do not wrap in markdown or backticks. Format:\n"
                "{\n"
                "  \"verdict\": \"<VERDICT>\",\n"
                "  \"explanation\": \"<One paragraph explanation citing your reasoning>\"\n"
                "}\n"
                "Verdict must be exactly one of: VERIFIED, MISLEADING, FALSE, UNVERIFIED."
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
        """Generic generation method with Google Search Grounding and robust regex parsing."""
        try:
            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=self.config
            )
            
            raw_text = response.text.strip()
            
            # Robust Regex Parser to isolate the JSON block if the model outputs markdown wrappers
            if "```" in raw_text:
                match = re.search(r"```(?:json)?\s*(.*?)\s*```", raw_text, re.DOTALL)
                if match:
                    raw_text = match.group(1).strip()
            
            result_json = json.loads(raw_text)
            
            # Inject grounding sources into the final JSON response
            grounding_sources = self._extract_grounding_sources(response)
            if grounding_sources:
                result_json['grounding_sources'] = grounding_sources
                
            return result_json
        except Exception as e:
            # Fallback output in case of parsing faults — return neutral UNVERIFIED
            return {
                "verdict": "UNVERIFIED",
                "explanation": f"Could not parse LLM response. Raw parsing error: {str(e)}"
            }

    def analyze_media(self, file_path: str, mime_type: str, context: str = "") -> dict:
        """
        Analyzes media (image, audio, video) using Gemini 2.5 Flash.
        Supports both gs:// URIs and local file paths.
        """
        try:
            contents = []
            if file_path.startswith("gs://"):
                # GCS URI: pass it using types.Part.from_uri
                contents.append(types.Part.from_uri(uri=file_path, mime_type=mime_type))
            else:
                # Local file path: read bytes and pass using types.Part.from_bytes
                with open(file_path, "rb") as f:
                    file_bytes = f.read()
                contents.append(types.Part.from_bytes(data=file_bytes, mime_type=mime_type))
            
            prompt = "Please analyze this media file carefully."
            if context:
                prompt += f"\n\nContext extracted from the media (e.g., OCR or transcript):\n{context}"
            contents.append(prompt)
            
            response = client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=self.config
            )
            
            raw_text = response.text.strip()
            if "```" in raw_text:
                match = re.search(r"```(?:json)?\s*(.*?)\s*```", raw_text, re.DOTALL)
                if match:
                    raw_text = match.group(1).strip()
            
            result_json = json.loads(raw_text)
            grounding_sources = self._extract_grounding_sources(response)
            if grounding_sources:
                result_json['grounding_sources'] = grounding_sources
                
            return result_json
        except Exception as e:
            return {
                "verdict": "UNVERIFIED",
                "explanation": f"Could not analyze media. Error: {str(e)}"
            }

llm_client = GeminiClient()
