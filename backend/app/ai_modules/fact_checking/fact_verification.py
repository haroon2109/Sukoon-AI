import os
from typing import List, Tuple, Optional, Dict, Any
from app.domain.schemas.schemas import ExtractedClaim, RetrievedEvidence, VerdictCategory, RecommendedAction, FactVerificationOutput
from google import genai

class FactVerificationAgent:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key) if api_key else genai.Client()

    async def verify(self, claims: List[ExtractedClaim], evidence: List[RetrievedEvidence]) -> Dict[str, Any]:
        """
        Autonomous agent that evaluates claims against retrieved evidence using Gemini.
        
        Returns:
            Dictionary containing fields for the Explainable AI Report.
        """
        claims_text = "\n".join([f"- {c.claim_text}" for c in claims])
        evidence_text = "\n".join([f"Source: {e.source_url}\n{e.content}" for e in evidence])
        
        prompt = f"""You are a Fact-Checking and Moderation Assistant.
Please evaluate the following claims based on the provided evidence.

Claims:
{claims_text}

Evidence:
{evidence_text}

Generate a comprehensive Explainable AI Report tailored for platform moderators.
CRITICAL INSTRUCTION: You MUST populate the `citations` array. For every factual assertion you make in your synthesis, you must provide an exact `direct_quote` from the provided Evidence and include the matching `source_url`. Do not hallucinate or invent sources.
"""

        response = await self.client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': FactVerificationOutput,
            }
        )
        
        if response.parsed:
            return response.parsed.model_dump()
            
        return {
            "summary_for_moderator": "Error generating report.",
            "verdict_category": VerdictCategory.UNVERIFIED_RUMOR,
            "recommended_action": RecommendedAction.NO_ACTION,
            "confidence_score": 0.0,
            "evidence_synthesis": "Failed to parse LLM response.",
            "counter_narrative_suggestion": None
        }
