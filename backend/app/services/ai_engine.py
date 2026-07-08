import os
import json
import logging
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from app.providers.reasoning_provider import ProviderFactory

load_dotenv()
logger = logging.getLogger(__name__)

class VerificationSchema(BaseModel):
    verdict: str = Field(description="Must be exactly one of: '🟢 Verified', '🟡 Needs Context', '🟠 Misleading', '🔴 False', '⚪ Unable to Verify'")
    confidence_score: float = Field(description="A confidence score between 0.0 and 100.0 based on the provided evidence")
    explanation: str = Field(description="A concise, neutral, and scientific explanation of why this verdict was reached, citing specific details from the text or media")

SUKOON_PERSONA = (
    "You are the core logic engine of Sukoon AI, an advanced fact-checking and responsible AI verification platform.\n"
    "Your objective is to evaluate incoming claims and retrieved database context (RAG) to determine objective truth.\n\n"
    "RULES FOR EVALUATION:\n"
    "1. You must cross-reference the CLAIM against the 'CONTEXT BLOCKS' provided.\n"
    "2. If the claim matches the context or is objectively true, respond with '🟢 Verified'.\n"
    "3. If the claim is demonstrably false, fabricated, or biased, respond with '🔴 False'.\n"
    "4. If the claim twists facts or removes critical nuance, respond with '🟠 Misleading'.\n"
    "5. If there is no evidence either way, respond with '⚪ Unable to Verify'.\n\n"
    "Provide a strict confidence score (0-100) reflecting the quality of the evidence, and a highly analytical, clinical explanation.\n"
    "You must return your output precisely in the requested JSON structure matching this schema:\n"
    '{"verdict": "string", "confidence_score": float, "explanation": "string"}'
)

async def _call_freellm_json(prompt: str) -> dict:
    provider = ProviderFactory.get_provider()
    result = await provider.generate_json(prompt, system_instruction=SUKOON_PERSONA)
    if "error" in result:
        return {
            "verdict": "⚪ Unable to Verify",
            "confidence_score": 0.0,
            "explanation": f"Failed to verify claim due to provider error: {result['error']}"
        }
    return result

async def verify_multimodal_content(text_content: str = None, media_bytes: bytes = None, mime_type: str = None, retrieved_context: str = "") -> dict:
    try:
        prompt = ""
        if retrieved_context:
            prompt += f"CONTEXT BLOCKS:\n{retrieved_context}\n\n"
            
        if media_bytes and mime_type and mime_type.startswith("image/"):
            # Route through vision_service if it's an image
            from .vision_service import vision_service
            media_desc = await vision_service.analyze_image(media_bytes, "Describe this media and extract any text.")
            prompt += f"MEDIA DESCRIPTION:\n{media_desc}\n\n"
            
        if text_content:
            prompt += f"CLAIM TO VERIFY:\n{text_content}"
        else:
            prompt += "CLAIM TO VERIFY:\nAnalyze the uploaded media for truth and potential hatred incitement based on its description."
            
        structured_data = await _call_freellm_json(prompt)
        
        return {
            "status": "success",
            "data": structured_data
        }
            
    except Exception as e:
        logger.error("AI Engine Verification Pipeline Failed", exc_info=True)
        return {"status": "error", "message": str(e)}
