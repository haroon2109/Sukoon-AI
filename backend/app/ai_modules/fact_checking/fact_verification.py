import logging
from typing import List, Tuple, Optional, Dict, Any
from app.domain.schemas.schemas import ExtractedClaim, RetrievedEvidence, VerdictCategory, RecommendedAction, FactVerificationOutput
from app.providers.reasoning_provider import ProviderFactory

logger = logging.getLogger(__name__)

class FactVerificationAgent:
    def __init__(self):
        pass

    async def verify(self, claims: List[ExtractedClaim], evidence: List[RetrievedEvidence]) -> Dict[str, Any]:
        """
        Autonomous agent that evaluates claims against retrieved evidence using the ReasoningProvider.
        
        Returns:
            Dictionary containing fields for the Explainable AI Report.
        """
        claims_text = "\n".join([f"- {c.claim_text}" for c in claims])
        # Include credibility score if available, otherwise just use URL
        evidence_text = "\n".join([f"Source: {e.source_url} (Credibility: {getattr(e, 'credibility_score', 'Unknown')})\n{e.content}" for e in evidence])
        
        schema_format = (
            '{\n'
            '  "summary_for_moderator": "string",\n'
            '  "verdict_category": "VERIFIED_TRUE | UNVERIFIED_RUMOR | FALSE_MISLEADING",\n'
            '  "recommended_action": "NO_ACTION | ADD_CONTEXT_LABEL | REMOVE_CONTENT",\n'
            '  "confidence_score": float,\n'
            '  "evidence_synthesis": "string",\n'
            '  "counter_narrative_suggestion": "string or null",\n'
            '  "citations": [{"source_url": "string", "direct_quote": "string"}]\n'
            '}'
        )

        system_instruction = f"""You are a Fact-Checking and Moderation Assistant.
Generate a comprehensive Explainable AI Report tailored for platform moderators.
CRITICAL INSTRUCTION: You MUST populate the `citations` array. For every factual assertion you make in your synthesis, you must provide an exact `direct_quote` from the provided Evidence and include the matching `source_url`. Do not hallucinate or invent sources.

Source Credibility Weights (incorporate these into your reasoning and confidence score):
Government = 100, WHO = 98, Reuters = 97, AP = 96, BBC = 94, Wikipedia = 80, Unknown Blog = 30, Random Social Media = 10.

Respond ONLY with a valid JSON object matching this schema exactly:
{schema_format}
"""

        prompt = f"Please evaluate the following claims based on the provided evidence.\n\nClaims:\n{claims_text}\n\nEvidence:\n{evidence_text}"

        try:
            provider = ProviderFactory.get_provider()
            result = await provider.generate_json(prompt, system_instruction=system_instruction)
            
            if "error" in result:
                logger.error(f"Error from provider during fact verification: {result['error']}")
                return self._error_response(f"API Error: {result['error']}")
                
            validated = FactVerificationOutput(**result)
            return validated.model_dump()
            
        except Exception as e:
            logger.error(f"Error in FactVerificationAgent: {e}")
            return self._error_response(f"Failed to parse LLM response: {e}")
            
    def _error_response(self, synthesis: str) -> Dict[str, Any]:
        return {
            "summary_for_moderator": "Error generating report.",
            "verdict_category": VerdictCategory.UNVERIFIED_RUMOR,
            "recommended_action": RecommendedAction.NO_ACTION,
            "confidence_score": 0.0,
            "evidence_synthesis": synthesis,
            "counter_narrative_suggestion": None,
            "citations": []
        }
