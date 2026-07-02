import os
from typing import List
from app.domain.schemas.schemas import ExtractedClaim, ExtractedClaimsList
from google import genai

class ClaimExtractionAgent:
    def __init__(self):
        # Initialize standard Gemini client
        api_key = os.environ.get("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key) if api_key else genai.Client()

    async def extract(self, text: str) -> List[ExtractedClaim]:
        """
        Autonomous agent that uses Gemini to identify and extract verifiable claims from raw text.
        """
        if not text.strip():
            return []
            
        prompt = f"Extract all distinct, verifiable claims from the following text. Provide the claim text and a brief context for each.\n\nText:\n{text}"
        
        response = await self.client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': ExtractedClaimsList,
            }
        )
        
        if response.parsed:
            return response.parsed.claims
        return []
