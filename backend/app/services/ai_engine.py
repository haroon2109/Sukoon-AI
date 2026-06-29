import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Initialize the official Gen AI client using your existing AI Studio Key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Strict system instructions to enforce neutral, unbiased community peace analysis
SUKOON_PERSONA = (
    "You are a reasoning engine and fact verification assistant.\n"
    "Your task is NOT to guess. You MUST evaluate the claim based ONLY on the provided CONTEXT BLOCKS.\n"
    "Do not use outside knowledge. Do not use Google Search.\n"
    "Possible verdicts:\n"
    "1. 🟢 Verified\n"
    "2. 🟡 Needs Context\n"
    "3. 🟠 Misleading\n"
    "4. 🔴 False\n"
    "5. ⚪ Unable to Verify\n\n"
    "If the evidence clearly supports the claim, return 🟢 Verified.\n"
    "If the evidence contradicts it, return 🔴 False.\n"
    "If the evidence requires more context to be accurate, return 🟡 Needs Context.\n"
    "If the claim is deceptive, return 🟠 Misleading.\n"
    "If evidence is insufficient, return ⚪ Unable to Verify.\n\n"
    "Never invent facts.\n"
    "Never assume political intent.\n"
    "Remain neutral.\n\n"
    "CRITICAL: You MUST respond ONLY with a valid JSON object. Do not include any other text. "
    "Use the following schema:\n"
    "{\n"
    "  \"verdict\": \"🟢 Verified\" | \"🟡 Needs Context\" | \"🟠 Misleading\" | \"🔴 False\" | \"⚪ Unable to Verify\",\n"
    "  \"confidence_score\": <float>,\n"
    "  \"explanation\": \"<string>\"\n"
    "}"
)

async def verify_multimodal_content(text_content: str = None, media_bytes: bytes = None, mime_type: str = None, retrieved_context: str = "") -> dict:
    try:
        # 1. Base prompt construction
        contents = []
        
        if retrieved_context:
            contents.append(f"CONTEXT BLOCKS:\n{retrieved_context}\n\nCLAIM TO VERIFY:\n")
        
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

        # 2. Configure for pure reasoning (No Google Search Tool)
        config = types.GenerateContentConfig(
            system_instruction=SUKOON_PERSONA,
            temperature=0.0,
            response_mime_type="application/json"
        )
        
        # gemini-2.5-flash handles mixed media inputs seamlessly
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=config
        )
                        
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        structured_data = json.loads(raw_text.strip())
            
        return {
            "status": "success",
            "data": structured_data
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
