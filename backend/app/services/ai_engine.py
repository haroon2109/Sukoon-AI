import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Initialize the official Gen AI client using your existing AI Studio Key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Strict system instructions to enforce neutral, unbiased community peace analysis
SUKOON_PERSONA = (
    "You are Sukoon AI, a strictly neutral, unbiased, and objective fact-checker. "
    "Your mandate is to verify factual truth and flag hate speech to promote community peace. "
    "You MUST use the Google Search tool to cross-reference claims against reputable global news "
    "and journalistic fact-checkers before giving a response. Do not use personal assumptions."
)

async def verify_multimodal_content(text_content: str = None, media_bytes: bytes = None, mime_type: str = None) -> dict:
    try:
        # 1. Base prompt construction
        contents = []
        
        # If media is uploaded (Image or Video bytes)
        if media_bytes and mime_type:
            contents.append(
                types.Part.from_bytes(
                    data=media_bytes,
                    mime_type=mime_type
                )
            )
            
        # Append the user's text description or URL string
        if text_content:
            contents.append(text_content)
        else:
            contents.append("Analyze this uploaded media for truth and potential hatred incitement.")

        # 2. Inject Google Search Tool Configuration
        config = types.GenerateContentConfig(
            system_instruction=SUKOON_PERSONA,
            tools=[types.Tool(google_search=types.GoogleSearch())],
            temperature=0.1
        )
        
        # gemini-2.5-flash handles mixed media inputs seamlessly
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=config
        )
        
        # 3. Extract grounding sources used to verify the truth
        sources = []
        if response.candidates:
            candidate = response.candidates[0]
            if getattr(candidate, 'grounding_metadata', None) and getattr(candidate.grounding_metadata, 'grounding_chunks', None):
                for chunk in candidate.grounding_metadata.grounding_chunks:
                    if getattr(chunk, 'web', None):
                        sources.append({
                            "title": getattr(chunk.web, 'title', 'Source'),
                            "url": getattr(chunk.web, 'uri', '')
                        })

        return {
            "status": "success",
            "verdict_analysis": response.text,
            "verified_sources": sources # Hands back real URLs to show the user/judges
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
