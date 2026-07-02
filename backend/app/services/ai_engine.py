import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from groq import Groq

load_dotenv()

# Initialize Google AI Studio Client (Multimodal)
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Groq Client (Fast Text)
groq_api_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=groq_api_key) if groq_api_key else None

# Define a strict Pydantic schema for the Truth Engine's output
class VerificationSchema(BaseModel):
    verdict: str = Field(description="Must be exactly one of: '🟢 Verified', '🟡 Needs Context', '🟠 Misleading', '🔴 False', '⚪ Unable to Verify'")
    confidence_score: float = Field(description="A confidence score between 0.0 and 100.0 based on the provided evidence")
    explanation: str = Field(description="A concise, neutral, and scientific explanation of why this verdict was reached, citing specific details from the text or media")

# Impartial, robust system prompt instructing the model to act as a logic-driven fact-checker
SUKOON_PERSONA = (
    "You are the core logic engine of Sukoon AI, an advanced fact-checking and responsible AI verification platform.\n"
    "Your objective is to evaluate incoming claims, multimodal media (images/video), and retrieved database context (RAG) to determine objective truth.\n\n"
    "RULES FOR EVALUATION:\n"
    "1. You must cross-reference the CLAIM against the provided CONTEXT BLOCKS (historical RAG data) or attached media.\n"
    "2. If the claim matches the context or is objectively true, respond with '🟢 Verified'.\n"
    "3. If the claim is demonstrably false, fabricated, or biased, respond with '🔴 False'.\n"
    "4. If the claim twists facts or removes critical nuance, respond with '🟠 Misleading'.\n"
    "5. If there is no evidence either way, respond with '⚪ Unable to Verify'.\n\n"
    "Provide a strict confidence score (0-100) reflecting the quality of the evidence, and a highly analytical, clinical explanation.\n"
    "You must return your output precisely in the requested JSON structure matching this schema:\n"
    '{"verdict": "string", "confidence_score": float, "explanation": "string"}'
)

async def verify_multimodal_content(text_content: str = None, media_bytes: bytes = None, mime_type: str = None, retrieved_context: str = "") -> dict:
    try:
        # Determine Routing: If media is attached, MUST use Gemini. If text-only, route to Groq (if configured).
        if not media_bytes and groq_client:
            return _route_to_groq_llama(text_content, retrieved_context)
        else:
            return _route_to_gemini_flash(text_content, media_bytes, mime_type, retrieved_context)
            
    except Exception as e:
        return {"status": "error", "message": str(e)}

def _route_to_groq_llama(text_content: str, retrieved_context: str) -> dict:
    """Uses Groq Llama 3.3 70B for blazing fast text verification (~300+ tokens/sec)"""
    prompt = ""
    if retrieved_context:
        prompt += f"CONTEXT BLOCKS:\n{retrieved_context}\n\n"
    prompt += f"CLAIM TO VERIFY:\n{text_content}"
    
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SUKOON_PERSONA},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        response_format={"type": "json_object"},
    )
    
    raw_json = response.choices[0].message.content
    structured_data = json.loads(raw_json)
    
    return {
        "status": "success",
        "data": structured_data
    }

def _route_to_gemini_flash(text_content: str, media_bytes: bytes, mime_type: str, retrieved_context: str) -> dict:
    """Uses Google AI Studio Gemini 2.5 Flash for Multimodal analysis"""
    contents = []
    
    if retrieved_context:
        contents.append(f"CONTEXT BLOCKS:\n{retrieved_context}\n\nCLAIM TO VERIFY:\n")
    
    if media_bytes and mime_type:
        contents.append(types.Part.from_bytes(data=media_bytes, mime_type=mime_type))
        
    if text_content:
        contents.append(text_content)
    else:
        contents.append("Analyze this uploaded media for truth and potential hatred incitement.")

    config = types.GenerateContentConfig(
        system_instruction=SUKOON_PERSONA,
        temperature=0.0,
        response_mime_type="application/json",
        response_schema=VerificationSchema,
    )
    
    response = gemini_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=contents,
        config=config
    )
                    
    raw_text = response.text.strip()
    structured_data = json.loads(raw_text)
        
    return {
        "status": "success",
        "data": structured_data
    }
