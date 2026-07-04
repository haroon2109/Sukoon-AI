from pydantic import BaseModel, Field
from typing import Optional
import json
import os
from google import genai
from google.genai import types

class ExtractedClaim(BaseModel):
    claim: str = Field(description="The core, testable assertion being made in the text.")
    location: Optional[str] = Field(description="The geographical location mentioned, if any.", default=None)
    date: Optional[str] = Field(description="The date or timeframe mentioned, if any.", default=None)
    confidence: float = Field(description="Confidence score of the extraction between 0.0 and 1.0.")

async def extract_claim_from_text(raw_text: str) -> str:
    """
    Takes raw noisy text (or OCR text) and extracts the core claim using Gemini.
    """
    from app.core.config import settings
    if not settings.GEMINI_API_KEY:
        return raw_text.strip()
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    persona = (
        "You are a Claim Extraction Agent.\n"
        "Your job is to read noisy user input and extract ONLY the core, testable assertion.\n"
        "Ignore conversational filler, greetings, or panic.\n"
        "Output the claim as a single clean sentence. Do not output anything else."
    )
    
    config = types.GenerateContentConfig(
        system_instruction=persona,
        temperature=0.0
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash-8b',
            contents=[raw_text],
            config=config
        )
        return response.text.strip()
    except Exception as e:
        # Fallback to returning the raw text if extraction fails
        return raw_text.strip()


class ClaimExtractorAgent:
    async def extract(self, text: str) -> dict:
        """
        Wrapper to match the SupervisorAgent expectation.
        Returns a dict with 'claim' key.
        """
        claim_text = await extract_claim_from_text(text)
        return {"claim": claim_text}

