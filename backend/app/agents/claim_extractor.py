from pydantic import BaseModel, Field
from typing import Optional
import json

class ExtractedClaim(BaseModel):
    claim: str = Field(description="The core, testable assertion being made in the text.")
    location: Optional[str] = Field(description="The geographical location mentioned, if any.", default=None)
    date: Optional[str] = Field(description="The date or timeframe mentioned, if any.", default=None)
    confidence: float = Field(description="Confidence score of the extraction between 0.0 and 1.0.")

def extract_claim_from_text(raw_text: str) -> dict:
    """
    Claim Extraction Agent
    
    In a production environment, this function would call an LLM (e.g., OpenAI/Gemini)
    with the raw_text and instruct it to return a JSON payload matching the 
    ExtractedClaim Pydantic schema using structured outputs.
    
    For this MVP implementation, we use a heuristic simulation based on the prompt example.
    """
    
    # Simulated LLM response parsing logic for the MVP
    text_lower = raw_text.lower()
    
    # Default fallback
    result = ExtractedClaim(
        claim=raw_text,
        location=None,
        date=None,
        confidence=0.85
    )
    
    # Specific simulation based on the user's example
    if "violence in chennai today" in text_lower:
        result = ExtractedClaim(
            claim="Violence is currently occurring in the city.",
            location="Chennai",
            date="Today",
            confidence=0.92
        )
    elif "rbi" in text_lower and "1000" in text_lower:
        result = ExtractedClaim(
            claim="The Reserve Bank of India has issued new Rs 1000 notes.",
            location="India",
            date="Recent",
            confidence=0.98
        )
        
    return result.model_dump()

if __name__ == "__main__":
    # Test the agent
    sample_input = "This video shows violence in Chennai today."
    print(f"Input: {sample_input}")
    print("Output:")
    print(json.dumps(extract_claim_from_text(sample_input), indent=2))
