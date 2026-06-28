import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import json

# Setup API Key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "DUMMY_KEY"))

# Model configuration
generation_config = {
  "temperature": 0.2,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 1024,
  "response_mime_type": "application/json"
}

class GeminiClient:
    def __init__(self):
        # We use gemini-1.5-flash for fast extraction and gemini-1.5-pro for deep reasoning
        self.flash_model = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config)
        
        # Enable Google Search Grounding for the reasoning model (live news lookup)
        self.pro_model = genai.GenerativeModel(
            'gemini-1.5-pro-latest', 
            generation_config=generation_config,
            tools="google_search_retrieval"
        )
        
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        }

    def generate(self, prompt: str, model_type: str = "pro") -> dict:
        """Generic generation method."""
        model = self.flash_model if model_type == "flash" else self.pro_model
        try:
            response = model.generate_content(prompt, safety_settings=self.safety_settings)
            result_json = json.loads(response.text)
            
            # Safely extract Live Google Search Grounding Metadata
            grounding_sources = []
            if hasattr(response, 'candidates') and len(response.candidates) > 0:
                candidate = response.candidates[0]
                if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                    metadata = candidate.grounding_metadata
                    if hasattr(metadata, 'grounding_chunks') and metadata.grounding_chunks:
                        for chunk in metadata.grounding_chunks:
                            if hasattr(chunk, 'web') and chunk.web:
                                if hasattr(chunk.web, 'uri') and chunk.web.uri:
                                    title = getattr(chunk.web, 'title', '')
                                    # Clean format for the TruthCard: "Title (URI)" or just "URI"
                                    if title:
                                        # To keep it short and clean for the frontend UI:
                                        grounding_sources.append(chunk.web.uri)
                                    else:
                                        grounding_sources.append(chunk.web.uri)
            
            # Inject grounding sources into the final JSON response
            if grounding_sources:
                result_json['grounding_sources'] = list(set(grounding_sources))
                
            return result_json
        except Exception as e:
            if "safety" in str(e).lower() or "blocked" in str(e).lower():
                return {"verdict": "Toxic", "flags": ["blocked_by_safety_filter"], "error": "Blocked by API safety filters"}
            return {"error": str(e), "raw_response": getattr(response, 'text', '') if 'response' in locals() else ''}

    def analyze_text(self, text: str) -> dict:
        """Analyzes text for fact-checking and sentiment/hate-speech."""
        prompt = f"""
        Analyze the following text for fact-checking and sentiment/hate-speech analysis.
        Provide a JSON response with the following keys:
        - claim: The main claim extracted.
        - sentiment: The sentiment of the text (Positive, Negative, Neutral).
        - hate_speech: Boolean indicating if hate speech is present.
        - verdict: Whether the claim is True, False, Unverified, or Misleading.
        - confidence: A float between 0 and 1 indicating confidence in the verdict.
        - analysis: A brief explanation.
        - toxicity_score: (Integer 0-100: How aggressively the piece tries to incite anger)
        - factuality_score: (Integer 0-100: How much can be cross-verified by reputable sources)
        - community_impact_rating: (Integer 0-100: Is this targeting vulnerable groups or disrupting peace?)
        - peace_verdict: (High Risk, Moderate Risk, Safe)
        - suggested_action: (Actionable advice, e.g., "Do not share.")
        
        Text: {text}
        """
        try:
            response = self.pro_model.generate_content(prompt, safety_settings=self.safety_settings)
            return json.loads(response.text)
        except Exception as e:
            if "safety" in str(e).lower() or "blocked" in str(e).lower():
                return {"verdict": "Toxic", "flags": ["blocked_by_safety_filter"], "error": "Blocked by API safety filters"}
            return {"error": str(e), "raw_response": getattr(response, 'text', '') if 'response' in locals() else ''}

    def analyze_media(self, file_path: str, mime_type: str, context: str = "") -> dict:
        """Analyzes a media file for context and potential hate speech patterns."""
        prompt = f"""
        Analyze this media using advanced forensic analysis. 
        
        1. Perform OCR (Optical Character Recognition) to extract any and all readable text from the image/video.
        2. Identify any public figures, landmarks, or specific visual contexts present.
        3. If a quote is extracted alongside a public figure, cross-reference it against verified historical records. Determine if the quote is authentic, misattributed, or entirely fabricated.
        4. Does the visual context contain hate symbols, altered text designed to mislead, or incitement to violence? Flag any discrepancies instantly.
        
        Context provided: {context}
        
        Respond ONLY in a valid JSON format with the keys: 
        - 'verdict' (Safe, Misleading, Toxic)
        - 'confidence_score' (0.0 to 1.0)
        - 'explanation' (a concise, neutral summary of the facts. Explicitly mention if a quote was verified or found to be misattributed/fake based on the visual context.)
        - 'flags' (an array of categories triggered, e.g., ["misattributed_quote", "hate_symbol"])
        - 'toxicity_score' (Integer 0-100: How aggressively the piece tries to incite anger)
        - 'factuality_score' (Integer 0-100: How much can be cross-verified by reputable sources)
        - 'community_impact_rating' (Integer 0-100: Is this targeting vulnerable groups or disrupting peace?)
        - 'peace_verdict' (High Risk, Moderate Risk, Safe)
        - 'suggested_action' (Actionable advice, e.g., "Do not share.")
        """
        try:
            # Check if it's a GCS URI or local file
            if file_path.startswith("gs://"):
                # Use URI directly for Gemini
                media_file = {"mime_type": mime_type, "file_uri": file_path}
                response = self.flash_model.generate_content([media_file, prompt], safety_settings=self.safety_settings)
            else:
                # Upload the local file to Gemini's API
                media_file = genai.upload_file(path=file_path, mime_type=mime_type)
                response = self.flash_model.generate_content([media_file, prompt], safety_settings=self.safety_settings)
                # Clean up the file from Gemini storage
                genai.delete_file(media_file.name)
            
            return json.loads(response.text)
        except Exception as e:
            if "safety" in str(e).lower() or "blocked" in str(e).lower():
                return {"verdict": "Toxic", "flags": ["blocked_by_safety_filter"], "error": "Blocked by API safety filters"}
            return {"error": str(e), "raw_response": getattr(response, 'text', '') if 'response' in locals() else ''}

llm_client = GeminiClient()
